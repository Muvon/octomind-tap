# __TAP_ID__ — Tap Authoring Guide

This repository is an Octomind tap. It packages runnable agent manifests,
capability providers, dependency installers, reusable skills, and workflows.
Keep the tap self-contained, deterministic, and safe to clone on another
machine. Never commit credentials or machine-specific configuration.

## Repository structure

```text
agents/<name>/config.toml        # Runnable agent manifest, one directory per agent
agents/<name>/skills/<skill>/SKILL.md  # Owned skill: used by this agent only
capabilities/<name>/            # Capability metadata and provider definitions
  config.toml                   # Auto-activation triggers and optional domains
  default.toml                  # Active provider, normally a relative symlink
  <provider>.toml               # Dependencies, tool permissions, MCP servers
deps/<org>/<tool>.sh            # Idempotent macOS/Linux installer
deps/<org>/<tool>.md            # Required companion documentation
deps/lib/platform.sh            # Shared platform helpers; source, do not duplicate
skills/<skill>/SKILL.md         # Shared skill: used by two or more agents
workflows/<name>.toml           # External multi-step workflow
templates/                      # Canonical starting points for new artifacts
scripts/check.sh                # Repository validation entrypoint
```

Keep only agent directories in `agents/`, with no symlinks. An agent directory
holds only `config.toml` and `skills/`. A skill sits at
`agents/<agent>/skills/<skill>/SKILL.md` or `skills/<skill>/SKILL.md`, and its
name exists once in the tap.

## Working protocol

1. Read this file and the nearest relevant existing artifact before editing.
2. Determine whether the request belongs to an agent, capability, dependency,
   skill, or workflow. Keep changes inside that artifact boundary.
3. Copy the matching file from `templates/` when creating something new.
4. Use capabilities to grant tools to agents. Never wire dependencies or MCP
   servers directly into an agent manifest.
5. Run `bash scripts/check.sh` after changes and fix every reported error.
6. Report the changed artifacts and anything not validated at runtime.

Preserve unrelated user changes. Do not modify Git state, publish, or push
unless the user explicitly asks.

## Agent manifests

Location:

```text
agents/<name>/config.toml
```

The directory name defines the runtime tag `<name>`: lowercase letters, digits, and
hyphens, starting with a letter, with no `:`. `octomind run <name>` starts the
agent. The `# Agent: <name>` header comment must equal the directory name. Each
manifest requires a top-level `capabilities = [...]` array followed by exactly
one `[[roles]]`. Do not set `name`; Octomind injects it from the tag.

An agent that hands work to other agents declares the `orchestration`
capability (`octomind/orchestration`). It sends a task with
`tap(action="run", prompt="<brief>")` and the runtime matches the task to an
agent by each agent's `# Title:` and `# Description:`, so write those in the
words a task brief would use.

A header comment lists the agents it may reach: `*` for every agent, or agent
names separated by commas. Names must exist in `agents/`, appear once, and
never be the agent's own name, and agents that list each other must not form a
loop. An agent with the header needs `orchestration`.

```toml
# agents/marketer/config.toml
# Uses: writer, seo
```

Required role fields:

```toml
capabilities = ["core"]

[[roles]]
welcome = "Agent ready. Working in {{CWD}}"
system = """
<identity>
Who the agent is and what expertise it owns.
</identity>

<scope>
What the agent owns and what it routes elsewhere.
</scope>

<workflow>
1. Understand the requested outcome.
2. Gather evidence.
3. Complete and verify the work.
</workflow>

<critical>
- Don't invent facts or completion evidence.
- State validation limits plainly.
</critical>
"""
```

System prompts use XML blocks in this canonical order when applicable:

```text
identity → voice → scope → workflow → rules → examples → output_format → interaction → critical
```

Rules:

- Put `{{CWD}}`, `{{DATE}}`, and other changing runtime values in `welcome`,
  never in `system`; a stable system prompt can be cached.
- Do not use Markdown `#` or `##` headers inside `system`; XML tags provide
  the primary structure. `###` is reserved for real subsections inside a tag.
- Do not use `**bold**` inside `system`.
- `temperature`, `top_p`, and `top_k` are deprecated; Octomind ignores them and
  sends no sampling parameters, so do not set them.
- Keep the system prompt focused. Prefer roughly 200–1000 words.
- Never add `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` to an agent.

## Capabilities

Agents declare what they need; capability providers describe how that need is
implemented. A capability may provide dependencies, MCP server references,
allowed tools, MCP server definitions, or any combination of them.

Provider location:

```text
capabilities/<name>/<provider>.toml
```

Provider shape:

```toml
# Capability: <name>
# Provider: <provider>
# Title: Human-readable title
# Description: What the capability provides.

[deps]
require = ["org/tool"]

[roles.mcp]
server_refs = ["server-name"]
allowed_tools = ["server-name:*"]

[[mcp.servers]]
name = "server-name"
type = "stdio"
command = "server-command"
args = ["mcp"]
timeout_seconds = 60
tools = []
```

Every non-built-in `server_ref` needs a matching `[[mcp.servers]]` block.
Create `default.toml` as a relative symlink to the chosen provider. Built-in
capabilities such as the scaffold's `core` may use a real `default.toml`.

