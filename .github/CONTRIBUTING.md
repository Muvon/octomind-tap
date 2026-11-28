# Contributing to octomind-tap

Thanks for contributing! This repo is the community registry of agent manifests for [Octomind](https://github.com/muvon/octomind).

---

## What is a manifest?

A manifest is a TOML file at `agents/<name>/default.toml`. The agent's own skills sit beside it under `agents/<name>/skills/`. When a user runs:

```bash
octomind run doctor
```

Octomind fetches `agents/doctor/default.toml` from this repo and merges it into their config — no installation, no global state.

---

## Adding a new agent

### 1. Decide: skill, variant or agent

The tap has one agent per field of work, for example `developer`, `devops`, `analyst`, `security-analyst`. Each agent has a namespace, the directory `agents/<ns>/`; its base agent is `agents/<ns>/default.toml` with the tag `<ns>`. The name is lowercase letters, digits and hyphens. Skills are the default for anything smaller than a field: this tap has 34 base agents and no variants.

- A specialty of an existing field (a procedure, a format, a jurisdiction, a platform; for example blood test interpretation for `doctor`) is a skill. An owned skill, used by one namespace, goes at `agents/<ns>/skills/<name>/SKILL.md`. A shared skill, used by two or more namespaces, goes at `skills/<name>/SKILL.md` with `domains:` naming them.
- A new field of work, with its own deliverables, is a new base agent.
- A variant (`agents/<ns>/<variant>.toml`, tag `<ns>:<variant>`) is the exception. Octomind supports it and this tap's lint rejects it (`AGENT_VARIANT`), so it belongs in a private tap. It is warranted only when a skill cannot do the job: the agent needs its own system prompt and identity, its own capability set (fewer or different tools), its own model, or its own safety rules. Extra instructions, or extra tools on top of the base agent, are a skill; `capabilities:` in its frontmatter brings tools.

The full statement is in [ARCHITECTURE.md](../ARCHITECTURE.md#namespaces-base-agents-variants-and-skills).

### 2. Create the manifest

```
agents/<name>/default.toml
```

Start from `templates/agent.toml`. The minimum:

```toml
# agents/<name>/default.toml
# Agent: <name>
# Title: Short agent title
# Description: What this agent does, in 120–155 characters.

capabilities = ["core"]

[[roles]]
# name is NOT set here — Octomind injects it from the tag at runtime.
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

- **No `name` field** — it is injected from the tag at runtime. Never set it.
- **One `[[roles]]` entry per file** — no multi-role manifests.
- **File path is `agents/<name>/default.toml`** — no symlinks and no other files directly under `agents/`; the agent directory holds only `default.toml` and `skills/`; the `# Agent:` header equals the directory name.
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

- [ ] File is at `agents/<name>/default.toml`
- [ ] No `name` field in `[[roles]]`
- [ ] Required fields present: `capabilities`, `system`, `welcome`; no `temperature`, `top_p`, `top_k`
- [ ] Tested locally with `octomind run <name>`
- [ ] `pre-commit run --all-files` passes
