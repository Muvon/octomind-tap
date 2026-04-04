# tanob/desktop-automation

Desktop automation MCP server. Control mouse, keyboard, and take screenshots for UI automation.

## MCP Server

- **Package**: `desktop-automation-mcp`
- **Transport**: stdio
- **Command**: `npx -y desktop-automation-mcp`

## Authentication

None (system permissions required)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `mouse_click` | Click |
| `mouse_move` | Move mouse |
| `keyboard_type` | Type text |
| `keyboard_press` | Press key |
| `take_screenshot` | Screenshot |

## Configuration Example

```toml
[[mcp.servers]]
name = "desktop-automation"
type = "stdio"
command = "npx"
args = ["-y", "desktop-automation-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Requires system accessibility permissions.

## Links

- [Homepage](https://mcp.so/server/desktop-automation/tanob)
