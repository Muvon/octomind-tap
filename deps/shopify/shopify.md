# shopify/shopify

Shopify Admin MCP server (`@acodera/shopify-admin-mcp`, a community server; Shopify publishes no Admin MCP of its own). It talks to the Admin GraphQL API 2026-10 and covers products and variants, collections, metafields, inventory, customers, orders, discounts, files, markets, and themes, plus raw GraphQL and live schema search. Toolsets, read-only mode, and theme-write switches narrow what an agent can call; the app's access scopes are the real limit.

## MCP Server

- **Package**: `@acodera/shopify-admin-mcp` (pinned in the capability file)
- **Transport**: stdio
- **Command**: `npx -y @acodera/shopify-admin-mcp@1.11.0 --toolsets products,collections,metafields,customers,orders,inventory,discounts --disable-theme-writes`
- **Runtime**: Node.js 22.12+

## Authentication

Create an app in the Shopify [Dev Dashboard](https://dev.shopify.com/dashboard), give it only the scopes the agent needs, release a version, and install it on the store (app and store in the same Shopify organization). The server exchanges the client ID and secret for 24-hour tokens and refreshes them itself. Stores with a legacy custom app can use its `shpat_` token instead.

| Variable | Required | Description |
|----------|----------|-------------|
| `SHOPIFY_STORE` | Yes | `mystore` or `mystore.myshopify.com` |
| `SHOPIFY_CLIENT_ID` | Yes (client credentials) | Dev Dashboard app client ID |
| `SHOPIFY_CLIENT_SECRET` | Yes (client credentials) | Dev Dashboard app client secret |
| `SHOPIFY_ACCESS_TOKEN` | Legacy only | `shpat_` token of a legacy custom app, instead of the ID and secret |

Scopes for store operations without refunds: `read_products,write_products,read_inventory,write_inventory,read_locations,read_customers,write_customers,read_orders,read_draft_orders,write_draft_orders,read_discounts,write_discounts` (add `read_all_orders` for orders older than 60 days). Customer personal data also needs Shopify's protected customer data approval.

## Available Tools

| Tool | Description |
|------|-------------|
| `shopify_products_list`, `shopify_product_get`, `shopify_product_create`, `shopify_product_update` | Catalog |
| `shopify_product_variants_create`, `shopify_product_variants_update` | Variants, prices, SKUs, barcodes |
| `shopify_collections_list`, `shopify_collection_get`, `shopify_collection_create`, `shopify_collection_update` | Collections |
| `shopify_metafields_list`, `shopify_metafields_set`, `shopify_metafield_definitions_list` | Structured attributes |
| `shopify_inventory_get_levels`, `shopify_inventory_adjust` | Stock per location (adjust needs the expected current quantity) |
| `shopify_customers_list`, `shopify_customer_get`, `shopify_customer_update` | Customers |
| `shopify_orders_list`, `shopify_order_get` | Orders (read) |
| `shopify_discounts_list`, `shopify_discount_get`, `shopify_discount_amount_off_create`, `shopify_discount_free_shipping_create`, `shopify_discount_bxgy_create`, `shopify_discount_codes_add` | Discounts |
| `shopify_graphql` | Any Admin GraphQL query or mutation the scopes allow (draft orders, reports) |
| `shopify_schema_search`, `shopify_schema_details` | Find types, queries, and mutations in the live schema |

## Configuration Example

```toml
[[mcp.servers]]
name = "shopify"
type = "stdio"
command = "npx"
args = ["-y", "@acodera/shopify-admin-mcp@1.11.0", "--toolsets", "products,collections,metafields,customers,orders,inventory,discounts", "--disable-theme-writes"]
timeout_seconds = 120
env = { SHOPIFY_STORE = "{{ENV:SHOPIFY_STORE}}", SHOPIFY_CLIENT_ID = "{{ENV:SHOPIFY_CLIENT_ID}}", SHOPIFY_CLIENT_SECRET = "{{ENV:SHOPIFY_CLIENT_SECRET}}" }
tools = []
```

Add `--read-only` for reporting-only agents, and `--disable-raw-graphql` to keep an agent to the listed toolsets.

## Links

- [Repository](https://github.com/acoderacom/shopify-admin-mcp)
- [Admin GraphQL API](https://shopify.dev/docs/api/admin-graphql)
- [Dev Dashboard apps](https://shopify.dev/docs/apps/build/dev-dashboard)
