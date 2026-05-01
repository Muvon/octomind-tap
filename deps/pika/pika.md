# pika/pika

Pika 2.x video generation MCP server. Fast iteration with stylized presets and Pikaffects (object-level transformations). Strong for stylized social ads.

## MCP Server

- **Package**: `pika-mcp-server` (community wrapper around the Pika API)
- **Transport**: stdio
- **Command**: `npx -y pika-mcp-server`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `PIKA_API_KEY` | Yes | Pika API key (request access at pika.art) |

## Available Tools

| Tool | Description |
|------|-------------|
| `pika_text_to_video` | T2V (Pika 2.x base model) |
| `pika_image_to_video` | I2V from input still + prompt |
| `pika_effect` | Apply a Pikaffect (cake-ify, melt, inflate, etc.) |
| `pika_scene_extend` | Extend an existing clip |
| `pika_get_job` | Poll job status |

## Configuration Example

```toml
[[mcp.servers]]
name = "pika"
type = "stdio"
command = "npx"
args = ["-y", "pika-mcp-server"]
timeout_seconds = 120
env = { PIKA_API_KEY = "{{INPUT:PIKA_API_KEY}}" }
tools = []
```

**Notes:** Pikaffects make for great pattern-interrupt opens in short-form ads. Cheaper per render than Runway/Veo when stylized output is acceptable.

## Links

- [Pika docs](https://pika.art/docs)
