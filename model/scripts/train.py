"""Fine-tune BGE-small on (anchor, positive) pairs and (anchor, positive,
negative) triplets.

Two MNRL objectives combined:

  - pairs.jsonl    → in-batch negatives only.
  - triplets.jsonl → in-batch negatives + one explicit HARD negative per row.

Both contribute gradient; the triplet objective is what teaches the model
to separate confusable clusters (e.g. shell vs programming-rust).
"""

from __future__ import annotations

import argparse
import json
import random
import warnings
from datetime import datetime
from pathlib import Path

import torch
import yaml
from sentence_transformers import InputExample, SentenceTransformer
from sentence_transformers.losses import MultipleNegativesRankingLoss
from torch.utils.data import DataLoader

warnings.filterwarnings("ignore", category=FutureWarning)


def load_pairs(path: Path) -> list[InputExample]:
    out: list[InputExample] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.append(InputExample(texts=[row["anchor"], row["positive"]]))
    return out


def load_triplets(path: Path) -> list[InputExample]:
    out: list[InputExample] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.append(InputExample(texts=[row["anchor"], row["positive"], row["negative"]]))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    train_cfg = cfg["train"]
    data_cfg = cfg["data"]

    root = Path(__file__).resolve().parents[1]
    pairs_path = root / data_cfg["pairs_path"]
    triplets_path = pairs_path.with_name("triplets.jsonl")
    if not pairs_path.exists():
        raise SystemExit(f"missing {pairs_path}; run build_dataset.py first")

    random.seed(train_cfg["seed"])

    pairs = load_pairs(pairs_path)
    random.shuffle(pairs)
    print(f"loaded {len(pairs)} pair examples from {pairs_path.name}")

    triplets: list[InputExample] = []
    if triplets_path.exists():
        triplets = load_triplets(triplets_path)
        random.shuffle(triplets)
        print(f"loaded {len(triplets)} triplet examples from {triplets_path.name}")
    else:
        print(f"no triplets at {triplets_path}; training on pairs only")

    model = SentenceTransformer(cfg["base_model"])
    model.max_seq_length = train_cfg["max_seq_length"]

    pin_memory = torch.cuda.is_available()
    pair_loader = DataLoader(
        pairs, shuffle=True, batch_size=train_cfg["batch_size"], drop_last=True, pin_memory=pin_memory
    )
    pair_loss = MultipleNegativesRankingLoss(model)
    objectives = [(pair_loader, pair_loss)]

    if triplets:
        trip_loader = DataLoader(
            triplets,
            shuffle=True,
            batch_size=max(8, train_cfg["batch_size"] // 2),
            drop_last=True,
            pin_memory=pin_memory,
        )
        trip_loss = MultipleNegativesRankingLoss(model)
        objectives.append((trip_loader, trip_loss))

    steps_per_epoch = max(len(loader) for loader, _ in objectives)
    warmup_steps = int(steps_per_epoch * train_cfg["epochs"] * train_cfg["warmup_ratio"])

    run_name = cfg["run_name"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"training {len(objectives)} objective(s) for {train_cfg['epochs']} epochs")
    model.fit(
        train_objectives=objectives,
        epochs=train_cfg["epochs"],
        warmup_steps=warmup_steps,
        optimizer_params={"lr": train_cfg["learning_rate"]},
        weight_decay=train_cfg["weight_decay"],
        output_path=str(out_dir),
        show_progress_bar=True,
    )

    (out_dir / "train_config.yaml").write_text(yaml.safe_dump(cfg))
    print(f"saved fine-tuned embedding model to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
