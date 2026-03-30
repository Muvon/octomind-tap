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
  mapfile -t SKILL_DIRS < <(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [[ ${#SKILL_DIRS[@]} -eq 0 ]]; then
  echo "No skill directories found under skills/."
  exit 0
fi

# Python YAML frontmatter validator
PYTHON_SKILL_CHECK=$(
  cat <<'EOF'
import sys, re, pathlib

path = pathlib.Path(sys.argv[1])

if not path.exists():
    print(f"MISSING: {path} does not exist", file=sys.stderr)
    sys.exit(1)

content = path.read_text(encoding="utf-8")
skill_dir = path.parent
dir_name = skill_dir.name

# ── Frontmatter extraction ────────────────────────────────────────────────────
stripped = content.lstrip()
if not stripped.startswith("---"):
    print("NO_FRONTMATTER: SKILL.md must start with --- frontmatter block", file=sys.stderr)
    sys.exit(1)

after_open = stripped[3:].lstrip("\n")
end = after_open.find("\n---")
if end == -1:
    print("FRONTMATTER_UNCLOSED: opening --- has no closing ---", file=sys.stderr)
    sys.exit(1)

frontmatter = after_open[:end]

# ── Parse key: value pairs (simple YAML subset) ───────────────────────────────
fields = {}
for line in frontmatter.splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    if ":" not in line:
        continue
    key, _, value = line.partition(":")
    key = key.strip()
    value = value.strip().strip('"').strip("'")
    fields[key] = value

# ── Required: name ────────────────────────────────────────────────────────────
if "name" not in fields or not fields["name"]:
    print("MISSING_NAME: 'name' is required in frontmatter", file=sys.stderr)
    sys.exit(1)

name = fields["name"]

# name format: lowercase letters, numbers, hyphens; no leading/trailing hyphen; max 64
if len(name) > 64:
    print(f"NAME_TOO_LONG: name '{name}' exceeds 64 characters", file=sys.stderr)
    sys.exit(1)

if not re.match(r'^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$', name):
    print(f"NAME_INVALID: name '{name}' must be lowercase letters, numbers, and hyphens only; must not start or end with a hyphen", file=sys.stderr)
    sys.exit(1)

# Directory name must match the name field
if dir_name != name:
    print(f"NAME_MISMATCH: directory name '{dir_name}' does not match name field '{name}'", file=sys.stderr)
    sys.exit(1)

# ── Required: title ───────────────────────────────────────────────────────────
if "title" not in fields or not fields["title"].strip():
    print("MISSING_TITLE: 'title' is required in frontmatter", file=sys.stderr)
    sys.exit(1)

skill_title = fields["title"]
if len(skill_title) < 5:
    print(f"TITLE_TOO_SHORT: title must be at least 5 characters ({len(skill_title)} chars)", file=sys.stderr)
    sys.exit(1)

if len(skill_title) > 60:
    print(f"TITLE_TOO_LONG: title exceeds 60 characters ({len(skill_title)} chars)", file=sys.stderr)
    sys.exit(1)

# ── Required: description ─────────────────────────────────────────────────────
if "description" not in fields or not fields["description"].strip():
    print("MISSING_DESCRIPTION: 'description' is required and must be non-empty", file=sys.stderr)
    sys.exit(1)

desc = fields["description"]
if len(desc) < 20:
    print(f"DESCRIPTION_TOO_SHORT: description must be at least 20 characters ({len(desc)} chars)", file=sys.stderr)
    sys.exit(1)

if len(desc) > 1024:
    print(f"DESCRIPTION_TOO_LONG: description exceeds 1024 characters ({len(desc)} chars)", file=sys.stderr)
    sys.exit(1)

# ── Optional: compatibility ───────────────────────────────────────────────────
if "compatibility" in fields and len(fields["compatibility"]) > 500:
    print(f"COMPATIBILITY_TOO_LONG: compatibility exceeds 500 characters ({len(fields['compatibility'])} chars)", file=sys.stderr)
    sys.exit(1)

# ── Body must be non-empty ────────────────────────────────────────────────────
body_start = after_open.find("\n---") + 4  # skip past closing ---
body = after_open[body_start:].strip()
if not body:
    print("EMPTY_BODY: SKILL.md body (after frontmatter) must not be empty", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
EOF
)

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
    if ! py_err=$(python3 -c "$PYTHON_SKILL_CHECK" "$skill_md" 2>&1); then
      echo "  ✗ $py_err"
      ok=0
    fi
  fi

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
