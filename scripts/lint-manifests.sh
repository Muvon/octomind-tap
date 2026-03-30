#!/usr/bin/env bash
# Lint all agent manifests in agents/**/*.toml
# Checks:
#   1. Valid TOML
#   2. Exactly one [[roles]] entry
#   3. `name` field is NOT set (injected at runtime from the tag)
#   4. Required fields present: system, welcome, temperature, top_p, top_k
#   5. File path matches agents/<domain>/<spec>.toml convention
#   6. Capability-driven agents must NOT have [deps], [roles.mcp], or [[mcp.servers]]
#   7. Every capability reference must have a matching capabilities/<name>/default.toml
#   8. Comment metadata: # Title: (5–60 chars) and # Description: (20–160 chars) required
#
# Usage:
#   scripts/lint-manifests.sh                  # lint all manifests
#   scripts/lint-manifests.sh <file> [<file>]  # lint specific files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

# Collect files to lint
if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  mapfile -t FILES < <(find "$REPO_ROOT/agents" -name "*.toml" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No manifest files found."
  exit 0
fi

# Python TOML parser — tomllib (3.11+) or tomli fallback
PYTHON_TOML_CHECK=$(
  cat <<'PYEOF'
import sys, pathlib, re, os

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

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
    if len(desc_val) < 20:
        errors.append(f"DESC_SHORT: description must be at least 20 characters ({len(desc_val)} chars)")
    elif len(desc_val) > 160:
        errors.append(f"DESC_LONG: description must be at most 160 characters ({len(desc_val)} chars)")

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
PYEOF
)

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  # Must be under agents/<domain>/<spec>.toml (exactly 3 path components)
  local inner="${file#"$REPO_ROOT/agents/"}"
  local depth
  depth=$(echo "$inner" | tr -cd '/' | wc -c)
  if [[ $depth -ne 1 ]]; then
    echo "  ✗ path: must be agents/<domain>/<spec>.toml (got extra nesting: $rel)"
    ok=0
  fi

  # TOML validity + field checks via Python
  local py_err
  if ! py_err=$(python3 -c "$PYTHON_TOML_CHECK" "$file" "$REPO_ROOT" 2>&1); then
    echo "  ✗ $py_err"
    ok=0
  fi

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $rel"
  else
    echo "    file: $rel"
    return 1
  fi
}

echo "Linting ${#FILES[@]} manifest(s)..."
echo ""

for file in "${FILES[@]}"; do
  # Normalise to absolute path
  [[ $file == /* ]] || file="$REPO_ROOT/$file"

  if ! lint_file "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS manifest(s) failed linting."
  exit 1
else
  echo "✅ All manifests passed."
fi
