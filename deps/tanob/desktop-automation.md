# tanob/desktop-automation

Desktop automation MCP server. Control mouse, keyboard, and take screenshots for UI automation on the local computer (macOS / Linux / Windows). Powered by RobotJS.

## MCP Server

- **Package**: `mcp-desktop-automation`
- **Transport**: stdio
- **Command**: `npx -y mcp-desktop-automation`

## Authentication

None — but the host OS must grant accessibility / screen-recording permissions to the process running the MCP server (Terminal, IDE, etc.). On macOS this is `System Settings → Privacy & Security → Accessibility / Screen Recording`.

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_screen_size` | Return the primary screen resolution |
| `screen_capture` | Capture the screen (≤ 800×600 reliable; larger may exceed the 1 MB MCP response cap) |
| `mouse_move` | Move the cursor to (x, y) |
| `mouse_click` | Click at the current position |
| `keyboard_type` | Type a string |
| `keyboard_press` | Press a named key (or combo) |

## Configuration Example

```toml
[[mcp.servers]]
name = "desktop-automation"
type = "stdio"
command = "npx"
args = ["-y", "mcp-desktop-automation"]
timeout_seconds = 60
tools = []
```

**Notes:**
- Requires system accessibility / screen-recording permissions on macOS.
- Screen captures above ~800×600 may exceed the 1 MB response limit and fail — prefer capturing a region or a sub-screen.
- Cross-platform via RobotJS (macOS / Linux / Windows).

## Links

- [GitHub](https://github.com/tanob/mcp-desktop-automation)
- [npm](https://www.npmjs.com/package/mcp-desktop-automation)
