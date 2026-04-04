# iflow-mcp/telegram

Telegram bot messaging MCP server. Send messages, manage channels and groups via Telegram Bot API.

## MCP Server

- **Package**: `@iflow-mcp/telegram-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/telegram-mcp-server`

## Authentication

Telegram Bot Token

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Bot token from @BotFather |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Telegram messaging, channel/group management |

## Configuration Example

```toml
[[mcp.servers]]
name = "telegram"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/telegram-mcp-server"]
timeout_seconds = 60
env = { TELEGRAM_BOT_TOKEN = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/telegram-mcp-server)
