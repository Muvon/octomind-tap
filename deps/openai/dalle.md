# openai/dalle

DALL-E image generation MCP server. Generate images using OpenAI's DALL-E models.

## MCP Server

- **Package**: `openai-image-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y openai-image-mcp-server`

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

**Notes:** OpenAI retired the DALL-E 2/3 API (2026-05-12); this server targets the gpt-image family.

## Links

- [Homepage](https://www.npmjs.com/package/@microagents/mcp-server-dalle)
