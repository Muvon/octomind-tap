# google/youtube-data

YouTube Studio MCP server on the YouTube Data and Analytics APIs: edits metadata of videos already on the channel (titles, descriptions, tags) and reads channel analytics. It has no upload tool; uploads go through the `publish-youtube` capability's default Upload-Post provider.

## MCP Server

- **Package**: `youtube-studio-mcp` (community, pinned in the capability file)
- **Transport**: stdio
- **Command**: `npx -y youtube-studio-mcp@2.1.0`

## Authentication

OAuth 2.0 with your own Google Cloud OAuth client (`youtube.force-ssl`, `youtube.readonly`, `yt-analytics.readonly`). The package reads `credentials.json` and `tokens.json`, created with its `node auth.js` script, from its own install directory; it reads no environment variables. OAuth clients left in "Testing" status get refresh tokens that expire after 7 days.

| File | Required | Description |
|------|----------|-------------|
| `credentials.json` | Yes | Desktop OAuth client from Google Cloud Console |
| `tokens.json` | Yes | Token file written by the package's auth script |

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
args = ["-y", "youtube-studio-mcp@2.1.0"]
timeout_seconds = 600
tools = []
```

**Notes:** Default quota is 10,000 units/day per project; `videos.update` costs 50 units. Since 2026-06-01 `videos.insert` has its own bucket of 100 calls/day (YouTube API quota page).

## Links

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [Quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