`config.toml` holds capability-level discovery metadata:

```toml
triggers = [
  "natural-language request that should activate this capability",
  "another distinct request phrasing",
]
domains = ["developer"]
```

Triggers belong in `config.toml`, not provider files. Use specific positive
phrases and include enough varied examples for semantic matching.

Agents reference capabilities in three forms:

| Reference | Resolves from |
|-----------|---------------|
| `<name>` | This tap first, then every connected tap |
| `octomind/<name>` | The baseline community tap only |
| `<org>/<name>` | The connected tap whose id starts with `<org>/` |

A capability's dependency scripts run from the tap that provides it, so
reference community capabilities as `octomind/<name>` instead of copying them.
Ship a capability here only when this tap owns it, together with every
dependency script it references. `scripts/check.sh` requires a local
`default.toml` for bare names only.

## Dependency installers

Every dependency consists of both files:

```text
deps/<org>/<tool>.sh
deps/<org>/<tool>.md
```

The shell script must:

1. Use `set -euo pipefail`.
2. Carry `# dep:`, `# type:`, `# description:`, and `# check:` headers plus a
   homepage URL.
3. Source `deps/lib/platform.sh`; do not reimplement platform detection.
4. Exit successfully immediately when `pkg_check <command>` succeeds.
5. Support macOS and Linux package managers: apt, dnf, pacman, zypper, apk,
   plus a universal fallback where practical.
6. Verify that the command is available after installation.

Use `type: mcp` when the script exists to make an MCP server runnable. Use
`type: dep` for a standalone CLI or runtime. MCP documentation requires
`MCP Server`, `Authentication`, `Available Tools`, and `Configuration Example`
sections. Plain dependency documentation requires `Key Commands` and
`Common Usage` sections.

## Skills

A skill used by one agent is an owned skill. It lives at
`agents/<agent>/skills/<skill>/SKILL.md` and belongs to that agent by location,
so its frontmatter has no `domains` line. A skill used by two or more agents is
a shared skill. It lives at `skills/<skill>/SKILL.md` and its `domains` line
lists those agents. A shared skill without `domains` loads only by hand or from
a workflow step. The directory and frontmatter `name` must match and use
lowercase letters, digits, and hyphens. Skills are addressed by bare name, so a
name exists once in the tap.

Required frontmatter:

```yaml
---
name: skill-name
title: "Human-readable title"
description: "What the skill does and when it should be activated."
license: MIT
---
```

Optional `capabilities`, `domains`, `allowed-tools`, and activation `rules`
may follow. Each `domains` entry is the name of an agent in `agents/`, and a shared skill
names at least two; a skill bound to one agent moves under that agent. A skill
auto-activates only for the agent that owns it or the agents in its `domains`.
Keep skills tied to the agents they serve and do not mention other agents in
the body. Their recommended body order is:

```text
Overview → Mental model → Rules → Examples → Checklist → Composition / References
```

Do not use `**bold**` in the skill body. Keep the checklist near the end as the
final action gate. Instructions must tell the model what to do, not merely
describe a topic.

## Workflows

Workflows are external pipelines under `workflows/<name>.toml`, run with:

```bash
octomind workflow <name>
```

They reference installed roles and tap agent tags. Do not put workflow blocks
or a `workflow =` field inside agent manifests.

Start from `templates/workflow.toml`. Keep step names stable because downstream
steps may reference earlier outputs by name.

## Secrets and placeholders

- `{{INPUT:KEY}}` is for user-global secrets stored by Octomind.
- `{{ENV:KEY}}` is for project-scoped environment values.
- `{{CWD}}` and `{{DATE}}` are prompt-time values and belong in `welcome` only.
- `{{SPECIALISTS}}` and `{{USES}}` are not expanded and must not appear in
  `system`; the check rejects them.
- Commit only placeholder names, never secret values or a populated `.env`.

Capability `env` tables primarily carry and document `{{ENV:KEY}}` values.
Ensure the key exactly matches the variable read by the child process.

## Validation checklist

- [ ] Agent directory names match their `# Agent: <name>` headers, and each directory holds only `config.toml` and `skills/`.
- [ ] Every agent has capabilities and exactly one complete role.
- [ ] Agent system prompts use canonical XML ordering and stable contents.
- [ ] Every bare capability exists locally with `default.toml`; community ones use `octomind/<name>`.
- [ ] Every capability dependency has a matching shell script and document.
- [ ] Every skill directory matches its frontmatter name, and no skill name appears twice.
- [ ] Owned skills have no `domains` line; shared skills list two or more agents.
- [ ] Every workflow parses and references intentional roles.
- [ ] No secret or populated `.env` is committed.
- [ ] `bash scripts/check.sh` passes.

## Never

- Write `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in an agent manifest.
- Set `name` inside `[[roles]]`.
- Copy a community capability into this tap; reference it as `octomind/<name>`.
- Add a non-built-in `server_ref` without a matching MCP server definition.
- Reimplement the platform matrix inside individual dependency scripts.
- Put dynamic runtime placeholders inside an agent's `system` prompt.
- Commit credentials, tokens, private endpoints, or generated `.env` files.
