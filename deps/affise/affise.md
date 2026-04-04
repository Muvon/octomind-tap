# affise/affise

Affise affiliate marketing platform MCP server. Manage campaigns, track performance, search offers, and run analytics.

## MCP Server

- **Package**: `mcp-affise (GitHub only — not on npm)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm start`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `AFFISE_BASE_URL` | Yes | Affise API endpoint |
| `AFFISE_API_KEY` | Yes | API key from Affise dashboard |

## Available Tools

| Tool | Description |
|------|-------------|
| `affise_status` | API health check |
| `affise_stats` | Performance analytics |
| `affise_search_offers` | Offer discovery |
| `affise_offer_categories` | Category management |

## Configuration Example

```toml
[[mcp.servers]]
name = "affise"
type = "stdio"
command = "npx"
args = ["-y", "mcp-affise (GitHub only — not on npm)"]
timeout_seconds = 60
env = { AFFISE_BASE_URL = "your-value", AFFISE_API_KEY = "your-value" }
tools = []
```

**Notes:** Not on npm — requires git clone and local build.

## Links

- [Homepage](https://github.com/affise/mcp-affise)
