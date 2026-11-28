---
name: finance-statement-analysis
title: "Financial Statement Analysis: Ratios, DCF, Red Flags"
description: "Interprets financial statements, computes ratios, explains valuation methods such as DCF and comps, and spots red flags. Education, not investment advice."
license: Apache-2.0
compatibility: "Uses market-data tools for quotes and fundamentals and web search for filings; check material figures against the filing itself."
capabilities: market-data
rules:
  - match((?i)\b(analy[sz]e|read|interpret|explain|break down|review).{0,40}(balance sheet|income statement|cash flow statement|10-?k|10-?q|earnings (report|call)|financial statements?|annual report))
  - match((?i)\b(DCF|discounted cash flow|WACC|EV/EBITDA|comparable companies|valuation multiples?|sum of the parts)\b)
  - match((?i)\b(free cash flow|interest coverage|current ratio|quick ratio|return on equity|ROIC|gross margin|operating margin|P/E ratio)\b)
  - match((?i)\bred flags?\b.{0,40}(financials?|accounting|earnings|10-?k|balance sheet|company))
  - match((?i)(is|are).{0,30}(this |the )?(company|stock|shares?).{0,30}(overvalued|undervalued|fairly valued|worth)|fair value of)
  - semantic(read this balance sheet and income statement and tell me the red flags, 0.72)
  - semantic(calculate the financial ratios for this company)
  - semantic(explain how a DCF valuation or comparable company analysis works, 0.74)
---

## Overview

Interpret and analyze company financials: explain statements and ratios, analyze a company from several angles, compare companies within an industry, spot trends and red flags, explain valuation methodologies and interpret earnings reports. This is educational analysis, not investment advice: it does not recommend securities, predict prices, give personalized financial guidance or guarantee outcomes; those belong to a licensed advisor. Personal-finance coaching (budgeting, debt, saving) is a different topic.

## Mental model

Analyze from evidence, not speculation. Base conclusions on the data, weigh multiple perspectives, compare to industry, history and peers, focus on material items, and question data quality. Financials can contain errors and past performance doesn't predict future results, so never rely on a single data point.

## Rules

### Company analysis

1. Business model: how the company makes money.
2. Competitive advantage: moat, differentiation.
3. Management quality: track record, alignment.
4. Financial health: balance sheet strength.
5. Profitability: margins, returns.
6. Growth: revenue and earnings trajectory.
7. Risks: key risk factors.

### Industry analysis

1. Market size: TAM, growth rate.
2. Competition: concentration, intensity.
3. Regulation: regulatory environment.
4. Trends: technology, consumer behavior.
5. Cyclicality: economic sensitivity.

### Valuation methods

1. DCF (discounted cash flow):
   - Free cash flow to the firm = operating profit after tax + depreciation and amortization - capital expenditure - increase in net working capital. Stock-based compensation counts as a cost.
   - Discount rate (WACC) = E/(D+E) x cost of equity + D/(D+E) x cost of debt x (1 - tax rate). Cost of equity by CAPM = risk-free rate + beta x equity risk premium; look up the current risk-free rate and state every input.
   - Terminal value by perpetual growth = final-year FCF x (1 + g) / (WACC - g), with g no higher than long-run nominal growth of the economy, or by an exit multiple. Report the terminal value as a share of enterprise value; when it dominates, say the answer rests on the terminal assumption.
   - Bridge from enterprise value to equity: equity value = enterprise value - net debt - minority interest - preferred stock - pension deficit + non-operating assets; divide by diluted shares, not basic.
   - Show a sensitivity table of value against WACC and g, never a single point.
   - Sanity checks: the exit multiple implied by the perpetual-growth value against peer multiples; growth against reinvestment (g is about reinvestment rate x return on invested capital); forecast margins against the company's history.
2. Comparable companies (relative valuation): choose peers by business model, growth, margin and size. Match the multiple to what it measures: EV/EBITDA and EV/Sales divide an enterprise value; P/E and P/B divide an equity value. Use the median, keep trailing and forward consistent, strip one-offs, and align lease treatment (see reporting standards below).
3. Precedent transactions (M&A multiples): these include a control premium, so they read higher than trading multiples; use deals from a comparable point in the cycle.
4. Sum of parts (segment valuation): value each segment on its own multiple, subtract unallocated corporate cost and net debt, and flag any holding-company discount.

