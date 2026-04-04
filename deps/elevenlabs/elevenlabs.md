# elevenlabs/elevenlabs

ElevenLabs text-to-speech MCP server. Generate speech, clone voices, transcribe audio, design voices, and create soundscapes.

## MCP Server

- **Package**: `elevenlabs-mcp (Python — use uvx)`
- **Transport**: stdio
- **Command**: `uvx elevenlabs-mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `ELEVENLABS_API_KEY` | Yes | API key from elevenlabs.io/app/settings/api-keys |
| `ELEVENLABS_MCP_BASE_PATH` | No | Default file location (~/Desktop) |

## Available Tools

| Tool | Description |
|------|-------------|
| `text_to_speech` | Generate speech from text |
| `voice_clone` | Clone a voice |
| `transcribe_audio` | Transcribe audio |
| `voice_design` | Design new voice |
| `audio_isolation` | Isolate audio |
| `soundscape` | Create soundscape |

## Configuration Example

```toml
[[mcp.servers]]
name = "elevenlabs"
type = "stdio"
command = "npx"
args = ["-y", "elevenlabs-mcp (Python — use uvx)"]
timeout_seconds = 60
env = { ELEVENLABS_API_KEY = "your-value", ELEVENLABS_MCP_BASE_PATH = "your-value" }
tools = []
```

**Notes:** Python-based — use uvx, not npx. Free tier: 10,000 monthly credits.

## Links

- [Homepage](https://github.com/elevenlabs/elevenlabs-mcp)
