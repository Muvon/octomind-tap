# github/github-mcp

GitHub MCP server. Full GitHub API — repos, issues, PRs, actions, code scanning, Dependabot, and more.

## MCP Server

- **Package**: `Remote: https://api.githubcopilot.com/mcp/ (or Docker: ghcr.io/github/github-mcp-server)`
- **Transport**: stdio
- **Command**: `Remote HTTP endpoint or Docker`

## Authentication

GitHub PAT or OAuth

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Yes | GitHub PAT (for local/Docker) |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_file_contents` | Read file |
| `create_issue` | Create issue |
| `create_pull_request` | Create PR |
| `list_commits` | List commits |
| `search_code` | Search code |
| `get_code_scanning_alerts` | Security alerts |

## Configuration Example

```toml
[[mcp.servers]]
name = "github-mcp"
type = "stdio"
command = "npx"
args = ["-y", "Remote: https://api.githubcopilot.com/mcp/ (or Docker: ghcr.io/github/github-mcp-server)"]
timeout_seconds = 60
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "your-value" }
tools = []
```

**Notes:** 70+ tools. Remote server supports OAuth. Minimal token scopes recommended.

## Links

- [Homepage](https://github.com/github/github-mcp-server)
