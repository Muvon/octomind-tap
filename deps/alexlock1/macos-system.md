# alexlock1/macos-system

macOS system integration MCP server. File dialogs, clipboard, notifications, screenshots, Finder, PDF, Notes, and image processing.

## MCP Server

- **Package**: `macos-mcp (GitHub only — not on npm)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm run build`

## Authentication

None (macOS system permissions required)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `pick_file` | File picker dialog |
| `clipboard_read` | Read clipboard |
| `clipboard_write` | Write clipboard |
| `notify` | System notification |
| `screenshot` | Take screenshot |
| `reveal_in_finder` | Show in Finder |
| `note_create` | Create Apple Note |
| `image_resize` | Resize image |
| `pdf_merge` | Merge PDFs |

## Configuration Example

```toml
[[mcp.servers]]
name = "macos-system"
type = "stdio"
command = "npx"
args = ["-y", "macos-mcp (GitHub only — not on npm)"]
timeout_seconds = 60
tools = []
```

**Notes:** macOS only. Not on npm — requires git clone. Uses AppleScript.

## Links

- [Homepage](https://github.com/alexlock1/macos-mcp)
