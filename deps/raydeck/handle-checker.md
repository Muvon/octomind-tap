# raydeck/handle-checker

Social media handle checker MCP server. Verify username availability across YouTube, TikTok, Instagram, Threads, and X.

## MCP Server

- **Package**: `@raydeck/social-media-handle-checker-mcp`
- **Transport**: stdio
- **Command**: `npx -y @raydeck/social-media-handle-checker-mcp`

## Authentication

None (public APIs)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `check_all_platforms` | Batch check all platforms |
| `check_youtube_handle` | YouTube |
| `check_tiktok_handle` | TikTok |
| `check_instagram_handle` | Instagram |
| `check_threads_handle` | Threads |
| `check_x_handle` | X/Twitter |

## Configuration Example

```toml
[[mcp.servers]]
name = "handle-checker"
type = "stdio"
command = "npx"
args = ["-y", "@raydeck/social-media-handle-checker-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Returns follower counts, verification status, profile info.

## Links

- [Homepage](https://www.npmjs.com/package/@raydeck/social-media-handle-checker-mcp)
