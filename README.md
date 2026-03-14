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
```

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
name = "developer:rust"          # Must match the tag (domain:spec)
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
| `{{SYSTEM}}` | Full system info (shell, OS, binaries, CWD) |
| `{{CONTEXT}}` | Project context (README, git status, file tree) |
| `{{DATE}}` | Current date and time with timezone |
| `{{ROLE}}` | Active role name |

`{{INPUT:KEY}}` is ideal for secrets (API tokens, credentials). The user is prompted once on first use; the value is cached locally and never committed anywhere.

### Role Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Must match the tag (`domain:spec` or `domain:spec-sub`) |
| `system` | ✅ | System prompt for the AI |
| `welcome` | ✅ | Message shown when the session starts |
| `temperature` | ✅ | Sampling temperature (0.0–1.0) |
| `top_p` | ✅ | Nucleus sampling (0.0–1.0) |
| `top_k` | ✅ | Top-k sampling (0 = disabled) |
| `model` | optional | Override the global model (e.g. `anthropic/claude-opus-4-5`) |
| `mcp` | optional | MCP server refs and tool allow-list |

### Merge Semantics

When Octomind loads a manifest it **additively merges** it into the user's base config:

- `[[roles]]` — appended; duplicates (by `name`) are skipped
- `[[mcp.servers]]` — appended; duplicates (by `name`) are skipped
- Everything else — override semantics (manifest wins)

This means your personal config is never destructively modified.

---

## How Caching Works

Manifests are cached at `~/.local/share/octomind/agents/<domain>/<spec>.toml`.

- **Fresh cache (< 24 h):** used immediately, no network call.
- **Stale cache (≥ 24 h):** stale copy returned immediately; refresh happens in the background.
- **No cache:** fetched synchronously from the first available source.

Cache TTL is configurable in your `config.toml`:

```toml
[registry]
sources = ["https://raw.githubusercontent.com/muvon/octomind-agents/main"]
cache_ttl_hours = 24
```

You can add private or local sources:

```toml
[registry]
sources = [
  "file://~/my-private-agents",
  "https://raw.githubusercontent.com/muvon/octomind-agents/main",
]
```

Sources are tried in order — first hit wins.

---

## Contributing

### Adding a New Agent

1. **Pick a tag** following the naming convention: `domain:spec` or `domain:spec-sub-spec`.
2. **Create the file** at `agents/<domain>/<spec>.toml` (or `agents/<domain>/<spec>-<sub>.toml`).
3. **Use the template** below as a starting point.
4. **Test locally** before opening a PR:

```bash
# Point your registry at your local checkout
# In ~/.config/octomind/config.toml:
# [registry]
# sources = ["file:///path/to/your/octomind-agents"]

octomind run developer:your-new-agent
```

5. **Open a PR** with a short description of what the agent does and which tools/models it targets.

### Manifest Template

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description of what this agent does.

[[roles]]
name = "<domain>:<spec>"
system = """
<Your system prompt here.>

Working directory: {{CWD}}
"""
welcome = "<Emoji> <Short greeting>. Working in {{CWD}}"
temperature = 0.3
top_p = 0.9
top_k = 0

[roles.mcp]
server_refs = ["core", "filesystem", "agent"]
allowed_tools = ["core:*", "filesystem:*", "agent_*"]
```

### Guidelines

- **`name` must match the tag** — `developer:rust` manifest must have `name = "developer:rust"`.
- **Keep system prompts focused** — describe the persona, constraints, and preferred patterns. Avoid walls of text.
- **Prefer `{{CWD}}` over hardcoded paths** — manifests are used across machines.
- **Use `{{INPUT:KEY}}` for secrets** — never hardcode tokens or credentials.
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
