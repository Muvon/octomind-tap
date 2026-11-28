#!/usr/bin/env python3
"""Skill gate: replay the runtime's skill rule engine on the labelled task briefs.

  uv run python scripts/eval_skills.py --model checkpoints/<run> [--split eval] [--agent NAME ...]
                                       [--misses SKILL] [--limit N] [--json out.json]

`--model` is a sentence-transformers directory (fp32 weights), an `onnx/`
directory holding `model_quantized.onnx` (the graph the runtime loads), or a hub
id with an optional revision, `muvon/octomind-embed@<sha>`, whose
`onnx/model_quantized.onnx` is used.

Every brief of `data/agent_briefs.jsonl` carries its agent and the skills that
hold its procedure (`skills`). Reproduces octomind's skill_auto::run_activation:

  * the message is stripped of <tag>...</tag> blocks, and abstains below 8
    non-whitespace characters (the keyword column ignores both);
  * the pool of a brief is every skill offered to its agent: the skills the
    agent owns, and the shared ones whose `domains:` has the agent (or `*`);
  * a rule line is an AND-group; a group with no semantic() check that matches
    loads its skill unconditionally;
  * a group with semantic() that matches makes the skill a candidate scored by
    the best cosine among that group's semantic checks (best group per skill);
    only the top candidate loads, and only if it beats #2 (or 0.0) by
    SEMANTIC_MARGIN;
  * semantic(phrase, 0.7): the last comma piece is the threshold if it parses
    as a float, else the default 0.68.

Columns per skill (own = briefs that carry the skill, other = briefs of the
agent's other work that load it):
  kw    keyword lines only
  full  keyword + semantic with threshold and margin
  reach full without the margin rule (top candidate always loads)
Targets, judged on full: own >= 70%, other <= 8%.

The skills measured are those that appear on any brief. The per-skill table and
the three summary lines count the skills that head a brief's `skills` list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skill_rules  # noqa: E402
from eval_gate import OnnxEncoder  # noqa: E402

SEMANTIC_MARGIN = 0.05  # skill.rs
MIN_INTENT_NON_WS_CHARS = 8  # skill_auto.rs
MAX_SEQ_LEN = 512  # octolib onnx.rs
MISSES_SHOWN = 12
BATCH = 32
OWN_TARGET, OTHER_TARGET = 0.70, 0.08
MODES = ("kw", "full", "reach")
SNAPSHOT_FILES = ["onnx/model_quantized.onnx", "tokenizer.json", "1_Pooling/config.json"]

_UNSUPPORTED_REGEX = re.compile(r"\(\?[=!<]|\\[1-9]")


# ------------------------------------------------------------------ embedding


def load_embedder(model: str):
    """Something with `.encode(texts, normalize_embeddings=True, convert_to_numpy=True, batch_size=)`."""
    path = Path(model)
    if path.is_dir():
        if (path / "model_quantized.onnx").exists():
            return OnnxEncoder(path, "model_quantized.onnx")
        from sentence_transformers import SentenceTransformer

        embedder = SentenceTransformer(str(path))
        embedder.max_seq_length = MAX_SEQ_LEN
        return embedder
    from huggingface_hub import snapshot_download

    repo_id, _, revision = model.partition("@")
    snapshot = snapshot_download(repo_id, revision=revision or None, allow_patterns=SNAPSHOT_FILES)
    return OnnxEncoder(Path(snapshot), "onnx/model_quantized.onnx")


def embed(embedder, texts: list[str]) -> dict[str, np.ndarray]:
    ordered = sorted(set(texts), key=len)  # length-sorted batches carry little padding
    vectors = embedder.encode(ordered, normalize_embeddings=True, convert_to_numpy=True, batch_size=BATCH)
    return dict(zip(ordered, vectors))


# ------------------------------------------------------------ message handling


def strip_xml_blocks(text: str) -> str:
    """Port of skill_auto::strip_xml_blocks."""
    if "<" not in text:
        return text
    out, rest = [], text
    while True:
        open_start = rest.find("<")
        if open_start < 0:
            break
        after = rest[open_start + 1:]
        end = next((i for i, c in enumerate(after) if not (c.isalnum() or c in "-_")), len(after))
        tag = after[:end]
        if not tag:
            out.append(rest[:open_start + 1])
            rest = rest[open_start + 1:]
            continue
        close_tag = f"</{tag}>"
        close_pos = rest.find(close_tag)
        if close_pos >= 0:
            out.append(rest[:open_start])
            rest = rest[close_pos + len(close_tag):]
        else:
            out.append(rest[:open_start + 1])
            rest = rest[open_start + 1:]
    out.append(rest)
    return "".join(out)


def runtime_text(text: str) -> str | None:
    """What the rule engine sees, or None when it abstains for lack of signal."""
    stripped = strip_xml_blocks(text)
    if sum(not c.isspace() for c in stripped) < MIN_INTENT_NON_WS_CHARS:
        return None
    return stripped


def message_checks_pass(group, text: str, cosines: dict[str, float] | None) -> bool | None:
    """All content/match/semantic checks of the group hold; None when it has none of them."""
    judged = False
    for kind, arg in group:
        if kind == "content":
            judged = True
            if not re.search(rf"(?i)\b{re.escape(arg.strip())}\b", text):
                return False
        elif kind == "match":
            judged = True
            if not re.search(arg, text):
                return False
        elif kind == "semantic":
            judged = True
            if cosines[arg[0]] < arg[1]:
                return False
    return True if judged else None


# ------------------------------------------------------------------ the engine


class Outcome:
    """Result of one activation cycle for one brief."""

    def __init__(self, pool: dict[str, list], raw: str, text: str | None, cosines: dict[str, float] | None):
        self.keyword = set()
        self.det = set()
        self.candidates = {}  # skill -> best group score
        self.best_cosine = {}  # skill -> (best cosine over its semantic checks, phrase)
        self.full_winner = self.reach_winner = None
        self.abstained = None
        for name, groups in pool.items():
            if any(not any(k == "semantic" for k, _ in g) and message_checks_pass(g, raw, None) for g in groups):
                self.keyword.add(name)
        if text is None:
            return
        for name, groups in pool.items():
            best = None
            for g in groups:
                sem = [arg for k, arg in g if k == "semantic"]
                for phrase, _ in sem:
                    if name not in self.best_cosine or cosines[phrase] > self.best_cosine[name][0]:
                        self.best_cosine[name] = (cosines[phrase], phrase)
                if not message_checks_pass(g, text, cosines):
                    continue
                if not sem:
                    self.det.add(name)
                    break
                score = max(cosines[p] for p, _ in sem)
                if best is None or score > best:
                    best = score
            else:
                if best is not None:
                    self.candidates[name] = best
        ranked = sorted(self.candidates.items(), key=lambda item: (-item[1], item[0]))
        if ranked:
            self.reach_winner = ranked[0][0]
            top2 = ranked[1][1] if len(ranked) > 1 else 0.0
            if ranked[0][1] - top2 >= SEMANTIC_MARGIN:
                self.full_winner = ranked[0][0]
            else:
                self.abstained = (ranked[0], ranked[1] if len(ranked) > 1 else None)

    def loads(self, skill: str, mode: str) -> bool:
        if mode == "kw":
            return skill in self.keyword
        if skill in self.det:
            return True
        return skill == (self.full_winner if mode == "full" else self.reach_winner)

    def describe_loaded(self) -> str:
        parts = sorted(self.det)
        if self.full_winner:
            parts.append(f"{self.full_winner} (semantic {self.candidates[self.full_winner]:.3f})")
        if parts:
            return "loaded: " + ", ".join(parts)
        if self.abstained:
            (n1, s1), second = self.abstained
            tail = f", {second[0]} {second[1]:.3f}" if second else ""
            return f"nothing loaded; semantic abstained: {n1} {s1:.3f}{tail}"
        return "nothing loaded"


def unsupported_rules(skills: dict[str, skill_rules.Skill]) -> list[str]:
    """Regexes Python accepts but octomind's Rust regex engine rejects."""
    bad = []
    for name, skill in skills.items():
        for group in skill.groups:
            for kind, arg in group:
                if kind != "match":
                    continue
                try:
                    re.compile(arg)
                except re.error as error:
                    bad.append(f"{name}: invalid regex ({error}): {arg[:60]}")
                if _UNSUPPORTED_REGEX.search(arg):
                    bad.append(f"{name}: lookaround or backreference, not valid in Rust regex: {arg[:60]}")
    return bad


