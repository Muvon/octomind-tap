# minimax/hailuo

MiniMax's official MCP server, wired for its video tools: text-to-video and image-to-video with MiniMax Hailuo models, a low-cost option when many variants are generated and the best are kept.

## MCP Server

- **Package**: `minimax-mcp` (official, MiniMax-AI/MiniMax-MCP)
- **Transport**: stdio
- **Command**: `uvx minimax-mcp==0.0.20`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `MINIMAX_API_KEY` | Yes | API key from the MiniMax platform dashboard |
| `MINIMAX_API_HOST` | Yes | `https://api.minimax.io` (global) or `https://api.minimaxi.com` (mainland China); must match the key's region |
| `MINIMAX_MCP_BASE_PATH` | No | Directory where generated files are saved |

## Available Tools

The server also ships audio and image tools; the `video-gen` capability exposes only the two video tools.

| Tool | Description |
|------|-------------|
| `generate_video` | Text-to-video, or image-to-video from a first frame |
| `query_video_generation` | Poll a generation task and download the result |

## Configuration Example

```toml
[[mcp.servers]]
name = "hailuo"
type = "stdio"
command = "uvx"
args = ["minimax-mcp==0.0.20"]
timeout_seconds = 120
env = { MINIMAX_API_KEY = "{{INPUT:MINIMAX_API_KEY}}", MINIMAX_API_HOST = "https://api.minimax.io" }
tools = []
```

**Notes:** Cheap per clip, so it suits a first wave of variants; re-render the chosen one on a higher-quality provider for the final upload.

## Links

- [MiniMax MCP on GitHub](https://github.com/MiniMax-AI/MiniMax-MCP)
- [MiniMax video generation API](https://platform.minimax.io/docs/api-reference/video-generation-t2v)
