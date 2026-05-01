# heygen/heygen

HeyGen MCP server. Generate AI-avatar talking-head videos for ads, UGC, and translation. Best-in-class for performance-ad UGC.

## MCP Server

- **Package**: `@heygen/mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @heygen/mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `HEYGEN_API_KEY` | Yes | HeyGen API key from app.heygen.com → Space Settings → API |

## Available Tools

| Tool | Description |
|------|-------------|
| `heygen_create_video` | Generate avatar video from script + avatar/voice IDs |
| `heygen_list_avatars` | List available stock and personal avatars |
| `heygen_list_voices` | List available voices |
| `heygen_translate_video` | Translate + lipsync a source video to a target language |
| `heygen_get_video_status` | Poll generation status |
| `heygen_create_avatar_iv` | Avatar IV (instant avatar from a single photo) |

## Configuration Example

```toml
[[mcp.servers]]
name = "heygen"
type = "stdio"
command = "npx"
args = ["-y", "@heygen/mcp-server"]
timeout_seconds = 120
env = { HEYGEN_API_KEY = "{{INPUT:HEYGEN_API_KEY}}" }
tools = []
```

**Notes:** Paid plans start at $29/mo (Creator). Avatar IV produces a brand-new avatar from a single photo — ideal for personalized UGC ads. Generation is async; poll status.

## Links

- [HeyGen API docs](https://docs.heygen.com/)
- [API key dashboard](https://app.heygen.com/settings)
