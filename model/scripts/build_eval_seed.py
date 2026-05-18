"""Generate a frozen "real user" evaluation set under data/eval_real.jsonl.

This is the eval set that `eval_gate.py` uses as the publish gate. It
is deliberately a *different distribution* than `holdout.jsonl`:

  - `holdout.jsonl` is rule-template-expanded held-out triggers — same
    generator that produced the training data, just with a held-out
    slice. Useful for in-distribution regression testing.

  - `eval_real.jsonl` reflects how real users actually phrase prompts
    in coding-assistant chats (informed by WildChat / LMSYS-Chat
    distributions): short utterances, follow-ups, typos, casual
    register, paste-dumps, chitchat, vague asks, and ambiguous edge
    cases. ~15-20% of real chat traffic is "Other/Unknown" — should
    abstain — so a healthy chunk of the eval set has `label: null`.

The seed is fully scripted and reproducible. Hand-edit the JSONL after
generation to add specific failure modes observed in production.

Output schema (JSONL):

    {"intent": "<user message>", "label": "<cap-name|null>", "kind": "<category>"}

`label: null` means the runtime SHOULD abstain (no capability picked).
`kind` is one of: positive, follow_up, typo_casual, multi_turn,
cross_domain_shell, chitchat, vague, sarcastic_feedback, paste_dump,
off_topic, ambiguous, compound. Used by `eval_gate.py` for per-category
breakdown.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]


# ---------------------------------------------------------------------------
# Catalog loaders (kept in sync with build_dataset.py::load_all_triggers)
# ---------------------------------------------------------------------------

_SEMANTIC_RE = re.compile(r"semantic\(\s*['\"]?(.+?)['\"]?\s*\)")


def load_all_triggers(caps_dir: Path, skills_dir: Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    if caps_dir.exists():
        for cap_dir in sorted(p for p in caps_dir.iterdir() if p.is_dir()):
            cfg = cap_dir / "config.toml"
            if not cfg.exists():
                continue
            data = tomllib.loads(cfg.read_text())
            triggers = [t.strip() for t in data.get("triggers", []) if t.strip()]
            if triggers:
                out[cap_dir.name] = list(triggers)
    if skills_dir.exists():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            md = skill_dir / "SKILL.md"
            if not md.exists():
                continue
            text = md.read_text()
            if not text.startswith("---"):
                continue
            end = text.find("\n---", 3)
            if end == -1:
                continue
            phrases = [m.group(1).strip() for m in _SEMANTIC_RE.finditer(text[3:end])]
            phrases = [p for p in phrases if p]
            if not phrases:
                continue
            if skill_dir.name in out:
                seen = set(out[skill_dir.name])
                out[skill_dir.name].extend(p for p in phrases if p not in seen)
            else:
                out[skill_dir.name] = phrases
    return {k: v for k, v in out.items() if len(v) >= 2}


# ---------------------------------------------------------------------------
# Per-cap "real user" phrasing transformations
# ---------------------------------------------------------------------------
#
# Applied to authored triggers to produce a small (~3-5/cap) real-user-
# shaped eval surface per capability. We deliberately do NOT reuse the
# rule-based templates from build_dataset.py — those are the training
# distribution. These transforms are intentionally different shapes:
# short, casual, problem-framed, follow-up-shaped, with occasional
# typos and lowercase i.


def _lower_first(s: str) -> str:
    if not s:
        return s
    head, _, tail = s.partition(" ")
    return head.lower() + ((" " + tail) if tail else "")


def _typo_lite(s: str) -> str:
    """Light typo pass: drop one vowel from a long-ish word. Cheap and
    deterministic — same input always yields the same output."""
    words = s.split()
    out = []
    for w in words:
        if len(w) >= 6 and any(v in w[1:-1].lower() for v in "aeiou"):
            # remove the first interior vowel
            for i, c in enumerate(w[1:-1], start=1):
                if c.lower() in "aeiou":
                    w = w[:i] + w[i+1:]
                    break
        out.append(w)
    return " ".join(out)


REAL_USER_TRANSFORMS: list[tuple[str, str]] = [
    # (template, kind). `{t_lc}` lowercased-first variant of the trigger.
    ("{t_lc}", "positive"),
    ("can u {t_lc}", "typo_casual"),
    ("how do i {t_lc}", "positive"),
    ("need help — {t_lc}", "positive"),
    ("{t_lc}?", "positive"),
    ("ok now {t_lc}", "follow_up"),
    ("and then {t_lc}", "follow_up"),
    ("same as before but {t_lc}", "follow_up"),
    ("trying to {t_lc} but stuck", "positive"),
    ("ugh {t_lc} isn't working", "positive"),
]


def gen_positives_for_label(label: str, triggers: list[str]) -> list[dict]:
    """Return ~4 real-user-style examples per capability, plus one
    light-typo variant. Caps under-trigger labels by recycling the
    available triggers."""
    out: list[dict] = []
    rotation = list(triggers)
    for i, (tpl, kind) in enumerate(REAL_USER_TRANSFORMS):
        trig = rotation[i % len(rotation)]
        t_lc = _lower_first(trig)
        surface = tpl.format(t_lc=t_lc).strip()
        if kind == "typo_casual":
            surface = _typo_lite(surface)
        out.append({"intent": surface, "label": label, "kind": kind})
    return out


# ---------------------------------------------------------------------------
# NULL / abstain examples — should never activate any capability.
# ---------------------------------------------------------------------------
#
# Calibration of `AUTO_ACTIVATE_THRESHOLD` and `AUTO_ACTIVATE_MARGIN`
# at runtime depends on having a representative slice of low-signal
# prompts in the eval set. Categories follow the WildChat/LMSYS-Chat
# distribution: chitchat, vague asks, sarcastic feedback, paste dumps
# (no instruction), off-topic.
# https://arxiv.org/html/2405.01470v1
# https://arxiv.org/html/2410.01627v1

NULL_EXAMPLES: list[tuple[str, str]] = [
    # ---- chitchat ----
    ("good morning", "chitchat"),
    ("good afternoon", "chitchat"),
    ("hi there", "chitchat"),
    ("hey", "chitchat"),
    ("yo", "chitchat"),
    ("hello!", "chitchat"),
    ("what's up", "chitchat"),
    ("how's it going", "chitchat"),
    ("how are you doing today", "chitchat"),
    ("thanks", "chitchat"),
    ("thank you", "chitchat"),
    ("thx", "chitchat"),
    ("appreciate it", "chitchat"),
    ("got it", "chitchat"),
    ("makes sense", "chitchat"),
    ("cool", "chitchat"),
    ("perfect", "chitchat"),
    ("nice one", "chitchat"),
    ("lol", "chitchat"),
    ("hahaha", "chitchat"),
    ("interesting", "chitchat"),
    ("ah okay", "chitchat"),
    ("I see", "chitchat"),
    ("noted", "chitchat"),
    ("sounds good", "chitchat"),
    ("alright", "chitchat"),
    ("one sec", "chitchat"),
    ("brb", "chitchat"),

    # ---- vague / under-specified ----
    ("help", "vague"),
    ("help me", "vague"),
    ("any ideas?", "vague"),
    ("what should I do", "vague"),
    ("what now?", "vague"),
    ("what's next", "vague"),
    ("I'm stuck", "vague"),
    ("stuck", "vague"),
    ("this is hard", "vague"),
    ("I don't get it", "vague"),
    ("explain", "vague"),
    ("what is this", "vague"),
    ("what does this mean", "vague"),
    ("can you clarify", "vague"),
    ("I'm confused", "vague"),
    ("fix it", "vague"),
    ("do something", "vague"),
    ("make it work", "vague"),
    ("just do it", "vague"),
    ("figure it out", "vague"),
    ("you decide", "vague"),

    # ---- sarcastic feedback ----
    ("that didn't work", "sarcastic_feedback"),
    ("still broken", "sarcastic_feedback"),
    ("doesn't work", "sarcastic_feedback"),
    ("nope", "sarcastic_feedback"),
    ("not working", "sarcastic_feedback"),
    ("still failing", "sarcastic_feedback"),
    ("same error", "sarcastic_feedback"),
    ("no change", "sarcastic_feedback"),
    ("great, now what", "sarcastic_feedback"),
    ("are you serious", "sarcastic_feedback"),
    ("that's not right", "sarcastic_feedback"),
    ("try again", "sarcastic_feedback"),
    ("never mind", "sarcastic_feedback"),
    ("forget it", "sarcastic_feedback"),

    # ---- paste dumps with no instruction ----
    ("Error: ENOENT: no such file or directory, open '/var/log/app.log'", "paste_dump"),
    ("Traceback (most recent call last):\n  File \"<stdin>\", line 1, in <module>\nNameError: name 'x' is not defined", "paste_dump"),
    ("{\"status\":500,\"message\":\"internal server error\"}", "paste_dump"),
    ("TypeError: Cannot read property 'foo' of undefined", "paste_dump"),
    ("warning: unused variable `x` at src/main.rs:42", "paste_dump"),
    ("Segmentation fault (core dumped)", "paste_dump"),
    ("panic: runtime error: index out of range", "paste_dump"),
    ("0\n1\n2\n3\n4\n5\n6\n7\n8\n9", "paste_dump"),
    ("foo bar baz", "paste_dump"),

    # ---- off-topic / non-engineering ----
    ("what's the weather today", "off_topic"),
    ("tell me a joke", "off_topic"),
    ("what time is it", "off_topic"),
    ("recommend a movie", "off_topic"),
    ("translate hello to spanish", "off_topic"),
    ("is the earth round", "off_topic"),
    ("summarize the news", "off_topic"),
    ("give me a fun fact", "off_topic"),
    ("what's your favorite color", "off_topic"),
    ("should I get pizza or sushi", "off_topic"),
]


# ---------------------------------------------------------------------------
# Edge-case structured examples (positives + ambiguous + compound)
# ---------------------------------------------------------------------------
#
# These exercise the failure modes we know the embedding has historically
# struggled with. Labels reflect what the runtime SHOULD activate (or
# null for "abstain — too ambiguous").

EDGE_POSITIVES: list[tuple[str, str, str]] = [
    # (intent, expected_label, kind)

    # cross-domain shell: leading verb dominates, not the tool name
    ("run cargo build", "shell", "cross_domain_shell"),
    ("execute pytest", "shell", "cross_domain_shell"),
    ("run npm install", "shell", "cross_domain_shell"),
    ("invoke swift build for me", "shell", "cross_domain_shell"),
    ("can you run go test", "shell", "cross_domain_shell"),
    ("please execute the deploy script", "shell", "cross_domain_shell"),
    ("fire off make clean", "shell", "cross_domain_shell"),

    # multi-turn shaped: clear domain in the tail
    ("earlier we were setting up postgres, now check the schema", "database-postgres", "multi_turn"),
    ("following up on the deploy: roll it back", "shell", "multi_turn"),
    ("back to the docker question — show running containers", "docker", "multi_turn"),
    ("alright, now query the postgres table", "database-postgres", "multi_turn"),
    ("ok scratch that. let's search the codebase", "codesearch-semantic", "multi_turn"),
]

EDGE_AMBIGUOUS: list[tuple[str, str]] = [
    # Intent is plausible across two+ near-domain caps. The runtime
    # margin gate should ABSTAIN here. Tags as label=null.
    ("query the database", "ambiguous"),               # postgres vs sqlite
    ("send a message", "ambiguous"),                   # whatsapp vs sms vs telegram vs instagram
    ("check the logs", "ambiguous"),                   # shell vs error-tracking vs k8s
    ("look at the build output", "ambiguous"),         # shell vs CI-ish
    ("read the schema", "ambiguous"),                  # postgres vs sqlite
    ("inspect the service", "ambiguous"),              # k8s vs docker
    ("show me the file", "ambiguous"),                 # filesystem-read vs others
    ("debug the issue", "ambiguous"),                  # any programming-* + shell
]

EDGE_COMPOUND: list[tuple[str, str, str]] = [
    # Two intents in one prompt. We pick the dominant (verb-first) intent
    # as the expected label; the runtime should NOT activate the second.
    ("build the project and then deploy it", "shell", "compound"),
    ("run tests then commit", "shell", "compound"),
]


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[2]
    ap.add_argument("--caps", type=Path, default=repo / "capabilities")
    ap.add_argument("--skills", type=Path, default=repo / "skills")
    ap.add_argument("--out", type=Path, default=root / "data" / "eval_real.jsonl")
    ap.add_argument(
        "--per-cap-positives",
        type=int,
        default=10,
        help="number of real-user-shaped positives per capability (default: full template set)",
    )
    args = ap.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)

    triggers_by_cap = load_all_triggers(args.caps, args.skills)
    if not triggers_by_cap:
        print("no capabilities found", file=sys.stderr)
        return 1

    rows: list[dict] = []

    # ---- per-cap positives ----
    pos_count = 0
    for label in sorted(triggers_by_cap):
        cap_rows = gen_positives_for_label(label, triggers_by_cap[label])
        cap_rows = cap_rows[: args.per_cap_positives]
        rows.extend(cap_rows)
        pos_count += len(cap_rows)

    # ---- edge positives (cross-domain shell, multi-turn) ----
    for intent, label, kind in EDGE_POSITIVES:
        # Only include if the expected label exists in this catalog.
        if label in triggers_by_cap or label == "shell":
            rows.append({"intent": intent, "label": label, "kind": kind})

    # ---- edge compound positives ----
    for intent, label, kind in EDGE_COMPOUND:
        if label in triggers_by_cap or label == "shell":
            rows.append({"intent": intent, "label": label, "kind": kind})

    # ---- NULL: chitchat, vague, sarcastic, paste, off-topic ----
    null_count = 0
    for intent, kind in NULL_EXAMPLES:
        rows.append({"intent": intent, "label": None, "kind": kind})
        null_count += 1

    # ---- NULL: ambiguous (should abstain via margin gate) ----
    amb_count = 0
    for intent, kind in EDGE_AMBIGUOUS:
        rows.append({"intent": intent, "label": None, "kind": kind})
        amb_count += 1

    with args.out.open("w") as fp:
        for r in rows:
            fp.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"wrote {len(rows)} rows to {args.out}")
    print(f"  positives:    {pos_count}")
    print(f"  edge cases:   {len(EDGE_POSITIVES) + len(EDGE_COMPOUND)}")
    print(f"  NULL chit/vague/feedback/paste/offtopic: {null_count}")
    print(f"  NULL ambiguous: {amb_count}")
    print()
    print("Next: hand-edit data/eval_real.jsonl to add real production-observed")
    print("failure modes. The file is the publish gate — anything you commit here")
    print("becomes part of the regression test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
