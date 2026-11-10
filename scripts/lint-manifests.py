import sys, pathlib, re, os

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

CHIEF_SPEC = "chief"
GLOBAL_AGENT_TAG = "assistant:concierge"
ORCHESTRATION_CAPABILITY = "orchestration"
SPECIALISTS_PATTERN = r'\{\{\s*SPECIALISTS\s*\}\}'
DOMAINS_PATTERN = r'\{\{\s*DOMAINS\s*\}\}'
TAG_PATTERN = r'(?<![\w:-])[a-z0-9-]+:[a-z0-9-]+(?![\w:-])'


if sys.argv[1] == "--domain":
    domain = sys.argv[2]
    domain_dir = pathlib.Path(sys.argv[3]) / "agents" / domain
    agent_count = len(list(domain_dir.glob("*.toml")))
    if agent_count >= 2 and domain != GLOBAL_AGENT_TAG.split(":")[0] and not (domain_dir / f"{CHIEF_SPEC}.toml").is_file():
        print(f"DOMAIN_NO_CHIEF: domain '{domain}' has {agent_count} agents but no {CHIEF_SPEC}.toml — add agents/{domain}/{CHIEF_SPEC}.toml as the domain's orchestrator", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

path = pathlib.Path(sys.argv[1])
repo_root = pathlib.Path(sys.argv[2])

raw_text = path.read_text()

try:
    data = tomllib.loads(raw_text)
except Exception as e:
    print(f"INVALID_TOML: {e}", file=sys.stderr)
    sys.exit(1)

errors = []

# ── Comment metadata: # Title: and # Description: ────────────────────────────
title_match = re.search(r'^# Title:\s*(.+)$', raw_text, re.MULTILINE)
desc_match = re.search(r'^# Description:\s*(.+)$', raw_text, re.MULTILINE)

if not title_match:
    errors.append("MISSING_TITLE: '# Title: ...' comment is required")
else:
    title_val = title_match.group(1).strip()
    if len(title_val) < 5:
        errors.append(f"TITLE_SHORT: title must be at least 5 characters ({len(title_val)} chars)")
    elif len(title_val) > 60:
        errors.append(f"TITLE_LONG: title must be at most 60 characters ({len(title_val)} chars)")

if not desc_match:
    errors.append("MISSING_DESCRIPTION: '# Description: ...' comment is required")
else:
    desc_val = desc_match.group(1).strip()
    # Also the agent page's search snippet on octomind.run: 120–155 chars.
    if len(desc_val) < 120:
        errors.append(f"DESC_SHORT: description must be at least 120 characters ({len(desc_val)} chars)")
    elif len(desc_val) > 155:
        errors.append(f"DESC_LONG: description must be at most 155 characters ({len(desc_val)} chars)")

roles = data.get("roles", [])

# Exactly one [[roles]] entry
if len(roles) != 1:
    errors.append(f"ROLES_COUNT: expected 1 [[roles]] entry, got {len(roles)}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

role = roles[0]

# name must NOT be set
if "name" in role:
    errors.append("NAME_SET: 'name' must not be set in manifests — it is injected from the tag at runtime")

# Required fields
required = ["system", "welcome", "temperature", "top_p", "top_k"]
missing = [f for f in required if f not in role]
if missing:
    errors.append(f"MISSING_FIELDS: {', '.join(missing)}")

# ── System prompt content guardrails (hard rules) ────────────────────────────
system_content = role.get("system", "")
if system_content:
    # Strip code (fenced ```, inline `code`, AND 4-space indented blocks) before checking
    # — markdown inside code is intentional and shouldn't trigger guardrails
    no_fences = re.sub(r'```.*?```', '', system_content, flags=re.DOTALL)
    no_fences = re.sub(r'`[^`\n]+`', '', no_fences)
    no_fences = re.sub(r'^    .*$', '', no_fences, flags=re.MULTILINE)

    # No **bold** outside code fences — XML tags are the structure
    bold_matches = re.findall(r'\*\*[^*\n]+?\*\*', no_fences)
    if bold_matches:
        sample = bold_matches[0][:60]
        errors.append(f"SYSTEM_HAS_BOLD: {len(bold_matches)} **bold** pattern(s) in system prompt — strip them (XML tags provide structure). First match: {sample}")

    # No headers (## or ###) outside code fences — XML tags are the section anchors
    header_matches = re.findall(r'^#{1,6}\s+\S.*$', no_fences, re.MULTILINE)
    if header_matches:
        sample = header_matches[0][:60]
        # ### subsections inside an XML block are allowed when there are 2+ in same block — skip ### check
        # but ## and # are never valid in an XML-block agent prompt
        h2_h1 = [h for h in header_matches if re.match(r'^#{1,2}\s', h)]
        if h2_h1:
            sample = h2_h1[0][:60]
            errors.append(f"SYSTEM_HAS_HEADER: ## or # markdown header in system prompt — XML tags replace these. First match: {sample}")

    # No dynamic placeholders ({{CWD}}, {{DATE}}) anywhere in system — they BREAK PROMPT CACHING
    # System prompt must be stable run-to-run. Dynamic context goes in `welcome` only.
    cwd_match = re.search(r'\{\{\s*CWD\s*\}\}', no_fences)
    if cwd_match:
        errors.append("SYSTEM_HAS_CWD: '{{CWD}}' in system prompt — breaks prompt caching (system must be stable run-to-run). Move to `welcome` field.")
    date_match = re.search(r'\{\{\s*DATE\s*\}\}', no_fences)
    if date_match:
        errors.append("SYSTEM_HAS_DATE: '{{DATE}}' in system prompt — breaks prompt caching (system must be stable run-to-run). Move to `welcome` field.")
    system_match = re.search(r'\{\{\s*SYSTEM\s*\}\}', no_fences)
    if system_match:
        errors.append("SYSTEM_HAS_SYSTEM: '{{SYSTEM}}' in system prompt — expands date/shell/OS/CWD, breaks prompt caching. Move to `welcome` field.")

    # System prompt length cap — production sweet spot 200-1000 words; >1500 risks context rot
    sys_word_count = len(system_content.split())
    SOFT_LIMIT = 1500
    HARD_LIMIT = 3000
    if sys_word_count > HARD_LIMIT:
        errors.append(f"SYSTEM_TOO_LONG: system prompt is {sys_word_count} words (hard limit {HARD_LIMIT}). Context rot at this length degrades rule recall. Move documentation to skills or reference files.")
    elif sys_word_count > SOFT_LIMIT:
        # Soft warning — surfaces but doesn't fail
        print(f"SYSTEM_LENGTH_WARN ({path}): system is {sys_word_count} words (soft target {SOFT_LIMIT}). Consider extracting reference content into skills.", file=sys.stderr)

# ── Cross-reference integrity: tap paths and skill names cited in prompts ────
# Agents run in the user's project directory, not the tap checkout, so a
# tap-relative path (skills/x/…, capabilities/x/…, deps/x/…) can never be read
# at runtime. Only the octomind domain works on the tap repo itself.
prompt_text = f"{system_content}\n{role.get('welcome', '')}"
domain = path.parent.name
if domain != "octomind":
    tap_paths = re.findall(r'(?<![\w/.~-])(?:skills|capabilities|deps)/[^\s`\'")]+/[^\s`\'")]+', prompt_text)
    if tap_paths:
        errors.append(f"TAP_PATH_REF: '{tap_paths[0]}' is a tap-relative path — unreadable from the project workdir at runtime. Reference the skill by name instead.")

# Every `name` skill mention must resolve — a phantom name silently fails to load.
# Placeholders such as `social-<platform>` are skipped.
for m in re.finditer(r'((?:`[a-z0-9<>-]+`(?:,\s*|\s+(?:and|or)\s+|\s+))+)skills?\b', prompt_text):
    for skill_name in re.findall(r'`([^`]+)`', m.group(1)):
        if '<' in skill_name:
            continue
        if not (repo_root / "skills" / skill_name / "SKILL.md").is_file():
            errors.append(f"SKILL_REF_UNKNOWN: '{skill_name}' skill has no skills/{skill_name}/SKILL.md")

# ── Domain orchestrator (the agent named chief) and delegation placeholders ──
agent_tag = f"{domain}:{path.stem}"
sibling_count = len([p for p in path.parent.glob("*.toml") if p != path])
is_orchestrator = path.stem == CHIEF_SPEC or agent_tag == GLOBAL_AGENT_TAG

for line in raw_text.splitlines():
    if not line.startswith("#"):
        break
    if line.startswith("# Default:"):
        errors.append(f"DEFAULT_HEADER_REMOVED: '# Default:' is no longer used — a domain's orchestrator is the agent named '{CHIEF_SPEC}' (agents/<domain>/{CHIEF_SPEC}.toml)")
        break

has_specialists = bool(re.search(SPECIALISTS_PATTERN, system_content))
if is_orchestrator and sibling_count > 0 and not has_specialists:
    errors.append("SPECIALISTS_MISSING: orchestrator must put '{{SPECIALISTS}}' in system so it can delegate to the other agents in its domain")
elif has_specialists and not is_orchestrator:
    errors.append(f"SPECIALISTS_MISPLACED: '{{{{SPECIALISTS}}}}' is only for a domain's orchestrator ('{CHIEF_SPEC}')")

if re.search(DOMAINS_PATTERN, system_content) and agent_tag != GLOBAL_AGENT_TAG:
    errors.append(f"DOMAINS_MISPLACED: '{{{{DOMAINS}}}}' in system is only allowed for {GLOBAL_AGENT_TAG}")

if path.stem == CHIEF_SPEC and sibling_count > 0:
    chief_caps = [c.rpartition("/")[2] for c in data.get("capabilities", [])]
    if ORCHESTRATION_CAPABILITY not in chief_caps:
        errors.append(f"CHIEF_NO_ORCHESTRATION: '{CHIEF_SPEC}' leads a domain with other agents and must declare the '{ORCHESTRATION_CAPABILITY}' capability")

# An orchestrator hands work off inside its own domain only; cross-domain routing is the concierge's job.
if is_orchestrator:
    all_tags = {f"{p.parent.name}:{p.stem}" for p in (repo_root / "agents").glob("*/*.toml")}
    foreign_tags = sorted({t for t in re.findall(TAG_PATTERN, prompt_text) if t in all_tags and t.split(":")[0] != domain})
    if foreign_tags:
        errors.append(f"FOREIGN_DOMAIN_TAG: orchestrator names agents from other domains: {', '.join(foreign_tags)}")

# Check for capabilities declaration
has_capabilities = bool(re.search(r'^capabilities\s*=\s*\[', raw_text, re.MULTILINE))

if has_capabilities:
    caps = data.get("capabilities", [])

    # Capability-driven agents must NOT have [deps]
    if "deps" in data:
        errors.append("AGENT_HAS_DEPS: capability-driven agents must NOT have [deps] — deps belong in capability files only")

    # Capability-driven agents must NOT have [roles.mcp]
    if "mcp" in role:
        errors.append("AGENT_HAS_ROLES_MCP: capability-driven agents must NOT have [roles.mcp] — injected from capabilities at runtime")

    # Capability-driven agents must NOT have [[mcp.servers]]
    if "mcp" in data and "servers" in data.get("mcp", {}):
        errors.append("AGENT_HAS_MCP_SERVERS: capability-driven agents must NOT have [[mcp.servers]] — MCP servers belong in capability files")

    # Each capability must have a directory with default.toml
    cap_root = repo_root / "capabilities"
    for cap in caps:
        cap_dir = cap_root / cap
        cap_default = cap_dir / "default.toml"
        if not cap_dir.is_dir():
            errors.append(f"CAP_MISSING_DIR: capability '{cap}' has no directory at capabilities/{cap}/")
        elif not cap_default.exists():
            errors.append(f"CAP_MISSING_DEFAULT: capability '{cap}' has no default.toml at capabilities/{cap}/default.toml")

else:
    # Legacy / explicit MCP: external server_refs must be defined under [[mcp.servers]]
    BUILTIN_SERVERS = {"core", "octofs", "agent", "octocode"}
    mcp_section = data.get("mcp", {})
    defined_servers = {s["name"] for s in mcp_section.get("servers", []) if "name" in s}
    server_refs = role.get("mcp", {}).get("server_refs", [])
    for ref in server_refs:
        if ref not in BUILTIN_SERVERS and ref not in defined_servers:
            errors.append(f"MCP_UNDEFINED: server_ref '{ref}' has no [[mcp.servers]] entry")
    for name in defined_servers:
        if name in BUILTIN_SERVERS:
            errors.append(f"MCP_BUILTIN_REDEFINED: [[mcp.servers]] name='{name}' is a built-in — remove the block")

# Optional [deps] validation (for legacy agents that still have it)
deps = data.get("deps", {})
if deps:
    require = deps.get("require", [])
    if not isinstance(require, list):
        errors.append("DEPS_INVALID: [deps] require must be an array")
    else:
        pattern = re.compile(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$')
        for entry in require:
            if not isinstance(entry, str):
                errors.append(f"DEPS_INVALID: require entries must be strings, got {type(entry).__name__}")
            elif not pattern.match(entry):
                errors.append(f"DEPS_INVALID: '{entry}' must match <org>/<tool>")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

sys.exit(0)
