# azure/azure

Azure cloud services MCP server. Manage Azure AI Search, Cosmos DB, Key Vault, Monitor, Redis, RBAC, and more.

## MCP Server

- **Package**: `@azure/mcp`
- **Transport**: stdio
- **Command**: `npx -y @azure/mcp@latest server start`

## Authentication

Azure service principal or managed identity

| Variable | Required | Description |
|----------|----------|-------------|
| `AZURE_TENANT_ID` | Yes | Azure tenant ID |
| `AZURE_CLIENT_ID` | Yes | Service principal client ID |
| `AZURE_CLIENT_SECRET` | Yes | Service principal secret |

## Available Tools

| Tool | Description |
|------|-------------|
| `*40+ tools*` | Azure AI Search, Cosmos DB, Key Vault, Monitor, Redis, RBAC, and more |

## Configuration Example

```toml
[[mcp.servers]]
name = "azure"
type = "stdio"
command = "npx"
args = ["-y", "@azure/mcp"]
timeout_seconds = 60
env = { AZURE_TENANT_ID = "your-value", AZURE_CLIENT_ID = "your-value", AZURE_CLIENT_SECRET = "your-value" }
tools = []
```

**Notes:** BETA. List tools: npx -y @azure/mcp@latest tools list.

## Links

- [Homepage](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/)
