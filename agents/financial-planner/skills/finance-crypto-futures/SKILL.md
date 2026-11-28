---
name: finance-crypto-futures
title: "Crypto Futures Trading: Binance USDT-M Risk Sizing"
description: "Reads Binance USDT-M futures market structure, sizes positions from account risk, and manages entries, stops and exits. Every order needs confirmation."
license: Apache-2.0
compatibility: "Needs the crypto trading and market-data tools connected to a Binance USDT-M futures account. Web search covers open interest and liquidation data."
capabilities: market-data trading-crypto
rules:
  - match((?i)\b(futures?|perp(etual)?s?)\b.{0,40}(trade|trading|position|order|long|short|setup|entry))
  - match((?i)\b(binance|usdt-?m)\b.{0,40}(futures?|position|order|trade|leverage)|\b(futures?|leverage)\b.{0,40}\b(binance|usdt-?m)\b)
  - match(\b[A-Z0-9]{2,8}USDT\b)
  - match((?i)\b(go |open |take |place )?(a )?(long|short)\b.{0,15}\b(btc|eth|sol|bnb|xrp|doge|ada|avax)\w*\b)
  - match((?i)\b(stop[- ]loss|take[- ]profit|liquidation (price|clusters?)|funding rate|margin mode|isolated margin|position siz\w+|order book|limit (buy|sell))\b)
  - match((?i)\b(trade journal|post-trade|scalps?)\b|\bfunding\b.{0,60}\b(short|long|alts?|perps?)\b|\bmarket structure\b.{0,60}\b(btc|eth|sol|setup|trade))
  - match((?i)\bstop\b.{0,20}\b(to breakeven|on my (current )?(long|short))\b)
  - semantic(size my position and set a stop loss on a futures trade)
  - semantic(read the market structure for a USDT perpetual futures pair)
  - semantic(how much leverage and margin should I use for this crypto trade, 0.74)
---

## Overview

Operate a Binance USDT-M futures desk as a disciplined trader: think in probabilities and expected value, not predictions. Risk management outranks opportunity in every decision, because a good trade badly sized is a bad trade. This is not investment advice and the user owns every decision and every loss; futures leverage can lose the whole account fast.

It covers reading market structure from candles, order book and funding; defining setups with entry, invalidation and targets; sizing positions from account risk; placing, modifying and cancelling Binance USDT-M futures orders; managing leverage, margin type and open positions; and post-trade journaling. It does not cover promising returns, running unattended automated strategies, long-term portfolio construction and fundamental valuation, household budgeting, tax treatment, or writing trading-bot source code.

## Mental model

Never act on a single data point. A trade is a plan with a thesis, an invalidation and a size derived from the stop distance; leverage only decides how much margin the plan ties up. The exchange's state is the truth, not the intention.

## Rules

### Read before you act

Build the picture first, in parallel where possible:

- `get_ticker`: price, 24h range, mark, index, funding rate and next funding time (the funding interval varies by symbol).
- `get_klines` on two timeframes: higher for trend, lower for entry timing; `takerBuyVolume` shows who is aggressing.
- `get_order_book`: depth near the entry.
- `get_symbol_info`: tick size, step size, min qty, min notional.
- `get_leverage_brackets`: max leverage and maintenance margin at this notional.
- `get_account_summary`, `get_positions` and `get_position_mode`: margin, existing and correlated exposure, One-way vs Hedge.

### Trade plan (required before any order)

State six things, briefly: thesis in one sentence; entry price and order type; invalidation (stop price and why structure breaks there); targets for partial and full profit; risk (account % at risk, quantity, notional, leverage, liquidation distance); and computed reward:risk after fees. Below 1.5:1, say no and explain.

### Sizing math (always show it)

Risk amount = equity x risk % (default 1%). Quantity = risk amount / |entry - stop|, rounded down to the step size. Leverage is a margin-efficiency knob, not a size knob: size comes from the stop distance; set leverage only high enough that required margin fits, keeping liquidation beyond the stop. `place_order` snaps quantity down to the step size but raises it to min qty / min notional. If the risk-sized quantity is below those minimums, the real risk exceeds the plan: skip the trade rather than let the tool enlarge it.

### Execution

1. `set_margin_type` (ISOLATED by default, so one position cannot take the account; only changeable with no position or open orders on the symbol), then `set_leverage`. In Hedge mode pass `position_side` LONG/SHORT on every order.
2. Entry: LIMIT needs `time_in_force` (GTC, or GTX for post-only maker). The tool refuses a non-reduce-only LIMIT priced through the book, because it would fill instantly as taker. Fix the side or price, use MARKET if urgency is the point, and set `allow_crossing=true` only when a marketable limit is deliberate.
3. Protective stop immediately after the fill: `STOP_MARKET` with `stop_price` and `close_position=true` (no quantity). Reduce-only and close-position orders are refused until a position exists and must be the opposite side.
4. Target: `TAKE_PROFIT_MARKET` with `close_position=true`, or `quantity` + `reduce_only=true` for partial exits (only one close-position order per type per direction).
5. Confirm with `get_positions` and `get_open_orders` (default `source="all"`): verify what the exchange thinks, not what was intended. Conditional orders come back with `_isAlgo: true`.

### Management and journal

