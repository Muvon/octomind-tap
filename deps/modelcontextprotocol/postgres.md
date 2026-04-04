# modelcontextprotocol/postgres

Official MCP PostgreSQL server. Read-only SQL queries against PostgreSQL databases.

## MCP Server

- **Package**: `@modelcontextprotocol/server-postgres`
- **Transport**: stdio
- **Command**: `npx @modelcontextprotocol/server-postgres postgresql://localhost/mydb`

## Authentication

PostgreSQL connection string (passed as arg)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `query` | Execute read-only SQL query |

## Configuration Example

```toml
[[mcp.servers]]
name = "postgres"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-postgres"]
timeout_seconds = 60
tools = []
```

**Notes:** DEPRECATED. All queries run in READ ONLY transaction.

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres)
