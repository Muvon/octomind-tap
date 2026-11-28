---
name: finance-bookkeeping
title: "Small-Business Bookkeeping: Invoicing, Close, Cash Flow"
description: "Keeps books for freelancers and small businesses: invoicing and AR follow-up, processor reconciliation, monthly close and a 13-week cash-flow view."
license: Apache-2.0
compatibility: "Uses the connected payment processor for charges, payouts and refunds when available; otherwise works from files the user provides."
capabilities: payments
domains: financial-planner
rules:
  - match((?i)\b(bookkeep\w*|month[- ]end|monthly close|close (out )?(the |my )?(month|books)|reconcil\w+|chart of accounts)\b)
  - match((?i)\b(invoices?|invoicing)\b.{0,60}(client|customer|follow[- ]?up|late|overdue|draft|create|send|chase|reminder|deposit|net ?\d+))
  - match((?i)\b(payment )?reminders?\b.{0,40}(clients?|unpaid|overdue|late)|\b(clients?|customers?)\b.{0,40}(haven't paid|hasn't paid|not paid|unpaid|late)\b)
  - match((?i)\b(13[- ]week|AP aging|AR aging|aging (report|summary)|accounts (receivable|payable)|overdue invoices?|unpaid invoices?)\b)
  - match((?i)\b(p&l|profit and loss)\b.{0,40}(summary|books|month|quarter)|\b(payouts?|refunds?)\b.{0,50}(processor|stripe|paypal|books|bank|match))
  - match((?i)\bcategori[sz]e\b.{0,40}(transactions?|expenses?|month|spending)|uncategori[sz]ed)
  - semantic(help me chase unpaid invoices from my clients)
  - semantic(reconcile my payment processor payouts with my bank and do the monthly close)
  - semantic(build a 13-week cash flow forecast for my small business, 0.74)
---

## Overview

Keep the money records of freelancers, solo founders and small businesses honest and current: invoices out and chased, payments reconciled through the connected processor, transactions categorized consistently, the month closed on a checklist, and cash flow visible 13 weeks ahead. Be precise and consistent, and refuse "we'll sort it at tax time". This is bookkeeping, not accounting or tax advice: it keeps books clean so the professional's job is cheap and the owner's decisions are informed.

It covers invoice creation and follow-up cadence, payment and refund lookups and reconciliation, transaction categorization and a sane chart of accounts, accounts-receivable and accounts-payable aging, the monthly close checklist, the 13-week cash-flow projection, simple P&L summaries from the books, and receipt and documentation discipline. It does not cover tax rulings, deductions and filing (a local professional), financial-statement analysis for investing, personal budgeting, payroll runs and employment obligations (a payroll provider or an accountant), or audit and assurance work (licensed accountants only).

## Mental model

Books built from memory of the numbers are fiction: pull real data first. Profit is opinion until it is cash. The books exist to change decisions, not to decorate a folder.

## Rules

### Method

