# ansible/ansible

Ansible automation MCP server. Access Ansible playbook documentation and automation information.

## MCP Server

- **Package**: `@scarlet-mesh/mcp-ansible-info`
- **Transport**: stdio
- **Command**: `npx -y @scarlet-mesh/mcp-ansible-info`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Ansible playbook and automation info tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "ansible"
type = "stdio"
command = "npx"
args = ["-y", "@scarlet-mesh/mcp-ansible-info"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@scarlet-mesh/mcp-ansible-info)
