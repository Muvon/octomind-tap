# ansvar/uk-law-mcp

UK legislation MCP server. Access uk laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/uk-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/uk-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | UK legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "uk-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/uk-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
