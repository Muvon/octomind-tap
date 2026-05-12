"""Fine-tune BGE-small on (anchor, positive) pairs and (anchor, positive,
negative) triplets.

Two MNRL objectives combined:

  - pairs.jsonl    → in-batch negatives only.
  - triplets.jsonl → in-batch negatives + one explicit HARD negative per row.

An InformationRetrievalEvaluator runs each epoch on holdout intents and
the script saves ONLY the checkpoint with the highest MRR@10. MNRL
converges fast on small label spaces; without best-checkpoint selection
later epochs frequently drift past the optimum.
"""

from __future__ import annotations

import argparse
import json
import random
import warnings
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import torch
import yaml
from sentence_transformers import InputExample, SentenceTransformer

# v3+ relocated losses/evaluation under `sentence_transformer.{losses,evaluation}`;
# older versions re-export at the package top. Try the new paths first to avoid
# deprecation warnings, fall back for compatibility.
try:
    from sentence_transformers.sentence_transformer.losses import MultipleNegativesRankingLoss
except ImportError:
    from sentence_transformers.losses import MultipleNegativesRankingLoss

try:
    from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator
except ImportError:
    from sentence_transformers.evaluation import InformationRetrievalEvaluator
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


def build_ir_evaluator(
    pairs_path: Path,
    holdout_path: Path,
    name: str,
) -> InformationRetrievalEvaluator | None:
    """Build a retrieval evaluator from holdout intents + training triggers.

    queries       : every holdout intent
    corpus        : every training trigger / paraphrase
    relevant_docs : doc ids whose label matches the query's label
    """
    if not holdout_path.exists():
        return None

    # Collect every distinct training trigger and group by label.
    label_to_docs: dict[str, set[str]] = defaultdict(set)
    with pairs_path.open() as f:
        for line in f:
            row = json.loads(line)
            label_to_docs[row["label"]].add(row["anchor"])
            label_to_docs[row["label"]].add(row["positive"])

    corpus: dict[str, str] = {}
    doc_id_by_text: dict[str, str] = {}
    for label, docs in label_to_docs.items():
        for d in docs:
            if d in doc_id_by_text:
                continue
            did = f"d{len(corpus)}"
            corpus[did] = d
            doc_id_by_text[d] = did

    label_to_doc_ids: dict[str, set[str]] = {
        label: {doc_id_by_text[d] for d in docs} for label, docs in label_to_docs.items()
    }

    queries: dict[str, str] = {}
    relevant_docs: dict[str, set[str]] = {}
    with holdout_path.open() as f:
        for line in f:
            row = json.loads(line)
            qid = f"q{len(queries)}"
            queries[qid] = row["intent"]
            relevant_docs[qid] = label_to_doc_ids.get(row["label"], set())

    if not queries or not corpus:
        return None

    return InformationRetrievalEvaluator(
        queries=queries,
        corpus=corpus,
        relevant_docs=relevant_docs,
        name=name,
        mrr_at_k=[10],
        ndcg_at_k=[10],
        accuracy_at_k=[1, 3, 5],
        show_progress_bar=False,
    )


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
    holdout_path = pairs_path.with_name("holdout.jsonl")
    if not pairs_path.exists():
        raise SystemExit(f"missing {pairs_path}; run build_dataset.py first")

    random.seed(train_cfg["seed"])
    torch.manual_seed(train_cfg["seed"])

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
    use_amp = bool(train_cfg.get("use_amp", False)) and torch.cuda.is_available()
    if use_amp:
        print("mixed precision (FP16): enabled (CUDA detected)")

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

    evaluator = build_ir_evaluator(pairs_path, holdout_path, name="holdout-ir")
    if evaluator is None:
        print("warn: no evaluator (holdout missing) — best-checkpoint selection disabled")

    steps_per_epoch = max(len(loader) for loader, _ in objectives)
    warmup_steps = int(steps_per_epoch * train_cfg["epochs"] * train_cfg["warmup_ratio"])
    evaluation_steps = int(train_cfg.get("evaluation_steps", 0))
    if evaluation_steps == 0:
        # Evaluate at end of each epoch.
        evaluation_steps = steps_per_epoch

    run_name = cfg["run_name"]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"training {len(objectives)} objective(s) for {train_cfg['epochs']} epochs")
    print(f"evaluation every {evaluation_steps} steps; save_best_model={train_cfg.get('save_best_model', True)}")

    model.fit(
        train_objectives=objectives,
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
    print(f"saved fine-tuned embedding model to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
