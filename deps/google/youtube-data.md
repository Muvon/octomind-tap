# google/youtube-data

YouTube Data API v3 MCP server. Uploads Shorts and long-form video, edits metadata, manages playlists, fetches analytics.

## MCP Server

- **Package**: `youtube-data-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y youtube-data-mcp`

## Authentication

OAuth 2.0 with `youtube.upload`, `youtube.readonly`, and (optional) `yt-analytics.readonly` scopes.

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_CLIENT_ID` | Yes | OAuth client ID from Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | Yes | OAuth client secret |
| `GOOGLE_REFRESH_TOKEN` | Yes | Long-lived refresh token for the channel owner |

## Available Tools

| Tool | Description |
|------|-------------|
| `youtube_upload_video` | Upload a video file (set title, description, tags, category, privacy) |
| `youtube_set_thumbnail` | Set custom thumbnail |
| `youtube_update_metadata` | Edit title / description / tags after upload |
| `youtube_list_videos` | List your channel's videos |
| `youtube_get_analytics` | Channel analytics (paid tier only for some metrics) |

## Configuration Example

```toml
[[mcp.servers]]
name = "youtube-data"
type = "stdio"
command = "npx"
args = ["-y", "youtube-data-mcp"]
timeout_seconds = 600
env = { GOOGLE_CLIENT_ID = "{{INPUT:GOOGLE_CLIENT_ID}}", GOOGLE_CLIENT_SECRET = "{{INPUT:GOOGLE_CLIENT_SECRET}}", GOOGLE_REFRESH_TOKEN = "{{INPUT:GOOGLE_REFRESH_TOKEN}}" }
tools = []
```

**Notes:** Free quota is 10,000 units/day; an upload costs ~1,600 units, so practical limit is ~6 uploads/day per project. For Shorts: vertical (9:16) + ≤60s + `#shorts` in title or description.

## Links

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
