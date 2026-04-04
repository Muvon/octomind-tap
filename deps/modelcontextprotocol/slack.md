# modelcontextprotocol/slack

Official MCP Slack server. List channels, post messages, reply to threads, add reactions, and query user profiles.

## MCP Server

- **Package**: `@modelcontextprotocol/server-slack`
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-slack`

## Authentication

Slack Bot Token

| Variable | Required | Description |
|----------|----------|-------------|
| `SLACK_BOT_TOKEN` | Yes | Bot token (xoxb-...) |
| `SLACK_TEAM_ID` | Yes | Workspace ID (T...) |
| `SLACK_CHANNEL_IDS` | No | Comma-separated channel IDs to limit access |

## Available Tools

| Tool | Description |
|------|-------------|
| `slack_list_channels` | List channels |
| `slack_post_message` | Post message |
| `slack_reply_to_thread` | Reply to thread |
| `slack_add_reaction` | Add reaction |
| `slack_get_channel_history` | Channel history |
| `slack_get_thread_replies` | Thread replies |
| `slack_get_users` | List users |
| `slack_get_user_profile` | User profile |

## Configuration Example

```toml
[[mcp.servers]]
name = "slack"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-slack"]
timeout_seconds = 60
env = { SLACK_BOT_TOKEN = "your-value", SLACK_TEAM_ID = "your-value", SLACK_CHANNEL_IDS = "your-value" }
tools = []
```

**Notes:** DEPRECATED but still functional. Requires OAuth scopes for each operation.

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/slack)
