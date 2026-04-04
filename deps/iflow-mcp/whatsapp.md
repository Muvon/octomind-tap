# iflow-mcp/whatsapp

WhatsApp Web messaging MCP server. Send messages, manage contacts, and share media via WhatsApp Web protocol.

## MCP Server

- **Package**: `@iflow-mcp/mcp-whatsapp-web`
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/mcp-whatsapp-web`

## Authentication

QR code scan via get_qr_code tool on first run; session persists locally

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_qr_code` | Generate QR code for auth |
| `send_message` | Send message |
| `search_contacts` | Search contacts |
| `list_chats` | List conversations |
| `send_media` | Share media |

## Configuration Example

```toml
[[mcp.servers]]
name = "whatsapp"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/mcp-whatsapp-web"]
timeout_seconds = 60
tools = []
```

**Notes:** No env vars needed. Auth via QR code scanning with WhatsApp mobile app.

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/mcp-whatsapp-web)
