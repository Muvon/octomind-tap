#!/usr/bin/env bash
# Lint all capability definitions in capabilities/**/*.toml
#
# Two file kinds, two rule sets:
#
#   capabilities/<cap>/config.toml        — capability-level metadata.
#     Required: `triggers = [...]` (non-empty array of strings).
#     No Title/Description required (file holds only routing metadata).
#
#   capabilities/<cap>/<provider>.toml    — provider-specific MCP wiring.
#     Required: # Title and # Description comment headers, valid mcp wiring,
#     server_refs ↔ [[mcp.servers]] consistency, dep scripts present.
#
# Plus structural rules: default.toml must exist and be a symlink (except
# for built-in caps: core, agent), and the symlink target must exist.
#
# Usage:
#   scripts/lint-capabilities.sh                  # lint all capabilities
#   scripts/lint-capabilities.sh <dir> [<dir>]    # lint specific capability dirs

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAP_ROOT="$REPO_ROOT/capabilities"
DEPS_ROOT="$REPO_ROOT/deps"
ERRORS=0
BUILTIN_CAPS=("core" "agent")

# Collect capability dirs to lint
if [[ $# -gt 0 ]]; then
  DIRS=("$@")
else
  mapfile -t DIRS < <(find "$CAP_ROOT" -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [[ ${#DIRS[@]} -eq 0 ]]; then
  echo "No capability directories found."
  exit 0
fi

PYTHON_CAP_CHECK=$(
  cat <<'PYEOF'
import sys, pathlib, re

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

path = pathlib.Path(sys.argv[1])
deps_root = pathlib.Path(sys.argv[2])
# Third arg is the file kind: "config" for capability-level metadata
# (capabilities/<cap>/config.toml), "provider" for provider files
# (capabilities/<cap>/<provider>.toml).
file_kind = sys.argv[3] if len(sys.argv) > 3 else "provider"

raw_text = path.read_text()

try:
    data = tomllib.loads(raw_text)
except Exception as e:
    print(f"INVALID_TOML: {e}", file=sys.stderr)
    sys.exit(1)

errors = []

if file_kind == "config":
    # Capability metadata: only require non-empty triggers array. No
    # Title/Description (this file is routing data, not a provider doc).
    triggers = data.get("triggers")
    if triggers is None:
        errors.append("MISSING_TRIGGERS: 'triggers = [...]' field is required in config.toml")
    elif not isinstance(triggers, list):
        errors.append("TRIGGERS_INVALID: 'triggers' must be an array of strings")
    else:
        non_empty = [t for t in triggers if isinstance(t, str) and t.strip()]
        if not non_empty:
            errors.append("TRIGGERS_EMPTY: 'triggers' array must contain at least one non-empty string")
        for t in triggers:
            if not isinstance(t, str):
                errors.append(f"TRIGGERS_INVALID: trigger entries must be strings, got {type(t).__name__}")
        if len(non_empty) < 3:
            errors.append(f"TRIGGERS_FEW: capabilities should have at least 3 trigger phrases for reliable embedding routing ({len(non_empty)} present)")
else:
    # Provider file: require Title/Description comment headers and full
    # MCP wiring validation.
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

    # Validate [deps] require
    deps = data.get("deps", {})
    require = deps.get("require", [])
    if require:
        if not isinstance(require, list):
            errors.append("DEPS_INVALID: [deps] require must be an array")
        else:
            pattern = re.compile(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$')
            for entry in require:
                if not isinstance(entry, str):
                    errors.append(f"DEPS_INVALID: require entries must be strings, got {type(entry).__name__}")
                elif not pattern.match(entry):
                    errors.append(f"DEPS_INVALID: '{entry}' must match <org>/<tool>")
                else:
                    # Check dep script exists
                    org, tool = entry.split("/", 1)
                    dep_script = deps_root / org / f"{tool}.sh"
                    if not dep_script.exists():
                        errors.append(f"DEPS_MISSING_SCRIPT: dep '{entry}' has no script at deps/{org}/{tool}.sh")

    # Validate server_refs have matching [[mcp.servers]] declarations
    roles_mcp = data.get("roles", {}).get("mcp", {})
    server_refs = roles_mcp.get("server_refs", [])
    mcp_section = data.get("mcp", {})
    defined_servers = {s["name"] for s in mcp_section.get("servers", []) if "name" in s}

    for ref in server_refs:
        if ref not in defined_servers:
            errors.append(f"MCP_MISSING_SERVER: server_ref '{ref}' has no matching [[mcp.servers]] name='{ref}' declaration")

    # Validate [[mcp.servers]] entries have required fields
    for server in mcp_section.get("servers", []):
        name = server.get("name", "<unnamed>")
        if "name" not in server:
            errors.append(f"MCP_NO_NAME: [[mcp.servers]] entry missing 'name' field")
        if "type" not in server:
            errors.append(f"MCP_NO_TYPE: [[mcp.servers]] name='{name}' missing 'type' field")
        stype = server.get("type", "")
        if stype == "stdio" and "command" not in server:
            errors.append(f"MCP_NO_COMMAND: [[mcp.servers]] name='{name}' type='stdio' missing 'command' field")
        if stype == "http" and "url" not in server:
            errors.append(f"MCP_NO_URL: [[mcp.servers]] name='{name}' type='http' missing 'url' field")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

sys.exit(0)
PYEOF
)

is_builtin() {
  local cap="$1"
  for b in "${BUILTIN_CAPS[@]}"; do
    [[ $b == "$cap" ]] && return 0
  done
  return 1
}

lint_capability() {
  local dir="$1"
  local cap_name
  cap_name="$(basename "$dir")"
  local ok=1

  # Check default.toml exists
  local default_file="$dir/default.toml"
  if [[ ! -e $default_file ]]; then
    echo "  ✗ $cap_name: missing default.toml"
    return 1
  fi

  # For non-built-in: default.toml must be a symlink
  if ! is_builtin "$cap_name"; then
    if [[ ! -L $default_file ]]; then
      echo "  ✗ $cap_name: default.toml must be a symlink (not a plain file)"
      ok=0
    else
      # Symlink target must exist
      local target
      target="$(readlink "$default_file")"
      if [[ ! -f "$dir/$target" ]]; then
        echo "  ✗ $cap_name: default.toml -> $target (target does not exist)"
        ok=0
      fi
    fi
  fi

  # Lint config.toml (capability-level metadata) and provider TOMLs with
  # different rule sets. Skip default.toml when it's a symlink (linted
  # already as the real provider file via its target).
  for toml in "$dir"/*.toml; do
    [[ -L $toml ]] && continue # skip symlinks (default.toml)
    local basename
    basename="$(basename "$toml")"

    local file_kind="provider"
    if [[ $basename == "config.toml" ]]; then
      file_kind="config"
    fi

    local py_err
    if ! py_err=$(python3 -c "$PYTHON_CAP_CHECK" "$toml" "$DEPS_ROOT" "$file_kind" 2>&1); then
      echo "  ✗ $cap_name/$basename: $py_err"
      ok=0
    fi
  done

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $cap_name"
  fi
  [[ $ok -eq 1 ]]
}

echo "Linting ${#DIRS[@]} capability(ies)..."
echo ""

for dir in "${DIRS[@]}"; do
  [[ $dir == /* ]] || dir="$CAP_ROOT/$dir"

  if ! lint_capability "$dir"; then
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS capability(ies) failed linting."
  exit 1
else
  echo "✅ All capabilities passed."
fi
