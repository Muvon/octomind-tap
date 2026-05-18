"""Production publish gate for the bi-encoder.

Evaluates a checkpoint against the frozen "real user" eval set
(`data/eval_real.jsonl`) using THE SAME scoring rule the runtime uses:

  per_cap_score = mean of top-K cosine(intent, trigger_of_cap)   (K=3)
  activate iff   top1 >= threshold  AND  top1 - top2 >= margin   (0.55, 0.08)

Metrics produced:

  - top1_acc        : positives where predicted-label == expected-label
                      AND the gate would fire.
  - top3_acc        : positives where expected-label is in the top-3
                      under the runtime scoring.
  - null_fpr        : NULL prompts (chitchat / vague / paste / etc.)
                      where the gate WOULD fire — the false-positive
                      activation rate. Lower is better.
  - mean_margin     : mean top1-top2 score on positives. Wider is
                      better; predicts how robust the runtime gate is.
  - per_kind        : breakdown by `kind` field in eval_real.jsonl.
  - per_label       : per-capability recall on positives.

Comparison to baseline: pass `--baseline <path>` to compare against a
recorded JSON file. The gate exits non-zero if:

  - top1_acc < baseline.top1_acc - top1_tol           (default 0.01)
  - null_fpr > baseline.null_fpr + fpr_tol            (default 0.01)
  - any per-label top1 recall drops by > per_label_tol (default 0.05)

Use `--write-baseline <path>` to record the current run as the new
baseline (after promotion).
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


# ---------------------------------------------------------------------------
# Runtime-mirror scoring (must stay aligned with
# octomind/src/mcp/core/capability.rs::score_capability + select_with_margin)
# ---------------------------------------------------------------------------


def cap_score(intent_vec: np.ndarray, trigger_vecs: np.ndarray, top_k: int) -> float:
    sims = trigger_vecs @ intent_vec
    sims.sort()
    take = min(top_k, len(sims))
    return float(sims[-take:].mean())


def select_with_margin(scored: list[tuple[float, str]], threshold: float, margin: float):
    """Mirror of `select_with_margin` in capability.rs:793."""
    if not scored:
        return None
    scored = sorted(scored, key=lambda x: -x[0])
    top1 = scored[0][0]
    if top1 < threshold:
        return None
    top2 = scored[1][0] if len(scored) >= 2 else 0.0
    if top1 - top2 < margin:
        return None
    return scored[0]


# ---------------------------------------------------------------------------
# Trigger source — mirrors how the runtime fetches them
# ---------------------------------------------------------------------------


def load_triggers_from_pairs(pairs_path: Path) -> dict[str, set[str]]:
    """Pull every (anchor, positive) across pairs.jsonl and group by
    label. This matches what the runtime would have — the trigger set
    per capability after training-time expansion."""
    triggers_by_cap: dict[str, set[str]] = defaultdict(set)
    with pairs_path.open() as f:
        for line in f:
            row = json.loads(line)
            label = row.get("label")
            if not label:
                continue
            # The synthetic `_oos` sink doesn't represent a runtime
            # capability — exclude it from scoring against the user
            # intent.
            if label == "_oos":
                continue
            triggers_by_cap[label].add(row["anchor"])
            triggers_by_cap[label].add(row["positive"])
    return triggers_by_cap


# ---------------------------------------------------------------------------
# Eval loop
# ---------------------------------------------------------------------------


def evaluate(
    model_path: str,
    eval_rows: list[dict],
    triggers_by_cap: dict[str, set[str]],
    top_k: int,
    threshold: float,
    margin: float,
) -> dict:
    print(f"loading model: {model_path}")
    model = SentenceTransformer(model_path)

    labels = sorted(triggers_by_cap.keys())
    label_trigger_vecs: dict[str, np.ndarray] = {}
    for label in labels:
        triggers = sorted(triggers_by_cap[label])
        label_trigger_vecs[label] = model.encode(
            triggers, normalize_embeddings=True, convert_to_numpy=True
        )

    intents = [r["intent"] for r in eval_rows]
    intent_vecs = model.encode(intents, normalize_embeddings=True, convert_to_numpy=True)

    # Counters
    pos_total = 0
    pos_top1 = 0
    pos_top3 = 0
    pos_gate_correct = 0     # gate fires AND picks the right label
    pos_abstain_wrong = 0    # positive intent but gate abstained
    null_total = 0
    null_fp = 0              # NULL prompt but gate fired
    margins: list[float] = []

    per_kind_total: dict[str, int] = defaultdict(int)
    per_kind_correct: dict[str, int] = defaultdict(int)
    per_label_total: dict[str, int] = defaultdict(int)
    per_label_correct: dict[str, int] = defaultdict(int)

    for row, iv in zip(eval_rows, intent_vecs):
        kind = row.get("kind", "")
        per_kind_total[kind] += 1

        scored = [(cap_score(iv, label_trigger_vecs[label], top_k), label) for label in labels]
        scored.sort(reverse=True)
        gate = select_with_margin(scored, threshold, margin)

        gold = row.get("label")
        if gold is None:
            # NULL prompt — gate must NOT fire.
            null_total += 1
            if gate is not None:
                null_fp += 1
            else:
                per_kind_correct[kind] += 1
            continue

        # Positive prompt — gate must fire AND pick the right label.
        pos_total += 1
        per_label_total[gold] += 1
        in_top3 = any(lab == gold for _, lab in scored[:3])
        if in_top3:
            pos_top3 += 1
        if scored and scored[0][1] == gold:
            pos_top1 += 1
            margins.append(scored[0][0] - (scored[1][0] if len(scored) >= 2 else 0.0))
            if gate is not None and gate[1] == gold:
                pos_gate_correct += 1
                per_kind_correct[kind] += 1
                per_label_correct[gold] += 1
            elif gate is None:
                pos_abstain_wrong += 1

    out = {
        "model": model_path,
        "n_eval": len(eval_rows),
        "n_positives": pos_total,
        "n_nulls": null_total,
        "top1_acc": (pos_top1 / pos_total) if pos_total else 0.0,
        "top3_acc": (pos_top3 / pos_total) if pos_total else 0.0,
        "gate_acc": (pos_gate_correct / pos_total) if pos_total else 0.0,
        "abstain_on_pos": (pos_abstain_wrong / pos_total) if pos_total else 0.0,
        "null_fpr": (null_fp / null_total) if null_total else 0.0,
        "mean_top1_margin": (float(np.mean(margins)) if margins else 0.0),
        "per_kind": {
            k: {
                "n": per_kind_total[k],
                "correct": per_kind_correct[k],
                "rate": (per_kind_correct[k] / per_kind_total[k]) if per_kind_total[k] else 0.0,
            }
            for k in sorted(per_kind_total)
        },
        "per_label_recall": {
            lab: {
                "n": per_label_total[lab],
                "correct": per_label_correct[lab],
                "rate": (per_label_correct[lab] / per_label_total[lab]) if per_label_total[lab] else 0.0,
            }
            for lab in sorted(per_label_total)
        },
        "settings": {
            "top_k": top_k,
            "threshold": threshold,
            "margin": margin,
        },
    }
    return out


def print_report(rep: dict) -> None:
    print()
    print(f"model:           {rep['model']}")
    print(f"eval set:        n={rep['n_eval']} (positives={rep['n_positives']}, nulls={rep['n_nulls']})")
    print(f"gate settings:   top_k={rep['settings']['top_k']}  "
          f"threshold={rep['settings']['threshold']}  margin={rep['settings']['margin']}")
    print()
    print(f"top1_acc:         {rep['top1_acc']:.3f}     ← positives ranked first")
    print(f"top3_acc:         {rep['top3_acc']:.3f}     ← gold in top-3")
    print(f"gate_acc:         {rep['gate_acc']:.3f}     ← runtime gate fires AND picks right")
    print(f"abstain_on_pos:   {rep['abstain_on_pos']:.3f}     ← positive but gate abstained (recall loss)")
    print(f"null_fpr:         {rep['null_fpr']:.3f}     ← NULL prompt but gate fired (false positive)")
    print(f"mean_top1_margin: {rep['mean_top1_margin']:.3f}     ← top1-top2 on correct positives")
    print()
    print("per-kind breakdown:")
    for k, v in rep["per_kind"].items():
        print(f"  {k:<22} n={v['n']:>4}  correct={v['correct']:>4}  rate={v['rate']:.3f}")
    weakest = sorted(rep["per_label_recall"].items(), key=lambda x: x[1]["rate"])[:10]
    if weakest:
        print()
        print("weakest 10 capabilities (recall on positives):")
        for lab, v in weakest:
            print(f"  {lab:<32} n={v['n']:>3}  correct={v['correct']:>3}  rate={v['rate']:.3f}")


# ---------------------------------------------------------------------------
# Baseline diff
# ---------------------------------------------------------------------------


def compare_to_baseline(rep: dict, baseline_path: Path,
                        top1_tol: float, fpr_tol: float, per_label_tol: float) -> tuple[bool, list[str]]:
    """Returns (passed, regressions). `passed=False` and a non-empty
    `regressions` list block the publish."""
    if not baseline_path.exists():
        return True, [f"no baseline at {baseline_path}; this run will become the baseline if --write-baseline is used"]
    baseline = json.loads(baseline_path.read_text())
    regs: list[str] = []

    if rep["top1_acc"] < baseline.get("top1_acc", 0.0) - top1_tol:
        regs.append(
            f"top1_acc regressed: {rep['top1_acc']:.3f} < "
            f"{baseline['top1_acc']:.3f} - {top1_tol:.3f}"
        )
    if rep["gate_acc"] < baseline.get("gate_acc", 0.0) - top1_tol:
        regs.append(
            f"gate_acc regressed: {rep['gate_acc']:.3f} < "
            f"{baseline['gate_acc']:.3f} - {top1_tol:.3f}"
        )
    if rep["null_fpr"] > baseline.get("null_fpr", 0.0) + fpr_tol:
        regs.append(
            f"null_fpr regressed: {rep['null_fpr']:.3f} > "
            f"{baseline['null_fpr']:.3f} + {fpr_tol:.3f}"
        )

    base_per_label = baseline.get("per_label_recall", {})
    for lab, v in rep["per_label_recall"].items():
        if lab not in base_per_label:
            continue
        base_rate = base_per_label[lab]["rate"]
        if v["rate"] < base_rate - per_label_tol:
            regs.append(
                f"per-label recall regressed for '{lab}': "
                f"{v['rate']:.3f} < {base_rate:.3f} - {per_label_tol:.3f}"
            )

    return (not regs), regs


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True,
                    help="checkpoint dir or HF id of the bi-encoder to evaluate")
    ap.add_argument("--config", type=Path,
                    default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--eval-set", type=Path, default=None,
                    help="override eval.real_set_path from the config")
    ap.add_argument("--pairs", type=Path, default=None,
                    help="trigger source (defaults to model/data/pairs.jsonl)")
    ap.add_argument("--baseline", type=Path, default=None,
                    help="path to baseline JSON for regression comparison")
    ap.add_argument("--write-baseline", type=Path, default=None,
                    help="if set, write the current report as the new baseline")
    ap.add_argument("--top1-tol", type=float, default=0.01)
    ap.add_argument("--fpr-tol", type=float, default=0.01)
    ap.add_argument("--per-label-tol", type=float, default=0.05)
    ap.add_argument("--json-out", type=Path, default=None,
                    help="dump the full report as JSON (in addition to printing)")
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    eval_cfg = cfg.get("eval", {})
    root = Path(__file__).resolve().parents[1]

    eval_path = args.eval_set or (root / eval_cfg.get("real_set_path", "data/eval_real.jsonl"))
    if not eval_path.exists():
        raise SystemExit(f"missing eval set: {eval_path}\n"
                         f"run: uv run python scripts/build_eval_seed.py")

    pairs_path = args.pairs or (root / cfg["data"]["pairs_path"])
    if not pairs_path.exists():
        raise SystemExit(f"missing pairs.jsonl: {pairs_path} — run build_dataset.py first")

    eval_rows = [json.loads(line) for line in eval_path.read_text().splitlines() if line.strip()]
    triggers_by_cap = load_triggers_from_pairs(pairs_path)

    top_k = int(eval_cfg.get("runtime_top_k", 3))
    threshold = float(eval_cfg.get("runtime_threshold", 0.55))
    margin = float(eval_cfg.get("runtime_margin", 0.08))

    rep = evaluate(args.model, eval_rows, triggers_by_cap, top_k, threshold, margin)
    print_report(rep)

    if args.json_out:
        args.json_out.write_text(json.dumps(rep, indent=2))
        print(f"\nwrote full report to {args.json_out}")

    baseline_path = args.baseline or (root / eval_cfg.get("baselines_path", "eval_baselines.json"))
    if args.write_baseline:
        args.write_baseline.write_text(json.dumps(rep, indent=2))
        print(f"\nwrote baseline to {args.write_baseline}")
        return 0

    passed, regs = compare_to_baseline(rep, baseline_path,
                                       args.top1_tol, args.fpr_tol, args.per_label_tol)
    if not passed:
        print()
        print("=" * 70)
        print("REGRESSION DETECTED — publish would be blocked.")
        print("=" * 70)
        for r in regs:
            print(f"  - {r}")
        print()
        print("Override with `bin/publish --force` only after manual confirmation.")
        return 1

    if baseline_path.exists():
        print()
        print(f"OK — no regression vs {baseline_path}")
    else:
        print()
        print(f"OK — no baseline at {baseline_path} (first run; record with --write-baseline)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
