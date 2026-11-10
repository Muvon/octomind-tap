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

CHIEF_SPEC = "chief"
GLOBAL_AGENT_TAG = "assistant:concierge"
ORCHESTRATION_CAPABILITY = "orchestration"
STARTER_SPEC_TOKEN = "__AGENT_SPEC__"
SPECIALISTS_PATTERN = re.compile(r"\{\{\s*SPECIALISTS\s*\}\}")
DOMAINS_PATTERN = re.compile(r"\{\{\s*DOMAINS\s*\}\}")
AGENT_TAG = re.compile(r"(?<![\w:-])[a-z0-9-]+:[a-z0-9-]+(?![\w:-])")
USES_PATTERN = re.compile(r"\{\{\s*USES\s*\}\}")
USES_HEADER = "# Uses:"
USES_ENTRY = re.compile(r"[a-z0-9-]+(?::[a-z0-9-]+)?")
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


def find_uses_cycle(start: str, root: Path) -> list[str] | None:
    """Loop of local domain entries from lead to lead that returns to `start`, or None. Tag entries end the walk."""

    def walk(current: str, trail: list[str]) -> list[str] | None:
        chief_path = root / "agents" / current / f"{CHIEF_SPEC}.toml"
        if not chief_path.is_file():
            return None
        for entry in read_uses_header(chief_path.read_text(encoding="utf-8")) or []:
            if ":" in entry or not USES_ENTRY.fullmatch(entry):
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


