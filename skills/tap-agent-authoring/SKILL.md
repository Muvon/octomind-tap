---
name: tap-agent-authoring
title: "Agent Manifest Authoring"
description: "Write Octomind agent manifests: TOML fields, capability tiers, system prompt structure, model settings, lint rules. Use when editing agents/*.toml."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-manifests.sh and bin/load."
domains: octomind assistant
---

## Overview

This skill encodes what a correct, high-quality `agents/<name>.toml` needs: the exact TOML shape, which fields are required or forbidden, how to structure and phrase the system prompt for current models, how sampling settings actually reach the model, and the checks that must pass before the manifest ships. Use it whenever you create or edit an agent manifest.

## Mental model

A manifest is `capabilities` plus exactly one `[[roles]]`. Capabilities decide the tool surface (`bin/load` and the runtime merge each capability's provider file into `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]`); the role decides behaviour. The system prompt is sent on every request and cached, so it must be stable, short, and structural: identity and rules live in `system`, reference material lives in skills loaded on demand.

There is one agent per field of work, for example `developer`, `writer` or `lawyer`. The agent does that field's work itself. Its prompt is short: the role, the scope, the working method every task in the field shares, the guards, and the output conventions.

A specialty is a procedure for one kind of task inside the field, such as QA test planning or contract review for one jurisdiction. It is not a second agent. It is a skill at `skills/<name>/SKILL.md` whose `domains:` names the agent. The skill loads when the user's message matches its `rules:`, when a workflow step lists it in `skills`, or when it is preloaded from the environment or by hand. A tool that only one specialty needs is declared by that skill through `capabilities:`, not by the agent. Load `tap-skill-authoring` to write such a skill.

Put in the agent prompt only what applies to every task of the field. Put a procedure, a checklist or an output contract that applies to one kind of task into a skill. Use a literal skill name in the system prompt when the skill itself is being authored or inspected, or when an exact manual reference is part of the deliverable contract.

Keep shared decisions in one session. A delegate gets the evidence and the output contract it needs to make its own decision.

## Rules

### Manifest format

```toml
# agents/<name>.toml
# Agent: <name>
# Title: Short Agent Title (5–60 chars)
# Description: What this agent does and returns (120–155 chars).

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-python"]

[[roles]]
system = """
<XML-tagged system prompt — see below>
"""
welcome = "<Emoji> <Short greeting>. Working in {{CWD}}"
# model = "<provider>:<model>"   # optional override
```

| Field | Rule |
|-------|------|
| `# Agent:`, `# Title:`, `# Description:` | Required header comments; title 5–60 chars, description 120–155; no `# Default:` header exists |
| `# Uses:` | Optional header, see Delegation below |
| `capabilities` | Required at top level; the only way to wire tools. Bare names only — `default.toml` picks the provider; users override it in their own `[capabilities]` config |
| `system` | Required; XML blocks in canonical order |
| `welcome` | Required; first message shown; emoji plus `{{CWD}}` |
| `temperature`, `top_p`, `top_k` | Deprecated; octomind ignores them and sends no sampling parameters, so do not set them |
| `model` | Optional `provider:model` override for this agent |
| `name`, `[deps]`, `[roles.mcp]`, `[[mcp.servers]]` | Forbidden — injected from the tag and from capability files |

The file is `agents/<name>.toml` with no subdirectory and no symlink. The tag is the file name: lowercase letters, digits and hyphens, starting with a letter, no `:`. The `# Agent:` header repeats the name. The manifest has exactly one `[[roles]]`. `octomind run <name>` starts the agent. A role with the same name in the user's local config takes priority over the tap agent. There is no README file per agent.

The `# Title:` and `# Description:` lines are what `tap` compares a task brief against when it picks an agent, so they say what the agent takes in and what it returns.

### Capability tiers

- `core` — every agent.
- Domain capabilities (`shell`, `filesystem-*`, `codesearch-*`, `websearch`, ...) — what the role actually needs, nothing speculative.
- `agent` (`agent_*`) — agents that run their own configured sub-agents; only `assistant` declares it.
- `orchestration` (`tap`, `schedule`, `monitor`) — agents that start copies of themselves or hand tasks to other agents; see Delegation.
- `runtime` (`mcp`, `agent`, `skill`, `capability`) — reconfigures the tool surface; only `octomind` declares it.

An agent that has no delegation job does not declare `orchestration`, `agent` or `runtime`; the unwanted server is then absent from its context. Capabilities beyond the manifest can still load at runtime: on intent, or through a skill's `capabilities:`.

### System prompt structure

XML-tagged blocks in a fixed U-shape order. Anthropic recommends XML tags to separate instructions, context, examples, and inputs; the start and end of a long prompt get the most attention, so identity goes first and the tight rule list last.

```
<identity>          who/what, expertise, style (3–5 lines)
<voice>             tone and register (omit for technical agents)
<scope>             what is owned / what is out of scope
<workflow>          numbered steps
<rules>             tables, decision matrices, domain knowledge
<examples>          bad → good pairs (omit if N/A)
<output_format>     artifact shape, file paths, schemas
<interaction>       trigger → response patterns
<critical>          brief Don't/Do list in plain language
```

Block rules:

- `<identity>` — one paragraph, nothing before it.
- `<scope>` — what the agent covers and what it does not. Describe out-of-scope work by what it is; for work outside the field, point the user to the global assistant (`octomind run` with no agent).
- `<workflow>` — numbered steps, one sentence each plus optional sub-bullets.
- `<rules>` — tables and bullets; prose only when the why is non-obvious.
- `<output_format>` — exact artifact shape; name file path patterns if the agent writes files.
- `<critical>` — short Don't/Do bullets, no explanations, no theatre.

### Delegation

An agent that declares `orchestration` can start copies of itself with `tap`. Each copy is a fresh session of the same agent; a copy cannot start further copies. A copy started with `readonly: true` can only use tools marked read-only, so it can scout a large change before it is made or review finished work independently. Several writable copies can run at once for independent parts, each on its own files. Write when to delegate, what evidence and constraints belong in the handoff, and what the agent must verify afterwards. The delegation tool documents its own actions and parameters.

An agent reaches other agents only through the `# Uses:` header, placed next to `# Title:` and `# Description:`. It is a comma-separated list of agent names, or `*` for every other agent. `tap` then matches a task brief against the `# Title:` and `# Description:` of each listed agent. An agent with the header must declare `orchestration`. Entries must be existing agent names, unique, not the agent itself, and must form no loop between agents. In this tap only `assistant` carries the header, as `# Uses: *`; it is the one agent that hands tasks across fields.

Prompt lines for an agent that has the header (the agents themselves are not listed; the runtime matches the brief):

```
You may hand a task only to the agents your `# Uses:` header declares.
Give the other agent a self-contained brief with the requested deliverable, verified evidence, constraints and acceptance checks.
```

Do not put `{{SPECIALISTS}}` or `{{USES}}` in `system`: lint rejects them (`SPECIALISTS_REMOVED`, `USES_PLACEHOLDER_REMOVED`).

### Tone for current models

Current Claude models are trained for precise instruction following and are more responsive to the system prompt than older generations. Anthropic's guidance: language written to stop under-triggering now over-triggers, so dial it back; and say explicitly what you want, because a vague request gets a literal reading.

- `CRITICAL: YOU MUST use tool X when …` → `Use tool X when …`
- `🚨 HARD RULES` + stacked `NEVER` bullets → `<critical>` with plain `Don't …` / `Do …`
- `If in doubt, use X` → state when X applies
- "Suggest changes" when you mean edits → "Make the changes"

Reserve all-caps for one or two genuine safety hard-stops (`Never force-push to main`). The substance test: drop the emphasis and lowercase the line — if it still makes sense, keep it soft; if it reads as filler, cut it. More detail: `skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

### Token and markdown discipline

- Target 200–1000 words. `lint-manifests.sh` warns above 1500 (`SYSTEM_LENGTH_WARN`) and fails above 3000 (`SYSTEM_TOO_LONG`).
- No reference documentation (CLI listings, config schemas, API tables) in `system` — move it to a skill and name the skill.
- The XML tag is the structure: no `#`/`##` headers (lint fails), `###` only when a block has two or more genuine sub-areas, no bold (lint fails), no `---` separators.
- Keep tables, code fences, and numbered lists — they carry structure.

### Placeholders

The system prompt must be identical run to run so the provider can cache it (cache reads bill at roughly a tenth of the input price).

| Placeholder | Where |
|-------------|-------|
| `{{CWD}}`, `{{DATE}}`, `{{SYSTEM}}` | `welcome` only — lint fails if they appear in `system` |
| `{{SPECIALISTS}}`, `{{USES}}`, `{{DOMAINS}}` | Not expanded; lint rejects them in `system` |
| `{{ROLE}}`, `{{SHELL}}`, `{{OS}}`, `{{GIT_STATUS}}`, `{{README}}`, ... | Expand in both, but anything that changes per session or project breaks caching in `system` |
| `{{INPUT:KEY}}`, `{{ENV:KEY}}` | Capability files, not prompts — credentials and env vars |

### Model setting

Use `model` only when the agent genuinely needs a specific model; otherwise let the user's config decide.

### Lint rules that bite

- No `{{CWD}}`, `{{DATE}}`, or `{{SYSTEM}}` in `system`.
- No tap-relative paths (`skills/…`, `capabilities/…`, `deps/…`) in `system` or `welcome` — agents run in the user's project, not the tap checkout. The `octomind` agent is exempt.
- Every `` `name` skill `` mention must exist at `skills/<name>/SKILL.md`.
- Every capability needs `capabilities/<name>/default.toml`.
- The path is `agents/<name>.toml` (`AGENT_PATH`, `AGENT_SUBDIR`, `AGENT_SYMLINK`, `AGENT_NAME_INVALID`), and the `# Agent:` header matches the file name (`MISSING_AGENT_HEADER`, `AGENT_HEADER_MISMATCH`).
- No `{{SPECIALISTS}}` (`SPECIALISTS_REMOVED`), `{{USES}}` (`USES_PLACEHOLDER_REMOVED`) or `{{DOMAINS}}` (`DOMAINS_REMOVED`) in `system`; no `# Default:` header (`DEFAULT_HEADER_REMOVED`).
- `# Uses:` entries are `*` or existing agent names, unique, not the agent itself (`USES_INVALID`, `USES_UNKNOWN`, `USES_CYCLE`), and an agent with the header declares `orchestration` (`USES_NO_ORCHESTRATION`).

### Required disclaimers

Medical, legal, and financial agents state their limits plainly in `<critical>` or `<identity>`: not a doctor and cannot diagnose or prescribe; not a licensed attorney, legal information only; not financial advice.

### Multi-step pipelines

Manifests do not define pipelines. Multi-step orchestration is the external `octomind workflow <file.toml>` CLI (sequential, parallel, loop, conditional, graph); load the `octomind-workflow` skill for its syntax. `[[commands]]` exists only in a user's local config, delegating to a role via `command = "octomind acp <role>"`.

## Examples

### Example 1: minimal correct agent

```toml
# agents/rustacean.toml
# Agent: rustacean
# Title: Rust Developer – Idiomatic, Safe Code
# Description: Writes, reviews and debugs Rust: ownership, async with tokio, error handling, FFI and Cargo. Runs check, clippy and tests before it reports the work.

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-rust"]

[[roles]]
system = """
<identity>
Expert Rust developer. You write idiomatic, safe, performant Rust — borrow-checker friendly, no unsafe unless justified in a comment.
</identity>

<scope>
Own: Rust code, Cargo workflows, async with tokio, error handling, FFI signatures.
Don't own: infrastructure and deployment.
</scope>

<workflow>
1. Read context — `Cargo.toml`, surrounding modules.
2. Outline non-trivial changes before writing.
3. Write — iterators over index loops, `Result` over panic.
4. Verify — `cargo check`, `cargo clippy -- -D warnings`, `cargo test`.
</workflow>

<rules>
- Errors: `thiserror` for libraries, `anyhow` for binaries.
- Async: tokio; don't mix runtimes.
</rules>

<interaction>
- Ambiguous spec → ask one clarifying question, then proceed.
</interaction>

<critical>
- Don't add `unsafe` without a SAFETY comment naming the invariant.
- Don't use `unwrap()` in production paths.
- Don't silence clippy — fix the cause.
</critical>
"""
welcome = "🦀 Rust developer ready. Working in {{CWD}}"
```

### Example 2: forbidden fields

```toml
# ❌ WRONG — these belong in capability files
[deps]
require = ["muvon/octofs"]

[roles.mcp]
server_refs = ["octofs"]
```

### Example 3: dynamic context in system

❌ `system = """<identity>Assistant working in {{CWD}} on {{DATE}}.</identity>"""`

✅ `welcome = "👋 Ready. Working in {{CWD}}"` and a stable `system`.

What changed: the system prompt is cacheable again and lint passes.

## Checklist

- [ ] Header comments present with valid lengths; path matches the `# Agent:` name?
- [ ] Every needed capability exists; `orchestration` only where the agent delegates, `runtime` only in `octomind`?
- [ ] A `# Uses:` header, if present, lists existing agents and comes with `orchestration`?
- [ ] A procedure for one kind of task sits in a skill bound to this agent, not in the prompt?
- [ ] XML blocks in canonical order, `<identity>` first, `<critical>` last and short?
- [ ] Tone calibrated: plain `Use X when …`, explicit asks, all-caps only for real hard-stops?
- [ ] No `{{CWD}}`/`{{DATE}}`/`{{SYSTEM}}`, headers, or bold in `system`; under ~1500 words?
- [ ] Reference material moved to skills; every named skill exists?
- [ ] Deprecated sampling fields absent?
- [ ] `bash scripts/lint-manifests.sh agents/<name>.toml` passes and `bin/load <name>` resolves?

## References

- `templates/agent.toml` — canonical agent template
- `agents/developer.toml` — execution-protocol reference
- `bin/load <name>` — print the merged manifest
- `skills/prompt-engineering/SKILL.md` — prompt theory across agents and skills
- [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
