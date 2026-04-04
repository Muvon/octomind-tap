# resend/resend

Resend email sending and management MCP server. Send emails, manage contacts, broadcasts, domains, and webhooks.

## MCP Server

- **Package**: `resend-mcp`
- **Transport**: stdio
- **Command**: `npx -y resend-mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `RESEND_API_KEY` | Yes | API key from Resend |
| `SENDER_EMAIL_ADDRESS` | No | Default sender email |

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send email |
| `batch_send` | Batch send |
| `list_emails` | List emails |
| `manage_contacts` | Contact management |
| `create_broadcast` | Create campaign |
| `verify_domain` | Domain verification |
| `manage_webhooks` | Webhook management |

## Configuration Example

```toml
[[mcp.servers]]
name = "resend"
type = "stdio"
command = "npx"
args = ["-y", "resend-mcp"]
timeout_seconds = 60
env = { RESEND_API_KEY = "your-value", SENDER_EMAIL_ADDRESS = "your-value" }
tools = []
```

**Notes:** Requires verified domain for external sends. Supports HTML, plain text, scheduling, and attachments.

## Links

- [Homepage](https://github.com/resend/mcp-send-email)
