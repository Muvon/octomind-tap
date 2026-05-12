"""Fine-tune a cross-encoder reranker on hard-negative triplets.

Base: `cross-encoder/ms-marco-MiniLM-L-6-v2` — 22M params, 6-layer MiniLM,
natively trained as a cross-encoder on MS-MARCO. Loads cleanly into the
standard `BertForSequenceClassification` head and is blazing fast on CPU.

Loss: `MultipleNegativesRankingLoss` — CONTRASTIVE/RANKING objective.

Critical detail: an earlier version used `BinaryCrossEntropyLoss`
(pointwise classification: "is this pair relevant? yes/no") and produced
held-out AP 0.98 BUT broke at runtime — when fed five plausible-looking
capability triggers, the model output near-identical high scores for all
five and got the top-1 wrong. The eval metric measured binary
classification, not ranking under competition. The runtime task IS
ranking, so we need a ranking loss.

`MultipleNegativesRankingLoss` (CE variant) optimizes:

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
from sentence_transformers.cross_encoder.losses import MultipleNegativesRankingLoss

warnings.filterwarnings("ignore", category=FutureWarning)


def load_triplet_rows(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            rows.append((r["anchor"], r["positive"], r["negative"]))
    return rows


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
