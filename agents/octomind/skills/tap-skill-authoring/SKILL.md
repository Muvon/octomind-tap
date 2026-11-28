---
name: tap-skill-authoring
title: "Tap Skill Authoring"
description: "Create AgentSkills-compliant SKILL.md packs: frontmatter, auto-activation rules, domains, bundled resources, lint gates. Use when editing a SKILL.md."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-skills.sh."
---

## Overview

A skill is a reusable instruction pack in a directory with a `SKILL.md`. A skill that one namespace uses is an owned skill at `agents/<ns>/skills/<name>/SKILL.md`, bound to that namespace by location: the base agent `<ns>` and every variant `<ns>:<variant>` get it. A skill that two or more namespaces use is a shared skill at `skills/<name>/SKILL.md`, bound to them by `domains:`. When it activates — preloaded, auto-activated by its rules, or loaded with `skill(action="use")` or `/skill <name>` — its body is injected into the session's context. Skills don't define a role or model; they add focused knowledge to the agent they are bound to, and can bring the tools that knowledge needs. Each specialty of a field is a skill, owned by that field's agent unless other agents apply it too. A skill is addressed by its bare name in workflows, `OCTOMIND_SKILLS` and `/skill use`, so the name exists once in the tap.

## Mental model

A skill is a checklist for a model that already knows the field. Anthropic's skill guidance starts from "Claude is already very smart — only add context Claude doesn't already have." Every token ships on every activation, so the body carries decisions, conventions, and gates, not textbook background. Activation is decided by the frontmatter (`domains` plus `rules`), so the frontmatter is as much a part of the design as the body.

## Rules

### Directory structure

```
agents/<ns>/skills/<skill-name>/      (owned) or skills/<skill-name>/   (shared)
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
domains: developer devops
rules:
  - content(rust)
  - file(Cargo.toml) match((?i)\b(compil\w+|panic\w*|\w+\.rs)\b)
---
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | yes | ≤64 chars, lowercase letters, digits, hyphens; no leading/trailing hyphen; equals the directory name |
| `title` | yes (tap lint) | 5–60 chars |
| `description` | yes | 20–1024 chars, third person, what it does plus when to use it with concrete trigger terms |
| `domains` | shared skills only | Space-separated or array of two or more agent namespaces; each value must have an `agents/<name>/default.toml` (`DOMAIN_UNKNOWN`); one name fails `SHARED_SKILL_SINGLE_DOMAIN` (move the skill under that namespace); an owned skill must not set it (`OWNED_SKILL_HAS_DOMAINS`); the runtime also accepts `*` for every agent, but tap lint rejects it |
| `rules` | for auto-activation | List of rule expressions, below |
| `capabilities` | optional | Capabilities enabled when the skill activates; each must exist under `capabilities/` (lint) |
| `compatibility` | optional | ≤500 chars, environment only (tools, OS, network) |
| `license`, `metadata`, `allowed-tools` | optional | `allowed-tools` is space-separated; missing tools are reported as an incompatibility |

The runtime parser reads `name`, `description`, `compatibility`, `license`, `allowed-tools`, `capabilities`, `domains`, and `rules`; a skill without `name` or `description` is skipped. Without both `domains` and `rules`, a skill is manual-only.

### Auto-activation rules

Rules are evaluated on fresh user messages when `[skills] auto_activation` is on and the session's agent is in `domains`. Each `- ` item is an OR branch; several expressions on one line are ANDed.

| Expression | Matches when |
|------------|--------------|
| `file(<path or glob>)` | Path exists in the workdir, or the glob matches (`*.rs`, `src/**/*.go`) |
| `content(<word>)` | User message contains the word (whole word, case-insensitive) |
| `match(<regex>)` | User message matches the regex (nested parentheses are fine) |
| `grep(<pattern>[, <glob>])` | A gitignore-respecting workdir file contains the pattern; the glob filters by file name only (`*.toml`, not `src/**/*.rs`) |
| `env(<VAR>)` / `env(<VAR>=<value>)` | Variable set and non-empty / equals value |
| `bin(<command>)` | Command found on `PATH` |
| `workdir(<text>)` | Working-directory path contains the text (case-insensitive) |
| `session(<text>)` | Session name contains the text (case-insensitive). Default names are `YYMMDD-<dir>-HHMM-<id>`; `tap run` sessions are `tap-<agent name>-<hex>`, so a session check cannot tell specialties apart. Tap skills use message checks instead |
| `semantic(<phrase>[, <threshold>])` | Embedding cosine between the message and the phrase clears the threshold (default 0.68) |

Deterministic matches activate directly. Semantic-only candidates must also beat the runner-up by a 0.05 margin, so near-ties abstain. Adding or changing `semantic(...)` phrases changes the tap embedding model's training data — see the `tap-model-training` skill.

A skill loads only when the request shows the work. Every rule line carries at least one check on the message (`content`, `match` or `semantic`); `file`, `grep`, `bin`, `env` and `workdir` only narrow a line, because on their own they fire in every session in a matching repo, whatever the user asked. Lint enforces this (`RULE_NO_INTENT`) and rejects unknown check types (`RULE_UNKNOWN_CHECK`), which the runtime would silently ignore. Single common words (`review`, `cost`, `pdf`, `node`) fire on passing mentions; use a phrase or a `match()` that needs the task verb.

### Validate script

`validate` in the skill directory runs at the end of each assistant turn while the skill is active, only when `[skills] auto_validation = true` (default `false`), and only for skills that come from a tap. Contract: argv[1] is `assistant`, the final assistant message arrives on stdin, cwd is the project workdir. A non-zero exit with non-empty stderr counts as a failure and the stderr is fed back to the model; retries per skill are capped by `[skills] max_retries`, timeout by `validation_timeout`. Make it executable.

### Body structure

Fixed section order, U-shaped for attention: the opening and the closing get read most carefully, the middle relies on headers as anchors.

```
## Overview              why and when (2–4 sentences)
## Mental model          governing principles
## Rules                 tables, bullets, decision guides
## Examples              bad → good pairs
## Checklist             verifiable gates before shipping
## Composition / References   sibling skills bound to the same agent, sources
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

