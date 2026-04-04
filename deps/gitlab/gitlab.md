# gitlab/gitlab

GitLab integration MCP server. Manage repositories, merge requests, issues, and CI/CD pipelines.

## MCP Server

- **Package**: `@yoda.digital/gitlab-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @yoda.digital/gitlab-mcp-server`

## Authentication

Personal Access Token

| Variable | Required | Description |
|----------|----------|-------------|
| `GITLAB_URL` | Yes | GitLab instance URL |
| `GITLAB_PRIVATE_TOKEN` | Yes | Personal access token |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_projects` | List projects |
| `get_repository` | Get repo |
| `manage_issues` | Issue management |
| `manage_merge_requests` | MR management |

## Configuration Example

```toml
[[mcp.servers]]
name = "gitlab"
type = "stdio"
command = "npx"
args = ["-y", "@yoda.digital/gitlab-mcp-server"]
timeout_seconds = 60
env = { GITLAB_URL = "your-value", GITLAB_PRIVATE_TOKEN = "your-value" }
tools = []
```

**Notes:** Supports self-hosted GitLab and gitlab.com.

## Links

- [Homepage](https://www.npmjs.com/package/@yoda.digital/gitlab-mcp-server)
