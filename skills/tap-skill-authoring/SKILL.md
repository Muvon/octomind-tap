---
name: tap-skill-authoring
title: "Tap Skill Authoring"
description: "Complete guide for creating AgentSkills-compliant SKILL.md packs in the octomind-tap registry: frontmatter fields, body structure, auto-activation rules, validate scripts, and quality principles. Activate when creating or editing skills/<name>/SKILL.md files."
license: Apache-2.0
compatibility: "Requires: any Octomind tap with a skills/ directory."
domains: octomind
---

## Overview

A skill is a reusable instruction pack stored under `skills/<name>/SKILL.md`. When activated in an Octomind session via `skill(action="use", name="<name>")`, the skill's full content is injected into the AI's context — giving it domain-specific knowledge, conventions, and workflows on demand.

Skills are not agents — they don't define a role or model. They are context injections: focused, composable knowledge packs that any agent can load on demand.

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

### Body Structure (mandatory section order — 2026 standard)

Skills are loaded into agent context as Markdown. They follow a fixed section order grounded in the U-shape attention curve: the start (Overview) and the end (Checklist + References) get the most attention, the middle holds the bulk knowledge with clear headers as retrieval anchors.

```
1. Overview              ← primacy: why this skill, when to activate (2–4 sentences)
2. Mental model          ← core principles or governing concepts (the framing)
3. Rules / Instructions  ← the actual rule content — tables, bullets, decision guides
4. Examples              ← concrete bad → good or input → output pairs
5. Diagnostic / Checklist ← recency: verifiable checks before shipping
6. Composition / References ← how this skill pairs with siblings (within-domain only) + external sources
```

Why this order:
- Overview first — reader (human or AI) needs to know if this skill applies before reading rules
- Mental model before rules — gives the framing so individual rules make sense
- Rules in the middle, but headed with clear `## H2` anchors so they survive "lost in the middle"
- Examples after rules so the rules are concrete by the time they're seen
- Checklist near the end — recency: it's the last actionable thing the model sees, so it acts as a final gate
- References last — outbound links, lowest attention need

Section authoring rules:
- Overview — 2–4 sentences. Names the problem, the trigger, and the outcome. No fluff.
- Mental model — Optional but recommended for any skill with >3 rules. Without it, rules read as a list; with it, they read as a system.
- Rules — Tables for decisions, bullet lists for sequential rules, prose only when the why is non-obvious. Never write paragraph-after-paragraph.
- Examples — Bad → Good is the strongest format. Show the AI tell, then the fix. One concrete example beats three abstract rules.
- Checklist — Verifiable items only. "Score 0–10 on each dimension" beats "Make sure quality is high."
- References — Within-domain skills, external authoritative sources, spec links. Don't list every blog post you read.

Token discipline (Claude 4.7 / 2026):
- Target: under 3000 words. Anthropic recommends "under 500 lines" for optimal performance.
- Hard cap: 4500 words. Above this, `lint-skills.sh` fails with `BODY_TOO_LONG` and the skill must be split via progressive disclosure (SKILL.md as navigator + `reference/*.md` files loaded on demand).
- Beyond ~3000 words, recall on individual rules starts degrading (context rot)
- Cut decorative prose; if a sentence doesn't make a rule clearer, delete it
- Be explicit — Claude 4.7 doesn't bridge implicit gaps anymore

Markdown discipline (token waste — hard-blocked by `lint-skills.sh`):
- No `# H1` at the top of the body. Frontmatter `title:` is the canonical title; an H1 duplicates it. Body starts with `## Overview` directly.
- No `**bold**` outside code. Use `## H2` and `### H3` headers for structure; the model doesn't need bold for emphasis.
- No `*italic*` and no `***bold-italic***`. Pure decoration, zero semantic value.
- No `---` horizontal-rule separators inside the body. `## H2` headers already mark sections; HR is visual noise.
- Tables and code fences stay — they are structural, not decorative.

The rule of thumb: every character ships to the model on every activation. If removing it doesn't change what the model would do, remove it.

Tone calibration (Claude 4.6+ over-emphasis — mandatory awareness):

Skills load into the agent context as instruction packs, so the same calibration rules that apply to agent prompts apply here. Claude 4.5+ over-triggers on aggressive language that older models needed.

- `CRITICAL: YOU MUST X` → `X.`
- `🚨 HARD RULES` + stacked `NEVER`/`ALWAYS` bullets → plain `Don't …` / `Do …` in the Rules section
- `MANDATORY:` headers → drop, use descriptive section names
- `NEVER X` → `Don't X.` (capitals reserved for one or two genuine safety hard-stops)
- `ALWAYS X` → `Do X.` or fold into a positive rule

The substance test: delete the `NEVER`/`ALWAYS`/`MUST` and lowercase the line. Does the rule still make sense? Soften it. Does it read as filler once softened? Cut it.

