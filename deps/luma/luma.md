# luma/luma

Luma AI video and image generation MCP server. Text-to-video, image-to-video, upscaling, and audio addition.

## MCP Server

- **Package**: `@runapi.ai/luma-mcp (GitHub only — not on npm)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm run build`

## Authentication

API key(s)

| Variable | Required | Description |
|----------|----------|-------------|
| `RUNAPI_API_KEY` | Yes | Luma AI API key |
| `RUNWAYML_API_SECRET` | No | Runway API key (optional) |
| `OPENROUTER_API_KEY` | No | OpenRouter API key (optional) |

## Available Tools

| Tool | Description |
|------|-------------|
| `modify_video` | Create/modify a Dream Machine video job |
| `get_task` | Poll a job |
| `check_pricing` | Gateway pricing info |
| `login` | Gateway auth check |

## Configuration Example

```toml
[[mcp.servers]]
name = "luma"
type = "stdio"
command = "npx"
args = ["-y", "@runapi.ai/luma-mcp (GitHub only — not on npm)"]
timeout_seconds = 60
env = { RUNAPI_API_KEY = "your-value", RUNWAYML_API_SECRET = "your-value", OPENROUTER_API_KEY = "your-value" }
tools = []
```

**Notes:** Not on npm. Supports multiple API providers.

## Links

- [Homepage](https://mcpservers.org/servers/wheattoast11/@runapi.ai/luma-mcp)
