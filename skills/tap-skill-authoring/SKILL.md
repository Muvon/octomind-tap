---
name: tap-skill-authoring
title: "Tap Skill Authoring"
description: "Complete guide for creating AgentSkills-compliant SKILL.md packs in the octomind-tap registry: frontmatter fields, body structure, auto-activation rules, validate scripts, and quality principles. Activate when creating or editing skills/<name>/SKILL.md files."
license: Apache-2.0
compatibility: "Requires: any Octomind tap with a skills/ directory."
domains: octomind
---

# Tap Skill Authoring

## Overview

A skill is a reusable instruction pack stored under `skills/<name>/SKILL.md`. When activated in an Octomind session via `skill(action="use", name="<name>")`, the skill's full content is injected into the AI's context — giving it domain-specific knowledge, conventions, and workflows on demand.

Skills are **not agents** — they don't define a role or model. They are **context injections**: focused, composable knowledge packs that any agent can load on demand.

---

## Instructions

### Directory Structure

```
skills/<skill-name>/
├── SKILL.md        # Required: metadata + instructions
├── scripts/        # Optional: executable code the skill references
├── references/     # Optional: supplementary docs (REFERENCE.md, FORMS.md, etc.)
├── assets/         # Optional: templates, config files, resources
└── validate        # Optional: output validation script (must be chmod +x)
```

### SKILL.md Format

```markdown
---
name: skill-name
title: "Skill Title (5–60 chars)"
description: "What this skill does and when to use it."
license: Apache-2.0
compatibility: "Environment requirements: tools needed, OS, network access."
capabilities: git memory
domains: developer devops
rules:
  - file(marker-file)              # OR: file exists in workdir (glob ok: *.rs)
  - content(keyword)               # OR: user message contains whole word
  - file(marker) content(keyword)  # OR: BOTH conditions (AND within one line)
  - grep(pattern, glob)            # OR: file content matches
  - match(regexp)                  # OR: user message matches regexp
  - env(VAR)                       # OR: env var is set
  - env(VAR=value)                 # OR: env var equals value
# metadata:
#   author: name
#   version: "1.0"
# allowed-tools: shell view text_editor
---

# Skill Title

## Overview
...

## Instructions
...

## Examples
...
```

### Frontmatter Fields

| Field | Required | Rules |
|-------|----------|-------|
| `name` | ✅ | Max 64 chars. Lowercase, numbers, hyphens only. No leading/trailing hyphen. Must match directory name exactly. |
| `title` | ✅ | 5–60 chars. Short human-readable label. |
| `description` | ✅ | Max 1024 chars. Describes what the skill does and when to use it. |
| `capabilities` | optional | Capabilities to auto-load when skill activates. Space-delimited or array. |
| `domains` | optional | Agent categories for auto-activation scoping. Without this, skill is manual-only. |
| `rules` | optional | Auto-activation rules. If any matches, skill activates. Omit for manual-only. |
| `license` | optional | License name (e.g. `Apache-2.0`, `MIT`). |
| `compatibility` | optional | Max 500 chars. Environment requirements. |
| `metadata` | optional | Arbitrary key-value mapping (author, version, tags, etc.). |
| `allowed-tools` | optional | Space-delimited pre-approved tools (experimental). |

### Body Structure

1. **Overview** — What problem this solves, when to use it (2–4 sentences)
2. **Instructions** — Core rules, workflows, decision guides (the main content)
3. **Examples** — Concrete input/output pairs (most valuable part)
4. **References** — Links to docs, standards, or bundled reference files

---

### Auto-Activation Rules

Skills with both `rules:` and `domains:` can auto-activate without the AI calling the skill tool. Logic: **OR between items, AND within a single item**.

```yaml
rules:
  - file(Cargo.toml)                  # OR: Rust project marker exists
  - content(rust)                     # OR: user message contains "rust"
  - file(Cargo.toml) content(async)   # OR: BOTH file exists AND message has "async"
```

| Expression | Matches when |
|------------|-------------|
| `file(<glob>)` | File matching glob exists in working directory |
| `content(<word>)` | User message contains the word (whole-word, case-insensitive) |
| `match(<pattern>)` | User message matches the regular expression |
| `grep(<pattern>, <glob>)` | A file matching glob contains a line matching pattern |
| `env(<VAR>)` | Environment variable is set (non-empty) |
| `env(<VAR>=<value>)` | Environment variable equals value |

Skills without `rules:` are manual-only — they never auto-activate.

---

### Validate Script

A `validate` script at `skills/<name>/validate` checks LLM output quality at the end of each assistant turn:
- Must be executable (`chmod +x`)
- exit 0 → output is valid
- exit non-zero → stderr is fed back to the LLM for correction (retries capped by `[skills] max_retries`)

---

### Quality Principles

1. **Specific beats generic** — "Rust error handling" is more useful than "Rust development"
2. **Instructions over descriptions** — Tell the AI what to DO, not just describe the domain
3. **Examples are gold** — Every non-obvious rule needs a concrete example
4. **One concern per skill** — Don't bundle unrelated knowledge; compose multiple skills instead
5. **Body must be actionable** — If the AI can't follow the instructions directly, rewrite them
6. **Compatibility matters** — Be explicit about what tools/environment the skill requires

---

### Creation Workflow

1. Identify the domain knowledge to encode (conventions, workflows, checklists, decision trees)
2. Choose a clear, specific name: `git-workflow`, `code-review`, `rust-error-handling`
3. Copy `templates/skill.md` as starting point
4. Write frontmatter: `name`, `title`, `description`, optional `capabilities`, `domains`, `rules`
5. Write body: overview → instructions → examples → references
6. Optionally add `validate` script (`chmod +x`)
7. Validate: `bash scripts/lint-skills.sh skills/<name>`
8. Test: `skill(action="use", name="<name>")`

### Review Checklist

- [ ] Does the description tell you exactly when to activate it?
- [ ] Are the instructions specific enough to follow without guessing?
- [ ] Are there examples for the non-obvious parts?
- [ ] Is the `name` field an exact match for the directory name?
- [ ] Is the `compatibility` field accurate?
- [ ] Does `bash scripts/lint-skills.sh skills/<name>` pass clean?

---

## Examples

### Example 1: Minimal valid skill

```markdown
---
name: git-workflow
title: "Git Workflow"
description: "Git commit conventions and branch naming. Activate when committing or branching."
license: Apache-2.0
---

# Git Workflow

## Overview
Encodes Conventional Commits and branch naming rules.

## Instructions
- Use `feat:`, `fix:`, `chore:` prefixes on commits
- Branch names: `feat/short-description`, `fix/short-description`

## Examples
...
```

### Example 2: Skill with auto-activation

```markdown
---
name: programming-rust
title: "Rust Programming"
description: "Rust idioms, error handling, async patterns. Auto-activates in Rust projects."
domains: developer
rules:
  - file(Cargo.toml)
  - file(*.rs)
  - content(rust)
---
```

### Example 3: Common mistake — skill trying to be an agent

```markdown
# ❌ WRONG — skills don't define roles, models, or capabilities wiring
[[roles]]
system = "..."
temperature = 0.1

# ✅ CORRECT — skills are pure instruction content, no TOML config
```

---

## References

- `templates/skill.md` — canonical skill template (copy to start)
- `bash scripts/lint-skills.sh` — validates skill files
- [AgentSkills specification](https://agentskills.io/specification)
