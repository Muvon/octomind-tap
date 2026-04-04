# ansvar/india-law-mcp

Indian legislation MCP server. Access indian laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/india-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/india-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Indian legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "india-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/india-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
