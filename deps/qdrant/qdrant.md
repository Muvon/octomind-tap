# qdrant/qdrant

Qdrant vector search engine MCP server. Store and retrieve information using semantic vector search.

## MCP Server

- **Package**: `mcp-server-qdrant (Python — use uvx)`
- **Transport**: stdio
- **Command**: `uvx mcp-server-qdrant`

## Authentication

API key (optional, for remote servers)

| Variable | Required | Description |
|----------|----------|-------------|
| `QDRANT_URL` | No | Remote server URL |
| `QDRANT_LOCAL_PATH` | No | Local database path |
| `QDRANT_API_KEY` | No | API key for remote |
| `COLLECTION_NAME` | Yes | Default collection name |

## Available Tools

| Tool | Description |
|------|-------------|
| `qdrant-store` | Store information with metadata |
| `qdrant-find` | Retrieve relevant information |

## Configuration Example

```toml
[[mcp.servers]]
name = "qdrant"
type = "stdio"
command = "npx"
args = ["-y", "mcp-server-qdrant (Python — use uvx)"]
timeout_seconds = 60
env = { QDRANT_URL = "your-value", QDRANT_LOCAL_PATH = "your-value", QDRANT_API_KEY = "your-value", COLLECTION_NAME = "your-value" }
tools = []
```

**Notes:** Python-based — use uvx. Supports local or remote deployment.

## Links

- [Homepage](https://github.com/punkpeye/awesome-mcp-servers)
