# Contributing to Octomind Tap

**The most valuable contribution is expertise, not code.**

If you have domain knowledge — medicine, law, finance, security, DevOps, or any other field — you can create an agent that thousands of people can run with a single command.

> Building a **private or team tap** instead of contributing here? Bootstrap one with `octomind tap init yourorg/yourtap` — see [`scaffolds/tap/`](scaffolds/tap/).

---

## What is a Tap Agent?

A tap agent is a fully-configured AI specialist that anyone can run:

```bash
octomind run developer      # The developer agent
octomind run doctor         # The doctor agent
octomind run                # The global assistant
```

Each agent is a single TOML file that defines:
- **System prompt** — The AI's role, scope, working method and guards
- **Capabilities** — The tools the agent needs, named as capabilities; the registry resolves each one to a provider and installs its dependencies before the session starts

---

## Quick Start: Create Your First Agent

### 1. Decide: Skill or Agent

The tap has one agent per field of work (`developer`, `doctor`, `lawyer`, `devops`, and so on). Each specialty inside a field is a skill bound to that agent.

- **A specialty of an existing field** (for example blood test interpretation for `doctor`) is a skill. See [Contributing a Skill](#contributing-a-skill).
- **A new field of work** with its own deliverables is an agent. Its name is the file name: lowercase letters, digits and hyphens, never a `:`. Examples: `developer`, `devops`, `finance`.

An agent starts copies of itself or hands tasks to another agent only when it declares the `orchestration` capability. Delegation matches a task to an agent from its `# Title:` and `# Description:` lines, so the description must say what the agent takes in and what it returns. The rules are in [ARCHITECTURE.md](ARCHITECTURE.md#agents-skills-and-delegation).

### 2. Copy the Template

```bash
cp templates/agent.toml agents/<name>.toml
```

### 3. Edit Your Agent

Open the file and customize:

```toml
# agents/<name>.toml
# Agent: <name>
# Title: Blood Test Interpreter
# Description: Explains blood test results (CBC, metabolic panels, lipids) in plain language, flags values to discuss with a clinician and never diagnoses.

capabilities = ["core", "filesystem-read", "websearch"]

[[roles]]
welcome = "Blood test interpreter ready. Working in {{CWD}}"

system = """
<identity>
You explain laboratory results in plain language for patients and their families.
</identity>

<scope>
Own: reading result values against reference ranges and saying what they usually mean.
Don't own: diagnosis and treatment decisions; send those to a clinician.
</scope>

<critical>
- Don't diagnose or recommend treatment.
- Don't invent reference ranges; cite the range printed on the report.
</critical>
"""
```

A manifest names capabilities and nothing else about tools. Never write `[deps]`, `[roles.mcp]` or `[[mcp.servers]]` in it; those blocks live in the capability's provider file. Declare `orchestration` only when the agent starts copies of itself or hands tasks to other agents. See [ARCHITECTURE.md](ARCHITECTURE.md#capability-access-tiers-least-privilege).

### 4. Test Locally

```bash
octomind run <name>             # the agent you added
```

### 5. Submit a Pull Request

That's it! Your agent is ready for review.

---

## Agent Manifest Reference

### Required Fields

```toml
# agents/<name>.toml
# Agent: <name>
# Title: <Short Agent Title (5–60 chars)>
# Description: <What the agent does (120–155 chars)>

capabilities = ["core"]

[[roles]]
welcome = "<Agent title> ready. Working in {{CWD}}"
system = """
<identity>
Your system prompt here.
</identity>
"""
```

The system prompt uses XML-tagged blocks in a fixed order; copy `templates/agent.toml` for the full set. `{{CWD}}` and `{{DATE}}` belong in `welcome` only, because they break prompt caching inside `system`. Do not set `name`, `temperature`, `top_p` or `top_k`.

### Optional Fields

```toml
# Override the global model
model = "openrouter:anthropic/claude-sonnet-4"
```

A new tool or install step is a capability, not a manifest field. See [MCP Server Configuration](#mcp-server-configuration) and [Creating Dependency Scripts](#creating-dependency-scripts).

### Placeholder Variables

| Placeholder | Description |
|-------------|-------------|
| `{{CWD}}` | Current working directory |
| `{{INPUT:KEY}}` | User-global secret (API tokens, credentials) |
| `{{ENV:KEY}}` | Project-scoped value (base URLs, env names) |

---

## Creating Dependency Scripts

If your agent needs tools installed, create a dependency script:

### Location

```
deps/<org>/<tool>.sh
```

### Template

```bash
#!/usr/bin/env bash
# dep: <org>/<tool>
# description: Brief description of what this installs
# check: <command-to-check-if-installed>
# https://example.com/tool-homepage

set -euo pipefail

# Resolve deps/lib/ relative to this script's location
DEPS_LIB="$(cd "$(dirname "${BASH_SOURCE[0]}")/../lib" && pwd)"
source "$DEPS_LIB/platform.sh"

# Fast path — already installed
if pkg_check <command>; then
  exit 0
fi

info "<tool> not found — installing..."

case "$OS" in
  macos)
    if pkg_check brew; then
      brew install <package>
    else
      die "brew not found. Install Homebrew first: https://brew.sh"
    fi
    ;;
  linux)
    case "$PKG_MANAGER" in
      apt)
        as_root apt-get install -y <package>
        ;;
      dnf)
        as_root dnf install -y <package>
        ;;
      pacman)
        as_root pacman -S --noconfirm <package>
        ;;
      *)
        # Universal fallback
        if pkg_check curl; then
          curl -fsSL https://example.com/install.sh | sh
        else
          die "No supported package manager found."
        fi
        ;;
    esac
    ;;
esac

info "<tool> installed successfully."
```

### Using Dependencies

A dependency script is listed in the `[deps]` block of a capability's provider file, never in an agent manifest:

```toml
# capabilities/<name>/<provider>.toml
[deps]
require = ["nodejs/node", "astral-sh/uv"]
```

The dependency system will:
1. Check if the tool is already installed
2. Install it if missing
3. Make it available for the agent session

---

## MCP Server Configuration

### Built-in Server Refs

| server_ref | Provides |
|------------|----------|
| `core` | `recall` — folded-context recall; planning is not a tool: a plugin sets the plan |
| `agent` | `agent_*` tools — delegate to your own configured sub-agents |

### Adding Custom MCP Servers

Server blocks go in a capability's provider file, `capabilities/<name>/<provider>.toml`. An agent gets the server by declaring that capability. Servers launched with `npx` or `uvx` pin an exact version.

```toml
[[mcp.servers]]
name = "my-tool"
type = "stdio"
command = "npx"
args = ["-y", "@scope/my-mcp-server@1.2.3"]
timeout_seconds = 60
tools = []  # Empty = all tools exposed
```

### Using Secrets in MCP Config

```toml
[[mcp.servers]]
name = "github"
type = "stdio"
command = "npx"
args = ["-y", "@github/mcp-server@1.2.3"]
env = { GITHUB_TOKEN = "{{INPUT:GITHUB_TOKEN}}" }
timeout_seconds = 60
tools = []
```

---

## Best Practices

### System Prompts

1. **Define the role clearly** — What is this agent? What does it do?
2. **Set boundaries** — What can it NOT do? (Important for medical/legal)
3. **Provide context** — Domain knowledge, reference tables, decision frameworks
4. **Be specific** — "You are a Blood Test Analysis Assistant" not "You are helpful"
5. **Include disclaimers** — For medical/legal/financial agents
6. **Calibrate tone for Claude 4.5+** — Don't write `CRITICAL: YOU MUST X` / `🚨 HARD RULES` / stacked `NEVER`/`ALWAYS` blocks. They over-trigger on 4.6/4.7 and dilute attention. Use plain `Use X when …` / `Don't X.` / `Do X.` Reserve all-caps for one or two genuine safety hard-stops (e.g. `Never force-push to main`). Full recipe with verbatim Anthropic guidance: [`skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md`](skills/prompt-engineering/reference/claude-4-emphasis-and-tools.md).
7. **Parallel tool use** — For tool-heavy agents, append the `<use_parallel_tool_calls>` block from the reference doc above. Anthropic's claim: takes parallel-call success from "high by default" to ~100%.

### Sampling Settings

Do not set `temperature`, `top_p` or `top_k`. Octomind ignores them and sends no sampling parameters.

### Tool Selection

- **Start minimal** — Declare only the capabilities the agent actually needs
- **Reuse existing capabilities** — List `capabilities/` before adding one
- **Consider security** — Can this agent modify files? Access secrets? Leave out `filesystem-write` and `shell` unless the work needs them

---

## Examples

### Minimal Agent

```toml
# agents/notes.toml
# Agent: notes
# Title: Note-Taking Assistant
# Description: Organizes notes, writes summaries and structures information from the files you point it at, keeping your wording and never inventing content.

capabilities = ["core", "filesystem-read", "filesystem-write"]

[[roles]]
welcome = "Note-taking agent ready. Working in {{CWD}}"

system = """
<identity>
You are a note-taking assistant. You organize thoughts, write summaries and structure information.
</identity>

<critical>
- Don't invent content that is not in the user's notes.
</critical>
"""
```

### Agent with a Toolchain

An agent that needs a toolchain declares the capability that installs it. The capability's provider file requires the dependency script.

```toml
# agents/rustacean.toml
# Agent: rustacean
# Title: Rust Developer
# Description: Builds, tests and reviews Rust crates with cargo, clippy and rustfmt, and reports the exact command output behind every claim it makes.

capabilities = ["core", "filesystem-read", "filesystem-write", "shell", "programming-rust"]

[[roles]]
welcome = "Rust developer ready. Working in {{CWD}}"

system = """
<identity>
You are a Rust development specialist.
</identity>

<critical>
- Don't claim a build or test passed without running it.
</critical>
"""
```

---

## Review Process

1. **Automated checks** — Manifest syntax, required fields
2. **Manual review** — System prompt quality, appropriate tools
3. **Testing** — Agent runs correctly with `octomind run <name>`
4. **Merge** — Agent becomes available to all users

---

## Need Help?

- **GitHub Issues** — Ask questions, report bugs, request agents
- **GitHub Discussions** — "What specialist agent would you run if it existed?"
- **Existing Agents** — Study `agents/doctor.toml` as a reference

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Thank you for sharing your expertise!** Every agent and skill you create helps someone work smarter in their domain.

---

## Contributing a Skill

Skills are a different kind of contribution from agents. Where an agent covers a whole field of work, a skill encodes **one specialty's knowledge** that its agent activates on demand.

### What is a skill?

A skill is a `SKILL.md` file stored at `skills/<name>/SKILL.md`. When activated in an Octomind session, its full content is injected into the AI's context — giving it specific conventions, workflows, checklists, or decision guides for a particular task.

**Good skill candidates:**
- Coding conventions for a language or framework
- Git workflow and commit message rules
- Code review checklists
- Security audit procedures
- API design guidelines
- Deployment runbooks

**Not a good skill** (use an agent instead):
- Something that needs its own model settings
- A whole new field of work (a new agent)

Note: Skills **can** declare `capabilities` to auto-load MCP servers when activated. A skill that needs git tools can declare `capabilities: git` and the backing MCP server loads automatically.

### Skill vs Agent

| | Skill | Agent |
|---|---|---|
| **File** | `skills/<name>/SKILL.md` | `agents/<name>.toml` |
| **Activation** | Manual via `skill` tool, or auto via `rules:` frontmatter field | `octomind run <name>` |
| **What it provides** | Domain knowledge + capabilities + validation | Full role: model, tools, system prompt |
| **Composable** | Yes — multiple skills per session | No — one role per session |
| **Auto-expand** | Yes — can auto-load MCP servers via capabilities | No — tools are static |

### Step-by-step: Create a skill

**1. Choose a name**

Lowercase, hyphens only, max 64 chars. Be specific:
- ✅ `rust-error-handling`, `git-workflow`, `openapi-design`
- ❌ `rust`, `git`, `api` (too generic)

**2. Copy the template**

```bash
cp templates/skill.md skills/<name>/SKILL.md
```

**3. Fill in the frontmatter**

```markdown
---
name: my-skill-name
title: "My Skill Name"
description: "One sentence: what this skill does and when to use it."
license: Apache-2.0
compatibility: "Requires git. Works with any project."
capabilities: git memory
domains: developer devops
rules:
  - content(keyword)                          # activate if the user message contains keyword
  - content(deploy) file(some-marker-file)    # message contains deploy AND the file exists in workdir
---
```

- `capabilities` — auto-loads MCP servers when skill activates (optional, space-delimited)
- `domains` — the agent names the skill is bound to; auto-activation applies only in those agents (optional, omit for manual-only)
- `rules` — list of auto-activation expressions; every line needs a message check (`content`, `match`); omit for manual-only skills

**Available rule expressions:**

| Expression | Matches when |
|------------|-------------|
| `file(<glob>)` | File matching glob exists in working directory (`*` and `**` supported) |
| `content(<word>)` | User message contains the word (whole-word, case-insensitive) |
| `match(<pattern>)` | User message matches the regular expression |
| `grep(<pattern>, <glob>)` | A file matching the glob contains a line matching the pattern |
| `env(<VAR>)` | Environment variable `VAR` is set (non-empty) |
| `env(<VAR>=<value>)` | Environment variable `VAR` equals `value` |
| `bin(<command>)` | Command is available in `$PATH` (detects installed runtimes/tools) |
| `workdir(<pattern>)` | Current working directory path contains the pattern (substring) |
| `session(<word>)` | Current session name contains the word. Tap-run sessions are named `tap-<agent name>-<hex>`, so tap skills use message checks instead |

Logic: each list item is an **OR branch**; multiple expressions on the same line are **AND**.

**4. Write the body**

Structure:
1. **Overview** — 2–4 sentences on what problem this solves
2. **Instructions** — Core rules, workflows, decision guides (the main content)
3. **Examples** — Concrete input/output pairs (most valuable part)
4. **References** — Links to docs or bundled reference files

**5. Add optional files and directories** (if needed)

```
skills/<name>/
  SKILL.md
  validate      ← validation script (chmod +x, exit 0 = valid, stderr = error)
  scripts/      ← executable scripts the skill references
  references/   ← supplementary docs (REFERENCE.md, FORMS.md, etc.)
  assets/       ← templates, config files, resources
```

`validate` receives event type (`user`|`assistant`|`turn`) as argv[1] and content on stdin. It runs in the project working directory.

**6. Validate**

```bash
bash scripts/lint-skills.sh skills/<name>
```

**7. Test in a session**

```bash
octomind run octomind       # the tap-authoring agent; it has the skill tool
# Then in session:
# skill(action="use", name="<name>")
```

**8. Submit a Pull Request**

That's it! Include a brief description of what domain knowledge the skill encodes.

### Skill quality checklist

- [ ] `name` matches the directory name exactly
- [ ] `title` is a short human-readable label (5–60 chars)
- [ ] `description` tells you *when* to activate the skill (not just what it is)
- [ ] `compatibility` lists any required tools or environment constraints
- [ ] `capabilities` lists all capabilities the skill needs (if any)
- [ ] `domains` lists the agent names that own the skill (if auto-activation desired)
- [ ] `rules` lists auto-activation expressions if auto-activation is desired
- [ ] Body has at least an Overview and Instructions section
- [ ] Instructions are specific enough to follow without guessing
- [ ] Non-obvious rules have examples
- [ ] `validate` script is executable if present (`chmod +x`)
- [ ] `bash scripts/lint-skills.sh skills/<name>` passes
