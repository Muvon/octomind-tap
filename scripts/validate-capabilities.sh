#!/usr/bin/env bash
# scripts/validate-capabilities.sh
# Validates all agent manifests by running bin/load on each one.
# Exits non-zero if any agent fails to resolve.
#
# Usage:
#   bash scripts/validate-capabilities.sh          # validate all agents
#   bash scripts/validate-capabilities.sh --quiet  # suppress per-agent output
#
# CI: add this to .github/workflows/validate.yml

set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOAD="$REPO_ROOT/bin/load"
AGENTS_DIR="$REPO_ROOT/agents"

QUIET=0
[[ ${1:-} == "--quiet" ]] && QUIET=1

if [[ ! -x $LOAD ]]; then
  echo "ERROR: bin/load is not executable. Run: chmod +x bin/load"
  exit 1
fi

PASS=0
FAIL=0
ERRORS=()

echo "Validating agent manifests..."
echo ""

for toml in "$AGENTS_DIR"/**/*.toml; do
  # Derive domain:spec from path
  rel="${toml#$AGENTS_DIR/}" # developer/rust.toml
  domain="${rel%%/*}"        # developer
  spec="${rel##*/}"          # rust.toml
  spec="${spec%.toml}"       # rust
  tag="$domain:$spec"

  if output=$(python3 "$LOAD" "$tag" 2>&1); then
    PASS=$((PASS + 1))
    if [[ $QUIET -eq 0 ]]; then
      echo "  ✅  $tag"
    fi
  else
    FAIL=$((FAIL + 1))
    ERRORS+=("$tag")
    echo "  ❌  $tag"
    echo "      $output"
  fi
done

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "Failed agents:"
  for e in "${ERRORS[@]}"; do
    echo "  - $e"
  done
  exit 1
fi

echo "All agents valid ✅"
