# shopify/dev-mcp

Shopify's official Dev MCP server for people building Shopify apps and themes: documentation search, Admin GraphQL schema lookup, and validation of GraphQL operations, UI extension components, and Liquid theme code. It has no access to a store's data; store operations use the `ecommerce` capability's default Shopify Admin provider.

## MCP Server

- **Package**: `@shopify/dev-mcp` (pinned in the capability file)
- **Transport**: stdio
- **Command**: `npx -y @shopify/dev-mcp@1.17.0`

## Authentication

None. The server reads public Shopify documentation and schemas.

## Available Tools

| Tool | Description |
|------|-------------|
| `learn_shopify_api` | Load guidance for a Shopify API before using it |
| `search_docs_chunks` | Search shopify.dev documentation |
| `validate_graphql_codeblocks` | Validate GraphQL operations against the Admin API schema |
| `validate_component_codeblocks` | Validate UI extension component code |
| `validate_theme_codeblocks` | Validate Liquid snippets |
| `validate_theme` | Validate a whole theme directory |

## Configuration Example

```toml
[[mcp.servers]]
name = "shopify-dev"
type = "stdio"
command = "npx"
args = ["-y", "@shopify/dev-mcp@1.17.0"]
timeout_seconds = 60
tools = []
```

## Links

- [Shopify Dev MCP](https://shopify.dev/docs/apps/build/devmcp)
- [Shopify AI Toolkit](https://github.com/Shopify/shopify-ai-toolkit)
