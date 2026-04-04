# paypal/paypal

Official PayPal MCP server. Manage invoices, payments, refunds, disputes, subscriptions, shipments, and catalog products.

## MCP Server

- **Package**: `@paypal/mcp`
- **Transport**: stdio
- **Command**: `npx -y @paypal/mcp --tools=all`

## Authentication

OAuth 2.0 Access Token

| Variable | Required | Description |
|----------|----------|-------------|
| `PAYPAL_ACCESS_TOKEN` | Yes | OAuth access token |
| `PAYPAL_ENVIRONMENT` | No | SANDBOX (default) or PRODUCTION |

## Available Tools

| Tool | Description |
|------|-------------|
| `create_invoice` | Create invoice |
| `list_invoices` | List invoices |
| `create_order` | Create payment order |
| `refund_payment` | Issue refund |
| `list_disputes` | List disputes |
| `create_subscription` | Create subscription |
| `create_product` | Create catalog product |
| `create_shipment_tracking` | Track shipment |

## Configuration Example

```toml
[[mcp.servers]]
name = "paypal"
type = "stdio"
command = "npx"
args = ["-y", "@paypal/mcp"]
timeout_seconds = 60
env = { PAYPAL_ACCESS_TOKEN = "your-value", PAYPAL_ENVIRONMENT = "your-value" }
tools = []
```

**Notes:** Official PayPal package. 30+ tools. Supports sandbox and production environments.

## Links

- [Homepage](https://github.com/paypal/paypal-mcp-server)