# ------------------------------------------------------------------ evaluation


def load_briefs(path: Path, skills: dict[str, skill_rules.Skill]) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    unknown = sorted({s for r in rows for s in r["skills"]} - set(skills))
    if unknown:
        raise SystemExit(f"{path} names skills that do not exist: {unknown}")
    return rows


def evaluate(embedder, skills: dict[str, skill_rules.Skill], all_rows: list[dict], split: str,
             agents: list[str] = (), misses_skill: str | None = None):
    """Hit counts per mode and skill, the per-skill table order, and the misses of `misses_skill`.

    Returns (hits, primary, missed, noise). `hits[mode][side][skill]` is
    [briefs that loaded it, briefs]; `primary` maps each skill that heads some
    brief's `skills` list to the agent of the first such brief.
    """
    rows = [r for r in all_rows if r["split"] == split and (not agents or r["agent"] in agents)]
    measured = {s for r in all_rows for s in r["skills"]}
    primary: dict[str, str] = {}
    for r in all_rows:
        if r["skills"]:
            primary.setdefault(r["skills"][0], r["agent"])

    phrases = sorted({arg[0] for s in skills.values() for g in s.groups for kind, arg in g if kind == "semantic"})
    runtime = {r["brief"]: runtime_text(r["brief"]) for r in rows}
    vectors = embed(embedder, phrases + [t for t in runtime.values() if t])
    phrase_matrix = np.stack([vectors[p] for p in phrases])

    hits = {m: {"own": defaultdict(lambda: [0, 0]), "other": defaultdict(lambda: [0, 0])} for m in MODES}
    missed, noise = defaultdict(list), defaultdict(list)
    for n, row in enumerate(rows, 1):
        agent, text = row["agent"], runtime[row["brief"]]
        pool = {nm: s.groups for nm, s in skills.items() if (agent in s.domains or "*" in s.domains) and s.groups}
        cosines = dict(zip(phrases, (phrase_matrix @ vectors[text]).tolist())) if text else None
        outcome = Outcome(pool, row["brief"], text, cosines)
        own = set(row["skills"])
        for skill in measured:
            if agent not in skills[skill].domains and "*" not in skills[skill].domains:
                continue
            side = "own" if skill in own else "other"
            for mode in MODES:
                cell = hits[mode][side][skill]
                cell[1] += 1
                cell[0] += outcome.loads(skill, mode)
            if misses_skill == skill:
                if side == "own" and not outcome.loads(skill, "full"):
                    cos = outcome.best_cosine.get(skill)
                    info = f"best semantic {cos[0]:.3f} ({cos[1][:50]})" if cos else "no semantic rule"
                    if skill in outcome.candidates:
                        info += f", candidate score {outcome.candidates[skill]:.3f}"
                    missed[skill].append(f"[{row['source']}] {info}; {outcome.describe_loaded()}\n    {row['brief'][:300]}")
                elif side == "other" and outcome.loads(skill, "full"):
                    noise[skill].append(f"[{row['source']}] {outcome.describe_loaded()}\n    {row['brief'][:300]}")
        if n % 500 == 0:
            print(f"scored {n}/{len(rows)} briefs", file=sys.stderr)
    return hits, primary, missed, noise


