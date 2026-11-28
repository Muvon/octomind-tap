# octomind-tap — Agent Registry Guide

Community-maintained registry of agent manifests, capability definitions, dependency scripts, skill packs, and public workflows for the [Octomind](https://github.com/muvon/octomind) AI assistant. Agents declare **capabilities** (never MCP servers directly) — the `bin/load` resolver merges provider wiring at runtime. Contributions are global and public; the `octomind` agent operates on the tap itself. No build step — correctness is defined by the lint scripts.

## Project Structure

```
agents/<name>.toml              # Agent manifests, one per field of work, flat (no subdirectories)
capabilities/<name>/
  config.toml                   # Capability metadata: triggers (+ optional domains gate)
  default.toml                  # Symlink → active provider (e.g. duckduckgo.toml)
  <provider>.toml               # Provider wiring: [deps], [roles.mcp], [[mcp.servers]]
deps/<org>/<tool>.sh            # Dependency install scripts (auto-run before sessions)
deps/<org>/<tool>.md            # Required companion doc for every dep script
deps/lib/platform.sh            # Shared platform detection (source in all dep scripts)
skills/<name>/SKILL.md          # Reusable instruction packs (AgentSkills spec); one per specialty
skills/<name>/validate          # Optional script (exit 0 = valid)
workflows/<name>.toml           # Public multi-step workflows — `octomind workflow <name>`
model/                          # Embedding fine-tune powering capability auto-activation
bin/load                        # Python resolver: merges capabilities → manifest on stdout
scripts/                        # lint-manifests / lint-capabilities / lint-skills /
                                # lint-deps / lint-workflows / validate-capabilities / setup-symlinks /
                                # mcp-versions (MCP version pin management)
templates/                      # Canonical templates — symlink into scaffolds/tap/root/
scaffolds/tap/                  # `octomind tap init` source: scaffold.toml + root/ tree
ARCHITECTURE.md                 # Canonical design doc — read before any change
CONTRIBUTING.md                 # Human contribution guide
```

## Commands

```bash
bash scripts/lint-manifests.sh [agents/<name>.toml ...]            # lint agents
bash scripts/lint-capabilities.sh [capabilities/<name> ...]        # lint capabilities
bash scripts/lint-skills.sh [skills/<name>]                        # lint skills
bash scripts/lint-deps.sh [deps/<org>/<tool>.sh]                   # lint dep scripts + docs
bash scripts/lint-workflows.sh [workflows/<name>.toml]             # lint workflows (+ octomind --dry-run)
bash scripts/validate-capabilities.sh                              # resolution check, all agents
bash scripts/setup-symlinks.sh                                     # create/refresh default.toml links
bin/load <name>                                                    # debug: print resolved manifest

scripts/mcp-versions.sh check [--strict]     # pin drift vs npm/PyPI latest (strict → exit 1)
scripts/mcp-versions.sh update [--all | <capability> ...]   # rewrite pins; leaves changes uncommitted
scripts/mcp-versions.sh test [<capability> ...]             # spawn servers, MCP handshake, tools/list

pre-commit run --all-files                   # local hooks: shfmt, whitespace, check-toml, 4 lints
octomind run <name>                          # smoke-test an agent from repo root
octomind workflow <name> --dry-run           # validate a workflow, run nothing
bash scripts/smoke-render.sh [dir]           # install artifact CLIs, render deck/PDF/DOCX/resume/thumbnail/captions

cd model && uv sync && bin/train             # embedding model full pipeline (--skip-export to skip ONNX)
```

- All lint scripts and `mcp-versions.sh` need Python 3.11+ (or `pip install tomli`).
- `pre-commit` runs `shfmt -w -s -i 2 -ci` on shell scripts — run it before committing dep scripts; `lint-deps.sh` is **not** in pre-commit, run it manually.
- CI: `.github/workflows/lint.yml` runs setup-symlinks, lint-manifests, lint-capabilities, validate-capabilities, lint-skills, lint-deps, and `scripts/test-seo-providers.py` on every push/PR; `test-deps.yml` runs each changed dep script twice (install + idempotency) on clean Ubuntu, macOS, and Windows; `render-smoke.yml` runs `scripts/smoke-render.sh` on Linux and macOS when the artifact CLIs or their deps change.

## Where to Look

| Task | Start here |
|------|------------|
| Add a new agent | Copy `templates/agent.toml` → `agents/<name>.toml`; spec: `skills/tap-agent-authoring/SKILL.md` |
| Add a new capability | Copy `templates/capability.toml` + `templates/capability-config.toml` → `capabilities/<name>/`; spec: `skills/tap-capability-authoring/SKILL.md` |
| Add a specialty to an agent | Add a skill (next row) with `domains: <agent name>`; a new agent only for a new field of work |
| Add a new skill | Copy `templates/skill.md` → `skills/<name>/SKILL.md`; spec: `skills/tap-skill-authoring/SKILL.md` |
| Add a new dep script | Copy `templates/dep.sh` + `templates/dep-mcp.md` or `templates/dep-tool.md` → `deps/<org>/`; spec: `skills/tap-deps-authoring/SKILL.md` |
| Add a new workflow | Copy `templates/workflow.toml` → `workflows/<name>.toml`; spec: `skills/octomind-workflow/SKILL.md` + `workflows/README.md` |
| Understand the capability system | `ARCHITECTURE.md` — design, capability table, access tiers |
| Prompt engineering theory | `skills/prompt-engineering/SKILL.md` (+ `reference/claude-4-emphasis-and-tools.md`) |
| Train the embedding model | `model/README.md`; spec: `skills/tap-model-training/SKILL.md` |
| Resolve a manifest (debug) | `bin/load <name>` — merged TOML on stdout |
| Platform helpers in dep scripts | `deps/lib/platform.sh` — source it, never re-implement |
| Tap, workflow and config authoring | `agents/octomind.toml` — it operates on the tap itself |
| Change what `octomind tap init` generates | `scaffolds/tap/` — edit `root/`, keep `scaffold.toml` and `scaffolds/tap/README.md` in sync |

## How Things Work

### Agents, skills, and delegation

- The tap has one agent per field of work (`developer`, `content`, `lawyer`, `doctor`, `video`, and so on), plus `assistant` (the global assistant) and `plain` (a baseline with a one-line system prompt and no persona, for prompt testing). An agent does its field's work itself. Its prompt is short: role, scope, the common working method, guards and output conventions.
- Each specialty procedure (QA test planning, contract review for one jurisdiction, lifecycle email) is a skill at `skills/<name>/SKILL.md`, bound to an agent by `domains: <agent name>`. A new subject or format is a new skill, not a new agent. A new agent needs a new field of work.
- A skill loads when the user's message matches its `rules:`, when a workflow step lists it in `skills = [...]`, when `OCTOMIND_SKILLS=a,b octomind run <name>` preloads it, or when `/skill use <name>` loads it by hand. Preload explicitly any skill a workflow step depends on.
- A skill can bring tools with it: `capabilities:` in its frontmatter loads them on activation. A tool that only one specialty needs is declared by that skill, not by the agent.
- Keep work that depends on the same evidence in one session. Give a delegate the relevant source, constraints, authority, and acceptance checks. Split work at an independently verifiable boundary or an independent review.
- Test a skill's rules with relevant requests next to close negatives, requests for other fields, and brief-only inputs. Check missed and false activation.

### Capability-Based Agents (the only way)

Agents declare **what they need**, not how to get it:

```toml
# ✅ correct — capability-based
capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "codesearch-semantic", "codesearch-structural", "codesearch-graph", "programming-rust"]

[[roles]]
system = "..."
welcome = "..."
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

`bin/load <name>` resolves each capability → reads `capabilities/<name>/default.toml` → merges `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]` into the final manifest at runtime. Manifests name capabilities only; users switch providers with `[capabilities] <name> = "<provider>"` in their Octomind config, never in a manifest.

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

**Version pins** — every registry-launched server (npx/uvx, including inside `sh -c`) must pin an exact package version (`pkg@X.Y.Z` / `pkg==X.Y.Z`) so a registry publish can never change what users run. `lint-capabilities.sh` enforces pin presence offline; `scripts/mcp-versions.sh` handles drift, updates, and live smoke-tests. A deliberate older pin carries `# mcp-versions: hold <package>` plus the reason; `update` skips it and `check` reports it as held.

