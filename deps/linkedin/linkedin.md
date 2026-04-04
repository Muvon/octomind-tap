# linkedin/linkedin

LinkedIn MCP server. Manage profile, posts, connections, skills, work experience, education, and content sharing.

## MCP Server

- **Package**: `@pegasusheavy/linkedin-mcp`
- **Transport**: stdio
- **Command**: `npx -y @pegasusheavy/linkedin-mcp`

## Authentication

OAuth 2.0 with automatic token refresh

| Variable | Required | Description |
|----------|----------|-------------|
| `LINKEDIN_CLIENT_ID` | No | OAuth app client ID |
| `LINKEDIN_CLIENT_SECRET` | No | OAuth app client secret |
| `LINKEDIN_ACCESS_TOKEN` | No | Existing access token (alternative to OAuth) |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_linkedin_profile` | Get profile |
| `get_linkedin_posts` | Get posts |
| `get_linkedin_connections` | Get connections |
| `search_linkedin_people` | Search people |
| `share_linkedin_post` | Share post |
| `add_linkedin_skill` | Add skill |
| `get_account_insights` | Account insights |

## Configuration Example

```toml
[[mcp.servers]]
name = "linkedin"
type = "stdio"
command = "npx"
args = ["-y", "@pegasusheavy/linkedin-mcp"]
timeout_seconds = 60
env = { LINKEDIN_CLIENT_ID = "your-value", LINKEDIN_CLIENT_SECRET = "your-value", LINKEDIN_ACCESS_TOKEN = "your-value" }
tools = []
```

**Notes:** 18 tools. Uses OpenID Connect scopes. No special API access required.

## Links

- [Homepage](https://www.npmjs.com/package/@pegasusheavy/linkedin-mcp)
