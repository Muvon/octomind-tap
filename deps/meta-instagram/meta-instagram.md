# meta-instagram/meta-instagram

Meta Instagram Graph API MCP server. Publishes Reels, feed video, Stories, and carousels through the official Meta Graph API.

## MCP Server

- **Package**: `@mcpware/instagram-mcp` (community)
- **Transport**: stdio
- **Command**: `npx -y @mcpware/instagram-mcp`

## Authentication

Requires a Meta App with Instagram Login (Business / Creator) and a long-lived access token.

| Variable | Required | Description |
|----------|----------|-------------|
| `INSTAGRAM_ACCESS_TOKEN` | Yes | Meta app ID |
| `INSTAGRAM_ACCOUNT_ID` | Yes | Meta app secret |
| `META_ACCESS_TOKEN` | Yes | Long-lived user access token with `instagram_basic`, `instagram_content_publish`, `pages_show_list` |
| `IG_USER_ID` | Yes | Instagram Business / Creator account ID |

## Available Tools

| Tool | Description |
|------|-------------|
| `publish_media / publish_carousel / publish_reel` | Publish via the Graph API |
| `get_content_publishing_limit` | Remaining publish quota |
| `get_media_posts / get_media_insights` | Published media and insights |
| `validate_access_token` | Token health check |

## Configuration Example

```toml
[[mcp.servers]]
name = "instagram"
type = "stdio"
command = "npx"
args = ["-y", "@mcpware/instagram-mcp"]
timeout_seconds = 180
env = { INSTAGRAM_ACCESS_TOKEN = "{{INPUT:INSTAGRAM_ACCESS_TOKEN}}", INSTAGRAM_ACCOUNT_ID = "{{INPUT:INSTAGRAM_ACCOUNT_ID}}", META_ACCESS_TOKEN = "{{INPUT:META_ACCESS_TOKEN}}", IG_USER_ID = "{{INPUT:IG_USER_ID}}" }
tools = []
```

**Notes:** Reels container needs a publicly reachable HTTPS URL. Use a temporary upload bucket (S3 / Cloudflare R2 / Mux). Always poll `IN_PROGRESS` → `FINISHED` before calling publish.

## Links

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
