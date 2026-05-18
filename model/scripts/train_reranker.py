"""Fine-tune a cross-encoder reranker on hard-negative triplets.

Base: `cross-encoder/ms-marco-MiniLM-L-6-v2` — 22M params, 6-layer MiniLM,
natively trained as a cross-encoder on MS-MARCO. Loads cleanly into the
standard `BertForSequenceClassification` head and is blazing fast on CPU.

Loss: `CachedMultipleNegativesRankingLoss` — CONTRASTIVE/RANKING objective
with GradCache so the effective in-batch-negatives count is much larger
than what fits in VRAM in a single forward pass. More competing negatives
per anchor = sharper top-1 vs top-2 separation, which is exactly the
runtime metric (margin gate over the bi-encoder's top-N candidates).

Critical detail: an earlier version used `BinaryCrossEntropyLoss`
(pointwise classification: "is this pair relevant? yes/no") and produced
held-out AP 0.98 BUT broke at runtime — when fed five plausible-looking
capability triggers, the model output near-identical high scores for all
five and got the top-1 wrong. The eval metric measured binary
classification, not ranking under competition. The runtime task IS
ranking, so we need a ranking loss.

`(Cached)MultipleNegativesRankingLoss` (CE variant) optimizes:

  score(anchor, positive) > score(anchor, every_other_doc_in_batch)

via softmax + cross-entropy. With our triplets (anchor, positive,
hard_negative), the explicit negative is also stacked in alongside the
in-batch negatives. This is the same pattern used for production
rerankers (e.g. BGE-reranker, Cohere rerank).

Dataset columns for CE MNRL: `query`, `positive`, optionally `negative`.
No `label` column — the loss is fully contrastive.

A `CrossEncoderClassificationEvaluator` still runs each epoch on a 10%
triplet split for sanity-check binary AP, but the model is now actually
trained to RANK.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import warnings
from datetime import datetime
from pathlib import Path

import torch
import yaml
from datasets import Dataset
from sentence_transformers.cross_encoder import (
    CrossEncoder,
    CrossEncoderTrainer,
    CrossEncoderTrainingArguments,
)
from sentence_transformers.cross_encoder.evaluation import (
    CrossEncoderClassificationEvaluator,
)
from sentence_transformers.cross_encoder.losses import (
    CachedMultipleNegativesRankingLoss,
    MultipleNegativesRankingLoss,
)

warnings.filterwarnings("ignore", category=FutureWarning)


def load_triplet_rows(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            rows.append((r["anchor"], r["positive"], r["negative"]))
    return rows


def _reset_classifier_head(cross_encoder: CrossEncoder) -> None:
    """Reinitialize the model's classification head, leaving the encoder
    backbone untouched.

    Handles both architectures we use:
      - BERT (`BertForSequenceClassification`): `classifier` is a single
        `nn.Linear(hidden, num_labels)`.
      - XLM-RoBERTa (`XLMRobertaForSequenceClassification`): `classifier`
        is `XLMRobertaClassificationHead` with `.dense` + `.out_proj` linears.
    """
    import torch.nn as nn

    hf_model = cross_encoder.model
    classifier = getattr(hf_model, "classifier", None)
    if classifier is None:
        raise RuntimeError(
            "could not find `.classifier` attribute on the loaded model — "
            "head reset not supported for this architecture"
        )

    reset_targets: list[nn.Linear] = []
    if isinstance(classifier, nn.Linear):
        reset_targets.append(classifier)
    else:
        # XLM-RoBERTa-style head: dense + out_proj
        for name in ("dense", "out_proj"):
            sub = getattr(classifier, name, None)
            if isinstance(sub, nn.Linear):
                reset_targets.append(sub)

    if not reset_targets:
        raise RuntimeError(
            f"classifier head shape unrecognized: {type(classifier).__name__} — "
            "head reset not supported"
        )

    for lin in reset_targets:
        nn.init.normal_(lin.weight, std=0.02)
        if lin.bias is not None:
            nn.init.zeros_(lin.bias)

    print(f"classifier head reset ({len(reset_targets)} linear layer(s)) — training from scratch on the head")


def rows_to_dataset(rows: list[tuple[str, str, str]]) -> Dataset:
    """One row per triplet: anchor / positive / negative.

    MultipleNegativesRankingLoss reads:
      - column 0 (`query`): the anchor
      - column 1 (`positive`): the matching doc
      - column 2+ (optional): explicit hard negatives, used IN ADDITION TO
        in-batch negatives. Each row's positives become other rows' negatives
        automatically via batch construction.
    No `label` column — the loss is contrastive softmax/cross-entropy.
    """
    queries: list[str] = []
    positives: list[str] = []
    negatives: list[str] = []
    for a, p, n in rows:
        queries.append(a)
        positives.append(p)
        negatives.append(n)
    return Dataset.from_dict({"query": queries, "positive": positives, "negative": negatives})


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "reranker.yaml",
    )
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    train_cfg = cfg["train"]

    root = Path(__file__).resolve().parents[1]
    triplets_path = root / cfg["data"]["triplets_path"]
    if not triplets_path.exists():
        raise SystemExit(f"missing {triplets_path}; run build_dataset.py first")

    random.seed(train_cfg["seed"])
    torch.manual_seed(train_cfg["seed"])

    rows = load_triplet_rows(triplets_path)
    random.shuffle(rows)
    print(f"loaded {len(rows)} triplets from {triplets_path.name}")

    n_eval = max(1, math.floor(len(rows) * 0.1))
    eval_rows = rows[:n_eval]
    train_rows = rows[n_eval:]
    print(f"split: train={len(train_rows)} triplets, eval={len(eval_rows)} triplets")

    train_ds = rows_to_dataset(train_rows)

    eval_pairs: list[list[str]] = []
    eval_labels: list[int] = []
    for a, p, n in eval_rows:
        eval_pairs.append([a, p]); eval_labels.append(1)
        eval_pairs.append([a, n]); eval_labels.append(0)

    model = CrossEncoder(
        cfg["base_model"],
        num_labels=1,
        max_length=train_cfg["max_seq_length"],
    )

    # Optionally reset the pre-trained classifier head before training.
    # MS-MARCO cross-encoders ship with a saturated head — any plausibly-
    # relevant pair scores ≈ +9 logit — and a few epochs of fine-tuning
    # cannot break that calibration. Resetting wipes the head so the model
    # has to learn discrimination from scratch on our domain. The encoder
    # backbone stays intact, so we still benefit from MS-MARCO pre-training.
    if cfg.get("reset_classifier_head", False):
        _reset_classifier_head(model)

    # Pick the cached vs uncached variant based on config. Cached gets us
    # bigger effective batches at the same VRAM by using GradCache: a no-
    # grad first pass populates the similarity matrix, then a second pass
    # with gradients only fills in the cells we actually backprop through.
    # Falls back to the legacy in-memory MNRL if `cached: false` is set
    # in the YAML (diagnostic only — cached is the production recipe).
    use_cached = bool(cfg.get("loss", {}).get("cached", True))
    if use_cached:
        mini_batch_size = int(train_cfg.get("mini_batch_size", 32))
        num_negatives = int(cfg.get("loss", {}).get("num_negatives", 4))
        print(
            f"loss: CachedMultipleNegativesRankingLoss "
            f"(num_negatives={num_negatives})"
        )
        loss = CachedMultipleNegativesRankingLoss(
            model,
            num_negatives=num_negatives,
            mini_batch_size=mini_batch_size,
        )
    else:
        print("loss: MultipleNegativesRankingLoss (legacy, no caching)")
        loss = MultipleNegativesRankingLoss(model)

    evaluator = CrossEncoderClassificationEvaluator(
        sentence_pairs=eval_pairs,
        labels=eval_labels,
        name="rerank-holdout",
        show_progress_bar=False,
    )

    use_fp16 = bool(train_cfg.get("use_amp", False)) and torch.cuda.is_available()
    if use_fp16:
        print("mixed precision (FP16): enabled (CUDA detected)")

    run_name = cfg["run_name"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    targs = CrossEncoderTrainingArguments(
        output_dir=str(out_dir),
        num_train_epochs=train_cfg["epochs"],
        per_device_train_batch_size=train_cfg["batch_size"],
        per_device_eval_batch_size=train_cfg["batch_size"],
        learning_rate=train_cfg["learning_rate"],
        warmup_ratio=train_cfg["warmup_ratio"],
        weight_decay=train_cfg["weight_decay"],
        fp16=use_fp16,
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=bool(train_cfg.get("save_best_model", True)),
        metric_for_best_model="eval_rerank-holdout_average_precision",
        greater_is_better=True,
        logging_steps=50,
        report_to=[],
        seed=train_cfg["seed"],
        dataloader_pin_memory=torch.cuda.is_available(),
    )

    trainer = CrossEncoderTrainer(
        model=model,
        args=targs,
        train_dataset=train_ds,
        loss=loss,
        evaluator=evaluator,
    )

    print(f"training cross-encoder for {train_cfg['epochs']} epochs (batch={train_cfg['batch_size']})")
    trainer.train()
    trainer.save_model(str(out_dir))

    (out_dir / "train_config.yaml").write_text(yaml.safe_dump(cfg))
    print(f"saved fine-tuned reranker to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
