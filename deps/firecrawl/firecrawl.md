# firecrawl/firecrawl

Firecrawl web scraping and data extraction MCP server. Scrape pages, crawl sites, search the web, and extract structured data.

## MCP Server

- **Package**: `firecrawl-mcp`
- **Transport**: stdio
- **Command**: `npx -y firecrawl-mcp`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `FIRECRAWL_API_KEY` | Yes | API key from firecrawl.dev/app/api-keys |
| `FIRECRAWL_API_URL` | No | Custom endpoint for self-hosted |

## Available Tools

| Tool | Description |
|------|-------------|
| `firecrawl_scrape` | Scrape single URL |
| `firecrawl_batch_scrape` | Scrape multiple URLs |
| `firecrawl_map` | Discover site URLs |
| `firecrawl_crawl` | Multi-page crawl |
| `firecrawl_search` | Web search |
| `firecrawl_extract` | Structured data extraction |

## Configuration Example

```toml
[[mcp.servers]]
name = "firecrawl"
type = "stdio"
command = "npx"
args = ["-y", "firecrawl-mcp"]
timeout_seconds = 60
env = { FIRECRAWL_API_KEY = "your-value", FIRECRAWL_API_URL = "your-value" }
tools = []
```

**Notes:** Paid service with credit system. Supports JSON schema for structured extraction.

## Links

- [Homepage](https://github.com/firecrawl/firecrawl-mcp-server)
