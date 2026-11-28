---
name: home-rent-vs-buy
title: "Rent vs Buy: Affordability, Mortgages, Tenant Basics"
description: "Runs rent-vs-buy math, stress-tests affordability, compares mortgages and covers offers, closing and tenant basics. Educational, not licensed advice."
license: Apache-2.0
compatibility: "Needs web access for current local mortgage rates, transaction costs, scheme rules and tenant law."
domains: financial-planner
rules:
  - match((?i)\b(rent\w*|buy\w*)\b.{0,40}\b(vs\.?|versus|or)\b.{0,30}\b(rent\w*|buy\w*)\b|\brent-vs-buy\b|\bkeep renting\b.{0,60}\bbuy\b)
  - match((?i)\b(model|compare|comparison|stress-?test|break-?even|worst-case|decision framework)\b.{0,80}\b(mortgages?|payments?|ownership|afford\w*)\b)
  - match((?i)\b(stress-?test|afford)\w*\b.{0,60}\b(rates?|income|house|home|mortgage|job)\b)
  - match((?i)\b(offer|bid|bidding)\b.{0,40}\b(house|home|flat|listed|market|price|contingenc\w+|earnest)\b|\bopening offer\b|\binspection report\b.{0,80}\bnegotiat\w+)
  - match((?i)\b(bond|deposit)\b.{0,40}\b(landlord|keeping|return\w*|dispute)\b|\blandlord\b.{0,40}\b(bond|deposit)\b|\b(student|new tenant)\b.{0,60}\b(lease|deposit|rental)\b|\bdeposit\s+(protections?|rules)\b)
  - match((?i)\btotal[- ]cost[- ]of[- ]ownership\b|\bclosing (costs?|day)\b|\bpre-approval\b)
  - match((?i)\b(fixed|tracker|offset|adjustable)\b.{0,30}\bmortgages?\b.{0,80}\b(compar\w+|model\w*|lenders?|decision)\b)
  - match((?i)\bmortgage\s+offers?\b|\b(lower|higher)\s+rate\b.{0,60}\bfee\b)
  - semantic(should I rent or buy a home in my situation, 0.74)
  - semantic(can I afford a mortgage on my income and how much down payment)
  - semantic(compare these two mortgage offers and their closing costs, 0.74)
  - semantic(walk me through making an offer and closing on a house, 0.74)
---

## Overview

Use this skill for the largest financial decision most people make: whether to rent or buy, how much home is affordable, which mortgage to take, how to structure an offer, and where a tenant stands. It runs the math with the user's own inputs, stress-tests it, and gives a recommendation with its uncertainty, for any country, anchored to current local numbers. It is educational and on the user's side of the table. It is not licensed agent, mortgage-broker or legal advice, and the local-law layer is always verified locally.

This skill does not value a specific property definitively, rule on contracts or disputes (those go to a qualified lawyer), give regulated mortgage or financial advice, prepare tax filings (a tax professional does), or predict market timing.

## Mental model

Numbers come before feelings on a six-figure decision: run the math, then talk. The framework is universal and the numbers never are, so every rate, cost and rule is looked up for the user's market. Housing markets are not predictable, so a decision must survive being wrong. Pressure tactics ("the market is moving") are not a reason to skip due diligence.

## Rules

Procedure:

1. Situate. Country and city, rent or buy, household income shape, savings, horizon ("how long will you stay?") and what drives the decision. Recall a returning user's situation from memory.
2. Verify the local layer. Search for current mortgage rates, transaction-cost percentages, deposit and loan-to-value norms and tenant-law basics in the user's market; never quote them from memory. Costs of buying range from about 2% to 15% or more of the price by country.
3. Run the math visibly, with their inputs, so they can re-run it when life changes.
4. Stress-test: rates up 2 to 3 points, an income drop, a 10% price fall, a forced sale in year 2. A plan that only works if everything goes right is not a plan.
5. Equip for the professionals: question lists for the agent, lender or broker, surveyor and, for disputes or foreign purchases, the lawyer handoff, plus documents to read when shared.

### Rent vs buy, the honest math

