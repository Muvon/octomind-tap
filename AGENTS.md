# octomind-tap — Agent Registry Guide

Community-maintained registry of agent manifests, capability definitions, dependency scripts, skill packs, and public workflows for the [Octomind](https://github.com/muvon/octomind) AI assistant. Agents declare **capabilities** (never MCP servers directly) — the `bin/load` resolver merges provider wiring at runtime. Contributions are global and public; the `octomind/` domain holds meta-agents that operate on the tap itself. No build step — correctness is defined by the lint scripts.

## Project Structure

```
agents/<domain>/<spec>.toml     # Agent manifests — the primary contribution type
capabilities/<name>/
  config.toml                   # Capability metadata: triggers (+ optional domains gate)
  default.toml                  # Symlink → active provider (e.g. duckduckgo.toml)
  <provider>.toml               # Provider wiring: [deps], [roles.mcp], [[mcp.servers]]
deps/<org>/<tool>.sh            # Dependency install scripts (auto-run before sessions)
deps/<org>/<tool>.md            # Required companion doc for every dep script
deps/lib/platform.sh            # Shared platform detection (source in all dep scripts)
skills/<name>/SKILL.md          # Reusable instruction packs (AgentSkills spec)
skills/<name>/activate|validate # Optional scripts (exit 0 = activate / valid)
workflows/<name>.toml           # Public multi-step workflows — `octomind workflow <name>`
model/                          # Embedding fine-tune powering capability auto-activation
bin/load                        # Python resolver: merges capabilities → manifest on stdout
scripts/                        # lint-manifests / lint-capabilities / lint-skills /
                                # lint-deps / validate-capabilities / setup-symlinks /
                                # mcp-versions (MCP version pin management)
templates/                      # Canonical templates — symlink into scaffolds/tap/root/
scaffolds/tap/                  # `octomind tap init` source: scaffold.toml + root/ tree
ARCHITECTURE.md                 # Canonical design doc — read before any change
CONTRIBUTING.md                 # Human contribution guide (partially pre-capability; this file wins)
```

## Commands

```bash
bash scripts/lint-manifests.sh [agents/<domain>/<spec>.toml ...]   # lint agents
bash scripts/lint-capabilities.sh [capabilities/<name> ...]        # lint capabilities
bash scripts/lint-skills.sh [skills/<name>]                        # lint skills
bash scripts/lint-deps.sh [deps/<org>/<tool>.sh]                   # lint dep scripts + docs
bash scripts/validate-capabilities.sh                              # resolution check, all agents
bash scripts/setup-symlinks.sh                                     # create/refresh default.toml links
bin/load <domain>:<spec>                                           # debug: print resolved manifest

scripts/mcp-versions.sh check [--strict]     # pin drift vs npm/PyPI latest (strict → exit 1)
scripts/mcp-versions.sh update [--all | <capability> ...]   # rewrite pins; leaves changes uncommitted
scripts/mcp-versions.sh test [<capability> ...]             # spawn servers, MCP handshake, tools/list

pre-commit run --all-files                   # local hooks: shfmt, whitespace, check-toml, 3 lints
octomind run <domain>:<spec>                 # smoke-test an agent from repo root
octomind workflow <name> --dry-run           # validate a workflow, run nothing

cd model && uv sync && bin/train             # embedding model full pipeline (--skip-export to skip ONNX)
```

- All lint scripts and `mcp-versions.sh` need Python 3.11+ (or `pip install tomli`).
- `pre-commit` runs `shfmt -w -s -i 2 -ci` on shell scripts — run it before committing dep scripts; `lint-deps.sh` is **not** in pre-commit, run it manually.
- `[UNCONFIRMED]` ARCHITECTURE.md says the five lint scripts run in `.github/workflows/lint.yml` on every push/PR; no `.github/` exists in this checkout.

## Where to Look

| Task | Start here |
|------|------------|
| Add a new agent | Copy `templates/agent.toml` → `agents/<domain>/<spec>.toml`; spec: `skills/tap-agent-authoring/SKILL.md` |
| Add a new capability | Copy `templates/capability.toml` + `templates/capability-config.toml` → `capabilities/<name>/`; spec: `skills/tap-capability-authoring/SKILL.md` |
| Add a new skill | Copy `templates/skill.md` → `skills/<name>/SKILL.md`; spec: `skills/tap-skill-authoring/SKILL.md` |
| Add a new dep script | Copy `templates/dep.sh` + `templates/dep-mcp.md` or `templates/dep-tool.md` → `deps/<org>/`; spec: `skills/tap-deps-authoring/SKILL.md` |
| Add a new workflow | Copy `templates/workflow.toml` → `workflows/<name>.toml`; spec: `skills/octomind-workflow/SKILL.md` + `workflows/README.md` |
| Understand the capability system | `ARCHITECTURE.md` — design, capability table, access tiers |
| Prompt engineering theory | `skills/prompt-engineering/SKILL.md` (+ `reference/claude-4-emphasis-and-tools.md`) |
| Train the embedding model | `model/README.md`; spec: `skills/tap-model-training/SKILL.md` |
| Resolve a manifest (debug) | `bin/load <domain>:<spec>` — merged TOML on stdout |
| Platform helpers in dep scripts | `deps/lib/platform.sh` — source it, never re-implement |
| Meta-agents (tap/workflow/config) | `agents/octomind/` — they operate on the tap itself |
| Change what `octomind tap init` generates | `scaffolds/tap/` — edit `root/`, keep `scaffold.toml` and `scaffolds/tap/README.md` in sync |

## How Things Work

### Capability-Based Agents (the only way)

Agents declare **what they need**, not how to get it:

```toml
# ✅ correct — capability-based
capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-rust"]

[[roles]]
system = "..."
welcome = "..."
temperature = 0.3
top_p = 0.9
top_k = 0
```

```toml
# ❌ forbidden — never write these in an agent manifest
[deps]
require = [...]

[roles.mcp]
server_refs = [...]
allowed_tools = [...]

[[mcp.servers]]
name = "..."
```

`bin/load <domain>:<spec>` resolves each capability → reads `capabilities/<name>/default.toml` (or `<name>:<provider>` for an explicit provider) → merges `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]` into the final manifest at runtime.

### Capability Files (two kinds per capability)

`capabilities/<name>/<provider>.toml` — provider wiring, with `# Capability:`, `# Provider:`, `# Title:` (5–60 chars), `# Description:` (20–160 chars) header comments:

```toml
[deps]
require = ["muvon/octofs"]          # dep scripts to run before session

[roles.mcp]
server_refs = ["octofs"]            # MCP server names to activate
allowed_tools = ["octofs:*"]        # tools to expose (wildcards OK)

[[mcp.servers]]                     # REQUIRED if server_ref is non-builtin
name = "octofs"
type = "stdio"
command = "octofs"
args = ["mcp"]
timeout_seconds = 300
tools = []
# env = { API_KEY = "{{ENV:API_KEY}}" }   # exact env var names read by the child
```

`capabilities/<name>/config.toml` — routing metadata: non-empty `triggers = [...]` (user phrasings for deterministic auto-activation; also training data for the `model/` embedding) and an optional `domains = ["developer"]` hard gate. No Title/Description required.

**Built-in server refs** (`core`, `octofs`, `agent`, `octocode`) do NOT need `[[mcp.servers]]` blocks. Every other server ref MUST have a matching `[[mcp.servers]]` block in its capability file.

**Version pins** — every registry-launched server (npx/uvx, including inside `sh -c`) must pin an exact package version (`pkg@X.Y.Z` / `pkg==X.Y.Z`) so a registry publish can never change what users run. `lint-capabilities.sh` enforces pin presence offline; `scripts/mcp-versions.sh` handles drift, updates, and live smoke-tests.

### Agent Manifest Rules

| Field | Rule |
|-------|------|
| Header comments | `# Agent: <domain>:<spec>`, `# Title:` (5–60 chars), `# Description:` (20–160 chars) — required, linted |
| `capabilities = [...]` | Required at top level; drives everything |
| `[[roles]]` | Exactly one entry |
| `name` | Must NOT be set — injected at runtime from the tag |
| `system` | Required; XML-tagged blocks in canonical order (below); stable run-to-run for prompt caching |
| `welcome` | Required; `{{CWD}}` and `{{DATE}}` allowed here only — they break caching if used in `system` |
| `temperature` / `top_p` / `top_k` | Required; 0.1–0.3 technical / 0.4–0.6 general; `top_p` 0.9; `top_k` 0 to disable, 10–40 for determinism |
| `model` | Optional override, e.g. `"openrouter:anthropic/claude-sonnet-4"` |

### System Prompt Structure (2026 standard — XML-tagged blocks)

Fixed U-shape order. Identity first (primacy), critical rules last (recency); the middle relies on tag anchors to survive "lost in the middle":

```
<identity>          who/what (3–5 lines)
<voice>             tone (omit for technical agents)
<scope>             ✅ own / ❌ route elsewhere
<workflow>          numbered steps + sub-protocols
<rules>             tables, decision matrices, domain knowledge
<examples>          good/bad pairs (omit if N/A)
<output_format>     artifact shape, file paths, schemas
<interaction>       trigger → response patterns
<critical>          brief Don't/Do list in plain language
```

**Tone calibration (Claude 4.5+ over-emphasis):** aggressive language written for 3.x now over-triggers. Substance stays; theatre goes.

- `CRITICAL: YOU MUST use tool X when …` → `Use tool X when …`
- `🚨 HARD RULES` + stacked `NEVER`/`ALWAYS` → plain `Don't …` / `Do …`
- `MANDATORY: Run validation` → `Run validation after edits.`

Reserve all-caps for one or two genuine safety hard-stops (e.g. `Never force-push to main`). Full recipe + parallel-tool-calls block: `skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`.

**Hard rules enforced by `lint-manifests.sh`:**
- No `**bold**` outside code — XML tags provide structure
- No `##`/`#` markdown headers — XML tags replace them (only `### Subsection` allowed inside a block with 2+ subsections)
- No `{{CWD}}` or `{{DATE}}` in `system` — place in `welcome` only (caching)
- Target 200–1000 words; beyond ~1500, context rot degrades recall
- No tap-relative paths (`skills/…`, `capabilities/…`, `deps/…`) in `system` or `welcome` — agents run in the project workdir, not the tap checkout; name the skill instead (`octomind` domain exempt)
- Every `` `name` skill `` mentioned must exist at `skills/<name>/SKILL.md`

Full authoring spec, rationale, anti-patterns: `skills/tap-agent-authoring/SKILL.md`.

### Capability Access Tiers (least privilege)

| Tier | Capability | Tools | Who declares it |
|------|-----------|-------|-----------------|
| self-management | `core` | `plan` | **every** agent |
| do the work | domain caps | `shell`, `filesystem-*`, `codesearch-*`, `legal-*`, … | per agent |
| intra-domain team | `agent` | `agent_*` | sub-orchestrators |
| orchestration | `orchestration` | `tap`, `schedule` | orchestrators only (e.g. `assistant:concierge`, `developer:general`) |
| runtime config | `runtime` | `mcp`, `agent`-register, `skill`, `capability` | high-trust only |

A narrow specialist declares `core` + domain capabilities and never `orchestration`/`runtime` — enforced structurally: the unwanted server never enters the tool surface. `orchestration`/`runtime` may still auto-activate on intent via their `config.toml` triggers; that is temporary, never a standing grant.

### Multi-Step Pipelines (external)

Agents are `capabilities` + one `[[roles]]` — they do **not** define pipelines. The old in-manifest `workflow = "..."` field and `[[workflows]]` block were removed from Octomind.

Orchestration is an external CLI: `octomind workflow <file.toml|name>` — portable TOML chaining `octomind run` invocations (sequential / parallel / loop / conditional steps, plus graph routing via `entry`, `max_transitions`, `[[edges]]`), piping output between steps by name (`{{input}}`, `{{<step-name>}}`). Rules that bite:

- Workflows fetched from a tap may use **public tap roles only** (`category:variant` tags) — no local config roles; this keeps them portable.
- Driving input arrives on stdin; validate with `--dry-run` before running.
- Author with `templates/workflow.toml`, the `octomind-workflow` skill, or the `octomind:workflow` agent; catalogue: `workflows/README.md`.

`[[layers]]` still exist in Octomind config (not tap manifests): they back `[[commands]]` slash commands (`/run <name>`) and delegate via `command = "octomind acp <role>"`.

### Naming Conventions

- **Agent files**: `agents/<domain>/<spec>.toml` — exactly two path components; domain groups related agents
- **Capabilities**: lowercase-hyphens; prefix grouping for variants: `programming-rust`, `legal-us`, `messaging-slack`
- **Dep scripts**: `deps/<org>/<tool>.sh` — matches `require = ["<org>/<tool>"]` in capability files
- **Skills**: `skills/<name>/SKILL.md` — exactly one directory level; directory name must match frontmatter `name`; lowercase-hyphens only

### Dep Script Pattern

Every dep script must:
1. Source `deps/lib/platform.sh` — all helpers and variables come from here, never re-implement
2. Exit 0 immediately if already installed (`pkg_check <command>`)
3. Install on every supported platform: macOS (brew, official-installer fallback) + Linux (apt/dnf/pacman/zypper/apk + universal curl/wget fallback)
4. Verify the tool is in PATH after install; add `~/.local/bin` or `~/.cargo/bin` if needed

**Required header comments** (parsed by tooling):

```bash
# dep: <org>/<tool>
# type: mcp|dep        # mcp = makes an MCP server runnable; dep = standalone CLI/runtime
# description: Brief description of what this installs
# check: <command-to-verify-installation>
# https://homepage-url
```

**Companion documentation** — every dep script needs `deps/<org>/<tool>.md`:
- `type: mcp` → sections `## MCP Server`, `## Authentication`, `## Available Tools`, `## Configuration Example`
- `type: dep` → sections `## Key Commands`, `## Common Usage`
- Templates: `templates/dep-mcp.md`, `templates/dep-tool.md`

**Boilerplate** (copy from `templates/dep.sh`):

```bash
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check "<command>"; then exit 0; fi
```

**Variables after sourcing `platform.sh`:** `$OS` (`macos`|`linux`) · `$ARCH` (`x86_64`|`arm64`) · `$PKG_MANAGER` (`brew`|`apt`|`dnf`|`pacman`|`zypper`|`apk`|`unknown`) · `$IS_MACOS` / `$IS_LINUX` / `$IS_ARM64` / `$IS_X86_64` (1 or 0)

**Functions after sourcing `platform.sh`:**

| Function | Purpose |
|----------|---------|
| `pkg_check <cmd>` | 0 if command exists — fast-path exit and post-install verify |
| `pkg_install <pkg>` | Install via detected package manager (same name on all PMs) |
| `brew_install` / `apt_install` / `dnf_install` | Platform-scoped, no-op elsewhere |
| `install_dep <org/tool>` | Run another dep script as prerequisite; sources PATH env after |
| `info` / `warn` / `die` | stderr messaging; `die` exits 1 |

### Skill Format (AgentSkills spec)

```markdown
---
name: skill-name            # required; matches directory name; ≤64 chars, lowercase-hyphens
title: "Skill Title"        # required; 5–60 chars
description: "What and when."  # required; 20–1024 chars
license: Apache-2.0
compatibility: "Requires: tool1. macOS/Linux."   # ≤500 chars; environment only — never skill pairings
capabilities: versioning memory-read    # auto-load capabilities on activation
domains: developer devops   # auto-activation scoping; omit for manual-only
rules:                      # auto-activation expressions; omit for manual-only
  - file(Cargo.toml)
  - content(rust) content(async)
---
```

Optional dirs alongside SKILL.md: `scripts/`, `references/`, `assets/`, plus `activate` and `validate` executables.

**Activation — three methods:**

- Env preload: `OCTOMIND_SKILLS=programming-rust,git-workflow octomind run developer:general` (permanent, no rules evaluated)
- Auto-activation: skills whose `domains` match the agent's domain get their `rules` evaluated on conversation events; already-active skills are skipped
- Manual: `skill(action="use"|"forget"|"list", name=...)` or `/skill <use|forget|list>`

**Rule expressions** — list items are OR branches; multiple expressions on one line are AND:

| Expression | Matches when |
|------------|-------------|
| `file(<glob>)` | File matching glob exists in workdir (`*`, `**`) |
| `content(<word>)` | User message contains the word (whole-word, case-insensitive) |
| `match(<regex>)` | User message matches the pattern |
| `grep(<pattern>, <glob>)` | A file matching the glob contains a matching line |
| `env(<VAR>)` / `env(<VAR>=<value>)` | Env var set / equals value |
| `bin(<command>)` | Command available in `$PATH` |
| `workdir(<pattern>)` | CWD path contains the pattern (substring) |
| `session(<word>)` | Session name contains the word (e.g. `developer:rust`) |

**Scripts:** `activate` receives event type (`user`|`assistant`|`turn`) as argv[1], content on stdin, runs in project workdir; exit 0 = activate. `validate` same interface at end of assistant turn; non-zero = invalid, stderr is fed back to the LLM (retries capped by `[skills] max_retries`). Both must be executable.

**Body — U-shape section order:** Overview (top) → Mental model → Rules → Examples → Checklist (near the end — final gate) → Composition / References. Under ~2000 words; beyond that, context rot hits skill recall.

**Hard rules enforced by `lint-skills.sh`:** valid frontmatter; required fields and length limits; `name` matches directory; non-empty body; every `reference/<file>` cited exists; `validate` executable; no `**bold**` in body outside code.

**Domain isolation:** `domains:` single-valued where possible; body does NOT reference agents from other domains (`content:article`, `developer:typescript`, …); `compatibility:` describes environment only. Cross-domain composition is the orchestrating agent's job.

### Adding a New Capability (full checklist)

1. Create `capabilities/<name>/config.toml` — `triggers = [...]` (required), optional `domains` gate
2. Create `capabilities/<name>/<provider>.toml` — header comments + `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`; pin exact versions for npx/uvx servers
3. Add `link "<name>" "<provider>.toml"` **and** `"<name>"` to the `DECLARED` array in `scripts/setup-symlinks.sh`
4. Run `bash scripts/setup-symlinks.sh` (exits 1 on MISSING, warns on undeclared dirs)
5. Create any `deps/<org>/<tool>.sh` + `.md` referenced in `[deps] require`
6. Reference `"<name>"` (default provider) or `"<name>:<provider>"` in agent `capabilities = [...]`
7. Adding capability triggers changes `model/` training data — see `skills/tap-model-training/SKILL.md` for retraining

### Placeholders

| Placeholder | Scope | Use |
|-------------|-------|-----|
| `{{CWD}}` | Session | Current working directory — `welcome` only in agents (breaks caching in `system`) |
| `{{DATE}}` | Session | Current date — same caching rule |
| `{{ENV:KEY}}` | Project env | Injects environment variable (e.g. API keys) in capability files; document required vars in the capability header comment |
| `{{INPUT:KEY}}` | User-global secret | API tokens, credentials (e.g. in `[[mcp.servers]] env`) |

## Done

Run the commands that touch what you changed — all must exit 0:

```bash
bash scripts/lint-manifests.sh        # touched agents/…toml
bash scripts/lint-capabilities.sh     # touched capabilities/…
bash scripts/lint-skills.sh           # touched skills/…
bash scripts/lint-deps.sh             # touched deps/…
bash scripts/validate-capabilities.sh # any capability change
bash scripts/setup-symlinks.sh        # any capability add/remove (symlink integrity)
bin/load <domain>:<spec>              # touched agent — resolves without errors
scripts/mcp-versions.sh test <capability>  # touched npx/uvx server wiring
octomind workflow <name> --dry-run    # touched workflow
```

**Agent done** — lints pass (incl. markdown/cache guardrails); XML blocks in canonical order; every capability has `capabilities/<name>/default.toml`; all `require` entries exist under `deps/`; `welcome` is descriptive and includes `{{CWD}}`; `octomind run <domain>:<spec>` starts clean.

**Skill done** — lints pass; `name` matches directory; canonical section order with Checklist near the end; instructions actionable (what to DO); domain-isolated.

**Capability done** — lints pass; `default.toml` symlink resolves; pins present; `mcp-versions.sh test` speaks MCP.

**Dep done** — `lint-deps.sh` passes (headers, `# type:`, companion `.md`, platform coverage); `bash deps/<org>/<tool>.sh` exits 0 on an already-installed machine and installs on a clean one.

**Full-repo done** — all five lint scripts + `pre-commit run --all-files` exit 0.

## Gotchas

- `bin/load` uses a regex-based TOML-subset parser (no external deps) — keep capability files simple: no multi-line arrays or complex TOML features.
- `setup-symlinks.sh` uses `ln -sf` (force) — safe to re-run; the `DECLARED` array must be updated manually or the script emits `WARN` for undeclared dirs.
- `capabilities/core/`, `capabilities/agent/`, and `capabilities/orchestration/` have **real** `default.toml` files — no provider variants, no `link` entries for them.
- Default providers live in `setup-symlinks.sh` — e.g. `websearch` currently defaults to `duckduckgo.toml` (not tavily; ARCHITECTURE.md's example is stale). Switch a provider with `ln -sf <provider>.toml capabilities/<name>/default.toml`; reset all with `setup-symlinks.sh`.
- `templates/` and `deps/lib/platform.sh` are symlinks into `scaffolds/tap/root/` — single source of truth so generated taps never drift; edit at the scaffold source.
- The `octomind/` agent domain is special — its agents operate on the tap itself. Run `octomind run octomind:tap` in this repo root for the tap-authoring assistant (`octomind:workflow`, `octomind:config`, `octomind:assistant` alongside).
- `mcp-versions.sh test` may report missing-key errors for servers needing credentials — judge by whether the process starts and speaks MCP at all.
- CONTRIBUTING.md quick-start examples still write `[roles.mcp]`/`[deps]` directly (pre-capability style) — this file and ARCHITECTURE.md are authoritative when they conflict.

## Never

- Write `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in an agent manifest — they belong exclusively in capability files
- Set `name = "..."` inside `[[roles]]` — injected at runtime from the file path tag
- Add a `server_ref` without a matching `[[mcp.servers]]` block (built-ins exempt: `core`, `octofs`, `agent`, `octocode`)
- Launch an npx/uvx server without an exact version pin
- Add `orchestration` or `runtime` to a leaf/domain-specialist agent — orchestrator- and high-trust-tier only
- Create a capability directory without adding it to both the `link` calls and the `DECLARED` array in `setup-symlinks.sh`
- Nest agents deeper than `agents/<domain>/<spec>.toml` or skills deeper than `skills/<name>/SKILL.md`
- Reference tap-relative paths or cross-domain agent tags in `system`/`welcome`/skill bodies — agents run in the user's project, not the tap checkout

## References

- `ARCHITECTURE.md` — canonical design; read before any structural change
- `CONTRIBUTING.md` — human-facing contribution guide (partially stale; this file wins)
- `workflows/README.md` — workflow catalogue, resolution rules, TOML structure
- `model/README.md` — embedding fine-tune pipeline (dataset → train → eval gates → ONNX → HuggingFace)
- `scaffolds/tap/README.md` — `octomind tap init` token table and renderer rules
- `skills/tap-agent-authoring/SKILL.md` · `tap-capability-authoring` · `tap-skill-authoring` · `tap-deps-authoring` · `tap-model-training` — per-type authoring specs
- `skills/prompt-engineering/SKILL.md` — prompt theory across agents, skills, layer prompts
- `skills/octomind-workflow/SKILL.md` — workflow authoring spec
