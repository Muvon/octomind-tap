# cybeleri/social-scheduler

Social media scheduler MCP server. Schedule and publish content across Twitter/X, LinkedIn, Bluesky, and Mastodon.

## MCP Server

- **Package**: `@cybeleri/social-media-scheduler-mcp`
- **Transport**: stdio
- **Command**: `npx -y @cybeleri/social-media-scheduler-mcp`

## Authentication

Platform-specific tokens (configure per-platform)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `schedule_post` | Schedule social media post |
| `manage_content` | Manage scheduled content |

## Configuration Example

```toml
[[mcp.servers]]
name = "social-scheduler"
type = "stdio"
command = "npx"
args = ["-y", "@cybeleri/social-media-scheduler-mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Supports 4 platforms. Cron-based scheduling.

## Links

- [Homepage](https://www.npmjs.com/package/@cybeleri/social-media-scheduler-mcp)
