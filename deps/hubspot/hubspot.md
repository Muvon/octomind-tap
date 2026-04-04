# hubspot/hubspot

HubSpot CRM MCP server. Manage contacts, deals, companies, and custom objects.

## MCP Server

- **Package**: `@hubspot/mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @hubspot/mcp-server`

## Authentication

API key (Private App Token)

| Variable | Required | Description |
|----------|----------|-------------|
| `HUBSPOT_API_KEY` | Yes | Private app access token from HubSpot |

## Available Tools

| Tool | Description |
|------|-------------|
| `manage_contacts` | Contact operations |
| `manage_deals` | Deal tracking |
| `manage_companies` | Company info |
| `custom_objects` | Custom object operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "hubspot"
type = "stdio"
command = "npx"
args = ["-y", "@hubspot/mcp-server"]
timeout_seconds = 60
env = { HUBSPOT_API_KEY = "your-value" }
tools = []
```

**Notes:** Official HubSpot package.

## Links

- [Homepage](https://www.npmjs.com/package/@hubspot/mcp-server)