def skill_cells(hits, mode: str, skill: str):
    h, f = hits[mode]["own"][skill], hits[mode]["other"][skill]
    recall = h[0] / h[1] if h[1] else 0
    false_rate = f[0] / f[1] if f[1] else 0
    return recall, false_rate, f"own {h[0]}/{h[1]} ({recall:.0%}) other {f[0]}/{f[1]} ({false_rate:.0%})"


def summarize(hits, primary: dict[str, str], agents: list[str] = (), print_table: bool = False) -> dict[str, dict]:
    """Per mode: own/other hits and briefs over the primary skills, and how many meet the targets."""
    totals = {m: {"own_hit": 0, "own_n": 0, "other_hit": 0, "other_n": 0, "skills_ok": 0, "skills": 0} for m in MODES}
    for skill, agent in sorted(primary.items(), key=lambda item: (item[1], item[0])):
        if agents and agent not in agents:
            continue
        cells, flags = {}, {}
        for mode in MODES:
            recall, false_rate, cells[mode] = skill_cells(hits, mode, skill)
            flags[mode] = recall >= OWN_TARGET and false_rate <= OTHER_TARGET
            t = totals[mode]
            t["own_hit"] += hits[mode]["own"][skill][0]
            t["own_n"] += hits[mode]["own"][skill][1]
            t["other_hit"] += hits[mode]["other"][skill][0]
            t["other_n"] += hits[mode]["other"][skill][1]
            t["skills_ok"] += flags[mode]
            t["skills"] += 1
        if print_table:
            print(f"{'ok  ' if flags['full'] else 'FIX '} {agent:18} {skill:38} "
                  f"kw: {cells['kw']} | full: {cells['full']} | reach: {cells['reach']}")
    return totals


