# mubert/mubert

Mubert Render API MCP server. Generates royalty-safe music loops and ambient tracks for ad soundtracks. Cleared for commercial use, unlike Suno/Udio.

## MCP Server

- **Package**: `mubert-mcp` (community wrapper around the Mubert Render API)
- **Transport**: stdio
- **Command**: `npx -y mubert-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `MUBERT_PAT` | Yes | Personal access token from mubert.com developer portal |

## Available Tools

| Tool | Description |
|------|-------------|
| `mubert_generate_track` | Render a track from a prompt (mood/genre tags + duration) |
| `mubert_generate_loop` | Generate a seamless loop (15s / 30s / 60s) |
| `mubert_get_job` | Poll job status |

## Configuration Example

```toml
[[mcp.servers]]
name = "mubert"
type = "stdio"
command = "npx"
args = ["-y", "mubert-mcp"]
timeout_seconds = 90
env = { MUBERT_PAT = "{{INPUT:MUBERT_PAT}}" }
tools = []
```

**Notes:** Tracks are licensed for commercial use under the Mubert subscription. For higher-fidelity bespoke tracks consider ElevenLabs Music (uses the same `ELEVENLABS_API_KEY`).

## Links

- [Mubert Render API](https://docs.mubert.com/)
