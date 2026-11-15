---
name: commerce-marketplace-ops
title: "Marketplace Seller Ops: Amazon, Etsy, eBay, TikTok Shop"
description: "Account health targets, fee stacks, suspension appeals and fulfilment choices for Amazon, Etsy, eBay and TikTok Shop sellers. Use for marketplace issues."
license: Apache-2.0
compatibility: "Needs web access to read each marketplace's current seller documentation. Proposes and drafts only; the seller submits appeals and changes."
capabilities: websearch webfetch
domains: commerce
rules:
  - match((?i)\b(amazon|etsy|ebay|tiktok\s+shop)\b.{0,50}\b(suspen\w*|deactivat\w*|account\s+health|appeal\w*|fees?|fba|fbm|policy|violation\w*)\b)
  - match((?i)\b(fba|fbm|seller\s+central|account\s+health|plan\s+of\s+action|offsite\s+ads|seller\s+level|top\s+rated)\b)
  - match((?i)\bmarketplace\s+(fees?|seller|account|suspension)\b)
---

## Overview

A marketplace seller has three recurring problems: the account is at risk, the fees eat the margin, or the seller must choose who ships. This skill gives the health targets that trigger action, the fee stack of each marketplace, a structure for an appeal, and a way to choose between self-shipping and a fulfilment program. It advises and drafts. The seller submits appeals, changes prices and edits listings.

Every figure below was read on the marketplace's own page or announcement on 2026-11-15. Marketplaces change fees and thresholds without notice, so read the current page before any calculation and tell the seller the date of the page you read.

## Mental model

The marketplace owns the customer relationship and the rulebook. Your margin is the sale price minus the fee stack, shipping, returns and ad spend. Your account is a standing permission that the marketplace can remove when a metric crosses a line. So work in this order: protect the account, then compute the real margin, then choose fulfilment.

## Rules

### Account health targets (as of 2026-11)

| Marketplace | Metric and target | What a miss costs |
|---|---|---|
| Amazon | Order defect rate under 1% (60-day window, 14-day delay); late shipment rate under 4% (10-day and 30-day windows); pre-fulfilment cancel rate under 2.5% (7-day window). Shipping metrics cover seller-fulfilled orders only | Account health rating below 100 makes the account eligible for deactivation. Account Health Assurance extends the time to fix an issue; an Amazon moderator's forum post gave 250 or more held six months and 3 to up to 13 days, which Amazon's help pages did not confirm, so read the seller's own Account Health page |
| eBay (US) | Transaction defect rate up to 2% and no more than 2 cases closed without seller resolution (or 0.3% of transactions) in an evaluation period; Below Standard only if defects involve more than 4 different buyers. Evaluated on the 20th of each month | Lower search placement, possible lower selling limits, no Promoted Listings, possible funds holds, possible higher final value fees from the next month |
| eBay Top Rated (US) | Defect rate 0.5% or less across no more than 3 buyers; late shipment no more than 5 orders or 3%; tracking uploaded and carrier-validated on at least 95%; 100 transactions and $1,000 US sales in 12 months | Loses the status when a target is missed |
| TikTok Shop (US) | Account health rating with escalating enforcement steps; point steps (150, 100, 50, 0) and fund holds (45, 90 or 365 days) were read from TikTok's page in 2026-10 and not re-checked, so read the live Seller Center policy | Escalating enforcement; funds can be withheld depending on the violation |
| Etsy | Read the Etsy seller policy and the shop's own dashboard; no numeric target was confirmed on Etsy's pages | Unverified. Ask the seller for the notice text |

### Fee stack (as of 2026-11)