### Agent Manifest Rules

| Field | Rule |
|-------|------|
| Header comments | `# Agent: <name>` (equals the file name), `# Title:` (5–60 chars), `# Description:` (120–155 chars) — required, linted; no `# Default:` header exists |
| `capabilities = [...]` | Required at top level; drives everything |
| `[[roles]]` | Exactly one entry |
| `name` | Must NOT be set — injected at runtime from the file name |
| `system` | Required; XML-tagged blocks in canonical order (below); stable run-to-run for prompt caching |
| `welcome` | Required; `{{CWD}}` and `{{DATE}}` allowed here only — they break caching if used in `system` |
| `temperature` / `top_p` / `top_k` | Deprecated; octomind ignores them and sends no sampling parameters, so do not set them |
| `model` | Optional override, `"<provider>:<model>"` |

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
- No tap-relative paths (`skills/…`, `capabilities/…`, `deps/…`) in `system` or `welcome` — agents run in the project workdir, not the tap checkout; name the skill instead (the `octomind` agent is exempt)
- Every `` `name` skill `` mentioned must exist at `skills/<name>/SKILL.md`
- The path is `agents/<name>.toml`: no subdirectories and no symlinks (`AGENT_PATH`, `AGENT_SUBDIR`, `AGENT_SYMLINK`); the name starts with a lowercase letter and is lowercase letters, digits and hyphens, never a `:` (`AGENT_NAME_INVALID`); the `# Agent:` header equals the file name (`MISSING_AGENT_HEADER`, `AGENT_HEADER_MISMATCH`)
- No manifest carries a `# Default:` header (`DEFAULT_HEADER_REMOVED`)
- `{{SPECIALISTS}}`, `{{USES}}` and `{{DOMAINS}}` are rejected in `system` (`SPECIALISTS_REMOVED`, `USES_PLACEHOLDER_REMOVED`, `DOMAINS_REMOVED`)
- A `# Uses:` header lists `*` or existing agent names; entries are unique, not the agent itself (`USES_INVALID`, `USES_UNKNOWN`), and agents must not use each other in a loop (`USES_CYCLE`); an agent with the header declares `orchestration` (`USES_NO_ORCHESTRATION`)

