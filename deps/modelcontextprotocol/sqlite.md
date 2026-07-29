# modelcontextprotocol/sqlite

Official MCP SQLite server. Query and manage SQLite databases.

## MCP Server

- **Package**: `mcp-server-sqlite (PyPI)`
- **Transport**: stdio
- **Command**: `npx mcp-server-sqlite (PyPI) /path/to/db.sqlite`

## Authentication

None (database path via arg)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `read_query` | Execute SELECT |
| `write_query` | Execute INSERT/UPDATE/DELETE |
| `create_table` | Create table |
| `list_tables` | List tables |
| `describe_table` | Table schema |

## Configuration Example

```toml
[[mcp.servers]]
name = "sqlite"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-sqlite (PyPI)"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite)
