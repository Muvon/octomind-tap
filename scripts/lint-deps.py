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
    if len(desc_val) < 120:
        errors.append(f"HEADER_DESC_SHORT: description must be >= 120 chars ({len(desc_val)}) — say what it does, what it needs")
    elif len(desc_val) > 155:
        errors.append(f"HEADER_DESC_LONG: description must be <= 155 chars ({len(desc_val)})")
    if ' - ' not in desc_val:
        errors.append("HEADER_DESC_NAME: description must read '<Name> - <what it does>'")

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
