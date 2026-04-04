# <org>/<tool>

<One-paragraph summary: what this MCP server does, what platform/service it integrates with.>

## MCP Server

- **Package**: `<npm-package>` or `<pip-package>` or `<docker-image>`
- **Transport**: stdio
- **Command**: `npx -y <package>` or `uvx <package>` or `docker run <image>`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `VAR_NAME` | Yes | What this variable is for |

## Available Tools

| Tool | Description |
|------|-------------|
| `tool_name` | What it does |

## Configuration Example

```toml
[[mcp.servers]]
name = "<server-name>"
type = "stdio"
command = "npx"
args = ["-y", "<package>"]
timeout_seconds = 60
env = { VAR_NAME = "your-value" }
tools = []
```

## Links

- [Homepage](<url>)
- [npm](<npm-url>) or [GitHub](<github-url>)