- Price-to-rent ratio: property price divided by annual rent for comparable places. Under about 15 buying looks strong; over about 20 renting the same quality is often financially better. Compute it for their actual candidates.
- Unrecoverable-costs comparison (the "5% rule" pattern): renting costs rent; owning costs property tax, maintenance (about 1 to 2% of value per year) and the cost of capital (mortgage interest and any forgone return on the deposit). Compare rent against that, not against the whole mortgage payment. Principal repayment is forced saving, not a cost, but only if you stay long enough.
- Breakeven horizon: with transaction costs on both ends, buying typically breaks even at about 5 to 7 years (3 to 10 depending on the market). Moving sooner usually makes buying a loss, even in a rising market. Mobility has real value; price it in.
- Lifestyle: buying is also stability, control and roots. Those are legitimate values, priced consciously rather than smuggled in as "rent is throwing money away" (it isn't; so is interest).

### Affordability, stress-tested and not maxed

- Housing at or under about 30% of gross (pre-tax) income is the widespread comfort heuristic; HUD counts a household as cost-burdened above 30% of monthly income, utilities included. Lender caps (debt-to-income patterns like 28/36, or loan-to-income multiples) are ceilings, not targets: the bank's maximum is not your budget.
- Stress-test at rate plus 2 to 3 points and, for couples, after a one-income scenario. Regulators differ. Canada's OSFI qualifies uninsured mortgages at the higher of the contract rate plus 2 points or 5.25% (as of its 2026 page; look up the current figure). The UK withdrew its +3-point affordability test from 1 Aug 2022, although lenders must still consider likely future interest rates over a minimum of five years unless the rate is fixed for five years or more (FCA MCOB 11.6.18 R, handbook.fca.org.uk/handbook/mcob11/mcob11s7, as of 2026-11; look up the FCA's own notice for the withdrawal date). Look up the user's market's rule; don't claim a mandated buffer.
- Total cost of ownership: purchase taxes or duties, notary and legal fees, agent fees, survey and mortgage fees upfront; then insurance, property taxes, maintenance (1 to 2% per year) and strata, HOA or service charges for as long as you own. Search the local percentages and list them.
- Deposit and loan-to-value norms and first-time-buyer schemes vary widely: check the current local programs. Mortgage insurance typically applies below about 20% equity where it exists.

### Mortgage mechanics, universal with local flavor

Amortization: early payments are mostly interest, which matters for breakeven math. Fixed versus variable: fixed-period norms differ hugely (30-year fixes in the US; 2 to 10-year fixes then refinance in much of Europe; floating common elsewhere). Compare the whole term's risk, not the teaser. Name overpayment rights and penalties, refinancing or remortgaging triggers, and negative-equity risk at high loan-to-value for the user's market. Compare offers on the effective annual rate including fees (the APR or APRC pattern), not the headline rate.

- Points or refinance breakeven: months to break even equal upfront cost (points plus closing fees) divided by the monthly payment saving. Compare it with how long the user will keep the loan; if they may move or refinance sooner, it loses.
- US private mortgage insurance (PMI) on conventional loans: the borrower can ask in writing to cancel at 80% of the original value, the servicer must end it automatically at 78% (if payments are current), and at the loan's midpoint at the latest (CFPB). Extra payments can bring the 80% point earlier but not the 78% automatic date.
- US FHA loans: 1.75% upfront mortgage insurance premium plus an annual premium of roughly 0.5% to 0.55% of the loan a year, set by loan size, term and loan-to-value (HUD Mortgagee Letter 2023-05; as of 2026-11, look up the current HUD table before quoting a rate). At 90% loan-to-value or less it ends after 11 years; above 90% it runs the whole term. Compare with conventional PMI, which can be cancelled.
- Adjustable-rate mortgages (ARMs): caps are written initial/periodic/lifetime, for example 5/1/5 means up to 5 points at the first adjustment, 1 point at each later one, 5 points over the life (CFPB). Compute the worst-case payment at the lifetime cap, not just the starting rate.
- Rate lock: ask how long the lock lasts, what it costs and what happens if closing slips past it.

### Offers, inspections, negotiation

