# hedra/hedra

Hedra Character-3 MCP server. Image + audio → expressive talking-character video. Best in class for stylized character avatars (illustrated, anime, mascots) speaking a script.

## MCP Server

- **Package**: `mcp-server-hedra` (community)
- **Transport**: stdio
- **Command**: `npx -y mcp-server-hedra`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `HEDRA_API_KEY` | Yes | API key from hedra.com → API Keys |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_video` | Image/asset + audio → talking-character video |
| `generate_video_with_tts` | Image + text (auto-TTS) → character video |
| `generate_text_to_speech` | Text → speech audio asset |
| `generate_image` | Text → image asset |
| `create_asset / upload_asset / list_assets` | Manage input assets |
| `list_generations / get_generation_status` | Track generation jobs |
| `list_models / get_credits` | Models catalog and account credits |

## Configuration Example

```toml
[[mcp.servers]]
name = "hedra"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-hedra"]
timeout_seconds = 120
env = { HEDRA_API_KEY = "{{INPUT:HEDRA_API_KEY}}" }
tools = []
```

**Notes:** Character-3 handles expressive head/shoulder motion + lipsync from a single still. Use as an alternative to HeyGen when you need illustrated or non-photoreal characters.

## Links

- [Hedra docs](https://www.hedra.com/docs)
