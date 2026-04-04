# llamaindex/llama-cloud

LlamaCloud MCP server. Access LlamaIndex managed indexes, queries, and data pipelines.

## MCP Server

- **Package**: `@llamaindex/llama-cloud-mcp`
- **Transport**: stdio
- **Command**: `npx -y @llamaindex/llama-cloud-mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `LLAMA_CLOUD_API_KEY` | Yes | LlamaCloud API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | LlamaCloud managed index and query tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "llama-cloud"
type = "stdio"
command = "npx"
args = ["-y", "@llamaindex/llama-cloud-mcp"]
timeout_seconds = 60
env = { LLAMA_CLOUD_API_KEY = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@llamaindex/llama-cloud-mcp)
