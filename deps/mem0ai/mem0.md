# mem0ai/mem0

Mem0 persistent AI memory MCP server. Store, search, update, and manage memories with graph support.

## MCP Server

- **Package**: `mem0-mcp-server (Python — use pip/uvx)`
- **Transport**: stdio
- **Command**: `uv run mem0-mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `MEM0_API_KEY` | Yes | Mem0 platform API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `add_memory` | Store memory |
| `search_memories` | Search memories |
| `get_memories` | List memories |
| `update_memory` | Update memory |
| `delete_memory` | Delete memory |
| `list_entities` | List entities |

## Configuration Example

```toml
[[mcp.servers]]
name = "mem0"
type = "stdio"
command = "npx"
args = ["-y", "mem0-mcp-server (Python — use pip/uvx)"]
timeout_seconds = 60
env = { MEM0_API_KEY = "your-value" }
tools = []
```

**Notes:** Python-based. Repository archived — Mem0 now offers official cloud-hosted MCP server.

## Links

- [Homepage](https://github.com/mem0ai/mem0-mcp)
