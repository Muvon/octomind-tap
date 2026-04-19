# octomind-tap — Agent Registry Guide

Community-maintained registry of agent manifests, capability definitions, dependency scripts, and skill packs for the [Octomind](https://github.com/muvon/octomind) AI assistant. Agents declare **capabilities** (not MCP servers directly) — the `bin/load` resolver merges them at runtime. Contributions are global and public; the `octomind/` domain contains meta-agents that operate on the tap itself.

## Project Structure

```
agents/<domain>/<spec>.toml     # Agent manifests — the primary contribution type
capabilities/<name>/            # Capability definitions
  default.toml                  # Symlink → active provider (e.g. octofs.toml)
  <provider>.toml               # Actual capability file with [deps], [roles.mcp], [[mcp.servers]]
deps/<org>/<tool>.sh            # Dependency install scripts (auto-run before sessions)
deps/lib/platform.sh            # Shared platform detection helpers (source in all dep scripts)
skills/<name>/SKILL.md          # Reusable instruction packs (AgentSkills spec)
skills/<name>/activate          # Optional: auto-activation script (exit 0 = activate)
skills/<name>/validate          # Optional: validation script (exit 0 = valid, stderr = error)
bin/load                        # Python resolver: merges capabilities → final manifest (stdout)
scripts/
  lint-manifests.sh             # Validate all agent TOML files
  lint-skills.sh                # Validate all SKILL.md files
  validate-capabilities.sh      # Check capability files are well-formed
  setup-symlinks.sh             # Create/refresh default.toml symlinks for all capabilities
templates/
  agent.toml                    # Canonical agent template (copy to start a new agent)
  skill.md                      # Canonical skill template (copy to start a new skill)
  dep.sh                        # Canonical dep script template (copy to start a new dep)
ARCHITECTURE.md                 # Canonical design doc — read before making any changes
CONTRIBUTING.md                 # Contribution guidelines
```

## Where to Look

| Task | Start here |
|------|------------|
| Add a new agent | Copy `templates/agent.toml` → `agents/<domain>/<spec>.toml` |
| Understand capability system | `ARCHITECTURE.md` — full design + capability table |
| See all available capabilities | `ARCHITECTURE.md` capability table + `capabilities/` directory |
| Add a new capability | `capabilities/<name>/<provider>.toml` + update `scripts/setup-symlinks.sh` |
| Add a new dep script | Copy `templates/dep.sh` → `deps/<org>/<tool>.sh` + `templates/dep-mcp.md` or `templates/dep-tool.md` → `deps/<org>/<tool>.md` |
| Lint dep scripts | `scripts/lint-deps.sh` |
| Add a new skill | Copy `templates/skill.md` → `skills/<name>/SKILL.md` |
| Lint agents | `scripts/lint-manifests.sh` |
| Lint skills | `scripts/lint-skills.sh` |
| Resolve a manifest (debug) | `bin/load <domain>:<spec>` — prints merged TOML to stdout |
| Refresh capability symlinks | `scripts/setup-symlinks.sh` |
| Platform detection in dep scripts | `deps/lib/platform.sh` — source this, never re-implement |
| Add a workflow-based agent | Study `agents/developer/autopilot.toml` for workflow + layer patterns |
| Meta-agents (tap/skill/instructions) | `agents/octomind/` — these operate on the tap itself |

## How Things Work

### Capability-Based Agents (the only way)

Agents declare **what they need**, not how to get it:

```toml
# ✅ correct — capability-based
capabilities = ["core", "filesystem", "codesearch", "programming-rust"]

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

`bin/load <domain>:<spec>` resolves each capability → reads `capabilities/<name>/default.toml` → merges `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]` into the final manifest at runtime.

### Capability File Format

```toml
# capabilities/<name>/<provider>.toml

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
```

**Built-in servers** (`core`, `octofs`, `agent`, `octocode`) do NOT need `[[mcp.servers]]` blocks. Every other server ref MUST have a matching `[[mcp.servers]]` block in its capability file.

### Agent Manifest Rules

| Field | Rule |
|-------|------|
| `capabilities = [...]` | Required at top level; drives everything |
| `[[roles]]` | Exactly one entry |
| `name` | Must NOT be set — injected at runtime from the tag |
| `system` | Required; be as detailed as possible — specificity prevents AI drift |
| `welcome` | Required; use `{{CWD}}` for working directory |
| `temperature` | Required; 0.1–0.3 for technical, 0.4–0.6 for general |
| `top_p` | Required; 0.9 for most cases |
| `top_k` | Required; 0 to disable, 10–40 for more deterministic output |
| `workflow` | Optional; `"workflow_name"` activates a workflow pipeline before main session |

### Workflows & Layers (Multi-Step Pipelines)

Agents can define **workflows** — multi-step AI pipelines that run before the main session (`""`). Each step runs a **layer** (a separate AI instance with its own model, prompt, and tools). The main session receives the accumulated workflow output and handles the final step.

```
workflow = "my_workflow"
         ↓
   [[workflows]] steps execute sequentially
         ↓
   main session runs with all accumulated output
