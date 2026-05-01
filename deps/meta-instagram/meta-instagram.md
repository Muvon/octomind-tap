# meta-instagram/meta-instagram

Meta Instagram Graph API MCP server. Publishes Reels, feed video, Stories, and carousels through the official Meta Graph API.

## MCP Server

- **Package**: `meta-instagram-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y meta-instagram-mcp`

## Authentication

Requires a Meta App with Instagram Login (Business / Creator) and a long-lived access token.

| Variable | Required | Description |
|----------|----------|-------------|
| `META_APP_ID` | Yes | Meta app ID |
| `META_APP_SECRET` | Yes | Meta app secret |
| `META_ACCESS_TOKEN` | Yes | Long-lived user access token with `instagram_basic`, `instagram_content_publish`, `pages_show_list` |
| `IG_USER_ID` | Yes | Instagram Business / Creator account ID |

## Available Tools

| Tool | Description |
|------|-------------|
| `instagram_create_reels_container` | Create a Reels media container (video URL upload) |
| `instagram_create_feed_video_container` | Create a feed video container |
| `instagram_create_carousel` | Create a carousel container |
| `instagram_publish_container` | Publish a finished container |
| `instagram_get_status` | Poll container processing status |

## Configuration Example

```toml
[[mcp.servers]]
name = "instagram"
type = "stdio"
command = "npx"
args = ["-y", "meta-instagram-mcp"]
timeout_seconds = 180
env = { META_APP_ID = "{{INPUT:META_APP_ID}}", META_APP_SECRET = "{{INPUT:META_APP_SECRET}}", META_ACCESS_TOKEN = "{{INPUT:META_ACCESS_TOKEN}}", IG_USER_ID = "{{INPUT:IG_USER_ID}}" }
tools = []
```

**Notes:** Reels container needs a publicly reachable HTTPS URL. Use a temporary upload bucket (S3 / Cloudflare R2 / Mux). Always poll `IN_PROGRESS` → `FINISHED` before calling publish.

## Links

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
