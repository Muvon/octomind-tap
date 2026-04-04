# youtube/youtube

YouTube MCP server. Download and work with video subtitles, transcripts, and channel information.

## MCP Server

- **Package**: `@anaisbetts/mcp-youtube`
- **Transport**: stdio
- **Command**: `npx -y @anaisbetts/mcp-youtube`

## Authentication

None (uses yt-dlp)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | YouTube subtitle/transcript tools via yt-dlp |

## Configuration Example

```toml
[[mcp.servers]]
name = "youtube"
type = "stdio"
command = "npx"
args = ["-y", "@anaisbetts/mcp-youtube"]
timeout_seconds = 60
tools = []
```

**Notes:** Requires yt-dlp pre-installed locally (brew install yt-dlp).

## Links

- [Homepage](https://www.npmjs.com/package/@anaisbetts/mcp-youtube)
