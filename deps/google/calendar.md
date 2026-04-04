# google/calendar

Google Calendar MCP server. Create events, manage calendars, check availability, and set vacation auto-replies.

## MCP Server

- **Package**: `@cocal/google-calendar-mcp`
- **Transport**: stdio
- **Command**: `npx -y @cocal/google-calendar-mcp`

## Authentication

OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | OAuth 2.0 Client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | OAuth 2.0 Client Secret |
| `GOOGLE_REFRESH_TOKEN` | Yes | Refresh token from OAuth flow |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_calendars` | List calendars |
| `create_event` | Create event |
| `update_event` | Update event |
| `delete_event` | Delete event |
| `get_availability` | Check availability |

## Configuration Example

```toml
[[mcp.servers]]
name = "calendar"
type = "stdio"
command = "npx"
args = ["-y", "@cocal/google-calendar-mcp"]
timeout_seconds = 60
env = { GOOGLE_CLIENT_ID = "your-value", GOOGLE_CLIENT_SECRET = "your-value", GOOGLE_REFRESH_TOKEN = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@cocal/google-calendar-mcp)