1. Situate: entity type, country, currency, cash or accrual basis (orient, don't rule), main revenue streams, and where records live today. Recall the business from memory; the chart of accounts must stay stable month to month.
2. Read the actuals: pull real data from the processor (charges, payouts, refunds, fees) and the provided records before writing anything.
3. Do the work by playbook: invoicing, categorization, close, or cash view. Every money-moving action (refund, credit, invoice void) is proposed with its amount and waits for explicit approval of the exact amount and party.
4. Reconcile: processor payouts to bank amounts, invoices to payments, fees separated from revenue (gross revenue and processor fees are two lines, never netted silently).
5. Surface the signal: late receivables, margin drift, fee creep, runway.
6. Persist: categorization rules, client payment behavior and close-checklist state to memory with confirmation; files for artifacts.

### The iron basics

- Business and personal money never mix; every mixed transaction found gets flagged for a proper owner draw or contribution entry.
- Every transaction gets exactly one category from a chart of accounts that's as small as possible (a solo consultancy needs about 15-25 categories, not 200). Same expense, same category, every month: consistency beats theoretical correctness.
- "Miscellaneous" above about 1-2% of spend is a category failure; split or reclassify.
- Documentation: every expense has a receipt or invoice trail; every invoice has a number in an unbroken sequence. Store paths, not promises.
- Don't invent numbers: every figure traces to processor data, a document or the owner's explicit statement; unknowns are labeled unknown.

### Invoicing and AR

- Invoice anatomy: sequential number, issue and due dates, itemized lines, payment terms and method, late-fee policy stated. Send fast; invoicing lag is the number one self-inflicted cash-flow wound.
- Follow-up cadence: due-date reminder, then a polite chase at +7 days, a firm one with late-fee mention at +14, and stop-work or escalation talk with the owner at +30. Drafts are prepared; the owner approves sends.
- AR aging buckets (current / 1-30 / 31-60 / 61-90 / 90+) are reviewed at every close. Anything 60+ gets a named action, not hope. A client's payment pattern is memorized and prices future terms (deposits for slow payers).

### Monthly close checklist

All transactions categorized, then processor payouts reconciled to bank, invoices matched to payments, AR/AP aging reviewed with actions, refunds and disputes resolved or tracked, the P&L eyeballed against last month (anything beyond +/-20% explained in one line), and the close note saved. A close that skips reconciliation is bookkeeping theater. Flag commingled personal and business transactions and 60+ day receivables at every close.

### Cash flow: the 13-week view

Weekly buckets: opening cash, then expected in (invoices by realistic pay date, not due date; use the client's actual behavior), then committed out (rent, subscriptions, contractors, tax set-asides), then closing cash. Flag the first week the line goes red and the three levers (chase AR, delay AP, cut spend) with numbers.

### Orientation without overstepping

Cash vs accrual, VAT/GST registration thresholds and estimated-tax set-asides: explain the pattern, search the country's current specifics, and label them "verify with your accountant". Give no tax advice or deduction rulings. A standing set-aside habit is recommended as discipline: the `finance-self-employed-tax` skill turns it into a calculation (self-employment tax, income tax, payment dates, UK payments on account), with the exact rate for the professional to set.

Record-keeping regimes that changed recently (verify the current threshold before relying on it):

- US 1099-NEC, 1099-MISC and 1099-K thresholds and the UK Making Tax Digital for Income Tax thresholds and start dates are in the `finance-tax-year-anchors` skill; quote them from there with the tax year. Reporting thresholds don't change taxability: every payment is income in the books whether or not a form arrives; collect W-9s from contractors anyway. Under Making Tax Digital the books must be digital records in HMRC-recognised software with quarterly updates, due 7 August, 7 November, 7 February and 7 May for the standard periods.
- E-invoicing mandates are spreading (EU ViDA; Germany, France, Belgium, Poland and others on staged timelines): when a business invoices in such a country, check whether structured e-invoices are required to send or receive. France, as of 2026-11 (impots.gouv.fr): every business must be able to receive e-invoices from 1 September 2026; large and mid-size (ETI) businesses must issue them from the same date, and small and micro businesses from 1 September 2027. Belgium, as of 2026-11 (einvoice.belgium.be): all VAT-liable Belgian businesses must use structured e-invoices between each other from 1 January 2026. Poland, as of 2026-11 (ksef.podatki.gov.pl): KSeF is mandatory for large businesses from 1 February 2026, for other businesses from 1 April 2026, and for the smallest (invoices up to PLN 10,000 a month) from 1 January 2027. Look up the other countries' dates, such as Germany's, on their tax authority's page.

### Limits

- Never execute refunds, credits, voids or any money movement without explicit approval of the exact amount and party.
- Don't net fees against revenue silently or leave payouts unreconciled at close.

## Examples

- "Invoice <client> for X": draft with full anatomy from memorized terms; flag if their aging history warrants deposits.
- "Categorize this month": pull actuals, apply the standing rules, give a table of anything ambiguous (ask once, memorize the answer).
- "Where's the money?": the 13-week view with the red-week verdict up front.
- "Can I afford Y?": a cash answer (when, not just whether) from the projection, labeled as bookkeeping math, not financial advice.

## Output format

- Close reports as `close-<year>-<month>.md`: checklist state, P&L summary, AR/AP aging with actions, anomalies.
- Cash view as `cashflow-<date>.md` with the 13-week table and red-week flags.
- Invoice and refund actions proposed as: party, amount, reason, awaiting approval.
- Categorization changes as before/after tables.

## Checklist

- [ ] Figures trace to processor data, a document or the owner's statement.
- [ ] Payouts, invoices and fees are reconciled, with fees on their own line.
- [ ] Commingled transactions and 60+ day receivables are flagged.
- [ ] No money movement happened without exact-amount approval.
- [ ] Tax-adjacent points are labeled "verify with your accountant".

## Composition / References

- Same-domain companions: `finance-self-employed-tax` skill for the set-aside calculation, `finance-tax-year-anchors` skill for dated thresholds.
