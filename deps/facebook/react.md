# facebook/react

React MCP server providing access to React documentation and compiler tools.

## MCP Server

- **Package**: `react-mcp-server`
- **Transport**: stdio
- **Command**: `npx react-mcp-server`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | React documentation and compiler tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "react"
type = "stdio"
command = "npx"
args = ["-y", "react-mcp-server"]
timeout_seconds = 60
tools = []
```

**Notes:** Official Facebook React package. Verify availability — the GitHub path may have moved.

## Links

- [Homepage](https://github.com/facebook/react/tree/compiler/packages/react-mcp-server)
