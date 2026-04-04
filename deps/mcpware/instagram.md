# mcpware/instagram

Instagram Graph API MCP server. Manage posts, comments, DMs, stories, reels, hashtags, and account analytics.

## MCP Server

- **Package**: `@mcpware/instagram-mcp`
- **Transport**: stdio
- **Command**: `npx -y @mcpware/instagram-mcp`

## Authentication

Meta long-lived access token

| Variable | Required | Description |
|----------|----------|-------------|
| `INSTAGRAM_ACCESS_TOKEN` | Yes | Meta long-lived access token (expires 60 days) |
| `INSTAGRAM_ACCOUNT_ID` | Yes | Instagram business account ID |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_profile_info` | Profile info |
| `get_media_posts` | List posts |
| `publish_media` | Publish post |
| `publish_carousel` | Publish carousel |
| `publish_reel` | Publish reel |
| `get_comments` | Get comments |
| `post_comment` | Post comment |
| `get_conversations` | DM conversations |
| `send_dm` | Send DM |
| `search_hashtag` | Search hashtag |
| `get_stories` | Get stories |

## Configuration Example

```toml
[[mcp.servers]]
name = "instagram"
type = "stdio"
command = "npx"
args = ["-y", "@mcpware/instagram-mcp"]
timeout_seconds = 60
env = { INSTAGRAM_ACCESS_TOKEN = "your-value", INSTAGRAM_ACCOUNT_ID = "your-value" }
tools = []
```

**Notes:** 23 tools. Requires Instagram Business/Creator account linked to Facebook Page. 200 API calls/hour. 25 posts/day limit.

## Links

- [Homepage](https://www.npmjs.com/package/@mcpware/instagram-mcp)
