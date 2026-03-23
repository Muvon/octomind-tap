# Octomind Tap — Architecture & Design Decisions

This document captures the canonical design of the tap registry. Read this before making any changes.

---

## Core Principle: Capability-Based Manifests

**Agents declare capabilities, not MCP servers. This is mandatory. There is no other way.**

Old (forbidden):
```toml
[roles.mcp]
server_refs = ["core", "octofs", "octocode"]
allowed_tools = ["core:*", "octofs:*", "octocode:*"]
```

New (the only way):
```toml
capabilities = ["core", "filesystem", "codesearch"]
```

`bin/load <domain>:<spec>` resolves capabilities at runtime and injects the full `[roles.mcp]` block automatically. Never write `[roles.mcp]` by hand in any manifest.

---

## How Capabilities Work

```
agents/developer/rust.toml
  └── capabilities = ["core", "filesystem", "codesearch"]
           │
           ▼
  bin/load developer:rust
           │
           ├── capabilities/core/default.toml        (real file, built-in)
           ├── capabilities/filesystem/default.toml  → octofs.toml (symlink)
           └── capabilities/codesearch/default.toml  → octocode.toml (symlink)
           │
           ▼
  Merged manifest with [deps], [roles.mcp], [[mcp.servers]] injected
```

Each `capabilities/<name>/default.toml` is either:
- A **real file** (built-ins: `core`, `agent`) — no symlink needed
- A **symlink** pointing to the active provider (e.g. `default.toml → tavily.toml`)

Symlinks are managed by `scripts/setup-symlinks.sh` which **always force-creates** them (`ln -sf`).

---

## Available Capabilities

| Capability   | Tools provided                                      | Default provider file  |
|--------------|-----------------------------------------------------|------------------------|
| `core`       | `plan`                                              | `core/default.toml`    |
| `agent`      | `agent_*`                                           | `agent/default.toml`   |
| `filesystem` | `view`, `shell`, `text_editor`, `workdir`, `ast_grep` | `filesystem/octofs.toml` |
| `codesearch` | `semantic_search`, `graphrag`, `view_signatures`    | `codesearch/octocode.toml` |
| `memory`     | `remember`, `memorize`                              | `memory/octobrain.toml` |
| `websearch`  | web search                                          | `websearch/tavily.toml` (alt: `brave.toml`) |
| `versioning` | git via shell                                       | `versioning/git.toml`  |

---

## Capability File Format

```toml
# capabilities/<name>/<provider>.toml

[deps]
require = ["muvon/octocode"]

[roles.mcp]
server_refs = ["octocode"]
allowed_tools = ["octocode:*"]

# Optional: [[mcp.servers]] if the provider needs a custom MCP server
```

---

## Manifest Rules (non-negotiable)

1. **`capabilities = [...]` is mandatory** — every manifest must have it at the top level.
2. **Never write `[roles.mcp]`** — it is injected by `bin/load` from capabilities.
3. **`[[mcp.servers]]` only for custom servers** — things with no matching capability (domain APIs, databases, etc.). Even then, no `[roles.mcp]`.
4. **Never set `name`** in `[[roles]]` — injected from the tag at runtime.
5. **One `[[roles]]` per file** — no multi-role manifests.
6. **File path must match tag** — `developer:rust` → `agents/developer/rust.toml`.

---

## Switching a Capability Provider

```bash
# Switch websearch from Tavily to Brave
ln -sf brave.toml capabilities/websearch/default.toml

# Reset all defaults
bash scripts/setup-symlinks.sh
```

`setup-symlinks.sh` behavior:
- Always **force-creates** symlinks (`ln -sf`) — never skips
- Reports `MISSING` + exits 1 if a provider `.toml` file doesn't exist
- Reports `WARN` for capability dirs with no mapping declared in the script

---

## Adding a New Capability

1. Create `capabilities/<name>/<provider>.toml` with `[deps]`, `[roles.mcp]`, optional `[[mcp.servers]]`
2. Add a `link "<name>" "<provider>.toml"` line to `scripts/setup-symlinks.sh`
3. Run `bash scripts/setup-symlinks.sh` to create the symlink
4. Use `capabilities = ["...", "<name>"]` in any agent that needs it

---

## bin/load

`bin/load <domain>:<spec>` (Python 3, no external deps):

1. Reads `agents/<domain>/<spec>.toml`
2. Extracts `capabilities = [...]`
3. Loads each `capabilities/<name>/default.toml`
4. Merges: `[deps].require`, `server_refs`, `allowed_tools`, `[[mcp.servers]]` (deduplicated by name)
5. Strips `capabilities =` line and `[deps]` from agent file
6. Injects merged `[roles.mcp]` (creates section if absent)
7. Outputs final TOML to stdout

---

## CI / Validation

```bash
# Lint all manifests (TOML validity, required fields, no name= set)
bash scripts/lint-manifests.sh

# Validate capability resolution for all agents
bash scripts/validate-capabilities.sh

# Both run in .github/workflows/lint.yml on every push/PR
```

The lint script skips the `server_refs` cross-check for capability-driven agents (those with `capabilities =` at top level), since MCP wiring is resolved at runtime.

---

## Canonical Manifest Template

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description.

capabilities = ["core", "filesystem"]   # REQUIRED — the only way to wire MCP tools

[[roles]]
system = """
You are a <persona> assistant.
Working directory: {{CWD}}
"""
welcome = "🔧 <Short greeting>. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0

# Optional: model override
# model = "openrouter:anthropic/claude-sonnet-4"

# Optional: dep scripts
# [deps]
# require = ["nodejs/node"]

# Optional: custom MCP servers NOT covered by any capability
# [[mcp.servers]]
# name = "my-server"
# type = "stdio"
# command = "npx"
# args = ["-y", "my-mcp-server"]
# timeout_seconds = 60
# tools = []
```
