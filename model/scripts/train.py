"""Fine-tune the bi-encoder on (anchor, positive) pairs and (anchor,
positive, negative) triplets.

Loss stack (configurable via configs/default.yaml::loss):

  1. CachedMultipleNegativesRankingLoss
     Equivalent to MNRL but with GradCache: processes the effective
     batch in `mini_batch_size` chunks while keeping the in-batch
     negatives count at `batch_size`. Lets us push the effective batch
     to 256-2048 on a single GPU. More in-batch negatives = harder
     contrast = wider runtime margins.
     https://huggingface.co/blog/train-sentence-transformers

  2. GISTEmbedLoss (optional, requires a guide model)
     A frozen "guide" embedder decides which in-batch candidates are
     *true* negatives — anything the guide rates above the
     anchor/positive similarity is excluded from the contrastive loss.
     Removes false-negative noise from semantically-near labels
     (legal-*, programming-*, codesearch-*, messaging-*).
     https://arxiv.org/abs/2402.16829

  3. MatryoshkaLoss (optional, wraps either of the above)
     Applies the inner loss at multiple truncation dims so the model
     learns to concentrate information at the front of the embedding
     vector. The same trained model can be served at 384, 256, 192,
     128, or 96 dims — useful when on-disk/in-memory cache size becomes
     a concern.
     https://sbert.net/examples/sentence_transformer/training/matryoshka/README.html

Two objectives are stacked (each gets its own loss instance built from
the same stack): pairs.jsonl for in-batch-only MNRL signal, and
triplets.jsonl for in-batch + explicit hard-negative signal.

An InformationRetrievalEvaluator runs each epoch on holdout intents
and the trainer keeps the checkpoint with the highest dev MRR@10.
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
from datasets import Dataset
from sentence_transformers import (
    InputExample,
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
# sentence-transformers 5.x relocated these under
# `sentence_transformer.{evaluation,losses,training_args}`. Try the new
# paths first, fall back to the deprecated ones for older installs.
try:
    from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator
    from sentence_transformers.sentence_transformer.losses import (
        CachedMultipleNegativesRankingLoss,
        GISTEmbedLoss,
        MatryoshkaLoss,
        MultipleNegativesRankingLoss,
    )
    from sentence_transformers.sentence_transformer.training_args import BatchSamplers
except ImportError:
    from sentence_transformers.evaluation import InformationRetrievalEvaluator
    from sentence_transformers.losses import (
        CachedMultipleNegativesRankingLoss,
        GISTEmbedLoss,
        MatryoshkaLoss,
        MultipleNegativesRankingLoss,
    )
    from sentence_transformers.training_args import BatchSamplers
from torch.utils.data import DataLoader

warnings.filterwarnings("ignore", category=FutureWarning)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------


def load_pairs_ds(path: Path) -> Dataset:
    """`MultipleNegativesRankingLoss` and its cached/GIST variants read
    (anchor, positive) as the first two columns. No `label` column —
    in-batch negatives are implicit."""
    anchors: list[str] = []
    positives: list[str] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            anchors.append(row["anchor"])
            positives.append(row["positive"])
    return Dataset.from_dict({"anchor": anchors, "positive": positives})


def load_triplets_ds(path: Path) -> Dataset:
    """Triplets give the same loss an explicit hard negative IN ADDITION
    to the in-batch negatives — Sentence Transformers reads columns
    [anchor, positive, negative] and stacks `negative` alongside the
    softmax denominator entries from other rows' positives."""
    anchors: list[str] = []
    positives: list[str] = []
    negatives: list[str] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            anchors.append(row["anchor"])
            positives.append(row["positive"])
            negatives.append(row["negative"])
    return Dataset.from_dict({"anchor": anchors, "positive": positives, "negative": negatives})


# Legacy loaders kept for the --legacy code path below.

def load_pairs_examples(path: Path) -> list[InputExample]:
    out: list[InputExample] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.append(InputExample(texts=[row["anchor"], row["positive"]]))
    return out


def load_triplets_examples(path: Path) -> list[InputExample]:
    out: list[InputExample] = []
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.append(InputExample(texts=[row["anchor"], row["positive"], row["negative"]]))
    return out


# ---------------------------------------------------------------------------
# Loss assembly
# ---------------------------------------------------------------------------