```

#### Workflow Definition

```toml
# In the agent manifest, after [[roles]]
[[workflows]]
name = "my_workflow"
description = "What this workflow does"

[[workflows.steps]]
name = "step_name"
type = "once"
layer = "layer_name"
```

#### Step Types

| Type | Fields | Behavior |
|------|--------|----------|
| `once` | `layer` | Run layer once |
| `loop` | `layer` or substeps, `max_iterations`, `exit_pattern` | Repeat until `exit_pattern` matches output or max iterations hit |
| `foreach` | `parse_pattern`, substeps | Iterate over regex-matched items from previous output |
| `conditional` | `layer`, `condition_pattern`, `on_match`, `on_no_match` | Run layer, then branch based on output pattern |
| `parallel` | `parallel_layers`, `aggregator` | Run multiple layers simultaneously, feed results to aggregator layer |

#### Nested Substeps

`loop` and `foreach` steps support nested substeps:

```toml
[[workflows.steps]]
name = "dev_cycle"
type = "loop"
max_iterations = 3
exit_pattern = "VERDICT:\\s*SHIP"

  [[workflows.steps.substeps]]
  name = "build"
  type = "once"
  layer = "builder"

  [[workflows.steps.substeps]]
  name = "review"
  type = "once"
  layer = "reviewer"
```

#### Layer Definition

```toml
[[layers]]
name = "layer_name"
description = "What this layer does"
model = "openrouter:google/gemini-2.5-flash"
max_tokens = 4096
temperature = 0.2
input_mode = "last"       # last | first | all — what conversation history to see
output_mode = "append"    # none | append | replace — how output enters conversation
output_role = "assistant" # assistant | user — role of the appended message
system_prompt = """..."""

[layers.mcp]
server_refs = ["octofs", "octocode"]
allowed_tools = ["octofs:view", "octocode:semantic_search"]
```

#### Layer Data Flow

| `input_mode` | Layer sees |
|-------------|-----------|
| `last` | Only the most recent message |
| `first` | Only the first message (user's original input) |
| `all` | Full conversation history |

| `output_mode` | Effect |
|--------------|--------|
| `none` | Output discarded (side effects only) |
| `append` | Output added as a new message |
| `replace` | Output replaces conversation history |

| `output_role` | Use when |
|--------------|----------|
| `user` | Layer output should be treated as instructions by the next layer |
| `assistant` | Layer output is a response/result |

#### Layer MCP Tools

Layers reference the same MCP servers that capabilities provide. `[layers.mcp]` specifies which servers and tools the layer can access — this is separate from `[roles.mcp]` (which is injected by `bin/load` for the main role).

#### Example: Autonomous Developer Pipeline

See `agents/developer/autopilot.toml` for a complete workflow-based agent:
- **scout** layer: cheap model, read-only context curation
- **builder** layer: best model, implement + test + commit
- **reviewer** layer: cheap model, code review
- **scorer** layer: no tools, quality gate with confidence score
- **main session**: finalizer, creates PR with confidence badge

### Naming Conventions

- **Agent files**: `agents/<domain>/<spec>.toml` — domain groups related agents (e.g. `developer`, `lawyer`, `devops`)
- **Capabilities**: lowercase with hyphens; use prefix grouping for related variants: `programming-rust`, `programming-python`, `legal-us`, `legal-uk`
- **Dep scripts**: `deps/<org>/<tool>.sh` — matches `require = ["<org>/<tool>"]` in capability files
- **Skills**: `skills/<name>/SKILL.md` — directory name must match `name:` field in frontmatter; lowercase, hyphens only

### Dep Script Pattern

Every dep script must:
1. Source `deps/lib/platform.sh` — all helpers and variables come from here, never re-implement them
2. Exit 0 immediately if the tool is already installed (`pkg_check <command>`)
3. Install for every supported platform: macOS (brew or official installer) + Linux (apt/dnf/pacman/zypper/apk + universal fallback)
4. Verify the tool is in PATH after install; add `~/.local/bin` or `~/.cargo/bin` if needed

**Required header comments** (parsed by tooling):
```bash
# dep: <org>/<tool>
# type: mcp|dep
# description: Brief description of what this installs
# check: <command-to-verify-installation>
# https://homepage-url
```

**Type classification:**
- `mcp` — script exists to make an MCP server runnable (ensures npx/uvx/docker)
- `dep` — script installs a standalone CLI tool or runtime used directly

**Companion documentation** — every dep script must have a matching `.md` file:
- `deps/<org>/<tool>.md` alongside `deps/<org>/<tool>.sh`
- MCP servers (`type: mcp`): must include `## MCP Server`, `## Authentication`, `## Available Tools`, `## Configuration Example`
- Plain deps (`type: dep`): must include `## Key Commands`, `## Common Usage`
- Templates: `templates/dep-mcp.md` and `templates/dep-tool.md`

