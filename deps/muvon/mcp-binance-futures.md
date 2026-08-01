# muvon/mcp-binance-futures

Binance USDT-M Futures MCP server by Muvon. Exposes market data, account state, order management, and position/margin control so an agent can monitor, place, and manage perpetual futures trades.

## MCP Server

- **Package**: `mcp-binance-futures` (PyPI, pinned)
- **Transport**: stdio
- **Command**: `uvx mcp-binance-futures==0.1.0`

## Authentication

Create a Binance API key with Futures trading enabled. Use IP whitelisting; never commit keys.

| Variable | Required | Description |
|----------|----------|-------------|
| `BINANCE_API_KEY` | yes (signed tools) | API key with Futures permission |
| `BINANCE_API_SECRET` | yes (signed tools) | API secret |

Public market-data tools work without keys; account, order, and position tools require both variables.

## Available Tools

| Tool | Description |
|------|-------------|
| `ping` | Test API connectivity |
| `get_ticker` | Price, 24h stats, mark price, funding rate |
| `get_order_book` | Top N bids/asks |
| `get_recent_trades` | Latest public trades |
| `get_klines` | OHLCV candles (1m → 1w) |
| `get_symbol_info` | Tick size, lot size, min notional, order types |
| `get_balance` | Wallet balances (non-zero assets) |
| `get_positions` | Open positions with PnL, leverage, margin type |
| `get_account_summary` | Total balance, unrealized PnL, margin usage |
| `place_order` | LIMIT, MARKET, STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET |
| `modify_order` | Change price or quantity of an open LIMIT order |
| `cancel_order` | Cancel a single order by ID |
| `cancel_all_orders` | Cancel all open orders for a symbol |
| `get_open_orders` | List open orders for a symbol |
| `get_order` | Get a specific order by ID |
| `get_order_history` | Recent order history (all statuses) |
| `get_trade_history` | Personal fill history for a symbol |
| `set_leverage` | Set leverage multiplier (1–125x) |
| `set_margin_type` | Switch ISOLATED / CROSSED |
| `adjust_isolated_margin` | Add or remove isolated margin |
| `set_position_mode` | One-way or Hedge mode |
| `get_position_mode` | Current position mode |
| `get_leverage_brackets` | Leverage tiers and maintenance margin rates |

## Configuration Example

```toml
[[mcp.servers]]
name = "binance-futures"
type = "stdio"
command = "uvx"
args = ["mcp-binance-futures==0.1.0"]
timeout_seconds = 60
tools = []
env = { BINANCE_API_KEY = "{{ENV:BINANCE_API_KEY}}", BINANCE_API_SECRET = "{{ENV:BINANCE_API_SECRET}}" }
```

## Links

- [Homepage](https://github.com/muvon/mcp-binance-futures)
