# jenkins/jenkins

Jenkins CI/CD pipeline MCP server. Manage jobs, builds, pipelines, nodes, and plugins.

## MCP Server

- **Package**: `jenkins-mcp-server (Python — use pip/uvx)`
- **Transport**: stdio
- **Command**: `python -m jenkins_mcp.server`

## Authentication

API Token, Username/Password, or OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `JENKINS_URL` | Yes | Jenkins server URL |
| `JENKINS_USERNAME` | Yes | Auth username |
| `JENKINS_API_TOKEN` | Yes | API token |

## Available Tools

| Tool | Description |
|------|-------------|
| `create_job` | Create job |
| `build_job` | Trigger build |
| `get_build_status` | Build status |
| `manage_pipeline` | Pipeline operations |
| `manage_nodes` | Node management |
| `manage_plugins` | Plugin management |

## Configuration Example

```toml
[[mcp.servers]]
name = "jenkins"
type = "stdio"
command = "npx"
args = ["-y", "jenkins-mcp-server (Python — use pip/uvx)"]
timeout_seconds = 60
env = { JENKINS_URL = "your-value", JENKINS_USERNAME = "your-value", JENKINS_API_TOKEN = "your-value" }
tools = []
```

**Notes:** Python-based — use pip install jenkins-mcp-server. Supports multi-master Jenkins.

## Links

- [Homepage](https://github.com/LokiMCPUniverse/jenkins-mcp-server)
