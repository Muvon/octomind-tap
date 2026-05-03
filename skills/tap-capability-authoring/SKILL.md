---
name: tap-capability-authoring
title: "Capability & Dep Script Authoring"
description: "Deep guide for creating Octomind capabilities and dep scripts: capability file format, provider/symlink pattern, dep script structure, platform coverage, companion .md requirements, setup-symlinks.sh registration, and validation checklist. Activate when creating or editing capabilities/<name>/ or deps/<org>/<tool>.sh files."
license: Apache-2.0
compatibility: "Requires: octomind-tap repo. Use alongside tap-agent-authoring for agent creation."
domains: octomind
---

# Capability & Dep Script Authoring

## Overview

This skill encodes everything needed to create a new capability or dep script in the octomind-tap registry. A **capability** is the abstraction layer between agents and MCP servers — agents declare what they need, capabilities provide the wiring. This skill covers the full creation checklist: capability file format, provider/symlink pattern, dep script structure, platform coverage requirements, companion documentation, `setup-symlinks.sh` registration, and how to validate everything.

Use this skill whenever you need to create a new capability or dep script, or when an agent needs a tool not covered by existing capabilities.

---

## Instructions

### What Is a Capability?

A capability is a named bundle that provides:
- **Deps** — install scripts to run before the session
- **MCP server config** — how to launch the server
- **Tool permissions** — which tools the agent can call

Agents declare `capabilities = ["name"]`. At runtime, `bin/load` resolves each name to `capabilities/<name>/default.toml` and merges everything into the final manifest.

**Key principle:** capabilities hide MCP complexity from agents. An agent says "I need websearch" — it doesn't care whether that's Tavily, Brave, or something else. The capability + provider pattern enables swapping implementations without touching agents.

### Capability Directory Structure

```
capabilities/<name>/
  <provider-a>.toml    ← provider definition (the real file)
  <provider-b>.toml    ← alternative provider (optional)
  default.toml         → <provider-a>.toml  (symlink to active provider)
```

- `default.toml` is ALWAYS a symlink — never a real file (except `core` and `agent` which are built-ins)
- Users can override the active provider via `[capabilities]` in their config

### Capability File Format

```toml
# capabilities/<name>/<provider>.toml
# Capability: <name>
# Provider: <provider-name>
# Title: Short Capability Title (5–60 chars)
# Description: What this capability provides (20–160 chars).

[deps]
require = ["org/tool"]       # each entry needs a deps/<org>/<tool>.sh script

[roles.mcp]
server_refs = ["servername"]       # must match a [[mcp.servers]] name below
allowed_tools = ["servername:*"]   # wildcards OK

[[mcp.servers]]
name = "servername"
type = "stdio"                     # "stdio", "http", or "builtin"
command = "..."                    # for stdio
args = [...]
timeout_seconds = 60
tools = []
```

**Not all sections are required:**
- Deps-only capability (e.g. `programming-python`): only `[deps]` section
- MCP-only capability: only `[roles.mcp]` + `[[mcp.servers]]`
- Full capability: all three sections

**Built-in servers** (`core`, `octofs`, `agent`, `octocode`) do NOT need `[[mcp.servers]]` blocks. Every other `server_refs` entry MUST have a matching `[[mcp.servers]]` block.

**Environment variable injection:** use `{{ENV:VAR_NAME}}` in capability files for runtime env vars (e.g. API keys). Document required env vars in the capability file header comment.

---

### Full Creation Checklist

When creating a new capability:

1. **Create** `capabilities/<name>/<provider>.toml` with `# Title:`, `# Description:`, and the appropriate sections
2. **Create** the dep script at `deps/<org>/<tool>.sh` (if needed) — see dep script format below
3. **Create** the companion doc at `deps/<org>/<tool>.md` — required for every `.sh`
4. **Create** the symlink: `cd capabilities/<name> && ln -s <provider>.toml default.toml`
5. **Register** in `scripts/setup-symlinks.sh`:
   - Add `link "<name>" "<provider>.toml"` line in the links section
   - Add `"<name>"` to the `DECLARED` array
