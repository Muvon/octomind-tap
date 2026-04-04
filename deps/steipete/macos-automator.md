# steipete/macos-automator

macOS Automator MCP server. Execute AppleScript/JXA scripts, get 200+ scripting recipes, and query UI accessibility elements.

## MCP Server

- **Package**: `@steipete/macos-automator-mcp`
- **Transport**: stdio
- **Command**: `npx -y @steipete/macos-automator-mcp@latest`

## Authentication

None (requires macOS Automation + Accessibility permissions)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `execute_script` | Run AppleScript/JXA |
| `get_scripting_tips` | 200+ automation recipes |
| `accessibility_query` | UI element control |

## Configuration Example

```toml
[[mcp.servers]]
name = "macos-automator"
type = "stdio"
command = "npx"
args = ["-y", "@steipete/macos-automator-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** macOS only.

## Links

- [Homepage](https://www.npmjs.com/package/@steipete/macos-automator-mcp)
