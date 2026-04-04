# ansvar/canadian-law-mcp

Canadian legislation MCP server. Access canadian laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/canadian-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/canadian-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Canadian legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "canadian-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/canadian-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
