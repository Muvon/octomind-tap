# google/gmail

Gmail MCP server. Send, search, read emails, manage drafts, labels, and threads.

## MCP Server

- **Package**: `@node2flow/gmail-mcp`
- **Transport**: stdio
- **Command**: `npx -y @node2flow/gmail-mcp`

## Authentication

OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | OAuth Client Secret |
| `GOOGLE_REFRESH_TOKEN` | Yes | Refresh token |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_messages` | List emails |
| `get_message` | Read email |
| `send_message` | Send email |
| `create_draft` | Create draft |
| `list_labels` | List labels |
| `list_threads` | List threads |
| `trash_message` | Trash email |
| `get_attachments` | Get attachments |

## Configuration Example

```toml
[[mcp.servers]]
name = "gmail"
type = "stdio"
command = "npx"
args = ["-y", "@node2flow/gmail-mcp"]
timeout_seconds = 60
env = { GOOGLE_CLIENT_ID = "your-value", GOOGLE_CLIENT_SECRET = "your-value", GOOGLE_REFRESH_TOKEN = "your-value" }
tools = []
```

**Notes:** 28 tools. Supports Gmail search syntax.

## Links

- [Homepage](https://www.npmjs.com/package/@node2flow/gmail-mcp)
