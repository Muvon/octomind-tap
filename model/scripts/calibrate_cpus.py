"""Pick runtime thresholds that hold on every CPU kind.

Input: one score dump per CPU kind from `dump_scores.py`. For each gate the
operating point is chosen by its WORST machine: the caps on false
activations must hold on every dump, and the accuracy that is maximised is
the lowest one across dumps.

  capability gate   octomind capability.rs AUTO_ACTIVATE_THRESHOLD / _MARGIN
                    (and skill.rs SEMANTIC_DEFAULT_THRESHOLD / SEMANTIC_MARGIN)
  route gate        octomind tap_route.rs ROUTE_THRESHOLD / ROUTE_MARGIN

  uv run python scripts/calibrate_cpus.py scores/arm64.json scores/x86-sse.json scores/x86-vnni.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_route import MAX_FIRED, MAX_WRONG, best_point, print_point  # noqa: E402

# Grid step for both gates. The dumps differ by a few hundredths, so a coarser
# grid can step over the only points that hold everywhere.
GRID_STEP = 0.01


def capability_metrics(rows: list[dict], threshold: float, margin: float) -> tuple[float, float]:
    """(gate_acc on positives, null_fpr), as eval_gate.py counts them."""
    pos_total = pos_correct = null_total = null_fired = 0
    for r in rows:
        fired = r["s1"] >= threshold and r["s1"] - r["s2"] >= margin
        if r["gold"] is None:
            null_total += 1
            null_fired += fired
        else:
            pos_total += 1
            pos_correct += fired and r["top1"] == r["gold"]
    return pos_correct / pos_total, null_fired / null_total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dumps", type=Path, nargs="+", help="score dumps from dump_scores.py, one per CPU kind")
    ap.add_argument("--target-fpr", type=float, default=0.03, help="capability gate: cap on null_fpr")
    ap.add_argument("--max-wrong", type=float, default=MAX_WRONG, help="route gate: cap on the wrong-handoff rate")
    ap.add_argument("--max-fired", type=float, default=MAX_FIRED, help="route gate: cap on the foreign fired rate")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    dumps = [json.loads(p.read_text()) for p in args.dumps]
    names = [f"{p.stem} ({d['cpu']})" for p, d in zip(args.dumps, dumps)]
    thresholds = [round(float(x), 2) for x in np.arange(0.40, 0.86, GRID_STEP)]
    margins = [round(float(x), 2) for x in np.arange(0.00, 0.21, GRID_STEP)]

    capability = None
    for t in thresholds:
        for m in margins:
            per_cpu = [capability_metrics(d["capability"], t, m) for d in dumps]
            if max(fpr for _, fpr in per_cpu) > args.target_fpr:
                continue
            gate_acc = min(acc for acc, _ in per_cpu)
            if capability is None or gate_acc > capability["gate_acc"]:
                capability = {"threshold": t, "margin": m, "gate_acc": gate_acc, "per_cpu": per_cpu}

    print(f"capability gate (null_fpr <= {args.target_fpr} on every CPU):")
    if capability:
        print(f"  threshold={capability['threshold']:.2f}  margin={capability['margin']:.2f}")
        for name, (acc, fpr) in zip(names, capability["per_cpu"]):
            print(f"  {name:<40} gate_acc={acc:.3f}  null_fpr={fpr:.3f}")
    else:
        print("  no point holds on every CPU")

    route = best_point([d["route"] for d in dumps], thresholds, margins, args.max_wrong, args.max_fired)
    print(f"\nroute gate (wrong <= {args.max_wrong}, foreign fired <= {args.max_fired} on every CPU):")
    if route:
        print(f"  threshold={route['threshold']:.2f}  margin={route['margin']:.2f}")
        for name, metrics in zip(names, route["per_cpu"]):
            print(f"  {name}")
            print_point(metrics)
    else:
        print("  no point holds on every CPU")

    if args.json_out:
        args.json_out.write_text(json.dumps({"dumps": names, "capability": capability, "route": route}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
