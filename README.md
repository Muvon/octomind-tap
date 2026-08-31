# Octomind Tap

> Run a fully-configured AI specialist with one command — no setup, no config files, no API plumbing.

The community registry for [Octomind](https://github.com/muvon/octomind), the CLI-first AI agent runtime. **140+ agents across 35 domains**, 100+ skill packs, 19 ready-made workflows, 120+ dependency scripts — each one a single TOML file that Octomind resolves and merges into your session at runtime.

```bash
octomind run doctor:blood        # interpret blood test results
octomind run developer:general   # senior full-stack developer
octomind run devops:kubernetes   # Kubernetes expert
```

Browse the catalog: [octomind.run/tap](https://octomind.run/tap/)

---

## Table of Contents

- [Quick Start](#quick-start)
- [What's in the Registry](#whats-in-the-registry)
- [Tag Format](#tag-format)
- [Capability System](#capability-system)
- [Workflows](#workflows)
- [Skills](#skills)
- [Dependency Scripts](#dependency-scripts)
- [Repository Layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

---

## Quick Start

You need the `octomind` binary first — the tap ships with it as the default registry, so no tap registration is required.

```bash
# 1. Install Octomind (macOS & Linux) — single Rust binary, no runtime dependencies
curl -fsSL https://raw.githubusercontent.com/muvon/octomind/master/install.sh | bash

# 2. Sign in — models included, no API keys to manage
octomind login

# 3. Run a specialist
octomind run doctor:blood
```

The default tap is cloned automatically on first use and updated on every run.

```bash
# Pin to a specific version
octomind run developer:general@1.0

# Run a ready-made multi-step pipeline
octomind workflow develop

# Bootstrap your own tap (private or team) — rendered, validated, ready to run
octomind tap init acme/team && octomind run team:assistant
```

---

## What's in the Registry

| Directory | What it holds | Count |
|-----------|---------------|-------|
| `agents/<domain>/<spec>.toml` | Agent manifests — a system prompt, sampling params, and capability declarations | 140+ across 35 domains |
| `capabilities/<name>/` | Capability definitions — the tools an agent needs, decoupled from how they're provided | 60+ |
| `skills/<name>/SKILL.md` | Reusable instruction packs (AgentSkills spec) that auto-activate by context | 100+ |
| `workflows/<name>.toml` | Multi-step pipelines chaining agent runs (sequential / parallel / loop / conditional) | 19 |
| `deps/<org>/<tool>.sh` | Dependency install scripts — auto-run before sessions, macOS + Linux | 120+ |
| `model/` | Embedding model fine-tune powering capability auto-activation | — |
| `bin/load` | The resolver: merges capabilities into the final manifest (stdout) | — |

Agents span domains like `developer`, `doctor`, `lawyer`, `finance`, `security`, `devops`, `data`, `marketing`, `writer`, `research`, and more.

---

## Tag Format

```
domain:spec[-sub-spec][@version]
```

| Part | Required | Description |
|------|----------|-------------|
| `domain` | ✅ | Top-level category (e.g. `developer`, `doctor`, `devops`) |
| `spec` | ✅ | Primary specialisation (e.g. `general`, `blood`, `kubernetes`) |
| `-sub-spec` | optional | Variant of the spec (e.g. `rust-nightly`, `python-ml`) |
| `@version` | optional | Pinned version tag (e.g. `@1.0`). Omit for latest. |

**Examples:**

```
developer:general                → agents/developer/general.toml
devops:kubernetes                → agents/devops/kubernetes.toml
data:sql                         → agents/data/sql.toml
developer:general@1.0            → agents/developer/general.toml  (version hint, future use)
```

> **Note on versioning:** `@x.y` is parsed and passed through, but the registry currently resolves to the same file path. Versioned paths are reserved for future use — for now, omit the version and rely on the 24-hour cache TTL.

---

## Capability System

Agents declare **what they need**, not how to get it. This is the only supported way — manifests never contain `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` blocks.

```toml
# agents/developer/general.toml

capabilities = ["core", "filesystem-read", "filesystem-write", "shell",
                "codesearch-semantic", "codesearch-structural", "versioning"]

[[roles]]
system = "..."
welcome = "..."
temperature = 0.3
top_p = 0.9
top_k = 0
```

### How resolution works

1. `bin/load <domain>:<spec>` reads each capability → `capabilities/<name>/default.toml`.
2. `default.toml` is a symlink to the active provider (e.g. `octofs.toml`, `duckduckgo.toml`).
3. The resolver merges every provider's `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]` into the final manifest on stdout.

### Capability highlights

| Capability | What it provides | Default provider |
|------------|-----------------|-----------------|
| `core` | `plan` task tracker — universal self-management (every agent) | built-in |
| `agent` | `agent_*` — delegate to your configured sub-agents | built-in |
| `orchestration` | `tap` (discover/run specialists) + `schedule` (defer/recur loops) — orchestrator-tier | built-in |
| `runtime` | `mcp` · `agent`-register · `skill` · `capability` — runtime config (high-trust) | built-in |
| `filesystem-read` / `filesystem-write` | `view`, `workdir` / `text_editor`, `batch_edit`, `extract_lines` | `octofs.toml` |
| `shell` | `shell` (command execution) | `octofs.toml` |
| `codesearch-semantic` / `-structural` / `-graph` | `semantic_search` / `structural_search`, `view_signatures` / `graphrag` | `octocode.toml` |
| `memory-read` / `memory-write` | persistent memory tools | `octobrain.toml` |
| `websearch` | web search | `duckduckgo.toml` |
| `versioning` | git operations via shell | `git.toml` |

Beyond these, the registry ships 50+ domain capabilities — `legal-*`, `video-gen`, `image-gen`, `messaging-*`, `trading-crypto`, and more. See [ARCHITECTURE.md](ARCHITECTURE.md) for the full table.

> **Access tiers (least privilege).** A narrow domain specialist declares `core` plus its domain tools and never `orchestration` — so it can't delegate across domains or schedule loops; that server isn't in its tool set at all. Only agents that intend to orchestrate declare `orchestration`. See [ARCHITECTURE.md](ARCHITECTURE.md#capability-access-tiers-least-privilege).

### Switching providers

```bash
# Switch websearch from DuckDuckGo to Brave
ln -sf brave.toml capabilities/websearch/default.toml

# Or reset all defaults
bash scripts/setup-symlinks.sh
```

### Debugging resolution

```bash
# Inspect the fully merged manifest for an agent
bin/load developer:general

# Validate capability resolution for every agent in the registry
bash scripts/validate-capabilities.sh
```

---

## Workflows

Multi-step pipelines live outside agent manifests: portable TOML files that chain `octomind run` invocations — sequential, parallel, looping, or conditional — piping output between steps by name.

```bash
octomind workflow develop       # plan → implement → review pipeline
octomind workflow deep-review   # multi-lens code review
octomind workflow launch        # release preparation pipeline
```

19 ready-made workflows ship in `workflows/` — see [workflows/README.md](workflows/README.md) for the full list. Author your own with the `octomind-workflow` skill or the `octomind:workflow` agent.

---

## Skills

Skills are reusable instruction packs ([AgentSkills](https://agentskills.io) spec) that inject domain knowledge into a session — and activate themselves when the context matches.

```markdown
---
name: git-workflow
title: "Git Workflow"
description: "Git commit conventions, branch naming, and workflow best practices..."
license: Apache-2.0
compatibility: "Requires git. Works with any git-based project."
capabilities: versioning
domains: developer devops
rules:
  - file(.git)
---
```

- `rules:` predicates (`file()`, `match()`, `semantic()`, `grep()`, `env()`, …) drive auto-activation. Skills without `rules:` are manual-only.
- `capabilities:` auto-loads capabilities when the skill activates.
- `domains:` scopes auto-activation to agent categories.
- Optional `activate` and `validate` scripts alongside `SKILL.md` add event-driven activation and output validation.

Preload skills without activate scripts:

```bash
OCTOMIND_SKILLS=programming-rust,git-workflow octomind run developer:general
```

Skill auto-activation is powered by the embedding fine-tune in `model/` — see [model/README.md](model/README.md) for the training pipeline.

---

## Dependency Scripts

Capabilities can require external tools. Octomind runs the matching `deps/<org>/<tool>.sh` automatically before the session starts — exit non-zero aborts the session with a clear error.

```toml
# inside a capability file
[deps]
require = ["astral-sh/uv", "nodejs/node"]
```

Every dep script must:

1. **Source `deps/lib/platform.sh`** — all platform helpers come from there, never re-implemented
2. **Be idempotent** — exit 0 immediately if the tool is already installed
3. **Cover macOS + Linux** — brew on macOS; apt/dnf/pacman/zypper/apk + universal fallback on Linux
4. **Carry the required header** (parsed by tooling) and a companion `.md` doc:

```bash
# dep: astral-sh/uv
# type: dep
# description: Fast Python package installer and resolver
# check: uv
# https://docs.astral.sh/uv/
```

`type: mcp` marks scripts that exist to make an MCP server runnable; `type: dep` marks standalone CLI tools. The registry ships 120+ scripts — run `bash scripts/lint-deps.sh` to validate them.

---

## Repository Layout

```
agents/<domain>/<spec>.toml     # Agent manifests — the primary contribution type
capabilities/<name>/            # Capability definitions
  default.toml                  # Symlink → active provider (e.g. octofs.toml)
  <provider>.toml               # [deps], [roles.mcp], [[mcp.servers]]
deps/<org>/<tool>.sh            # Dependency install scripts (+ companion .md)
deps/lib/platform.sh            # Shared platform detection helpers
skills/<name>/SKILL.md          # Reusable instruction packs (AgentSkills spec)
workflows/<name>.toml           # Multi-step pipelines — octomind workflow <name>
model/                          # Embedding fine-tune powering capability auto-activation
bin/load                        # Resolver: merges capabilities → final manifest (stdout)
scripts/                        # Lint + validation tooling
templates/                      # Canonical templates for agents, skills, deps, capabilities
scaffolds/tap/                  # Source of truth for `octomind tap init` (new user taps)
ARCHITECTURE.md                 # Design doc — read before making changes
CONTRIBUTING.md                 # Contribution guidelines
```

### Taps

This repo is the **default tap** — always active, cloned to `~/.local/share/octomind/taps/`, auto-updated via `git pull` on every run. You can layer your own:

```bash
octomind tap myorg/agents                  # add a GitHub tap (checked before the default)
octomind tap myorg/agents /path/to/repo    # add a local tap (no clone)
octomind tap                               # list active taps
octomind untap myorg/agents                # remove a tap
```

### Create your own tap

One command bootstraps a private or public tap from the scaffold in
[`scaffolds/tap/`](scaffolds/tap/):

```bash
octomind tap init acme/team
```

This renders the scaffold into `./octomind-team/`, validates it, initializes
Git, and registers it as a local tap — the starter agent runs immediately:

```bash
octomind run team:assistant
```

`scaffolds/tap/` in this repository is the single source of truth for the
generated layout; any GitHub template repository is only a synchronized mirror.

### Placeholder variables

Manifests support placeholders expanded at runtime — run `octomind vars` to see them all:

| Placeholder | Behaviour |
|-------------|-----------|
| `{{INPUT:KEY}}` | Prompts once, stores in `~/.local/share/octomind/inputs.toml` — for global secrets (API tokens) |
| `{{ENV:KEY}}` | Reads the environment; if unset, prompts and saves to `./.env` — for project-scoped values |
| `{{CWD}}`, `{{DATE}}`, … | Runtime context — use in `welcome` only, never in `system` (breaks prompt caching) |

---

## Contributing

**The most valuable contribution is expertise, not code.** If you have domain knowledge — medicine, law, finance, security, DevOps — you can ship a specialist that thousands of people run with one command.

```bash
# 1. Start from the canonical template
cp templates/agent.toml agents/<domain>/<spec>.toml

# 2. Edit: capabilities, system prompt (XML-tagged blocks), sampling params

# 3. Validate
bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml
bash scripts/validate-capabilities.sh
bin/load <domain>:<spec>
```

Key rules:

- Agents declare `capabilities = [...]` only — never `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in a manifest
- System prompts use XML-tagged blocks in canonical order (`<identity>` → … → `<critical>`), 200–1000 words
- Exactly one `[[roles]]` entry; never set `name` (injected at runtime from the tag)
- New capabilities need a provider file, a `setup-symlinks.sh` entry, and a `DECLARED` registration

Full guidelines: [CONTRIBUTING.md](CONTRIBUTING.md) · Design doc: [ARCHITECTURE.md](ARCHITECTURE.md) · Agent conventions: [AGENTS.md](AGENTS.md)

---

## License

Apache 2.0 — see [LICENSE](LICENSE).

**Octomind** by [Muvon](https://muvon.io) | [Website](https://octomind.run) | [Documentation](https://octomind.run/docs/)
