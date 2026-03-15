# Contributing to Octomind Tap

**The most valuable contribution is expertise, not code.**

If you have domain knowledge — medicine, law, finance, security, DevOps, or any other field — you can create an agent that thousands of people can run with a single command.

---

## What is a Tap Agent?

A tap agent is a fully-configured AI specialist that anyone can run:

```bash
octomind run doctor:blood      # Blood test interpreter
octomind run developer:rust    # Rust development specialist
octomind run devops:kubernetes  # Kubernetes expert
```

Each agent is a single TOML file that defines:
- **System prompt** — The AI's personality, knowledge, and behavior
- **Model settings** — Temperature, top_p, top_k for optimal responses
- **MCP servers** — Tools the agent can use (databases, APIs, filesystem)
- **Dependencies** — Tools that auto-install before the session starts

---

## Quick Start: Create Your First Agent

### 1. Choose Your Domain and Spec

- **Domain**: The category (doctor, developer, devops, security, finance, lawyer, etc.)
- **Spec**: The specialization (blood, rust, kubernetes, owasp, analyst, contracts)

Examples:
- `doctor:blood` — Blood test analysis
- `developer:rust` — Rust development
- `devops:kubernetes` — Kubernetes management
- `security:owasp` — OWASP security review
- `finance:analyst` — Financial statement analysis

### 2. Copy the Template

```bash
cp templates/agent.toml agents/<domain>/<spec>.toml
```

### 3. Edit Your Agent

Open the file and customize:

```toml
# agents/doctor/blood.toml
# Agent: doctor:blood
# Description: Blood test results interpreter. Explains CBC, metabolic panels...

[[roles]]
temperature = 0.15
top_p = 0.9
top_k = 0
welcome = "🩸 Blood test analysis agent ready..."

system = """
You are a Blood Test Analysis Assistant...

[Your detailed system prompt here]
"""

[roles.mcp]
server_refs = ["core", "octofs", "medical"]
allowed_tools = ["core:*", "octofs:*", "search-medical-literature"]
```

### 4. Test Locally

```bash
octomind run doctor:blood
```

### 5. Submit a Pull Request

That's it! Your agent is ready for review.

---

## Agent Manifest Reference

### Required Fields

```toml
# agents/<domain>/<spec>.toml
# Agent: <domain>:<spec>
# Description: One-line description of what this agent does.

[[roles]]
temperature = 0.3          # 0.0–1.0 (lower = more deterministic)
top_p = 0.9                 # 0.0–1.0 (nucleus sampling)
top_k = 0                   # 0 = disabled
welcome = "🩸 Agent ready. Working in {{CWD}}"
system = """
Your system prompt here.

Working directory: {{CWD}}
"""
```

### Optional Fields

```toml
# Override the global model
model = "openrouter:anthropic/claude-sonnet-4"

# MCP server configuration
[roles.mcp]
server_refs = ["core", "octofs", "octocode"]
allowed_tools = ["core:*", "octofs:*", "semantic_search"]

# Additional MCP servers (beyond built-in)
[[mcp.servers]]
name = "medical"
type = "stdio"
command = "medical-mcp-server"
args = []
timeout_seconds = 60
tools = []

# Dependencies (auto-install before session)
[deps]
require = ["medical/medical", "astral-sh/uv"]
```

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
        sudo apt-get install -y <package>
        ;;
      dnf)
        sudo dnf install -y <package>
        ;;
      pacman)
        sudo pacman -S --noconfirm <package>
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

### Using Dependencies in Agents

```toml
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
| `core` | `plan` — structured task tracker |
| `octofs`     | `view`, `text_editor`, `batch_edit`, `shell`, `workdir`, `ast_grep` |
| `octocode` | `semantic_search`, `remember`, `memorize`, `view_signatures`, `graphrag` |
| `octobrain` | Knowledge graph and reasoning tools |
| `agent` | `agent_*` tools — delegate to configured layers |
| `tavily` | `tavily_search`, `tavily_extract`, `tavily_map` — web search |

### Adding Custom MCP Servers

```toml
[[mcp.servers]]
name = "my-tool"
type = "stdio"
command = "npx"
args = ["-y", "@scope/my-mcp-server"]
timeout_seconds = 60
tools = []  # Empty = all tools exposed
```

### Using Secrets in MCP Config

```toml
[[mcp.servers]]
name = "github"
type = "stdio"
command = "npx"
args = ["-y", "@github/mcp-server"]
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

### Temperature Settings

| Domain | Recommended | Why |
|--------|-------------|-----|
| Medical/Legal | 0.1–0.2 | Precision matters |
| Code Review | 0.2–0.3 | Accuracy over creativity |
| Development | 0.1–0.3 | Consistent, correct code |
| Creative Writing | 0.7–0.9 | Variety and exploration |
| General Chat | 0.4–0.6 | Balanced |

### Tool Selection

- **Start minimal** — Only include tools the agent actually needs
- **Use wildcards** — `"octofs:*"` for full file access
- **Be specific** — `["view", "shell"]` for restricted access
- **Consider security** — Can this agent modify files? Access secrets?

---

## Examples

### Minimal Agent

```toml
# agents/utility/notes.toml
# Agent: utility:notes
# Description: Quick note-taking assistant

[[roles]]
temperature = 0.5
top_p = 0.9
top_k = 0
welcome = "📝 Note-taking agent ready. Working in {{CWD}}"

system = """
You are a note-taking assistant. Help users organize thoughts, create summaries, and structure information.

Working directory: {{CWD}}
"""

[roles.mcp]
server_refs = ["core", "octofs"]
allowed_tools = ["core:*", "octofs:*"]
```

### Complex Agent with Dependencies

```toml
# agents/developer/rust.toml
# Agent: developer:rust
# Description: Rust development specialist with cargo, clippy, and rustfmt

[deps]
require = ["rust/cargo"]

[[roles]]
temperature = 0.1
top_p = 0.2
top_k = 10
welcome = "🦀 Rust developer agent ready. Working in {{CWD}}"

system = """
You are a Rust development specialist...

[Detailed system prompt]
"""

[roles.mcp]
server_refs = ["core", "octofs", "octocode"]
allowed_tools = ["core:*", "octofs:*", "octocode:*"]
```

---

## Review Process

1. **Automated checks** — Manifest syntax, required fields
2. **Manual review** — System prompt quality, appropriate tools
3. **Testing** — Agent runs correctly with `octomind run <domain>:<spec>`
4. **Merge** — Agent becomes available to all users

---

## Need Help?

- **GitHub Issues** — Ask questions, report bugs, request agents
- **GitHub Discussions** — "What specialist agent would you run if it existed?"
- **Existing Agents** — Study `agents/doctor/blood.toml` as a reference

---

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

---

**Thank you for sharing your expertise!** Every agent you create helps someone work smarter in their domain.
