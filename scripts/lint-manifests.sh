#!/usr/bin/env bash
# Lint all agent manifests in agents/*.toml
# Checks:
#   1. Valid TOML
#   2. Exactly one [[roles]] entry
#   3. `name` field is NOT set (injected at runtime from the tag)
#   4. Required fields present: system, welcome; deprecated sampling fields absent
#   5. Layout: agents/<name>.toml with no subdirectories and no symlinks; the
#      `# Agent: <name>` header equals the file name
#   6. Capability-driven agents must NOT have [deps], [roles.mcp], or [[mcp.servers]]
#   7. Every capability reference must have a matching capabilities/<name>/default.toml
#   8. Comment metadata: # Title: (5–60 chars) and # Description: (120–155 chars) required
#      {{SPECIALISTS}} / {{USES}} placeholders are rejected
#      `# Uses:` lists `*` or existing agent names, needs the `orchestration` capability, no loops
#   9. Prompts must not cite tap-relative paths (skills/…, capabilities/…, deps/…) — octomind agent exempt
#  10. Every `name` skill mentioned in prompts must exist at skills/<name>/SKILL.md
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
  while IFS= read -r found; do
    FILES+=("$found")
  done < <(find "$REPO_ROOT/agents" -name "*.toml" -type f | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No manifest files found."
  exit 0
fi

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  # Must be a regular file directly under agents/: agents/<name>.toml
  local inner="${file#"$REPO_ROOT/agents/"}"
  if [[ -L $file ]]; then
    echo "  ✗ AGENT_SYMLINK: $rel is a symlink; agents are regular files"
    ok=0
  fi
  if [[ $inner == */* || $inner != *.toml ]]; then
    echo "  ✗ AGENT_PATH: must be agents/<name>.toml (got $rel)"
    ok=0
  fi

  # TOML validity + field checks via Python
  local py_err
  if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-manifests.py" "$file" "$REPO_ROOT" 2>&1); then
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

# Nothing but agent files lives under agents/: no subdirectories, no symlinks.
if [[ $# -eq 0 ]]; then
  while IFS= read -r entry; do
    echo "  ✗ AGENT_SUBDIR: ${entry#"$REPO_ROOT/"} is a directory; agents live directly in agents/<name>.toml"
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 1 -type d | sort)
  while IFS= read -r entry; do
    echo "  ✗ AGENT_SYMLINK: ${entry#"$REPO_ROOT/"} is a symlink; agents are regular files"
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 1 -type l | sort)
fi

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