Full authoring spec, rationale, anti-patterns: `skills/tap-agent-authoring/SKILL.md`.

### Capability Access Tiers (least privilege)

| Tier | Capability | Tools | Who declares it |
|------|-----------|-------|-----------------|
| self-management | `core` | `recall` (planning is not a tool: a plugin sets the plan) | **every** agent |
| do the work | domain caps | `shell`, `filesystem-*`, `codesearch-*`, `legal-*`, … | per agent |
| own sub-agents | `agent` | `agent_*` | agents that run their own configured sub-agents (`assistant`) |
| orchestration | `orchestration` | `tap`, `schedule`, `monitor` | agents that start copies of themselves (for example `developer`); `assistant`, which also hands tasks to other agents through `# Uses: *` |
| runtime config | `runtime` | `mcp`, `agent`-register, `skill`, `capability` | high-trust only; declared by `octomind` |

An agent declares `core` + the capabilities its field needs. `orchestration` is declared only by agents that start copies of themselves or hand tasks to other agents; `runtime` is declared only by `octomind`. Each server enters the tool surface only when declared. `orchestration`/`runtime` may also auto-activate on intent via their `config.toml` triggers; that is temporary, never a standing grant.

### Running and delegating

The tag of an agent is its file name, with no `:`.

- `octomind run <name>` starts that agent. `octomind run` with no argument starts the config `default`, which is `assistant`.
- A role in the user's local config with the same name as a tap agent takes priority over the tap agent.
- A tag written with `:` is an error that shows the flat form.
- `octomind run <name> --readonly` starts a session that is offered and runs only tools whose MCP `readOnlyHint` annotation is true. A tool with no hint counts as mutable, and shell runners declare `readOnlyHint: false`, so a read-only session has no shell and cannot delegate.

