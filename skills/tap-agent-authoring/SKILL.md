---
name: tap-agent-authoring
title: "Agent Manifest Authoring"
description: "Deep guide for writing Octomind agent manifests: TOML format, required fields, system prompt structure, temperature guidelines, workflow/layer patterns, and the pre-write checklist. Activate when creating or editing agents/<domain>/<spec>.toml files."
license: Apache-2.0
compatibility: "Requires: octomind-tap repo. Use alongside tap-capability-authoring for capability creation."
domains: octomind
---

## Overview

This skill encodes everything needed to write a correct, high-quality `agents/<domain>/<spec>.toml` file for the octomind-tap registry. It covers the exact TOML format, required and forbidden fields, how to write effective system prompts, temperature/top_p guidelines by domain, workflow and layer patterns for multi-step pipelines, and the pre-write checklist.

Use this skill whenever you are creating or editing an agent manifest.

## Instructions

### Agent Manifest Format

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Title: Short Agent Title (5–60 chars)
# Description: What this agent does (20–160 chars).

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-python"]

[[roles]]
system = """
<XML-tagged system prompt — see "System Prompt Structure" below>
"""
welcome = "<Emoji> <Short greeting>. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0

# Optional model override:
# model = "openrouter:anthropic/claude-sonnet-4"
```

### Required Fields

| Field | Notes |
|-------|-------|
| `# Title:` | Comment. Short human-readable label. 5–60 chars. |
| `# Description:` | Comment. What the agent does. 20–160 chars. |
| `capabilities` | Top-level, always first. The ONLY way to wire tools. |
| `system` | The system prompt — agent's identity, rules, domain knowledge. |
| `welcome` | First message shown to user. Include emoji + `{{CWD}}`. |
| `temperature` | 0.1–0.2 for precise tasks, 0.3–0.5 for balanced, 0.6–0.8 for creative. |
| `top_p` | Typically 0.2 (precise) to 0.9 (creative). |
| `top_k` | 0 or 10 for most agents. |

### Optional Fields

| Field | Notes |
|-------|-------|
| `workflow` | `"workflow_name"` — activates a workflow pipeline before main session. |
| `model` | Override model for this agent (e.g. `"openrouter:anthropic/claude-sonnet-4"`). |

### Forbidden in Agents

| Field | Why |
|-------|-----|
| `name` | Injected from tag at runtime. |
| `[deps]` | Deps belong in capability files. |
| `[roles.mcp]` | Injected from capabilities at runtime. |
| `[[mcp.servers]]` | MCP servers belong in capability files. |

### System Prompt Structure (mandatory — 2026 standard)

System prompts must use XML-tagged blocks in a fixed order. This is grounded in three findings: (1) the U-shape attention curve — beginning and end of the prompt get the most attention, the middle gets "lost"; (2) Anthropic's published guidance that XML tags are the preferred structuring method for Claude; (3) Claude Opus 4.7 follows instructions more literally than 4.6 — implicit gaps don't get bridged anymore, so structure has to be explicit.

The eight-block order, top to bottom:

```
<identity>          ← primacy: who/what (3–5 lines, role + expertise + style)
<voice>             ← tone, register, formality (omit if technical agent)
<scope>             ← what's owned / what routes elsewhere
<workflow>          ← numbered steps for the main pipeline
<rules>             ← decision rules, tables, domain knowledge
<examples>          ← good/bad pairs (omit if not applicable)
<output_format>     ← exact artifact shape, file location, schema
<interaction>       ← trigger → response patterns
<critical>          ← recency: brief Don't/Do list in plain language; reserve all-caps for one or two genuine safety hard-stops
```

Why this order:
- `<identity>` first because primacy: the model commits to role early
- `<critical>` last because recency: the tail is load-bearing — it's the last thing the model sees before the user message and gets disproportionate attention
- `<workflow>` and `<rules>` in the middle have to do their work via clear tagging, since middle-of-prompt content is the "lost" zone — the XML tags act as retrieval anchors

