"""Routing eval: does a task brief reach its agent under the runtime's rule?

Mirrors octomind/src/mcp/orchestration/tap_route.rs: the brief and each
candidate's "<title>. <description>" are embedded, candidates are ranked by
cosine, and the best one gets the task iff

  top1 >= ROUTE_THRESHOLD  and  top1 - top2 >= ROUTE_MARGIN

Who the candidates are depends on the caller (resolver.rs
`reachable_specialists`), so every eval brief is scored three ways:

  domain   the brief's own domain, as its lead sees it: every member but the
           lead (`chief`). A brief written for the lead is scored against the
           whole domain, as another member would see it.
  all      every agent: a caller that is not a tap agent reaches all of them.
  foreign  another domain's members. Nothing there should take the brief.

Per scenario and (threshold, margin):

  handoff  the gate fires and picks the brief's agent
  wrong    the gate fires and picks another agent: a silent wrong handoff
  fired    foreign only: the gate fires at all

A refusal costs the caller one turn, a wrong handoff is not noticed, so the
recommended point maximises `handoff` in the domain scenario while `wrong`
and `fired` stay under their caps.

  uv run python scripts/eval_route.py --model checkpoints/<run>
  uv run python scripts/eval_route.py --model checkpoints/<run>/onnx --onnx-file model_quantized.onnx
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from eval_gate import load_encoder  # noqa: E402

# The agent that leads a domain (octomind `ORCHESTRATOR_SPEC`).
LEAD = "chief"
# How many other domains each brief is scored against in the foreign scenario.
FOREIGN_DOMAINS_PER_BRIEF = 2
# The decision seam shortlists this many candidates (octomind `TAP_TOP_K`).
SHORTLIST = 16

# Caps for the recommended operating point: the share of briefs handed to the
# wrong agent, and the share of foreign briefs that get handed to anyone.
MAX_WRONG = 0.02
MAX_FIRED = 0.03

DEFAULT_THRESHOLDS = "0.40,0.45,0.50,0.52,0.55,0.58,0.60,0.62,0.65,0.67,0.70,0.72,0.75,0.78,0.80"
DEFAULT_MARGINS = "0.00,0.02,0.03,0.04,0.05,0.06,0.08,0.10,0.12,0.15"


def load_agents(path: Path) -> list[dict]:
    """data/raw_agents.jsonl: {tag, domain, text} per agent."""
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_eval_briefs(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    return [r for r in rows if r["split"] == "eval"]


def score_rows(encoder, agents: list[dict], briefs: list[dict], seed: int = 42) -> list[dict]:
    """One row per (brief, scenario): the top two scores and who won.

    Row: {scenario, style, gold, top1, s1, s2, rank}. `gold` is None in the
    foreign scenario; `rank` is the gold agent's 0-based position, None there.
    `s2` is 0.0 for a single candidate, as in the runtime's `select_with_margin`.
    """
    agent_vecs = encoder.encode([a["text"] for a in agents], normalize_embeddings=True, convert_to_numpy=True)
    brief_vecs = encoder.encode([b["brief"] for b in briefs], normalize_embeddings=True, convert_to_numpy=True)

    index = {a["tag"]: i for i, a in enumerate(agents)}
    by_domain: dict[str, list[int]] = defaultdict(list)
    for i, agent in enumerate(agents):
        by_domain[agent["domain"]].append(i)

    def members(domain: str) -> list[int]:
        """The domain as its lead sees it."""
        return [i for i in by_domain[domain] if agents[i]["tag"] != f"{domain}:{LEAD}"]

    def ranked(vec: np.ndarray, candidates: list[int]) -> list[tuple[float, int]]:
        scores = agent_vecs[candidates] @ vec
        order = np.argsort(-scores)
        return [(float(scores[j]), candidates[j]) for j in order]

    def row(scenario: str, brief: dict, gold: int | None, order: list[tuple[float, int]]) -> dict:
        return {
            "scenario": scenario,
            "style": brief["style"],
            "gold": agents[gold]["tag"] if gold is not None else None,
            "top1": agents[order[0][1]]["tag"],
            "s1": order[0][0],
            "s2": order[1][0] if len(order) > 1 else 0.0,
            "rank": next(k for k, (_, i) in enumerate(order) if i == gold) if gold is not None else None,
        }

    rng = random.Random(seed)
    foreign_pool = sorted(d for d in by_domain if members(d))
    out: list[dict] = []
    for brief, vec in zip(briefs, brief_vecs):
        gold = index.get(brief["agent"])
        if gold is None:
            continue  # the agent was removed after the brief was written
        domain = agents[gold]["domain"]
        own = by_domain[domain] if agents[gold]["tag"] == f"{domain}:{LEAD}" else members(domain)
        out.append(row("domain", brief, gold, ranked(vec, own)))
        out.append(row("all", brief, gold, ranked(vec, list(range(len(agents))))))
        for other in rng.sample([d for d in foreign_pool if d != domain], FOREIGN_DOMAINS_PER_BRIEF):
            out.append(row("foreign", brief, None, ranked(vec, members(other))))
    return out


def route_metrics(rows: list[dict], threshold: float, margin: float) -> dict[str, dict]:
    """Per scenario: n, handoff, wrong, fired rates at one operating point."""
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"n": 0, "handoff": 0, "wrong": 0})
    for r in rows:
        c = counts[r["scenario"]]
        c["n"] += 1
        if r["s1"] >= threshold and r["s1"] - r["s2"] >= margin:
            c["handoff" if r["top1"] == r["gold"] else "wrong"] += 1
    return {
        scenario: {
            "n": c["n"],
            "handoff": c["handoff"] / c["n"],
            "wrong": c["wrong"] / c["n"],
        }
        for scenario, c in counts.items()
    }


def ranking_metrics(rows: list[dict]) -> dict[str, dict]:
    """Threshold-free quality per scenario: top-1 accuracy and shortlist recall."""
    out: dict[str, dict] = {}
    for scenario in ("domain", "all"):
        ranks = [r["rank"] for r in rows if r["scenario"] == scenario]
        out[scenario] = {
            "top1_acc": sum(1 for k in ranks if k == 0) / len(ranks),
            "shortlist_recall": sum(1 for k in ranks if k < SHORTLIST) / len(ranks),
        }
    return out


def best_point(
    rows_per_cpu: list[list[dict]],
    thresholds: list[float],
    margins: list[float],
    max_wrong: float,
    max_fired: float,
) -> dict | None:
    """The (threshold, margin) with the highest domain handoff rate whose wrong
    rate (domain and all) and foreign fired rate stay under the caps. With
    several score sets (one per CPU kind) every cap must hold on each of them
    and the handoff rate compared is the lowest one."""
    best = None
    for t in thresholds:
        for m in margins:
            per_cpu = [route_metrics(rows, t, m) for rows in rows_per_cpu]
            if any(
                x["domain"]["wrong"] > max_wrong or x["all"]["wrong"] > max_wrong or x["foreign"]["wrong"] > max_fired
                for x in per_cpu
            ):
                continue
            handoff = min(x["domain"]["handoff"] for x in per_cpu)
            if best is None or handoff > best["handoff"]:
                best = {"threshold": t, "margin": m, "handoff": handoff, "per_cpu": per_cpu}
    return best


def print_styles(rows: list[dict], threshold: float, margin: float) -> None:
    """Domain scenario per brief style. `long` is the one cut at the runtime's
    512-token window, so it shows whether a real lead brief still routes."""
    by_style: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        if r["scenario"] == "domain":
            by_style[r["style"]].append(r)
    for style, style_rows in sorted(by_style.items()):
        m = route_metrics(style_rows, threshold, margin)["domain"]
        top1 = sum(1 for r in style_rows if r["rank"] == 0) / len(style_rows)
        print(f"  {style:<8} n={m['n']:>5}  top1_acc={top1:.3f}  handoff={m['handoff']:.3f}  wrong={m['wrong']:.3f}")


def print_point(metrics: dict[str, dict]) -> None:
    for scenario in ("domain", "all"):
        m = metrics[scenario]
        print(f"  {scenario:<8} n={m['n']:>5}  handoff={m['handoff']:.3f}  wrong={m['wrong']:.3f}")
    m = metrics["foreign"]
    print(f"  {'foreign':<8} n={m['n']:>5}  fired={m['wrong']:.3f}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", type=str, required=True, help="checkpoint dir or HF id; with --onnx-file, the dir holding the graph")
    ap.add_argument("--onnx-file", type=str, default=None)
    ap.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "configs" / "default.yaml")
    ap.add_argument("--threshold-grid", type=str, default=DEFAULT_THRESHOLDS)
    ap.add_argument("--margin-grid", type=str, default=DEFAULT_MARGINS)
    ap.add_argument("--max-wrong", type=float, default=MAX_WRONG, help="cap on the wrong-handoff rate (domain and all)")
    ap.add_argument("--max-fired", type=float, default=MAX_FIRED, help="cap on the foreign fired rate")
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
    for scenario, m in ranking.items():
        print(f"  {scenario:<8} top1_acc={m['top1_acc']:.3f}  top{SHORTLIST}_recall={m['shortlist_recall']:.3f}")

    threshold, margin = float(eval_cfg["route_threshold"]), float(eval_cfg["route_margin"])
    configured = route_metrics(rows, threshold, margin)
    print(f"\nat the configured point (threshold={threshold}, margin={margin}):")
    print_point(configured)

    best = best_point(
        [rows],
        [float(x) for x in args.threshold_grid.split(",")],
        [float(x) for x in args.margin_grid.split(",")],
        args.max_wrong,
        args.max_fired,
    )
    if best:
        print(f"\nbest point with wrong <= {args.max_wrong} and foreign fired <= {args.max_fired}: "
              f"threshold={best['threshold']:.2f} margin={best['margin']:.2f}")
        print_point(best["per_cpu"][0])
        print("\nper brief style at that point (domain scenario):")
        print_styles(rows, best["threshold"], best["margin"])
    else:
        print(f"\nno point keeps wrong <= {args.max_wrong} and foreign fired <= {args.max_fired}")

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
