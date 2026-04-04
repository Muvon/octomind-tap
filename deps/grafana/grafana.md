# grafana/grafana

Grafana monitoring MCP server. Query dashboards, Prometheus, Loki logs, incidents, alerting, OnCall, and profiling.

## MCP Server

- **Package**: `@leval/mcp-grafana`
- **Transport**: stdio
- **Command**: `npx -y @leval/mcp-grafana`

## Authentication

Service Account Token, API Key, or Basic Auth

| Variable | Required | Description |
|----------|----------|-------------|
| `GRAFANA_URL` | Yes | Grafana instance URL |
| `GRAFANA_SERVICE_ACCOUNT_TOKEN` | Yes | Service account token |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_dashboards` | Search dashboards |
| `get_dashboard` | Get dashboard |
| `prometheus_query` | Prometheus PromQL |
| `loki_query` | Loki log query |
| `list_incidents` | List incidents |
| `list_alert_rules` | Alert rules |
| `get_oncall_schedules` | OnCall schedules |

## Configuration Example

```toml
[[mcp.servers]]
name = "grafana"
type = "stdio"
command = "npx"
args = ["-y", "@leval/mcp-grafana"]
timeout_seconds = 60
env = { GRAFANA_URL = "your-value", GRAFANA_SERVICE_ACCOUNT_TOKEN = "your-value" }
tools = []
```

**Notes:** 43 tools. Supports mTLS. Covers Prometheus, Loki, incidents, alerting, OnCall, Pyroscope profiling.

## Links

- [Homepage](https://www.npmjs.com/package/@leval/mcp-grafana)
