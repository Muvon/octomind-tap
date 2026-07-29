# google/youtube-data

YouTube Data API v3 MCP server. Uploads Shorts and long-form video, edits metadata, manages playlists, fetches analytics.

## MCP Server

- **Package**: `youtube-studio-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y youtube-studio-mcp`

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
| `get_video_details / get_all_videos / search_my_videos` | Own-channel video metadata |
| `update_video_seo` | Update title/description/tags |
| `get_channel_overview / get_analytics_over_time / get_top_videos_analytics` | Analytics |
| `get_audience_demographics / get_traffic_sources` | Audience insight |
| `analyze_and_suggest_topics` | Topic suggestions |

## Configuration Example

```toml
[[mcp.servers]]
name = "youtube-data"
type = "stdio"
command = "npx"
args = ["-y", "youtube-studio-mcp"]
timeout_seconds = 600
env = { GOOGLE_CLIENT_ID = "{{INPUT:GOOGLE_CLIENT_ID}}", GOOGLE_CLIENT_SECRET = "{{INPUT:GOOGLE_CLIENT_SECRET}}", GOOGLE_REFRESH_TOKEN = "{{INPUT:GOOGLE_REFRESH_TOKEN}}" }
tools = []
```

**Notes:** Free quota is 10,000 units/day; an upload costs ~1,600 units, so practical limit is ~6 uploads/day per project. For Shorts: vertical (9:16) + ≤60s + `#shorts` in title or description.

## Links

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
