#!/usr/bin/env bash
# Lint all skill manifests in skills/*/SKILL.md
# Validates per the AgentSkills specification (https://agentskills.io/specification):
#   1. File exists at skills/<name>/SKILL.md
#   2. Valid YAML frontmatter (delimited by ---)
#   3. Required fields: name, title, description
#   4. name: lowercase letters, numbers, hyphens only; no leading/trailing hyphen; max 64 chars
#   5. title: non-empty, 5–60 chars
#   6. description: non-empty, 20–1024 chars
#   7. Optional fields validated if present: license, compatibility (max 500 chars), allowed-tools
#   8. Directory name matches the `name` field in frontmatter
#   9. Every reference/<file> cited in the body exists (skill-local, or skills/<other>/reference/)
#
# Usage:
#   scripts/lint-skills.sh                        # lint all skills
#   scripts/lint-skills.sh skills/git-workflow    # lint specific skill dir(s)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ERRORS=0

# Collect skill dirs to lint
if [[ $# -gt 0 ]]; then
  SKILL_DIRS=("$@")
else
  while IFS= read -r found; do
    SKILL_DIRS+=("$found")
  done < <(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [[ ${#SKILL_DIRS[@]} -eq 0 ]]; then
  echo "No skill directories found under skills/."
  exit 0
fi

lint_skill() {
  local skill_dir="$1"
  local rel="${skill_dir#"$REPO_ROOT/"}"
  local skill_md="$skill_dir/SKILL.md"
  local ok=1

  # Must be directly under skills/ (no extra nesting)
  local inner="${skill_dir#"$REPO_ROOT/skills/"}"
  if [[ $inner == */* ]]; then
    echo "  ✗ path: skills must be at skills/<name>/ (got extra nesting: $rel)"
    ok=0
  fi

  # SKILL.md must exist
  if [[ ! -f $skill_md ]]; then
    echo "  ✗ missing: $rel/SKILL.md"
    ok=0
  else
    # Validate frontmatter and content
    local py_err
    if ! py_err=$(python3 "$REPO_ROOT/scripts/lint-skills.py" "$skill_md" 2>&1); then
      echo "  ✗ $py_err"
      ok=0
    fi
  fi

  # validate script must be executable if it exists
  for script_name in validate; do
    local script_path="$skill_dir/$script_name"
    if [[ -f $script_path && ! -x $script_path ]]; then
      echo "  ✗ $rel/$script_name: exists but is not executable (chmod +x)"
      ok=0
    fi
  done

  if [[ $ok -eq 1 ]]; then
    echo "  ✓ $rel"
  else
    echo "    skill: $rel"
    return 1
  fi
}

echo "Linting ${#SKILL_DIRS[@]} skill(s)..."
echo ""

for skill_dir in "${SKILL_DIRS[@]}"; do
  # Normalise to absolute path
  [[ $skill_dir == /* ]] || skill_dir="$REPO_ROOT/$skill_dir"
  # Strip trailing slash
  skill_dir="${skill_dir%/}"

  if ! lint_skill "$skill_dir"; then
    ERRORS=$((ERRORS + 1))
  fi
done

echo ""
if [[ $ERRORS -gt 0 ]]; then
  echo "❌ $ERRORS skill(s) failed linting."
  exit 1
else
  echo "✅ All skills passed."
fi
