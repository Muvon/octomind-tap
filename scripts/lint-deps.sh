#!/usr/bin/env bash
# Lint all dep scripts in deps/**/*.sh
# Checks:
#   1. Header: # dep: <org>/<tool> matches file path
#   2. Header: # type: mcp|dep
#   3. Header: # description: (10–160 chars)
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
  mapfile -t FILES < <(find "$REPO_ROOT/deps" -name "*.sh" -not -path "*/lib/*" | sort)
fi

if [[ ${#FILES[@]} -eq 0 ]]; then
  echo "No dep scripts found."
  exit 0
fi

PYTHON_LINT=$(
  cat <<'PYEOF'
import sys, pathlib, re

path = pathlib.Path(sys.argv[1])
repo_root = pathlib.Path(sys.argv[2])

lines = path.read_text().splitlines()
errors = []

if len(lines) < 6:
    errors.append("HEADER_SHORT: dep script must have at least 6 header lines")
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

# Line 1: shebang (not checked here)
# Line 2: # dep: <org>/<tool>
dep_match = re.match(r'^# dep:\s*([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)$', lines[1])
if not dep_match:
    errors.append("HEADER_DEP: line 2 must be '# dep: <org>/<tool>'")
else:
    declared = dep_match.group(1)
    # Derive expected from file path: deps/<org>/<tool>.sh
    rel = path.relative_to(repo_root / "deps")
    expected = f"{rel.parent}/{rel.stem}"
    if declared != expected:
        errors.append(f"HEADER_DEP_MISMATCH: declared '{declared}' but file path says '{expected}'")

# Line 3: # type: mcp|dep
type_match = re.match(r'^# type:\s*(mcp|dep)$', lines[2])
if not type_match:
    errors.append("HEADER_TYPE: line 3 must be '# type: mcp' or '# type: dep'")
dep_type = type_match.group(1) if type_match else None

# Line 4: # description: <text>
desc_match = re.match(r'^# description:\s*(.+)$', lines[3])
if not desc_match:
    errors.append("HEADER_DESC: line 4 must be '# description: <text>'")
else:
    desc_val = desc_match.group(1).strip()
    if len(desc_val) < 10:
        errors.append(f"HEADER_DESC_SHORT: description must be >= 10 chars ({len(desc_val)})")
    elif len(desc_val) > 160:
        errors.append(f"HEADER_DESC_LONG: description must be <= 160 chars ({len(desc_val)})")

# Line 5: # check: <command>
check_match = re.match(r'^# check:\s*(.+)$', lines[4])
if not check_match:
    errors.append("HEADER_CHECK: line 5 must be '# check: <command>'")

# Line 6: # https://...
url_match = re.match(r'^# https?://', lines[5])
if not url_match:
    errors.append("HEADER_URL: line 6 must be a URL starting with '# https://'")

# Companion .md file
md_path = path.with_suffix('.md')
if not md_path.exists():
    errors.append(f"COMPANION_MISSING: {md_path.name} must exist alongside {path.name}")
else:
    md_text = md_path.read_text()
    md_lines = md_text.splitlines()

    # Check H1 heading matches <org>/<tool>
    h1_match = None
    for ml in md_lines:
        m = re.match(r'^#\s+(.+)$', ml)
        if m:
            h1_match = m.group(1).strip()
            break

    if dep_match:
        expected_h1 = dep_match.group(1)
        if not h1_match:
            errors.append("COMPANION_H1: .md file must have an H1 heading")
        elif h1_match != expected_h1:
            errors.append(f"COMPANION_H1_MISMATCH: H1 is '{h1_match}', expected '{expected_h1}'")

    # Check required sections based on type
    h2_headings = [re.match(r'^##\s+(.+)$', ml).group(1).strip()
                   for ml in md_lines if re.match(r'^##\s+', ml)]

    if dep_type == "mcp":
        required_sections = ["MCP Server", "Authentication", "Available Tools", "Configuration Example"]
        for sect in required_sections:
            if sect not in h2_headings:
                errors.append(f"COMPANION_MCP_SECTION: missing '## {sect}' in .md")
    elif dep_type == "dep":
        required_sections = ["Key Commands", "Common Usage"]
        for sect in required_sections:
            if sect not in h2_headings:
                errors.append(f"COMPANION_DEP_SECTION: missing '## {sect}' in .md")

if errors:
    print("\n".join(errors), file=sys.stderr)
    sys.exit(1)

sys.exit(0)
PYEOF
)

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
  if ! py_err=$(python3 -c "$PYTHON_LINT" "$file" "$REPO_ROOT" 2>&1); then
    while IFS= read -r line; do
      echo "  ✗ $line"
    done <<<"$py_err"
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
