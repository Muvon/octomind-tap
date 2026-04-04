# hashicorp/terraform

Terraform MCP server. Access provider docs, module info, workspace management, and Sentinel policies.

## MCP Server

- **Package**: `Remote/native integration (no npm package)`
- **Transport**: stdio
- **Command**: `Native integration in supported clients`

## Authentication

Terraform Cloud/Enterprise API Token

| Variable | Required | Description |
|----------|----------|-------------|
| `TERRAFORM_API_TOKEN` | Yes | Terraform Cloud/Enterprise token |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_provider_docs` | Provider documentation |
| `get_module_info` | Module inputs/outputs |
| `manage_workspaces` | Workspace CRUD |
| `manage_variables` | Variable management |

## Configuration Example

```toml
[[mcp.servers]]
name = "terraform"
type = "stdio"
command = "npx"
args = ["-y", "Remote/native integration (no npm package)"]
timeout_seconds = 60
env = { TERRAFORM_API_TOKEN = "your-value" }
tools = []
```

**Notes:** BETA. Supports HCP Terraform and Terraform Enterprise.

## Links

- [Homepage](https://developer.hashicorp.com/terraform/mcp-server)
