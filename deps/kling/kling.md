# kling/kling

Kling AI 2.x video generation MCP server. Strong motion physics, cheap 1080p/10s, motion-brush control. Good price/quality for performance video iteration.

## MCP Server

- **Package**: `mcp-kling` (community)
- **Transport**: stdio
- **Command**: `npx -y mcp-kling`

## Authentication

API key (issue + secret pair via the KlingAI Open Platform).

| Variable | Required | Description |
|----------|----------|-------------|
| `KLING_ACCESS_KEY` | Yes | Access key from app.klingai.com Open Platform |
| `KLING_SECRET_KEY` | Yes | Secret key paired with the access key |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_video` | Text → video |
| `generate_image_to_video` | Image → video |
| `check_video_status / list_tasks` | Track generation tasks |
| `extend_video` | Extend an existing generation |
| `create_lipsync` | Lipsync a generated video |
| `apply_video_effect` | Apply effects to a video |
| `get_account_balance / get_resource_packages` | Account status |

## Configuration Example

```toml
[[mcp.servers]]
name = "kling"
type = "stdio"
command = "npx"
args = ["-y", "mcp-kling"]
timeout_seconds = 120
env = { KLING_ACCESS_KEY = "{{INPUT:KLING_ACCESS_KEY}}", KLING_SECRET_KEY = "{{INPUT:KLING_SECRET_KEY}}" }
tools = []
```

**Notes:** Credit-based pricing; cheaper per second than Runway/Veo for 1080p output. Lipsync endpoint useful for UGC-style ads.

## Links

- [KlingAI API docs](https://app.klingai.com/global/dev/document-api/)