Full reference (verbatim Anthropic guidance, parallel-tool-calls block, message-history rules): `skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

Bloat prevention (the three patterns that cause skills to outgrow the cap):

1. Default to skip — for every paragraph longer than 2 sentences, ask: "what specifically does this tell the model that it doesn't already know?" If the answer is general industry context, history, or motivation that Claude already has, cut it. Skills are checklists for the model that already knows the domain, not textbooks. Anthropic's stance: "Default assumption: Claude is already very smart. Only add context Claude doesn't already have."
2. Examples cap — keep 2–3 best examples in SKILL.md (bad → good with one-line caption per pair). The rest go in `reference/examples.md` and load on demand. An Examples section over ~800 words is almost always duplicating rules.
3. Reference content goes in `reference/*.md`, not in SKILL.md — long tables of values, exhaustive option lists, full schema dumps, and platform-history detail belong in `reference/*.md` files that are loaded only when the model needs them. SKILL.md is the navigator: rules + decision guide + 2–3 examples + pointers.

When a skill exceeds the soft 3000-word warning, audit before adding more. The fix is almost always trimming teach-mode paragraphs in Instructions, not extracting structure into more references.

### Auto-Activation Rules

Skills with both `rules:` and `domains:` can auto-activate without the AI calling the skill tool. Logic: OR between items, AND within a single item.

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

### Validate Script

A `validate` script at `skills/<name>/validate` checks LLM output quality at the end of each assistant turn:
- Must be executable (`chmod +x`)
- exit 0 → output is valid
- exit non-zero → stderr is fed back to the LLM for correction (retries capped by `[skills] max_retries`)

### Quality Principles

1. Specific beats generic — "Rust error handling" is more useful than "Rust development"
2. Instructions over descriptions — Tell the AI what to DO, not just describe the domain
3. Examples are gold — Every non-obvious rule needs a concrete example
4. One concern per skill — Don't bundle unrelated knowledge; compose multiple skills instead
5. Body must be actionable — If the AI can't follow the instructions directly, rewrite them
6. Compatibility matters — Be explicit about what tools/environment the skill requires
7. Stay in your domain — A skill belongs to one domain (its `domains:` field), and its body must not reach into others. No "hand off to `<other-domain>:<spec>`", no "companion agent: `<other-domain>:<spec>`", no language-specific build-agent references. The orchestrating agent composes domains; the skill stays focused on the work that lives inside its own. Cross-domain pollution makes skills brittle and creates implicit coupling that the agent layer can't override.

### Domain Isolation (the hard rule)

Skills are domain-scoped instruction packs. They are loaded by an agent in a specific domain (marketing, content, video, developer, etc.) and must focus only on what that domain owns. Concretely:

- `domains:` — single domain wherever possible. `domains: marketing content launch` couples the skill to three roles at once and is almost always wrong; pick the one that owns this skill's deliverable.
- `compatibility:` — environment requirements only (tools, OS, network). Do NOT use it to declare "Pairs with X agent" — pairing is the orchestrator's job.
- Body — never name agents from other domains (`content:`, `developer:`, `marketing:*`). If the work needs to be handed off, describe it as a downstream concern (e.g. "outreach copy is owned by another domain") without pinning a specific agent.
- Within-domain skill references are fine when genuinely useful (a marketing skill mentioning a sibling marketing skill), but keep them minimal — the orchestrator decides composition.

The architectural reason: a skill that names downstream agents bakes in routing decisions that belong to the agent that loaded it. When the orchestrator changes (e.g., a different marketing agent runs the same skill, or the content domain reuses it), those names become wrong. Keeping skills domain-isolated lets the agent layer compose them freely without rewriting skill bodies.

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
- [ ] Body follows the canonical section order? (Overview → Mental model → Rules → Examples → Checklist → Composition / References)
- [ ] Checklist section near the end? (recency — it's the final gate before the model acts)
- [ ] Are the instructions specific enough to follow without guessing?
- [ ] Are there examples for the non-obvious parts?
- [ ] Total skill body under ~2000 words? (context rot threshold for skills)
- [ ] Is the `name` field an exact match for the directory name?
- [ ] Is the `compatibility` field accurate?
- [ ] Tone calibrated for Claude 4.6+: no `CRITICAL: YOU MUST` / `🚨 HARD RULES` / stacked all-caps `NEVER`/`ALWAYS`? `Use X when ...` rather than `Default to X`?
- [ ] Does `bash scripts/lint-skills.sh skills/<name>` pass clean?

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

## References

- `templates/skill.md` — canonical skill template (copy to start)
- `bash scripts/lint-skills.sh` — validates skill files
- [AgentSkills specification](https://agentskills.io/specification)