**Boilerplate** (copy from `templates/dep.sh`):
```bash
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

if pkg_check "<command>"; then exit 0; fi
```

**Variables available after sourcing `platform.sh`:**

| Variable | Values |
|----------|--------|
| `$OS` | `macos` \| `linux` |
| `$ARCH` | `x86_64` \| `arm64` |
| `$PKG_MANAGER` | `brew` \| `apt` \| `dnf` \| `pacman` \| `zypper` \| `apk` \| `unknown` |
| `$IS_MACOS` | `1` or `0` |
| `$IS_LINUX` | `1` or `0` |
| `$IS_ARM64` | `1` or `0` |
| `$IS_X86_64` | `1` or `0` |

**Functions available after sourcing `platform.sh`:**

| Function | Purpose |
|----------|---------|
| `pkg_check <cmd>` | Returns 0 if command exists — use for fast-path exit and post-install verify |
| `pkg_install <pkg>` | Install via detected package manager (same name on all PMs) |
| `brew_install <formula>` | macOS only, no-op on Linux |
| `apt_install <pkg>` | Debian/Ubuntu only, no-op elsewhere |
| `dnf_install <pkg>` | Fedora/RHEL only, no-op elsewhere |
| `install_dep <org/tool>` | Run another dep script as a prerequisite; sources PATH env after |
| `info <msg>` | Print informational message to stderr |
| `warn <msg>` | Print warning to stderr |
| `die <msg>` | Print error to stderr and exit 1 |

**Platform coverage requirement** — every dep script must handle:
```bash
case "$OS" in
  macos)
    # brew preferred; fall back to official installer if brew absent
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)    ... ;;
      dnf)    ... ;;
      pacman) ... ;;
      zypper) ... ;;
      apk)    ... ;;
      *)      # universal fallback: curl/wget official installer ;;
    esac
    ;;
esac
```

### Skill Format (AgentSkills spec)

```markdown
---
name: skill-name
title: "Skill Title (5–60 chars)"
description: "What this skill does and when to use it."
license: Apache-2.0
compatibility: "Requires: tool1, tool2. macOS/Linux."
capabilities: git memory
domains: developer devops
---

# Skill Title

## Overview
...

## Instructions
...

## Examples
...
```

Required frontmatter: `name`, `title`, `description`. Directory name must match `name`.

Optional fields:
- `capabilities` — capabilities to auto-load when skill activates (space-delimited or array)
- `domains` — agent categories for auto-activation scoping (omit for manual-only)
- `allowed-tools` — space-delimited pre-approved tools

### Skill Scripts (Optional)

Skills can include `activate` and `validate` scripts alongside SKILL.md:

