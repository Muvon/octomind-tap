# zendesk/zendesk

Zendesk customer support MCP server. Manage tickets, users, organizations, macros, triggers, and Help Center articles.

## MCP Server

- **Package**: `zendesk-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y zendesk-mcp-server`

## Authentication

API token + email

| Variable | Required | Description |
|----------|----------|-------------|
| `ZENDESK_SUBDOMAIN` | Yes | Zendesk subdomain |
| `ZENDESK_EMAIL` | Yes | Admin user email |
| `ZENDESK_API_TOKEN` | Yes | Zendesk API token |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_tickets` | List tickets |
| `create_ticket` | Create ticket |
| `update_ticket` | Update ticket |
| `manage_users` | User CRUD |
| `manage_organizations` | Org management |
| `manage_articles` | Help Center articles |
| `search` | Full search |

## Configuration Example

```toml
[[mcp.servers]]
name = "zendesk"
type = "stdio"
command = "npx"
args = ["-y", "zendesk-mcp-server"]
timeout_seconds = 60
env = { ZENDESK_SUBDOMAIN = "your-value", ZENDESK_EMAIL = "your-value", ZENDESK_API_TOKEN = "your-value" }
tools = []
```

## Links

- [Homepage](https://github.com/mattcoatsworth/zendesk-mcp-server)
