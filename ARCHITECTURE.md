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
| `filesystem`   | octofs                 | `view`, `shell`, `text_editor`, `workdir` |
| `codesearch`   | octocode               | `semantic_search`, `structural_search`, `graphrag`, `view_signatures`      |
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
# Capability: <name>
# Provider: <provider-name>
# Title: <Short Capability Title (5–60 chars)>
# Description: <What this capability provides (20–160 chars)>

[deps]
require = ["muvon/octocode"]

[roles.mcp]
server_refs = ["octocode"]
allowed_tools = ["octocode:*"]

# Optional: [[mcp.servers]] if the provider needs a custom MCP server
[[mcp.servers]]
name = "octocode"
type = "stdio"
command = "octocode"
args = ["mcp"]
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
    validate        # Optional: executable script — validates LLM output quality
    scripts/        # Optional: executable scripts the skill references
    references/     # Optional: supplementary docs (REFERENCE.md, etc.)
    assets/         # Optional: templates, config files, resources
```

### SKILL.md frontmatter

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | ✅ | Max 64 chars. Lowercase letters, numbers, hyphens. No leading/trailing hyphen. Must match directory name. |
| `title` | ✅ | 5–60 chars. Short human-readable label for the skill. |
| `description` | ✅ | 20–1024 chars. What the skill does and when to use it. |
| `capabilities` | optional | Capabilities to auto-load when skill activates. Space-delimited or array: `git memory` or `["git", "memory"]`. |
| `domains` | optional | Agent categories for auto-activation scoping. Space-delimited or array. Without this, skill is manual-only. |
| `rules` | optional | Auto-activation rules — list of expressions evaluated against the project and conversation. See [Auto-activation rules](#auto-activation-rules). |
| `license` | optional | License name or path to bundled license file. |
| `compatibility` | optional | Max 500 chars. Environment requirements (tools, OS, network). |
| `metadata` | optional | Arbitrary key-value mapping (author, version, tags). |
| `allowed-tools` | optional | Space-delimited pre-approved tools (experimental). |

### Activation: three methods

**Environment variable** — preload skills at session start:
```bash
OCTOMIND_SKILLS=programming-rust,git-workflow octomind run developer:general
```
Comma-delimited skill names. Activated permanently, no rules evaluated.

**Auto-activation** — skills with a `rules:` frontmatter field are automatically evaluated on conversation events. The system scans skills whose `domains` match the current agent's role, evaluates their rules, and activates matching skills. Already-active skills (including env-loaded) are skipped.

**Manual activation** — the AI calls the `skill` MCP tool or user runs `/skill` command:

- `skill(action="use", name="<name>")` or `/skill use <name>` — inject skill into context
- `skill(action="forget", name="<name>")` or `/skill forget <name>` — remove skill
- `skill(action="list")` or `/skill list` — discover available skills

### Auto-activation rules

The `rules:` frontmatter field declares a list of expressions that determine when a skill should auto-activate. Rules are evaluated against the project working directory and the current conversation.

#### Logic: OR between items, AND within a single item

Each list item (`- ...`) is an **OR branch** — if any item matches, the skill activates.
Multiple expressions on the **same line** (space-separated) act as **AND** — all must match.

```yaml
rules:
  - file(Cargo.toml)              # OR: activates if Cargo.toml exists
  - content(rust)                 # OR: activates if user message contains "rust"
  - file(Cargo.toml) content(async)  # OR: activates if BOTH conditions are true