- Price from comparables (sold, not asking) and days on market. Over-asked markets and stale listings negotiate differently.
- Never waive the inspection or survey lightly. The local norm differs (US inspection, UK homebuyer or building survey, notary-centric systems elsewhere) but the function is universal: finding the 30,000-euro problem before it is yours. Big findings are negotiation levers or exits, not paperwork.
- Everything is negotiable somewhere: price, fixtures, completion dates, repairs and agent fees. The seller's agent works for the seller. US since the Aug 2024 NAR settlement: buyers sign a written agreement with their agent before touring, which must state the agent's pay; compensation offers no longer appear on the MLS. Buyer-agent pay is negotiated, either paid by the buyer or requested from the seller as a concession in the offer, so model it as a cost line, not a given.
- Selling (orientation, not listing-agent advice): price from sold comparables; compare offers by net proceeds, not headline price: sale price minus mortgage payoff, agent fees, transfer taxes and fees, repair credits and any seller concessions. Check what the local law says a seller must disclose and what contingencies (financing, inspection, sale of the buyer's home) put the sale at risk.
- Closing (US pattern; ask for the local equivalent): earnest money is held in escrow and applied to the price; the title search and title insurance check ownership and liens; the lender must deliver the Closing Disclosure at least 3 business days before closing (12 CFR 1026.19(f)(1)(ii)(A), as of 2026-11; timeshares and a documented personal financial emergency are exceptions). Compare its numbers with the Loan Estimate, ask about any change before signing, and keep funds and ID ready for the closing agent.
- Buying abroad: an independent local lawyer (not the seller's or developer's), foreign-ownership restrictions checked first, currency risk on deposit and mortgage, and tax on both sides. It is always professional-heavy; the job here is orientation and the question list.

### Tenant basics, concepts universal and law local

Deposit: document move-in condition (dated photos, shared in writing). Many countries protect deposits in schemes or escrow; search the user's. Disputes are usually won by whoever documented. Notice periods and rent-increase limits are regulated nearly everywhere, differently: find the local rule and cite it. England changed on 1 May 2026 (Renters' Rights Act 2025): no-fault Section 21 evictions ended, fixed-term tenancies became periodic, and rent rises are limited to once a year through the statutory process; tenant guidance written before then is stale. Repairs: structural and habitability issues are typically the landlord's; report in writing and keep the trail. Escalation: deposit scheme arbitration, rent tribunals, ombudsmen, then a qualified lawyer for real disputes.

Situations:

- "Can I afford this?": run affordability and the stress test with real numbers; answer plainly, including "the bank will say yes but it's tight" when true.
- "Should I buy now or wait?": no market predictions; run rent-vs-buy on today's numbers, name what would change the answer, and decide on horizon and stability.
- Deposit or landlord dispute: document-first triage, the local rule via search, then the lawyer route if real money is involved.
- Listing or contract shared: read it, extract the numbers into the math, flag what needs the professional.
- Missing country or city: ask first; nothing here works without the market.

## Output format

- Decisions: the math shown with their inputs (a table where it helps), the stress-test verdict, and the recommendation with its reasoning and its uncertainty.
- Mortgages: a comparison on effective cost over the realistic horizon, with risks named.
- Tenant issues: their likely position (concept level), the local rule found and cited, the documented next step and the escalation path; a lawyer handoff for disputes.
- Always: numbers dated and sourced ("at current rates of about X%, per [source]"), local currency, and the professional-question list when a professional is next.

## Checklist

- [ ] Country and city are known, and every rate, cost and rule came from a search with a source and date.
- [ ] The math is shown with the user's inputs so it can be re-run.
- [ ] The stress test covers higher rates, an income drop, a price fall and a forced early sale.
- [ ] The lender's maximum was not treated as the budget.
- [ ] No market prediction was made; the plan does not depend on prices rising.
- [ ] Any inspection or survey waiver names what it risks.
- [ ] Disputes, contracts and foreign purchases got a plain lawyer handoff.

## Composition / References

- The `home-repair-diy` skill covers repairs; a tenant's repair request is drafted here, the repair itself there.
- CFPB, HUD, FCA and OSFI pages named in the rules, re-read before quoting a figure.
