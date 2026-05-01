# openai/sora

OpenAI Sora 2 video generation MCP server. Long coherent shots, brand-safe defaults, remix and "cameo" workflows. Best when you need narrative coherence across a longer take.

## MCP Server

- **Package**: `openai-sora-mcp` (community wrapper around the OpenAI Video API)
- **Transport**: stdio
- **Command**: `npx -y openai-sora-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key with Sora access |

## Available Tools

| Tool | Description |
|------|-------------|
| `sora_generate_video` | Text-to-video |
| `sora_remix` | Remix an existing video with a new prompt |
| `sora_image_to_video` | Animate an image |
| `sora_get_job` | Poll job status |

## Configuration Example

```toml
[[mcp.servers]]
name = "sora"
type = "stdio"
command = "npx"
args = ["-y", "openai-sora-mcp"]
timeout_seconds = 180
env = { OPENAI_API_KEY = "{{INPUT:OPENAI_API_KEY}}" }
tools = []
```

**Notes:** Sora 2 has the strictest content moderation of the major providers — useful when shipping ads to enterprise / regulated platforms. Long generations are async; poll `sora_get_job`.

## Links

- [OpenAI Video API](https://platform.openai.com/docs/guides/video)
