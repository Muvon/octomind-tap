# ansvar/australian-law-mcp

Australian legislation MCP server. Access australian laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/australian-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/australian-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Australian legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "australian-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/australian-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
