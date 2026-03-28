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
| Add a new dep script | Copy `templates/dep.sh` → `deps/<org>/<tool>.sh` |
| Add a new skill | Copy `templates/skill.md` → `skills/<name>/SKILL.md` |
| Lint agents | `scripts/lint-manifests.sh` |
| Lint skills | `scripts/lint-skills.sh` |
| Resolve a manifest (debug) | `bin/load <domain>:<spec>` — prints merged TOML to stdout |
| Refresh capability symlinks | `scripts/setup-symlinks.sh` |
| Platform detection in dep scripts | `deps/lib/platform.sh` — source this, never re-implement |
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
# description: Brief description of what this installs
# check: <command-to-verify-installation>
# https://homepage-url
```

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
description: "What this skill does and when to use it."
license: Apache-2.0
compatibility: "Requires: tool1, tool2. macOS/Linux."
---

# Skill Title

## Overview
...

## Instructions
...

## Examples
...
```

Required frontmatter: `name`, `description`. Directory name must match `name`.

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