An agent that declares `orchestration` delegates with the `tap` tool. It can start copies of itself (`role` set to its own name, or no `role` when it has no `# Uses:` header). Each copy is a fresh session of the same agent. `readonly: true` starts a read-only copy that scouts before a large change or reviews finished work independently. Several writable copies can run at once for independent parts, each on its own files. A copy cannot start further copies.

The `# Uses:` header is a comma-separated list of agent names, or `*` for every other agent. It sets which other agents this agent's `tap` runs can be matched to. `tap` matches a task to an agent by comparing the brief with each reachable agent's `# Title:` and `# Description:`, so those headers specify the work and deliverable. In this tap only `assistant` carries the header, as `# Uses: *`: it is the one agent that hands tasks across fields.

```toml
# agents/assistant.toml
# Uses: *
```

The placeholders `{{SPECIALISTS}}`, `{{USES}}` and `{{DOMAINS}}` in `system` are not expanded, and the lint rejects them. Detail: `ARCHITECTURE.md`, "Agents, Skills, and Delegation". `octomind tap init` generates the starter agent at `agents/<name>.toml`.

### Multi-Step Pipelines (external)

Agents are `capabilities` + one `[[roles]]` — they do **not** define pipelines.

Orchestration is an external CLI: `octomind workflow <file.toml|name>` — portable TOML chaining `octomind run` invocations (sequential / parallel / loop / conditional steps, plus graph routing via `entry`, `max_transitions`, `[[edges]]`), piping output between steps by name (`{{input}}`, `{{<step-name>}}`). Rules that bite:

- Workflows fetched from a tap may use **tap agents only** (a step `role` is an agent name such as `developer`, never a tag with `:`) — no local config roles; this keeps them portable. A step that needs a specialty preloads skills: `role = "developer"`, `skills = ["spec-authoring"]`.
- Driving input arrives on stdin; validate with `--dry-run` before running.
- Author with `templates/workflow.toml`, the `octomind-workflow` skill, or the `octomind` agent; catalogue: `workflows/README.md`.

`[[commands]]` in Octomind config (not tap manifests) define the slash commands run with `/run <name>`; they delegate via `command = "octomind acp <role>"`.

### Naming Conventions

- **Agent files**: `agents/<name>.toml` — directly under `agents/`, lowercase letters, digits and hyphens; one agent per field of work
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
domains: developer devops   # agent names the skill is bound to; omit for manual-only
rules:                      # auto-activation expressions; omit for manual-only
  - content(rust)
  - file(Cargo.toml) match((?i)\b(compil\w+|panic\w*|\w+\.rs)\b)
  - content(rust) content(async)
