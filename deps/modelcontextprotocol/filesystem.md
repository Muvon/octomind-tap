# modelcontextprotocol/filesystem

Official MCP filesystem server. Secure file read, write, search, and directory operations with configurable access.

## MCP Server

- **Package**: `@modelcontextprotocol/server-filesystem`
- **Transport**: stdio
- **Command**: `npx @modelcontextprotocol/server-filesystem /path/to/allowed/dir`

## Authentication

None (filesystem path restriction via args)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `read_file` | Read file content |
| `write_file` | Write file |
| `list_directory` | List directory |
| `search_files` | Search files |
| `create_directory` | Create directory |
| `move_file` | Move/rename file |

## Configuration Example

```toml
[[mcp.servers]]
name = "filesystem"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
