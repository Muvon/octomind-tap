# linear-app/linear

Linear project management MCP server. Find, create, and update issues, projects, and comments.

## MCP Server

- **Package**: `Remote SSE: https://mcp.linear.app/sse`
- **Transport**: stdio
- **Command**: `npx -y mcp-remote https://mcp.linear.app/sse`

## Authentication

Linear platform authentication (via SSE connection)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `find_issues` | Search issues |
| `create_issue` | Create issue |
| `update_issue` | Update issue |
| `manage_projects` | Project management |
| `add_comment` | Add comment |

## Configuration Example

```toml
[[mcp.servers]]
name = "linear"
type = "stdio"
command = "npx"
args = ["-y", "Remote SSE: https://mcp.linear.app/sse"]
timeout_seconds = 60
tools = []
```

**Notes:** Remote server — no local installation. Uses mcp-remote for client access.

## Links

- [Homepage](https://linear.app/changelog/2025-05-01-mcp)
