# tiktok-posting/tiktok-posting

TikTok Content Posting API MCP server. Direct Post and Photo Post for finished video creative. Distinct from `deps/tiktok/tiktok-shop` which targets product / shop endpoints.

## MCP Server

- **Package**: `tiktok-posting-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y tiktok-posting-mcp`

## Authentication

OAuth 2.0. Requires a TikTok for Developers app with the `video.publish` scope approved.

| Variable | Required | Description |
|----------|----------|-------------|
| `TIKTOK_CLIENT_KEY` | Yes | Client key from developers.tiktok.com |
| `TIKTOK_CLIENT_SECRET` | Yes | Client secret |
| `TIKTOK_ACCESS_TOKEN` | Yes | User access token (OAuth) |
| `TIKTOK_OPEN_ID` | No | Cached open_id for the authorized user |

## Available Tools

| Tool | Description |
|------|-------------|
| `tiktok_publish_video` | Direct Post (FILE_UPLOAD or PULL_FROM_URL) |
| `tiktok_inbox_video` | Inbox upload (user finishes posting in-app) |
| `tiktok_publish_photo` | Carousel / photo post |
| `tiktok_query_creator_info` | Fetch creator caps (max duration, watermarked, etc.) |
| `tiktok_get_publish_status` | Poll publish status |

## Configuration Example

```toml
[[mcp.servers]]
name = "tiktok-posting"
type = "stdio"
command = "npx"
args = ["-y", "tiktok-posting-mcp"]
timeout_seconds = 180
env = { TIKTOK_CLIENT_KEY = "{{INPUT:TIKTOK_CLIENT_KEY}}", TIKTOK_CLIENT_SECRET = "{{INPUT:TIKTOK_CLIENT_SECRET}}", TIKTOK_ACCESS_TOKEN = "{{INPUT:TIKTOK_ACCESS_TOKEN}}" }
tools = []
```

**Notes:** App must pass TikTok review for production-tier posting. Sandbox apps can only post unlisted to test users. Always call `query_creator_info` first to respect per-creator caps.

## Links

- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started/)
