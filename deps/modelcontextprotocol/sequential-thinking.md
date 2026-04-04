# modelcontextprotocol/sequential-thinking

Official MCP sequential thinking server. Structured problem-solving through dynamic thought steps with branching and revision.

## MCP Server

- **Package**: `@modelcontextprotocol/server-sequential-thinking`
- **Transport**: stdio
- **Command**: `npx @modelcontextprotocol/server-sequential-thinking`

## Authentication

None

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `sequential_thinking` | Dynamic problem-solving with thought steps, branching, and revision |

## Configuration Example

```toml
[[mcp.servers]]
name = "sequential-thinking"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-sequential-thinking"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/sequential-thinking)