Use the market-data tools (`yahoo_quote`, `yahoo_quote_summary`, `yahoo_stock_history`, `yahoo_chart`, `yahoo_search`) for quotes, fundamentals, historical prices and company info. Treat their fundamentals as a convenience feed and check material figures against the filing itself (SEC EDGAR 10-K/10-Q/8-K, or the issuer's annual report outside the US). Use web search for company news, industry analysis, economic data and regulatory filings.

### Balance sheet (financial position)

| Component | What it shows | Key metrics |
|-----------|---------------|-------------|
| Assets | What the company owns | Current ratio, quick ratio |
| Liabilities | What the company owes | Debt-to-equity, interest coverage |
| Equity | Owners' residual interest | ROE, book value per share |

### Income statement (profitability)

| Component | What it shows | Key metrics |
|-----------|---------------|-------------|
| Revenue | Top-line sales | Revenue growth rate |
| COGS | Cost of goods sold | Gross margin |
| Operating expenses | SG&A, R&D, D&A | Operating margin |
| Net income | Bottom-line profit | Net margin, EPS |

### Cash flow statement (liquidity)

| Component | What it shows | Key metrics |
|-----------|---------------|-------------|
| Operating CF | Cash from operations | Free cash flow |
| Investing CF | Capital expenditures | CapEx ratio |
| Financing CF | Debt/equity changes | Dividend payout ratio |

### Profitability ratios

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Gross margin | (Revenue - COGS) / Revenue | Efficiency of production |
| Operating margin | Operating Income / Revenue | Core business profitability |
| Net margin | Net Income / Revenue | Overall profitability |
| ROE | Net Income / Equity | Return to shareholders |
| ROA | Net Income / Assets | Asset efficiency |
| ROIC | NOPAT / Invested Capital | Capital efficiency |

### Liquidity ratios

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Current ratio | Current Assets / Current Liabilities | Short-term solvency |
| Quick ratio | (Current Assets - Inventory) / Current Liabilities | Immediate liquidity |
| Cash ratio | Cash / Current Liabilities | Cash coverage |

### Leverage ratios

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Debt-to-equity | Total Debt / Equity | Financial leverage |
| Debt-to-assets | Total Debt / Total Assets | Asset financing |
| Interest coverage | EBIT / Interest Expense | Debt servicing ability |

### Valuation ratios

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| P/E | Price / EPS | Earnings valuation |
| P/B | Price / Book Value | Asset valuation |
| P/S | Price / Revenue | Sales valuation |
| EV/EBITDA | Enterprise Value / EBITDA | Operating value |
| PEG | P/E / Growth Rate | Growth-adjusted valuation |

### Efficiency ratios

| Ratio | Formula | Interpretation |
|-------|---------|----------------|
| Asset turnover | Revenue / Assets | Asset utilization |
| Inventory turnover | COGS / Inventory | Inventory efficiency |
| Receivables turnover | Revenue / Receivables | Collection efficiency |
| Days sales outstanding | 365 / Receivables Turnover | Collection period |

### Red flags

- Balance sheet: high and growing debt, declining current ratio, large goodwill relative to assets, off-balance-sheet liabilities, receivables growing faster than sales.
- Income statement: declining margins, revenue growth without profit growth, large one-time gains, rising SG&A as a percentage of revenue, unusual expense categorization.
- Cash flow: negative operating cash flow, operating cash flow below net income (quality issue), consistent negative free cash flow, financing cash flow exceeding operating.
- Governance: related-party transactions, auditor changes, insider selling, complex structure, limited disclosure.
- Adjusted metrics: "adjusted EBITDA" that excludes recurring costs, stock-based compensation treated as non-cash and ignored (it is real dilution; check share-count growth), and free cash flow that skips lease payments or capitalized software.

### Reporting standards in transition (check which basis a filing uses)

- IFRS 18 replaces IAS 1 for annual periods beginning on or after 1 January 2027: mandatory operating-profit subtotal, operating/investing/financing categories in the income statement, and management-defined performance measures disclosed and reconciled in the audited notes. 2026 comparatives get restated, so IFRS margins can shift without the business changing.
- US GAAP: ASU 2024-03 requires disaggregating expense captions (inventory purchases, employee compensation, D&A) in the notes for public business entities' annual periods beginning after 15 December 2026 and interim periods within annual periods beginning after 15 December 2027 (as amended by ASU 2025-01; as of 2026-11, fasb.org), a new source for cost-structure analysis. ASU 2023-07 already expanded segment expense disclosure.
- Leases sit on the balance sheet under both ASC 842 and IFRS 16; IFRS EBITDA excludes all lease cost while US GAAP operating leases keep it in operating expense. Adjust before comparing EV/EBITDA across the two.

### Limits

- Don't recommend specific investments, predict prices or guarantee outcomes.
- Don't give personalized financial advice: analyze and interpret only.
- Verify figures across sources.

## Examples

- A ticker or company: pull the financials, compute the material ratios, compare to peers and history, and flag risks.
- A statement or ratio: explain what it measures and how to read it in context.
- "Should I buy X?": analyze the fundamentals and risks; the buy/sell decision and personal suitability aren't part of the answer.

## Output format

Scale to the question: lead with the direct answer, and include the sections below only when they change what the user should do, or on request. The disclaimer stays one line; deadlines and red flags always appear when present.

1. Brief disclaimer: one line, then content.
2. Direct answer: clear, concise analysis.
3. Key metrics: relevant ratios and figures.
4. Context: industry and historical comparison.
5. Trends: direction and trajectory.
6. Risks: key risk factors.
7. Questions to consider: what to investigate further.

## Checklist

- [ ] The answer states up front that it is educational analysis, not investment advice, and points to a licensed advisor for decisions.
- [ ] Material figures were checked against the filing, not only the data feed.
- [ ] Valuation shows every input and a sensitivity range, not one point.
- [ ] Peer, history and accounting-basis differences are noted.
- [ ] No price prediction or recommendation appears.

## Composition / References

- SEC EDGAR for US filings: https://www.sec.gov/edgar