| Marketplace | Fees read on the marketplace's page |
|---|---|
| Amazon US | Individual plan $0.99 per item sold; Professional plan $39.99 per month. Referral fee is a percentage of the sale price or a per-item minimum, whichever is higher: 8% to 15% in the categories listed (Home and Kitchen and Toys 15%; Computers and Consumer Electronics 8%; Beauty 8% up to $10 and 15% above; $0.30 minimum). Media items add a $1.80 closing fee. FBA fees are on a separate Amazon page |
| Etsy | $0.20 per listing; 6.5% transaction fee on the order total including shipping and gift wrap; US payment processing 3% plus $0.25 on the gross order; Offsite Ads 15% of the order total (12% once the shop has sold $10,000 or more in the past 365 days), capped per order (a $100 cap was reported; read Etsy's fees page for the current cap); 2.5% currency conversion when currencies differ |
| eBay US | Final value fee 13.6% on the sale total up to $7,500 per item and 2.35% above that, in most categories; per-order fee $0.30 for orders of $10 or less and $0.40 above; first 250 listings per month free, then $0.35 each |
| TikTok Shop US | Referral fee 6% per qualified order (5% to 6% by category) on the last official fee page found, updated 2025-05-08. On a refund the referral fee is returned minus a fee of 20% of it, capped at $5 per SKU. Read the live Seller Center table: the last official page found predates 2026 |

Worked example, Etsy US, a $30 order with free shipping: listing $0.20 + transaction $1.95 + processing $0.90 + $0.25 = $3.30, which is 11.0% of the order. If the sale came from an Offsite Ad at 15%, add $4.50, for $7.80 or 26.0%. Cost of goods, postage, packaging and returns come on top. Build the floor price from the full stack, not from the headline percentage.

### Suspension and violation appeals

1. Read the notice and copy the exact policy name, the affected listings or orders, and the deadline. TikTok Shop states windows: first appeal within 30 days of notification, a second within 15 days of a rejection, two appeals per violation; immediate actions and corrections run on 12 to 72 hours.
2. Find the root cause in the seller's own data: which orders, listings or supplier caused it. A cause such as "carrier delay" needs tracking proof; a cause such as "supplier changed the item" needs the supplier message.
3. Draft the appeal in three parts: what went wrong and why (the root cause), what was fixed for the affected orders or listings (corrective action), and what now prevents a repeat (preventive action, with a date). Use the sections the marketplace's own notice asks for if they differ.
4. Attach only evidence the notice asks for: invoices, tracking, photos, supplier documents. Don't invent documents, pressure buyers to change feedback, or open a second account to keep selling; each breaks marketplace rules and weakens the appeal.
5. Keep one thread per case. Record each submission with date and reference number.

### Fulfilment choice

| Situation | Lean toward |
|---|---|
| Amazon seller with fast-moving, small, standard-size items and no packing capacity | Amazon-fulfilled (FBA): Amazon-fulfilled orders do not count in the seller's shipping metrics, and the FBA fee goes into the floor price |
| Large, slow-moving, fragile or made-to-order goods | Seller-fulfilled: storage and fulfilment fees can exceed the margin; shipping metrics then apply |
| Etsy handmade goods | Seller-fulfilled; the buyer's handling-time expectation is part of the listing |
| Multi-channel stock | One stock count across channels, so a sale on one never leaves a promise open on another |

For any fulfilment program, ask the seller for last quarter's units, average sale price, weight and size, then compute margin per unit with the current program fees before recommending a switch.

## Examples

- Wrong: "Etsy takes about 6.5%." Right: "$30 order, free shipping: $3.30 in fees (11.0%), $7.80 (26.0%) if it came from an Offsite Ad. Read on Etsy's fee pages 2026-11-15."
- Wrong: "Amazon says your account is fine." Right: "Late shipment rate 4.7% over 30 days against a target under 4%; 14 of 301 orders shipped late, all from one supplier. Draft the appeal around that supplier."
- Wrong appeal: "We apologise and promise to do better." Right appeal: root cause with order numbers, the corrective action already done, a preventive step with a date.

## Checklist

- [ ] Every target and fee has a page and a date from this session, or is marked unverified.
- [ ] Margin is computed per unit from the full fee stack, shipping and returns.
- [ ] The appeal names the root cause, the corrective action and the preventive action, with evidence the notice asked for.
- [ ] No step involves a second account, review manipulation or invented documents.
- [ ] Nothing was submitted, repriced or edited without the seller's yes.

## Composition / References

- Related skill: `commerce-disputes-returns` for chargebacks and return handling.
- [Amazon selling plans and referral fees](https://sell.amazon.com/pricing)
- [Amazon Seller Forums: account health targets, posted by Amazon staff](https://sellercentral.amazon.com/seller-forums/discussions/t/f360047c-af63-4910-a37a-e26df9b14b45)
- [Etsy: fees and taxes for selling](https://help.etsy.com/hc/en-us/articles/115014483627-What-are-the-Fees-and-Taxes-for-Selling-on-Etsy)
- [Etsy: payment processing fees](https://help.etsy.com/hc/en-us/articles/115015628847-What-are-Payment-Processing-Fees-for-Selling-on-Etsy)
- [eBay: selling fees](https://www.ebay.com/help/selling/fees-credits-invoices/selling-fees?id=4822)
- [eBay: seller standards policy](https://www.ebay.com/help/policies/selling-policies/seller-standards-policy?id=4347)
- [TikTok Shop: referral fee updates, last updated 2025-05-08](https://seller-us.tiktok.com/university/essay?knowledge_id=5982454398175018&lang=en)
- [TikTok Shop: seller enforcement policy, last updated 2026-10-09](https://seller-us.tiktok.com/university/essay?knowledge_id=2380042836166443)
