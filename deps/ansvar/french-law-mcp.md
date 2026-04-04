# ansvar/french-law-mcp

French legislation MCP server. Access french laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/french-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/french-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | French legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "french-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/french-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
