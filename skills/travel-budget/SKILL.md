---
name: travel-budget
title: "Trip Budget Planner – Per-Day and Per-Person Costs"
description: "Trip budget planner in one currency: fares, stays, food, activities, fees, exchange rates, per-day totals, contingency. Use when asked what a trip costs."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
capabilities: webfetch
domains: travel
rules:
  - content(budget)
  - content(afford)
  - content(cost)
  - content(costs)
  - match((?i)\bhow much (will|would|does|is)\b.*\b(cost|trip|holiday|vacation)\b)
  - match((?i)\b(per day|daily allowance|exchange rate|make it cheaper)\b)
---

## Overview

This skill turns one trip's transport, stays, meals, activities and unavoidable fees into an honest total and a usable daily allowance. It starts from the itinerary already in the session when one exists and asks only for what is missing. When it is active, its cost table replaces the session's simple budget table. The outcome is a reconciled budget in one stated currency with the gap or headroom against the traveler's ceiling.

## Mental model

Research current prices rather than dressing remembered numbers as quotes. Show quantity times unit price, not just "mid-range". Treat the spending ceiling as a hard constraint, not a target to exhaust. An unavailable quote is a gap, not permission to invent one. This is spending plan work: the traveler decides what to spend and makes every purchase.

## Rules

### Workflow

1. Intake: take destinations, dates, bases and activities from the itinerary in the session. Ask only for what is missing: nights and travel days, party composition, origin, travel style, booked costs, budget ceiling and reporting currency.
2. Research: use web search and `knowledge(command="read", source="<url>")` to check date- and party-matched transport fares, accommodation rates, representative menus, activity tickets and official fee schedules.
3. Normalize: record the checked date, original currency, pricing unit, inclusions, cancellation conditions and availability caveats, then convert using a cited current exchange rate.
4. Calculate: multiply explicit quantities by unit rates, separate fixed trip costs from daily costs, and build transport, stays, food, activities, fees and contingency subtotals.
5. Reconcile: cross-check quantities, nights versus days, shared versus per-person costs, currency conversions, category sums and the daily average against the grand total.
6. Deliver: show the spending gap or headroom, offer concrete cuts if needed, and list unresolved quotes or fees the traveler must verify before booking.

### Pricing rules

- Cite source URLs and verification dates beside prices and exchange rates. Don't invent prices, specifications, laws or references.
- Prefer direct operators, accommodation sites, current menus, and official attraction or government pages. Compare like-for-like rates, not a headline fare against an all-in price.
- Label each line as already booked, live quote or modeled estimate. Show the assumptions behind estimates, and don't describe a search snippet or inaccessible checkout as a confirmed payable total.
- If exact-date pricing is unavailable, use a clearly labeled comparable-date range or leave the line unquoted. Don't silently substitute a different season or occupancy.
- Include baggage, seat or reservation charges, transfers, local transport, parking or tolls where relevant, lodging taxes, cleaning or resort fees, service charges and applicable official entry fees. Flag unknowns rather than setting them to zero.
- Avoid double counting included breakfasts, prepaid activities, shared rooms, deposits or return fares. Distinguish total trip cost from remaining cash needed.
- State currency with an unambiguous code such as USD or EUR throughout. Retain original-currency figures and the conversion date, and distinguish reference rates from card or cash exchange costs.
- Use the actual trip's spending days as the denominator. Show the total-trip average per day and per person separately from the on-the-ground daily allowance.
- Add a separately visible 10-15% contingency unless the user specifies another amount, and explain its basis. Show low, base and high estimates when uncertainty materially changes affordability.
- This is travel cost planning, not financial advice. Don't recommend borrowing, guarantee affordability, pick insurance products, or determine legal eligibility for exemptions or visas.
- Booking, buying and paying stay draft-only until the user explicitly approves.

### Output shape

- Budget frame: dates, days and nights, party, style, currency, ceiling and assumptions.
- Cost table: category or item, quantity, unit price and currency, converted subtotal, evidence status, source and checked date.
- Totals: transport, stays, food, activities, fees, contingency, grand total, and remaining amount after prepayments.
- Daily view: all-in per-day total, per-person-per-day total and local daily spending allowance, with denominators stated.
- Trade-offs: overage or headroom, highest-impact cuts, and the effect on comfort or flexibility.
- Before booking: missing quotes, exchange-rate caveats, fee checks and direct research links.

### Running without a human

- Chatting directly: if a material gap remains after reading the session, ask one focused question, then proceed with labeled assumptions.
- Brief marked AUTONOMOUS or non-interactive: ask nothing and skip confirmations. State the currency and trip assumptions, deliver a provisional budget, and make missing quotes explicit.
- In both modes, an unquoted line stays visible as a gap; it is never filled with an invented number.

## Examples

Bad: "Can we do this for 3,000 EUR?" answered with "Yes, easily" and a mid-range total.
Good: test the ceiling against researched costs and say plainly when the evidence does not support it, with the gap in EUR and the lines that drive it.

Bad: "Make it cheaper" answered with a vague tip list and a new total with no basis.
Good: change the largest flexible category first, quantify the saving, and don't pretend a quote is locked.

Bad: "Hotel: 600" with no nights, currency, date or source.
Good: "6 nights x 100 EUR = 600 EUR, live quote, taxes excluded (flagged), source URL, checked on the stated date."

## Checklist

- [ ] One currency code is used throughout, with original-currency figures and the conversion date kept.
- [ ] Every price and exchange rate has a source URL and a checked date.
- [ ] Every line is labeled booked, live quote or modeled estimate.
- [ ] Each cost line shows quantity times unit price.
- [ ] Category sums, grand total and daily averages reconcile, with denominators stated.
- [ ] Contingency is shown as its own line with its basis.
- [ ] Fees, taxes and baggage or transfer costs are included or flagged, not set to zero.
- [ ] Gap or headroom against the ceiling is stated, with cuts if over.
- [ ] Unresolved quotes are listed under Before booking.

## Composition / References

- Starts from the itinerary in the session; pairs with `travel-packing` for luggage costs and `travel-road-trip` for fuel, charging and tolls.
- Sources are direct operator and accommodation pages, current menus, official attraction and government fee schedules, and a cited exchange-rate source.
