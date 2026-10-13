---
name: tap-agent-authoring
title: "Agent Manifest Authoring"
description: "Guide for writing Octomind agent manifests: TOML format, required and forbidden fields, capability tiers, system prompt structure and tone for current models, sampling and model settings, placeholders, lint rules, and the pre-write checklist. Activate when creating or editing agents/<domain>/<spec>.toml files."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-manifests.sh and bin/load."
domains: octomind
---

## Overview

This skill encodes what a correct, high-quality `agents/<domain>/<spec>.toml` needs: the exact TOML shape, which fields are required or forbidden, how to structure and phrase the system prompt for current models, how sampling settings actually reach the model, and the checks that must pass before the manifest ships. Use it whenever you create or edit an agent manifest.

## Mental model

A manifest is `capabilities` plus exactly one `[[roles]]`. Capabilities decide the tool surface (`bin/load` and the runtime merge each capability's provider file into `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]`); the role decides behaviour. The system prompt is sent on every request and cached, so it must be stable, short, and structural: identity and rules live in `system`, reference material lives in skills loaded on demand.

## Rules

### Manifest format

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Title: Short Agent Title (5–60 chars)
# Description: What this agent does (20–160 chars).

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-python"]

[[roles]]
system = """
<XML-tagged system prompt — see below>
"""
welcome = "<Emoji> <Short greeting>. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0
# model = "<provider>:<model>"   # optional override
```

| Field | Rule |
|-------|------|
| `# Agent:`, `# Title:`, `# Description:` | Required header comments; title 5–60 chars, description 20–160 |
| `capabilities` | Required at top level; the only way to wire tools. Bare name = default provider, `name:provider` = explicit |
| `system` | Required; XML blocks in canonical order |
| `welcome` | Required; first message shown; emoji plus `{{CWD}}` |
| `temperature`, `top_p`, `top_k` | Required by lint; see Sampling below |
| `model` | Optional `provider:model` override for this agent |
| `name`, `[deps]`, `[roles.mcp]`, `[[mcp.servers]]` | Forbidden — injected from the tag and from capability files |

File path matches the tag (`developer:rust` → `agents/developer/rust.toml`), exactly one `[[roles]]`, sub-specs use hyphens (`developer:rust-nightly`).

### Capability tiers

- `core` — every agent.
- Domain capabilities (`shell`, `filesystem-*`, `codesearch-*`, `websearch`, ...) — what the role actually needs, nothing speculative.
- `agent` — sub-orchestrators delegating to their own configured agents.
- `orchestration` (`tap`, `schedule`, `monitor`) — only agents that genuinely route across domains.
- `runtime` (`mcp`, `agent`, `skill`, `capability`) — high-trust agents that reconfigure the tool surface.

A narrow specialist never declares `orchestration` or `runtime`; the unwanted server is then physically absent from its context. Domain capabilities beyond the manifest can still auto-activate on intent at runtime.

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
- `<scope>` — required when siblings exist. Describe out-of-scope work by what it is, not by naming agents from other domains.
- `<workflow>` — numbered steps, one sentence each plus optional sub-bullets.
- `<rules>` — tables and bullets; prose only when the why is non-obvious.
- `<output_format>` — exact artifact shape; name file path patterns if the agent writes files.
- `<critical>` — short Don't/Do bullets, no explanations, no theatre.

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
| `{{ROLE}}`, `{{SHELL}}`, `{{OS}}`, `{{GIT_STATUS}}`, `{{README}}`, ... | Expand in both, but anything that changes per session or project breaks caching in `system` |
| `{{INPUT:KEY}}`, `{{ENV:KEY}}` | Capability files, not prompts — credentials and env vars |

### Sampling and model settings

The runtime folds `temperature`, `top_p`, and `top_k` into the role's model override and the provider layer sends only what the target model accepts. On the `anthropic:` provider, Claude Opus 4.7 and later, the Claude 5 family, and any request with thinking on (the default `reasoning_effort` is `medium`) get no sampling parameters at all — the API rejects non-default values, so octolib omits them. Several Claude 4.x models reject `top_p`; it is dropped there. OpenAI reasoning models (o-series, GPT-5 and later) reject `temperature`/`top_p` as well, and octolib drops them there too.

So the fields are required, but on current Claude models behaviour comes from the prompt, not the sampler. Set conservative values for the models that still honour them:

| Domain | temperature | top_p | top_k |
|--------|-------------|-------|-------|
| Developer, DevOps, security | 0.1–0.2 | 0.9 | 0 |
| Medical, legal, finance | 0.15–0.2 | 0.9 | 0 |
| General assistant | 0.3 | 0.9 | 0 |
| Content, creative | 0.4–0.7 | 0.9 | 0 |

`top_k = 0` disables it. Use `model` only when the agent genuinely needs a specific model; otherwise let the user's config and `[taps]` decide.

### Lint rules that bite

- No `{{CWD}}`, `{{DATE}}`, or `{{SYSTEM}}` in `system`.
- No tap-relative paths (`skills/…`, `capabilities/…`, `deps/…`) in `system` or `welcome` — agents run in the user's project, not the tap checkout. The `octomind` domain is exempt.
- Every `` `name` skill `` mention must exist at `skills/<name>/SKILL.md`.
- Every capability needs `capabilities/<name>/default.toml`.

### Required disclaimers

Medical, legal, and financial agents state their limits plainly in `<critical>` or `<identity>`: not a doctor and cannot diagnose or prescribe; not a licensed attorney, legal information only; not financial advice.

### Multi-step pipelines

Manifests do not define pipelines. Multi-step orchestration is the external `octomind workflow <file.toml>` CLI (sequential, parallel, loop, conditional, graph); load the `octomind-workflow` skill for its syntax. `[[layers]]` and `[[commands]]` exist only in a user's local config, delegating to a role via `command = "octomind acp <role>"`.

## Examples

### Example 1: minimal correct agent

```toml
# agents/developer/rust.toml
# Agent: developer:rust
# Title: Rust Developer
# Description: Expert Rust developer. Writes idiomatic, safe, performant Rust code.

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
temperature = 0.1
top_p = 0.9
top_k = 0
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

- [ ] Header comments present with valid lengths; path matches tag?
- [ ] Every needed capability exists; tiers respected (no `orchestration`/`runtime` on a specialist)?
- [ ] XML blocks in canonical order, `<identity>` first, `<critical>` last and short?
- [ ] Tone calibrated: plain `Use X when …`, explicit asks, all-caps only for real hard-stops?
- [ ] No `{{CWD}}`/`{{DATE}}`/`{{SYSTEM}}`, headers, or bold in `system`; under ~1500 words?
- [ ] Reference material moved to skills; every named skill exists?
- [ ] Sampling fields set conservatively, behaviour driven by the prompt?
- [ ] `bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml` passes and `bin/load <domain>:<spec>` resolves?

## References

- `templates/agent.toml` — canonical agent template
- `agents/developer/general.toml` — execution-protocol reference
- `bin/load <domain>:<spec>` — print the merged manifest
- `skills/prompt-engineering/SKILL.md` — prompt theory across agents and skills
- [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
