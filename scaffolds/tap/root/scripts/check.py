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


def validate_agent(path: Path, root: Path, errors: list[str]) -> None:
    relative = path.relative_to(root / "agents")
    if len(relative.parts) != 2:
        errors.append(f"{path}: agents must use agents/<domain>/<spec>.toml")

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

    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append(f"{path}: non-empty top-level capabilities array is required")
        capabilities = []
    for capability in capabilities:
        if not isinstance(capability, str):
            errors.append(f"{path}: capability names must be strings")
            continue
        default = root / "capabilities" / capability / "default.toml"
        if not default.exists():
            errors.append(f"{path}: capability '{capability}' has no local default.toml")

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
    for field in ("system", "welcome", "temperature", "top_p", "top_k"):
        if field not in role:
            errors.append(f"{path}: missing role field '{field}'")

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

    for path in sorted((root / "agents").glob("**/*.toml")):
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

