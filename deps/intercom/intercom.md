# intercom/intercom

Intercom customer support MCP server. Manage support tickets and customer conversations.

## MCP Server

- **Package**: `@iflow-mcp/mcp-intercom`
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/mcp-intercom`

## Authentication

Access token

| Variable | Required | Description |
|----------|----------|-------------|
| `INTERCOM_ACCESS_TOKEN` | Yes | Intercom access token |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Customer support ticket management |

## Configuration Example

```toml
[[mcp.servers]]
name = "intercom"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/mcp-intercom"]
timeout_seconds = 60
env = { INTERCOM_ACCESS_TOKEN = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/mcp-intercom)
