---
name: tap-agent-authoring
title: "Agent Manifest Authoring"
description: "Deep guide for writing Octomind agent manifests: TOML format, required fields, system prompt structure, temperature guidelines, workflow/layer patterns, and the pre-write checklist. Activate when creating or editing agents/<domain>/<spec>.toml files."
license: Apache-2.0
compatibility: "Requires: octomind-tap repo. Use alongside tap-capability-authoring for capability creation."
domains: octomind
---

# Agent Manifest Authoring

## Overview

This skill encodes everything needed to write a correct, high-quality `agents/<domain>/<spec>.toml` file for the octomind-tap registry. It covers the exact TOML format, required and forbidden fields, how to write effective system prompts, temperature/top_p guidelines by domain, workflow and layer patterns for multi-step pipelines, and the pre-write checklist.

Use this skill whenever you are creating or editing an agent manifest.

---

## Instructions

### Agent Manifest Format

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Title: Short Agent Title (5–60 chars)
# Description: What this agent does (20–160 chars).

capabilities = ["core", "filesystem", "codesearch", "programming-python"]

[[roles]]
system = """
<System prompt — the agent's personality, knowledge, and behavior rules>
Working directory: {{CWD}}
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

---

### Writing Good System Prompts

The system prompt is the most important part of an agent. Structure it:

1. **Identity** — Who is this agent? One sentence: role + expertise + style.
2. **Domain knowledge** — Specific best practices, patterns, tools, and conventions for the domain.
3. **Execution protocol** — How the agent should work (parallel execution, planning, tool usage).
4. **Scope discipline** — What the agent does and doesn't do.
5. **Never / Always** — Hard rules that prevent common mistakes.

**Good patterns:**
- **Be specific, not generic** — "Use `uv run pytest` for testing" beats "Run the tests"
- **Include tool commands** — List the actual CLI commands for the domain (cargo, kubectl, npm, etc.)
- **Set boundaries** — "Fix X" means fix X only, not refactor the neighborhood
- **Reference examples** — Study `developer:general` for the execution protocol pattern

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

---

### Placeholder Variables

| Placeholder | Use for |
|-------------|---------|
| `{{CWD}}` | Current working directory — always include in `welcome` and `system` |
| `{{DATE}}` | Current date |
| `{{INPUT:KEY}}` | Secret, user-global (e.g. API keys) |
| `{{ENV:KEY}}` | Non-secret or project-scoped env var |

---

### Naming and Metadata Rules

- File path matches tag: `developer:rust` → `agents/developer/rust.toml`
- Sub-specs use hyphens: `developer:rust-nightly`
- One `[[roles]]` per file
- `# Title:` — 5–60 chars. Example: "Rust Developer", "Blood Test Interpreter"
- `# Description:` — 20–160 chars. Concise and scannable, like an SEO meta description

---

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

---

### Pre-Write Checklist

Before writing any agent manifest, verify:

- [ ] `# Title:` comment present? (5–60 chars)
- [ ] `# Description:` comment present? (20–160 chars)
- [ ] Is there a similar agent to reference for prompt structure?
- [ ] Do all needed capabilities exist? If not, use `tap-capability-authoring` skill first.
- [ ] Is the system prompt specific enough? (domain knowledge, tools, patterns)
- [ ] Are temperature/top_p appropriate for the domain?
- [ ] Does the welcome message include an emoji + `{{CWD}}`?
- [ ] No `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in the agent file?
- [ ] Run `bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml` — passes clean?
- [ ] Run `bin/load <domain>:<spec>` — resolves without errors?

---

## Examples

### Example 1: Minimal correct agent

```toml
# agents/developer/rust.toml
# Agent: developer:rust
# Title: Rust Developer
# Description: Expert Rust developer. Writes idiomatic, safe, performant Rust code.

capabilities = ["core", "filesystem", "codesearch", "programming-rust"]

[[roles]]
system = """
You are an expert Rust developer...
Working directory: {{CWD}}
"""
welcome = "🦀 Rust developer ready. Working in {{CWD}}"
temperature = 0.1
top_p = 0.9
top_k = 0
```

### Example 2: Agent with model override

```toml
capabilities = ["core", "filesystem", "websearch"]

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

---

## References

- `templates/agent.toml` — canonical agent template
- `agents/developer/general.toml` — reference for execution protocol pattern
- `agents/developer/autopilot.toml` — reference for workflow + layer patterns
- `bin/load` — resolves capabilities → merged manifest (run to debug)
- `bash scripts/lint-manifests.sh` — validates agent TOML files
