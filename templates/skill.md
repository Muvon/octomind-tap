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

<!-- Canonical section order (2026 standard — see tap-skill-authoring):
     Overview → Mental model → Rules → Examples → Checklist → Composition / References
     Overview at the top (primacy), Checklist near the end (recency). -->

## Overview

Describe the skill's purpose in 2–4 sentences. Name the problem, the trigger, and the outcome. No fluff.

---

## Mental model

<!-- Optional but recommended for any skill with >3 rules. The framing concept that makes
     the rules read as a system, not a list. Skip if the skill is purely mechanical. -->

The core principle that governs all the rules below: ...

---

## Rules

<!-- The bulk of the skill. Tables for decisions, bullet lists for sequential rules, prose
     only when WHY is non-obvious. Never paragraph-after-paragraph. -->

### Core rules

- Rule 1: ...
- Rule 2: ...
- Rule 3: ...

### Decision guide

| Situation | Action |
|-----------|--------|
| Case A    | Do X   |
| Case B    | Do Y   |

### Workflow (if applicable)

1. Step one — description
2. Step two — description
3. Step three — description

---

## Examples

<!-- Bad → Good is the strongest format. Show the AI tell, then the fix. -->

### Example 1: Bad → Good

❌ Bad:
```
[the wrong way]
```

✅ Good:
```
[the right way]
```

What changed: <one-line explanation>

### Example 2: Edge case

<!-- Describe what makes this tricky and how to handle it. -->

---

## Checklist

<!-- Recency: this is the last actionable thing the model sees, so it acts as a final gate.
     Verifiable items only — "does X have Y" not "make sure quality is high". -->

- [ ] <verifiable check>
- [ ] <verifiable check>
- [ ] <verifiable check>

---

## Composition / References

<!-- Within-domain skill pairings (do NOT name agents from other domains).
     External authoritative sources, spec links. -->

- Pairs with `<sibling-skill-in-same-domain>` when ...
- [Official documentation](https://example.com/docs)
- [Specification](https://example.com/spec)

<!-- Optional directories alongside this SKILL.md:
  validate    — executable script: validates LLM output quality (exit 0 = valid)
  scripts/    — executable scripts the skill references
  references/ — supplementary documentation (REFERENCE.md, FORMS.md, etc.)
  assets/     — templates, config files, other resources
-->
