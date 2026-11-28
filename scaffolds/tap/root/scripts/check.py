#!/usr/bin/env python3
"""Dependency-free structural validation for an Octomind user tap."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is the contract
    print("ERROR: validation requires Python 3.11 or newer", file=sys.stderr)
    raise SystemExit(2)

AGENT_NAME = re.compile(r"[a-z][a-z0-9-]*")
AGENT_HEADER = "# Agent:"
ORCHESTRATION_CAPABILITY = "orchestration"
SPECIALISTS_PATTERN = re.compile(r"\{\{\s*SPECIALISTS\s*\}\}")
DOMAINS_PATTERN = re.compile(r"\{\{\s*DOMAINS\s*\}\}")
USES_PATTERN = re.compile(r"\{\{\s*USES\s*\}\}")
USES_HEADER = "# Uses:"
# Entry for "every other agent"; it is not followed when looking for delegation loops.
USES_ALL = "*"
CYCLE_SEPARATOR = " → "

BUILTIN_SERVERS = {"core", "octofs", "agent", "octocode"}
SYSTEM_TAGS = [
    "identity",
    "voice",
    "scope",
    "workflow",
    "rules",
    "examples",
    "output_format",
    "interaction",
    "critical",
]
RENDER_TOKEN = re.compile(r"__[A-Z][A-Z0-9_]*__")


def parse_toml(path: Path, errors: list[str]):
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid TOML: {exc}")
        return None


def read_uses_header(raw: str) -> list[str] | None:
    """Entries of the '# Uses:' header comment, or None when the header is absent."""
    for line in raw.splitlines():
        if not line.startswith("#"):
            break
        if line.startswith(USES_HEADER):
            return [entry.strip() for entry in line[len(USES_HEADER):].split(",")]
    return None


def agent_exists(name: str, root: Path) -> bool:
    path = root / "agents" / f"{name}.toml"
    return path.is_file() and not path.is_symlink()


def find_uses_cycle(start: str, root: Path) -> list[str] | None:
    """Loop of named '# Uses:' entries from agent to agent that returns to `start`, or None."""

    def walk(current: str, trail: list[str]) -> list[str] | None:
        if not agent_exists(current, root):
            return None
        text = (root / "agents" / f"{current}.toml").read_text(encoding="utf-8")
        entries = []
        for entry in read_uses_header(text) or []:
            if entry == USES_ALL:
                # '*' reaches every other agent, so it can close a loop like any named entry.
                entries.extend(sorted(path.stem for path in (root / "agents").glob("*.toml") if path.stem != current))
            else:
                entries.append(entry)
        for entry in entries:
            if not AGENT_NAME.fullmatch(entry):
                continue
            if entry == start and len(trail) > 1:
                return trail + [entry]
            if entry in trail:
                continue
            found = walk(entry, trail + [entry])
            if found:
                return found
        return None

    return walk(start, [start])


def check_uses_entries(entries: list[str], name: str, root: Path) -> list[str]:
    problems = []
    seen = set()
    for entry in entries:
        if not entry:
            problems.append("USES_INVALID: empty entry in '# Uses:' (stray comma or no value)")
            continue
        if entry != USES_ALL and not AGENT_NAME.fullmatch(entry):
            problems.append(f"USES_INVALID: '{entry}' is malformed — write an agent name such as 'seo' (tags are flat, no ':'), or '{USES_ALL}'")
            continue
        if entry in seen:
            problems.append(f"USES_INVALID: '{entry}' is listed more than once")
            continue
        seen.add(entry)
        if entry == name:
            problems.append(f"USES_INVALID: '{entry}' is the agent itself")
        elif entry != USES_ALL and not agent_exists(entry, root):
            problems.append(f"USES_UNKNOWN: agent '{entry}' has no agents/{entry}.toml")
    if not problems:
        cycle = find_uses_cycle(name, root)
        if cycle:
            problems.append(f"USES_CYCLE: {CYCLE_SEPARATOR.join(cycle)} — agents that use each other would delegate in a loop")
    return problems


def validate_agent(path: Path, root: Path, errors: list[str]) -> None:
    agent_name = path.stem
    if path.parent != root / "agents":
        errors.append(f"{path}: AGENT_PATH: agents must be agents/<name>.toml")
    # An unrendered starter keeps its render token as the name; unresolved tokens are reported separately.
    if not AGENT_NAME.fullmatch(agent_name) and not RENDER_TOKEN.fullmatch(agent_name):
        errors.append(f"{path}: AGENT_NAME_INVALID: file name '{agent_name}' must match {AGENT_NAME.pattern} (tags are flat, no ':')")

    raw = path.read_text(encoding="utf-8")
    data = parse_toml(path, errors)
    if data is None:
        return

    title = re.search(r"^# Title:\s*(.+)$", raw, re.MULTILINE)
    description = re.search(r"^# Description:\s*(.+)$", raw, re.MULTILINE)
    if not title or not 5 <= len(title.group(1).strip()) <= 60:
        errors.append(f"{path}: # Title must contain 5–60 characters")
    if not description or not 20 <= len(description.group(1).strip()) <= 160:
        errors.append(f"{path}: # Description must contain 20–160 characters")
    header_lines = []
    for line in raw.splitlines():
        if not line.startswith("#"):
            break
        header_lines.append(line)
    agent_headers = [line[len(AGENT_HEADER):].strip() for line in header_lines if line.startswith(AGENT_HEADER)]
    if not agent_headers:
        errors.append(f"{path}: MISSING_AGENT_HEADER: '# Agent: {agent_name}' comment is required")
    elif agent_headers[0] != agent_name:
        errors.append(f"{path}: AGENT_HEADER_MISMATCH: '# Agent: {agent_headers[0]}' must equal the file name '{agent_name}'")
    if any(line.startswith("# Default:") for line in header_lines):
        errors.append(f"{path}: DEFAULT_HEADER_REMOVED: '# Default:' is not used; delete the header")

    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append(f"{path}: non-empty top-level capabilities array is required")
        capabilities = []
    for capability in capabilities:
        if not isinstance(capability, str):
            errors.append(f"{path}: capability names must be strings")
            continue
        prefix, _, name = capability.rpartition("/")
        if prefix:
            # `octomind/<name>` (baseline tap) or `<org>/<name>` (connected tap)
            # resolves from that tap at runtime, together with its dependencies.
            if "/" in prefix or not name:
                errors.append(f"{path}: capability '{capability}' must be '<name>' or '<tap>/<name>'")
            continue
        default = root / "capabilities" / capability / "default.toml"
        if not default.exists():
            errors.append(
                f"{path}: capability '{capability}' has no local default.toml "
                f"(reference the baseline tap as 'octomind/{capability}')"
            )

    if "deps" in data or "mcp" in data:
        errors.append(f"{path}: deps and MCP servers belong in capability files")

    roles = data.get("roles")
    if not isinstance(roles, list) or len(roles) != 1:
        errors.append(f"{path}: exactly one [[roles]] entry is required")
        return

    role = roles[0]
    if "name" in role:
        errors.append(f"{path}: roles.name is injected from the path and must be absent")
    if "mcp" in role:
        errors.append(f"{path}: [roles.mcp] belongs in capability files")
    for field in ("system", "welcome"):
        if field not in role:
            errors.append(f"{path}: missing role field '{field}'")
    for field in ("temperature", "top_p", "top_k"):
        if field in role:
            errors.append(f"{path}: `{field}` is deprecated and ignored by octomind; remove it")

    system = role.get("system")
    if not isinstance(system, str):
        return
    for placeholder in ("{{CWD}}", "{{DATE}}"):
        if placeholder in system:
            errors.append(f"{path}: {placeholder} must not appear in system")
    if "**" in system:
        errors.append(f"{path}: Markdown bold is not allowed in system")
    if re.search(r"^#{1,2}\s", system, re.MULTILINE):
        errors.append(f"{path}: use XML tags instead of # or ## headings in system")
    if "<identity>" not in system or "<critical>" not in system:
        errors.append(f"{path}: system requires <identity> and <critical> blocks")

    positions = []
    for tag in SYSTEM_TAGS:
        position = system.find(f"<{tag}>")
        if position >= 0:
            positions.append((tag, position))
    if positions != sorted(positions, key=lambda item: item[1]):
        errors.append(f"{path}: system XML blocks are not in canonical order")

    if SPECIALISTS_PATTERN.search(system):
        errors.append(f"{path}: SPECIALISTS_REMOVED: '{{{{SPECIALISTS}}}}' is not expanded; delete the placeholder")
    if DOMAINS_PATTERN.search(system):
        errors.append(f"{path}: DOMAINS_REMOVED: '{{{{DOMAINS}}}}' is not a placeholder; name agents in a '# Uses:' header ('# Uses: {USES_ALL}' for every agent)")
    uses_entries = read_uses_header(raw)
    if USES_PATTERN.search(system):
        errors.append(f"{path}: USES_PLACEHOLDER_REMOVED: '{{{{USES}}}}' is not expanded; the '# Uses:' header alone sets which agents tasks may be matched to, so delete the placeholder")
    if uses_entries is not None:
        errors.extend(f"{path}: {problem}" for problem in check_uses_entries(uses_entries, agent_name, root))
        if not any(
            isinstance(capability, str) and capability.rpartition("/")[2] == ORCHESTRATION_CAPABILITY
            for capability in capabilities
        ):
            errors.append(f"{path}: USES_NO_ORCHESTRATION: an agent with a '# Uses:' header must declare the '{ORCHESTRATION_CAPABILITY}' capability")


def validate_capability(cap_dir: Path, root: Path, errors: list[str]) -> None:
    default = cap_dir / "default.toml"
    if not default.exists():
        errors.append(f"{cap_dir}: missing default.toml")
        return
    data = parse_toml(default, errors)
    if data is None:
        return

    roles = data.get("roles", {})
    mcp = roles.get("mcp", {}) if isinstance(roles, dict) else {}
    refs = mcp.get("server_refs", []) if isinstance(mcp, dict) else []
    servers = data.get("mcp", {}).get("servers", []) if isinstance(data.get("mcp"), dict) else []
    server_names = {
        server.get("name") for server in servers if isinstance(server, dict)
    }
    for ref in refs:
        if ref not in BUILTIN_SERVERS and ref not in server_names:
            errors.append(f"{default}: server_ref '{ref}' has no MCP server definition")

    deps = data.get("deps", {}).get("require", []) if isinstance(data.get("deps"), dict) else []
    for dependency in deps:
        script = root / "deps" / f"{dependency}.sh"
        document = root / "deps" / f"{dependency}.md"
        if not script.is_file():
            errors.append(f"{default}: dependency '{dependency}' has no {script.relative_to(root)}")
        if not document.is_file():
            errors.append(f"{default}: dependency '{dependency}' has no {document.relative_to(root)}")


def validate_skill(path: Path, errors: list[str]) -> None:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.DOTALL)
    if not match:
        errors.append(f"{path}: missing YAML frontmatter")
        return
    frontmatter, body = match.groups()
    fields = {}
    for line in frontmatter.splitlines():
        field = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if field:
            fields[field.group(1)] = field.group(2).strip().strip("\"'")
    for required in ("name", "title", "description"):
        if not fields.get(required):
            errors.append(f"{path}: frontmatter field '{required}' is required")
    if fields.get("name") != path.parent.name:
        errors.append(f"{path}: frontmatter name must match directory '{path.parent.name}'")
    if "**" in body:
        errors.append(f"{path}: Markdown bold is not allowed in skill bodies")


def validate_dep(path: Path, errors: list[str]) -> None:
    raw = path.read_text(encoding="utf-8")
    for header in ("dep", "type", "description", "check"):
        if not re.search(rf"^# {header}:\s*\S", raw, re.MULTILINE):
            errors.append(f"{path}: missing '# {header}:' header")
    document = path.with_suffix(".md")
    if not document.is_file():
        errors.append(f"{path}: missing companion document {document.name}")
    if "deps/lib/platform.sh" not in raw and 'DEPS_LIB/platform.sh' not in raw:
        errors.append(f"{path}: must source deps/lib/platform.sh")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--template", action="store_true", help="allow scaffold render tokens")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors: list[str] = []

    for required in ("README.md", "AGENTS.md", "agents", "capabilities", "deps", "skills", "workflows"):
        if not (root / required).exists():
            errors.append(f"{root / required}: required scaffold path is missing")

    if not args.template:
        for path in root.rglob("*"):
            if RENDER_TOKEN.search(path.name):
                errors.append(f"{path}: unresolved render token in path")
            if path.is_file() and not path.is_symlink():
                try:
                    raw = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if RENDER_TOKEN.search(raw):
                    errors.append(f"{path}: unresolved render token in contents")

    agents_dir = root / "agents"
    for path in sorted(agents_dir.iterdir() if agents_dir.is_dir() else []):
        if path.is_symlink():
            errors.append(f"{path}: AGENT_SYMLINK: agents are regular files, not symlinks")
        elif path.is_dir():
            errors.append(f"{path}: AGENT_SUBDIR: agents live directly in agents/<name>.toml, not in subdirectories")
        elif path.suffix == ".toml":
            validate_agent(path, root, errors)
    for cap_dir in sorted((root / "capabilities").iterdir() if (root / "capabilities").is_dir() else []):
        if cap_dir.is_dir():
            validate_capability(cap_dir, root, errors)
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        validate_skill(path, errors)
    for path in sorted((root / "deps").glob("*/*.sh")):
        if path.parent.name != "lib":
            validate_dep(path, errors)
    for path in sorted((root / "workflows").glob("*.toml")):
        parse_toml(path, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Tap validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Tap validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
