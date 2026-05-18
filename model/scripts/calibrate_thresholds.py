"""Sweep runtime (threshold, margin) on a checkpoint + eval_real.jsonl
and report the Pareto front of (gate_acc, null_fpr).

The runtime in octomind/src/mcp/core/capability.rs uses two constants
that determine whether a capability auto-activates:

  AUTO_ACTIVATE_THRESHOLD = 0.55   (top-1 cosine floor)
  AUTO_ACTIVATE_MARGIN    = 0.08   (top-1 minus top-2)

Those numbers were hand-picked for the base BGE-small. After fine-
tuning the operating point shifts — usually the FT model lets us
TIGHTEN the margin (kill more false positives) without sacrificing
recall. This script measures it.

Usage:

  uv run python scripts/calibrate_thresholds.py --model checkpoints/embed-<ts>
  # → prints Pareto frontier + recommended (threshold, margin) for
  #   a target FPR (default 0.02).

The output is a copy-paste-ready snippet for capability.rs:772/781 if
the new operating point beats the current one.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import yaml
from sentence_transformers import SentenceTransformer

# Re-use the runtime-mirror scoring from eval_gate.py.
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import cap_score, select_with_margin, load_triggers_from_pairs  # noqa: E402


def evaluate_at(scored_per_row: list[list[tuple[float, str]]],
                rows: list[dict],
                threshold: float,
                margin: float) -> tuple[float, float, int, int, int, int]:
    """Given the precomputed (score, label) lists per row, evaluate a
    single (threshold, margin) point.

    Returns: (gate_acc_on_positives, null_fpr, pos_correct, pos_total,
              null_fp, null_total)
    """
    pos_correct = 0
    pos_total = 0
    null_fp = 0
    null_total = 0
    for row, scored in zip(rows, scored_per_row):
        gold = row.get("label")
        gate = select_with_margin(scored, threshold, margin)
        if gold is None:
            null_total += 1
            if gate is not None:
                null_fp += 1
        else:
            pos_total += 1
            if gate is not None and gate[1] == gold:
                pos_correct += 1
    gate_acc = (pos_correct / pos_total) if pos_total else 0.0
    null_fpr = (null_fp / null_total) if null_total else 0.0
    return gate_acc, null_fpr, pos_correct, pos_total, null_fp, null_total


def precompute_scored(model_path: str,
                      rows: list[dict],
                      triggers_by_cap: dict,
                      top_k: int) -> list[list[tuple[float, str]]]:
    print(f"loading model: {model_path}")
    model = SentenceTransformer(model_path)

    labels = sorted(triggers_by_cap.keys())
    label_trigger_vecs: dict[str, np.ndarray] = {}
    for label in labels:
        triggers = sorted(triggers_by_cap[label])
        label_trigger_vecs[label] = model.encode(
            triggers, normalize_embeddings=True, convert_to_numpy=True
        )
    intents = [r["intent"] for r in rows]
    intent_vecs = model.encode(intents, normalize_embeddings=True, convert_to_numpy=True)

    out: list[list[tuple[float, str]]] = []
    for iv in intent_vecs:
        scored = [(cap_score(iv, label_trigger_vecs[label], top_k), label) for label in labels]
        scored.sort(reverse=True)
        out.append(scored)
    return out


def pareto_front(points: list[tuple[float, float, float, float]]) -> list[tuple[float, float, float, float]]:
    """Filter `(τ, δ, gate_acc, null_fpr)` to the Pareto-optimal subset
    maximizing gate_acc while minimizing null_fpr."""
    out = []
    for p in points:
        _, _, acc_p, fpr_p = p
        dominated = False
        for q in points:
            if q is p:
                continue
            _, _, acc_q, fpr_q = q
            if acc_q >= acc_p and fpr_q <= fpr_p and (acc_q > acc_p or fpr_q < fpr_p):
                dominated = True
                break
        if not dominated:
            out.append(p)
    return sorted(out, key=lambda x: (-x[2], x[3]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True)
    ap.add_argument("--config", type=Path,
                    default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--eval-set", type=Path, default=None)
    ap.add_argument("--pairs", type=Path, default=None)
    ap.add_argument(
        "--threshold-grid",
        type=str,
        default="0.45,0.48,0.50,0.52,0.55,0.58,0.60,0.62,0.65,0.68,0.70",
    )
    ap.add_argument(
        "--margin-grid",
        type=str,
        default="0.03,0.05,0.06,0.08,0.10,0.12,0.15,0.18",
    )
    ap.add_argument(
        "--target-fpr",
        type=float,
        default=0.02,
        help="recommend the operating point with highest gate_acc whose null_fpr <= target",
    )
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    eval_cfg = cfg.get("eval", {})
    root = Path(__file__).resolve().parents[1]

    eval_path = args.eval_set or (root / eval_cfg.get("real_set_path", "data/eval_real.jsonl"))
    if not eval_path.exists():
        raise SystemExit(f"missing eval set: {eval_path}; run build_eval_seed.py first")

    pairs_path = args.pairs or (root / cfg["data"]["pairs_path"])
    if not pairs_path.exists():
        raise SystemExit(f"missing pairs.jsonl: {pairs_path}; run build_dataset.py first")

    rows = [json.loads(line) for line in eval_path.read_text().splitlines() if line.strip()]
    triggers_by_cap = load_triggers_from_pairs(pairs_path)
    top_k = int(eval_cfg.get("runtime_top_k", 3))

    scored = precompute_scored(args.model, rows, triggers_by_cap, top_k)

    thresholds = [float(x) for x in args.threshold_grid.split(",")]
    margins = [float(x) for x in args.margin_grid.split(",")]

    all_points: list[tuple[float, float, float, float]] = []
    print()
    print(f"{'τ':>6} {'δ':>6} {'gate_acc':>10} {'null_fpr':>10} {'pos':>8} {'null':>8}")
    print("-" * 56)
    for t in thresholds:
        for m in margins:
            gate_acc, null_fpr, pc, pt, nfp, nt = evaluate_at(scored, rows, t, m)
            all_points.append((t, m, gate_acc, null_fpr))
            print(f"{t:>6.2f} {m:>6.2f} {gate_acc:>10.3f} {null_fpr:>10.3f} "
                  f"{pc:>4}/{pt:<3} {nfp:>4}/{nt:<3}")

    pareto = pareto_front(all_points)
    print()
    print("Pareto frontier (sorted by gate_acc desc, then fpr asc):")
    for t, m, acc, fpr in pareto:
        print(f"  τ={t:.2f}  δ={m:.2f}   gate_acc={acc:.3f}  null_fpr={fpr:.3f}")

    # Recommendation: highest gate_acc with null_fpr <= target.
    eligible = [p for p in all_points if p[3] <= args.target_fpr]
    if eligible:
        rec = max(eligible, key=lambda p: (p[2], -p[3]))
        t, m, acc, fpr = rec
        print()
        print(f"RECOMMENDATION (target null_fpr <= {args.target_fpr}):")
        print(f"  threshold = {t:.2f}")
        print(f"  margin    = {m:.2f}")
        print(f"  gate_acc  = {acc:.3f}")
        print(f"  null_fpr  = {fpr:.3f}")
        print()
        print("Update octomind/src/mcp/core/capability.rs:")
        print(f"  const AUTO_ACTIVATE_THRESHOLD: f32 = {t:.2f};")
        print(f"  const AUTO_ACTIVATE_MARGIN: f32 = {m:.2f};")
        print()
        print("And octomind/src/mcp/core/skill.rs SEMANTIC_DEFAULT_THRESHOLD / SEMANTIC_MARGIN")
        print("to match (they share the same embedding).")
    else:
        print()
        print(f"NO operating point achieves null_fpr <= {args.target_fpr}.")
        print("Either: relax --target-fpr, expand eval_real with more positives, or "
              "retrain — the FT model isn't separating NULL from positives cleanly.")

    if args.json_out:
        args.json_out.write_text(json.dumps({
            "model": args.model,
            "top_k": top_k,
            "grid": all_points,
            "pareto": pareto,
            "target_fpr": args.target_fpr,
            "recommendation": rec if eligible else None,
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
