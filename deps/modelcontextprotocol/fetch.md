# modelcontextprotocol/fetch

Official Anthropic MCP server for web content retrieval. Fetches URLs and converts to markdown for LLM consumption.

## MCP Server

- **Package**: `@modelcontextprotocol/server-fetch`
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-fetch`

## Authentication

None required.

## Available Tools

| Tool | Description |
|------|-------------|
| `fetch` | Fetch a URL and return content as markdown |

## Configuration Example

```toml
[[mcp.servers]]
name = "fetch"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-fetch"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
