"""Where the tap keeps agents and skills.

Base agent:      agents/<ns>/default.toml  (tag `<ns>`)
Variant:         agents/<ns>/<variant>.toml  (tag `<ns>:<variant>`; private taps only)
Owned skill:     agents/<ns>/skills/<skill>/SKILL.md  (belongs to the namespace <ns> by location)
Shared skill:    skills/<skill>/SKILL.md                (bound through `domains:`, or manual-only)

Import from a script, or list from shell:
  python3 scripts/tap_paths.py agents <repo-root>   # one manifest path per line
  python3 scripts/tap_paths.py skills <repo-root>   # one skill directory per line
"""

import sys
from pathlib import Path

AGENT_MANIFEST = "default.toml"
SKILLS_DIR = "skills"


def agent_manifests(root):
    """Base agent file of every namespace directory under agents/ that has one, sorted."""
    return sorted(root.glob(f"agents/*/{AGENT_MANIFEST}"))


def skill_dirs(root):
    """Every skill directory: the shared ones, then the ones owned by an agent."""
    shared = sorted(p for p in (root / SKILLS_DIR).glob("*") if p.is_dir())
    owned = sorted(p for p in root.glob(f"agents/*/{SKILLS_DIR}/*") if p.is_dir())
    return shared + owned


def find_skill_dirs(root, name):
    """Skill directories called `name` in either location; more than one is a lint error."""
    return [p for p in skill_dirs(root) if p.name == name]


def skill_owner(root, skill_dir):
    """Namespace that owns the skill by location, or None for a shared skill."""
    relative = skill_dir.resolve().relative_to(root.resolve())
    return relative.parts[1] if relative.parts[0] == "agents" else None


if __name__ == "__main__":
    listing, repo_root = sys.argv[1], Path(sys.argv[2])
    paths = agent_manifests(repo_root) if listing == "agents" else skill_dirs(repo_root)
    for path in paths:
        print(path)
