# iflow-mcp/social-media

Social media multi-platform MCP server. Post and schedule content across multiple social platforms.

## MCP Server

- **Package**: `@iflow-mcp/2389-research-mcp-socialmedia`
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/2389-research-mcp-socialmedia`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `SOCIALMEDIA_API_KEY` | Yes | API authentication key |
| `SOCIALMEDIA_API_BASE_URL` | Yes | Base API URL |
| `SOCIALMEDIA_TEAM_ID` | Yes | Team identifier |

## Available Tools

| Tool | Description |
|------|-------------|
| `login` | Authenticate |
| `read_posts` | Read posts |
| `create_post` | Create post |

## Configuration Example

```toml
[[mcp.servers]]
name = "social-media"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/2389-research-mcp-socialmedia"]
timeout_seconds = 60
env = { SOCIALMEDIA_API_KEY = "your-value", SOCIALMEDIA_API_BASE_URL = "your-value", SOCIALMEDIA_TEAM_ID = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/2389-research-mcp-socialmedia)
