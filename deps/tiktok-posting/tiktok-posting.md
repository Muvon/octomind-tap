# tiktok-posting/tiktok-posting

TikTok Content Posting API MCP server. Direct Post and Photo Post for finished video creative. Distinct from `deps/tiktok/tiktok-shop` which targets product / shop endpoints.

## MCP Server

- **Package**: `@upload-post/mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y @upload-post/mcp`

## Authentication

OAuth 2.0. Requires a TikTok for Developers app with the `video.publish` scope approved.

| Variable | Required | Description |
|----------|----------|-------------|
| `UPLOAD_POST_API_KEY` | Yes | Client key from developers.tiktok.com |
| `TIKTOK_CLIENT_SECRET` | Yes | Client secret |
| `TIKTOK_ACCESS_TOKEN` | Yes | User access token (OAuth) |
| `TIKTOK_OPEN_ID` | No | Cached open_id for the authorized user |

## Available Tools

| Tool | Description |
|------|-------------|
| `upload_video` | Post video; TikTok via platforms:["tiktok"] |
| `upload_photos` | Post photo sets |
| `get_status / get_job_status` | Track upload jobs |
| `list_scheduled / edit_scheduled / cancel_scheduled` | Scheduled posts |
| `retry_post / unpublish_post` | Post lifecycle |

## Configuration Example

```toml
[[mcp.servers]]
name = "tiktok-posting"
type = "stdio"
command = "npx"
args = ["-y", "@upload-post/mcp"]
timeout_seconds = 180
env = { UPLOAD_POST_API_KEY = "{{INPUT:UPLOAD_POST_API_KEY}}", TIKTOK_CLIENT_SECRET = "{{INPUT:TIKTOK_CLIENT_SECRET}}", TIKTOK_ACCESS_TOKEN = "{{INPUT:TIKTOK_ACCESS_TOKEN}}" }
tools = []
```

**Notes:** App must pass TikTok review for production-tier posting. Sandbox apps can only post unlisted to test users. Always call `query_creator_info` first to respect per-creator caps.

## Links

- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started/)
