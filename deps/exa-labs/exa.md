# exa-labs/exa

Exa AI-powered web search MCP server. Semantic search, code search, company research, and webpage content extraction.

## MCP Server

- **Package**: `Remote: https://mcp.exa.ai/mcp`
- **Transport**: stdio
- **Command**: `Remote HTTP endpoint (or npx @exa-ai/mcp-server locally)`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `EXA_API_KEY` | Yes | API key from dashboard.exa.ai/api-keys |

## Available Tools

| Tool | Description |
|------|-------------|
| `web_search_exa` | Web search |
| `get_code_context_exa` | Code search (GitHub/StackOverflow) |
| `crawling_exa` | Extract webpage content |
| `web_search_advanced_exa` | Advanced filtered search (disabled by default) |

## Configuration Example

```toml
[[mcp.servers]]
name = "exa"
type = "stdio"
command = "npx"
args = ["-y", "Remote: https://mcp.exa.ai/mcp"]
timeout_seconds = 60
env = { EXA_API_KEY = "your-value" }
tools = []
```

**Notes:** Hosted endpoint recommended. Paid API.

## Links

- [Homepage](https://github.com/exa-labs/exa-mcp-server)
