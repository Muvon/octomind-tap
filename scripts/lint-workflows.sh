#!/usr/bin/env bash
# Lint all workflows in workflows/*.toml
# Checks:
#   1. Valid TOML; `name` matches the file stem; description 20–400 chars
#   2. Comment metadata: # Title: (5–60 chars)
#   3. Step names unique across steps and sub-steps; none named `input`
#   4. Every sequential step / sub-step has a prompt and a public role tag
#      (category:variant) that resolves to agents/<domain>/<spec>.toml
#   5. Every {{var}} is `input`, a step name, or an uppercase placeholder
#   6. exit_when / condition / edge `when` set exactly one of contains|matches,
#      and every `matches` regex compiles
#   7. Loops set exit_when and a max_iterations of 1–3
#   8. Graph mode (entry / [[edges]]) sets max_transitions
#   9. max_cost, when set, is a positive number
#  10. Listed in workflows/README.md; the root README workflow count is current
#  11. `octomind workflow <file> --dry-run` passes (skipped when octomind is not installed)
#
# Usage:
#   scripts/lint-workflows.sh                         # lint all workflows
#   scripts/lint-workflows.sh workflows/review.toml   # lint specific files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

if [[ $# -gt 0 ]]; then
  FILES=("$@")
else
  while IFS= read -r found; do
    FILES+=("$found")
  done < <(find "$REPO_ROOT/workflows" -maxdepth 1 -name "*.toml" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No workflow files found."
  exit 0
fi

lint_file() {
  local file="$1"
  local rel="${file#"$REPO_ROOT/"}"
  local ok=1

  local py_err
  if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-workflows.py" "$file" "$REPO_ROOT" 2>&1); then
    echo "$py_err"
    ok=0
  fi

  local stem
  stem="$(basename "$file" .toml)"
  if ! grep -qF "](./$stem.toml)" "$REPO_ROOT/workflows/README.md"; then
    echo "  ✗ NOT_LISTED: add $stem to the table in workflows/README.md"
    ok=0
  fi

  if command -v octomind >/dev/null 2>&1; then
    local dry_err
    if ! dry_err=$(octomind workflow "$file" --dry-run 2>&1 >/dev/null); then
      echo "  ✗ DRY_RUN: ${dry_err##*$'\n'}"
      ok=0
    fi
  fi

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $rel"
  else
    echo "    file: $rel"
    return 1
  fi
}

echo "Linting ${#FILES[@]} workflow(s)..."
echo ""

for file in "${FILES[@]}"; do
  [[ $file == /* ]] || file="$REPO_ROOT/$file"

  if ! lint_file "$file"; then
    ERRORS=$((ERRORS + 1))
  fi
done

# Repo-wide: the root README count must match what ships
if [[ $# -eq 0 ]]; then
  actual=${#FILES[@]}
  claimed=$(grep -oE '[0-9]+ ready-made workflows' "$REPO_ROOT/README.md" | grep -oE '^[0-9]+' || true)
  table=$(grep -E '^\| `workflows/<name>\.toml`' "$REPO_ROOT/README.md" | grep -oE '[0-9]+ \|$' | grep -oE '^[0-9]+' || true)
  for n in $claimed $table; do
    if [[ $n -ne $actual ]]; then
      echo "  ✗ README.md claims $n workflows but workflows/ has $actual"
      ERRORS=$((ERRORS + 1))
    fi
  done
fi

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS workflow check(s) failed."
  exit 1
else
  echo "✅ All workflows passed."
fi
