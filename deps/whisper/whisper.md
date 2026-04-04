# whisper/whisper

Whisper audio transcription MCP server. Transcribe audio, convert formats, and generate speech using OpenAI's Whisper.

## MCP Server

- **Package**: `mcp-server-whisper (Python — use uvx)`
- **Transport**: stdio
- **Command**: `uvx mcp-server-whisper`

## Authentication

OpenAI API key

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `AUDIO_FILES_PATH` | Yes | Directory for audio files |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_audio_files` | List audio files |
| `transcribe_audio` | Transcribe audio |
| `convert_audio` | Convert format |
| `compress_audio` | Compress audio |
| `create_audio` | Text-to-speech |
| `chat_with_audio` | Chat about audio |

## Configuration Example

```toml
[[mcp.servers]]
name = "whisper"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-whisper (Python — use uvx)"]
timeout_seconds = 60
env = { OPENAI_API_KEY = "your-value", AUDIO_FILES_PATH = "your-value" }
tools = []
```

**Notes:** Python-based — use uvx. 11 tools total.

## Links

- [Homepage](https://www.npmjs.com/package/whisper-mcp)
