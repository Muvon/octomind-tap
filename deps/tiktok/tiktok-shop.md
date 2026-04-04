# tiktok/tiktok-shop

TikTok Shop MCP server. Manage orders, conversations, and reviews on TikTok Shop.

## MCP Server

- **Package**: `mcp-tiktokshop`
- **Transport**: stdio
- **Command**: `npx -y mcp-tiktokshop`

## Authentication

OAuth2 with HMAC-SHA256 request signing

| Variable | Required | Description |
|----------|----------|-------------|
| `TIKTOK_SHOP_APP_KEY` | Yes | TikTok Shop app key |
| `TIKTOK_SHOP_APP_SECRET` | Yes | App secret |
| `TIKTOK_SHOP_ACCESS_TOKEN` | Yes | OAuth access token |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_orders` | List orders |
| `get_order_detail` | Order details |
| `list_conversations` | List conversations |
| `read_conversation` | Read conversation |
| `reply_to_conversation` | Reply |
| `list_reviews` | List reviews |
| `reply_to_review` | Reply to review |

## Configuration Example

```toml
[[mcp.servers]]
name = "tiktok-shop"
type = "stdio"
command = "npx"
args = ["-y", "mcp-tiktokshop"]
timeout_seconds = 60
env = { TIKTOK_SHOP_APP_KEY = "your-value", TIKTOK_SHOP_APP_SECRET = "your-value", TIKTOK_SHOP_ACCESS_TOKEN = "your-value" }
tools = []
```

**Notes:** Original package name @aisar-labs/tiktok-shop-mcp does not exist. Use mcp-tiktokshop. Requires TikTok Shop Partner Center credentials.

## Links

- [Homepage](https://www.npmjs.com/package/@aisar-labs/tiktok-shop-mcp)
