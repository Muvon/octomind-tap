---
name: tap-agent-authoring
title: "Agent Manifest Authoring"
description: "Write Octomind agent manifests: TOML fields, capability tiers, system prompt structure, model settings, lint rules. Use when editing agents/*/*.toml."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-manifests.sh and bin/load."
domains: octomind
---

## Overview

This skill encodes what a correct, high-quality `agents/<domain>/<spec>.toml` needs: the exact TOML shape, which fields are required or forbidden, how to structure and phrase the system prompt for current models, how sampling settings actually reach the model, and the checks that must pass before the manifest ships. Use it whenever you create or edit an agent manifest.

## Mental model

A manifest is `capabilities` plus exactly one `[[roles]]`. Capabilities decide the tool surface (`bin/load` and the runtime merge each capability's provider file into `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]`); the role decides behaviour. The system prompt is sent on every request and cached, so it must be stable, short, and structural: identity and rules live in `system`, reference material lives in skills loaded on demand.

Keep one recognizable deliverable or decision in each specialist. Put reusable procedures and decision rules in focused skills. Use workflow steps to bind inputs, skills, and checks. Keep shared decisions in one session and give any delegate the evidence and output contract needed to make its own decision.

Describe the task and its essential guardrails in the role. Use domain-scoped skill rules for optional augmentation and explicit workflow preloads for required procedures. Use a literal skill name in the system prompt when the skill itself is being authored or inspected, or when an exact manual reference is part of the deliverable contract.

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
# model = "<provider>:<model>"   # optional override
```

| Field | Rule |
|-------|------|
| `# Agent:`, `# Title:`, `# Description:` | Required header comments; title 5–60 chars, description 20–160 |
| `chief` file name | `agents/<domain>/chief.toml` is the domain's orchestrator, the agent `octomind run <domain>` starts. No `# Default:` header exists |
| `capabilities` | Required at top level; the only way to wire tools. Bare names only — `default.toml` picks the provider; users override it in their own `[capabilities]` config |
| `system` | Required; XML blocks in canonical order |
| `welcome` | Required; first message shown; emoji plus `{{CWD}}` |
| `temperature`, `top_p`, `top_k` | Deprecated; octomind ignores them and sends no sampling parameters, so do not set them |
| `model` | Optional `provider:model` override for this agent |
| `name`, `[deps]`, `[roles.mcp]`, `[[mcp.servers]]` | Forbidden — injected from the tag and from capability files |

File path matches the tag (`developer:rust` → `agents/developer/rust.toml`), exactly one `[[roles]]`, sub-specs use hyphens (`developer:rust-nightly`).

The `# Description:` line is also the entry the domain's `chief` shows for this agent, so it says what the agent takes in and what it returns.

### Capability tiers

- `core` — every agent.
- Domain capabilities (`shell`, `filesystem-*`, `codesearch-*`, `websearch`, ...) — what the role actually needs, nothing speculative.
- `agent` — sub-orchestrators delegating to their own configured agents.
- `orchestration` (`tap`, `schedule`, `monitor`) — each domain's `chief`, which delegates inside its own domain (`assistant:chief`, the global assistant, reaches every domain).
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

Chief agent blocks:

- Do not put `{{SPECIALISTS}}` or `{{USES}}` in `system`. Octomind 0.71 and older expanded them to lists of agents; newer octomind does not expand them, and lint rejects them (`SPECIALISTS_REMOVED`, `USES_PLACEHOLDER_REMOVED`). The `chief` names no specialist.
- Describe when to delegate, what evidence and constraints belong in the handoff, and what the chief must verify. The delegation tool documents its own actions and parameters. Write each agent's `# Title:` and `# Description:` in the terms a task brief would use for the work and deliverable. The runtime matches the brief within the chief's domain and its declared reach.
- Name no other domain's agent tag in `system` or `welcome`. Only `assistant:chief` routes across all domains: it declares `# Uses: *`, which stands for every other domain that has a `chief`.

A chief can reach other domains or single agents it declares. Put one header comment next to `# Title:` and `# Description:`: `# Uses: <entry>[, <entry>…]`, where an entry is a bare domain (`content`, meaning that domain's `chief`) or a full tag (`seo:audit`, meaning that agent). The header alone makes them reachable; it is validated at load and bounds which agents the runtime can match for this chief. Only a `chief` may carry the header, it needs `orchestration`, and it must not list its own domain (its agents are reachable without it), write `<domain>:chief` (write the bare domain), or form a loop with another lead.

```toml
# agents/marketing/chief.toml
# Uses: content, seo:audit
```

Prompt lines to copy into `<scope>` or `<rules>` of a chief that has the header (the agents themselves are not listed; the runtime matches the brief):

```
Outside your domain you may reach only the domains and agents your `# Uses:` header declares.
Give the specialist a self-contained brief with the requested deliverable, verified evidence, constraints and acceptance checks.
```

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
| `{{SPECIALISTS}}`, `{{USES}}` | Removed: not expanded in newer octomind (lists of agents in 0.71 and older); lint rejects them in `system` |
| `{{ROLE}}`, `{{SHELL}}`, `{{OS}}`, `{{GIT_STATUS}}`, `{{README}}`, ... | Expand in both, but anything that changes per session or project breaks caching in `system` |
| `{{INPUT:KEY}}`, `{{ENV:KEY}}` | Capability files, not prompts — credentials and env vars |

### Model setting

Use `model` only when the agent genuinely needs a specific model; otherwise let the user's config and `[taps]` decide.

### Lint rules that bite

- No `{{CWD}}`, `{{DATE}}`, or `{{SYSTEM}}` in `system`.
- No tap-relative paths (`skills/…`, `capabilities/…`, `deps/…`) in `system` or `welcome` — agents run in the user's project, not the tap checkout. The `octomind` domain is exempt.
- Every `` `name` skill `` mention must exist at `skills/<name>/SKILL.md`.
- Every capability needs `capabilities/<name>/default.toml`.
- Every domain with two or more agents has a `chief` that declares `orchestration`; no `{{SPECIALISTS}}` (`SPECIALISTS_REMOVED`) or `{{USES}}` (`USES_PLACEHOLDER_REMOVED`) in `system`; no foreign domain tag in a `chief`; no `# Default:` header; `{{DOMAINS}}` no longer exists (`DOMAINS_REMOVED`: the global assistant declares `# Uses: *`). A `# Uses:` header goes only in a `chief` (`USES_MISPLACED`); entries are valid, unique, outside the chief's own domain, not `<domain>:chief`, and `*` only in `assistant:chief` (`USES_INVALID`), exist (`USES_UNKNOWN`) and form no loop between leads (`USES_CYCLE`).

### Required disclaimers

Medical, legal, and financial agents state their limits plainly in `<critical>` or `<identity>`: not a doctor and cannot diagnose or prescribe; not a licensed attorney, legal information only; not financial advice.

### Multi-step pipelines

Manifests do not define pipelines. Multi-step orchestration is the external `octomind workflow <file.toml>` CLI (sequential, parallel, loop, conditional, graph); load the `octomind-workflow` skill for its syntax. `[[commands]]` exists only in a user's local config, delegating to a role via `command = "octomind acp <role>"`.

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
- [ ] A domain with two or more agents has a `chief` that declares `orchestration`, delegates inside its domain, names no other domain's tag?
- [ ] XML blocks in canonical order, `<identity>` first, `<critical>` last and short?
- [ ] Tone calibrated: plain `Use X when …`, explicit asks, all-caps only for real hard-stops?
- [ ] No `{{CWD}}`/`{{DATE}}`/`{{SYSTEM}}`, headers, or bold in `system`; under ~1500 words?
- [ ] Reference material moved to skills; every named skill exists?
- [ ] Deprecated sampling fields absent?
- [ ] `bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml` passes and `bin/load <domain>:<spec>` resolves?

## References

- `templates/agent.toml` — canonical agent template
- `agents/developer/general.toml` — execution-protocol reference
- `bin/load <domain>[:<spec>]` — print the merged manifest (a bare domain loads `<domain>:chief`)
- `skills/prompt-engineering/SKILL.md` — prompt theory across agents and skills
- [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
