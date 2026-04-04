# atlassian/jira

Jira Data Center MCP server. Issue tracking, project management, comments, and workflow operations.

## MCP Server

- **Package**: `@atlassian-dc-mcp/jira`
- **Transport**: stdio
- **Command**: `npx -y @atlassian-dc-mcp/jira`

## Authentication

API token

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_URL` | Yes | Jira instance URL |
| `JIRA_EMAIL` | Yes | User email |
| `JIRA_API_TOKEN` | Yes | API token |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Issue tracking, projects, workflows tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "jira"
type = "stdio"
command = "npx"
args = ["-y", "@atlassian-dc-mcp/jira"]
timeout_seconds = 60
env = { JIRA_URL = "your-value", JIRA_EMAIL = "your-value", JIRA_API_TOKEN = "your-value" }
tools = []
```

**Notes:** Specifically for Jira Data Center.

## Links

- [Homepage](https://www.npmjs.com/package/@atlassian-dc-mcp/jira)
