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
    rust-nightly.toml
    python.toml
    go.toml
  devops/
    k8s.toml
    k8s-helm.toml
    docker.toml
  data/
    python-ml.toml
    sql.toml
  ...
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

Each file lives at `agents/<domain>/<spec>.toml` and is fetched via:
```
https://raw.githubusercontent.com/muvon/octomind-agents/main/agents/<domain>/<spec>.toml
```

---

## Manifest Format

A manifest is a TOML file with one required `[[roles]]` entry and optional `[[mcp.servers]]` entries.

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
server_refs = ["core", "filesystem", "agent"]
allowed_tools = ["core:*", "filesystem:*", "agent_*"]

# Optional: add extra MCP servers (e.g. language-specific tooling via Docker)
# [[mcp.servers]]
# name = "rust-analyzer-mcp"
# type = "stdin"
# command = "docker"
# args = ["run", "--rm", "-i", "--volume", "{{CWD}}:/workspace", "ghcr.io/muvon/rust-analyzer-mcp:latest"]
# timeout_seconds = 60
```

### Placeholder Variables

| Placeholder | Resolved to |
|-------------|-------------|
| `{{CWD}}` | Current working directory at runtime |
| `{{INPUT:KEY}}` | Prompts user once, stored in `~/.local/share/octomind/inputs.toml` |
| `{{ENV:KEY}}` | Reads from environment; if unset, prompts user and saves to `./.env` |
| `{{SYSTEM}}` | Full system info (shell, OS, binaries, CWD) |
| `{{CONTEXT}}` | Project context (README, git status, file tree) |
| `{{DATE}}` | Current date and time with timezone |
| `{{ROLE}}` | Active role name |

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

Each entry maps to `deps/<org>/<tool>.sh` inside the tap. Scripts run in order, **before** MCP servers are initialised. If any script exits non-zero the session is aborted with a clear error.

### Script contract

Every dep script **must** follow this contract so the runtime can trust it:

| Rule | Detail |
|------|--------|
| **Idempotent** | Check first — exit `0` immediately if the tool is already installed |
| **Exit codes** | `0` = installed (or already present), `1` = failed |
| **Output** | Stderr only — stdout is reserved for Octomind |
| **No side-effects** | Do not modify the user's config, shell profile, or working directory |

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
source "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/lib/platform.sh"

# Fast path — already installed
if pkg_check <tool>; then
  exit 0
fi

info "<tool> not found — installing..."

case "$OS" in
  macos) brew_install <formula> ;;
  linux) pkg_install <package>  ;;
esac
```

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
server_refs = ["core", "filesystem", "agent"]
allowed_tools = ["core:*", "filesystem:*", "agent_*"]

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

## License

Apache 2.0 — see [LICENSE](LICENSE).
