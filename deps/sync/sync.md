# sync/sync

Sync.so (Sync Labs) MCP server. State-of-the-art lipsync. Takes a source video + a target audio track and produces a perfectly lipsynced output. Drop-in postprocess after voiceover replacement, dubbing, or AI-avatar generation.

## MCP Server

- **Package**: `@sync.so/mcp-server` (community)
- **Transport**: stdio
- **Command**: `npx -y @sync.so/mcp-server`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `SYNC_API_KEY` | Yes | API key from sync.so dashboard |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_create-generation` | Create a lipsync generation |
| `generate_get-generation / generations_get-by-id` | Poll generation status |
| `generate_estimate-cost` | Estimate generation cost |
| `assets_* (create, get, update, delete, create-upload-url)` | Manage media assets |
| `batch_* / projects_*` | Batch jobs and project organization |
| `tts_create / voices_*` | TTS and voice management |

## Configuration Example

```toml
[[mcp.servers]]
name = "sync"
type = "stdio"
command = "npx"
args = ["-y", "@sync.so/mcp-server"]
timeout_seconds = 120
env = { SYNC_API_KEY = "{{INPUT:SYNC_API_KEY}}" }
tools = []
```

**Notes:** Pricing is per-second of output (~$0.10/s). Use only on the final selected cut, not on every variant.

## Links

- [Sync.so docs](https://docs.sync.so/)
