# google-cloud/gcloud

Google Cloud Platform MCP server. Manage GCP resources, services, and operations.

## MCP Server

- **Package**: `@google-cloud/gcloud-mcp`
- **Transport**: stdio
- **Command**: `npx -y @google-cloud/gcloud-mcp`

## Authentication

Service Account (JSON file)

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Yes | Path to service account JSON |
| `GOOGLE_CLOUD_PROJECT` | Yes | GCP project ID |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | GCP resource management, cloud operations, data access |

## Configuration Example

```toml
[[mcp.servers]]
name = "gcloud"
type = "stdio"
command = "npx"
args = ["-y", "@google-cloud/gcloud-mcp"]
timeout_seconds = 60
env = { GOOGLE_APPLICATION_CREDENTIALS = "your-value", GOOGLE_CLOUD_PROJECT = "your-value" }
tools = []
```

**Notes:** Official Google Cloud package.

## Links

- [Homepage](https://www.npmjs.com/package/@google-cloud/gcloud-mcp)
