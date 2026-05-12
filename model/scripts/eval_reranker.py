"""Evaluate the reranker on the holdout intents using bi-encoder retrieval
+ cross-encoder rerank — the same two-stage pipeline the runtime will use.

For each holdout intent:
  1. Bi-encoder scores every capability via mean-of-top-K cosine over its
     training triggers, returns the top-N candidates.
  2. Cross-encoder reranks (intent, best_trigger) for each of those N
     candidates and replaces their scores with the rerank scores.
  3. We measure top-k accuracy and the top1-top2 margin.

Without --base, we use the fine-tuned reranker. With --base, the upstream
turbo cross-encoder. The diff between the two tells us whether the fine-
tune actually sharpened the gap (it should).
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml
from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import CrossEncoder


TOP_K_CAP_SCORE = 3
RERANK_TOP_N = 5


def cap_score(intent_vec: np.ndarray, trigger_vecs: np.ndarray) -> tuple[float, int]:
    sims = trigger_vecs @ intent_vec
    order = np.argsort(-sims)
    take = min(TOP_K_CAP_SCORE, len(order))
    return float(sims[order[:take]].mean()), int(order[0])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True, help="reranker checkpoint dir")
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "reranker.yaml")
    ap.add_argument("--embed-model", type=str, default="BAAI/bge-small-en-v1.5",
                    help="bi-encoder for first-stage retrieval (use the fine-tuned one for fair eval)")
    ap.add_argument("--base", action="store_true", help="use the upstream reranker base instead of --run")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    root = Path(__file__).resolve().parents[1]
    pairs_path = root / "data" / "pairs.jsonl"
    holdout_path = root / "data" / "holdout.jsonl"
    if not (pairs_path.exists() and holdout_path.exists()):
        raise SystemExit("missing pairs.jsonl or holdout.jsonl; run build_dataset.py")

    triggers_by_cap: dict[str, set[str]] = defaultdict(set)
    with pairs_path.open() as f:
        for line in f:
            row = json.loads(line)
            triggers_by_cap[row["label"]].add(row["anchor"])
            triggers_by_cap[row["label"]].add(row["positive"])

    holdout: list[tuple[str, str]] = []
    with holdout_path.open() as f:
        for line in f:
            row = json.loads(line)
            holdout.append((row["intent"], row["label"]))

    bi = SentenceTransformer(args.embed_model)
    rerank_model = cfg["base_model"] if args.base else str(args.run)
    print(f"bi-encoder: {args.embed_model}")
    print(f"reranker:   {rerank_model}")
    ce = CrossEncoder(rerank_model)

    labels = sorted(triggers_by_cap.keys())
    trigger_lists: dict[str, list[str]] = {label: sorted(triggers_by_cap[label]) for label in labels}
    trigger_vecs: dict[str, np.ndarray] = {
        label: bi.encode(triggers, normalize_embeddings=True, convert_to_numpy=True)
        for label, triggers in trigger_lists.items()
    }

    intents = [intent for intent, _ in holdout]
    intent_vecs = bi.encode(intents, normalize_embeddings=True, convert_to_numpy=True)

    top_ks = cfg["eval"]["top_k"]
    rerank_n = cfg["eval"].get("rerank_top_n", RERANK_TOP_N)

    hits = {k: 0 for k in top_ks}
    margins: list[float] = []

    for (intent, gold), iv in zip(holdout, intent_vecs):
        # Stage 1: bi-encoder retrieval — score every capability.
        scored = []
        best_trig_idx = {}
        for label in labels:
            s, bi_idx = cap_score(iv, trigger_vecs[label])
            scored.append((s, label))
            best_trig_idx[label] = bi_idx
        scored.sort(reverse=True)

        # Stage 2: cross-encoder rerank top-N.
        candidates = scored[:rerank_n]
        ce_pairs = [(intent, trigger_lists[label][best_trig_idx[label]]) for _, label in candidates]
        ce_scores = ce.predict(ce_pairs)
        reranked = sorted(
            ((float(ce_scores[i]), label) for i, (_, label) in enumerate(candidates)),
            reverse=True,
        )

        rank = next((i for i, (_, lab) in enumerate(reranked) if lab == gold), len(reranked))
        for k in top_ks:
            if rank < k:
                hits[k] += 1
        if len(reranked) >= 2:
            margins.append(reranked[0][0] - reranked[1][0])

    n = len(holdout)
    print(f"\nholdout size: {n}")
    for k in top_ks:
        print(f"top-{k}: {hits[k] / n:.3f} ({hits[k]}/{n})")
    if margins:
        print(f"mean top1-top2 margin (reranker scores): {sum(margins) / len(margins):.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
