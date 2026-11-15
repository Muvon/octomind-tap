---
name: commerce-disputes-returns
title: "Chargeback Response & Return Flow for Online Sellers"
description: "Card dispute reason codes, response deadlines, evidence packs and an RMA flow for online stores. Use when a chargeback arrives or to design returns."
license: Apache-2.0
compatibility: "Needs web access to re-read card network and processor rules. Drafts evidence and recommendations only; the seller submits and refunds."
capabilities: websearch webfetch
domains: commerce
rules:
  - match((?i)\b(charge\s?backs?|disputes?)\b.{0,40}\b(evidence|respond|reason\s+code|deadline|win|lose|visa|mastercard|stripe|paypal)\b)
  - match((?i)\b(reason\s+code|rma|return\s+merchandise|friendly\s+fraud|compelling\s+evidence|vamp)\b)
  - match((?i)\bpayment\s+disputes?\b)
  - match((?i)\bcharge\s?backs?\b)
---

## Overview

A chargeback is a refund forced by the buyer's bank. The seller loses the sale amount and a dispute fee at once, and the card networks count every dispute against the store, win or lose. This skill sorts a dispute by its reason code, gives the evidence that answers that code, lists the deadlines and monitoring thresholds, and sets out a return flow that prevents disputes. It drafts and recommends. The seller submits evidence and issues refunds.

The figures come from Stripe's dispute documentation and the networks' programs as Stripe reports them, read on 2026-11-15. Other processors differ in deadlines and evidence formats, so ask which processor handles the payment and read its page.

## Mental model

The bank reviewer reads thousands of cases and checks one thing: does the evidence answer this reason code? Evidence for another claim is noise. Disputes are also counted when received, not when won, so prevention (clear terms, tracking, fast refunds) beats a good response.

## Rules

### Match reason code to evidence

| Claim | Visa | Mastercard | Evidence that answers it |
|---|---|---|---|
| Fraud, card not present | 10.4 | 4837 | Prior undisputed orders from the same customer with matching device, IP, account and shipping details (Visa Compelling Evidence 3.0); AVS and CVC results; 3D Secure result; delivery to the billing address; signed delivery for high-value goods |
| Not received | 13.1 | 4855 | Carrier tracking showing delivery, the full delivery address (not only city and postal code), signature or photo where available, the shipping promise shown at checkout |
| Not as described or defective | 13.3 (also 13.4 counterfeit, 13.5 misrepresentation) | 4853 | The listing as shown at purchase, photos before shipment, return policy and proof it was shown, correspondence where the buyer did not return the item or refused an offered fix |
| Credit not processed | 13.6 (13.7 canceled merchandise or services) | 4860 | Proof that the refund was issued with date and amount, or the policy that makes the item ineligible with proof the buyer accepted it |
| Canceled recurring | 13.2 | 4853 | Proof of agreement to the billing terms, the reminder sent, the cancellation record or its absence |
| Duplicate | 12.6.1 (12.6.2 paid by other means) | 4834 | Two receipts showing separate orders, or the refund of the duplicate |

Visa 10.x and Mastercard 4837 are the fraud codes where proving the cardholder authorised the order is the whole case. For every other code, authorisation is not in dispute and the argument is delivery, description or refund.

### Deadlines and monitoring

- Window to file: card networks typically allow the cardholder 120 days from the payment; some situations allow more, and for events or future services the window can start on the event date.
- Time to respond: usually 7 to 21 days after the dispute, depending on the network. A missed deadline loses the case automatically.
- Time for the bank to decide: usually 60 to 75 days; the whole case takes 2 to 3 months.
- Respond to an inquiry or early fraud warning at once. An unanswered inquiry can turn into a dispute that cannot be won.
- One submission only. No edits or extra files after submitting. Build the full pack first.
- Visa VAMP (disputes plus fraud reports over captured payments, monthly), as listed in Stripe's documentation of the card network programs (read the network's current rules): non-compliant at a ratio of 0.5% with a count of 5; excessive at 1.5% and 1,500 in the US, EU, Canada, Asia-Pacific and Latin America. Disputes resolved by pre-dispute tools or qualifying under Compelling Evidence 3.0 are excluded from the count.
- Mastercard Excessive Chargeback Merchant: 100 to 299 chargebacks and 1.5% to 2.99% of the prior month's payments; High Excessive at 300 or more and 3%. Fines start in the second month.
- Refunding before a dispute does not remove it from the network count when the bank still raises it.

