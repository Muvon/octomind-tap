# n8n/n8n

n8n workflow automation MCP server. Create, manage, execute, and audit workflows with full lifecycle control.

## MCP Server

- **Package**: `@makafeli/n8n-workflow-builder`
- **Transport**: stdio
- **Command**: `npx @makafeli/n8n-workflow-builder`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `N8N_HOST` | Yes | n8n instance URL |
| `N8N_API_KEY` | Yes | n8n API key from Settings > API Keys |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_workflows` | List workflows |
| `get_workflow` | Get workflow |
| `create_workflow` | Create workflow |
| `execute_workflow` | Execute workflow |
| `activate_workflow` | Activate workflow |
| `deactivate_workflow` | Deactivate |
| `list_executions` | List executions |
| `generate_audit` | Compliance audit |

## Configuration Example

```toml
[[mcp.servers]]
name = "n8n"
type = "stdio"
command = "npx"
args = ["-y", "@makafeli/n8n-workflow-builder"]
timeout_seconds = 60
env = { N8N_HOST = "your-value", N8N_API_KEY = "your-value" }
tools = []
```

**Notes:** 15 tools. Works with n8n Cloud and self-hosted.

## Links

- [Homepage](https://www.npmjs.com/package/@makafeli/n8n-workflow-builder)
