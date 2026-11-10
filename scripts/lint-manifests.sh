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
#      Orchestrator is the agent named `chief` (agents/<domain>/chief.toml); {{SPECIALISTS}} / {{DOMAINS}} placement
#   9. Prompts must not cite tap-relative paths (skills/…, capabilities/…, deps/…) — octomind domain exempt
#  10. Every `name` skill mentioned in prompts must exist at skills/<name>/SKILL.md
#  11. Optional agents/<domain>/README.md: a "# <domain name>" line, a blank line, then
#      one description paragraph of 120–155 chars (octomind.run shows them on the domain page)
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
  done < <(find "$REPO_ROOT/agents" -name "*.toml" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No manifest files found."
  exit 0
fi

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

DOMAINS_SEEN=""
for file in "${FILES[@]}"; do
  # Normalise to absolute path
  [[ $file == /* ]] || file="$REPO_ROOT/$file"

  inner="${file#"$REPO_ROOT/agents/"}"
  DOMAINS_SEEN+="${inner%%/*}"$'\n'

  if ! lint_file "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

# A domain with two or more agents needs a chief.toml; checked once per domain, not per file.
while IFS= read -r domain; do
  [[ -n $domain ]] || continue
  if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-manifests.py" --domain "$domain" "$REPO_ROOT" 2>&1); then
    echo "  ✗ $py_err"
    ERRORS=$((ERRORS + 1))
  fi
done < <(printf '%s' "$DOMAINS_SEEN" | sort -u)

# Domain READMEs: octomind.run uses the H1 as the domain name and the paragraph as
# its description, so the shape is fixed.
for readme in "$REPO_ROOT"/agents/*/README.md; do
  [[ -e $readme ]] || continue
  rel="${readme#"$REPO_ROOT/"}"
  if ! py_err=$(python3 -c '
import sys, re
m = re.fullmatch(r"# (\S[^\n]*)\n\n([^\n]+)\n", open(sys.argv[1]).read())
if not m:
    sys.exit("README_SHAPE: want \"# <domain name>\", a blank line, then one description line")
n = len(m.group(2))
if not 120 <= n <= 155:
    sys.exit(f"README_DESC: description must be 120-155 chars ({n})")
' "$readme" 2>&1); then
    echo "  ✗ $py_err"
    echo "    file: $rel"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✓ $rel"
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS manifest(s) failed linting."
  exit 1
else
  echo "✅ All manifests passed."
fi
