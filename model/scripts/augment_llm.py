"""Generate naturally-phrased user intents per authored trigger using an LLM.

This is the high-quality augmentation step. Rule-based templates can only
vary surface; an LLM can vary vocabulary, register, structure, and add
realistic context — which is what real user prompts look like.

Output: model/data/intents.jsonl, one JSON object per line:
  {"label": "<capability>", "source": "<trigger>", "intent": "<paraphrase>"}

`build_dataset.py` auto-loads this file if present.

Provider: Anthropic Claude (Haiku for cost). Override with --provider openai
if preferred. Reads API key from ANTHROPIC_API_KEY or OPENAI_API_KEY.

Cost rough estimate (Haiku):
  53 caps × 5 triggers × 10 paraphrases × ~80 tokens ≈ 210k output tokens
  ≈ $0.25 input + $1.05 output ≈ $1.30 total.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]


SYSTEM_PROMPT = """You generate diverse, natural user paraphrases for an embedding-model training dataset.

Given an authored trigger phrase that describes a capability (e.g. "execute a shell command"), produce N paraphrases representing how a real human would actually request the same thing in a chat with a coding assistant.

Cover ALL of these forms across the N paraphrases:
- terse keyword form ("shell command")
- question form ("how do I run X")
- problem statement ("my script won't run")
- context-laden request ("for this project I need to ...")
- formal request ("please execute ...")
- casual/slang ("just need to fire off a shell command")
- imperative without articles ("run shell command")

Vary the VOCABULARY, not just the phrasing. Use synonyms, domain-appropriate jargon, and different verbs. Each paraphrase must clearly map to the SAME capability — do not invent unrelated tasks.

Output strictly as JSON array of strings, no prose, no markdown fences, no numbering.
Example output: ["foo","bar","baz"]"""


USER_TEMPLATE = """Capability: {label}
Authored trigger: {trigger}

Generate {n} diverse user paraphrases for this trigger."""


_SEMANTIC_RE = __import__("re").compile(r"semantic\(\s*['\"]?(.+?)['\"]?\s*\)")


def load_triggers(caps_dir: Path, skills_dir: Path | None = None) -> dict[str, list[str]]:
    """Load capability triggers + skill semantic() phrases under one label
    space. Mirrors `build_dataset.py::load_all_triggers` so the LLM
    augmentation and dataset assembly stay in sync."""
    out: dict[str, list[str]] = {}
    if caps_dir and caps_dir.exists():
        for cap_dir in sorted(p for p in caps_dir.iterdir() if p.is_dir()):
            cfg = cap_dir / "config.toml"
            if not cfg.exists():
                continue
            data = tomllib.loads(cfg.read_text())
            triggers = [t.strip() for t in data.get("triggers", []) if t.strip()]
            if triggers:
                out[cap_dir.name] = list(triggers)
    if skills_dir and skills_dir.exists():
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
    return out


# ---------------------------------------------------------------------------
# Provider adapters
# ---------------------------------------------------------------------------


def call_anthropic(model: str, label: str, trigger: str, n: int, max_retries: int = 3) -> list[str]:
    import anthropic
    client = anthropic.Anthropic()
    user = USER_TEMPLATE.format(label=label, trigger=trigger, n=n)
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user}],
            )
            text = "".join(b.text for b in msg.content if hasattr(b, "text")).strip()
            return parse_array(text)
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"anthropic call failed for {label}/{trigger}: {last_err}")


def call_openai(model: str, label: str, trigger: str, n: int, max_retries: int = 3) -> list[str]:
    from openai import OpenAI
    client = OpenAI()
    user = USER_TEMPLATE.format(label=label, trigger=trigger, n=n)
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_object"},
            )
            text = resp.choices[0].message.content or ""
            return parse_array(text)
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"openai call failed for {label}/{trigger}: {last_err}")


def parse_array(text: str) -> list[str]:
    # Strip code fences if model added them.
    t = text.strip()
    if t.startswith("```"):
        t = t.strip("`")
        if t.lower().startswith("json"):
            t = t[4:]
        t = t.strip()
    # Some models wrap arrays in {"items": [...]} when JSON-mode is on.
    try:
        parsed = json.loads(t)
    except json.JSONDecodeError:
        # Try to extract array between first [ and last ]
        l = t.find("[")
        r = t.rfind("]")
        if l == -1 or r == -1 or r <= l:
            raise
        parsed = json.loads(t[l:r + 1])
    if isinstance(parsed, dict):
        for key in ("items", "paraphrases", "intents", "results"):
            if key in parsed and isinstance(parsed[key], list):
                parsed = parsed[key]
                break
    if not isinstance(parsed, list):
        raise ValueError(f"expected JSON array, got {type(parsed).__name__}")
    out = []
    for item in parsed:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[2]
    ap.add_argument("--caps", type=Path, default=repo / "capabilities")
    ap.add_argument("--skills", type=Path, default=repo / "skills")
    ap.add_argument("--out", type=Path, default=root / "data" / "intents.jsonl")
    ap.add_argument("--provider", choices=["anthropic", "openai"], default="anthropic")
    ap.add_argument("--model", type=str, default="")
    ap.add_argument("--n", type=int, default=10, help="paraphrases per trigger")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--only", type=str, default="", help="comma-separated list of capability names to process")
    ap.add_argument("--resume", action="store_true", help="append, skipping (label,source) pairs already present")
    args = ap.parse_args()

    model_name = args.model or {"anthropic": "claude-haiku-4-5", "openai": "gpt-4o-mini"}[args.provider]
    key_env = "ANTHROPIC_API_KEY" if args.provider == "anthropic" else "OPENAI_API_KEY"
    if not os.environ.get(key_env):
        print(f"set {key_env} env var", file=sys.stderr)
        return 1

    triggers_by_cap = load_triggers(args.caps, args.skills)
    if not triggers_by_cap:
        print("no capabilities found", file=sys.stderr)
        return 1

    if args.only:
        allow = {x.strip() for x in args.only.split(",") if x.strip()}
        triggers_by_cap = {k: v for k, v in triggers_by_cap.items() if k in allow}

    # Resume: build a set of (label, source) already in output.
    done: set[tuple[str, str]] = set()
    if args.resume and args.out.exists():
        with args.out.open() as f:
            for line in f:
                try:
                    row = json.loads(line)
                    done.add((row["label"], row["source"]))
                except (json.JSONDecodeError, KeyError):
                    continue
        print(f"resume: {len(done)} (label,source) pairs already present")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if args.resume else "w"

    # Build job list.
    jobs: list[tuple[str, str]] = []
    for label, triggers in triggers_by_cap.items():
        for trig in triggers:
            if (label, trig) in done:
                continue
            jobs.append((label, trig))

    if not jobs:
        print("nothing to do")
        return 0
    print(f"generating {args.n} paraphrases each for {len(jobs)} (label,trigger) pairs via {args.provider}:{model_name}")

    caller = call_anthropic if args.provider == "anthropic" else call_openai

    written = 0
    failures = 0
    with args.out.open(mode) as fp, ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(caller, model_name, label, trig, args.n): (label, trig) for label, trig in jobs}
        for fut in as_completed(futures):
            label, trig = futures[fut]
            try:
                paraphrases = fut.result()
            except Exception as e:  # noqa: BLE001
                print(f"[fail] {label}/{trig}: {e}", file=sys.stderr)
                failures += 1
                continue
            for p in paraphrases:
                fp.write(json.dumps({"label": label, "source": trig, "intent": p}) + "\n")
                written += 1
            fp.flush()

    print(f"wrote {written} paraphrases; {failures} failures")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
