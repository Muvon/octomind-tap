# ansvar/thailand-law-mcp

Thai legislation MCP server. Access thai laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/thailand-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/thailand-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Thai legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "thailand-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/thailand-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
