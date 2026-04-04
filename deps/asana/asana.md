# asana/asana

Asana project management MCP server. Manage tasks, subtasks, projects, sections, and dependencies.

## MCP Server

- **Package**: `mcp-server-asana (GitHub only — not on npm)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm start`

## Authentication

Asana Personal Access Token

| Variable | Required | Description |
|----------|----------|-------------|
| `ASANA_TOKEN` | Yes | Personal Access Token from Asana Developer Console |
| `ASANA_WORKSPACE_ID` | Yes | Workspace identifier |

## Available Tools

| Tool | Description |
|------|-------------|
| `create-task` | Create task |
| `get-task` | Get task details |
| `list-tasks` | List tasks |
| `update-task` | Update task |
| `create-subtask` | Create subtask |
| `list-projects` | List projects |
| `create-section` | Create section |
| `add-dependencies` | Add task dependencies |

## Configuration Example

```toml
[[mcp.servers]]
name = "asana"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-asana (GitHub only — not on npm)"]
timeout_seconds = 60
env = { ASANA_TOKEN = "your-value", ASANA_WORKSPACE_ID = "your-value" }
tools = []
```

**Notes:** Not on npm — requires git clone from GitHub.

## Links

- [Homepage](https://www.npmjs.com/package/mcp-server-asana)
