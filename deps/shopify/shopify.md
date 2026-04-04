# shopify/shopify

Shopify e-commerce MCP server.

## MCP Server

- **Package**: `@ajackus/shopify-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @ajackus/shopify-mcp-server`

## Authentication

Shopify API access token

| Variable | Required | Description |
|----------|----------|-------------|
| `SHOPIFY_ACCESS_TOKEN` | Yes | Shopify API access token |
| `SHOPIFY_STORE_URL` | Yes | Store URL |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Products, orders, customers, inventory management |

## Configuration Example

```toml
[[mcp.servers]]
name = "shopify"
type = "stdio"
command = "npx"
args = ["-y", "@ajackus/shopify-mcp-server"]
timeout_seconds = 60
env = { SHOPIFY_ACCESS_TOKEN = "your-value", SHOPIFY_STORE_URL = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use.

## Links

- [Homepage](https://www.npmjs.com/package/@ajackus/shopify-mcp-server)
