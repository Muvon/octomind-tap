"""Zero-shot base-model bake-off on the frozen real-user eval set.

For each candidate base model, score eval_real.jsonl with the SAME
runtime rule as eval_gate.py (mean-of-top-K cosine over a capability's
triggers), then report:

  - top1_acc / top3_acc  : threshold-FREE ranking quality. This is the
    true "ceiling" a base offers before any fine-tuning — the fair way
    to compare bases, since each model has its own cosine scale.
  - best gate operating point: the (threshold, margin) that MAXIMISES
    gate_acc subject to null_fpr <= --target-fpr. Each model is judged
    at ITS OWN best operating point, so a model isn't penalised just
    because the production 0.55/0.08 was tuned for BGE.
  - mean_top1_margin : separation on correctly-ranked positives.
  - enc_intents_per_s: CPU encode throughput (runtime cost proxy).

Asymmetric models (e5, arctic) need query/doc instruction prefixes to
perform; pass them per-model in MODELS so the comparison is fair. The
production pipeline is prefix-FREE, so a model that only wins WITH a
prefix implies a runtime change — flagged in the output.

Usage:
  uv run python scripts/compare_bases.py                 # default roster
  uv run python scripts/compare_bases.py --models a,b    # explicit ids
  uv run python scripts/compare_bases.py --json-out cmp.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import yaml
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import cap_score, select_with_margin, load_triggers_from_pairs  # noqa: E402

# Default roster. `q`/`d` are optional query/doc prefixes for asymmetric
# models — when present the model needs a runtime change to deploy
# (the production encode path is prefix-free), so `prefix` is flagged.
DEFAULT_ROSTER: list[dict] = [
    {"id": "BAAI/bge-small-en-v1.5", "tag": "base (current), 33M/384d"},
    {"id": "sentence-transformers/all-MiniLM-L6-v2", "tag": "22M/384d"},
    {"id": "thenlper/gte-small", "tag": "33M/384d, symmetric-ok"},
    {"id": "BAAI/bge-base-en-v1.5", "tag": "109M/768d (dim change!)"},
    {"id": "intfloat/e5-small-v2", "q": "query: ", "d": "passage: ",
     "tag": "33M/384d, NEEDS prefix"},
    {"id": "Snowflake/snowflake-arctic-embed-s",
     "q": "Represent this sentence for searching relevant passages: ", "d": "",
     "tag": "33M/384d, NEEDS query prefix"},
    {"id": "muvon/octomind-embed", "tag": "current FT (reference upper bound)"},
]


def grid_best_gate(scored_per_row: list[list[tuple[float, str]]],
                   rows: list[dict],
                   thresholds: list[float],
                   margins: list[float],
                   target_fpr: float) -> dict:
    """Sweep (threshold, margin); return the point with max gate_acc whose
    null_fpr <= target_fpr (fallback: min null_fpr if none qualify)."""
    best = None
    best_unconstrained = None
    for t in thresholds:
        for m in margins:
            pos_correct = pos_total = null_fp = null_total = 0
            for row, scored in zip(rows, scored_per_row):
                gold = row.get("label")
                gate = select_with_margin(scored, t, m)
                if gold is None:
                    null_total += 1
                    if gate is not None:
                        null_fp += 1
                else:
                    pos_total += 1
                    if gate is not None and gate[1] == gold:
                        pos_correct += 1
            gate_acc = pos_correct / pos_total if pos_total else 0.0
            null_fpr = null_fp / null_total if null_total else 0.0
            pt = {"threshold": t, "margin": m, "gate_acc": gate_acc, "null_fpr": null_fpr}
            if best_unconstrained is None or gate_acc > best_unconstrained["gate_acc"]:
                best_unconstrained = pt
            if null_fpr <= target_fpr:
                if best is None or (gate_acc, -null_fpr) > (best["gate_acc"], -best["null_fpr"]):
                    best = pt
    return best or best_unconstrained


def eval_model(spec: dict, eval_rows: list[dict], triggers_by_cap: dict,
               top_k: int, thresholds: list[float], margins: list[float],
               target_fpr: float, batch_size: int) -> dict:
    mid = spec["id"]
    q_pref = spec.get("q", "")
    d_pref = spec.get("d", "")
    print(f"\n=== {mid} ===", flush=True)
    model = SentenceTransformer(mid)

    labels = sorted(triggers_by_cap.keys())
    label_trigger_vecs: dict[str, np.ndarray] = {}
    for label in labels:
        triggers = [d_pref + t for t in sorted(triggers_by_cap[label])]
        label_trigger_vecs[label] = model.encode(
            triggers, normalize_embeddings=True, convert_to_numpy=True,
            batch_size=batch_size, show_progress_bar=False)

    intents = [q_pref + r["intent"] for r in eval_rows]
    t0 = time.time()
    intent_vecs = model.encode(intents, normalize_embeddings=True,
                               convert_to_numpy=True, batch_size=batch_size,
                               show_progress_bar=False)
    enc_s = time.time() - t0

    scored_per_row: list[list[tuple[float, str]]] = []
    pos_total = pos_top1 = pos_top3 = 0
    margins_top1: list[float] = []
    for row, iv in zip(eval_rows, intent_vecs):
        scored = [(cap_score(iv, label_trigger_vecs[l], top_k), l) for l in labels]
        scored.sort(reverse=True)
        scored_per_row.append(scored)
        gold = row.get("label")
        if gold is None:
            continue
        pos_total += 1
        if any(l == gold for _, l in scored[:3]):
            pos_top3 += 1
        if scored[0][1] == gold:
            pos_top1 += 1
            margins_top1.append(scored[0][0] - (scored[1][0] if len(scored) > 1 else 0.0))

    gate = grid_best_gate(scored_per_row, eval_rows, thresholds, margins, target_fpr)
    return {
        "model": mid,
        "tag": spec.get("tag", ""),
        "prefix": bool(q_pref or d_pref),
        "dim": int(intent_vecs.shape[1]),
        "top1_acc": pos_top1 / pos_total if pos_total else 0.0,
        "top3_acc": pos_top3 / pos_total if pos_total else 0.0,
        "mean_top1_margin": float(np.mean(margins_top1)) if margins_top1 else 0.0,
        "best_gate": gate,
        "enc_intents_per_s": len(intents) / enc_s if enc_s else 0.0,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path,
                    default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--models", type=str, default=None,
                    help="comma-separated model ids (overrides default roster, prefix-free)")
    ap.add_argument("--eval-set", type=Path, default=None)
    ap.add_argument("--pairs", type=Path, default=None)
    ap.add_argument("--target-fpr", type=float, default=0.03)
    ap.add_argument("--batch-size", type=int, default=128)
    ap.add_argument("--threshold-grid", type=str,
                    default="0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80")
    ap.add_argument("--margin-grid", type=str,
                    default="0.02,0.03,0.05,0.06,0.08,0.10,0.12,0.15")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    eval_cfg = cfg.get("eval", {})
    root = Path(__file__).resolve().parents[1]
    eval_path = args.eval_set or (root / eval_cfg.get("real_set_path", "data/eval_real.jsonl"))
    pairs_path = args.pairs or (root / cfg["data"]["pairs_path"])
    eval_rows = [json.loads(l) for l in eval_path.read_text().splitlines() if l.strip()]
    triggers_by_cap = load_triggers_from_pairs(pairs_path)
    top_k = int(eval_cfg.get("runtime_top_k", 3))
    thresholds = [float(x) for x in args.threshold_grid.split(",")]
    margins = [float(x) for x in args.margin_grid.split(",")]

    roster = ([{"id": m.strip()} for m in args.models.split(",")]
              if args.models else DEFAULT_ROSTER)

    results = []
    for spec in roster:
        try:
            results.append(eval_model(spec, eval_rows, triggers_by_cap, top_k,
                                      thresholds, margins, args.target_fpr,
                                      args.batch_size))
        except Exception as e:  # one bad model shouldn't kill the sweep
            print(f"  FAILED {spec['id']}: {e}", flush=True)

    results.sort(key=lambda r: r["top1_acc"], reverse=True)
    print("\n" + "=" * 110)
    print(f"{'model':<42}{'dim':>4}{'pfx':>4}{'top1':>7}{'top3':>7}"
          f"{'margin':>8}{'gate':>7}{'fpr':>6}{'τ':>6}{'δ':>6}{'enc/s':>8}")
    print("-" * 110)
    for r in results:
        g = r["best_gate"]
        print(f"{r['model']:<42}{r['dim']:>4}{('Y' if r['prefix'] else '-'):>4}"
              f"{r['top1_acc']:>7.3f}{r['top3_acc']:>7.3f}{r['mean_top1_margin']:>8.3f}"
              f"{g['gate_acc']:>7.3f}{g['null_fpr']:>6.3f}{g['threshold']:>6.2f}"
              f"{g['margin']:>6.2f}{r['enc_intents_per_s']:>8.1f}")
    print("=" * 110)
    print("top1/top3 = threshold-free ranking ceiling (fair base comparison).")
    print("gate/fpr/τ/δ = each model's OWN best operating point (max gate_acc, fpr<=%.2f)." % args.target_fpr)
    print("pfx=Y means the model needs query/doc prefixes → runtime change to deploy.")

    if args.json_out:
        args.json_out.write_text(json.dumps(results, indent=2))
        print(f"\nwrote {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
