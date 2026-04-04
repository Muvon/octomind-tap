# google/search-console

Google Search Console MCP server. Query search analytics, inspect URLs, and detect SEO optimization opportunities.

## MCP Server

- **Package**: `mcp-server-gsc`
- **Transport**: stdio
- **Command**: `npx -y mcp-server-gsc`

## Authentication

Service Account

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Service account JSON file path |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_analytics` | Query GSC data with dimensions/filters, up to 25,000 rows |

## Configuration Example

```toml
[[mcp.servers]]
name = "search-console"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-gsc"]
timeout_seconds = 60
env = { GOOGLE_APPLICATION_CREDENTIALS = "your-value" }
tools = []
```

**Notes:** Supports regex filtering and automatic quick wins detection.

## Links

- [Homepage](https://www.npmjs.com/package/mcp-server-gsc)
