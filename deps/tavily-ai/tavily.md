# tavily-ai/tavily

Tavily AI-powered web search MCP server. Real-time search, content extraction, site mapping, and systematic crawling.

## MCP Server

- **Package**: `@tavily/mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @tavily/mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `TAVILY_API_KEY` | Yes | API key from tavily.com |

## Available Tools

| Tool | Description |
|------|-------------|
| `tavily_search` | Web search |
| `tavily_extract` | Extract page content |
| `tavily_map` | Map site URLs |
| `tavily_crawl` | Systematic crawl |

## Configuration Example

```toml
[[mcp.servers]]
name = "tavily"
type = "stdio"
command = "npx"
args = ["-y", "@tavily/mcp-server"]
timeout_seconds = 60
env = { TAVILY_API_KEY = "your-value" }
tools = []
```

**Notes:** Also available as remote: https://mcp.tavily.com/mcp/?tavilyApiKey=KEY.

## Links

- [Homepage](https://github.com/tavily-ai/tavily-mcp)
