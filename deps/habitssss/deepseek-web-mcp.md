# habitssss/deepseek-web-mcp

Community MCP server for DeepSeek's official Search and Fetch APIs. Returns raw search results and page Markdown; no chat model is called.

## MCP Server

- **Package**: `deepseek-web-mcp`
- **Transport**: stdio
- **Command**: `npx -y deepseek-web-mcp@0.1.0`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes | API key from platform.deepseek.com |

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Web search: ranked results, source URLs, summaries; optional page content |
| `fetch` | Fetch one public URL as Markdown |

## Configuration Example

```toml
[[mcp.servers]]
name = "deepseek-web"
type = "stdio"
command = "npx"
args = ["-y", "deepseek-web-mcp@0.1.0"]
timeout_seconds = 60
env = { DEEPSEEK_API_KEY = "your-value" }
tools = []
```

**Notes:** Billed per successful request by DeepSeek (Search and Fetch priced separately). The package declares Node.js >= 22.

## Links

- [Homepage](https://github.com/habitssss/deepseek-web-mcp)
- [DeepSeek Search API docs](https://api-docs.deepseek.com/guides/search)
