"""Fine-tune a cross-encoder reranker on hard-negative triplets.

Base: `jinaai/jina-reranker-v1-turbo-en` (33M, English-only, fastembed-ready).

Loss: `BinaryCrossEntropyLoss` over (query, document) pairs. Each triplet
(anchor, positive, negative) produces TWO training rows:

  (anchor, positive)  → label 1
  (anchor, negative)  → label 0

The cross-encoder reads each (q, d) pair as one sequence with full self-
attention. This is what teaches it to discriminate clusters that look
generic-similar to the bi-encoder (shell vs programming-rust collision).
"""

from __future__ import annotations

import argparse
import json
import random
import warnings
from datetime import datetime
from pathlib import Path

import yaml
from sentence_transformers import InputExample
from sentence_transformers.cross_encoder import CrossEncoder
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss
from torch.utils.data import DataLoader

warnings.filterwarnings("ignore", category=FutureWarning)


def load_triplets(path: Path) -> list[InputExample]:
    out: list[InputExample] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.append(InputExample(texts=[row["anchor"], row["positive"]], label=1.0))
            out.append(InputExample(texts=[row["anchor"], row["negative"]], label=0.0))
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
    examples = load_triplets(triplets_path)
    random.shuffle(examples)
    print(f"loaded {len(examples)} (q, d, label) rows from {triplets_path.name}")

    model = CrossEncoder(cfg["base_model"], num_labels=1, max_length=train_cfg["max_seq_length"])

    loader = DataLoader(examples, shuffle=True, batch_size=train_cfg["batch_size"], drop_last=True)
    loss = BinaryCrossEntropyLoss(model)

    steps_per_epoch = len(loader)
    warmup_steps = int(steps_per_epoch * train_cfg["epochs"] * train_cfg["warmup_ratio"])

    run_name = cfg["run_name"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"training cross-encoder for {train_cfg['epochs']} epochs (batch={train_cfg['batch_size']})")
    model.fit(
        train_dataloader=loader,
        loss_fct=loss,
        epochs=train_cfg["epochs"],
        warmup_steps=warmup_steps,
        optimizer_params={"lr": train_cfg["learning_rate"]},
        weight_decay=train_cfg["weight_decay"],
        output_path=str(out_dir),
        show_progress_bar=True,
    )

    (out_dir / "train_config.yaml").write_text(yaml.safe_dump(cfg))
    print(f"saved fine-tuned reranker to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
