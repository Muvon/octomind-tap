# Octomind Agents Registry

Community-maintained collection of agent manifests for [Octomind](https://github.com/muvon/octomind) — a session-based AI development assistant.

Each manifest is a single TOML file that defines a role (system prompt, model, tools) and optional MCP servers. Octomind fetches and merges it into your config at runtime — no installation, no global state.

---

## Quick Start

```bash
# Run a registry agent directly
octomind run developer:rust

# Pin to a specific version
octomind run developer:rust@1.0

# With a sub-variant
octomind run developer:rust-nightly
```

---

## Tag Format

```
domain:spec[-sub-spec][@version]
```

| Part | Required | Description |
|------|----------|-------------|
| `domain` | ✅ | Top-level category (e.g. `developer`, `devops`, `data`) |
| `spec` | ✅ | Primary specialisation (e.g. `rust`, `python`, `k8s`) |
| `-sub-spec` | optional | Variant of the spec (e.g. `rust-nightly`, `python-ml`) |
| `@version` | optional | Pinned version tag (e.g. `@1.0`, `@2025-06`). Omit for latest. |

**Examples:**

```
developer:rust                 → agents/developer/rust.toml
developer:rust-nightly         → agents/developer/rust-nightly.toml
developer:rust@1.0             → agents/developer/rust.toml  (version hint, future use)
devops:k8s-helm                → agents/devops/k8s-helm.toml
data:python-ml                 → agents/data/python-ml.toml
```

> **Note on versioning:** Version (`@x.y`) is parsed and passed through but the registry currently resolves to the same file path. Versioned paths (e.g. `agents/developer/rust@1.0.toml`) are reserved for future use. For now, use the unversioned tag and rely on the 24-hour cache TTL.

---

## Repository Layout

```
agents/
  developer/
    rust.toml
    typescript.toml
    general.toml
  devops/
    kubernetes.toml
  octomind/
    tap.toml          ← octomind:tap  — tap management agent
    skill.toml        ← octomind:skill — skill development agent
  security/
    owasp.toml
  ...
skills/
  git-workflow/
    SKILL.md          ← git commit conventions and workflow best practices
  code-review/
    SKILL.md          ← code review checklist and guidelines
  ...                 ← community skills (one directory per skill)
capabilities/
  core/
    default.toml      ← plan tool (built-in, no symlink needed)
  agent/
    default.toml      ← agent delegation (built-in, no symlink needed)
  filesystem/
    octofs.toml       ← provider: octofs MCP
    default.toml      → octofs.toml  (symlink, set by setup-symlinks.sh)
  codesearch/
    octocode.toml     ← provider: octocode MCP
    default.toml      → octocode.toml
  memory/
    octobrain.toml    ← provider: octobrain MCP
    default.toml      → octobrain.toml
  websearch/
    tavily.toml       ← provider: Tavily search MCP
    brave.toml        ← provider: Brave search MCP  (alternative)
    default.toml      → tavily.toml  (switch with: ln -sf brave.toml ...)
  versioning/
    git.toml          ← provider: git via shell
    default.toml      → git.toml
deps/
  lib/
    platform.sh       ← shared OS/arch/pkg-manager detection (sourced by all dep scripts)
  muvon/
    octocode.sh
  astral-sh/
    uv.sh
  nodejs/
    node.sh
  ...
templates/
  agent.toml          ← canonical agent manifest template
  skill.md            ← canonical SKILL.md template
bin/
  load              ← resolves capabilities and outputs a merged manifest to stdout
scripts/
  setup-symlinks.sh ← creates/forces default.toml symlinks; warns on missing providers
  lint-manifests.sh ← validates all agent TOML files
  lint-skills.sh    ← validates all skills/*/SKILL.md files per AgentSkills spec
  validate-capabilities.sh ← runs bin/load on every agent to catch resolution errors
```

Each agent file lives at `agents/<domain>/<spec>.toml` and is fetched via:
```
https://raw.githubusercontent.com/muvon/octomind-agents/main/agents/<domain>/<spec>.toml
```

---

## Capability System

Agents declare **capabilities** instead of hardcoding MCP servers. This decouples what an agent *needs* from *how* it is provided.

### How it works

1. An agent declares `capabilities = ["filesystem", "codesearch", "websearch"]` at the top of its manifest.
2. At runtime, `bin/load <domain>:<spec>` resolves each capability to `capabilities/<name>/default.toml`.
3. `default.toml` is a symlink pointing to the active provider (e.g. `octofs.toml`, `tavily.toml`).
4. `bin/load` merges all `[deps]`, `server_refs`, `allowed_tools`, and `[[mcp.servers]]` blocks into the final manifest output.

### Available capabilities

| Capability | What it provides | Default provider |
|------------|-----------------|-----------------|
| `core` | `plan` task tracker | `core/default.toml` (built-in) |
| `agent` | `agent_*` delegation tools | `agent/default.toml` (built-in) |
| `filesystem` | `view`, `shell`, `text_editor`, `workdir` | `octofs.toml` |
| `codesearch` | `semantic_search`, `structural_search`, `graphrag`, `view_signatures` | `octocode.toml` |
| `memory` | `remember`, `memorize` | `octobrain.toml` |
| `websearch` | web search tool | `tavily.toml` |
| `versioning` | git operations via shell | `git.toml` |

### Switching providers

```bash
# Switch websearch from Tavily to Brave
ln -sf brave.toml capabilities/websearch/default.toml

# Or run the setup script to reset all defaults
bash scripts/setup-symlinks.sh
```

### Setup after cloning

```bash
bash scripts/setup-symlinks.sh   # create/force all default.toml symlinks
chmod +x bin/load

# Validate all agents resolve correctly
bash scripts/validate-capabilities.sh
```

### Writing a capability-driven agent

```toml
# agents/developer/rust.toml

capabilities = ["core", "filesystem", "codesearch", "versioning"]

[[roles]]
system = "..."
welcome = "🦀 Rust agent ready."
temperature = 0.2
top_p = 0.9
top_k = 0

# No [roles.mcp] needed — bin/load injects it from capabilities
# Add custom MCP servers here only for things NOT covered by capabilities:
# [[mcp.servers]]
# name = "my-special-server"
# ...
```

`bin/load` merges everything and outputs a complete, ready-to-use manifest to stdout.

---

## Manifest Format

A manifest is a TOML file with one required `[[roles]]` entry. Agents use either `capabilities = [...]` (preferred) or explicit `[roles.mcp]` + `[[mcp.servers]]` blocks.

```toml
# agents/developer/rust.toml

[[roles]]
# name is injected automatically from the tag — do not set it
system = """
You are an expert Rust developer assistant.
Working directory: {{CWD}}

You write idiomatic, safe, performant Rust...
"""
welcome = "🦀 Rust developer agent ready. Working in {{CWD}}"
temperature = 0.2
top_p = 0.9
top_k = 0

# Optional: override the global model for this role
# model = "anthropic/claude-sonnet-4-5"

[roles.mcp]
server_refs = ["core", "octofs", "agent"]
allowed_tools = ["core:*", "octofs:*", "agent_*"]

# Optional: add extra MCP servers (e.g. language-specific tooling via Docker)
# [[mcp.servers]]
# name = "rust-analyzer-mcp"
# type = "stdio"
# command = "docker"
# args = ["run", "--rm", "-i", "--volume", "{{CWD}}:/workspace", "ghcr.io/muvon/rust-analyzer-mcp:latest"]
# timeout_seconds = 60
# tools = []
```

### MCP Server Configuration

**Important:** `server_refs` and `[[mcp.servers]]` serve different purposes:

| Field | Purpose |
|-------|---------|
| `server_refs` | References servers that are **already defined** in the user's config (built-in: `core`, `octofs`, `agent`, `octocode`) or defined in this manifest's `[[mcp.servers]]` |
| `[[mcp.servers]]` | **Defines new MCP servers** that will be started when this agent runs |

**To use a custom MCP server:**

1. Define it in `[[mcp.servers]]` with name, type, command, args
2. Reference it in `server_refs` to make it available to the agent
3. (Optional) Restrict tools in `allowed_tools`

```toml
# Example: Adding a custom MCP server

[roles.mcp]
server_refs = ["core", "agent", "my-custom-server"]
allowed_tools = ["core:*", "agent:*", "my-custom-server:my_custom-tool"]

[[mcp.servers]]
name = "my-custom-server"
type = "stdio"
command = "npx"
args = ["-y", "my-mcp-server"]
timeout_seconds = 60
tools = []
```

**Built-in servers** (always available, no `[[mcp.servers]]` needed):
- `core` — `plan`, `mcp`, `agent` tools
- `agent` — `agent_*` tools for delegating to layers

### Placeholder Variables

Run `octomind vars` to see all available placeholders:

```bash
octomind vars              # List all placeholders
octomind vars --preview    # Show preview values
octomind vars --expand     # Show full values
```

**Special placeholders:**

| Placeholder | Description |
|-------------|-------------|
| `{{INPUT:KEY}}` | Prompts user once, stored in `~/.local/share/octomind/inputs.toml` |
| `{{ENV:KEY}}` | Reads from environment; if unset, prompts and saves to `./.env` |

#### `{{INPUT:KEY}}` — persistent credential store

Use for **secrets that belong to the user globally** — API tokens, personal access tokens, license keys. The user is prompted once on first use; the value is saved to `~/.local/share/octomind/inputs.toml` and reused on every subsequent run across all projects.

```toml
system = """
GitHub token: {{INPUT:GITHUB_TOKEN}}
"""
```

#### `{{ENV:KEY}}` — environment variable with `.env` fallback

Use for **project-scoped or deployment-specific values** — base URLs, feature flags, environment names, project IDs. The resolution order is:

1. If `KEY` is already set in the environment (and non-empty) → use it directly, no prompt.
2. If not set → prompt the user, then append `KEY=VALUE` to `./.env` in the current working directory.

On the next run Octomind loads `.env` automatically, so the user is never prompted again for that project. The value also becomes available to MCP tools and shell commands in the session immediately.

```toml
system = """
API base URL: {{ENV:API_BASE_URL}}
Environment: {{ENV:DEPLOY_ENV}}
"""
```

**When to use which:**

| Situation | Use |
|-----------|-----|
| API token / secret key (global, user-owned) | `{{INPUT:KEY}}` |
| Project base URL / environment name / feature flag | `{{ENV:KEY}}` |
| Value already set in CI/CD environment | `{{ENV:KEY}}` |
| Value that should never touch the filesystem | `{{INPUT:KEY}}` |

### Role Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ❌ omit | Injected automatically from the tag at runtime |
| `system` | ✅ | System prompt for the AI |
| `welcome` | ✅ | Message shown when the session starts |
| `temperature` | ✅ | Sampling temperature (0.0–1.0) |
| `top_p` | ✅ | Nucleus sampling (0.0–1.0) |
| `top_k` | ✅ | Top-k sampling (0 = disabled) |
| `model` | optional | Override the global model (e.g. `anthropic/claude-opus-4-5`) |
| `mcp` | optional | MCP server refs and tool allow-list |
| `deps` | optional | List of dep scripts to run before the session starts |

### Merge Semantics

When Octomind loads a manifest it **additively merges** it into the user's base config:

- `[[roles]]` — appended; duplicates (by `name`) are skipped
- `[[mcp.servers]]` — appended; duplicates (by `name`) are skipped
- Everything else — override semantics (manifest wins)

This means your personal config is never destructively modified.

---

## How Taps Work

Taps are Git repositories containing agent manifests. Octomind uses a Homebrew-style tap system:

- **Default tap** (`muvon/tap`) is always active — cloned automatically on first use and updated on every `octomind run`.
- **User taps** are checked before the default tap (first match wins).

### Managing Taps

```bash
# Add a GitHub tap (clones https://github.com/myorg/octomind-agents)
octomind tap myorg/agents

# Add a local tap (no clone — uses directory directly)
octomind tap myorg/agents /path/to/local/repo

# List all active taps
octomind tap

# Remove a tap
octomind untap myorg/agents
```

Tap repos are cloned to `~/.local/share/octomind/taps/<user>/octomind-<repo>/` and auto-updated via `git pull` on every run.

---

## Dependency Scripts

Manifests can declare external tools that must be present before the session starts. Octomind runs the corresponding scripts automatically on first use.

### Declaring deps in a manifest

```toml
[deps]
require = ["astral-sh/uv", "nodejs/node"]
```

Each entry maps to `deps/<org>/<tool>.sh` inside the tap. Scripts run before MCP servers are initialised. If any script exits non-zero the session is aborted with a clear error.

Each script is **self-sufficient** — if it needs another tool (e.g. `cargo`), it invokes that dep script directly. No ordering required in the manifest.

### Script contract

Every dep script **must** follow two rules:

1. **Self-sufficient** — if it needs another tool to run (e.g. `cargo`), it `source`s that dep script itself. The caller never needs to set anything up beforehand.
2. **Idempotent** — exits `0` immediately if the tool is already installed. Safe to run twice, ten times, on every session start.

| Rule | Detail |
|------|--------|
| **Self-sufficient** | `source` prerequisite dep scripts directly — do not assume the caller did it |
| **Idempotent** | Fast-path `exit 0` if already installed — no side effects on repeat runs |
| **Exit codes** | `0` = ready to use, non-zero = failed |
| **Output** | Stderr only — stdout is reserved for Octomind |
| **No profile changes** | Do not modify `.bashrc`, `.zshrc`, or any shell profile |

### Using the platform library

All dep scripts should source `deps/lib/platform.sh` for portable OS/arch/package-manager detection:

```bash
#!/usr/bin/env bash
source "$(dirname "${BASH_SOURCE[0]}")/../lib/platform.sh"
# (adjust relative path depth to match your location under deps/)
```

After sourcing, these are available:

| Variable | Values |
|----------|--------|
| `$OS` | `macos` \| `linux` |
| `$ARCH` | `x86_64` \| `arm64` |
| `$PKG_MANAGER` | `brew` \| `apt` \| `dnf` \| `pacman` \| `zypper` \| `apk` \| `unknown` |
| `$IS_MACOS` / `$IS_LINUX` | `1` or `0` |
| `$IS_X86_64` / `$IS_ARM64` | `1` or `0` |

Helper functions: `pkg_install <pkg>`, `pkg_check <cmd>`, `info <msg>`, `die <msg>`.

### Minimal dep script template

```bash
#!/usr/bin/env bash
# dep: <org>/<tool>
# description: One-line description
# check: <command-to-verify-install>

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check <tool>; then
	exit 0
fi

# If this script depends on another dep, use install_dep:
# install_dep rust/cargo
# This runs the dep script and sources common env files (~/.cargo/env, ~/.local/bin).

info "<tool> not found — installing..."

case "$OS" in
	macos) brew_install <formula> ;;
	linux) pkg_install <package>  ;;
esac
```

### Available Dep Scripts

| Script | Provides | Used For |
|--------|----------|----------|
| `rust/cargo` | Rust toolchain (cargo, rustc) | Building Rust binaries, installing crates |
| `astral-sh/uv` | uv package manager | Running Python MCP servers via `uvx` |
| `nodejs/node` | Node.js LTS (node, npm, npx) | Running Node.js MCP servers via `npx` |
| `docker/docker` | Docker CLI + daemon | Running containerized MCP servers |
| `github/github-mcp` | GitHub MCP Server | Full GitHub API operations (repos, issues, PRs) |
| `microsoft/playwright` | Playwright MCP Server | Browser automation, screenshots, web scraping |
| `brave/brave-search` | Brave Search MCP Server | Web search via Brave Search API |
| `upstash/context7` | Context7 MCP Server | Up-to-date library documentation |
| `muvon/octocode` | octocode CLI | Octomind's semantic code search |
| `muvon/octobrain` | octobrain CLI | Octomind's code indexing |
| `muvon/octofs` | octofs CLI | Octomind's file editing and viewing tool |

### MCP Server Runtime Requirements

| Runtime | MCP Servers (examples) | Dep Required |
|---------|------------------------|--------------|
| **Node.js (npx)** | github, postgres, sqlite, brave-search, puppeteer, slack, memory, context7 | `nodejs/node` |
| **Python (uvx)** | Many Python-based servers | `astral-sh/uv` |
| **Rust (cargo)** | octocode, octobrain, octofs, other compiled binaries | `rust/cargo` |
| **Docker** | Containerized MCP servers | `docker/docker` |

### Popular MCP Servers and Their Deps

| MCP Server | Package | Dep Required |
|-----------|---------|--------------|
| GitHub | `@github/mcp-server` | `github/github-mcp` (or `nodejs/node`) |
| Playwright | `@playwright/mcp` | `microsoft/playwright` (or `nodejs/node`) |
| Brave Search | `@brave/brave-search-mcp-server` | `brave/brave-search` (or `nodejs/node`) |
| Context7 | `@upstash/context7-mcp` | `upstash/context7` (or `nodejs/node`) |
| Octofs | `octofs` CLI | `muvon/octofs` |
| Postgres | `@modelcontextprotocol/server-postgres` | `nodejs/node` |
| SQLite | `@modelcontextprotocol/server-sqlite` | `nodejs/node` |
| Memory | `@modelcontextprotocol/server-memory` | `nodejs/node` |
| Puppeteer | `@modelcontextprotocol/server-puppeteer` | `nodejs/node` |
| Slack | `@modelcontextprotocol/server-slack` | `nodejs/node` |

**Note:** `@modelcontextprotocol/*` is the npm namespace for MCP reference implementations, not an org. For generic Node.js MCP servers, just use `nodejs/node` dep.

### Adding a dep script

1. Create `deps/<org>/<tool>.sh` — use the template above.
2. `chmod +x deps/<org>/<tool>.sh`
3. Reference it in your manifest: `[deps] require = ["<org>/<tool>"]`
4. Test it on a clean machine (or a Docker container) before opening a PR.

## Contributing

### Adding a New Agent

1. **Pick a tag** following the naming convention: `domain:spec` or `domain:spec-sub-spec`.
2. **Create the file** at `agents/<domain>/<spec>.toml` (or `agents/<domain>/<spec>-<sub>.toml`).
3. **Use the template** below as a starting point.
4. **Test locally** before opening a PR:

```bash
# Add this repo as a local tap (one-time setup)
octomind tap muvon/tap /path/to/octomind-tap

# Run your agent
octomind run developer:your-new-agent

# Remove the local override when done
octomind untap muvon/tap
```

5. **Open a PR** with a short description of what the agent does and which tools/models it targets.

### Manifest Template

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description of what this agent does.

[[roles]]
# name is NOT set here — Octomind injects it automatically from the tag at runtime.
system = """
<Your system prompt here.>

Working directory: {{CWD}}

# Use {{INPUT:KEY}} for user-global secrets (API tokens, credentials).
# Prompted once, stored in ~/.local/share/octomind/inputs.toml.
# Example: GitHub token: {{INPUT:GITHUB_TOKEN}}

# Use {{ENV:KEY}} for project-scoped values (base URLs, env names, flags).
# Reads from environment if set; otherwise prompts and saves to ./.env.
# Example: API base: {{ENV:API_BASE_URL}}
"""
welcome = "<Emoji> <Short greeting>. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0

[roles.mcp]
server_refs = ["core", "octofs", "agent"]
allowed_tools = ["core:*", "octofs:*", "agent_*"]

# Optional: declare tools that must be installed before the session starts.
# Octomind runs deps/<org>/<tool>.sh from the tap automatically.
# [deps]
# require = ["astral-sh/uv", "nodejs/node"]
```

### Guidelines

- **Never set `name`** — it is injected from the tag at runtime. Do not include it in the manifest.
- **Keep system prompts focused** — describe the persona, constraints, and preferred patterns. Avoid walls of text.
- **Prefer `{{CWD}}` over hardcoded paths** — manifests are used across machines.
- **Use `{{INPUT:KEY}}` for user-global secrets** — API tokens, credentials. Prompted once, stored in `~/.local/share/octomind/inputs.toml`, reused across all projects.
- **Use `{{ENV:KEY}}` for project-scoped values** — base URLs, environment names, feature flags. Reads from the environment if set; otherwise prompts and saves to `./.env` in the working directory. Never use `{{ENV:KEY}}` for secrets — the value lands in a plain-text file.
- **Declare deps for non-Docker tooling** — if your agent needs a CLI tool that isn't wrapped in Docker, add a dep script and reference it via `[deps] require = [...]`. See [Dependency Scripts](#dependency-scripts).
- **Docker for zero-install tooling** — if your agent needs a language server or CLI tool, wrap it in a Docker MCP server so users don't need to install anything.
- **One role per file** — a manifest should define exactly one `[[roles]]` entry (the primary agent role). Additional helper roles are discouraged.
- **Test with `file://` source** before submitting — see the local testing instructions above.

### Naming Conventions

| Domain | Use for |
|--------|---------|
| `developer` | Language-specific coding assistants |
| `devops` | Infrastructure, CI/CD, containers, cloud |
| `data` | Data engineering, ML, analytics |
| `security` | Security review, pen-testing, auditing |
| `docs` | Documentation, technical writing |
| `review` | Code review, PR analysis |

New domains are welcome — just be consistent and descriptive.

---

## Skills

Skills are reusable instruction packs that inject domain knowledge into any Octomind session on demand. Unlike agents (which define a full role), skills are **context injections** — focused, composable knowledge that any agent can activate.

Skills live in `skills/<name>/SKILL.md` and follow the [AgentSkills specification](https://agentskills.io/specification).

### Using skills in a session

```
skill(action="list")                          # discover available skills
skill(action="list", pattern="git")           # filter by name or description
skill(action="use", name="git-workflow")      # inject skill into context
skill(action="forget", name="git-workflow")   # remove skill from context
```

### Skill format

```markdown
---
name: skill-name
description: "What this skill does and when to use it."
license: Apache-2.0
compatibility: "Requires git. Works with any git-based project."
---

# Skill Title

## Overview
...

## Instructions
...

## Examples
...
```

### Auto-activation rules

Skills can declare `rules:` in their frontmatter to auto-activate when conditions are met. Rules are evaluated against the project and conversation — no user action needed.

**Logic: OR between items, AND within a single item.**

```yaml
rules:
  - file(Cargo.toml)              # activates if Cargo.toml exists in workdir
  - content(rust)                 # activates if user message contains "rust"
  - file(Cargo.toml) content(async)  # activates if BOTH are true (AND)
  - semantic(rewrite this in rust)   # activates when the user's intent is semantically close to the phrase
```

#### Rule expressions

| Expression | Matches when |
|------------|-------------|
| `file(<glob>)` | File matching glob exists in working directory. Supports `*` and `**`. |
| `content(<word>)` | User message contains the word (whole-word, case-insensitive). |
| `match(<pattern>)` | User message matches the regular expression. |
| `semantic(<phrase>)` | User message is semantically close to the phrase — intent-based, paraphrase-tolerant. Use for triggers that natural language can express many ways (e.g. `semantic(how do I land guest posts)` covers "pitch articles", "write for other blogs", "get accepted as a contributor"). |
| `grep(<pattern>, <glob>)` | A file matching the glob contains a line matching the pattern. |
| `env(<VAR>)` | Environment variable `VAR` is set (non-empty). |
| `env(<VAR>=<value>)` | Environment variable `VAR` equals `value`. |
| `bin(<command>)` | Command is available in `$PATH` (detects installed runtimes/tools). |
| `workdir(<pattern>)` | Current working directory path contains the pattern (substring). |
| `session(<word>)` | Current session name contains the word (e.g. `session(rust)` matches `developer:rust`). |

Skills without `rules:` are manual-only — they never auto-activate. Add `domains:` to scope auto-activation to specific agent categories (e.g. `domains: developer devops`).

### Creating a skill

```bash
# Copy the template
cp templates/skill.md skills/<name>/SKILL.md

# Edit and fill in frontmatter + body
# Then validate:
bash scripts/lint-skills.sh skills/<name>

# Or use the skill development agent:
octomind run octomind:skill
```

### Skill vs Agent

| | Skill | Agent |
|---|---|---|
| **What it is** | Instruction pack injected into context | Full role with model, tools, system prompt |
| **Activation** | `skill(action="use", name="...")` | `octomind run domain:spec` |
| **Scope** | Single domain concern | Complete task persona |
| **Composable** | Yes — activate multiple skills | No — one role per session |
| **File format** | `SKILL.md` (Markdown + YAML frontmatter) | `.toml` (TOML manifest) |

---

## License

Apache 2.0 — see [LICENSE](LICENSE).
