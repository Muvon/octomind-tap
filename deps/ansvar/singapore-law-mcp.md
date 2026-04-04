# ansvar/singapore-law-mcp

Singaporean legislation MCP server. Access singaporean laws, statutes, and legal references via Ansvar.

## MCP Server

- **Package**: `@ansvar/singapore-law-mcp`
- **Transport**: stdio
- **Command**: `npx -y @ansvar/singapore-law-mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Singaporean legislation and legal reference tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "singapore-law-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@ansvar/singapore-law-mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/ansvar)
