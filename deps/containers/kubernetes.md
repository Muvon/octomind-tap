# containers/kubernetes

Kubernetes cluster management MCP server. Manage pods, deployments, services, helm charts, and execute commands on resources.

## MCP Server

- **Package**: `kubernetes-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y kubernetes-mcp-server@latest`

## Authentication

Kubernetes kubeconfig or in-cluster service account

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_resources` | List K8s resources |
| `get_resource` | Get resource details |
| `create_resource` | Create resource |
| `delete_resource` | Delete resource |
| `exec_command` | Execute on resource |
| `helm_install` | Install Helm chart |
| `helm_list` | List Helm releases |

## Configuration Example

```toml
[[mcp.servers]]
name = "kubernetes"
type = "stdio"
command = "npx"
args = ["-y", "kubernetes-mcp-server"]
timeout_seconds = 60
tools = []
```

**Notes:** Also available via pip (kubernetes-mcp-server) and Docker. Supports --read-only and --disable-destructive flags.

## Links

- [Homepage](https://github.com/containers/kubernetes-mcp-server)
