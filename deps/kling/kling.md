# kling/kling

Kling AI 2.x video generation MCP server. Strong motion physics, cheap 1080p/10s, motion-brush control. Good price/quality for performance video iteration.

## MCP Server

- **Package**: `kling-mcp-server` (community)
- **Transport**: stdio
- **Command**: `npx -y kling-mcp-server`

## Authentication

API key (issue + secret pair via the KlingAI Open Platform).

| Variable | Required | Description |
|----------|----------|-------------|
| `KLING_ACCESS_KEY` | Yes | Access key from app.klingai.com Open Platform |
| `KLING_SECRET_KEY` | Yes | Secret key paired with the access key |

## Available Tools

| Tool | Description |
|------|-------------|
| `kling_text_to_video` | Generate clip from text prompt (5s / 10s, 720p / 1080p) |
| `kling_image_to_video` | Animate input image with prompt + camera motion |
| `kling_motion_brush` | Mask-driven motion control |
| `kling_extend_video` | Extend an existing clip |
| `kling_lipsync` | Add lipsync to a clip with text or audio |
| `kling_get_task` | Poll generation status |

## Configuration Example

```toml
[[mcp.servers]]
name = "kling"
type = "stdio"
command = "npx"
args = ["-y", "kling-mcp-server"]
timeout_seconds = 120
env = { KLING_ACCESS_KEY = "{{INPUT:KLING_ACCESS_KEY}}", KLING_SECRET_KEY = "{{INPUT:KLING_SECRET_KEY}}" }
tools = []
```

**Notes:** Credit-based pricing; cheaper per second than Runway/Veo for 1080p output. Lipsync endpoint useful for UGC-style ads.

## Links

- [KlingAI API docs](https://app.klingai.com/global/dev/document-api/)
