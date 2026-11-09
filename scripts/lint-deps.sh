#!/usr/bin/env bash
# Lint all dep scripts in deps/**/*.sh
# Checks:
#   1. Header: # dep: <org>/<tool> matches file path
#   2. Header: # type: mcp|dep
#   3. Header: # description: <Name> - <what it does> (120–155 chars; octomind.run
#      shows the name as the page title and the whole line as the search snippet)
#   4. Header: # check: <command>
#   5. Header: # https://... URL
#   6. Companion .md file exists alongside .sh
#   7. Companion H1 matches <org>/<tool>
#   8. Companion required sections (MCP: MCP Server, Authentication, Available Tools, Configuration Example)
#   9. Companion required sections (dep: Key Commands, Common Usage)
#
# Usage:
#   scripts/lint-deps.sh                  # lint all dep scripts
#   scripts/lint-deps.sh <file> [<file>]  # lint specific files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

# Collect files to lint
if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  while IFS= read -r found; do
    FILES+=("$found")
  done < <(find "$REPO_ROOT/deps" -name "*.sh" -not -path "*/lib/*" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No dep scripts found."
  exit 0
fi

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  # Must be under deps/<org>/<tool>.sh (exactly 2 path components under deps/)
  local inner="${file#"$REPO_ROOT/deps/"}"
  local depth
  depth=$(echo "$inner" | tr -cd '/' | wc -c)
  if [[ $depth -ne 1 ]]; then
    echo "  ✗ path: must be deps/<org>/<tool>.sh (got: $rel)"
    ok=0
  fi

  # Header + companion checks via Python
  local py_err
  if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-deps.py" "$file" "$REPO_ROOT" 2>&1); then
    while IFS= read -r line; do
      echo "  ✗ $line"
    done < <(printf '%s\n' "$py_err")
    ok=0
  fi

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $rel"
  else
    echo "    file: $rel"
    return 1
  fi
}

echo "Linting ${#FILES[@]} dep script(s)..."
echo ""

for file in "${FILES[@]}"; do
  [[ $file == /* ]] || file="$REPO_ROOT/$file"

  if ! lint_file "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS dep script(s) failed linting."
  exit 1
else
  echo "✅ All dep scripts passed."
fi
