"""Generate task briefs per agent with an LLM, for the routing half of the dataset.

`tap(action="run")` matches a task brief against each reachable agent's
"<title>. <description>" (octomind/src/mcp/orchestration/tap_route.rs). An
agent manifest gives the document but no example of a brief that should
reach it, so the briefs are generated here: for one agent at a time, with
every agent shown as the roster it must be told apart from.

Output: model/data/agent_briefs.jsonl, one JSON object per line:
  {"agent": "<name>", "split": "train|eval", "style": "<style>",
   "brief": "<text>", "model": "<llm id>", "skills": [...], "source": "<tag>"}

`skills` names the skills that hold the procedure the brief asks for, and
`source` the tag the brief was written for. A brief written here carries no
skills and its source is the agent; briefs carried over from earlier
corpora keep their own source tag and skills.

The two splits come from two different models so the eval briefs do not
share a writer with the training briefs. `build_dataset.py` reads the
train split, `eval_route.py` the eval split.

Brief length matters. A lead's real brief carries the user's request, error
text and specs and runs to thousands of characters, while the runtime
embeds only its first 512 tokens (octolib's ONNX provider truncates there).
The `long` style is written past that window so both training and the eval
see what the runtime sees: the opening of a long brief, cut mid-material.

The file is a frozen record and every run only adds what is missing: an
agent, split or style that has no briefs yet. Eval briefs written once
stay, so routing scores remain comparable across retrains. To replace an
agent's briefs (its description changed), delete its lines first.

  uv run python scripts/augment_agents.py                  # whatever is missing
  uv run python scripts/augment_agents.py --only developer  # one agent
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_dataset import load_agents  # noqa: E402

# style -> briefs per agent, per split.
STYLE_COUNTS: dict[str, dict[str, int]] = {
    "train": {"lead": 6, "short": 6, "user": 4, "full": 4, "long": 3},
    "eval": {"lead": 3, "short": 3, "user": 2, "full": 2, "long": 2},
}

SPLIT_MODELS: dict[str, str] = {
    "train": "claude-sonnet-5-5",
    "eval": "claude-opus-5-5",
}

# How much of the manifest's own notes the writer sees per agent.
NOTES_MAX_CHARS = 1500

SYSTEM_PROMPT = """You write task briefs for a dataset that trains a router. The router reads one task brief and hands it to the right member of a team.

You get the team roster (name, title, description of each member) and one TARGET member with notes on how it works. Write briefs for tasks the TARGET should take.

Rules:
- Every brief is a concrete task with invented but realistic specifics: file paths, product names, numbers, dates, people. No placeholders like <name> or [company].
- The task must clearly belong to the TARGET and to no other member of the roster. If another member would fit equally well, write a different task.
- Describe the work itself. Do not reuse the wording of the TARGET's title or description, and never mention a member's name or title or the word "agent".
- Cover different parts of what the TARGET does. No two briefs about the same task.
- Write in English.

Styles:
- lead: written by the team lead who delegates the task. The first sentence names the kind of work and the deliverable (for example "Implement a bug fix: ...", "Write tests for ...", "Draft a demand letter for ..."), then one to three sentences of context. 30 to 90 words.
- short: one sentence of 8 to 20 words, the task and nothing else.
- user: how an end user would ask an assistant for this in a chat, casual wording, 10 to 40 words.
- full: a structured brief with four labelled parts, OBJECTIVE, CONTEXT, SOURCE MATERIAL, OUTPUT SHAPE, one or two sentences each. 80 to 160 words.
- long: the complete brief a lead sends, 500 to 900 words. The first line names the kind of work and the deliverable. Then four labelled parts. OBJECTIVE: one deliverable in its exact form. CONTEXT: the setup, constraints and decisions already made. SOURCE MATERIAL: the requester's message quoted verbatim, then the raw material the worker cannot find alone, written out in full with invented content in labelled blocks (error output, logs, document excerpts, data rows, earlier correspondence). OUTPUT SHAPE AND BOUNDARIES: return format, acceptance criteria, what must not be touched. Last line: "Return the complete result in your final message. Assume I cannot see your tools, files, or intermediate steps."

Write only the styles the request asks for. Output exactly one JSON object and nothing else, no prose and no markdown fences, one key per requested style:
{"lead": ["..."], "short": ["..."]}"""

USER_TEMPLATE = """Team roster:
{roster}

TARGET: {tag}
Title: {title}
Description: {description}
Notes from the TARGET's own instructions:
{notes}

