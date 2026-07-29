# freepik/freepik

Freepik MCP server. Combines stock photos / vectors / templates with AI image and video generation under a single API. Useful when ad creative needs polished templated frames + b-roll.

## MCP Server

- **Package**: `@iflow-mcp/freepik-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/freepik-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `FREEPIK_API_KEY` | Yes | API key from freepik.com developer portal |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_resources` | Search stock resources |
| `get_resource / download_resource` | Fetch a resource |
| `generate_image` | AI image generation |
| `check_status` | Poll generation status |

## Configuration Example

```toml
[[mcp.servers]]
name = "freepik"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/freepik-mcp"]
timeout_seconds = 120
env = { FREEPIK_API_KEY = "{{INPUT:FREEPIK_API_KEY}}" }
tools = []
```

**Notes:** Pay-as-you-go credits. Useful as a single bill for stock + AI generation.

## Links

- [Freepik API](https://www.freepik.com/api)