---
```

Optional dirs alongside SKILL.md: `scripts/`, `references/`, `assets/`, plus a `validate` executable.

**Activation — four methods:**

- Workflow step: `skills = ["spec-authoring"]` on the step preloads the skills it depends on
- Env preload: `OCTOMIND_SKILLS=programming-rust,git-workflow octomind run developer` (permanent, no rules evaluated)
- Auto-activation: skills whose `domains` include the running agent's name get their `rules` evaluated on conversation events; already-active skills are skipped. A skill loads only when the request shows the work: every rule line needs a message check (`content`, `match` or `semantic`); `file`/`grep`/`bin`/`env`/`workdir` only narrow a line, since alone they fire for any request in a matching repo. `session(...)` alone is allowed by the lint, but tap skills do not use it.
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
| `session(<word>)` | Session name contains the word — default `YYMMDD-<dir>-HHMM-<id>`, tap runs `tap-<agent name>-<hex>`, so it cannot tell specialties apart; tap skills use message checks |

**Script:** `validate` runs in the project workdir at the end of an assistant turn. It receives `assistant` as argv[1] and the assistant message on stdin; non-zero = invalid, and its stderr (stdout if stderr is empty) is fed back to the LLM (retries capped by `[skills] max_retries`). It must be executable. Octomind never runs a file named `activate`; `/skill` only lists it. Auto-activation works through `rules` only.

**Body — U-shape section order:** Overview (top) → Mental model → Rules → Examples → Checklist (near the end — final gate) → Composition / References. Under ~2000 words; beyond that, context rot hits skill recall.

**Hard rules enforced by `lint-skills.sh`:** valid frontmatter; required fields and length limits; `name` matches directory; non-empty body; every `reference/<file>` cited exists; `validate` executable; no `**bold**` in body outside code; every rule line has a message check (`RULE_NO_INTENT`); no unknown check types (`RULE_UNKNOWN_CHECK`).

**Agent binding:** `domains:` lists agent names (each must have `agents/<name>.toml`, else `DOMAIN_UNKNOWN`) and is single-valued where possible; the body does not name other agents; `compatibility:` describes environment only. Handing work to another agent is the delegating agent's job.

### Adding a New Capability (full checklist)

1. Create `capabilities/<name>/config.toml` — `triggers = [...]` (required), optional `domains` gate
2. Create `capabilities/<name>/<provider>.toml` — header comments + `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`; pin exact versions for npx/uvx servers
3. Add `link "<name>" "<provider>.toml"` **and** `"<name>"` to the `DECLARED` array in `scripts/setup-symlinks.sh`
4. Run `bash scripts/setup-symlinks.sh` (exits 1 on MISSING, warns on undeclared dirs)
5. Create any `deps/<org>/<tool>.sh` + `.md` referenced in `[deps] require`
6. Reference `"<name>"` in agent `capabilities = [...]` — `default.toml` picks the provider; users override it in their own `[capabilities]` config
7. Adding capability triggers changes `model/` training data — see `skills/tap-model-training/SKILL.md` for retraining

### Placeholders

| Placeholder | Scope | Use |
|-------------|-------|-----|
| `{{CWD}}` | Session | Current working directory — `welcome` only in agents (breaks caching in `system`) |
| `{{DATE}}` | Session | Current date — same caching rule |
| `{{ENV:KEY}}` | Project env | Injects environment variable (e.g. API keys) in capability files; document required vars in the capability header comment |
| `{{INPUT:KEY}}` | User-global secret | API tokens, credentials (e.g. in `[[mcp.servers]] env`) |
| `{{SPECIALISTS}}`, `{{USES}}`, `{{DOMAINS}}` | Not placeholders | Not expanded; rejected in `system` by lint |

## Done

Run the commands that touch what you changed — all must exit 0:

```bash
bash scripts/lint-manifests.sh        # touched agents/…toml
bash scripts/lint-capabilities.sh     # touched capabilities/…
bash scripts/lint-skills.sh           # touched skills/…
bash scripts/lint-deps.sh             # touched deps/…
bash scripts/lint-workflows.sh        # touched workflows/… or the README workflow count
bash scripts/validate-capabilities.sh # any capability change
bash scripts/setup-symlinks.sh        # any capability add/remove (symlink integrity)
bin/load <name>                       # touched agent — resolves without errors
scripts/mcp-versions.sh test <capability>  # touched npx/uvx server wiring
octomind workflow <name> --dry-run    # touched workflow
```

**Agent done** — lints pass (incl. markdown/cache guardrails); XML blocks in canonical order; every capability has `capabilities/<name>/default.toml`; all `require` entries exist under `deps/`; `welcome` is descriptive and includes `{{CWD}}`; `# Agent:` equals the file name; `octomind run <name>` starts clean.

