# prometheus/prometheus

Prometheus metrics MCP server. Query metrics, get server status, list targets, and explore labels.

## MCP Server

- **Package**: `@wkronmiller/prometheus-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y -p @wkronmiller/prometheus-mcp-server prometheus-mcp-server`

## Authentication

None (direct URL connection)

| Variable | Required | Description |
|----------|----------|-------------|
| `PROMETHEUS_URL` | Yes | Prometheus server URL |

## Available Tools

| Tool | Description |
|------|-------------|
| `prometheus_status` | Server status |
| `prometheus_targets` | Scrape targets |
| `prometheus_label_names` | Label names |
| `prometheus_label_values` | Label values |
| `prometheus_instant_query` | PromQL instant query |

## Configuration Example

```toml
[[mcp.servers]]
name = "prometheus"
type = "stdio"
command = "npx"
args = ["-y", "@wkronmiller/prometheus-mcp-server"]
timeout_seconds = 60
env = { PROMETHEUS_URL = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@wkronmiller/prometheus-mcp-server)
