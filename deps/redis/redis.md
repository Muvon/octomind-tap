# redis/redis

Redis key-value store MCP server.

## MCP Server

- **Package**: `@modelcontextprotocol/server-redis`
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-redis`

## Authentication

Redis connection string

| Variable | Required | Description |
|----------|----------|-------------|
| `REDIS_URL` | Yes | Redis connection URL |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Redis key-value operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "redis"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-redis"]
timeout_seconds = 60
env = { REDIS_URL = "your-value" }
tools = []
```

**Notes:** DEPRECATED — package no longer supported.

## Links

- [Homepage](https://www.npmjs.com/package/@modelcontextprotocol/server-redis)
