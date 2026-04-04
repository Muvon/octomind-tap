# ahrefs/ahrefs

Ahrefs SEO toolset MCP server. Access backlink data, keyword research, rank tracking, and site audits.

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

**Notes:** Official Ahrefs package. Paid API.

## Links

- [Homepage](https://www.npmjs.com/package/@ahrefs/mcp)
