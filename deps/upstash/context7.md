# upstash/context7

Context7 MCP server. Access up-to-date library documentation and code examples for any programming library.

## MCP Server

- **Package**: `@upstash/context7-mcp`
- **Transport**: stdio
- **Command**: `npx -y @upstash/context7-mcp`

## Authentication

None for basic use (API key for higher rate limits via context7.com/dashboard)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `resolve-library-id` | Find library by name |
| `query-docs` | Query library documentation |

## Configuration Example

```toml
[[mcp.servers]]
name = "context7"
type = "stdio"
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Setup: npx ctx7 setup. Free tier available.

## Links

- [Homepage](https://github.com/upstash/context7-mcp)