def build_loss(
    model: SentenceTransformer,
    loss_cfg: dict,
    mini_batch_size: int,
):
    """Compose the loss stack from config.

    Order of wrapping (inside-out):
      CachedMNRL or MNRL  →  GIST wrap (optional)  →  Matryoshka wrap (optional)

    GISTEmbedLoss doesn't take a `mini_batch_size`; it accepts a guide
    model and computes its own in-batch filtering. When `gist` is on we
    SKIP the cached variant — caching's two-pass trick isn't compatible
    with GIST's guide-model masking. Effective batch is then capped at
    `mini_batch_size * gradient_accumulation_steps` (the trainer arg).
    """
    use_cached = bool(loss_cfg.get("cached", True))
    use_gist = bool(loss_cfg.get("gist", False))
    use_matryoshka = bool(loss_cfg.get("matryoshka", False))

    if use_gist:
        guide_name = loss_cfg.get("gist_guide", "BAAI/bge-small-en-v1.5")
        print(f"loss: GISTEmbedLoss (guide={guide_name})")
        guide = SentenceTransformer(guide_name)
        for p in guide.parameters():
            p.requires_grad_(False)
        # GISTEmbedLoss(model, guide, ...) — positional. The kwarg used
        # to be `guide_model` in early drafts; settled on `guide`.
        inner = GISTEmbedLoss(model, guide)
    elif use_cached:
        print(f"loss: CachedMultipleNegativesRankingLoss (mini_batch_size={mini_batch_size})")
        inner = CachedMultipleNegativesRankingLoss(model, mini_batch_size=mini_batch_size)
    else:
        print("loss: MultipleNegativesRankingLoss (legacy in-memory variant)")
        inner = MultipleNegativesRankingLoss(model)

    if use_matryoshka:
        dims = list(loss_cfg.get("matryoshka_dims", [384, 256, 192, 128, 96]))
        weights = loss_cfg.get("matryoshka_weights")
        if weights is not None:
            weights = list(weights)
        print(f"loss: MatryoshkaLoss wrap dims={dims} weights={weights}")
        inner = MatryoshkaLoss(model, inner, matryoshka_dims=dims, matryoshka_weights=weights)

    return inner


# ---------------------------------------------------------------------------
# Evaluation builder (unchanged behavior)
# ---------------------------------------------------------------------------


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

    label_to_docs: dict[str, set[str]] = defaultdict(set)
    with pairs_path.open() as f:
        for line in f:
            row = json.loads(line)
            label = row["label"]
            # Skip the `_oos` sink — it's a training-only label for OOD
            # separation, never registered as a runtime capability, so
            # the IR evaluator shouldn't score against it.
            if label == "_oos":
                continue
            label_to_docs[label].add(row["anchor"])
            label_to_docs[label].add(row["positive"])

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


# ---------------------------------------------------------------------------
# Legacy path: `model.fit(...)` with plain MNRL. Kept as escape hatch.
# ---------------------------------------------------------------------------


