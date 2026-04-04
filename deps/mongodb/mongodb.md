# mongodb/mongodb

MongoDB Atlas and database operations MCP server. Manage clusters, databases, collections, and run queries.

## MCP Server

- **Package**: `@mongodb-js/mongodb-mcp-server (renamed to mongodb-mcp-server)`
- **Transport**: stdio
- **Command**: `npx @mongodb-js/mongodb-mcp-server`

## Authentication

MongoDB connection string and/or Atlas API credentials

| Variable | Required | Description |
|----------|----------|-------------|
| `MDB_MCP_CONNECTION_STRING` | No | MongoDB connection string |
| `MDB_MCP_API_CLIENT_ID` | No | Atlas API client ID |
| `MDB_MCP_API_CLIENT_SECRET` | No | Atlas API client secret |

## Available Tools

| Tool | Description |
|------|-------------|
| `find` | Query documents |
| `aggregate` | Aggregation pipeline |
| `insert_one` | Insert document |
| `update_one` | Update document |
| `delete_one` | Delete document |
| `list_databases` | List databases |
| `list_collections` | List collections |
| `atlas-list-clusters` | List Atlas clusters |

## Configuration Example

```toml
[[mcp.servers]]
name = "mongodb"
type = "stdio"
command = "npx"
args = ["-y", "@mongodb-js/mongodb-mcp-server (renamed to mongodb-mcp-server)"]
timeout_seconds = 60
env = { MDB_MCP_CONNECTION_STRING = "your-value", MDB_MCP_API_CLIENT_ID = "your-value", MDB_MCP_API_CLIENT_SECRET = "your-value" }
tools = []
```

**Notes:** DEPRECATED name — renamed to mongodb-mcp-server. 20+ tools covering Atlas + database ops.

## Links

- [Homepage](https://www.npmjs.com/package/@mongodb-js/mongodb-mcp-server)
