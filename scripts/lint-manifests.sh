#!/usr/bin/env bash
# Lint all agent manifests in agents/<name>/config.toml
# Checks:
#   1. Valid TOML
#   2. Exactly one [[roles]] entry
#   3. `name` field is NOT set (injected at runtime from the tag)
#   4. Required fields present: system, welcome; deprecated sampling fields absent
#   5. Layout: agents/<name>/config.toml; nothing else directly under agents/, only
#      config.toml and skills/ inside an agent directory, no symlinks; the
#      `# Agent: <name>` header equals the directory name
#   6. Capability-driven agents must NOT have [deps], [roles.mcp], or [[mcp.servers]]
#   7. Every capability reference must have a matching capabilities/<name>/default.toml
#   8. Comment metadata: # Title: (5–60 chars) and # Description: (120–155 chars) required
#      {{SPECIALISTS}} / {{USES}} placeholders are rejected
#      `# Uses:` lists `*` or existing agent names, needs the `orchestration` capability, no loops
#   9. Prompts must not cite tap-relative paths (skills/…, capabilities/…, deps/…) — octomind agent exempt
#  10. Every `name` skill mentioned in prompts must exist at skills/<name>/SKILL.md or agents/<agent>/skills/<name>/SKILL.md
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
  done < <(python3 "$REPO_ROOT/scripts/tap_paths.py" agents "$REPO_ROOT")
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No manifest files found."
  exit 0
fi

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  # Must be a regular file: agents/<name>/config.toml
  if [[ -L $file ]]; then
    echo "  ✗ AGENT_SYMLINK: $rel is a symlink; agents are regular files"
    ok=0
  fi
  if [[ ! $rel =~ ^agents/[^/]+/config\.toml$ ]]; then
    echo "  ✗ AGENT_PATH: must be agents/<name>/config.toml (got $rel)"
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

# Only agent directories live under agents/, and each holds config.toml and skills/.
if [[ $# -eq 0 ]]; then
  while IFS= read -r entry; do
    if [[ $entry == *.toml ]]; then
      echo "  ✗ AGENT_FLAT_FILE: ${entry#"$REPO_ROOT/"} is a flat manifest; move it to agents/$(basename "$entry" .toml)/config.toml"
    else
      echo "  ✗ AGENT_STRAY_FILE: ${entry#"$REPO_ROOT/"} is a file directly under agents/; agents are directories agents/<name>/"
    fi
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 1 -maxdepth 1 -type f | sort)
  for agent_dir in "$REPO_ROOT"/agents/*/; do
    agent_dir="${agent_dir%/}"
    if [[ ! -f $agent_dir/config.toml ]]; then
      echo "  ✗ AGENT_NO_MANIFEST: ${agent_dir#"$REPO_ROOT/"} has no config.toml"
      ERRORS=$((ERRORS + 1))
    fi
  done
  while IFS= read -r entry; do
    echo "  ✗ AGENT_DIR_ENTRY: ${entry#"$REPO_ROOT/"} is not allowed; an agent directory holds only config.toml and skills/"
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 2 -maxdepth 2 ! -name config.toml ! -name skills | sort)
  while IFS= read -r entry; do
    echo "  ✗ AGENT_SYMLINK: ${entry#"$REPO_ROOT/"} is a symlink; agents are regular files"
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 1 -type l | sort)
  while IFS= read -r entry; do
    echo "  ✗ AGENT_DIR_ENTRY: ${entry#"$REPO_ROOT/"} must be a directory"
    ERRORS=$((ERRORS + 1))
  done < <(find "$REPO_ROOT/agents" -mindepth 2 -maxdepth 2 -name skills ! -type d ! -type l | sort)
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
