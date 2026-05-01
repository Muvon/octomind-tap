# google/veo

Google Veo 3 video generation MCP server. Text-to-video and image-to-video with native dialogue and SFX via the Gemini API or Vertex AI.

## MCP Server

- **Package**: `mcp-google-veo` (community wrapper around the Gemini Video API)
- **Transport**: stdio
- **Command**: `npx -y mcp-google-veo`

## Authentication

API key (Gemini Developer API) **or** Application Default Credentials (Vertex AI).

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes (Gemini path) | Gemini API key from aistudio.google.com |
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes (Vertex path) | Path to a Google Cloud service-account JSON with Vertex AI access |
| `GOOGLE_CLOUD_PROJECT` | Yes (Vertex path) | GCP project ID for Vertex |
| `GOOGLE_CLOUD_REGION` | No | Vertex region (default `us-central1`) |

## Available Tools

| Tool | Description |
|------|-------------|
| `veo_generate_video` | Text-to-video, native audio (8s default) |
| `veo_image_to_video` | Animate an input image with a prompt |
| `veo_extend_video` | Extend an existing clip by another segment |
| `veo_get_operation` | Poll a long-running generation job |

## Configuration Example

```toml
[[mcp.servers]]
name = "veo"
type = "stdio"
command = "npx"
args = ["-y", "mcp-google-veo"]
timeout_seconds = 120
env = { GOOGLE_API_KEY = "{{INPUT:GOOGLE_API_KEY}}" }
tools = []
```

**Notes:** Veo 3 produces video with synchronized speech and ambient audio. Output is paid-tier only — confirm pricing in Vertex / Gemini before running production batches. Long generations are async; poll `veo_get_operation` until done.

## Links

- [Gemini Video API](https://ai.google.dev/gemini-api/docs/video)
- [Vertex AI Veo](https://cloud.google.com/vertex-ai/generative-ai/docs/video/generate-videos)
