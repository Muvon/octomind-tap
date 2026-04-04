# us-legal-tools/courtlistener

CourtListener US court case MCP server. Search court opinions, legal research, and case law.

## MCP Server

- **Package**: `@us-legal-tools/courtlistener-sdk`
- **Transport**: stdio
- **Command**: `npx -y @us-legal-tools/courtlistener-sdk`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `COURTLISTENER_API_KEY` | Yes | CourtListener API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | US court cases, opinions, legal research |

## Configuration Example

```toml
[[mcp.servers]]
name = "courtlistener"
type = "stdio"
command = "npx"
args = ["-y", "@us-legal-tools/courtlistener-sdk"]
timeout_seconds = 60
env = { COURTLISTENER_API_KEY = "your-value" }
tools = []
```

**Notes:** SDK may not function as standalone MCP server — verify implementation.

## Links

- [Homepage](https://www.npmjs.com/package/@us-legal-tools/courtlistener-sdk)
