# upload-post/upload-post

MCP server for the hosted Upload-Post API, which publishes and schedules posts on YouTube, TikTok, Instagram, LinkedIn, X, and other networks from one account. Social accounts are connected once in the Upload-Post dashboard under a profile name (the `user` argument); the platforms' OAuth tokens and YouTube API quota stay with Upload-Post, so no Google Cloud project or TikTok developer app is needed. The tap's `publish-youtube` and `publish-tiktok` capabilities share one server block named `upload-post`.

## MCP Server

- **Package**: `@upload-post/mcp` (pinned in the capability files)
- **Transport**: stdio
- **Command**: `npx -y @upload-post/mcp@0.11.4`

## Authentication

API key from app.upload-post.com. Connect the YouTube channel and TikTok account to a profile there first. The free plan includes a small monthly upload allowance; TikTok needs a paid plan.

| Variable | Required | Description |
|----------|----------|-------------|
| `UPLOAD_POST_API_KEY` | Yes | Upload-Post API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `upload_video` | Publish or schedule a video: `user`, `platforms` (array), `videoPathOrUrl` (absolute local path or HTTPS URL), `title`, `description`, `scheduledDate` + `timezone`, `platformOptions` (e.g. `youtubePrivacyStatus`, `youtubeTags`, `youtubeCategoryId`, `youtubeThumbnailUrl`, `youtubePlaylistId`, `youtubeContainsSyntheticMedia`, `youtubeHasPaidProductPlacement`, `youtubeSelfDeclaredMadeForKids`, `tiktokPrivacyLevel`) |
| `upload_photos` | Photo posts and carousels |
| `get_status`, `get_job_status` | Poll an upload by `request_id` / job |
| `list_scheduled`, `edit_scheduled`, `cancel_scheduled` | Scheduled posts |
| `retry_post`, `unpublish_post` | Post lifecycle |
| `create_media_upload`, `complete_media_upload`, `get_media_upload` | Stage a local file (thumbnail, subtitles) as a temporary HTTPS `media_url`; the bytes are sent with an HTTP PUT in between |
| `list_users`, `get_history`, `get_post_analytics` | Profiles, posting history, per-post analytics |

## Configuration Example

```toml
[[mcp.servers]]
name = "upload-post"
type = "stdio"
command = "npx"
args = ["-y", "@upload-post/mcp@0.11.4"]
timeout_seconds = 600
env = { UPLOAD_POST_API_KEY = "{{ENV:UPLOAD_POST_API_KEY}}" }
tools = []
```

## Links

- [Repository](https://github.com/Upload-Post/upload-post-mcp)
- [Upload-Post](https://www.upload-post.com)
- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