### Build the evidence pack

1. Open with a two-sentence summary that quotes the claim and states why the evidence refutes it: customer, product, order date, ship date, delivery date and proof.
2. Order evidence by time. Group receipts, shipping, communications, policy and system logs.
3. Combine items of one evidence type into a single file. Format: PDF, JPEG or PNG; combined size no more than 4.5 MB; fewer than 50 pages, and no more than 19 pages for Mastercard cases; 12-point text or larger.
4. Use only relevant excerpts, such as the cancellation clause, not the whole terms. No links, audio or video: the reviewer will not open them.
5. Do not edit fields that the processor pre-filled for a Compelling Evidence 3.0 response.
6. Decide first whether to fight. Compare the amount with the dispute fee and the cost of the pack. Accept when the claim is valid or the amount is small. Accepting does not remove the dispute fee, and it still counts toward the networks' ratios.

### Return (RMA) flow

| Step | Rule |
|---|---|
| Request | Buyer states order number, reason, photos for damage. Reply the same working day with the next step |
| Authorise | Issue an RMA number only when the item is inside the window the store published and the law allows no better terms; consumer-law minimums come from the store's policy, not this flow |
| Ship back | Label paid by the party the policy names; tracking required |
| Inspect | Record condition with photos on arrival; same checklist for every return |
| Resolve | Refund, exchange or partial refund by the published rule. Refund to the original payment method |
| Close | Restock or write off; log the reason code so repeated defects reach the supplier |

Timing floors for refunds: the US FTC Mail, Internet, or Telephone Order Rule requires a refund within seven working days after an order is cancelled for most payment methods. In the EU and UK, the buyer's withdrawal right for distance sales is 14 days (UK: 12 months if the seller did not tell the buyer about it). Policy wording and other legal minimums belong to the store policy drafter.

### Friendly fraud and repeat claimants

Keep a record per customer of orders, refunds and disputes. A pattern is a reason to require signature, verify the address, or decline the next order; the record is not a reason to accuse. Send the legitimate customer a refund or fix before the dispute when the claim is valid.

## Examples

- Wrong: send the full terms of service against a "not received" claim. Right: tracking showing delivery on 3 May to the full address, plus the order confirmation with the promised date.
- Wrong: "The customer is lying." Right: "Order placed 2 May from IP 203.0.113.9, the same IP and device as undisputed orders on 4 Jan and 12 Feb; shipped to the same address; delivered 5 May, tracking attached."
- Wrong: fight a $12 dispute with a three-hour pack. Right: accept it, refund the pattern at the source, and log the cause.

## Checklist

- [ ] Reason code read from the dispute, not guessed from the buyer's words.
- [ ] Evidence matches the code; every item is dated and readable.
- [ ] Deadline noted; pack submitted once, complete.
- [ ] Decision to fight or accept recorded with the cost comparison.
- [ ] Refund or exchange issued by the seller, not by this skill.
- [ ] Cause logged: supplier, listing, carrier or fraud.

## Composition / References

- Related skill: `commerce-marketplace-ops` for marketplace account metrics.
- [Stripe: dispute categories and reason codes](https://docs.stripe.com/disputes/categories)
- [Stripe: respond to disputes](https://docs.stripe.com/disputes/responding)
- [Stripe: how disputes work](https://docs.stripe.com/disputes/how-disputes-work)
- [Stripe: dispute evidence best practices](https://docs.stripe.com/disputes/best-practices)
- [Stripe: card network monitoring programs](https://docs.stripe.com/disputes/monitoring-programs)
- [FTC: Mail, Internet, or Telephone Order Merchandise Rule](https://www.ftc.gov/business-guidance/resources/business-guide-ftcs-mail-internet-or-telephone-order-merchandise-rule)
- [GOV.UK: online and distance selling](https://www.gov.uk/online-and-distance-selling-for-businesses)
