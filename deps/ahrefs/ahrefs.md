# ahrefs/ahrefs

Legacy local Ahrefs MCP package documentation, retained for the existing dep script. The seo-data `ahrefs` provider uses hosted HTTP MCP with `AHREFS_MCP_TOKEN`, not this package or `AHREFS_API_KEY`; use the hosted provider for new connections.

## MCP Server

- **Package**: `@ahrefs/mcp`
- **Transport**: stdio
- **Command**: `npx -y @ahrefs/mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `AHREFS_API_KEY` | Yes | Ahrefs API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | SEO, backlinks, keywords, rank tracking tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "ahrefs"
type = "stdio"
command = "npx"
args = ["-y", "@ahrefs/mcp"]
timeout_seconds = 60
env = { AHREFS_API_KEY = "your-value" }
tools = []
```

Notes: This legacy dep is not used or validated by the hosted SEO integration; its package/API-key example above is not hosted MCP setup guidance.

## Links

- [Homepage](https://www.npmjs.com/package/@ahrefs/mcp)