**Skill done** — lints pass; `name` matches directory; `domains:` names existing agents; canonical section order with Checklist near the end; instructions actionable (what to DO); names no other agent.

**Capability done** — lints pass; `default.toml` symlink resolves; pins present; `mcp-versions.sh test` speaks MCP.

**Dep done** — `lint-deps.sh` passes (headers, `# type:`, companion `.md`, platform coverage); `bash deps/<org>/<tool>.sh` exits 0 on an already-installed machine and installs on a clean one.

**Full-repo done** — all six lint scripts + `pre-commit run --all-files` exit 0.

## Gotchas

- `bin/load` uses a regex-based TOML-subset parser (no external deps) — keep capability files simple: no multi-line arrays or complex TOML features.
- Don't put a heredoc or here-string over 512 bytes in a shell script: bash 5.1+ writes it into a pipe before anything reads it, and macOS pipes can hold only 512 bytes, so the script hangs. Python goes in `scripts/<name>.py`, test data in `scripts/fixtures/`.
- A symlink or subdirectory under `agents/` fails lint (`AGENT_SYMLINK`, `AGENT_SUBDIR`); every agent is a regular file `agents/<name>.toml`.
- `setup-symlinks.sh` uses `ln -sf` (force) — safe to re-run; the `DECLARED` array must be updated manually or the script emits `WARN` for undeclared dirs.
- `capabilities/core/`, `capabilities/agent/`, and `capabilities/orchestration/` have **real** `default.toml` files — no provider variants, no `link` entries for them.
- Default providers live in `setup-symlinks.sh` — e.g. `websearch` currently defaults to `duckduckgo.toml` (not tavily). Switch a provider with `ln -sf <provider>.toml capabilities/<name>/default.toml`; reset all with `setup-symlinks.sh`.
- `templates/` and `deps/lib/platform.sh` are symlinks into `scaffolds/tap/root/` — single source of truth so generated taps never drift; edit at the scaffold source.
- The `octomind` agent is special — it operates on the tap itself and is exempt from the tap-path lint. Run `octomind run octomind` in this repo root for the tap-authoring assistant; its tap, workflow and config procedures are skills.
- `mcp-versions.sh test` may report missing-key errors for servers needing credentials — judge by whether the process starts and speaks MCP at all.

## Never

- Write `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in an agent manifest — they belong exclusively in capability files
- Set `name = "..."` inside `[[roles]]` — injected at runtime from the file name
- Add a `server_ref` without a matching `[[mcp.servers]]` block (built-ins exempt: `core`, `octofs`, `agent`, `octocode`)
- Launch an npx/uvx server without an exact version pin
- Add `orchestration` to an agent that neither starts copies of itself nor hands tasks to other agents, or `runtime` to any agent but `octomind` — `runtime` is high-trust only
- Create a capability directory without adding it to both the `link` calls and the `DECLARED` array in `setup-symlinks.sh`
- Put agents in subdirectories of `agents/`, name an agent with a `:`, or nest skills deeper than `skills/<name>/SKILL.md`
- Reference tap-relative paths in `system`/`welcome`/skill bodies — agents run in the user's project, not the tap checkout
- Give an agent a `# Uses:` header without the `orchestration` capability

## References

- `ARCHITECTURE.md` — canonical design; read before any structural change
- `CONTRIBUTING.md` — human-facing contribution guide
- `workflows/README.md` — workflow catalogue, resolution rules, TOML structure
- `model/README.md` — embedding fine-tune pipeline (dataset → train → eval gates → ONNX → HuggingFace)
- `scaffolds/tap/README.md` — `octomind tap init` token table and renderer rules
- `skills/tap-agent-authoring/SKILL.md` · `tap-capability-authoring` · `tap-skill-authoring` · `tap-deps-authoring` · `tap-model-training` — per-type authoring specs
- `skills/prompt-engineering/SKILL.md` — prompt theory across agents, skills, layer prompts
- `skills/octomind-workflow/SKILL.md` — workflow authoring spec
