# freepik/freepik

Freepik MCP server. Combines stock photos / vectors / templates with AI image and video generation under a single API. Useful when ad creative needs polished templated frames + b-roll.

## MCP Server

- **Package**: `freepik-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y freepik-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `FREEPIK_API_KEY` | Yes | API key from freepik.com developer portal |

## Available Tools

| Tool | Description |
|------|-------------|
| `freepik_search_resources` | Search the stock library (photos, vectors, icons, templates) |
| `freepik_download_resource` | Get download URL for a specific resource |
| `freepik_generate_image` | AI image generation (Mystic / Flux backends) |
| `freepik_generate_video` | AI video generation (Kling, Pixverse, Veo backends) |
| `freepik_get_task` | Poll generation status |

## Configuration Example

```toml
[[mcp.servers]]
name = "freepik"
type = "stdio"
command = "npx"
args = ["-y", "freepik-mcp"]
timeout_seconds = 120
env = { FREEPIK_API_KEY = "{{INPUT:FREEPIK_API_KEY}}" }
tools = []
```

**Notes:** Pay-as-you-go credits. Useful as a single bill for stock + AI generation.

## Links

- [Freepik API](https://www.freepik.com/api)
