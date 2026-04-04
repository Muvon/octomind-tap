# discord/discord

Discord bot integration MCP server. Manage channels, messages, roles, members, webhooks, and forum operations.

## MCP Server

- **Package**: `mcp-discord`
- **Transport**: stdio
- **Command**: `npx mcp-discord --config ${DISCORD_TOKEN}`

## Authentication

Discord bot token

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | Yes | Bot token from Discord Developer Portal |

## Available Tools

| Tool | Description |
|------|-------------|
| `send_message` | Send message |
| `list_servers` | List servers |
| `create_channel` | Create channel |
| `manage_roles` | Manage roles |
| `create_webhook` | Create webhook |
| `search_messages` | Search messages |
| `manage_forum` | Forum operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "discord"
type = "stdio"
command = "npx"
args = ["-y", "mcp-discord"]
timeout_seconds = 60
env = { DISCORD_TOKEN = "your-value" }
tools = []
```

**Notes:** 40+ tools. Requires bot permissions: Send Messages, Manage Messages, Manage Channels, Manage Roles, View Channels. HTTP transport: --transport http --port 3000.

## Links

- [Homepage](https://www.npmjs.com/package/mcp-discord)
