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

A **capability** is something an agent can do, achievable by different tools (providers).
Agents declare capabilities; the runtime resolves providers and injects dependencies.

Each capability name maps to `capabilities/<name>/default.toml` (a symlink to the active provider).
Users can override providers via `[capabilities]` in their config (e.g. `websearch = "brave"`).

Use prefix naming to group related capabilities: `programming-python`, `programming-rust`, etc.

```
agents/developer/rust.toml
  └── capabilities = ["core", "filesystem", "codesearch", "programming-rust"]
           │
           ▼
  bin/load developer:rust
           │
           ├── capabilities/core/default.toml              (built-in)
           ├── capabilities/filesystem/default.toml        → octofs.toml
           ├── capabilities/codesearch/default.toml        → octocode.toml
           └── capabilities/programming-rust/default.toml  → cargo.toml
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

| Capability     | Providers              | What it provides                                      |
|----------------|------------------------|-------------------------------------------------------|
| `core`         | default                | `plan` task tracker                                   |
| `agent`        | default                | `agent_*` delegation tools                            |
| `filesystem`   | octofs                 | `view`, `shell`, `text_editor`, `workdir`, `ast_grep` |
| `codesearch`   | octocode               | `semantic_search`, `graphrag`, `view_signatures`      |
| `memory`       | octobrain              | `remember`, `memorize`                                |
| `websearch`    | tavily                 | web search and content extraction                     |
| `versioning`   | git                    | git operations                                        |
| `programming-python`  | uv               | Python runtime (uv, uvx)                              |
| `programming-rust`    | cargo            | Rust toolchain (cargo, rustc, clippy, rustfmt)        |
| `programming-nodejs`  | node             | Node.js runtime (node, npm, npx)                      |
| `docker`              | docker           | Docker CLI (docker, docker-compose)                   |
| `kubernetes`          | kubernetes       | Kubernetes CLI (kubectl, helm)                        |
| `svelte`              | svelte           | Svelte/SvelteKit documentation MCP server             |
| `medical`             | medical          | medical references (PubMed, FDA, WHO, RxNorm)         |
| `finance`             | yfinance         | financial data (Yahoo Finance)                        |

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
2. **Never write `[roles.mcp]`** in an agent — injected by `bin/load` from capabilities.
3. **Never write `[deps]`** in an agent — deps belong in capability files only.
4. **Never write `[[mcp.servers]]`** in an agent — MCP servers belong in capability files.
5. **Never set `name`** in `[[roles]]` — injected from the tag at runtime.
6. **One `[[roles]]` per file** — no multi-role manifests.
7. **File path must match tag** — `developer:rust` → `agents/developer/rust.toml`.

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
3. Run `bash scripts/setup-symlinks.sh` to create the default symlink
4. Use `"<name>"` (default provider) or `"<name>:<provider>"` (explicit) in any agent

To add an alternative provider to an existing capability:
1. Create `capabilities/<name>/<new-provider>.toml`
2. Use `"<name>:<new-provider>"` in agents that need it

---

## bin/load

`bin/load <domain>:<spec>` (Python 3, no external deps):

1. Reads `agents/<domain>/<spec>.toml`
2. Extracts `capabilities = [...]`
3. For each capability reference, resolves provider:
   - `"name"` → `capabilities/<name>/default.toml`
   - `"name:provider"` → `capabilities/<name>/<provider>.toml`
4. Merges: `[deps].require`, `server_refs`, `allowed_tools`, `[[mcp.servers]]` (deduplicated by name)
5. Strips `capabilities =` line from agent file
6. Injects merged `[roles.mcp]` (creates section if absent)
7. Outputs final TOML to stdout

---

## Skills

Skills are reusable instruction packs stored alongside agents in the tap. They follow the [AgentSkills specification](https://agentskills.io/specification).

### Directory layout

```
skills/
  <skill-name>/
    SKILL.md        # Required: YAML frontmatter + instruction body
    scripts/        # Optional: executable scripts the skill references
    references/     # Optional: supplementary docs (REFERENCE.md, etc.)
    assets/         # Optional: templates, config files, resources
```

### SKILL.md frontmatter

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | ✅ | Max 64 chars. Lowercase letters, numbers, hyphens. No leading/trailing hyphen. Must match directory name. |
| `description` | ✅ | Max 1024 chars. Non-empty. What the skill does and when to use it. |
| `license` | optional | License name or path to bundled license file. |
| `compatibility` | optional | Max 500 chars. Environment requirements (tools, OS, network). |
| `metadata` | optional | Arbitrary key-value mapping (author, version, tags). |
| `allowed-tools` | optional | Space-delimited pre-approved tools (experimental). |

### How Octomind discovers and injects skills

1. The `skill` MCP tool (built into Octomind core) scans all active taps for `skills/*/SKILL.md`
2. `skill(action="list")` returns all discovered skills with their metadata
3. `skill(action="use", name="<name>")` reads the full `SKILL.md` and injects it into the session context
4. `skill(action="forget", name="<name>")` removes the skill and triggers conversation compression

Skills are **not** loaded automatically — the AI must explicitly activate them. This keeps context lean.

### Validation

```bash
# Lint all skills
bash scripts/lint-skills.sh

# Lint a specific skill
bash scripts/lint-skills.sh skills/git-workflow
```

The lint script validates:
- Valid YAML frontmatter (delimited by `---`)
- Required fields: `name`, `description`
- `name` format and length constraints
- `name` matches directory name
- `description` and `compatibility` length limits
- Non-empty body after frontmatter

### Skill vs Agent

Skills and agents serve different purposes:

| | Skill | Agent |
|---|---|---|
| **File** | `skills/<name>/SKILL.md` | `agents/<domain>/<spec>.toml` |
| **Activation** | `skill(action="use", name="...")` | `octomind run domain:spec` |
| **What it provides** | Domain knowledge injected into context | Full role: model, tools, system prompt |
| **Composable** | Yes — multiple skills per session | No — one role per session |

---

## CI / Validation

```bash
# Lint all manifests (TOML validity, required fields, no name= set)
bash scripts/lint-manifests.sh

# Lint all skills (frontmatter validity, required fields, name format)
bash scripts/lint-skills.sh

# Validate capability resolution for all agents
bash scripts/validate-capabilities.sh

# All three run in .github/workflows/lint.yml on every push/PR
```

The lint script skips the `server_refs` cross-check for capability-driven agents (those with `capabilities =` at top level), since MCP wiring is resolved at runtime.

---

## Canonical Manifest Template

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description.

capabilities = ["core", "filesystem", "programming-python"]   # REQUIRED

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
```
