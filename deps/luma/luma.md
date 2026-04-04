# luma/luma

Luma AI video and image generation MCP server. Text-to-video, image-to-video, upscaling, and audio addition.

## MCP Server

- **Package**: `mcp-video-gen (GitHub only — not on npm)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm run build`

## Authentication

API key(s)

| Variable | Required | Description |
|----------|----------|-------------|
| `LUMAAI_API_KEY` | Yes | Luma AI API key |
| `RUNWAYML_API_SECRET` | No | Runway API key (optional) |
| `OPENROUTER_API_KEY` | No | OpenRouter API key (optional) |

## Available Tools

| Tool | Description |
|------|-------------|
| `luma_generate_image` | Generate image |
| `generate_text_to_video` | Text to video |
| `generate_image_to_video` | Image to video |
| `luma_upscale` | Upscale resolution |
| `luma_add_audio` | Add audio |
| `luma_get_camera_motions` | Camera motion options |

## Configuration Example

```toml
[[mcp.servers]]
name = "luma"
type = "stdio"
command = "npx"
args = ["-y", "mcp-video-gen (GitHub only — not on npm)"]
timeout_seconds = 60
env = { LUMAAI_API_KEY = "your-value", RUNWAYML_API_SECRET = "your-value", OPENROUTER_API_KEY = "your-value" }
tools = []
```

**Notes:** Not on npm. Supports multiple API providers.

## Links

- [Homepage](https://mcpservers.org/servers/wheattoast11/mcp-video-gen)
