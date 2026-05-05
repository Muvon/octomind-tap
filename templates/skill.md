---
# Required fields
name: my-skill-name
title: "My Skill Name (5–60 chars)"
description: "One-line description of what this skill does and when to use it. Be specific — this is what the AI reads when deciding whether to activate the skill."

# Optional fields
license: Apache-2.0
compatibility: "Describe environment requirements: intended product (e.g. Octomind), system tools needed (e.g. git, docker), network access, OS constraints."
# capabilities: git memory              # capabilities to auto-load when skill activates (space-delimited)
# domains: developer devops             # agent categories that auto-check this skill (omit for manual-only)
# allowed-tools: shell view text_editor  # space-delimited pre-approved tools (experimental)
# rules:                                # auto-activation rules (omit for manual-only)
#   - file(Cargo.toml)                  # OR: file exists in workdir (glob ok: *.rs, src/**/*.go)
#   - content(rust)                     # OR: user message contains whole word "rust" (not "rusty")
#   - file(Cargo.toml) content(async)   # OR: BOTH file exists AND message contains "async" (AND within line)
#   - grep(tokio, Cargo.toml)           # OR: file content matches pattern (grep(pattern, glob))
#   - match(rewrite.*in rust)           # OR: user message matches regexp
#   - env(CI)                           # OR: env var CI is set
#   - env(NODE_ENV=production)          # OR: env var equals value
#   - bin(cargo)                        # OR: binary is available in $PATH
#   - workdir(my-project)               # OR: working directory path contains substring
#   - session(rust)                     # OR: current session name contains word (e.g. developer:rust)
#   - semantic(rewrite this in rust)    # OR: user message is semantically close to the phrase (intent-based, paraphrase-tolerant)
# metadata:
#   author: your-name
#   version: "1.0"
#   tags: "tag1 tag2"
---

# My Skill Name

<!-- One-paragraph overview: what problem this skill solves and when to use it. -->

## Overview

Describe the skill's purpose in 2–4 sentences. What domain knowledge does it encode?
What tasks does it help with? When should the AI activate this skill?

---

## Instructions

<!-- The core of the skill: step-by-step guidance, rules, conventions, decision trees. -->
<!-- Write as if instructing the AI directly. Be precise and actionable. -->

### Core Rules

- Rule 1: ...
- Rule 2: ...
- Rule 3: ...

### Workflow

1. **Step one** — description
2. **Step two** — description
3. **Step three** — description

### Decision Guide

| Situation | Action |
|-----------|--------|
| Case A    | Do X   |
| Case B    | Do Y   |

---

## Examples

<!-- Concrete examples are the most valuable part of a skill. -->
<!-- Show input → output, before → after, or command → result. -->

### Example 1: Basic case

```
Input or context here
```

Expected output or behavior:

```
Result here
```

### Example 2: Edge case

<!-- Describe what makes this tricky and how to handle it. -->

---

## References

<!-- Optional: link to external docs, standards, or bundled reference files. -->
<!-- For bundled files, use relative paths: references/FORMS.md -->

- [Official documentation](https://example.com/docs)
- [Specification](https://example.com/spec)

<!-- If you have reference files, place them in references/ and link here:
- See [references/REFERENCE.md](references/REFERENCE.md) for the full reference guide.
-->

---

<!-- Optional directories and files you can add alongside this SKILL.md:
  validate    — executable script: validates LLM output quality (exit 0 = valid, stderr = error)
  scripts/    — executable scripts the skill references
  references/ — supplementary documentation (REFERENCE.md, FORMS.md, etc.)
  assets/     — templates, config files, other resources
-->
