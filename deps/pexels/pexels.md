# pexels/pexels

Pexels MCP server. Free, attribution-optional stock video and photos. The best zero-cost b-roll source for ad creative.

## MCP Server

- **Package**: `pexels-mcp-server` (community)
- **Transport**: stdio
- **Command**: `npx -y pexels-mcp-server`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `PEXELS_API_KEY` | Yes | API key from pexels.com/api → register a new app |

## Available Tools

| Tool | Description |
|------|-------------|
| `pexels_search_videos` | Search videos by query, filter by orientation/size/duration |
| `pexels_search_photos` | Search photos by query |
| `pexels_get_video` | Fetch a video by ID with all rendition URLs |
| `pexels_curated_photos` | Editorially curated photo feed |
| `pexels_popular_videos` | Currently popular videos |

## Configuration Example

```toml
[[mcp.servers]]
name = "pexels"
type = "stdio"
command = "npx"
args = ["-y", "pexels-mcp-server"]
timeout_seconds = 60
env = { PEXELS_API_KEY = "{{INPUT:PEXELS_API_KEY}}" }
tools = []
```

**Notes:** API is free with a generous quota (200 req/hr, 20k req/mo). Always download the right rendition for the target aspect ratio.

## Links

- [Pexels API docs](https://www.pexels.com/api/documentation/)
