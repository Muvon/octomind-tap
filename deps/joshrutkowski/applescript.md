# joshrutkowski/applescript

AppleScript MCP server with 100+ tools for macOS system control — calendar, clipboard, Finder, system, and iTerm.

## MCP Server

- **Package**: `applescript-mcp (GitHub only — build locally)`
- **Transport**: stdio
- **Command**: `node path/to/server/index.js`

## Authentication

None (requires macOS system permissions)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `calendar_create` | Create calendar event |
| `clipboard_read` | Read clipboard |
| `finder_reveal` | Reveal in Finder |
| `system_info` | System information |
| `iterm_execute` | iTerm command execution |

## Configuration Example

```toml
[[mcp.servers]]
name = "applescript"
type = "stdio"
command = "npx"
args = ["-y", "applescript-mcp (GitHub only — build locally)"]
timeout_seconds = 60
tools = []
```

**Notes:** macOS 10.15+ only. Requires Full System Permissions. 100+ tools.

## Links

- [Homepage](https://github.com/joshrutkowski/applescript-mcp)
