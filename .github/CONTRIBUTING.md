# Contributing to octomind-tap

Thanks for contributing! This repo is the community registry of agent manifests for [Octomind](https://github.com/muvon/octomind).

---

## What is a manifest?

A manifest is a TOML file at `agents/<name>/config.toml`. The agent's own skills sit beside it under `agents/<name>/skills/`. When a user runs:

```bash
octomind run doctor
```

Octomind fetches `agents/doctor/config.toml` from this repo and merges it into their config — no installation, no global state.

---

## Adding a new agent

### 1. Pick a name

The tap has one agent per field of work, for example `developer`, `devops`, `analyst`, `security-analyst`. The name is the directory name: lowercase letters, digits and hyphens, never a `:`.

A specialty of an existing field (for example blood test interpretation for `doctor`) is a skill, not a new agent. A skill that only one agent uses goes at `agents/<agent>/skills/<name>/SKILL.md`; a skill that two or more agents use goes at `skills/<name>/SKILL.md` with `domains:` naming them. Add an agent only for a new field of work.

### 2. Create the manifest

```
agents/<name>/config.toml
```

Start from `templates/agent.toml`. The minimum:

```toml
# agents/<name>/config.toml
# Agent: <name>
# Title: Short agent title
# Description: What this agent does, in 120–155 characters.

capabilities = ["core"]

[[roles]]
# name is NOT set here — Octomind injects it from the directory name at runtime.
welcome = "<Short greeting>. Working in {{CWD}}"
system = """
<identity>
<Your system prompt here.>
</identity>
"""
```

Name capabilities only. Tool wiring (`[deps]`, `[roles.mcp]`, `[[mcp.servers]]`) lives in the capability's provider file, never in a manifest.

### 3. Test locally

```bash
# Register this repo as a local tap (one-time setup)
octomind tap muvon/tap /path/to/octomind-tap

# Run your agent
octomind run <name>

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
- Which capabilities it declares
- Any model override and why

---

## Manifest rules

- **No `name` field** — it is injected from the directory name at runtime. Never set it.
- **One `[[roles]]` entry per file** — no multi-role manifests.
- **File path is `agents/<name>/config.toml`** — no symlinks and no other files directly under `agents/`; the agent directory holds only `config.toml` and `skills/`; the `# Agent:` header equals the directory name.
- **Required fields**: top-level `capabilities`, and in the role `system` and `welcome`. Do not set `temperature`, `top_p` or `top_k`: they are deprecated and Octomind ignores them.
- **No tool wiring** — no `[deps]`, `[roles.mcp]` or `[[mcp.servers]]` in a manifest.
- **Use `{{INPUT:KEY}}` for secrets** in capability files — never hardcode tokens or credentials.
- **Use `{{CWD}}` in `welcome` only** — it breaks prompt caching inside `system`.

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
| `core` | `recall` |
| `octofs` | `view`, `text_editor`, `batch_edit`, `extract_lines`, `shell`, `workdir` |
| `agent` | `agent_*` (delegate to configured sub-agents) |
| `octocode` | `semantic_search`, `remember`, `memorize`, `view_signatures`, `graphrag` and more |

---

## PR checklist

- [ ] File is at `agents/<name>/config.toml`
- [ ] No `name` field in `[[roles]]`
- [ ] Required fields present: `capabilities`, `system`, `welcome`; no `temperature`, `top_p`, `top_k`
- [ ] Tested locally with `octomind run <name>`
- [ ] `pre-commit run --all-files` passes
