# openai/dalle

DALL-E image generation MCP server. Generate images using OpenAI's DALL-E models.

## MCP Server

- **Package**: `@microagents/mcp-server-dalle`
- **Transport**: stdio
- **Command**: `npx -y @microagents/mcp-server-dalle`

## Authentication

OpenAI API key

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Generate image from text prompt |

## Configuration Example

```toml
[[mcp.servers]]
name = "dalle"
type = "stdio"
command = "npx"
args = ["-y", "@microagents/mcp-server-dalle"]
timeout_seconds = 60
env = { OPENAI_API_KEY = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use. Alternatives: @gongrzhe/image-gen-mcp-server.

## Links

- [Homepage](https://www.npmjs.com/package/@microagents/mcp-server-dalle)
