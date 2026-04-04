# amplitude/amplitude

Amplitude product analytics MCP server. Query charts, dashboards, cohorts, experiments, and user feedback insights.

## MCP Server

- **Package**: `Remote server only (no npm package)`
- **Transport**: stdio
- **Command**: `Remote HTTP: https://mcp.amplitude.com/mcp`

## Authentication

OAuth 2.0 (completed through client interface)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Discovery search |
| `query_chart` | Query chart data |
| `get_dashboard` | Get dashboard |
| `get_cohorts` | Get cohorts |
| `create_chart` | Create charts |
| `get_feedback_insights` | Feedback insights |

## Configuration Example

```toml
[[mcp.servers]]
name = "amplitude"
type = "stdio"
command = "npx"
args = ["-y", "Remote server only (no npm package)"]
timeout_seconds = 60
tools = []
```

**Notes:** Remote server only — no local installation. EU endpoint: https://mcp.eu.amplitude.com/mcp. 24+ tools.

## Links

- [Homepage](https://amplitude.com/docs/amplitude-ai/amplitude-mcp)
