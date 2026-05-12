# modelcontextprotocol/fetch

Official Anthropic MCP server for web content retrieval. Fetches URLs and converts to markdown for LLM consumption.

## MCP Server

- **Package**: `mcp-server-fetch` (Python, published on PyPI)
- **Transport**: stdio
- **Command**: `uvx mcp-server-fetch`
- **Runtime**: requires `uv` / `uvx` (https://github.com/astral-sh/uv). Install once with `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`.

> Note: there is no `@modelcontextprotocol/server-fetch` npm package. The official fetch server is Python-based and shipped via PyPI. Earlier `npx` invocations 404 against the npm registry.

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
command = "uvx"
args = ["mcp-server-fetch"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch)
