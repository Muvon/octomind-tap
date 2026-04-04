# calendly/calendly

Calendly scheduling MCP server. Manage events, invitees, event types, and availability with OAuth or PAT auth.

## MCP Server

- **Package**: `calendly-mcp-server`
- **Transport**: stdio
- **Command**: `npx calendly-mcp-server`

## Authentication

Personal Access Token or OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `CALENDLY_API_KEY` | Yes | Personal Access Token |
| `CALENDLY_CLIENT_ID` | No | OAuth client ID |
| `CALENDLY_CLIENT_SECRET` | No | OAuth client secret |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_current_user` | Current user info |
| `list_events` | List events |
| `get_event` | Get event details |
| `list_event_invitees` | List invitees |
| `cancel_event` | Cancel event |
| `list_event_types` | List event types |
| `schedule_event` | Schedule event (paid plan) |

## Configuration Example

```toml
[[mcp.servers]]
name = "calendly"
type = "stdio"
command = "npx"
args = ["-y", "calendly-mcp-server"]
timeout_seconds = 60
env = { CALENDLY_API_KEY = "your-value", CALENDLY_CLIENT_ID = "your-value", CALENDLY_CLIENT_SECRET = "your-value" }
tools = []
```

**Notes:** schedule_event requires paid Calendly plan. 12 tools total.

## Links

- [Homepage](https://github.com/meAmitPatil/calendly-mcp-server)
