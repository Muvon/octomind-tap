---
name: tap-skill-authoring
title: "Tap Skill Authoring"
description: "Guide for creating AgentSkills-compliant SKILL.md packs in an Octomind tap: frontmatter fields, auto-activation rules and domains, bundled resources, validate scripts, body structure, tone, and the lint gates. Activate when creating or editing skills/<name>/SKILL.md files."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-skills.sh."
domains: octomind
---

## Overview

A skill is a reusable instruction pack at `skills/<name>/SKILL.md`. When it activates — preloaded, auto-activated by its rules, or loaded with `skill(action="use")` or `/skill <name>` — its body is injected into the session's context. Skills don't define a role, model, or tools; they add focused knowledge any agent in their domain can use.

## Mental model

A skill is a checklist for a model that already knows the field. Anthropic's skill guidance starts from "Claude is already very smart — only add context Claude doesn't already have." Every token ships on every activation, so the body carries decisions, conventions, and gates, not textbook background. Activation is decided by the frontmatter (`domains` plus `rules`), so the frontmatter is as much a part of the design as the body.

## Rules

### Directory structure

```
skills/<skill-name>/
├── SKILL.md        # required
├── reference/      # long reference files, cited from the body and lint-checked
├── scripts/        # executables the skill tells the agent to run
├── assets/         # templates and resources
└── validate        # optional output validator (chmod +x)
```

On activation the runtime lists every file under `scripts/`, `references/`, and `assets/` with absolute paths in a Skill Resources section. `reference/` (singular, the tap convention) is not in that list, so cite those files from the body by path; `lint-skills.sh` fails if a cited `reference/<file>` does not exist. Keep references one level deep from SKILL.md.

### Frontmatter

