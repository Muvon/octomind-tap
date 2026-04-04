# pulumi/pulumi

Official Pulumi Infrastructure as Code MCP server. Manage stacks, search resources, enforce policies, and deploy to AWS.

## MCP Server

- **Package**: `Remote: https://mcp.ai.pulumi.com/mcp (or @pulumi/mcp-server locally)`
- **Transport**: stdio
- **Command**: `Remote HTTP endpoint`

## Authentication

Pulumi Cloud account (via remote auth)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `get-stacks` | List stacks |
| `resource-search` | Search resources |
| `get-policy-violations` | Policy violations |
| `deploy-to-aws` | Deploy to AWS |
| `neo-bridge` | Delegate to Pulumi Neo |

## Configuration Example

```toml
[[mcp.servers]]
name = "pulumi"
type = "stdio"
command = "npx"
args = ["-y", "Remote: https://mcp.ai.pulumi.com/mcp (or @pulumi/mcp-server locally)"]
timeout_seconds = 60
tools = []
```

**Notes:** Remote endpoint recommended. Supports delegating to Pulumi Neo for autonomous infrastructure tasks.

## Links

- [Homepage](https://www.pulumi.com/docs/ai/mcp-server/)
