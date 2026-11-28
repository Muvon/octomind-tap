"""Skill rule parsing shared by the dataset scripts and eval_skills.py.

A skill's `rules:` frontmatter block is a list of lines. Each line is an AND
group of checks (`content(..)`, `match(..)`, `semantic(..)`, `file(..)` ...);
the lines are OR branches. `semantic(phrase)` or `semantic(phrase, 0.76)` asks
whether the user message is close enough to the phrase: the trailing number is
that phrase's threshold, not part of the phrase the model is trained on.

Skills live in two places (`scripts/tap_paths.py` at the repository root): the
shared `skills/<name>/` bound through `domains:`, and `agents/<ns>/skills/<name>/`,
owned by the agent `<ns>` by location.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import tap_paths  # noqa: E402

# skill.rs SEMANTIC_DEFAULT_THRESHOLD: the threshold of a `semantic(phrase)` with no number.
SEMANTIC_DEFAULT_THRESHOLD = 0.68

_CHECK = re.compile(r"(content|match|semantic|file|grep|env|bin|workdir|session)\(")
_DOMAINS = re.compile(r"^domains:\s*(.+)$", re.M)
_RULES = re.compile(r"^rules:\n((?:\s+- .*\n?)+)", re.M)


@dataclass
class Skill:
    name: str
    domains: list[str]  # agents the skill is offered to; "*" = every agent
    groups: list[list[tuple[str, object]]]  # rule lines; semantic args are (phrase, threshold)


def split_checks(rule: str) -> list[tuple[str, str]]:
    """The `kind(arg)` checks of one rule line, with balanced parentheses in the arg."""
    checks, i = [], 0
    while True:
        m = _CHECK.search(rule, i)
        if not m:
            return checks
        depth, j = 1, m.end()
        while j < len(rule) and depth:
            depth += rule[j] == "("
            depth -= rule[j] == ")"
            j += 1
        checks.append((m.group(1), rule[m.end():j - 1]))
        i = j


def parse_semantic(arg: str) -> tuple[str, float] | None:
    """Runtime `ActivateCheck::parse` for semantic(): (phrase, threshold), or None when empty."""
    arg = arg.strip()
    if not arg:
        return None
    phrase, sep, tail = arg.rpartition(",")
    if sep:
        try:
            threshold = float(tail.strip())
        except ValueError:
            return arg, SEMANTIC_DEFAULT_THRESHOLD
        phrase = phrase.strip()
        return (phrase, threshold) if phrase else None
    return arg, SEMANTIC_DEFAULT_THRESHOLD


def _parse_domains(value: str) -> list[str]:
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        return [p.strip().strip("\"'") for p in value[1:-1].split(",") if p.strip().strip("\"'")]
    return value.split()


def load_skills(repo: Path = REPO) -> dict[str, Skill]:
    skills: dict[str, Skill] = {}
    for skill_dir in tap_paths.skill_dirs(repo):
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---")[1]
        owner = tap_paths.skill_owner(repo, skill_dir)
        domains_line = _DOMAINS.search(frontmatter)
        block = _RULES.search(frontmatter)
        groups: list[list[tuple[str, object]]] = []
        for rule_line in block.group(1).splitlines() if block else []:
            group: list[tuple[str, object]] = []
            for kind, arg in split_checks(rule_line.strip()[2:]):
                if kind == "semantic":
                    parsed = parse_semantic(arg)
                    if parsed:
                        group.append((kind, parsed))
                else:
                    group.append((kind, arg))
            if group:
                groups.append(group)
        domains = [owner] if owner else _parse_domains(domains_line.group(1)) if domains_line else []
        skills[skill_dir.name] = Skill(skill_dir.name, domains, groups)
    return skills


def semantic_phrases(skills: dict[str, Skill]) -> dict[str, list[str]]:
    """{skill: its distinct semantic() phrases in rule order}, skills without any left out."""
    out: dict[str, list[str]] = {}
    for name, skill in skills.items():
        phrases = list(dict.fromkeys(arg[0] for group in skill.groups for kind, arg in group if kind == "semantic"))
        if phrases:
            out[name] = phrases
    return out
