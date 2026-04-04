# serpstat/serpstat

Serpstat SEO MCP server.

## MCP Server

- **Package**: `@serpstat/serpstat-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @serpstat/serpstat-mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `SERPSTAT_API_KEY` | Yes | Serpstat API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | SERP tracking, backlinks, domain authority tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "serpstat"
type = "stdio"
command = "npx"
args = ["-y", "@serpstat/serpstat-mcp-server"]
timeout_seconds = 60
env = { SERPSTAT_API_KEY = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use.

## Links

- [Homepage](https://www.npmjs.com/package/@serpstat/serpstat-mcp-server)
