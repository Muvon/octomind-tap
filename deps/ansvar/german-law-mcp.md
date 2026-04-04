# ansvar/german-law-mcp

German legislation MCP server. Access german laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/german-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/german-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | German legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "german-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/german-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
