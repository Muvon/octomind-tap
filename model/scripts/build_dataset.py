"""Walk capabilities/*/config.toml and emit a training dataset.

Outputs three files under model/data/:

  pairs.jsonl     — {anchor, positive, label}
                    In-capability pairs for MNRL training signal.
  triplets.jsonl  — {anchor, positive, negative, label, neg_label}
                    Hard-negative triplets mined with the BASE model.
  holdout.jsonl   — {intent, label}
                    User-phrased intents held out for eval.

Data sources, in priority order:

  1. data/intents.jsonl  (preferred) — produced by scripts/augment_llm.py.
     One {label, intent, source} per line. These are LLM-rewritten user
     paraphrases per authored trigger — the highest-quality signal.

  2. config.toml triggers — always loaded. Expanded with rule-based
     paraphrase templates and verb-synonym substitution to widen the
     linguistic surface.

The two sources are concatenated per capability. With both, you typically
get 30–60 distinct surface forms per trigger, which is enough to train
a sentence-transformer to high precision on the capability-classification
task.

Hard negatives: for each capability we embed its expanded triggers with
the base model, find the top-K most-similar OTHER capabilities by
centroid similarity, and emit explicit contrastive triplets. This is
what makes confusable clusters (e.g. shell vs programming-rust)
separable after fine-tuning.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from itertools import combinations
from pathlib import Path

try:
    import tomllib  # py311+
except ModuleNotFoundError:  # py310
    import tomli as tomllib  # type: ignore[no-redef]


# ---------------------------------------------------------------------------
# Rule-based augmentation
# ---------------------------------------------------------------------------
#
# Two layers: verb synonyms and surface templates. Applied per trigger.
#
# Why: authored triggers ("execute a shell command") are imperative and
# verb-anchored. Real users phrase the same intent as questions, problem
# statements, terse keywords, or with surrounding context. The model must
# learn that all of these map to the same capability.

VERB_SYNONYMS: dict[str, list[str]] = {
    # Action verbs — keep the meaning, swap the surface.
    "execute": ["run", "invoke", "launch", "fire off", "kick off"],
    "run":     ["execute", "invoke", "launch", "trigger", "start"],
    "build":   ["compile", "assemble", "produce", "make"],
    "compile": ["build", "make"],
    "fix":     ["resolve", "debug", "repair", "patch", "troubleshoot"],
    "debug":   ["troubleshoot", "investigate", "diagnose", "fix"],
    "write":   ["author", "create", "implement", "draft"],
    "create":  ["make", "set up", "build", "spin up"],
    "manage":  ["handle", "configure", "administer", "control"],
    "deploy":  ["ship", "publish", "release", "push live"],
    "install": ["add", "set up", "bring in", "pull in"],
    "configure": ["set up", "tune", "adjust", "wire up"],
    "resolve": ["fix", "address", "sort out"],
    "list":    ["show", "enumerate", "see"],
    "inspect": ["check", "look at", "examine", "review"],
    "check":   ["verify", "look at", "inspect"],
    "search":  ["look up", "find", "query", "look for"],
    "find":    ["search for", "look up", "track down"],
    "fetch":   ["pull", "retrieve", "grab", "download"],
    "download": ["fetch", "pull", "grab"],
    "upload":  ["push", "send", "post"],
    "render":  ["draw", "generate", "produce"],
    "generate": ["produce", "create", "make"],
    "remove":  ["delete", "drop", "clean up", "get rid of"],
    "delete":  ["remove", "drop", "wipe", "clear"],
    "send":    ["post", "deliver", "transmit"],
    "stop":    ["halt", "kill", "shut down", "terminate"],
    "start":   ["spin up", "launch", "boot", "kick off"],
    "use":     ["work with", "leverage", "apply"],
    "work":    ["deal", "operate"],
}


# Surface templates. `{t}` is the trigger (with synonyms possibly already
# substituted). `{t_lc}` is lower-cased first word — for templates that
# expect a verb to follow a connector.

TEMPLATES: list[str] = [
    # bare imperative (the authored form)
    "{t}",
    # explicit need / want / try
    "I need to {t_lc}",
    "I want to {t_lc}",
    "I'm trying to {t_lc}",
    "trying to {t_lc}",
    # asks / requests
    "can you {t_lc}",
    "can you help me {t_lc}",
    "could you {t_lc}",
    "would you {t_lc}",
    "please {t_lc}",
    "help me {t_lc}",
    # questions
    "how do I {t_lc}",
    "how can I {t_lc}",
    "how to {t_lc}",
    "what's the way to {t_lc}",
    # collaborative
    "let's {t_lc}",
    "we should {t_lc}",
    # context + need
    "for my project I need to {t_lc}",
    "right now I need to {t_lc}",
    "I just want to {t_lc}",
    # terminal / terse phrasings
    "{t_lc}?",
    "{t}.",
]


def lowercase_first_word(s: str) -> str:
    """Lowercase only the first whitespace-delimited word, preserving the
    rest (so proper nouns inside the phrase keep their casing)."""
    if not s:
        return s
    head, _, tail = s.partition(" ")
    return head.lower() + ((" " + tail) if tail else "")


def substitute_synonyms(trigger: str, rng: random.Random, max_variants: int = 2) -> list[str]:
    """Return up to `max_variants` versions of the trigger with the leading
    verb (if known) swapped for a synonym. Always includes the original.
    """
    words = trigger.split()
    if not words:
        return [trigger]
    head = words[0].lower().strip(",.")
    if head not in VERB_SYNONYMS:
        return [trigger]

    out = [trigger]
    pool = VERB_SYNONYMS[head][:]
    rng.shuffle(pool)
    for syn in pool[:max_variants]:
        new_head = syn[0].upper() + syn[1:] if words[0][0].isupper() else syn
        out.append(" ".join([new_head] + words[1:]))
    return out


def expand_trigger(trigger: str, rng: random.Random) -> list[str]:
    """Generate the full set of rule-based variants for one trigger."""
    out: set[str] = set()
    for variant in substitute_synonyms(trigger, rng):
        t_lc = lowercase_first_word(variant)
        for tpl in TEMPLATES:
            out.add(tpl.format(t=variant, t_lc=t_lc).strip())
    return sorted(out)


# ---------------------------------------------------------------------------
# Sources: TOML triggers + (optional) LLM intents
# ---------------------------------------------------------------------------


def load_triggers(caps_dir: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for cap_dir in sorted(p for p in caps_dir.iterdir() if p.is_dir()):
        cfg = cap_dir / "config.toml"
        if not cfg.exists():
            continue
        data = tomllib.loads(cfg.read_text())
        triggers = [t.strip() for t in data.get("triggers", []) if t.strip()]
        if len(triggers) >= 2:
            out[cap_dir.name] = triggers
        else:
            print(f"[skip] {cap_dir.name}: needs >=2 triggers, has {len(triggers)}", file=sys.stderr)
    return out


def load_llm_intents(path: Path) -> dict[str, list[tuple[str, str]]]:
    """Returns {label: [(source_trigger, intent), ...]}."""
    out: dict[str, list[tuple[str, str]]] = {}
    if not path.exists():
        return out
    with path.open() as f:
        for line in f:
            row = json.loads(line)
            out.setdefault(row["label"], []).append((row.get("source", ""), row["intent"]))
    return out


# ---------------------------------------------------------------------------
# Splits and pair writing
# ---------------------------------------------------------------------------


def split_triggers(triggers: list[str], holdout_ratio: float, seed: int) -> tuple[list[str], list[str]]:
    rng = random.Random(seed)
    shuffled = sorted(triggers)
    rng.shuffle(shuffled)
    n_hold = max(1, int(round(len(shuffled) * holdout_ratio))) if len(shuffled) >= 3 else 0
    return shuffled[n_hold:], shuffled[:n_hold]


def cap_max_pairs(items: list[str], cap: int) -> list[tuple[str, str]]:
    """Return up to `cap` unordered pairs from `items` (random sample if
    the full combination set exceeds cap)."""
    all_pairs = list(combinations(items, 2))
    if len(all_pairs) <= cap:
        return all_pairs
    rng = random.Random(len(items))
    rng.shuffle(all_pairs)
    return all_pairs[:cap]


# ---------------------------------------------------------------------------
# Hard negative mining
# ---------------------------------------------------------------------------


def mine_hard_negatives(
    triplets_path: Path,
    train_surfaces: dict[str, list[str]],
    base_model: str,
    top_k_caps: int,
    per_pair: int,
    max_per_label: int,
    seed: int,
) -> int:
    import numpy as np
    from sentence_transformers import SentenceTransformer

    print(f"loading base model for negative mining: {base_model}")
    model = SentenceTransformer(base_model)

    labels = sorted(train_surfaces.keys())
    centroids: dict[str, np.ndarray] = {}
    for label in labels:
        v = model.encode(train_surfaces[label], normalize_embeddings=True, convert_to_numpy=True)
        c = v.mean(axis=0)
        n = np.linalg.norm(c) + 1e-9
        centroids[label] = c / n

    neighbors: dict[str, list[str]] = {}
    for label in labels:
        sims = sorted(
            ((float(centroids[label] @ centroids[other]), other) for other in labels if other != label),
            reverse=True,
        )
        neighbors[label] = [n for _, n in sims[:top_k_caps]]

    rng = random.Random(seed)
    written = 0
    with triplets_path.open("w") as fp:
        for label in labels:
            surfaces = train_surfaces[label]
            if len(surfaces) < 2:
                continue
            label_written = 0
            pairs = cap_max_pairs(surfaces, max_per_label)
            rng.shuffle(pairs)
            for a, p in pairs:
                if label_written >= max_per_label:
                    break
                for _ in range(per_pair):
                    neg_label = rng.choice(neighbors[label])
                    neg = rng.choice(train_surfaces[neg_label])
                    fp.write(json.dumps({
                        "anchor": a,
                        "positive": p,
                        "negative": neg,
                        "label": label,
                        "neg_label": neg_label,
                    }) + "\n")
                    written += 1
                    label_written += 1
                    if label_written >= max_per_label:
                        break
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[2]
    ap.add_argument("--caps", type=Path, default=repo / "capabilities")
    ap.add_argument("--intents", type=Path, default=root / "data" / "intents.jsonl",
                    help="optional LLM-generated paraphrases (from augment_llm.py)")
    ap.add_argument("--pairs-out", type=Path, default=root / "data" / "pairs.jsonl")
    ap.add_argument("--triplets-out", type=Path, default=root / "data" / "triplets.jsonl")
    ap.add_argument("--holdout-out", type=Path, default=root / "data" / "holdout.jsonl")
    ap.add_argument("--holdout-ratio", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--base-model", type=str, default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--max-pairs-per-cap", type=int, default=400,
                    help="cap on pair examples per capability (random sample if exceeded)")
    ap.add_argument("--neg-top-k-caps", type=int, default=5)
    ap.add_argument("--neg-per-pair", type=int, default=2)
    ap.add_argument("--max-triplets-per-cap", type=int, default=200)
    ap.add_argument("--skip-negatives", action="store_true")
    args = ap.parse_args()

    triggers_by_cap = load_triggers(args.caps)
    if not triggers_by_cap:
        print("No capabilities with triggers found.", file=sys.stderr)
        return 1
    print(f"loaded {len(triggers_by_cap)} capabilities with >=2 triggers")

    llm_by_cap = load_llm_intents(args.intents)
    if llm_by_cap:
        print(f"loaded LLM-augmented intents for {len(llm_by_cap)} capabilities from {args.intents}")
    else:
        print(f"no LLM intents found at {args.intents} (rule-based only)")

    for p in (args.pairs_out, args.triplets_out, args.holdout_out):
        p.parent.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)

    train_surfaces: dict[str, list[str]] = {}
    holdout_rows: list[tuple[str, str]] = []  # (intent, label)
    pair_count = 0

    with args.pairs_out.open("w") as fp_train, args.holdout_out.open("w") as fp_hold:
        for label, triggers in triggers_by_cap.items():
            train_trigs, hold_trigs = split_triggers(triggers, args.holdout_ratio, args.seed)

            # ---- TRAINING SURFACES ----
            # 1. Rule-based expansions of every training trigger.
            surfaces: set[str] = set()
            for t in train_trigs:
                surfaces.update(expand_trigger(t, rng))

            # 2. LLM intents whose source IS NOT in the holdout.
            for source, intent in llm_by_cap.get(label, []):
                if source in hold_trigs:
                    continue
                surfaces.add(intent)
                # Also expand the LLM intent with templates for extra surface.
                surfaces.update(expand_trigger(intent, rng))

            surfaces_list = sorted(surfaces)
            train_surfaces[label] = surfaces_list

            # ---- PAIRS (MNRL) ----
            pairs = cap_max_pairs(surfaces_list, args.max_pairs_per_cap)
            for a, b in pairs:
                fp_train.write(json.dumps({"anchor": a, "positive": b, "label": label}) + "\n")
                fp_train.write(json.dumps({"anchor": b, "positive": a, "label": label}) + "\n")
                pair_count += 2

            # ---- HOLDOUT ----
            # Use rule-based expansions of HELD-OUT triggers (so eval phrases
            # are completely unseen during training). Also include LLM intents
            # whose source IS the held-out trigger, if any.
            for h in hold_trigs:
                for variant in expand_trigger(h, rng):
                    if variant == h:
                        continue  # skip bare form (too easy)
                    fp_hold.write(json.dumps({"intent": variant, "label": label, "source": h}) + "\n")
                    holdout_rows.append((variant, label))
                for source, intent in llm_by_cap.get(label, []):
                    if source == h:
                        fp_hold.write(json.dumps({"intent": intent, "label": label, "source": h}) + "\n")
                        holdout_rows.append((intent, label))

    print(f"wrote {pair_count} pair examples to {args.pairs_out}")
    print(f"wrote {len(holdout_rows)} holdout intents to {args.holdout_out}")
    avg = sum(len(v) for v in train_surfaces.values()) / max(1, len(train_surfaces))
    print(f"avg distinct surfaces per capability: {avg:.1f}")

    if args.skip_negatives:
        print("skipping hard-negative mining (--skip-negatives)")
        return 0

    triplets = mine_hard_negatives(
        args.triplets_out,
        train_surfaces,
        args.base_model,
        args.neg_top_k_caps,
        args.neg_per_pair,
        args.max_triplets_per_cap,
        args.seed,
    )
    print(f"wrote {triplets} hard-negative triplets to {args.triplets_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
