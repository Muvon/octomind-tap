"""Audit the capability-routing training data for issues that sabotage
fine-tuning — chiefly FALSE NEGATIVES (the same/near-same surface living
under two labels). Contrastive losses (MNRL) push every in-batch /
triplet negative away from the anchor; if a "negative" is actually a
legitimate paraphrase of the anchor's intent, the model is forced to
separate two things that *should* be close, which collapses the
inter-cluster margin the runtime gate relies on.

Checks (string-based ones need no model and run instantly):
  1. cross-label EXACT-duplicate surfaces in pairs.jsonl
  2. cross-label surfaces that differ ONLY by the shared augmentation
     template (template-induced collisions)
  3. triplet false-negatives:
       a. exact: `negative` text is also a surface of the anchor's label
       b. model: cos(anchor, negative) >= frac * cos(anchor, positive)
  4. holdout / train leakage (identical surface in both)
  5. label cardinality + balance
  6. eval_real gold-label coverage vs the trigger corpus

Usage:
  uv run python scripts/audit_data.py                 # string checks only
  uv run python scripts/audit_data.py --model sentence-transformers/all-MiniLM-L6-v2
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


def load_jsonl(p: Path):
    with p.open() as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


# Strip the augmentation wrapper so we can detect surfaces that are identical
# except for a shared template ("can you help me X" vs "how do I X"). Mirrors
# the TEMPLATES/prefixes in build_dataset.py at a coarse level.
_WRAP = re.compile(
    r"^(i\s+|we\s+)?(need to|want to|wanna|gotta|trying to|just|please|"
    r"can you( help me)?|could you|would you|help me|how (do|can) i|how to|"
    r"let'?s|we should|now|next,?|ok now|and then|i'?m trying to)\s+",
    re.I,
)
_MTPREFIX = re.compile(
    r"^(earlier we set up the project; now|following up:|as i was saying —|"
    r"back to what we discussed:|ok so given that context,|"
    r"ignore the previous output\.|let'?s try again —|scratch that\.|"
    r"alright,|circling back:)\s*",
    re.I,
)


def core(s: str) -> str:
    s = s.strip()
    s = _MTPREFIX.sub("", s)
    s = _WRAP.sub("", s)
    return s.rstrip("?.").strip().lower()


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    ap.add_argument("--data", type=Path, default=root / "data")
    ap.add_argument("--model", type=str, default=None,
                    help="encode triplets to measure model-based false-negative rate")
    ap.add_argument("--frac", type=float, default=0.95,
                    help="false-neg if cos(a,neg) >= frac*cos(a,pos)")
    ap.add_argument("--caps", type=Path, default=root.parent / "capabilities")
    ap.add_argument("--skills", type=Path, default=root.parent / "skills")
    args = ap.parse_args()

    pairs = list(load_jsonl(args.data / "pairs.jsonl"))
    trips = list(load_jsonl(args.data / "triplets.jsonl")) if (args.data / "triplets.jsonl").exists() else []
    holds = list(load_jsonl(args.data / "holdout.jsonl")) if (args.data / "holdout.jsonl").exists() else []

    # surfaces per label (exclude _oos from the "real cap" collision view but
    # report separately — _oos colliding with a real cap IS a real problem).
    label_surfaces: dict[str, set[str]] = defaultdict(set)
    surface_labels: dict[str, set[str]] = defaultdict(set)
    for r in pairs:
        for key in ("anchor", "positive"):
            s = r[key]
            label_surfaces[r["label"]].add(s)
            surface_labels[s].add(r["label"])

    print(f"== corpus ==")
    print(f"pairs rows={len(pairs)}  labels={len(label_surfaces)}  "
          f"unique surfaces={len(surface_labels)}  triplets={len(trips)}  holdout={len(holds)}")

    # --- 1. exact cross-label duplicate surfaces ---
    exact_collisions = {s: labs for s, labs in surface_labels.items() if len(labs) > 1}
    print(f"\n== 1. EXACT cross-label duplicate surfaces ==")
    print(f"{len(exact_collisions)} surfaces appear under >1 label "
          f"({100*len(exact_collisions)/max(1,len(surface_labels)):.1f}% of unique surfaces)")
    pair_counter = Counter()
    for s, labs in exact_collisions.items():
        for a in sorted(labs):
            for b in sorted(labs):
                if a < b:
                    pair_counter[(a, b)] += 1
    for (a, b), n in pair_counter.most_common(15):
        print(f"   {n:>4}  {a}  <->  {b}")

    # --- 2. template-stripped cross-label collisions ---
    core_labels: dict[str, set[str]] = defaultdict(set)
    for s, labs in surface_labels.items():
        core_labels[core(s)].update(labs)
    core_coll = {c: labs for c, labs in core_labels.items() if len(labs) > 1 and c}
    print(f"\n== 2. TEMPLATE-STRIPPED cross-label collisions ==")
    print(f"{len(core_coll)} core phrases map to >1 label "
          f"({100*len(core_coll)/max(1,len(core_labels)):.1f}% of core phrases)")
    examples = sorted(core_coll.items(), key=lambda x: -len(x[1]))[:10]
    for c, labs in examples:
        print(f"   [{', '.join(sorted(labs))}]  <=  \"{c[:60]}\"")

    # --- 3a. triplet exact false-negatives ---
    fn_exact = 0
    neg_is_own_label = 0
    for t in trips:
        own = label_surfaces.get(t["label"], set())
        if t["negative"] in own:
            fn_exact += 1
        if t.get("neg_label") == t["label"]:
            neg_is_own_label += 1
    print(f"\n== 3a. triplet EXACT false-negatives ==")
    print(f"{fn_exact}/{len(trips)} triplets ({100*fn_exact/max(1,len(trips)):.1f}%) "
          f"have a negative that is ALSO a surface of the anchor's own label")
    print(f"{neg_is_own_label} triplets have neg_label == label (self-negative)")

    # --- 4. label balance ---
    sizes = {l: len(s) for l, s in label_surfaces.items()}
    ssz = sorted(sizes.items(), key=lambda x: x[1])
    print(f"\n== 4. label balance (surfaces/label) ==")
    print(f"min={ssz[0][1]} ({ssz[0][0]})  max={ssz[-1][1]} ({ssz[-1][0]})  "
          f"median={ssz[len(ssz)//2][1]}")
    print("   smallest 5:", [f"{l}={n}" for l, n in ssz[:5]])

    # --- 5. holdout/train leakage ---
    train_surf = set(surface_labels)
    leak = sum(1 for h in holds if h["intent"] in train_surf)
    print(f"\n== 5. holdout/train leakage ==")
    print(f"{leak}/{len(holds)} holdout intents ({100*leak/max(1,len(holds)):.1f}%) "
          f"appear verbatim in training surfaces")

    # --- 6. eval_real coverage ---
    ev = args.data / "eval_real.jsonl"
    if ev.exists():
        evrows = list(load_jsonl(ev))
        gold = {r["label"] for r in evrows if r.get("label")}
        missing = sorted(gold - set(label_surfaces))
        print(f"\n== 6. eval_real coverage ==")
        print(f"{len(gold)} gold labels; {len(missing)} missing from pairs corpus: {missing}")

    # --- 3b. model-based false-negative rate (optional) ---
    if args.model:
        import numpy as np
        from sentence_transformers import SentenceTransformer
        print(f"\n== 3b. model-based triplet false-negatives ({args.model}) ==")
        m = SentenceTransformer(args.model)
        uniq = sorted({x for t in trips for x in (t["anchor"], t["positive"], t["negative"])})
        idx = {s: i for i, s in enumerate(uniq)}
        V = m.encode(uniq, normalize_embeddings=True, convert_to_numpy=True,
                     batch_size=256, show_progress_bar=False)
        fn = 0
        worse = 0
        for t in trips:
            a, p, n = V[idx[t["anchor"]]], V[idx[t["positive"]]], V[idx[t["negative"]]]
            cap, can = float(a @ p), float(a @ n)
            if can >= args.frac * cap:
                fn += 1
            if can >= cap:
                worse += 1
        print(f"{fn}/{len(trips)} ({100*fn/max(1,len(trips)):.1f}%) negatives score >= "
              f"{args.frac}*pos  (NV-Retriever would drop these)")
        print(f"{worse}/{len(trips)} ({100*worse/max(1,len(trips)):.1f}%) negatives score "
              f">= the positive (hard false negatives)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
