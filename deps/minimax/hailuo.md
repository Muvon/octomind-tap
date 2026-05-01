# minimax/hailuo

MiniMax Hailuo 02 video MCP server. The cheapest viable text-to-video and image-to-video model — ideal for high-volume creative testing where you generate dozens of variants and pick the winners.

## MCP Server

- **Package**: `minimax-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y minimax-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `MINIMAX_API_KEY` | Yes | API key from minimax.io platform dashboard |
| `MINIMAX_GROUP_ID` | No | Group/workspace ID, required by some endpoints |

## Available Tools

| Tool | Description |
|------|-------------|
| `hailuo_text_to_video` | T2V (6s default, 720p/1080p) |
| `hailuo_image_to_video` | I2V from a still + prompt |
| `hailuo_get_task` | Poll generation status |
| `minimax_tts` | MiniMax TTS as a fallback voice option |

## Configuration Example

```toml
[[mcp.servers]]
name = "hailuo"
type = "stdio"
command = "npx"
args = ["-y", "minimax-mcp"]
timeout_seconds = 120
env = { MINIMAX_API_KEY = "{{INPUT:MINIMAX_API_KEY}}" }
tools = []
```

**Notes:** Best price/quality ratio for short-form social. Use Hailuo for the first wave of variants, then re-render the chosen winner on Veo / Runway for the final upload.

## Links

- [MiniMax Platform docs](https://www.minimax.io/platform/document/)
