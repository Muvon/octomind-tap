# google/drive

Google Drive MCP server. Search, read, and manage Google Drive files.

## MCP Server

- **Package**: `@dguido/google-drive-mcp`
- **Transport**: stdio
- **Command**: `npx -y @dguido/google-drive-mcp`

## Authentication

OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | OAuth 2.0 Client ID |
| `GOOGLE_CLIENT_SECRET` | Yes | OAuth 2.0 Client Secret |
| `GOOGLE_REFRESH_TOKEN` | Yes | Refresh token |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Drive file operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "drive"
type = "stdio"
command = "npx"
args = ["-y", "@dguido/google-drive-mcp"]
timeout_seconds = 60
env = { GOOGLE_CLIENT_ID = "your-value", GOOGLE_CLIENT_SECRET = "your-value", GOOGLE_REFRESH_TOKEN = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use.

## Links

- [Homepage](https://www.npmjs.com/package/@dguido/google-drive-mcp)
