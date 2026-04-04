# microsoft/teams

Microsoft Teams MCP server. Send messages, manage chats, search conversations, and interact with Teams channels.

## MCP Server

- **Package**: `teams-mcp`
- **Transport**: stdio
- **Command**: `npx -y teams-mcp@latest`

## Authentication

OAuth 2.0 with Microsoft Graph (authenticate via: npm run auth)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `send_channel_message` | Send channel message |
| `send_chat_message` | Send chat message |
| `list_teams` | List teams |
| `list_channels` | List channels |
| `search_messages` | Search messages (KQL) |
| `get_my_mentions` | Get mentions |
| `create_chat` | Create chat |

## Configuration Example

```toml
[[mcp.servers]]
name = "teams"
type = "stdio"
command = "npx"
args = ["-y", "teams-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Rich message formatting (markdown/HTML). XSS prevention. Init auth: node dist/index.js authenticate.

## Links

- [Homepage](https://www.npmjs.com/package/teams-mcp)