- **`activate`** — executable script that decides if the skill should be active. Receives event type (`user`|`assistant`|`turn`) as argv[1], content on stdin. Runs in project workdir. exit 0 = activate, non-zero = don't. Already-active skills are skipped.
- **`validate`** — executable script that validates LLM output. Runs at end of assistant turn. exit 0 = valid, non-zero = invalid (stderr fed back to LLM). Retries capped by `[skills] max_retries`.

Both must be executable (`chmod +x`). The lint script checks this.

### Environment Variable

Preload skills at session start without activate scripts:
```bash
OCTOMIND_SKILLS=programming-rust,git-workflow octomind run developer:general
```

### Adding a New Capability (full checklist)

1. Create `capabilities/<name>/<provider>.toml` with `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`
2. Add `link "<name>" "<provider>.toml"` line to `scripts/setup-symlinks.sh`
3. Add `"<name>"` to the `DECLARED` array in `scripts/setup-symlinks.sh`
4. Run `bash scripts/setup-symlinks.sh` to create the symlink
5. Reference `"<name>"` in agent `capabilities = [...]`

## Validation & Quality

### Checks to Run

```bash
# Lint all agent manifests
bash scripts/lint-manifests.sh

# Lint a specific agent
bash scripts/lint-manifests.sh agents/<domain>/<spec>.toml

# Lint all skills
bash scripts/lint-skills.sh

# Lint a specific skill
bash scripts/lint-skills.sh skills/<name>

# Lint all dep scripts (headers + companion docs)
bash scripts/lint-deps.sh

# Lint a specific dep script
bash scripts/lint-deps.sh deps/<org>/<tool>.sh

# Verify capability symlinks are intact
bash scripts/setup-symlinks.sh

# Debug: inspect the resolved manifest for an agent
bin/load <domain>:<spec>
```

### Quality Criteria — Agent is "Done" When

- [ ] All lints pass (`lint-manifests.sh`)
- [ ] Every capability in `capabilities = [...]` has a `capabilities/<name>/default.toml`
- [ ] `bin/load <domain>:<spec>` resolves without errors
- [ ] All required dep scripts exist under `deps/` for every `require` entry in used capabilities
- [ ] All dep scripts pass linting (`lint-deps.sh`) — includes `# type:` header and companion `.md`
- [ ] System prompt is detailed and domain-focused — covers what the agent does, what it won't do, and key decision rules
- [ ] `welcome` message is descriptive and includes `{{CWD}}`

### Quality Criteria — Skill is "Done" When

- [ ] `lint-skills.sh` passes
- [ ] `name` in frontmatter matches directory name exactly
- [ ] Body has Overview + Instructions + Examples sections
- [ ] Instructions are actionable (tell the AI what to DO, not just describe the domain)

## Gotchas

- `bin/load` uses a regex-based TOML parser (no external deps) — it handles the subset needed but does not parse full TOML. Keep capability files simple; don't use multi-line arrays or complex TOML features.
- `setup-symlinks.sh` uses `ln -sf` (force) — safe to re-run, but the `DECLARED` array must be updated manually when adding capabilities or the script will emit a `WARN` for undeclared dirs.
- `capabilities/core/default.toml` and `capabilities/agent/default.toml` are real files, not symlinks — they have no provider variants. Do not add `link` entries for them in `setup-symlinks.sh`.
- `{{ENV:VAR_NAME}}` in capability files injects environment variables at runtime (e.g. `TAVILY_API_KEY`). Document required env vars in the capability file header comment.
- The `octomind/` agent domain is special — these agents operate on the tap itself. Run `octomind run octomind:tap` in this repo root to use the tap-creation assistant.

## Never

- Write `[deps]`, `[roles.mcp]`, or `[[mcp.servers]]` in an agent manifest — these belong exclusively in capability files
- Set `name = "..."` inside `[[roles]]` — it is injected at runtime from the file path tag
- Add a `server_ref` in a capability file without a matching `[[mcp.servers]]` block (unless it's a built-in: `core`, `octofs`, `agent`, `octocode`)
- Create a capability directory without adding it to both the `link` calls and the `DECLARED` array in `setup-symlinks.sh`
- Nest agents deeper than `agents/<domain>/<spec>.toml` — exactly two path components required
- Nest skills deeper than `skills/<name>/SKILL.md` — exactly one directory level required
