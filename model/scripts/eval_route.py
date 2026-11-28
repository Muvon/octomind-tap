"""Routing eval: does a task brief reach its agent under the runtime's rule?

Mirrors octomind/src/mcp/orchestration/tap_route.rs: the brief and each
agent's "<title>. <description>" are embedded, agents are ranked by cosine,
and the best one gets the task iff

  top1 >= ROUTE_THRESHOLD  and  top1 - top2 >= ROUTE_MARGIN

Every eval-split brief (`data/agent_briefs.jsonl`) is ranked against all base
agents, as a caller that reaches every one of them sees them. Three numbers:

  top1_acc  the brief's own agent ranks first (threshold-free)
  handoff   the gate fires and picks the brief's agent
  wrong     the gate fires and picks another agent: a silent wrong handoff

A refusal costs the caller one turn, a wrong handoff is not noticed, so the
recommended point maximises `handoff` while `wrong` stays under its cap.

  uv run python scripts/eval_route.py --model checkpoints/<run>
  uv run python scripts/eval_route.py --model checkpoints/<run>/onnx --onnx-file model_quantized.onnx
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import load_encoder  # noqa: E402

# The decision seam shortlists this many candidates (octomind `TAP_TOP_K`).
SHORTLIST = 16

# Cap for the recommended operating point: the share of briefs handed to the
# wrong agent.
MAX_WRONG = 0.02

DEFAULT_THRESHOLDS = "0.40,0.45,0.50,0.52,0.55,0.58,0.60,0.62,0.65,0.67,0.70,0.72,0.75,0.78,0.80"
DEFAULT_MARGINS = "0.00,0.02,0.03,0.04,0.05,0.06,0.08,0.10,0.12,0.15"


def load_agents(path: Path) -> list[dict]:
    """data/raw_agents.jsonl: {tag, text} per agent."""
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_eval_briefs(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"missing {path}. Run: uv run python scripts/augment_agents.py")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [r for r in rows if r["split"] == "eval"]


def score_rows(encoder, agents: list[dict], briefs: list[dict]) -> list[dict]:
    """One row per brief: the top two scores and who won.

    Row: {style, gold, top1, s1, s2, rank}. `rank` is the gold agent's 0-based
    position. `s2` is 0.0 for a single candidate, as in the runtime's
    `select_with_margin`.
    """
    agent_vecs = encoder.encode([a["text"] for a in agents], normalize_embeddings=True, convert_to_numpy=True)
    brief_vecs = encoder.encode([b["brief"] for b in briefs], normalize_embeddings=True, convert_to_numpy=True)

    index = {a["tag"]: i for i, a in enumerate(agents)}
    unknown = sorted({b["agent"] for b in briefs} - set(index))
    if unknown:
        raise SystemExit(f"eval briefs for agents missing from the agent texts: {unknown}")

    out: list[dict] = []
    for brief, vec in zip(briefs, brief_vecs):
        gold = index[brief["agent"]]
        scores = agent_vecs @ vec
        order = np.argsort(-scores)
        out.append({
            "style": brief["style"],
            "gold": brief["agent"],
            "top1": agents[order[0]]["tag"],
            "s1": float(scores[order[0]]),
            "s2": float(scores[order[1]]) if len(order) > 1 else 0.0,
            "rank": int(np.where(order == gold)[0][0]),
        })
    return out


def route_metrics(rows: list[dict], threshold: float, margin: float) -> dict:
    """n, handoff and wrong rates at one operating point."""
    handoff = wrong = 0
    for r in rows:
        if r["s1"] >= threshold and r["s1"] - r["s2"] >= margin:
            if r["top1"] == r["gold"]:
                handoff += 1
            else:
                wrong += 1
    return {"n": len(rows), "handoff": handoff / len(rows), "wrong": wrong / len(rows)}


def ranking_metrics(rows: list[dict]) -> dict:
    """Threshold-free quality: top-1 accuracy and shortlist recall."""
    ranks = [r["rank"] for r in rows]
    return {
        "top1_acc": sum(1 for k in ranks if k == 0) / len(ranks),
        "shortlist_recall": sum(1 for k in ranks if k < SHORTLIST) / len(ranks),
    }


def best_point(
    rows_per_cpu: list[list[dict]],
    thresholds: list[float],
    margins: list[float],
    max_wrong: float,
) -> dict | None:
    """The (threshold, margin) with the highest handoff rate whose wrong rate
    stays under the cap. With several score sets (one per CPU kind) the cap
    must hold on each of them and the handoff rate compared is the lowest one."""
    best = None
    for t in thresholds:
        for m in margins:
            per_cpu = [route_metrics(rows, t, m) for rows in rows_per_cpu]
            if any(x["wrong"] > max_wrong for x in per_cpu):
                continue
            handoff = min(x["handoff"] for x in per_cpu)
            if best is None or handoff > best["handoff"]:
                best = {"threshold": t, "margin": m, "handoff": handoff, "per_cpu": per_cpu}
    return best


def print_styles(rows: list[dict], threshold: float, margin: float) -> None:
    """Per brief style. `long` is the one cut at the runtime's 512-token
    window, so it shows whether a real lead brief still routes."""
    by_style: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_style[r["style"]].append(r)
    for style, style_rows in sorted(by_style.items()):
        m = route_metrics(style_rows, threshold, margin)
        top1 = sum(1 for r in style_rows if r["rank"] == 0) / len(style_rows)
        print(f"  {style:<8} n={m['n']:>5}  top1_acc={top1:.3f}  handoff={m['handoff']:.3f}  wrong={m['wrong']:.3f}")


def print_point(metrics: dict) -> None:
    print(f"  n={metrics['n']:>5}  handoff={metrics['handoff']:.3f}  wrong={metrics['wrong']:.3f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True, help="checkpoint dir or HF id; with --onnx-file, the dir holding the graph")
    ap.add_argument("--onnx-file", type=str, default=None)
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--threshold-grid", type=str, default=DEFAULT_THRESHOLDS)
    ap.add_argument("--margin-grid", type=str, default=DEFAULT_MARGINS)
    ap.add_argument("--max-wrong", type=float, default=MAX_WRONG, help="cap on the wrong-handoff rate")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    cfg = yaml.safe_load(args.config.read_text())
    eval_cfg = cfg["eval"]
    root = Path(__file__).resolve().parents[1]
    agents = load_agents(root / eval_cfg["agents_path"])
    briefs = load_eval_briefs(root / eval_cfg["agent_briefs_path"])

    encoder = load_encoder(args.model, args.onnx_file)
    rows = score_rows(encoder, agents, briefs)

    ranking = ranking_metrics(rows)
    print(f"\nmodel: {args.model}{'/' + args.onnx_file if args.onnx_file else ''}")
    print(f"eval briefs: {len(briefs)} over {len(agents)} agents")
    print(f"  top1_acc={ranking['top1_acc']:.3f}  top{SHORTLIST}_recall={ranking['shortlist_recall']:.3f}")

    threshold, margin = float(eval_cfg["route_threshold"]), float(eval_cfg["route_margin"])
    configured = route_metrics(rows, threshold, margin)
    print(f"\nat the configured point (threshold={threshold}, margin={margin}):")
    print_point(configured)

    best = best_point(
        [rows],
        [float(x) for x in args.threshold_grid.split(",")],
        [float(x) for x in args.margin_grid.split(",")],
        args.max_wrong,
    )
    if best:
        print(f"\nbest point with wrong <= {args.max_wrong}: threshold={best['threshold']:.2f} margin={best['margin']:.2f}")
        print_point(best["per_cpu"][0])
        print("\nper brief style at that point:")
        print_styles(rows, best["threshold"], best["margin"])
    else:
        print(f"\nno point keeps wrong <= {args.max_wrong}")

    if args.json_out:
        args.json_out.write_text(json.dumps({
            "model": args.model,
            "ranking": ranking,
            "configured": {"threshold": threshold, "margin": margin, "metrics": configured},
            "best": best,
        }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
