# yahoo/yfinance

Yahoo Finance MCP server. Get stock prices, historical data, charts, quotes, and search financial instruments.

## MCP Server

- **Package**: `@szemeng76/yfinance-mcp-server`
- **Transport**: stdio
- **Command**: `npx @szemeng76/yfinance-mcp-server`

## Authentication

None required (public Yahoo Finance APIs)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `yahoo_stock_history` | Historical stock data |
| `yahoo_chart` | Chart data |
| `yahoo_quote` | Current quote |
| `yahoo_search` | Search instruments |
| `yahoo_quote_summary` | Quote summary |

## Configuration Example

```toml
[[mcp.servers]]
name = "yfinance"
type = "stdio"
command = "npx"
args = ["-y", "@szemeng76/yfinance-mcp-server"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/@szemeng76/yfinance-mcp-server)
