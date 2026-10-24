# modelcontextprotocol/filesystem

Official MCP filesystem server. Secure file read, write, search, and directory operations with configurable access. The tap's `image-view` capability exposes only `read_media_file`, which returns an image file as an MCP image block so the model can see it.

## MCP Server

- **Package**: `@modelcontextprotocol/server-filesystem` (pinned in the capability file)
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-filesystem@2025.8.21 /path/to/allowed/dir`
- **Runtime**: Node.js 20+
- **Pin note**: `image-view` stays on 2025.8.21; later releases duplicate the image payload in `structuredContent`

## Authentication

None (filesystem path restriction via args)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `read_file` / `read_text_file` | Read file content |
| `read_media_file` | Read an image or audio file; returns base64 data with its MIME type (image block for images) |
| `write_file` | Write file |
| `list_directory` | List directory |
| `search_files` | Search files |
| `create_directory` | Create directory |
| `move_file` | Move/rename file |

## Configuration Example

```toml
[[mcp.servers]]
name = "image-view"
type = "stdio"
command = "sh"
args = ["-c", "exec npx -y @modelcontextprotocol/server-filesystem@2025.8.21 \"$PWD\""]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
