# codefuturist/email

Email MCP server using standard SMTP/IMAP protocols. Works with any mail server — Gmail, Outlook, self-hosted, etc.

## MCP Server

- **Package**: `@codefuturist/email-mcp`
- **Transport**: stdio
- **Command**: `npx @codefuturist/email-mcp stdio`

## Authentication

Password-based or OAuth2 (experimental for Gmail/Microsoft 365)

| Variable | Required | Description |
|----------|----------|-------------|
| `MCP_EMAIL_ADDRESS` | Yes | Email address |
| `MCP_EMAIL_PASSWORD` | Yes | Password or app password |
| `MCP_EMAIL_IMAP_HOST` | Yes | IMAP server hostname |
| `MCP_EMAIL_SMTP_HOST` | Yes | SMTP server hostname |

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send email |
| `search_emails` | Search emails |
| `read_email` | Read email |
| `list_labels` | List labels |
| `schedule_email` | Schedule sending |

## Configuration Example

```toml
[[mcp.servers]]
name = "email"
type = "stdio"
command = "npx"
args = ["-y", "@codefuturist/email-mcp"]
timeout_seconds = 60
env = { MCP_EMAIL_ADDRESS = "your-value", MCP_EMAIL_PASSWORD = "your-value", MCP_EMAIL_IMAP_HOST = "your-value", MCP_EMAIL_SMTP_HOST = "your-value" }
tools = []
```

**Notes:** 47 tools + 7 prompts. Multi-account via ~/.config/email-mcp/config.toml. Setup wizard: npx @codefuturist/email-mcp setup.

## Links

- [Homepage](https://github.com/codefuturist/email-mcp)