6. **Run** `bash scripts/setup-symlinks.sh` to verify symlinks
7. **Run** `bash scripts/lint-deps.sh deps/<org>/<tool>.sh` to validate dep script
8. **Run** `bash scripts/lint-capabilities.sh capabilities/<name>` to validate capability
9. **Reference** `"<name>"` in the agent's `capabilities = [...]`

---

### Dep Script Authoring

Dep scripts are covered in full by the **`tap-deps-authoring`** skill. Load it when you need to write or edit a `deps/<org>/<tool>.sh` file:

```
skill(action="use", name="tap-deps-authoring")
```

Key points to know here:
- Every `require = ["<org>/<tool>"]` entry in a capability needs a matching `deps/<org>/<tool>.sh`
- `type: mcp` — ensures an MCP server runtime is runnable (e.g. `npx`, `uvx`)
- `type: dep` — installs a standalone CLI tool used directly
- Every `.sh` must have a companion `.md` at the same path


---

### Companion Documentation Format

Every dep script MUST have a matching `.md` file at `deps/<org>/<tool>.md`.

**For MCP servers** (`type: mcp`) — use `templates/dep-mcp.md` as base, must include:
- `## MCP Server` — what the server provides
- `## Authentication` — required env vars, tokens, setup
- `## Available Tools` — list of tools the server exposes
- `## Configuration Example` — example capability TOML snippet

**For plain deps** (`type: dep`) — use `templates/dep-tool.md` as base, must include:
- `## Key Commands` — most important CLI commands
- `## Common Usage` — typical usage patterns

---

### setup-symlinks.sh Registration

When adding a new capability, you MUST update `scripts/setup-symlinks.sh` in two places:

1. Add a `link` call in the links section:
```bash
link "my-capability" "provider.toml"
```

2. Add the name to the `DECLARED` array:
```bash
DECLARED=(
  ...existing entries...
  "my-capability"
)
```

If you skip either step, `setup-symlinks.sh` will emit a `WARN` for undeclared dirs.

**Note:** `core` and `agent` are built-in capabilities — do NOT add `link` entries for them. They have real files, not symlinks.

---

## Examples

### Example 1: Simple MCP capability

```toml
# capabilities/websearch/tavily.toml
# Capability: websearch
# Provider: tavily
# Title: Web Search via Tavily
# Description: Web search and content extraction using the Tavily API. Requires TAVILY_API_KEY.

[deps]
require = ["tavily/tavily-mcp"]

[roles.mcp]
server_refs = ["tavily"]
allowed_tools = ["tavily:*"]

[[mcp.servers]]
name = "tavily"
type = "stdio"
command = "npx"
args = ["-y", "tavily-mcp@0.1.14", "--api-key", "{{ENV:TAVILY_API_KEY}}"]
timeout_seconds = 60
tools = []
```

### Example 2: Deps-only capability (no MCP server)

```toml
# capabilities/programming-python/uv.toml
# Capability: programming-python
# Provider: uv
# Title: Python Runtime via uv
# Description: Python runtime and package management via uv and uvx.

[deps]
require = ["astral-sh/uv"]
```

### Example 3: Capability with HTTP MCP server

```toml
# capabilities/octoweb/octoweb.toml
# Capability: octoweb
# Provider: octoweb
# Title: Browser Automation via Octoweb
# Description: Browser automation and web scraping via Octoweb HTTP MCP server.

[deps]
require = ["muvon/octoweb"]

[roles.mcp]
server_refs = ["octoweb"]
allowed_tools = ["octoweb:*"]

[[mcp.servers]]
name = "octoweb"
type = "http"
url = "http://localhost:3333"
timeout_seconds = 30
tools = []
```

---

## References

- `templates/agent.toml` — canonical agent template (for agent creation)
- `scripts/setup-symlinks.sh` — symlink management (must update when adding capabilities)
- `bash scripts/lint-capabilities.sh` — validates capability files
- `bash scripts/setup-symlinks.sh` — creates/refreshes default.toml symlinks
- `tap-deps-authoring` skill — full dep script authoring guide
