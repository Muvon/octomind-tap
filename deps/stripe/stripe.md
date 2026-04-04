# stripe/stripe

Stripe payments MCP server.

## MCP Server

- **Package**: `@stripe/mcp`
- **Transport**: stdio
- **Command**: `npx -y @stripe/mcp`

## Authentication

Stripe secret key

| Variable | Required | Description |
|----------|----------|-------------|
| `STRIPE_SECRET_KEY` | Yes | Stripe secret key |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Payments, customers, subscriptions, invoices |

## Configuration Example

```toml
[[mcp.servers]]
name = "stripe"
type = "stdio"
command = "npx"
args = ["-y", "@stripe/mcp"]
timeout_seconds = 60
env = { STRIPE_SECRET_KEY = "your-value" }
tools = []
```

**Notes:** Package may not exist on npm — verify before use. Alternatives may be available.

## Links

- [Homepage](https://www.npmjs.com/package/@stripe/mcp)