```

#### Rule expressions

| Expression | Matches when |
|------------|-------------|
| `file(<glob>)` | A file matching the glob pattern exists in the working directory. Supports `*` and `**`. Examples: `file(Cargo.toml)`, `file(*.rs)`, `file(src/**/*.go)` |
| `content(<word>)` | The user's message contains the word as a whole-word match (word-boundary aware, case-insensitive). Example: `content(rust)` matches "Rust" but not "rusty" |
| `match(<pattern>)` | The user's message matches the regular expression pattern. Example: `match(fix.*bug)` |
| `grep(<pattern>, <glob>)` | A file matching the glob contains a line matching the pattern. Example: `grep(tokio, Cargo.toml)`, `grep(use async_trait, src/**/*.rs)` |
| `env(<VAR>)` | The environment variable `VAR` is set (non-empty). Example: `env(CI)` |
| `env(<VAR>=<value>)` | The environment variable `VAR` equals `value`. Example: `env(NODE_ENV=production)` |
| `bin(<command>)` | The command is available in `$PATH`. Use to detect installed runtimes or tools. Example: `bin(cargo)`, `bin(docker)`, `bin(kubectl)` |
| `workdir(<pattern>)` | The current working directory path contains the pattern (substring match). Example: `workdir(projects/backend)`, `workdir(monorepo)` |
| `session(<word>)` | The current session name contains the word (case-insensitive substring). Example: `session(rust)` activates when running `octomind run developer:rust` |

#### Full example

```yaml
rules:
  - file(Cargo.toml)                        # Rust project marker
  - file(*.rs)                              # any .rs file in workdir
  - content(rust) content(async)            # user mentions both "rust" AND "async"
  - grep(tokio, Cargo.toml)                 # project uses tokio
  - match(rewrite.*in rust)                 # user asks to rewrite something in Rust
  - env(RUSTUP_HOME)                        # rustup is configured
  - bin(cargo)                              # cargo is installed (Rust toolchain present)
  - workdir(rust-projects)                  # working dir path contains "rust-projects"
  - session(rust)                           # running under a rust-tagged agent session
```

Skills without `rules:` are manual-only — they never auto-activate.

### validate script

An executable file at `skills/<name>/validate`. Checks LLM output quality deterministically.

- `argv[1]` = event type: `user` | `assistant` | `turn`
- `stdin` = event content (user message, assistant response, or turn summary with tool names)
- **exit 0** = output is valid
- **exit non-zero** = invalid. stderr (or stdout if stderr empty) is captured and fed back to the LLM as an error message for correction.

### Capabilities auto-loading

When a skill declares `capabilities: git memory`, activating the skill resolves each capability from tap files (`capabilities/<name>/<provider>.toml`) and automatically loads the backing MCP servers. This replaces the previous warning about missing tools.

### Domain scoping

The `domains` field limits auto-activation to relevant agent categories:

```yaml
domains: developer devops
```

Only agents with matching role names (e.g., `developer:rust`) evaluate this skill's `rules`. Skills without `domains` are manual-only (backward compatible).

### Validation

```bash
# Lint all skills
bash scripts/lint-skills.sh

# Lint a specific skill
bash scripts/lint-skills.sh skills/git-workflow
```

The lint script validates:
- Valid YAML frontmatter (delimited by `---`)
- Required fields: `name`, `title`, `description`
- `name` format and length constraints
- `name` matches directory name
- `title` length (5–60 chars)
- `description` length (20–1024 chars) and `compatibility` length limits
- Non-empty body after frontmatter
- `validate` script is executable if it exists

### Skill vs Agent

Skills and agents serve different purposes:

| | Skill | Agent |
|---|---|---|
| **File** | `skills/<name>/SKILL.md` | `agents/<domain>/<spec>.toml` |
| **Activation** | Manual via `skill` tool, or auto via `rules:` frontmatter field | `octomind run domain:spec` |
| **What it provides** | Domain knowledge + capabilities + validation | Full role: model, tools, system prompt |
| **Composable** | Yes — multiple skills per session | No — one role per session |
| **Auto-expand** | Yes — skills can auto-load MCP servers via capabilities | No — tools are static |

---

## CI / Validation

```bash
# Lint all manifests (TOML validity, required fields, title/description, no name= set)
bash scripts/lint-manifests.sh

# Lint all capabilities (TOML validity, title/description, MCP server description)
bash scripts/lint-capabilities.sh

# Lint all skills (frontmatter validity, required fields incl. title)
bash scripts/lint-skills.sh

# Validate capability resolution for all agents
bash scripts/validate-capabilities.sh

# All four run in .github/workflows/lint.yml on every push/PR
```

The lint script skips the `server_refs` cross-check for capability-driven agents (those with `capabilities =` at top level), since MCP wiring is resolved at runtime.

---

## Metadata Comments

All agents and capabilities require `# Title:` and `# Description:` comment lines:

| Entity | Field | Constraints |
|--------|-------|-------------|
| Agent | `# Title:` | 5–60 chars. Short human-readable label. |
| Agent | `# Description:` | 20–160 chars. What the agent does. |
| Capability | `# Title:` | 5–60 chars. Short capability label. |
| Capability | `# Description:` | 20–160 chars. What the capability provides. |

---

## Canonical Manifest Template

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Title: Short Agent Title
# Description: One-line description of what this agent does.

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
