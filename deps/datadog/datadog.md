# datadog/datadog

Datadog monitoring and observability MCP server. Query metrics, logs, incidents, hosts, downtimes, and RUM data.

## MCP Server

- **Package**: `@winor30/mcp-server-datadog`
- **Transport**: stdio
- **Command**: `npx -y @winor30/mcp-server-datadog`

## Authentication

API key + Application key

| Variable | Required | Description |
|----------|----------|-------------|
| `DATADOG_API_KEY` | Yes | Datadog API key |
| `DATADOG_APP_KEY` | Yes | Datadog Application key |
| `DATADOG_SITE` | No | Site endpoint (e.g. datadoghq.eu) |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_incidents` | List incidents |
| `get_monitors` | Get monitors |
| `query_metrics` | Query metrics |
| `get_logs` | Get logs |
| `list_dashboards` | List dashboards |
| `list_hosts` | List hosts |
| `schedule_downtime` | Schedule downtime |
| `get_rum_events` | RUM events |

## Configuration Example

```toml
[[mcp.servers]]
name = "datadog"
type = "stdio"
command = "npx"
args = ["-y", "@winor30/mcp-server-datadog"]
timeout_seconds = 60
env = { DATADOG_API_KEY = "your-value", DATADOG_APP_KEY = "your-value", DATADOG_SITE = "your-value" }
tools = []
```

**Notes:** 20 tools including RUM (Real User Monitoring).

## Links

- [Homepage](https://www.npmjs.com/package/@winor30/mcp-server-datadog)