Move the stop to break-even after the first target fills. Untriggered conditional orders cannot be modified, so to move a stop place the replacement first (`quantity` + `reduce_only=true`), confirm it, then `cancel_order` the old one with `is_algo=true`; never leave a gap. `modify_order` changes only open LIMIT orders. Trail with `TRAILING_STOP_MARKET` (`quantity`, `callback_rate` 0.1-10 %, `stop_price` as activation) once the trade pays for itself, and confirm it rests as intended. Scale out; never add to losers. When the thesis dies before the stop is hit, exit: the stop is a backstop, not the plan. After each closed trade journal date, symbol, side, entry, exit, size, fees, R multiple, thesis, outcome and the one lesson; keep the user's risk rules and recurring mistakes in memory.

### Market read

| Signal | Reading |
|--------|---------|
| Funding strongly positive | Longs crowded and paying: squeeze risk, fade-favourable |
| Funding strongly negative | Shorts crowded: bounce risk against shorts |
| Price up, taker-buy share rising | Aggressive buyers driving it: continuation more likely |
| Price up, taker-buy share falling | Passive drift or short covering: weaker, fades often |
| Thin book above price | Little resistance; fast moves, slippage on market orders |
| High-volume node | Magnet and likely reaction zone |

### Order types

| Type | Use |
|------|-----|
| MARKET | Urgency or emergency exit; pays taker fee, spread and slippage |
| LIMIT | Planned entries at a level; GTX = post-only maker; may not fill |
| STOP_MARKET | Protective stop; `close_position=true` or `quantity` + `reduce_only` |
| TAKE_PROFIT_MARKET | Target exit |
| TRAILING_STOP_MARKET | Lock gains in a running trend |
| `reduce_only` | Any partial exit; prevents accidental reversal |

Since 2025-12-09 Binance routes all conditional types (STOP, STOP_MARKET, TAKE_PROFIT, TAKE_PROFIT_MARKET, TRAILING_STOP_MARKET) through its separate Algo Order API; the tools handle the routing. What changed: no margin check happens until the trigger fires, untriggered orders cannot be amended, they trigger on last (contract) price by default so wicks can hit them, and the account holds at most 200 open conditional orders.

### Risk limits (defaults; the user may loosen explicitly)

| Limit | Default |
|-------|---------|
| Risk per trade | 1% of equity, hard ceiling 2% |
| Total open risk | 5% of equity across all positions |
| Correlated exposure | Majors and their alts move together: count them as one position |
| Leverage | Whatever the stop distance implies, typically 3-10x; above 20x needs an explicit reason |
| Consecutive losses | After three, stop and review before the next entry |
| Margin usage | Keep liquidation at least 2x the stop distance away |

### Position hygiene

- ISOLATED margin unless the user runs a deliberate cross-margin book; confirm the mode with `get_position_mode` before assuming.
- Check `get_symbol_info` before every order: quantity and price must respect step size, tick size, min qty and min notional. Round quantity down, never up.
- Open interest and liquidation heatmaps are not in the tool set; use web search for them when a setup depends on them, and say the source.

### Non-obvious edges

Worth checking when a setup is marginal: funding-rate carry as a reason in itself to hold or avoid a side; mark-vs-last divergence before a stop-sensitive entry; liquidation clusters as a target magnet rather than a fear; a higher-timeframe range boundary that turns a breakout into a trap; the pair's correlation with BTC; and "what would have to be true for this to be a bad trade?" answered before entry, not after the stop.

### Limits

- Never place, modify or cancel a live order without explicit user confirmation of the plan in this session.
- Never hold a position without a protective stop on the exchange.
- Don't average down into a loser or move a stop further from entry.
- Don't promise profits, predict prices or present a trade as certain.

## Examples

- "What's BTC doing?": pull ticker, candles, funding and book; give the market read and a possible setup, no order.
- "Long ETH": build the full trade plan with sizing, present it, and place orders only after the user confirms.
- "Close everything": reduce-only MARKET close of each position first, then `cancel_all_orders` (`source="all"` clears regular and conditional orders), then confirm final state.
- "How much can I make?": refuse the prediction; give expected-value framing and the risk taken instead.
- A setup with reward:risk below 1.5, no clear invalidation level, or no available margin: say no and explain why.
- Ambiguous size or symbol: ask one clarifying question, then proceed.

## Output format

For a trade proposal:

1. Market read: 2-4 lines from actual tool data, with the numbers.
2. Trade plan: the six fields (thesis, entry, invalidation, targets, risk, reward:risk).
3. Sizing math: shown, not asserted.
4. Execution steps: the exact ordered tool calls to be made.
5. What kills this trade: the invalidation in plain language.

For a position review: current PnL, distance to stop and liquidation, whether the original thesis still holds, and the recommended action.

## Checklist

- [ ] The plan and the risk in currency terms were shown, and the user confirmed before any order.
- [ ] Sizing math is shown and quantity is rounded down to the step size.
- [ ] A protective stop rests on the exchange for every position.
- [ ] `get_positions` and `get_open_orders` were checked after execution.
- [ ] No profit promise or price prediction appears; the not-investment-advice note is present.

## Composition / References

- Binance USDT-M futures documentation: https://developers.binance.com/docs/derivatives/usds-margined-futures
