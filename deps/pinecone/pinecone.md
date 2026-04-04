# pinecone/pinecone

Official Pinecone vector database MCP server. Create indexes, upsert records, search with auto-embedding, and rerank results.

## MCP Server

- **Package**: `@pinecone-database/mcp`
- **Transport**: stdio
- **Command**: `npx @pinecone-database/mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `PINECONE_API_KEY` | Yes | API key from Pinecone console |

## Available Tools

| Tool | Description |
|------|-------------|
| `search-docs` | Search Pinecone docs |
| `list-indexes` | List indexes |
| `describe-index` | Index config |
| `create-index-for-model` | Create index |
| `upsert-records` | Insert/update with auto-embedding |
| `search-records` | Query with metadata filter |
| `cascading-search` | Multi-index search |
| `rerank-documents` | Apply reranking |

## Configuration Example

```toml
[[mcp.servers]]
name = "pinecone"
type = "stdio"
command = "npx"
args = ["-y", "@pinecone-database/mcp"]
timeout_seconds = 60
env = { PINECONE_API_KEY = "your-value" }
tools = []
```

**Notes:** Official Pinecone package. 9 tools. Only supports indexes with integrated inference.

## Links

- [Homepage](https://www.npmjs.com/package/@pinecone-database/mcp)
