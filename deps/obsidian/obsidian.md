# obsidian/obsidian

Obsidian vault MCP server. Read, create, search, and manage notes with backlink generation and folder operations.

## MCP Server

- **Package**: `@huangyihe/obsidian-mcp`
- **Transport**: stdio
- **Command**: `npx @huangyihe/obsidian-mcp`

## Authentication

API Token (from Obsidian Local REST API plugin)

| Variable | Required | Description |
|----------|----------|-------------|
| `OBSIDIAN_VAULT_PATH` | Yes | Path to Obsidian vault |
| `OBSIDIAN_API_TOKEN` | Yes | Token from Local REST API plugin |
| `OBSIDIAN_API_PORT` | No | API port (default: 27123) |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_notes` | List notes |
| `read_note` | Read note |
| `create_note` | Create note |
| `delete_note` | Delete note |
| `search_notes` | Full-text search |
| `manage_folders` | Folder operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "obsidian"
type = "stdio"
command = "npx"
args = ["-y", "@huangyihe/obsidian-mcp"]
timeout_seconds = 60
env = { OBSIDIAN_VAULT_PATH = "your-value", OBSIDIAN_API_TOKEN = "your-value", OBSIDIAN_API_PORT = "your-value" }
tools = []
```

**Notes:** Requires Obsidian Local REST API community plugin installed and running.

## Links

- [Homepage](https://www.npmjs.com/package/@huangyihe/obsidian-mcp)
