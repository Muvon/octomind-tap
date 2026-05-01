# assemblyai/assemblyai

AssemblyAI MCP server. Speech-to-text with speaker diarization, auto-chapters, sentiment, and caption-ready SRT/VTT output. Best-in-class metadata for caption-driven social videos.

## MCP Server

- **Package**: `@assemblyai/mcp-server` (official)
- **Transport**: stdio
- **Command**: `npx -y @assemblyai/mcp-server`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `ASSEMBLYAI_API_KEY` | Yes | API key from assemblyai.com dashboard |

## Available Tools

| Tool | Description |
|------|-------------|
| `assemblyai_transcribe` | Transcribe audio/video URL → words + speakers + chapters |
| `assemblyai_get_subtitles` | Fetch SRT/VTT for a transcript |
| `assemblyai_summarize` | LeMUR summary of a transcript |
| `assemblyai_get_transcript` | Poll transcription status / fetch result |

## Configuration Example

```toml
[[mcp.servers]]
name = "assemblyai"
type = "stdio"
command = "npx"
args = ["-y", "@assemblyai/mcp-server"]
timeout_seconds = 120
env = { ASSEMBLYAI_API_KEY = "{{INPUT:ASSEMBLYAI_API_KEY}}" }
tools = []
```

**Notes:** Use AssemblyAI for the final captioned upload (chapters, speaker labels). Whisper is fine for quick drafts. Free tier 100 hr/mo.

## Links

- [AssemblyAI docs](https://www.assemblyai.com/docs)
