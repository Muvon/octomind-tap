# openai/chatgpt

ChatGPT collaboration MCP server. Send queries to ChatGPT from other AI tools.

## MCP Server

- **Package**: `@chinchillaenterprises/mcp-chatgpt`
- **Transport**: stdio
- **Command**: `npx @chinchillaenterprises/mcp-chatgpt`

## Authentication

OpenAI API key

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | ChatGPT interaction tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "chatgpt"
type = "stdio"
command = "npx"
args = ["-y", "@chinchillaenterprises/mcp-chatgpt"]
timeout_seconds = 60
env = { OPENAI_API_KEY = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@chinchillaenterprises/mcp-chatgpt)
