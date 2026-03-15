#!/usr/bin/env bash
# Lint all agent manifests in agents/**/*.toml
# Checks:
#   1. Valid TOML
#   2. Exactly one [[roles]] entry
#   3. `name` field is NOT set (injected at runtime from the tag)
#   4. Required fields present: system, welcome, temperature, top_p, top_k
#   5. File path matches agents/<domain>/<spec>.toml convention
#   6. Every non-built-in server_ref must be defined under [[mcp.servers]]
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
  cat <<'EOF'
import sys, pathlib

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        print("ERROR: need python 3.11+ or 'pip install tomli'", file=sys.stderr)
        sys.exit(2)

path = pathlib.Path(sys.argv[1])
try:
    data = tomllib.loads(path.read_text())
except Exception as e:
    print(f"INVALID_TOML: {e}", file=sys.stderr)
    sys.exit(1)

roles = data.get("roles", [])

# Exactly one [[roles]] entry
if len(roles) != 1:
    print(f"ROLES_COUNT: expected 1 [[roles]] entry, got {len(roles)}", file=sys.stderr)
    sys.exit(1)

role = roles[0]

# name must NOT be set
if "name" in role:
    print(f"NAME_SET: 'name' must not be set in manifests — it is injected from the tag at runtime", file=sys.stderr)
    sys.exit(1)

# Required fields
required = ["system", "welcome", "temperature", "top_p", "top_k"]
missing = [f for f in required if f not in role]
if missing:
    print(f"MISSING_FIELDS: {', '.join(missing)}", file=sys.stderr)
    sys.exit(1)

# Optional [deps] section validation
import re
deps = data.get("deps", {})
if deps:
    require = deps.get("require", [])
    if not isinstance(require, list):
        print("DEPS_INVALID: [deps] require must be an array", file=sys.stderr)
        sys.exit(1)
    pattern = re.compile(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+$')
    for entry in require:
        if not isinstance(entry, str):
            print(f"DEPS_INVALID: require entries must be strings, got {type(entry).__name__}", file=sys.stderr)
            sys.exit(1)
        if not pattern.match(entry):
            print(f"DEPS_INVALID: '{entry}' must match <org>/<tool> (no .sh extension, no extra slashes)", file=sys.stderr)
            sys.exit(1)

# External server_refs must be defined under [[mcp.servers]]
BUILTIN_SERVERS = {"core", "filesystem", "agent"}
mcp_section = data.get("mcp", {})
defined_servers = {s["name"] for s in mcp_section.get("servers", []) if "name" in s}
server_refs = role.get("mcp", {}).get("server_refs", [])
for ref in server_refs:
    if ref not in BUILTIN_SERVERS and ref not in defined_servers:
        print(f"MCP_UNDEFINED: server_ref '{ref}' is not a built-in server and has no [[mcp.servers]] entry with name='{ref}'", file=sys.stderr)
        sys.exit(1)
sys.exit(0)
EOF
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
  if ! py_err=$(python3 -c "$PYTHON_TOML_CHECK" "$file" 2>&1); then
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
