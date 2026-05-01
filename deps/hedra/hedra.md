# hedra/hedra

Hedra Character-3 MCP server. Image + audio → expressive talking-character video. Best in class for stylized character avatars (illustrated, anime, mascots) speaking a script.

## MCP Server

- **Package**: `hedra-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y hedra-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `HEDRA_API_KEY` | Yes | API key from hedra.com → API Keys |

## Available Tools

| Tool | Description |
|------|-------------|
| `hedra_create_character_video` | Image + audio → animated character video |
| `hedra_text_to_character` | Image + text (auto-TTS) → character video |
| `hedra_get_generation` | Poll job status |
| `hedra_list_voices` | Available voices for text-to-character mode |

## Configuration Example

```toml
[[mcp.servers]]
name = "hedra"
type = "stdio"
command = "npx"
args = ["-y", "hedra-mcp"]
timeout_seconds = 120
env = { HEDRA_API_KEY = "{{INPUT:HEDRA_API_KEY}}" }
tools = []
```

**Notes:** Character-3 handles expressive head/shoulder motion + lipsync from a single still. Use as an alternative to HeyGen when you need illustrated or non-photoreal characters.

## Links

- [Hedra docs](https://www.hedra.com/docs)