Write {counts} for the TARGET."""

_NOTE_TAGS = ("identity", "scope")


def agent_notes(manifest: str) -> str:
    """The identity and scope sections of the agent's system prompt, capped."""
    parts: list[str] = []
    for tag in _NOTE_TAGS:
        section = re.search(rf"<{tag}>(.*?)</{tag}>", manifest, re.S)
        if section:
            parts.append(section.group(1).strip())
    return "\n".join(parts)[:NOTES_MAX_CHARS] or "(none)"


def build_user_prompt(agent: dict, roster: list[dict], counts: dict[str, int]) -> str:
    roster_lines = "\n".join(f"- {a['tag']}: {a['text']}" for a in roster)
    wanted = ", ".join(f"{n} {style} briefs" for style, n in counts.items())
    return USER_TEMPLATE.format(
        roster=roster_lines,
        tag=agent["tag"],
        title=agent["title"],
        description=agent["description"],
        notes=agent_notes(agent["manifest"]),
        counts=wanted,
    )


def parse_briefs(text: str, counts: dict[str, int]) -> dict[str, list[str]]:
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object in the reply")
    parsed = json.loads(text[start : end + 1])
    out: dict[str, list[str]] = {}
    for style, wanted in counts.items():
        briefs = [b.strip() for b in parsed.get(style, []) if isinstance(b, str) and b.strip()]
        if len(briefs) < wanted:
            raise ValueError(f"{style}: wanted {wanted} briefs, got {len(briefs)}")
        out[style] = briefs[:wanted]
    return out


def generate(model: str, agent: dict, roster: list[dict], counts: dict[str, int], max_retries: int = 3):
    import anthropic

    client = anthropic.Anthropic()
    user = build_user_prompt(agent, roster, counts)
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=16000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user}],
            )
            text = "".join(b.text for b in msg.content if hasattr(b, "text"))
            return parse_briefs(text, counts)
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"{agent['tag']}: {last_err}")


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    repo = Path(__file__).resolve().parents[2]
    ap.add_argument("--repo", type=Path, default=repo, help="tap checkout holding agents/")
    ap.add_argument("--out", type=Path, default=root / "data" / "agent_briefs.jsonl")
    ap.add_argument("--split", choices=["train", "eval", "both"], default="both")
    ap.add_argument("--only", type=str, default="", help="comma-separated agent names")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("set ANTHROPIC_API_KEY env var", file=sys.stderr)
        return 1

    roster = load_agents(args.repo)
    agents = roster

    if args.only:
        allow = {x.strip() for x in args.only.split(",") if x.strip()}
        agents = [a for a in roster if a["tag"] in allow]
        if len(agents) != len(allow):
            raise SystemExit(f"--only names no agent: {sorted(allow - {a['tag'] for a in agents})}")

    done: set[tuple[str, str, str]] = set()
    if args.out.exists():
        with args.out.open() as f:
            for line in f:
                row = json.loads(line)
                done.add((row["agent"], row["split"], row["style"]))
        print(f"{len(done)} (agent, split, style) already present")

    splits = ["train", "eval"] if args.split == "both" else [args.split]
    jobs: list[tuple[dict, str, dict[str, int]]] = []
    for agent in agents:
        for split in splits:
            missing = {s: n for s, n in STYLE_COUNTS[split].items() if (agent["tag"], split, s) not in done}
            if missing:
                jobs.append((agent, split, missing))
    if not jobs:
        print("nothing to do")
        return 0
    print(f"generating briefs for {len(jobs)} (agent, split) jobs")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    written = failures = 0
    with args.out.open("a") as fp, ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(generate, SPLIT_MODELS[split], agent, roster, counts): (agent, split)
            for agent, split, counts in jobs
        }
        for fut in as_completed(futures):
            agent, split = futures[fut]
            try:
                briefs = fut.result()
            except Exception as e:  # noqa: BLE001
                print(f"[fail] {split} {e}", file=sys.stderr)
                failures += 1
                continue
            for style, texts in briefs.items():
                for text in texts:
                    fp.write(json.dumps({
                        "agent": agent["tag"],
                        "split": split,
                        "style": style,
                        "brief": text,
                        "model": SPLIT_MODELS[split],
                        "skills": [],
                        "source": agent["tag"],
                    }, ensure_ascii=False) + "\n")
                    written += 1
            fp.flush()

    print(f"wrote {written} briefs; {failures} failures")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