Where {{CWD}}, {{DATE}}, and other dynamic placeholders go (and where they don't):

The system prompt must be STABLE run-to-run. Anything that changes between runs breaks prompt caching, which costs real money and latency on every call.

- `{{CWD}}` and `{{DATE}}` change every run — they belong in the `welcome` field ONLY.
- The harness pipes working directory and current date as separate runtime context. Putting them in `system` duplicates that state AND breaks the cache.
- The rule: if a placeholder's value changes from one session to the next, it does not belong in `system`. System is identity + rules + structure — all stable. Welcome handles "where am I, when am I" dynamics.
- Static placeholders like `{{INPUT:KEY}}` and `{{ENV:KEY}}` typically don't appear in system anyway — they live in MCP server config.

The lint enforces this: `{{CWD}}` or `{{DATE}}` anywhere inside `system = """..."""` is a hard error.

Block-by-block authoring rules:

- `<identity>` — One paragraph. Role, expertise, style. Don't bury this; the model uses it to pick its register.
- `<voice>` — Only include if voice/tone matters (content, marketing, video, creative agents). Omit for pure technical agents (developer, devops, security) where voice is uniform.
- `<scope>` — Two lists: ✅ Own / ❌ Don't own (route to <other-agent>). Required for any agent that sits next to siblings (e.g. `marketing:seo` vs `content:seo`).
- `<workflow>` — Numbered steps (1, 2, 3…). Each step is one sentence + optional sub-bullets. Don't write paragraphs.
- `<rules>` — Tables and bullet lists win here. Decision matrices, parameter ranges, vocabulary lists. This is the agent's domain knowledge.
- `<examples>` — Bad → Good pairs are the strongest format. Skip this block if the agent's output is freeform.
- `<output_format>` — Exact structure of the artifact. If the agent saves files, name the path pattern (`./video-out/<slug>/script.md`). If the agent returns markdown blocks, show the schema.
- `<interaction>` — Trigger patterns. "When user says X → do Y". Especially "Ambiguous → ask ONE clarifying question."
- `<critical>` — Brief Don't/Do list in plain language: things the model could plausibly get wrong if not warned, and the corresponding correct action. Reserve all-caps `NEVER`/`ALWAYS` for one or two genuine safety hard-stops (e.g. `Never force-push to main`); stacking more dilutes attention on Claude 4.6+ (see "Tone calibration"). No CWD/DATE placeholders, no preamble, no `🚨 HARD RULES` theatre.

Token discipline (Claude 4.7 / 2026):
- Target: 200–1000 words for the full system prompt is the production sweet spot
- Soft warning at 1500 words (`SYSTEM_LENGTH_WARN`) — context rot risk
- Hard cap: 3000 words. Above this, `lint-manifests.sh` fails with `SYSTEM_TOO_LONG` — extract documentation/reference content into skills.
- Be explicit — Claude 4.7 doesn't bridge implicit gaps the way 4.6 did
- Static content first for prompt caching (saves up to 90% cost on repeat sessions)
- No decorative prose — every line must do work; if you can cut it without losing meaning, cut it

Authoring patterns that work:
- Specific over generic — "Use `uv run pytest` for testing" beats "Run the tests"
- Tool commands inline — actual CLI commands for the domain (cargo, kubectl, npm, etc.)
- Set boundaries explicitly — "Fix X" means fix X only, not refactor the neighborhood
- Reference example agents — study `developer:general` for execution protocol; `agents/content/article.toml` for content-style structure

Anti-patterns that break the structure:
- Free-form markdown sections without `<tag>` wrappers — defeats the U-shape strategy
- `IDENTITY` / `WORKFLOW` as plain `##` headers — Claude treats them as content, not structural anchors
- Long preambles before `<identity>` (e.g. "Welcome to this agent...") — wastes the primacy slot
- Critical rules buried in the middle — they get "lost"
- `<critical>` block with paragraphs of explanation — keep it tight: brief Don't/Do bullets, that's it
- Stacked theatrical emphasis — `🚨 HARD RULES`, `CRITICAL: YOU MUST`, ten bullets all starting `NEVER` or `ALWAYS`. On Claude 4.5+ this over-triggers and dilutes signal. See "Tone calibration" below.
- Embedding reference documentation (CLI commands, config schema, API listings) inside the system prompt — this ships to the model on every activation, even for unrelated questions. Reference content belongs in skills loaded on demand, not in `system`. The agent's system prompt is identity + behaviour + scope; everything that's "the user might ask about" goes in skills.

Tone calibration (Claude 4.6+ over-emphasis, mandatory awareness):

Claude 4.5+ is far more responsive to the system prompt than 3.x. Aggressive language written to defeat under-triggering on older models now over-triggers. Substance stays; theatre goes.

- `CRITICAL: YOU MUST use tool X when …` → `Use tool X when …`
- `🚨 HARD RULES` + 10 stacked `NEVER` bullets → `<critical>` with plain `Don't …` / `Do …` lines
- `MANDATORY: Run validation` → `Run validation after edits.`
- `NEVER assert X you haven't verified` → `Don't assert X you haven't verified.`
- `DEFAULT TO using web search` → `Use web search when it would enhance your understanding.`
- `After every 3 tool calls, summarize progress` → drop on 4.7 (internalised)

Reserve all-caps and "must" for one or two genuine safety hard-stops (e.g. `Never force-push to main`). The substance test: delete the `NEVER`/`ALWAYS`/`MUST` and lowercase the line. Does the rule still make sense? Soften it. Does it read as filler once softened? Cut it.

Full reference (verbatim Anthropic guidance, parallel-tool-calls block, message-history rules): `skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

Markdown discipline inside XML blocks (token economy — mandatory):

The XML tag IS the structural anchor. Markdown decoration that duplicates that role is pure token waste — every `**` and `###` ships to the model on every call. Strip the noise:

- No `### subsection` heading at the top of an XML block. The opening tag already names the section. `<voice>` followed immediately by `### Voice & Tone` is redundant — drop the H3.
- `### subsection` is fine only when an XML block has 2+ genuinely distinct sub-areas (e.g. `<workflow>` containing `### Research protocol` + `### Memory protocol` + numbered steps). Single-subsection blocks should flow as plain prose under the tag.
- No `bold` on bullet leads. `- Active voice — "Studies show X"` becomes `- Active voice — "Studies show X"`. The em-dash already separates lead from explanation. Bold adds tokens, not meaning.
- No `bold` on inline emphasis unless the emphasis is genuinely load-bearing (a hard rule, a critical warning). Default: drop it.
- Keep tables. `|---|---|` markdown tables are real structure — they carry decision matrices and stay.
- Keep code fences. Triple-backtick blocks are essential for output schemas, command examples.
- Keep numbered lists. `1. Step` becomes `1. Step` — but the numbering stays.
- No `---` separators between content inside an XML block. Use blank lines.

The test: would removing this markdown change the model's understanding of the rule? If no, drop it.

### Temperature Guidelines by Domain

| Domain | Temperature | top_p | Why |
|--------|-------------|-------|-----|
| Developer | 0.1 | 0.9 | Precision, deterministic code |
| DevOps | 0.15 | 0.9 | Reliable infrastructure |
| Security | 0.15 | 0.9 | Conservative, no guessing |
| Medical/Legal | 0.15–0.2 | 0.9 | Evidence-based, cautious |
| Content/Creative | 0.4–0.8 | 0.9 | Voice, creativity, variation |
| General assistant | 0.3 | 0.9 | Balanced |

### Required Disclaimers

Medical, legal, and financial agents MUST include prominent disclaimers in the system prompt:
- Medical: "NOT a doctor, CANNOT diagnose or prescribe"
- Legal: "NOT a licensed attorney, legal information only"
- Financial: "NOT financial advice"

### Placeholder Variables

| Placeholder | Use for |
|-------------|---------|
| `{{CWD}}` | Current working directory — always include in `welcome` and `system` |
| `{{DATE}}` | Current date |
| `{{INPUT:KEY}}` | Secret, user-global (e.g. API keys) |
| `{{ENV:KEY}}` | Non-secret or project-scoped env var |

### Naming and Metadata Rules

- File path matches tag: `developer:rust` → `agents/developer/rust.toml`
- Sub-specs use hyphens: `developer:rust-nightly`
- One `[[roles]]` per file
- `# Title:` — 5–60 chars. Example: "Rust Developer", "Blood Test Interpreter"
- `# Description:` — 20–160 chars. Concise and scannable, like an SEO meta description

### Workflows & Layers (Multi-Step Pipelines)

Use workflows when:
- Agent needs multiple AI processing stages (context curation → implementation → review)
- Different steps need different models (cheap for analysis, best for code generation)
- A feedback loop is needed (build → review → score → fix)
- The main session should only handle finalization (e.g., shipping a PR)

#### Workflow Definition

```toml
workflow = "my_workflow"

[[workflows]]
name = "my_workflow"
description = "What this workflow does"

[[workflows.steps]]
name = "step_name"
type = "once"
layer = "layer_name"
```

#### Step Types

| Type | Key fields | Behavior |
|------|-----------|----------|
| `once` | `layer` | Run layer once |
| `loop` | substeps, `max_iterations`, `exit_pattern` | Repeat until pattern matches or max hit |
| `foreach` | `parse_pattern`, substeps | Iterate over regex-matched items |
| `conditional` | `layer`, `condition_pattern`, `on_match`, `on_no_match` | Branch based on output |
| `parallel` | `parallel_layers`, `aggregator` | Run layers simultaneously, aggregate results |

#### Layer Definition

```toml
[[layers]]
name = "layer_name"
description = "What this layer does"
model = "openrouter:google/gemini-2.5-flash"
max_tokens = 4096
temperature = 0.2
input_mode = "last"       # last | first | all
output_mode = "append"    # none | append | replace
output_role = "assistant" # assistant | user
system_prompt = """..."""

[layers.mcp]
server_refs = ["octofs", "octocode"]
allowed_tools = ["octofs:view", "octocode:semantic_search"]
```

#### Data Flow

| `input_mode` | Layer sees |
|-------------|-----------|
| `last` | Only the most recent message |
| `first` | Only the first message (user's original input) |
| `all` | Full conversation history |

| `output_mode` | Effect |
|--------------|--------|
| `none` | Output discarded |
| `append` | Output added as new message |
| `replace` | Output replaces history |

#### Model Selection for Layers

| Role | Model choice | Why |
|------|-------------|-----|
| Context curation | Cheap (gemini-flash, gpt-4.1-mini) | Read-only, no code generation |
| Code implementation | Best (claude-sonnet-4, opus) | Quality matters most here |
| Review / scoring | Cheap (gemini-flash) | Analysis, not generation |
| Shipping / PR | Cheap (gemini-flash) | Mechanical, no reasoning |

See `agents/developer/autopilot.toml` for a complete workflow example.

### Pre-Write Checklist

Before writing any agent manifest, verify:

- [ ] `# Title:` comment present? (5–60 chars)
- [ ] `# Description:` comment present? (20–160 chars)
- [ ] Is there a similar agent to reference for prompt structure?
- [ ] Do all needed capabilities exist? If not, use `tap-capability-authoring` skill first.
- [ ] System prompt uses XML-tagged blocks in the canonical order? (`<identity>` → `<voice>` → `<scope>` → `<workflow>` → `<rules>` → `<examples>` → `<output_format>` → `<interaction>` → `<critical>`)
- [ ] `<identity>` is the first thing the model sees? (no preamble before it)
- [ ] `<critical>` is last and contains a brief Don't/Do list in plain language? (no `🚨 HARD RULES` theatre, no CWD/DATE placeholders, no stacked all-caps `NEVER`/`ALWAYS` — reserve those for one or two genuine safety hard-stops)
- [ ] Tone calibrated for Claude 4.6+: `Use X when ...` rather than `Default to X` / `CRITICAL: YOU MUST X`?
- [ ] `{{CWD}}` and `{{DATE}}` appear in the `welcome` field, NOT in `system`?
- [ ] Total system prompt under ~1500 words? (context rot threshold)
- [ ] Is the system prompt specific enough? (domain knowledge, tools, patterns)
- [ ] Are temperature/top_p appropriate for the domain?
- [ ] Does the welcome message include an emoji + `{{CWD}}`?
- [ ] No `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in the agent file?
- [ ] Run `bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml` — passes clean?
- [ ] Run `bin/load <domain>:<spec>` — resolves without errors?

## Examples

### Example 1: Minimal correct agent (2026 XML structure)

```toml
# agents/developer/rust.toml
# Agent: developer:rust
# Title: Rust Developer
# Description: Expert Rust developer. Writes idiomatic, safe, performant Rust code.

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-rust"]

[[roles]]
system = """
<identity>
Expert Rust developer. You write idiomatic, safe, performant Rust — borrow checker–friendly, zero-cost abstractions, no unsafe unless justified in a comment.
</identity>

<scope>
✅ Own: Rust code, Cargo workflows, async with tokio, error handling with thiserror/anyhow, no_std embedded, FFI bindings.
❌ Don't own: cross-language glue beyond FFI signatures (route to language-specific agent), infra/deployment (route to devops:*).
</scope>

<workflow>
1. **Read context** — `cargo metadata`, `Cargo.toml`, surrounding modules.
2. **Plan** — for non-trivial changes, present an outline before writing.
3. **Write** — idiomatic Rust, prefer iterators over loops, `Result` over panic.
4. **Verify** — `cargo check`, `cargo clippy`, `cargo test`.
</workflow>

<rules>
- Errors: `thiserror` for libraries, `anyhow` for binaries. Never `unwrap()` outside tests/examples.
- Async: tokio is the default runtime. Don't mix runtimes.
- Lints: `cargo clippy -- -D warnings` must pass clean.
- No `unsafe` blocks without a SAFETY comment naming the invariant.
</rules>

<output_format>
Code edits via Edit/Write tools. After non-trivial changes, run `cargo check` and report the result.
</output_format>

<interaction>
- New task → confirm the scope before editing if files >3 will change.
- Ambiguous spec → ask ONE clarifying question, then proceed.
</interaction>

<critical>
- Don't add `unsafe` without a SAFETY comment naming the invariant.
- Don't use `unwrap()` in production code paths.
- Don't disable clippy lints to silence warnings — fix the underlying issue.
- Run `cargo check` after edits.
- Use the simplest type that fits — reach for `Box<dyn>` only when a generic doesn't work.
</critical>
"""
welcome = "🦀 Rust developer ready. Working in {{CWD}}"
temperature = 0.1
top_p = 0.9
top_k = 0
```

### Example 2: Agent with model override

```toml
capabilities = ["core", "filesystem-read", "filesystem-write", "websearch"]

[[roles]]
system = """..."""
welcome = "🔍 Research agent ready. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0
model = "openrouter:anthropic/claude-sonnet-4"
```

### Example 3: Common mistake — forbidden fields

```toml
# ❌ WRONG — never put these in an agent manifest
[deps]
require = ["muvon/octofs"]

[roles.mcp]
server_refs = ["octofs"]

[[mcp.servers]]
name = "octofs"
```

## References

- `templates/agent.toml` — canonical agent template
- `agents/developer/general.toml` — reference for execution protocol pattern
- `agents/developer/autopilot.toml` — reference for workflow + layer patterns
- `bin/load` — resolves capabilities → merged manifest (run to debug)
- `bash scripts/lint-manifests.sh` — validates agent TOML files