Reserve all-caps for one or two genuine safety hard-stops. Full guidance: `agents/assistant/skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

### Skills that carry a specialty

A specialty is a procedure for one kind of task in a field, such as QA test planning, contract review for one jurisdiction or lifecycle email. It is a skill bound to the field's agent.

- A shared skill's `domains:` names the agents, for example `domains: developer devops`. An owned skill has no `domains:` line.
- `capabilities:` lists tools only this specialty needs. They load when the skill activates, so the agent's manifest does not declare them.
- `rules:` are message-based: a `match()` on the verbs and nouns of the task, or a `semantic()` phrase, so the skill loads when the request shows the work and not on passing mentions.
- The body holds the full procedure and the output contract: the steps, the decision rules, the shape and file path of the deliverable, and the checks before reporting done. The agent prompt does not repeat them.
- A workflow step that depends on the specialty preloads it with `skills = [...]`; it does not rely on the rules matching.

Test the rules against the intended prompts, against close requests that should not load the skill, and against a neutral prompt.

### Domain isolation

- Bind a skill to one agent wherever possible: put it under the agent that owns the deliverable. Use `domains:` only when two or more agents apply the same procedure.
- `compatibility:` describes the environment, never pairings with agents.
- The body never names other agents; describe downstream work as owned by another field. Sibling skills bound to the same agent may be named sparingly.

### Creation workflow

1. Identify the knowledge the model lacks: conventions, decision rules, gates.
2. Pick a specific name (`rust-error-handling`, not `rust`).
3. Copy `templates/skill.md`; write frontmatter, then the body in canonical order.
4. Place the skill: under the one agent that uses it, or in `skills/` with `domains:` for two or more. Add `rules` only if it should auto-activate; test that the rules match the intended prompts and nothing broader.
5. Optionally add `validate`.
6. Run `bash scripts/lint-skills.sh <skill dir>`; test with `/skill <name>` in a session.

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
description: "Rust idioms, error handling, async patterns. Auto-activates when Rust work is asked for in a Rust project."
domains: developer devops
rules:
  - match((?i)\b(compil\w+|panic\w*|\w+\.rs)\b) file(Cargo.toml)
  - grep(tokio, Cargo.toml) content(async)
  - semantic(write idiomatic rust code)
---
```

### Example 3: common mistakes

❌ `# Git Workflow` as the first body line — lint fails with `BODY_HAS_REDUNDANT_H1`.

❌ `grep(async_trait, src/**/*.rs)` — the glob is matched against file names only, so it never matches. Use `grep(async_trait, *.rs)`.

❌ `domains: dev developer` — `dev` is not an agent name, so lint fails (`DOMAIN_UNKNOWN`) and it would never activate.

❌ `- file(Cargo.toml)` on its own line — loads the skill for every request in a Rust repo, even "summarize the changes"; lint fails with `RULE_NO_INTENT`. Add a message check on the same line.

## Checklist

- [ ] Description in third person, says what and when, with concrete trigger terms?
- [ ] `name` equals the directory and exists once in the tap; an owned skill has no `domains`, a shared skill's `domains` names two or more existing agents; `capabilities` names existing capabilities?
- [ ] Rules match the intended prompts and nothing broader; every line has a message check; semantic phrases one idea each?
- [ ] Body in canonical order, no H1, bold, italics, or `---`; under ~2000 words?
- [ ] Instructions actionable and specific; examples for non-obvious rules?
- [ ] Tone calibrated: plain directives, all-caps only for real hard-stops?
- [ ] Cited `reference/` files exist; `validate` executable if present?
- [ ] `bash scripts/lint-skills.sh <skill dir>` passes?

## Composition / References

- `templates/skill.md` — canonical skill template
- `tap-model-training` — retrain after changing `semantic(...)` phrases
- [AgentSkills specification](https://agentskills.io/specification)
- [Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
