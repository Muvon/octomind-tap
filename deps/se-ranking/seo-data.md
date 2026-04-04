# se-ranking/seo-data

SE Ranking SEO data MCP server. SERP analysis, keyword research, backlinks, site audits, rank tracking, and competitor monitoring.

## MCP Server

- **Package**: `seo-data-api-mcp-server (GitHub/Docker — not on npm)`
- **Transport**: stdio
- **Command**: `Docker recommended`

## Authentication

Two separate API tokens

| Variable | Required | Description |
|----------|----------|-------------|
| `DATA_API_TOKEN` | Yes | Data API access token (UUID) |
| `PROJECT_API_TOKEN` | Yes | Project API token (40-char hex) |

## Available Tools

| Tool | Description |
|------|-------------|
| `*100+ tools*` | 70+ Data API tools (SERP, keywords, backlinks) + 30+ Project API tools (rank tracking, competitors) |

## Configuration Example

```toml
[[mcp.servers]]
name = "seo-data"
type = "stdio"
command = "npx"
args = ["-y", "seo-data-api-mcp-server (GitHub/Docker — not on npm)"]
timeout_seconds = 60
env = { DATA_API_TOKEN = "your-value", PROJECT_API_TOKEN = "your-value" }
tools = []
```

**Notes:** Not on npm. Docker recommended for deployment. 100+ tools total.

## Links

- [Homepage](https://github.com/seranking/seo-data-api-mcp-server)