def summary_line(split: str, mode: str, t: dict) -> str:
    own_rate = t["own_hit"] / t["own_n"] if t["own_n"] else 0
    other_rate = t["other_hit"] / t["other_n"] if t["other_n"] else 0
    return (f"split={split} {mode:5}: own {t['own_hit']}/{t['own_n']} ({own_rate:.1%}) "
            f"other {t['other_hit']}/{t['other_n']} ({other_rate:.1%})"
            f"  {t['skills_ok']}/{t['skills']} skills meet own>=70% and other<=8%")


def to_numbers(split: str, totals: dict[str, dict]) -> dict:
    """The summary lines as numbers; `right_rate` is the own hit rate, `wrong_rate` the other one."""
    modes = {}
    for mode, t in totals.items():
        modes[mode] = {
            **t,
            "right_rate": t["own_hit"] / t["own_n"] if t["own_n"] else 0.0,
            "wrong_rate": t["other_hit"] / t["other_n"] if t["other_n"] else 0.0,
        }
    return {"split": split, "modes": modes}


def main() -> int:
    ap = argparse.ArgumentParser()
    root = Path(__file__).resolve().parents[1]
    ap.add_argument("--model", required=True,
                    help="sentence-transformers dir, onnx/ dir, or hub id[@revision] (its onnx/model_quantized.onnx)")
    ap.add_argument("--repo", type=Path, default=skill_rules.REPO, help="tap checkout holding skills/ and agents/")
    ap.add_argument("--briefs", type=Path, default=root / "data" / "agent_briefs.jsonl")
    ap.add_argument("--split", default="eval", choices=["train", "eval"])
    ap.add_argument("--agent", nargs="*", default=[], help="only briefs of these agents")
    ap.add_argument("--misses", help="list the briefs a skill missed and the ones that loaded it by mistake")
    ap.add_argument("--limit", type=int, default=MISSES_SHOWN)
    ap.add_argument("--json", type=Path, default=None, help="write the three summary lines as numbers")
    args = ap.parse_args()

    skills = skill_rules.load_skills(args.repo)
    all_rows = load_briefs(args.briefs, skills)
    embedder = load_embedder(args.model)
    hits, primary, missed, noise = evaluate(embedder, skills, all_rows, args.split, args.agent, args.misses)

    for problem in unsupported_rules(skills):
        print("BAD RULE", problem)

    if args.misses:
        print(f"== {args.misses}: own briefs the full engine did not load it for")
        for item in missed[args.misses][:args.limit]:
            print("-", item)
        print(f"== {args.misses}: other briefs that loaded it")
        for item in noise[args.misses][:args.limit]:
            print("-", item)
        return 0

    totals = summarize(hits, primary, args.agent, print_table=True)
    print()
    for mode in MODES:
        print(summary_line(args.split, mode, totals[mode]))
    # The denominators: a change in either count moves every rate above.
    n_briefs = sum(1 for r in all_rows if r["split"] == args.split and (not args.agent or r["agent"] in args.agent))
    n_measured = len({s for r in all_rows for s in r["skills"]})
    print(f"scored {n_briefs} {args.split} briefs; {totals['full']['skills']} skills counted in the summary "
          f"(of {n_measured} carried by any brief)")
    if args.json:
        counts = {"briefs": n_briefs, "skills_counted": totals["full"]["skills"], "skills_measured": n_measured}
        args.json.write_text(json.dumps({"model": args.model, **counts, **to_numbers(args.split, totals)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
