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
    # ---- real-user style (WildChat / ShareGPT distribution) -----------
    # Short utterances and abbreviations dominate the long-tail of real
    # chat data — ~30% of WildChat messages are short imperatives or
    # one-line questions. Casual register and dropped articles too.
    "i want to {t_lc}",       # lowercase i — common in chat
    "wanna {t_lc}",
    "gotta {t_lc}",
    "need to {t_lc}",
    "just {t_lc}",
    "trying {t_lc}",
    # bug-report / problem-statement frame
    "{t_lc} but it's not working",
    "{t_lc} isn't working",
    "can't {t_lc}",
    "unable to {t_lc}",
    # acceptance-style ("ok now do X") follow-up framing — train the
    # model that a leading "now"/"next" still names the same intent.
    "now {t_lc}",
    "next, {t_lc}",
    "ok now {t_lc}",
    "and then {t_lc}",
]


# Multi-turn-shaped prefixes. Real chats often presume prior context —
# the latest user message references work from earlier turns. Training
# on a slice of surfaces with such prefixes teaches the embedding to
# attend to the intent tail, not the leading conversational filler.
# https://arxiv.org/html/2411.14252v1
MULTI_TURN_PREFIXES: list[str] = [
    "earlier we set up the project; now {t_lc}",
    "following up: {t_lc}",
    "as I was saying — {t_lc}",
    "back to what we discussed: {t_lc}",
    "ok so given that context, {t_lc}",
    "ignore the previous output. {t_lc}",
    "let's try again — {t_lc}",
    "scratch that. {t_lc}",
    "alright, {t_lc}",
    "circling back: {t_lc}",
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


_SEMANTIC_RE = re.compile(r"semantic\(\s*['\"]?(.+?)['\"]?\s*\)")


def load_capability_triggers(caps_dir: Path) -> dict[str, list[str]]:
    """Read `triggers = [...]` from each capability's config.toml."""
    out: dict[str, list[str]] = {}
    if not caps_dir.exists():
        return out
    for cap_dir in sorted(p for p in caps_dir.iterdir() if p.is_dir()):
        cfg = cap_dir / "config.toml"
        if not cfg.exists():
            continue
        data = tomllib.loads(cfg.read_text())
        triggers = [t.strip() for t in data.get("triggers", []) if t.strip()]
        if triggers:
            out[cap_dir.name] = triggers
    return out


def load_skill_semantic_phrases(skills_dir: Path) -> dict[str, list[str]]:
    """Read `semantic(...)` rules from each SKILL.md frontmatter.

    Skills use the same embedding model for their `Semantic { phrase }` rule
    type — see `octomind/src/mcp/core/skill_auto.rs`. The phrases are the
    same kind of supervision signal as capability triggers, just sourced
    from a different file format.
    """
    out: dict[str, list[str]] = {}
    if not skills_dir.exists():
        return out
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        text = md.read_text()
        # Frontmatter only — between first two `---` lines.
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end == -1:
            continue
        frontmatter = text[3:end]
        phrases = [m.group(1).strip() for m in _SEMANTIC_RE.finditer(frontmatter)]
        phrases = [p for p in phrases if p]
        if phrases:
            out[skill_dir.name] = phrases
    return out


def load_all_triggers(caps_dir: Path, skills_dir: Path) -> dict[str, list[str]]:
    """Merge capability triggers and skill semantic phrases under one label
    space. If a name exists in both (e.g. `programming-rust` has a capability
    AND a skill), their phrases are concatenated into one label — they
    describe the same domain so combining sharpens that cluster.
    """
    caps = load_capability_triggers(caps_dir)
    skills = load_skill_semantic_phrases(skills_dir)

    merged: dict[str, list[str]] = {}
    for name, phrases in caps.items():
        merged[name] = list(phrases)
    for name, phrases in skills.items():
        if name in merged:
            seen = set(merged[name])
            merged[name].extend(p for p in phrases if p not in seen)
        else:
            merged[name] = list(phrases)

    filtered: dict[str, list[str]] = {}
    for name, phrases in merged.items():
        if len(phrases) >= 2:
            filtered[name] = phrases
        else:
            print(f"[skip] {name}: needs >=2 phrases, has {len(phrases)}", file=sys.stderr)

    n_cap_only = sum(1 for n in caps if n not in skills)
    n_skill_only = sum(1 for n in skills if n not in caps)
    n_both = sum(1 for n in caps if n in skills)
    print(
        f"sources: {n_cap_only} capabilities, {n_skill_only} skills, "
        f"{n_both} merged (same name in both) → {len(filtered)} labels"
    )
    return filtered


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
# Cross-domain shell augmentation
# ---------------------------------------------------------------------------
#
# Critical disambiguation signal: "run/execute/invoke <language-specific-tool>"
# must route to `shell`, not to `programming-<that-language>`. The user's
# intent is command execution; the programming capability is for code-level
# help (architecture, debugging, idioms).
#
# Without these synthetic surfaces in the training set, the embedding model
# weights the strong domain noun ("swift", "cargo", "pytest") over the
# generic verb ("run") and routes incorrectly. These pairs teach the model
# that for run/execute/invoke verbs, the verb dominates the tool name.

_SHELL_TOOLS: list[str] = [
    # Build / package
    "cargo build", "cargo test", "cargo run", "cargo check",
    "swift build", "swift test", "swift package update",
    "npm install", "npm run build", "npm test", "pnpm install", "yarn install",
    "pip install -r requirements.txt", "pip install <pkg>", "uv sync", "uv run",
    "go build", "go test ./...", "go run main.go",
    "mvn install", "gradle build",
    "make", "make test", "make clean",
    "bun install", "bun run",
    "composer install",
    # Containers / infra
    "docker build", "docker compose up", "docker ps",
    "kubectl get pods", "kubectl apply -f",
    "terraform plan", "terraform apply",
    # Scripts / tests
    "pytest", "pytest -k <name>", "jest", "vitest",
    "bash script.sh", "sh ./setup",
    "ruby script.rb",
    "node script.js",
    "python script.py",
    "./run.sh",
    # Common one-offs
    "ls -la", "grep -r foo .", "find . -name '*.rs'",
    "git status", "git log", "git diff",
]

_SHELL_VERB_TEMPLATES: list[str] = [
    "run {tool}",
    "execute {tool}",
    "invoke {tool}",
    "I need to run {tool}",
    "can you run {tool}",
    "please execute {tool}",
    "run {tool} in the terminal",
    "fire off {tool}",
    "kick off {tool}",
    "run {tool} for me",
    "how do I run {tool}",
    "{tool} isn't working, can you run it",
]


def synth_shell_surfaces() -> list[str]:
    """Generate cross-domain shell-execution surfaces.

    These belong to the `shell` label even though they name tools from
    other capability domains (cargo, swift, npm, …). They're the model's
    only signal that "run <programming-tool>" → shell, not → programming-X.
    """
    out: set[str] = set()
    for tool in _SHELL_TOOLS:
        for tpl in _SHELL_VERB_TEMPLATES:
            out.add(tpl.format(tool=tool))
    return sorted(out)


# ---------------------------------------------------------------------------
# Out-of-domain ("_oos") sink label
# ---------------------------------------------------------------------------
#
# Real user chats include a lot of low-signal traffic — chitchat,
# acknowledgments, vague asks, paste-without-instruction — that the
# embedding model should NOT route to any capability. Without an
# explicit OOS cluster, those inputs land near whichever real cap
# happens to share surface vocabulary, and the runtime threshold has
# to do all the heavy lifting on its own.
#
# Training on a `_oos` label lets the encoder learn a dedicated cluster
# for "no real intent" — real-cap cosines for these inputs drop, the
# 0.55 floor catches them, and false-positive activation rate falls.
# We never register `_oos` as a runtime capability; it exists only in
# the training set as a separator force.
#
# Phrases informed by the WildChat / LMSYS-Chat distribution of
# information-seeking + chitchat + acknowledgments + sarcasm/feedback.
# https://arxiv.org/html/2405.01470v1
# https://arxiv.org/html/2410.01627v1

_OOS_CHITCHAT: list[str] = [
    "good morning",
    "good afternoon",
    "good evening",
    "hi there",
    "hello",
    "hey",
    "yo",
    "sup",
    "what's up",
    "how's it going",
    "how are you",
    "how are you doing",
    "thanks",
    "thank you",
    "thx",
    "ty",
    "appreciate it",
    "cheers",
    "ok",
    "okay",
    "alright",
    "got it",
    "understood",
    "makes sense",
    "cool",
    "nice",
    "perfect",
    "great",
    "awesome",
    "lol",
    "haha",
    "interesting",
    "hmm",
    "huh",
    "ah ok",
    "I see",
    "noted",
    "sounds good",
    "sure",
    "yes",
    "no",
    "maybe",
    "I don't know",
    "not sure",
    "let me think",
    "one sec",
    "hold on",
    "give me a moment",
    "back in a bit",
    "be right back",
    "brb",
]

_OOS_VAGUE: list[str] = [
    "help",
    "help me",
    "any ideas",
    "any idea",
    "what should I do",
    "what now",
    "what's next",
    "where do we go from here",
    "I'm stuck",
    "stuck",
    "this is hard",
    "I don't get it",
    "I don't understand",
    "explain",
    "explain this",
    "what is this",
    "what does this mean",
    "huh what",
    "wait what",
    "can you clarify",
    "I'm confused",
    "lost",
    "fix it",
    "do something",
    "make it work",
    "just do it",
    "figure it out",
    "you decide",
]

_OOS_FEEDBACK_SARCASM: list[str] = [
    "that didn't work",
    "still broken",
    "doesn't work",
    "nope",
    "not working",
    "still failing",
    "same error",
    "no change",
    "no luck",
    "great, now what",
    "you sure about that",
    "are you serious",
    "really?",
    "that's not right",
    "wrong answer",
    "try again",
    "do it again",
    "never mind",
    "forget it",
]

_OOS_PASTE_DUMP: list[str] = [
    # Long pastes with no instruction — researchers note these
    # are a common misclassification source (intent has to be
    # *inferred* from content).
    "Error: ENOENT: no such file or directory, open '/var/log/app.log'",
    "Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name 'x' is not defined",
    "{\"status\":500,\"message\":\"internal server error\"}",
    "TypeError: Cannot read property 'foo' of undefined",
    "warning: unused variable `x` at src/main.rs:42",
    "Segmentation fault (core dumped)",
    "panic: runtime error: index out of range",
]

_OOS_OFF_TOPIC: list[str] = [
    "what's the weather today",
    "tell me a joke",
    "what time is it",
    "who won the game last night",
    "should I get pizza or sushi",
    "recommend a movie",
    "translate hello to spanish",
    "is the earth round",
    "summarize the news",
    "give me a fun fact",
    "what's your favorite color",
]


def synth_oos_surfaces() -> list[str]:
    """All curated OOS phrases. De-duplicated, sorted for reproducibility."""
    s: set[str] = set()
    for bucket in (_OOS_CHITCHAT, _OOS_VAGUE, _OOS_FEEDBACK_SARCASM,
                   _OOS_PASTE_DUMP, _OOS_OFF_TOPIC):
        for p in bucket:
            s.add(p)
    return sorted(s)


# ---------------------------------------------------------------------------
# Multi-turn surface expansion
# ---------------------------------------------------------------------------


def maybe_multi_turn(surface: str, rng: random.Random, ratio: float) -> str | None:
    """With probability `ratio`, wrap `surface` in a multi-turn prefix
    referencing prior conversation context. Returns the new surface or
    None to keep the original."""
    if ratio <= 0 or not surface:
        return None
    if rng.random() >= ratio:
        return None
    tpl = rng.choice(MULTI_TURN_PREFIXES)
    t_lc = lowercase_first_word(surface)
    return tpl.format(t_lc=t_lc).strip()


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


def mine_hard_negatives_from_retriever(
    triplets_path: Path,
    train_surfaces: dict[str, list[str]],
    embed_model: str,
    top_k_candidates: int,
    per_pair: int,
    max_per_label: int,
    seed: int,
    pos_aware_frac: float = 0.95,
) -> int:
    """Mine hard negatives by running the bi-encoder over training queries
    and taking its top-K WRONG retrievals as the hard negative pool.

    Rationale: the centroid-based mining picks negatives by inter-centroid
    similarity (computed once over averaged trigger vectors). That gives
    domain-neighbor capabilities as a class, not specific phrases the
    bi-encoder actually retrieves at inference. With this function, the
    negatives ARE the retrieval competitors — train-time and inference-time
    distributions match. Standard technique from BGE / ColBERT training
    recipes.

    `embed_model` should be the FINE-TUNED bi-encoder checkpoint that
    powers retrieval in production. Mining with that model produces
    negatives matching its mistake patterns.

    `pos_aware_frac` implements NV-Retriever's positive-aware mining
    rule: a candidate is only accepted as a hard negative if its
    cosine to the anchor is below `pos_aware_frac * cos(anchor,
    positive)`. Set to 0.95 (the paper's reported optimum) to filter
    out *false* hard negatives — items that score >= the positive
    are almost certainly mislabeled near-duplicates of the positive,
    and training against them collapses the margin we're trying to
    widen. Set to 1.0 to disable.
    https://arxiv.org/pdf/2407.15831
    """
    import numpy as np
    from sentence_transformers import SentenceTransformer

    print(f"loading bi-encoder for retrieval-based negative mining: {embed_model}")
    model = SentenceTransformer(embed_model)

    labels = sorted(train_surfaces.keys())

    # Flatten all surfaces into a single corpus, tracking per-surface label.
    corpus_texts: list[str] = []
    corpus_labels: list[str] = []
    text_to_idx: dict[tuple[str, str], int] = {}
    label_indices: dict[str, list[int]] = {label: [] for label in labels}
    for label in labels:
        for s in train_surfaces[label]:
            idx = len(corpus_texts)
            corpus_texts.append(s)
            corpus_labels.append(label)
            text_to_idx[(label, s)] = idx
            label_indices[label].append(idx)

    print(f"encoding {len(corpus_texts)} surfaces for retrieval...")
    corpus_vecs = model.encode(
        corpus_texts,
        normalize_embeddings=True,
        batch_size=64,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    rng = random.Random(seed)
    written = 0

    with triplets_path.open("w") as fp:
        for label in labels:
            surfaces = train_surfaces[label]
            if len(surfaces) < 2:
                continue
            own_indices = label_indices[label]
            label_written = 0
            pairs = cap_max_pairs(surfaces, max_per_label)
            rng.shuffle(pairs)

            for a, p in pairs:
                if label_written >= max_per_label:
                    break

                a_idx = text_to_idx[(label, a)]
                p_idx = text_to_idx[(label, p)]
                # Cosine vs entire corpus, mask own-label entries.
                scores = corpus_vecs @ corpus_vecs[a_idx]
                scores = scores.copy()
                pos_score = float(corpus_vecs[p_idx] @ corpus_vecs[a_idx])
                # NV-Retriever positive-aware filter: drop candidates that
                # score above `pos_aware_frac * pos_score` (likely false
                # negatives — semantically equivalent to the positive but
                # under a different label).
                if pos_aware_frac < 1.0:
                    ceiling = pos_aware_frac * pos_score
                    scores[scores > ceiling] = -np.inf
                for own in own_indices:
                    scores[own] = -np.inf
                # Top-K wrong retrievals (this is what the bi-encoder
                # actually surfaces at inference time as competitors),
                # after the false-negative filter.
                order = np.argsort(-scores)
                top_wrong = [int(i) for i in order if scores[i] != -np.inf][:top_k_candidates]
                if not top_wrong:
                    continue

                for _ in range(per_pair):
                    if label_written >= max_per_label:
                        break
                    neg_idx = int(rng.choice(top_wrong))
                    neg = corpus_texts[neg_idx]
                    neg_label = corpus_labels[neg_idx]
                    fp.write(json.dumps({
                        "anchor": a,
                        "positive": p,
                        "negative": neg,
                        "label": label,
                        "neg_label": neg_label,
                    }) + "\n")
                    written += 1
                    label_written += 1
    return written


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[2]
    ap.add_argument("--caps", type=Path, default=repo / "capabilities")
    ap.add_argument("--skills", type=Path, default=repo / "skills")
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
    ap.add_argument(
        "--oos-label",
        action="store_true",
        default=True,
        help="add an `_oos` sink label with curated chitchat / vague / paste-dump phrases "
             "so the model learns a dedicated out-of-domain cluster.",
    )
    ap.add_argument(
        "--no-oos-label",
        dest="oos_label",
        action="store_false",
        help="disable the _oos sink label (not recommended).",
    )
    ap.add_argument(
        "--multi-turn-ratio",
        type=float,
        default=0.15,
        help="fraction of training surfaces per label that get a multi-turn / "
             "context-laden prefix attached. 0 disables.",
    )
    ap.add_argument(
        "--pos-aware-frac",
        type=float,
        default=0.95,
        help="(retrieval mode) accept a hard negative only if its score is <= "
             "POS_AWARE_FRAC * positive_score. 0.95 = NV-Retriever default; "
             "1.0 disables (every top-K candidate is accepted).",
    )
    ap.add_argument(
        "--neg-embed-model",
        type=str,
        default=None,
        help=(
            "Path or HF id of a bi-encoder to use for retrieval-based hard-negative mining. "
            "When provided, hard negatives are the bi-encoder's actual top-K WRONG retrievals "
            "per training query (matches train-time and inference-time distributions). "
            "When omitted, falls back to centroid-similarity mining with the base BGE-small."
        ),
    )
    ap.add_argument(
        "--neg-top-k-candidates",
        type=int,
        default=20,
        help="(retrieval mode) per-anchor top-K wrong retrievals to sample negatives from.",
    )
    args = ap.parse_args()

    triggers_by_cap = load_all_triggers(args.caps, args.skills)
    if not triggers_by_cap:
        print("No capabilities with triggers found.", file=sys.stderr)
        return 1

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

    # ---- OOS sink injection ----
    # `_oos` is a synthetic label that never appears as a runtime capability.
    # Its sole purpose during training is to give chitchat / vague / paste-
    # dump phrases their own cluster, so real-cap cosines for those inputs
    # drop and the runtime floor catches them. We splice it into the same
    # `triggers_by_cap` map so the standard MNRL + hard-neg pipeline picks
    # it up without special-casing downstream.
    if args.oos_label:
        oos_phrases = synth_oos_surfaces()
        if "_oos" in triggers_by_cap:
            # Merge if the catalog also defines _oos (treat as concat).
            seen = set(triggers_by_cap["_oos"])
            triggers_by_cap["_oos"].extend(p for p in oos_phrases if p not in seen)
        else:
            triggers_by_cap["_oos"] = oos_phrases
        print(f"OOS sink: injected {len(oos_phrases)} curated phrases under label '_oos'")

    with args.pairs_out.open("w") as fp_train, args.holdout_out.open("w") as fp_hold:
        for label, triggers in triggers_by_cap.items():
            # The OOS label doesn't participate in holdout — its job is
            # training-time separation; evaluation of abstention happens via
            # `eval_real.jsonl` with `label: null`, not via holdout.
            if label == "_oos":
                train_trigs = list(triggers)
                hold_trigs = []
            else:
                train_trigs, hold_trigs = split_triggers(triggers, args.holdout_ratio, args.seed)

            # ---- TRAINING SURFACES ----
            # 1. Rule-based expansions of every training trigger.
            surfaces: set[str] = set()
            for t in train_trigs:
                if label == "_oos":
                    # OOS phrases are *already* user-shaped — adding
                    # imperative/question templates ("how do I {oos}")
                    # makes nonsensical surfaces that confuse training.
                    surfaces.add(t)
                else:
                    surfaces.update(expand_trigger(t, rng))

            # 2. LLM intents whose source IS NOT in the holdout.
            for source, intent in llm_by_cap.get(label, []):
                if source in hold_trigs:
                    continue
                surfaces.add(intent)
                # Also expand the LLM intent with templates for extra surface.
                surfaces.update(expand_trigger(intent, rng))

            # 3. Cross-domain shell surfaces — for the `shell` label only.
            # These are synthetic "run <TOOL>" patterns covering language-
            # specific CLIs (cargo, swift, npm, …). They teach the model
            # that the verb dominates the tool name for routing decisions.
            if label == "shell":
                for s in synth_shell_surfaces():
                    surfaces.add(s)

            # 4. Multi-turn-shaped surfaces. For a fraction of the existing
            # surfaces, attach a context-laden prefix (e.g. "earlier we set
            # up X; now ..."). Trains the embedding to attend to the
            # actionable tail when the message references prior turns.
            # Skipped for `_oos` and `shell`-synth where the surfaces are
            # already structured to be self-contained.
            if label not in ("_oos",) and args.multi_turn_ratio > 0:
                multi_turn_extras: set[str] = set()
                for s in surfaces:
                    mt = maybe_multi_turn(s, rng, args.multi_turn_ratio)
                    if mt is not None:
                        multi_turn_extras.add(mt)
                surfaces.update(multi_turn_extras)

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

    if args.neg_embed_model:
        triplets = mine_hard_negatives_from_retriever(
            args.triplets_out,
            train_surfaces,
            args.neg_embed_model,
            args.neg_top_k_candidates,
            args.neg_per_pair,
            args.max_triplets_per_cap,
            args.seed,
            pos_aware_frac=args.pos_aware_frac,
        )
        mode = "positive-aware" if args.pos_aware_frac < 1.0 else "raw top-K"
        print(
            f"wrote {triplets} retrieval-aligned hard-negative triplets "
            f"({mode}, frac={args.pos_aware_frac}) to {args.triplets_out}"
        )
    else:
        triplets = mine_hard_negatives(
            args.triplets_out,
            train_surfaces,
            args.base_model,
            args.neg_top_k_caps,
            args.neg_per_pair,
            args.max_triplets_per_cap,
            args.seed,
        )
        print(f"wrote {triplets} centroid-based hard-negative triplets to {args.triplets_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
