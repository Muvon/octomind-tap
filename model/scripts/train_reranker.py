"""Fine-tune a cross-encoder reranker on hard-negative triplets.

Base: `jinaai/jina-reranker-v1-turbo-en` (33M, English-only, fastembed-ready).

Loss: `BinaryCrossEntropyLoss`. Each triplet (anchor, positive, negative)
produces TWO training rows:

  (anchor, positive)  → label 1
  (anchor, negative)  → label 0

A CEBinaryClassificationEvaluator runs each epoch on a held-out 10%
split of the same triplets. We save only the checkpoint with the
highest average precision (AP) — cross-encoders, like bi-encoders,
can drift past the optimum after 2-3 epochs.
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
from sentence_transformers import InputExample
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.evaluation import CEBinaryClassificationEvaluator
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss
from torch.utils.data import DataLoader

warnings.filterwarnings("ignore", category=FutureWarning)


def load_triplet_rows(path: Path) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            rows.append((r["anchor"], r["positive"], r["negative"]))
    return rows


def to_examples(rows: list[tuple[str, str, str]]) -> list[InputExample]:
    out: list[InputExample] = []
    for a, p, n in rows:
        out.append(InputExample(texts=[a, p], label=1.0))
        out.append(InputExample(texts=[a, n], label=0.0))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "reranker.yaml")
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

    train_examples = to_examples(train_rows)
    eval_sentence_pairs: list[list[str]] = []
    eval_labels: list[int] = []
    for a, p, n in eval_rows:
        eval_sentence_pairs.append([a, p])
        eval_labels.append(1)
        eval_sentence_pairs.append([a, n])
        eval_labels.append(0)

    model = CrossEncoder(cfg["base_model"], num_labels=1, max_length=train_cfg["max_seq_length"])

    loader = DataLoader(train_examples, shuffle=True, batch_size=train_cfg["batch_size"], drop_last=True)
    loss = BinaryCrossEntropyLoss(model)

    evaluator = CEBinaryClassificationEvaluator(
        sentence_pairs=eval_sentence_pairs,
        labels=eval_labels,
        name="rerank-holdout",
        show_progress_bar=False,
    )

    steps_per_epoch = len(loader)
    warmup_steps = int(steps_per_epoch * train_cfg["epochs"] * train_cfg["warmup_ratio"])
    evaluation_steps = int(train_cfg.get("evaluation_steps", 0)) or steps_per_epoch

    use_amp = bool(train_cfg.get("use_amp", False)) and torch.cuda.is_available()
    if use_amp:
        print("mixed precision (FP16): enabled (CUDA detected)")

    run_name = cfg["run_name"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"training cross-encoder for {train_cfg['epochs']} epochs (batch={train_cfg['batch_size']})")
    print(f"evaluation every {evaluation_steps} steps; save_best_model={train_cfg.get('save_best_model', True)}")

    model.fit(
        train_dataloader=loader,
        loss_fct=loss,
        evaluator=evaluator,
        evaluation_steps=evaluation_steps,
        epochs=train_cfg["epochs"],
        warmup_steps=warmup_steps,
        optimizer_params={"lr": train_cfg["learning_rate"]},
        weight_decay=train_cfg["weight_decay"],
        output_path=str(out_dir),
        save_best_model=bool(train_cfg.get("save_best_model", True)),
        use_amp=use_amp,
        show_progress_bar=True,
    )

    (out_dir / "train_config.yaml").write_text(yaml.safe_dump(cfg))
    print(f"saved fine-tuned reranker to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