def train_legacy(
    cfg: dict,
    model: SentenceTransformer,
    pairs_path: Path,
    triplets_path: Path,
    holdout_path: Path,
    out_dir: Path,
) -> None:
    train_cfg = cfg["train"]

    pairs = load_pairs_examples(pairs_path)
    random.shuffle(pairs)
    print(f"[legacy] loaded {len(pairs)} pair examples")

    triplets: list[InputExample] = []
    if triplets_path.exists():
        triplets = load_triplets_examples(triplets_path)
        random.shuffle(triplets)
        print(f"[legacy] loaded {len(triplets)} triplet examples")

    pin_memory = torch.cuda.is_available()
    use_amp = bool(train_cfg.get("use_amp", False)) and torch.cuda.is_available()

    pair_loader = DataLoader(
        pairs, shuffle=True, batch_size=train_cfg["batch_size"],
        drop_last=True, pin_memory=pin_memory,
    )
    pair_loss = MultipleNegativesRankingLoss(model)
    objectives = [(pair_loader, pair_loss)]

    if triplets:
        trip_loader = DataLoader(
            triplets, shuffle=True,
            batch_size=max(8, train_cfg["batch_size"] // 2),
            drop_last=True, pin_memory=pin_memory,
        )
        trip_loss = MultipleNegativesRankingLoss(model)
        objectives.append((trip_loader, trip_loss))

    evaluator = build_ir_evaluator(pairs_path, holdout_path, name="holdout-ir")

    steps_per_epoch = max(len(loader) for loader, _ in objectives)
    warmup_steps = int(steps_per_epoch * train_cfg["epochs"] * train_cfg["warmup_ratio"])
    evaluation_steps = int(train_cfg.get("evaluation_steps", 0)) or steps_per_epoch

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


# ---------------------------------------------------------------------------
# Modern path: SentenceTransformerTrainer with composable losses.
# ---------------------------------------------------------------------------


def train_modern(
    cfg: dict,
    model: SentenceTransformer,
    pairs_path: Path,
    triplets_path: Path,
    holdout_path: Path,
    out_dir: Path,
    resume: bool = False,
) -> None:
    train_cfg = cfg["train"]
    loss_cfg = cfg.get("loss", {})

    pairs_ds = load_pairs_ds(pairs_path)
    print(f"loaded {len(pairs_ds)} pair examples from {pairs_path.name}")

    train_datasets: dict[str, Dataset] = {"pairs": pairs_ds}
    if triplets_path.exists():
        trip_ds = load_triplets_ds(triplets_path)
        train_datasets["triplets"] = trip_ds
        print(f"loaded {len(trip_ds)} triplet examples from {triplets_path.name}")
    else:
        print(f"no triplets at {triplets_path}; training on pairs only")

    # Build one loss instance per dataset. Both share the same model and
    # the same loss class — they differ only in column count.
    mini_batch_size = int(train_cfg.get("mini_batch_size", train_cfg["batch_size"]))
    losses = {name: build_loss(model, loss_cfg, mini_batch_size) for name in train_datasets}

    evaluator = build_ir_evaluator(pairs_path, holdout_path, name="holdout-ir")
    if evaluator is None:
        print("warn: no evaluator (holdout missing) — best-checkpoint selection disabled")

    use_fp16 = bool(train_cfg.get("use_amp", False)) and torch.cuda.is_available()
    if use_fp16:
        print("mixed precision (FP16): enabled (CUDA detected)")

    targs = SentenceTransformerTrainingArguments(
        output_dir=str(out_dir),
        num_train_epochs=train_cfg["epochs"],
        per_device_train_batch_size=train_cfg["batch_size"],
        per_device_eval_batch_size=train_cfg["batch_size"],
        learning_rate=train_cfg["learning_rate"],
        warmup_ratio=train_cfg["warmup_ratio"],
        weight_decay=train_cfg["weight_decay"],
        fp16=use_fp16,
        # `BatchSamplers.NO_DUPLICATES` is mandatory for MNRL-family
        # losses: the in-batch-negatives signal collapses if a batch
        # contains two anchors for the same positive (they would
        # appear as each other's "negative").
        batch_sampler=BatchSamplers.NO_DUPLICATES,
        eval_strategy="epoch" if evaluator is not None else "no",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=bool(train_cfg.get("save_best_model", True)) and evaluator is not None,
        metric_for_best_model=("eval_holdout-ir_cosine_mrr@10" if evaluator is not None else None),
        greater_is_better=True,
        logging_steps=50,
        report_to=[],
        seed=train_cfg["seed"],
        dataloader_pin_memory=torch.cuda.is_available(),
    )

    trainer = SentenceTransformerTrainer(
        model=model,
        args=targs,
        train_dataset=train_datasets,
        loss=losses,
        evaluator=evaluator,
    )

    print(
        f"training {len(train_datasets)} objective(s) for {train_cfg['epochs']} epochs "
        f"(effective batch={train_cfg['batch_size']}, mini_batch={mini_batch_size})"
    )
    if resume:
        ckpts = sorted(out_dir.glob("checkpoint-*"), key=lambda p: int(p.name.split("-")[-1]))
        if ckpts:
            print(f"resuming from {ckpts[-1]}")
            trainer.train(resume_from_checkpoint=str(ckpts[-1]))
        else:
            print(f"warn: --resume requested but no checkpoint-* under {out_dir}; starting fresh")
            trainer.train()
    else:
        trainer.train()
    trainer.save_model(str(out_dir))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--config",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml",
    )
    ap.add_argument(
        "--legacy",
        action="store_true",
        help="use the old model.fit() loop with plain MultipleNegativesRankingLoss. "
             "Diagnostic only — the modern path with cached/GIST/Matryoshka is the "
             "production recipe.",
    )
    ap.add_argument(
        "--resume",
        action="store_true",
        help="resume training from the latest checkpoint-* under the most recent "
             "checkpoints/embed-* run directory (instead of starting a fresh "
             "timestamped run). Use this when a long training was interrupted "
             "(SSH disconnect, OOM, etc).",
    )
    ap.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="explicit run directory to resume into. Overrides --resume's "
             "auto-detection of the latest checkpoints/embed-* dir.",
    )
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

    model = SentenceTransformer(cfg["base_model"])
    model.max_seq_length = train_cfg["max_seq_length"]

    # Determine output directory: a fresh timestamped one for a normal
    # run, OR the existing (latest / explicit) run dir for --resume.
    if args.resume_from is not None:
        out_dir = args.resume_from
        if not out_dir.exists():
            raise SystemExit(f"--resume-from path does not exist: {out_dir}")
        resume = True
    elif args.resume:
        ckpt_root = root / cfg["output_dir"]
        existing = sorted(ckpt_root.glob("embed-*"), key=lambda p: p.stat().st_mtime)
        if not existing:
            raise SystemExit(
                f"--resume requested but no embed-* run found under {ckpt_root}"
            )
        out_dir = existing[-1]
        print(f"--resume: targeting latest run {out_dir}")
        resume = True
    else:
        run_name = cfg["run_name"]
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = root / cfg["output_dir"] / f"{run_name}-{timestamp}"
        out_dir.mkdir(parents=True, exist_ok=True)
        resume = False

    if args.legacy:
        if resume:
            print("warn: --legacy + --resume not supported; the legacy model.fit() "
                  "loop has no checkpoint-resume. Running fresh.")
        train_legacy(cfg, model, pairs_path, triplets_path, holdout_path, out_dir)
    else:
        train_modern(cfg, model, pairs_path, triplets_path, holdout_path, out_dir, resume=resume)

    (out_dir / "train_config.yaml").write_text(yaml.safe_dump(cfg))
    print(f"saved fine-tuned embedding model to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
