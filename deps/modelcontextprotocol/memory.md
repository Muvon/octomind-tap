# modelcontextprotocol/memory

Official MCP memory server. Knowledge graph-based persistent memory for storing and retrieving context.

## MCP Server

- **Package**: `@modelcontextprotocol/server-memory`
- **Transport**: stdio
- **Command**: `npx @modelcontextprotocol/server-memory`

## Authentication

None

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `create_entities` | Create knowledge entities |
| `create_relations` | Create relationships |
| `search_nodes` | Search graph |
| `read_graph` | Read full graph |
| `delete_entities` | Delete entities |

## Configuration Example

```toml
[[mcp.servers]]
name = "memory"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-memory"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
