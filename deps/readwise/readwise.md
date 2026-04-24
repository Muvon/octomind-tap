# readwise/readwise

Readwise MCP server. Access reading highlights, books, articles, and documents.

## MCP Server

- **Package**: `readwise-mcp`
- **Transport**: stdio
- **Command**: `npx -y readwise-mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `READWISE_API_KEY` | Yes | API key from readwise.io |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_highlights` | Search reading highlights |
| `get_books` | List books and articles |
| `get_documents` | Access documents |

## Configuration Example

```toml
[[mcp.servers]]
name = "readwise"
type = "stdio"
command = "npx"
args = ["-y", "readwise-mcp"]
timeout_seconds = 60
env = { READWISE_API_KEY = "your-value" }
tools = []
```

## Links

- [Homepage](https://github.com/IAmAlexander/readwise-mcp)
