# adobe/react-aria

Adobe's official React Aria documentation MCP server. Provides access to React Aria component docs, patterns, and API references.

## MCP Server

- **Package**: `@react-aria/mcp`
- **Transport**: stdio
- **Command**: `npx -y @react-aria/mcp`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | React Aria documentation access tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "react-aria"
type = "stdio"
command = "npx"
args = ["-y", "@react-aria/mcp"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@react-aria/mcp)
