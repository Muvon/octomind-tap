---
name: vehicle-buying
title: "Car Buying Guide – Out-the-Door Price, Loans & Leases"
description: "Car purchase steps: price research, out-the-door math, loan and lease terms, as-is and warranty basics, lemon-law pointers. Use when buying or leasing."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
capabilities: webfetch
rules:
  - match((?i)\b(out[- ]the[- ]door|trade[- ]?in|lemon law|car loan|auto loan|lease deal|money factor|residual value|dealer fees?|extended warranty|service contract)\b)
  - match((?i)\b(buy(ing)? a (new |used )?car|lease (a|or) (new |used )?car|lease vs\.? buy|financ(e|ing)( a)? car)\b)
  - match((?i)\b(monthly payment|[0-9]+ months?)\b.*\b(car|dealer|lease)\b)
  - match((?i)\b(car|auto|vehicle) (financing|price|deal|purchase)\b)
  - match((?i)\b(negotiat\w+|pay for) .{0,20}(car|dealer)\b)
---

## Overview

This skill covers the money side of getting a car: what it should cost, what the final bill is made of, how a loan or lease is priced, and what the warranty paperwork means. Use it when someone is shopping, comparing offers or reading a dealer quote. The outcome is a price target, a side-by-side of offers on the same basis, and a list of questions to ask. It does not inspect a specific car (the used-car inspection guide does that), and it gives orientation, not financial or legal advice.

## Mental model

A dealer quote is several numbers at once: the car's price, the trade-in's value, the financing and the add-ons. Mixed together, a good number in one hides a bad number in another. Pull them apart, negotiate the car's price first, then compare offers by the total out-the-door amount and the total paid over the term.

## Rules

### Price research

- Collect asking prices for the same make, model, year, trim and similar mileage within driving distance, from at least three sources (dealer listings, independent listings, an independent price guide). Record the date and URL of each.
- For used cars, use sold or advertised-for-weeks prices over asking prices when the source shows them. Note how long each car has been listed.
- Check the manufacturer's current incentives and any recall notices by VIN with the national regulator before settling on a car.
- Ask for the price in writing, as an itemized quote.

### Out-the-door math

Out-the-door price = vehicle price + sales tax + title and registration fees + dealer documentation fee + any add-ons the buyer accepts - rebates - trade-in credit.

| Check | Pass | Fail |
|---|---|---|
| Quote is itemized line by line | Every line has a name and an amount | A single monthly payment or a bundle of unnamed fees |
| Taxes and government fees | Match the state or country's published rates (look them up) | Rounded or unexplained |
| Dealer documentation fee | Disclosed in writing; compared with other dealers | Added after agreement |
| Add-ons (paint protection, etching, service contracts, GAP cover) | Each is optional, priced separately, and can be declined | Pre-installed or described as required |
| Trade-in | Valued separately from the new price; the buyer has an outside offer to compare | Value moves when the price moves |

- If the buyer owes more on the trade-in than it is worth (negative equity), the FTC warns that dealers may add the shortfall to the new loan. Show the effect: the new loan then exceeds the new car's price.
- The FTC advises checking the trade-in's value before dealing.

### Loan terms

- Compare loans by APR, term in months, total interest and total paid, not by monthly payment. A longer term lowers the payment and raises total interest.
- Get a pre-approval from a bank or credit union before visiting a dealer; the dealer's financing then has to beat a known number.
- Monthly payment for a fixed-rate loan: payment = P x r / (1 - (1 + r)^-n), where P is the amount financed, r is the monthly rate (APR / 12) and n is the number of months. Show the working so the buyer can re-run it.
- Ask about any prepayment penalty and whether extra payments reduce principal.

### Lease terms

- A lease charges for the car's expected loss in value over the term, plus a rent charge, taxes and fees (FTC). Monthly payment is roughly (negotiated price - residual value) / months + (negotiated price + residual value) x money factor + taxes and fees.
- Residual value is the lessor's estimate of the car's worth at lease end. It sets the payment, so ask for it in writing and compare it across offers.
- Money factor x 2,400 = the equivalent APR (CFPB). Ask for the money factor, not just the payment.
- Negotiate the car's price (the capitalized cost) the same way as for a purchase; the lease price is negotiable.
- Add the end-of-term costs: mileage allowance and per-mile charge, wear-and-tear terms, disposition fee, and early-termination cost.
- Lease vs buy: compare the total cost over the years the buyer expects to keep a car, including what the owned car is worth at the end.

### Warranty and lemon-law orientation

- US dealers must show an FTC Buyers Guide on each used car, stating whether it is sold "as is" or with a warranty. In an "as is" sale the dealer does not pay for repairs after the sale. Any verbal promise should be written on the Guide; if the Guide and the contract conflict, the Guide controls (FTC).
- Implied warranties (an unwritten promise of reasonable quality) are set by state law; most states let a dealer disclaim them with "as is", some restrict that, and a service contract bought from the dealer within 90 days can keep them alive for the covered systems (FTC). A private sale is usually "as is".
- Read a manufacturer warranty for: what is covered, years and miles, whether the clock started when the car was first sold, what voids it and whether it transfers to a second owner.
- Service contracts are sold insurance-like products: ask who pays claims, what the deductible is, what is excluded, and whether it is cancellable for a refund.
- Lemon laws are state or national laws that give a remedy for a new car with repeated unfixed defects. Terms, time limits and which cars count differ by place. Look up the state attorney general's or consumer office's lemon-law page, keep every repair order, and note dates.
- Where legal questions go: whether a contract is enforceable, whether a defect qualifies under a lemon law, title disputes and insurance coverage questions are for a consumer lawyer, the state attorney general's consumer office, or the legal domain through the global assistant. Say so plainly and do not rule on them.

## Examples

Bad: "The dealer says $489 a month for 84 months. That's fine."
Good: "$489 x 84 = $41,076 paid. The car is $31,500 out the door, so the loan costs $9,576 in interest and fees at that APR. Get a 60-month quote from a credit union and compare total paid, not the payment. Ask the dealer to quote the price first, then the financing."

Bad: "Sign the lease; the money factor is probably fine."
Good: "Ask for the money factor and the residual in writing. A money factor of 0.0020 is 4.8% APR (0.0020 x 2,400). Compare it with a purchase loan at the same date."

## Checklist

- [ ] Price comparables come from at least three sources, each with date and URL.
- [ ] The quote is itemized and every add-on is shown as optional.
- [ ] Trade-in, price and financing were compared separately.
- [ ] Offers are compared by out-the-door price and total paid, not monthly payment.
- [ ] Money factor and residual value were requested in writing for any lease.
- [ ] The Buyers Guide or warranty terms were read, and as-is limits explained.
- [ ] Legal questions were pointed to the right place, not decided here.

## Composition / References

- For one specific used car, hand the walk-through to the used-car inspection guide; this skill stays on money and paperwork.
- FTC, buying a used car from a dealer: https://consumer.ftc.gov/articles/buying-used-car-dealer
- FTC, financing or leasing a car: https://consumer.ftc.gov/financing-or-leasing-car
- FTC, trade-ins and negative equity: https://consumer.ftc.gov/articles/auto-trade-ins-and-negative-equity-when-you-owe-more-your-car-worth
- CFPB, leasing versus buying: https://www.consumerfinance.gov/ask-cfpb/what-should-i-know-about-leasing-versus-buying-a-car-en-815/