def check_uses_entries(entries: list[str], domain: str, root: Path) -> list[str]:
    # A generated tap may depend on domains of another tap: an entry whose domain
    # is not a local directory is accepted without further checks.
    problems = []
    seen = set()
    for entry in entries:
        if not entry:
            problems.append("USES_INVALID: empty entry in '# Uses:' (stray comma or no value)")
            continue
        if not USES_ENTRY.fullmatch(entry):
            problems.append(f"USES_INVALID: '{entry}' is malformed — write a bare domain ('content') or a full tag ('seo:audit')")
            continue
        if entry in seen:
            problems.append(f"USES_INVALID: '{entry}' is listed more than once")
            continue
        seen.add(entry)
        entry_domain, _, entry_spec = entry.partition(":")
        if entry_domain == domain:
            problems.append(f"USES_INVALID: '{entry}' is in the agent's own domain — use {{{{SPECIALISTS}}}} for it")
        elif entry_spec == CHIEF_SPEC:
            problems.append(f"USES_INVALID: '{entry}' — write the bare domain '{entry_domain}' instead of '{entry_domain}:{CHIEF_SPEC}'")
        elif not (root / "agents" / entry_domain).is_dir():
            continue
        elif not entry_spec and not (root / "agents" / entry_domain / f"{CHIEF_SPEC}.toml").is_file():
            problems.append(f"USES_UNKNOWN: domain '{entry}' has no agents/{entry_domain}/{CHIEF_SPEC}.toml")
        elif entry_spec and not (root / "agents" / entry_domain / f"{entry_spec}.toml").is_file():
            problems.append(f"USES_UNKNOWN: agent '{entry}' has no agents/{entry_domain}/{entry_spec}.toml")
    if not problems:
        cycle = find_uses_cycle(domain, root)
        if cycle:
            problems.append(f"USES_CYCLE: {CYCLE_SEPARATOR.join(cycle)} — leads that use each other would delegate in a loop")
    return problems

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
    for line in raw.splitlines():
        if not line.startswith("#"):
            break
        if line.startswith("# Default:"):
            errors.append(
                f"{path}: DEFAULT_HEADER_REMOVED: '# Default:' is no longer used; "
                f"a domain's orchestrator is the agent named '{CHIEF_SPEC}'"
            )
            break

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

    domain = path.parent.name
    tag = f"{domain}:{path.stem}"
    # The unrendered starter is generated as chief.toml, so --template treats its token as chief.
    is_chief = path.stem in (CHIEF_SPEC, STARTER_SPEC_TOKEN)
    is_orchestrator = is_chief or tag == GLOBAL_AGENT_TAG
    has_specialists = bool(SPECIALISTS_PATTERN.search(system))
    has_siblings = any(sibling != path for sibling in path.parent.glob("*.toml"))
    if is_orchestrator and has_siblings and not has_specialists:
        errors.append(f"{path}: SPECIALISTS_MISSING: orchestrator must put '{{{{SPECIALISTS}}}}' in system to delegate to the other agents of its domain")
    if has_specialists and not is_orchestrator:
        errors.append(f"{path}: SPECIALISTS_MISPLACED: '{{{{SPECIALISTS}}}}' in system is only for a domain's orchestrator ('{CHIEF_SPEC}')")
    if DOMAINS_PATTERN.search(system) and tag != GLOBAL_AGENT_TAG:
        errors.append(f"{path}: DOMAINS_MISPLACED: '{{{{DOMAINS}}}}' in system is only allowed for {GLOBAL_AGENT_TAG}")
    uses_entries = read_uses_header(raw)
    has_uses_placeholder = bool(USES_PATTERN.search(system))
    if not is_chief:
        if uses_entries is not None or has_uses_placeholder:
            errors.append(f"{path}: USES_MISPLACED: '# Uses:' header and '{{{{USES}}}}' in system are only for a domain's orchestrator ('{CHIEF_SPEC}')")
    else:
        if uses_entries is not None and not has_uses_placeholder:
            errors.append(f"{path}: USES_MISSING: '# Uses:' header needs '{{{{USES}}}}' in system so the orchestrator can name what it may call")
        elif uses_entries is None and has_uses_placeholder:
            errors.append(f"{path}: USES_MISSING: '{{{{USES}}}}' in system needs a '# Uses: <entry>[, <entry>…]' header comment")
        if uses_entries is not None:
            errors.extend(f"{path}: {problem}" for problem in check_uses_entries(uses_entries, domain, root))
    if is_chief and (has_siblings or uses_entries is not None) and not any(
        isinstance(capability, str) and capability.rpartition("/")[2] == ORCHESTRATION_CAPABILITY
        for capability in capabilities
    ):
        reason = "leads a domain with other agents" if has_siblings else "declares '# Uses:'"
        errors.append(f"{path}: CHIEF_NO_ORCHESTRATION: '{CHIEF_SPEC}' {reason} and must declare the '{ORCHESTRATION_CAPABILITY}' capability")
    if is_orchestrator:
        local_tags = {f"{other.parent.name}:{other.stem}" for other in (root / "agents").glob("*/*.toml")}
        prompt_text = f"{system}\n{role.get('welcome', '')}"
        foreign = sorted(
            found for found in set(AGENT_TAG.findall(prompt_text)) if found in local_tags and found.split(":")[0] != domain
        )
        if foreign:
            errors.append(f"{path}: FOREIGN_DOMAIN_TAG: orchestrator names agents from other domains: {', '.join(foreign)}")


def validate_domain_chief(domain_dir: Path, errors: list[str]) -> None:
    # Inside a user tap every domain, including one extending a base-tap domain,
    # needs its own chief once it has two or more agents.
    agents = sorted(path.name for path in domain_dir.glob("*.toml"))
    if len(agents) >= 2 and domain_dir.name != GLOBAL_AGENT_TAG.split(":")[0] and not {f"{CHIEF_SPEC}.toml", f"{STARTER_SPEC_TOKEN}.toml"} & set(agents):
        errors.append(
            f"{domain_dir}: DOMAIN_NO_CHIEF: a domain with {len(agents)} agents needs {CHIEF_SPEC}.toml "
            f"as its orchestrator, found: {', '.join(agents)}"
        )


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
    agents_dir = root / "agents"
    for domain_dir in sorted(agents_dir.iterdir() if agents_dir.is_dir() else []):
        if domain_dir.is_dir():
            validate_domain_chief(domain_dir, errors)
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
