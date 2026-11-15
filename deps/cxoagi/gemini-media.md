# cxoagi/gemini-media

Community MCP server for Google's Gemini media models. The `video-gen` capability uses its Gemini Omni Flash tools: text-to-video and image-to-video clips of 3-15 s with native audio, plus extension and edits, paid through a Gemini API key.

## MCP Server

- Package: `gemini-media-mcp` (PyPI, community-maintained, CxOAGI/gemini-media-mcp)
- Transport: `stdio`
- Command: `uvx gemini-media-mcp==0.1.14`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Gemini API key from Google AI Studio; `GOOGLE_API_KEY` is also read |

## Available Tools

The package also ships image and Veo tools; Veo and Omni upscaling need Vertex AI credentials, so the capability exposes only the four tools below.

| Tool | Description |
|------|-------------|
| `generate_video_omni` | Generate or edit a video with Gemini Omni 1.2 Flash (3-15 s, 16:9 or 9:16, native audio) |
| `extend_video_omni` | Append a continuation to an Omni video |
| `edit_video` | Refine a generated Omni video over several turns |
| `get_omni_interaction` | Check a render by interaction id and save it when finished |

## Configuration Example

```toml
[[mcp.servers]]
name = "gemini-media"
type = "stdio"
command = "uvx"
args = ["gemini-media-mcp==0.1.14"]
timeout_seconds = 600
env = { GEMINI_API_KEY = "{{INPUT:GEMINI_API_KEY}}" }
tools = []
```

## Links

- [Homepage](https://github.com/CxOAGI/gemini-media-mcp)
- [Gemini Omni Flash model page](https://aistudio.google.com/docs/models/gemini-omni-flash)
