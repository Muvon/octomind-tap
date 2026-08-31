# __TAP_ID__ — Tap Authoring Guide

This repository is an Octomind tap. It packages runnable agent manifests,
capability providers, dependency installers, reusable skills, and workflows.
Keep the tap self-contained, deterministic, and safe to clone on another
machine. Never commit credentials or machine-specific configuration.

## Repository structure

```text
agents/<domain>/<spec>.toml     # Runnable agent manifests
capabilities/<name>/            # Capability metadata and provider definitions
  config.toml                   # Auto-activation triggers and optional domains
  default.toml                  # Active provider, normally a relative symlink
  <provider>.toml               # Dependencies, tool permissions, MCP servers
deps/<org>/<tool>.sh            # Idempotent macOS/Linux installer
deps/<org>/<tool>.md            # Required companion documentation
deps/lib/platform.sh            # Shared platform helpers; source, do not duplicate
skills/<name>/SKILL.md          # AgentSkills instruction pack
workflows/<name>.toml           # External multi-step workflow
templates/                      # Canonical starting points for new artifacts
scripts/check.sh                # Repository validation entrypoint
```

Do not nest agents deeper than `agents/<domain>/<spec>.toml` or skills deeper
than `skills/<name>/SKILL.md`.

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
agents/<domain>/<spec>.toml
```

The path defines the runtime tag `<domain>:<spec>`. Each manifest requires a
top-level `capabilities = [...]` array followed by exactly one `[[roles]]`.
Do not set `name`; Octomind injects it from the tag.

Required role fields:

```toml
capabilities = ["core"]

[[roles]]
temperature = 0.3
top_p = 0.9
top_k = 0
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
- Keep technical temperatures around 0.1–0.3 and general roles around 0.4–0.6.
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

Current static agent resolution requires every declared capability to exist in
this tap. The scaffold therefore includes `capabilities/core/default.toml`.
Before declaring another community capability, add its provider definition and
all dependency scripts it references. Do not silently assume another tap will
supply static capabilities until the runtime explicitly supports that contract.

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

Skills live at `skills/<name>/SKILL.md`. The directory and frontmatter `name`
must match and use lowercase letters, digits, and hyphens.

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
may follow. Keep skills domain-isolated. Their recommended body order is:

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
- Commit only placeholder names, never secret values or a populated `.env`.

Capability `env` tables primarily carry and document `{{ENV:KEY}}` values.
Ensure the key exactly matches the variable read by the child process.

## Validation checklist

- [ ] Agent paths match their `<domain>:<spec>` tags.
- [ ] Every agent has capabilities and exactly one complete role.
- [ ] Agent system prompts use canonical XML ordering and stable contents.
- [ ] Every declared static capability exists locally and has `default.toml`.
- [ ] Every capability dependency has a matching shell script and document.
- [ ] Every skill directory matches its frontmatter name.
- [ ] Every workflow parses and references intentional roles.
- [ ] No secret or populated `.env` is committed.
- [ ] `bash scripts/check.sh` passes.

## Never

- Write `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in an agent manifest.
- Set `name` inside `[[roles]]`.
- Add a capability reference that cannot resolve from this tap.
- Add a non-built-in `server_ref` without a matching MCP server definition.
- Reimplement the platform matrix inside individual dependency scripts.
- Put dynamic runtime placeholders inside an agent's `system` prompt.
- Commit credentials, tokens, private endpoints, or generated `.env` files.

