# Contributing to octomind-tap

Thanks for contributing! This repo is the community registry of agent manifests for [Octomind](https://github.com/muvon/octomind).

---

## What is a manifest?

A manifest is a single TOML file at `agents/<domain>/<spec>.toml`. When a user runs:

```bash
octomind run developer:rust
```

Octomind fetches `agents/developer/rust.toml` from this repo and merges it into their config — no installation, no global state.

---

## Adding a new agent

### 1. Pick a tag

Follow the naming convention: `domain:spec` or `domain:spec-sub-spec`.

| Domain | Use for |
|--------|---------|
| `developer` | Language-specific coding assistants |
| `devops` | Infrastructure, CI/CD, containers, cloud |
| `data` | Data engineering, ML, analytics |
| `security` | Security review, pen-testing, auditing |
| `docs` | Documentation, technical writing |
| `review` | Code review, PR analysis |

New domains are welcome — be consistent and descriptive.

### 2. Create the file

```
agents/<domain>/<spec>.toml
```

Use this template:

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description of what this agent does.

[[roles]]
# name is NOT set here — Octomind injects it automatically from the tag at runtime.
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

### 3. Test locally

```bash
# Register this repo as a local tap (one-time setup)
octomind tap muvon/tap /path/to/octomind-tap

# Run your agent
octomind run <domain>:<spec>

# Remove the local override when done
octomind untap muvon/tap
```

### 4. Set up pre-commit (recommended)

```bash
pip install pre-commit
pre-commit install
```

This runs the manifest linter automatically before every commit.

### 5. Open a PR

Include a short description of:
- What the agent does
- Which tools/MCP servers it uses
- Any model override and why

---

## Manifest rules

- **No `name` field** — it is injected from the tag at runtime. Never set it.
- **One `[[roles]]` entry per file** — no multi-role manifests.
- **File path must match the tag** — `developer:rust` → `agents/developer/rust.toml`.
- **Sub-specs use hyphens** — `developer:rust-nightly` → `agents/developer/rust-nightly.toml`.
- **Required fields**: `system`, `welcome`, `temperature`, `top_p`, `top_k`.
- **Use `{{INPUT:KEY}}` for secrets** — never hardcode tokens or credentials.
- **Use `{{CWD}}` over hardcoded paths** — manifests run on any machine.
- **Docker for zero-install tooling** — wrap language servers or CLIs in a Docker MCP server.

---

## Available placeholder variables

| Placeholder | Resolved to |
|-------------|-------------|
| `{{CWD}}` | Current working directory at runtime |
| `{{INPUT:KEY}}` | Prompts user once, cached in `~/.local/share/octomind/inputs.toml` |
| `{{SYSTEM}}` | Full system info (shell, OS, binaries, CWD) |
| `{{CONTEXT}}` | Project context (README, git status, file tree) |
| `{{DATE}}` | Current date and time with timezone |
| `{{ROLE}}` | Active role name |

---

## Built-in MCP server refs

| `server_refs` | Tools provided |
|---------------|----------------|
| `core` | `plan` |
| `filesystem` | `view`, `text_editor`, `batch_edit`, `extract_lines`, `shell`, `workdir`, `ast_grep` |
| `agent` | `agent_*` (delegate to configured layers) |
| `octocode` | `semantic_search`, `remember`, `memorize`, `view_signatures`, `graphrag` and more |

---

## PR checklist

- [ ] File is at `agents/<domain>/<spec>.toml`
- [ ] No `name` field in `[[roles]]`
- [ ] All required fields present: `system`, `welcome`, `temperature`, `top_p`, `top_k`
- [ ] Tested locally with `octomind run <domain>:<spec>`
- [ ] `pre-commit run --all-files` passes
