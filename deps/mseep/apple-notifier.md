# mseep/apple-notifier

macOS native notification MCP server. Send notifications, show dialogs, speak text, take screenshots, and pick files.

## MCP Server

- **Package**: `@mseep/apple-notifier-mcp`
- **Transport**: stdio
- **Command**: `npx -y @mseep/apple-notifier-mcp`

## Authentication

None (macOS system access)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `send_notification` | macOS notification |
| `prompt_user` | Dialog prompt |
| `speak` | Text-to-speech |
| `take_screenshot` | Screenshot |
| `select_file` | File picker |

## Configuration Example

```toml
[[mcp.servers]]
name = "apple-notifier"
type = "stdio"
command = "npx"
args = ["-y", "@mseep/apple-notifier-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** macOS only. Node.js 18+.

## Links

- [Homepage](https://npmjs.com/package/@mseep/apple-notifier-mcp)
