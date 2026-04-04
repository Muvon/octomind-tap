# brave/brave-search

Brave Search API MCP server. Web search, local search, video, image, and news results with AI summaries.

## MCP Server

- **Package**: `@modelcontextprotocol/server-brave-search`
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-brave-search`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `BRAVE_API_KEY` | Yes | Brave Search API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `brave_web_search` | Web search with filtering |
| `brave_local_search` | Local business search |
| `brave_video_search` | Video search |
| `brave_image_search` | Image search |
| `brave_news_search` | News search |
| `brave_summarizer` | AI-powered summaries |

## Configuration Example

```toml
[[mcp.servers]]
name = "brave-search"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-brave-search"]
timeout_seconds = 60
env = { BRAVE_API_KEY = "your-value" }
tools = []
```

**Notes:** DEPRECATED — use @brave/brave-search-mcp-server instead.

## Links

- [Homepage](https://github.com/brave/brave-search-mcp-server)
