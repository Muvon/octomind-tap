# macos-tools/contacts

macOS Contacts database MCP server. List, search, and retrieve contacts with phone/email lookup.

## MCP Server

- **Package**: `@macos-tools/mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @macos-tools/mcp-server`

## Authentication

None (requires macOS Full Disk Access permission)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `contacts_list` | List contacts with pagination |
| `contacts_get` | Get contact by ID |
| `contacts_search` | Multi-criteria search |
| `contacts_search_by_name` | Name search |
| `contacts_search_by_phone` | Phone lookup |
| `contacts_search_by_email` | Email lookup |
| `contacts_count` | Total count |

## Configuration Example

```toml
[[mcp.servers]]
name = "contacts"
type = "stdio"
command = "npx"
args = ["-y", "@macos-tools/mcp-server"]
timeout_seconds = 60
tools = []
```

**Notes:** macOS only. Node.js 22+ required. Reads Contacts SQLite database directly.

## Links

- [Homepage](https://www.npmjs.com/package/@macos-tools/mcp-server)
