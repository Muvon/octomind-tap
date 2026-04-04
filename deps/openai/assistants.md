# openai/assistants

OpenAI Assistants API MCP server. Interact with OpenAI Assistants.

## MCP Server

- **Package**: `openai-assistants-mcp`
- **Transport**: stdio
- **Command**: `npx -y openai-assistants-mcp`

## Authentication

OpenAI API key

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | OpenAI Assistants API tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "assistants"
type = "stdio"
command = "npx"
args = ["-y", "openai-assistants-mcp"]
timeout_seconds = 60
env = { OPENAI_API_KEY = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use.

## Links

- [Homepage](https://www.npmjs.com/package/openai-assistants-mcp)