```markdown
---
name: skill-name
title: "Skill Title"
description: "What this skill does and when to use it."
license: Apache-2.0
compatibility: "Requires: tool1. macOS/Linux."
capabilities: versioning
domains: developer
rules:
  - file(Cargo.toml)
  - content(rust) content(async)
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | yes | ≤64 chars, lowercase letters, digits, hyphens; no leading/trailing hyphen; equals the directory name |
| `title` | yes (tap lint) | 5–60 chars |
| `description` | yes | 20–1024 chars, third person, what it does plus when to use it with concrete trigger terms |
| `domains` | for auto-activation | Space-separated or array; each value must be an existing `agents/<domain>/` directory (lint); the runtime also accepts `*` for every domain, but tap lint rejects it |
| `rules` | for auto-activation | List of rule expressions, below |
| `capabilities` | optional | Capabilities enabled when the skill activates; each must exist under `capabilities/` (lint) |
| `compatibility` | optional | ≤500 chars, environment only (tools, OS, network) |
| `license`, `metadata`, `allowed-tools` | optional | `allowed-tools` is space-separated; missing tools are reported as an incompatibility |

The runtime parser reads `name`, `description`, `compatibility`, `license`, `allowed-tools`, `capabilities`, `domains`, and `rules`; a skill without `name` or `description` is skipped. Without both `domains` and `rules`, a skill is manual-only.

### Auto-activation rules

Rules are evaluated on fresh user messages when `[skills] auto_activation` is on and the session domain is in `domains`. Each `- ` item is an OR branch; several expressions on one line are ANDed.

| Expression | Matches when |
|------------|--------------|
| `file(<path or glob>)` | Path exists in the workdir, or the glob matches (`*.rs`, `src/**/*.go`) |
| `content(<word>)` | User message contains the word (whole word, case-insensitive) |
| `match(<regex>)` | User message matches the regex (nested parentheses are fine) |
| `grep(<pattern>[, <glob>])` | A gitignore-respecting workdir file contains the pattern; the glob filters by file name only (`*.toml`, not `src/**/*.rs`) |
| `env(<VAR>)` / `env(<VAR>=<value>)` | Variable set and non-empty / equals value |
| `bin(<command>)` | Command found on `PATH` |
| `workdir(<text>)` | Working-directory path contains the text (case-insensitive) |
| `session(<text>)` | Session name contains the text (case-insensitive). Default names are `YYMMDD-<dir>-HHMM-<id>`; `tap run` sessions are `tap-<domain>-<spec>-<hex>`, so `session(<spec>)` targets one agent only in tap runs or `-n`-named sessions |
| `semantic(<phrase>[, <threshold>])` | Embedding cosine between the message and the phrase clears the threshold (default 0.65) |

Deterministic matches activate directly. Semantic-only candidates must also beat the runner-up by a 0.06 margin, so near-ties abstain. Adding or changing `semantic(...)` phrases changes the tap embedding model's training data — see the `tap-model-training` skill.

### Validate script

`skills/<name>/validate` runs at the end of each assistant turn while the skill is active, only when `[skills] auto_validation = true` (default `false`), and only for skills that come from a tap. Contract: argv[1] is `assistant`, the final assistant message arrives on stdin, cwd is the project workdir. A non-zero exit with non-empty stderr counts as a failure and the stderr is fed back to the model; retries per skill are capped by `[skills] max_retries`, timeout by `validation_timeout`. Make it executable.

### Body structure

Fixed section order, U-shaped for attention: the opening and the closing get read most carefully, the middle relies on headers as anchors.

```
## Overview              why and when (2–4 sentences)
## Mental model          governing principles
## Rules                 tables, bullets, decision guides
## Examples              bad → good pairs
## Checklist             verifiable gates before shipping
## Composition / References   sibling skills in the same domain, sources
```

- Overview names the problem, trigger, and outcome.
- Rules: tables for decisions, bullets for sequences, prose only when the why is non-obvious.
- Examples: two or three bad → good pairs with a one-line caption; more go to `reference/`.
- Checklist: verifiable items only.

### Length and markdown

- Aim under ~2000 words. `lint-skills.sh` warns above 3000 body words and fails above 4500; Anthropic recommends keeping SKILL.md under 500 lines.
- Move long tables, exhaustive option lists, and schema dumps to `reference/*.md`; SKILL.md stays the navigator.
- No `# H1` at the top of the body (frontmatter `title` is the title), no bold, no italics, no `---` rules inside the body — all lint failures. Tables and code fences stay.
- Avoid time-sensitive phrasing ("before August"); write the current method.

### Tone

The same calibration as agent prompts: current Claude models follow instructions precisely and over-trigger on emphatic language.

- `CRITICAL: YOU MUST X` → `X.`
- Stacked `NEVER`/`ALWAYS` bullets → plain `Don't …` / `Do …`
- `MANDATORY:` headers → descriptive section names

Reserve all-caps for one or two genuine safety hard-stops. Full guidance: `skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

### Domain isolation

- `domains:` single-valued wherever possible — pick the domain that owns the deliverable.
- `compatibility:` describes the environment, never pairings with agents.
- The body never names agents from other domains; describe downstream work as owned by another domain. Sibling skills in the same domain may be named sparingly.

### Creation workflow

1. Identify the knowledge the model lacks: conventions, decision rules, gates.
2. Pick a specific name (`rust-error-handling`, not `rust`).
3. Copy `templates/skill.md`; write frontmatter, then the body in canonical order.
4. Add `domains` + `rules` only if it should auto-activate; test that the rules match the intended prompts and nothing broader.
5. Optionally add `validate`.
6. Run `bash scripts/lint-skills.sh skills/<name>`; test with `/skill <name>` in a session.

## Examples

### Example 1: minimal valid skill

```markdown
---
name: git-workflow
title: "Git Workflow"
description: "Commit message conventions and branch naming. Use when committing or creating branches."
license: Apache-2.0
---

## Overview
Encodes Conventional Commits and branch naming.

## Rules
- Prefix commits with `feat:`, `fix:`, `chore:`.
- Branch names: `feat/short-description`, `fix/short-description`.
```

### Example 2: auto-activation

```markdown
---
name: programming-rust
title: "Rust Programming"
description: "Rust idioms, error handling, async patterns. Auto-activates in Rust projects."
domains: developer
rules:
  - file(Cargo.toml)
  - grep(tokio, Cargo.toml) content(async)
  - semantic(write idiomatic rust code)
---
```

### Example 3: common mistakes

❌ `# Git Workflow` as the first body line — lint fails with `BODY_HAS_REDUNDANT_H1`.

❌ `grep(async_trait, src/**/*.rs)` — the glob is matched against file names only, so it never matches. Use `grep(async_trait, *.rs)`.

❌ `domains: dev` — no `agents/dev/` directory, so lint fails and it would never activate.

## Checklist

- [ ] Description in third person, says what and when, with concrete trigger terms?
- [ ] `name` equals the directory; `domains` and `capabilities` reference real directories?
- [ ] Rules match the intended prompts and nothing broader; semantic phrases one idea each?
- [ ] Body in canonical order, no H1, bold, italics, or `---`; under ~2000 words?
- [ ] Instructions actionable and specific; examples for non-obvious rules?
- [ ] Tone calibrated: plain directives, all-caps only for real hard-stops?
- [ ] Cited `reference/` files exist; `validate` executable if present?
- [ ] `bash scripts/lint-skills.sh skills/<name>` passes?

## Composition / References

- `templates/skill.md` — canonical skill template
- `tap-model-training` — retrain after changing `semantic(...)` phrases
- [AgentSkills specification](https://agentskills.io/specification)
- [Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
