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
# The description is also the skill page's search snippet on octomind.run:
# 120–155 chars says what it covers and when to use it without being cut off.
if len(desc) < 120:
    print(f"DESCRIPTION_TOO_SHORT: description must be at least 120 characters ({len(desc)} chars)", file=sys.stderr)
    sys.exit(1)

if len(desc) > 155:
    print(f"DESCRIPTION_TOO_LONG: description must be at most 155 characters ({len(desc)} chars)", file=sys.stderr)
    sys.exit(1)

# ── Optional: compatibility ───────────────────────────────────────────────────
if "compatibility" in fields and len(fields["compatibility"]) > 500:
    print(f"COMPATIBILITY_TOO_LONG: compatibility exceeds 500 characters ({len(fields['compatibility'])} chars)", file=sys.stderr)
    sys.exit(1)

# ── Optional: domains / capabilities must reference real directories ──────────
# domains: exact-match against agents/<domain>/ (runtime compares the role's
# domain prefix); a phantom value silently never auto-activates.
# capabilities: resolved from capabilities/<name>/ at activation; a phantom
# value silently fails to load its MCP servers.
repo_root = skill_dir.parent.parent

def _split_values(raw):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [v.strip().strip('"').strip("'") for v in raw[1:-1].split(",") if v.strip()]
    return raw.split()

if fields.get("domains"):
    for d in _split_values(fields["domains"]):
        if not (repo_root / "agents" / d).is_dir():
            print(f"DOMAIN_UNKNOWN: domains value '{d}' has no agents/{d}/ directory — it will never auto-activate", file=sys.stderr)
            sys.exit(1)

if fields.get("capabilities"):
    for c in _split_values(fields["capabilities"]):
        cap_name = c.split(":")[0]
        if not (repo_root / "capabilities" / cap_name).is_dir():
            print(f"CAPABILITY_UNKNOWN: capabilities value '{c}' has no capabilities/{cap_name}/ directory — it will silently fail to load", file=sys.stderr)
            sys.exit(1)

# ── Body must be non-empty ────────────────────────────────────────────────────
body_start = after_open.find("\n---") + 4  # skip past closing ---
body = after_open[body_start:].strip()
if not body:
    print("EMPTY_BODY: SKILL.md body (after frontmatter) must not be empty", file=sys.stderr)
    sys.exit(1)

# ── reference/ files cited in the body must exist ─────────────────────────────
# `reference/x.md` resolves inside this skill; `skills/<other>/reference/x.md`
# resolves from the repo root. Placeholders (<topic>, *.md) and paths under
# another directory (doc/reference/…) are skipped.
for m in re.finditer(r'(?<![\w/.-])(?:skills/([a-z0-9-]+)/)?reference/([A-Za-z0-9_./<>*-]+)', body):
    other_skill, ref_file = m.group(1), m.group(2).rstrip('.,;:)')
    if '<' in ref_file or '*' in ref_file:
        continue
    base = (repo_root / "skills" / other_skill) if other_skill else skill_dir
    if not (base / "reference" / ref_file).is_file():
        print(f"REFERENCE_MISSING: body cites '{m.group(0)}' but {base.relative_to(repo_root)}/reference/{ref_file} does not exist", file=sys.stderr)
        sys.exit(1)

# ── Markdown noise guardrails (hard rules) ────────────────────────────────────
# Strip code (fenced, inline, and 4-space indented blocks) before checking
no_fences = re.sub(r'```.*?```', '', body, flags=re.DOTALL)
no_fences = re.sub(r'^    .*$', '', no_fences, flags=re.MULTILINE)
no_inline_code = re.sub(r'`[^`\n]+`', '', no_fences)

# No **bold** outside code blocks — markdown headers and structure are enough
bold_matches = re.findall(r'\*\*[^*\n]+?\*\*', no_inline_code)
if bold_matches:
    sample = bold_matches[0][:60]
    print(f"BODY_HAS_BOLD: {len(bold_matches)} **bold** pattern(s) in body — strip them (headers and lists provide structure). First match: {sample}", file=sys.stderr)
    sys.exit(1)

# No ***bold-italic*** — pure decoration
bi_matches = re.findall(r'\*\*\*[^*\n]+?\*\*\*', no_inline_code)
if bi_matches:
    sample = bi_matches[0][:60]
    print(f"BODY_HAS_BOLD_ITALIC: {len(bi_matches)} ***bold-italic*** pattern(s) in body — strip them. First match: {sample}", file=sys.stderr)
    sys.exit(1)

# No *italic* — pure decoration (asterisk emphasis adds no semantic value for the model)
italic_matches = re.findall(r'(?<![*\w])\*([^*\s][^*\n]{0,200}?[^*\s])\*(?!\*)', no_inline_code)
if italic_matches:
    sample = italic_matches[0][:60]
    print(f"BODY_HAS_ITALIC: {len(italic_matches)} *italic* pattern(s) in body — strip them (decoration, not semantics). First match: *{sample}*", file=sys.stderr)
    sys.exit(1)

# No --- horizontal rule separators — ## H2 already marks sections
hr_matches = re.findall(r'^---\s*$', no_inline_code, re.MULTILINE)
if hr_matches:
    print(f"BODY_HAS_HR: {len(hr_matches)} '---' horizontal-rule separator(s) in body — strip them (## headers already mark sections; HR is pure decoration)", file=sys.stderr)
    sys.exit(1)

# No leading # H1 — frontmatter `title:` is the canonical title; H1 in body duplicates it
body_stripped = body.lstrip()
if body_stripped.startswith('# '):
    h1_line = body_stripped.split('\n', 1)[0]
    print(f"BODY_HAS_REDUNDANT_H1: body starts with '{h1_line[:60]}' — frontmatter `title:` is the canonical title; remove the H1 (token waste, no semantic gain)", file=sys.stderr)
    sys.exit(1)

# Body length cap — Anthropic recommends "under 500 lines" (~2500-3500 words)
# Beyond ~4000 words, context rot degrades recall on individual rules
word_count = len(body.split())
SOFT_LIMIT = 3000
HARD_LIMIT = 4500
if word_count > HARD_LIMIT:
    print(f"BODY_TOO_LONG: body is {word_count} words (hard limit {HARD_LIMIT}). Anthropic recommends splitting large skills via progressive disclosure (SKILL.md + reference/*.md files).", file=sys.stderr)
    sys.exit(1)
if word_count > SOFT_LIMIT:
    # Soft warning — does not fail lint, just surfaces
    print(f"BODY_LENGTH_WARN: body is {word_count} words (soft target {SOFT_LIMIT}). Consider splitting into reference files for better token economy.", file=sys.stderr)

sys.exit(0)
