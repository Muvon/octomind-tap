#!/usr/bin/env bash
# Lint all capability definitions in capabilities/**/*.toml
# Checks:
#   1. Valid TOML
#   2. Every server_refs entry has a matching [[mcp.servers]] name declaration
#   3. Every [deps] require entry matches <org>/<tool> format
#   4. Every [deps] require entry has a corresponding deps/<org>/<tool>.sh script
#   5. default.toml exists and is a symlink (except for built-in: core, agent)
#   6. default.toml symlink target exists
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

try:
    data = tomllib.loads(path.read_text())
except Exception as e:
    print(f"INVALID_TOML: {e}", file=sys.stderr)
    sys.exit(1)

errors = []

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

  # Lint all provider .toml files (not default.toml symlink)
  for toml in "$dir"/*.toml; do
    [[ -L $toml ]] && continue # skip symlinks (default.toml)
    local basename
    basename="$(basename "$toml")"

    local py_err
    if ! py_err=$(python3 -c "$PYTHON_CAP_CHECK" "$toml" "$DEPS_ROOT" 2>&1); then
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
