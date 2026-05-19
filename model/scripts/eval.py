"""Evaluate top-k capability retrieval on the holdout intents.

For each holdout intent, embed it, then score against the *training* triggers
of every capability. The capability whose triggers have the highest mean-of-
top-K cosine wins (same scoring as octomind's `score_capability`).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml
from sentence_transformers import SentenceTransformer


TOP_K_CAP_SCORE = 3  # mirror AUTO_ACTIVATE_TOP_K in octomind


def cap_score(intent_vec: np.ndarray, trigger_vecs: np.ndarray) -> float:
    sims = trigger_vecs @ intent_vec
    sims.sort()
    take = min(TOP_K_CAP_SCORE, len(sims))
    return float(sims[-take:].mean())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="checkpoint dir from train.py")
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--base", action="store_true", help="evaluate base model instead of fine-tuned run")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    root = Path(__file__).resolve().parents[1]
    pairs_path = root / cfg["data"]["pairs_path"]
    holdout_path = pairs_path.with_name("holdout.jsonl")
    if not holdout_path.exists() or not pairs_path.exists():
        raise SystemExit("missing pairs.jsonl or holdout.jsonl; run build_dataset.py")

    triggers_by_cap: dict[str, set[str]] = defaultdict(set)
    with pairs_path.open() as f:
        for line in f:
            row = json.loads(line)
            label = row["label"]
            # `_oos` is a training-only sink (not a runtime capability)
            # — exclude from eval so the metrics mirror what production
            # actually scores against.
            if label == "_oos":
                continue
            triggers_by_cap[label].add(row["anchor"])
            triggers_by_cap[label].add(row["positive"])

    holdout: list[tuple[str, str]] = []
    with holdout_path.open() as f:
        for line in f:
            row = json.loads(line)
            holdout.append((row["intent"], row["label"]))

    if not holdout:
        print("empty holdout set", file=sys.stderr)
        return 1

    model_path = str(cfg["base_model"]) if args.base else str(args.run)
    print(f"loading model: {model_path}")
    model = SentenceTransformer(model_path)

    labels = sorted(triggers_by_cap.keys())
    label_trigger_vecs: dict[str, np.ndarray] = {}
    for label in labels:
        triggers = sorted(triggers_by_cap[label])
        v = model.encode(triggers, normalize_embeddings=True, convert_to_numpy=True)
        label_trigger_vecs[label] = v

    intents = [intent for intent, _ in holdout]
    intent_vecs = model.encode(intents, normalize_embeddings=True, convert_to_numpy=True)

    top_ks = cfg["eval"]["top_k"]
    hits = {k: 0 for k in top_ks}
    margins: list[float] = []

    for (intent, gold), intent_vec in zip(holdout, intent_vecs):
        scored = [(cap_score(intent_vec, label_trigger_vecs[label]), label) for label in labels]
        scored.sort(reverse=True)
        rank = next((i for i, (_, lab) in enumerate(scored) if lab == gold), len(scored))
        for k in top_ks:
            if rank < k:
                hits[k] += 1
        if len(scored) >= 2:
            margins.append(scored[0][0] - scored[1][0])

    n = len(holdout)
    print(f"\nholdout size: {n}")
    for k in top_ks:
        print(f"top-{k}: {hits[k] / n:.3f} ({hits[k]}/{n})")
    if margins:
        print(f"mean top1-top2 margin: {sum(margins) / len(margins):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
