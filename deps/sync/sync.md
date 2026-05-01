# sync/sync

Sync.so (Sync Labs) MCP server. State-of-the-art lipsync. Takes a source video + a target audio track and produces a perfectly lipsynced output. Drop-in postprocess after voiceover replacement, dubbing, or AI-avatar generation.

## MCP Server

- **Package**: `sync-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y sync-mcp`

## Authentication

| Variable | Required | Description |
|----------|----------|-------------|
| `SYNC_API_KEY` | Yes | API key from sync.so dashboard |

## Available Tools

| Tool | Description |
|------|-------------|
| `sync_lipsync` | Lipsync a video to a target audio track (sync-1.9 / sync-2 models) |
| `sync_translate_dub` | Lipsync + dub to a different language |
| `sync_get_job` | Poll job status |

## Configuration Example

```toml
[[mcp.servers]]
name = "sync"
type = "stdio"
command = "npx"
args = ["-y", "sync-mcp"]
timeout_seconds = 120
env = { SYNC_API_KEY = "{{INPUT:SYNC_API_KEY}}" }
tools = []
```

**Notes:** Pricing is per-second of output (~$0.10/s). Use only on the final selected cut, not on every variant.

## Links

- [Sync.so docs](https://docs.sync.so/)
