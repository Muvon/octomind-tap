# webflow/webflow

Official Webflow CMS MCP server. Manage sites, pages, collections, and CMS content.

## MCP Server

- **Package**: `webflow-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y webflow-mcp-server@latest`

## Authentication

API token or OAuth (remote)

| Variable | Required | Description |
|----------|----------|-------------|
| `WEBFLOW_TOKEN` | Yes | API token from Webflow API Playground |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Webflow Data API — sites, pages, collections, CMS |

## Configuration Example

```toml
[[mcp.servers]]
name = "webflow"
type = "stdio"
command = "npx"
args = ["-y", "webflow-mcp-server"]
timeout_seconds = 60
env = { WEBFLOW_TOKEN = "your-value" }
tools = []
```

**Notes:** Official Webflow package. Remote endpoint: https://mcp.webflow.com/sse. Requires Node.js 22.3.0+.

## Links

- [Homepage](https://www.npmjs.com/package/webflow-mcp-server)
