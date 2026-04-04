# spotify/spotify

Spotify music MCP server. Control playback, manage playlists, search music, and view library.

## MCP Server

- **Package**: `spotify-mcp (Python — use uvx)`
- **Transport**: stdio
- **Command**: `uvx spotify-mcp`

## Authentication

OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `SPOTIFY_CLIENT_ID` | Yes | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Yes | Spotify app client secret |
| `SPOTIFY_REDIRECT_URI` | Yes | OAuth redirect URI |

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Search music |
| `now_playing` | Current track |
| `manage_playlists` | Playlist operations |
| `manage_queue` | Queue management |
| `playback_control` | Play/pause/skip |

## Configuration Example

```toml
[[mcp.servers]]
name = "spotify"
type = "stdio"
command = "npx"
args = ["-y", "spotify-mcp (Python — use uvx)"]
timeout_seconds = 60
env = { SPOTIFY_CLIENT_ID = "your-value", SPOTIFY_CLIENT_SECRET = "your-value", SPOTIFY_REDIRECT_URI = "your-value" }
tools = []
```

**Notes:** Python-based — use uvx. Spotify Premium required. Most popular: github.com/varunneal/spotify-mcp (592 stars).

## Links

- [Homepage](https://www.npmjs.com/package/@darrenjaws/spotify-mcp)
