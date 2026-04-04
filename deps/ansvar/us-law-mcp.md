# ansvar/us-law-mcp

US legislation MCP server. Access us laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/us-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/us-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | US legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "us-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/us-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
