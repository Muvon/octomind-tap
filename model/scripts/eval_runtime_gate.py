"""Faithful reproduction of octomind's runtime capability-routing gate.

This mirrors `octomind/src/mcp/runtime/capability.rs::capability_routing_diversity_fixtures`
EXACTLY — same triggers, same fixtures, same production constants — so a model
can be judged under real deployment conditions BEFORE publishing.

Why this exists: the older offline harness (compare_bases.py) judged each model
at its OWN best swept threshold and on the augmented trigger corpus, so it
flattered models that don't actually fire at the production 0.45 gate. This
script removes that gap. candle (the runtime embedder) reproduces
sentence-transformers to ~5 decimals, so a Python score here == the Rust runtime.

The runtime decision is: gate short inputs out, else
  score(cap) = mean of top-3 cosine(intent, cap.triggers)
  fire iff  top1 >= THRESHOLD  AND  (top1 - top2) >= MARGIN

Pass == every category meets its floor. Exit code 0 on pass, 1 on fail, so a
training loop can gate on it:  python scripts/eval_runtime_gate.py --model <path>

KEEP TRIGGERS/FIXTURES IN SYNC with capability.rs if that test changes.
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
from sentence_transformers import SentenceTransformer

# --- Production constants (capability.rs / skill_auto.rs) -------------------
THRESHOLD = 0.45  # AUTO_ACTIVATE_THRESHOLD
MARGIN = 0.08  # AUTO_ACTIVATE_MARGIN
TOP_K = 3  # runtime mean-of-top-K
MIN_NONWS_CHARS = 8  # MIN_INTENT_NON_WS_CHARS (short-input gate)

# --- Capabilities + triggers (mirror capability.rs make_cap_with_triggers) --
CAPS: dict[str, list[str]] = {
    "database-postgres": [
        "query a postgres database",
        "EXPLAIN ANALYZE a slow postgres query",
        "look at the postgres schema",
        "investigate a Postgres query plan",
        "check rows in a postgres table",
        "run SQL against postgres",
    ],
    "filesystem": [
        "read the contents of a file",
        "view the contents of a file",
        "edit a file on disk",
        "list directory contents",
        "search files for a pattern",
        "find files by name",
    ],
    "codesearch-graph": [
        "trace code dependencies",
        "find what calls this function",
        "graph traversal of code",
    ],
    "codesearch-structural": [
        "find a function or symbol",
        "locate a class or method",
        "view file signatures",
        "AST search",
    ],
    "codesearch-semantic": [
        "find code by what it does",
        "search code by description",
        "natural-language code search",
    ],
    "docker": [
        "list running docker containers",
        "build a docker image",
        "inspect a container's logs",
        "run a docker compose service",
        "stop a docker container",
    ],
    "kubernetes": [
        "list pods in a kubernetes cluster",
        "check kubectl logs",
        "inspect a kubernetes deployment status",
        "deploy a helm chart to the cluster",
        "troubleshoot a failing pod",
        "scale a kubernetes deployment",
        "apply a kubectl manifest",
    ],
    "webfetch": [
        "fetch a URL's content",
        "download a webpage",
        "get the contents of a web page",
        "retrieve a web resource",
    ],
    "messaging-slack": [
        "send a slack message",
        "post to a slack channel",
        "search slack history",
        "look up a slack thread",
        "list slack channels",
    ],
    "calendar": [
        "schedule a meeting",
        "check my calendar for tomorrow",
        "find a free slot next week",
        "create a calendar event",
        "list upcoming events",
    ],
    "maps": [
        "how do I drive from here to there",
        "give me directions on the map",
        "how far is it between these two places",
        "restaurants near this location on the map",
        "how long does it take to get there by car",
    ],
}

# --- Fixtures: (category, intent, expected_cap_or_None) ---------------------
FIXTURES: list[tuple[str, str, str | None]] = [
    ("paraphrase", "explain analyze this slow postgres query", "database-postgres"),
    ("paraphrase", "why is this postgres query so slow", "database-postgres"),
    ("paraphrase", "show me the schema for the users table in postgres", "database-postgres"),
    ("paraphrase", "inspect the postgres execution plan", "database-postgres"),
    ("paraphrase", "search the codebase for callers of save_user", "codesearch-graph"),
    ("paraphrase", "find where validate_token is defined in the code", "codesearch-structural"),
    ("paraphrase", "show me running docker containers", "docker"),
    ("paraphrase", "docker ps please", "docker"),
    ("paraphrase", "build a docker image from this Dockerfile", "docker"),
    ("paraphrase", "kubectl get pods in my cluster", "kubernetes"),
    ("paraphrase", "what pods are running in my k8s cluster", "kubernetes"),
    ("paraphrase", "fetch the contents of this URL", "webfetch"),
    ("paraphrase", "download this webpage so I can read it", "webfetch"),
    ("paraphrase", "what files are in the current directory", "filesystem"),
    ("paraphrase", "read the contents of package.json", "filesystem"),
    ("paraphrase", "send a slack message to the team", "messaging-slack"),
    ("paraphrase", "post in our slack channel about the launch", "messaging-slack"),
    ("paraphrase", "what meetings do I have tomorrow", "calendar"),
    ("paraphrase", "schedule a 30 minute meeting with Bob", "calendar"),
    ("paraphrase", "how do I get to the airport from my office", "maps"),
    ("paraphrase", "find coffee shops near this location", "maps"),
    ("ambiguous", "send the docker container logs to our slack channel", None),
    ("short", "try", None),
    ("short", "ok", None),
    ("short", "yes", None),
    ("short", "go", None),
    ("short", "next", None),
    ("short", "do it", None),
    ("short", "thanks", None),
    ("chitchat", "what's the weather today", None),
    ("chitchat", "good morning how are you", None),
    ("chitchat", "tell me a joke please", None),
]

# Per-category accuracy floors (capability.rs `floors`).
FLOORS: dict[str, float] = {
    "short": 1.00,
    "paraphrase": 0.75,
    "chitchat": 0.66,
    "ambiguous": 0.33,
}


def has_enough_signal(intent: str) -> bool:
    return sum(1 for c in intent if not c.isspace()) >= MIN_NONWS_CHARS


def cap_score(intent_vec: np.ndarray, trigger_vecs: np.ndarray) -> float:
    sims = np.sort(trigger_vecs @ intent_vec)
    return float(sims[-TOP_K:].mean())


def select_with_margin(scored: list[tuple[float, str]]) -> str | None:
    """Mirror capability.rs::select_with_margin (top1>=THRESHOLD, gap>=MARGIN)."""
    if not scored:
        return None
    scored = sorted(scored, key=lambda x: -x[0])
    top1 = scored[0][0]
    if top1 < THRESHOLD:
        return None
    top2 = scored[1][0] if len(scored) >= 2 else 0.0
    if top1 - top2 < MARGIN:
        return None
    return scored[0][1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="muvon/octomind-embed",
                    help="model id or local path")
    ap.add_argument("--verbose", action="store_true",
                    help="print top-3 scores for every miss")
    args = ap.parse_args()

    print(f"=== runtime gate eval: {args.model} (tau={THRESHOLD}, delta={MARGIN}, top_k={TOP_K}) ===")
    model = SentenceTransformer(args.model)

    labels = list(CAPS.keys())
    trig_vecs = {
        c: model.encode(CAPS[c], normalize_embeddings=True, convert_to_numpy=True)
        for c in labels
    }

    # category -> [correct, total, misses]
    totals: dict[str, list] = {}
    for cat, intent, expected in FIXTURES:
        t = totals.setdefault(cat, [0, 0, []])
        t[1] += 1

        if not has_enough_signal(intent):
            outcome, ranked = None, []
        else:
            iv = model.encode(intent, normalize_embeddings=True, convert_to_numpy=True)
            scored = [(cap_score(iv, trig_vecs[c]), c) for c in labels]
            ranked = sorted(scored, key=lambda x: -x[0])
            outcome = select_with_margin(scored)

        if outcome == expected:
            t[0] += 1
        else:
            top3 = ", ".join(f"{c}={s:.3f}" for s, c in ranked[:3]) or "<gated>"
            t[2].append(f"{intent!r} -> expected {expected!r}, got {outcome!r}  [{top3}]")

    print("\nDiversity gate breakdown:")
    for cat in sorted(totals):
        correct, total, misses = totals[cat]
        acc = correct / total if total else 1.0
        print(f"  {cat:>12}: {correct:>2}/{total:<2}  ({acc:.2f})")
        if args.verbose:
            for m in misses:
                print(f"                - {m}")

    print("\nFloors:")
    passed = True
    for cat, floor in FLOORS.items():
        correct, total, _ = totals.get(cat, [0, 0, []])
        acc = correct / total if total else 0.0
        ok = acc >= floor
        passed &= ok
        print(f"  {cat:>12}: {acc:.2f} >= {floor:.2f}  {'PASS' if ok else 'FAIL'}")

    print(f"\n{'== PASS ==' if passed else '== FAIL =='}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
