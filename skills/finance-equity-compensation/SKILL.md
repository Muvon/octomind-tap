---
name: finance-equity-compensation
title: "RSU, ISO, NSO & ESPP Taxes: Equity Compensation Rules"
description: "How RSUs, ISOs, NSOs, ESPP shares, 83(b) elections and AMT are taxed in the US, with decision steps and the questions to bring to a CPA."
license: Apache-2.0
compatibility: "US federal rules. Needs web search to confirm current thresholds. Other countries differ; say so."
domains: finance
rules:
  - content(RSU)
  - content(RSUs)
  - content(ISO)
  - content(NSO)
  - content(ESPP)
  - content(83(b))
  - match((?i)stock options?)
  - match((?i)(restricted stock|equity compensation|exercise.{0,20}options))
---

## Overview

Employees at US companies are often paid partly in company stock: restricted stock units (RSUs), incentive stock options (ISOs), nonqualified stock options (NSOs), employee stock purchase plan (ESPP) shares, or restricted stock. Each type is taxed at different moments, and the common mistakes come from mixing them up. This skill gives the taxable events, the forms, and the decisions that need a professional. It teaches the mechanics; it does not prepare a return or say whether to exercise.

## Mental model

Ask three questions for any grant, in this order.

1. What is the type? The plan document and the grant notice name it.
2. When is income recognized: grant, vest, exercise, or sale?
3. Is the income ordinary (taxed like wages, with payroll tax) or capital gain (holding period decides the rate), and does the Alternative Minimum Tax (AMT) apply?

The income at each step is the market value minus what the employee paid. The basis in the shares is what was already taxed plus what was paid.

## Rules

### Taxable events by type

| Type | Grant | Vest | Exercise or purchase | Sale |
|---|---|---|---|---|
| RSU | none | wages equal to the share value when the shares are delivered; payroll tax and withholding apply | not applicable | capital gain or loss from the value at delivery; holding period starts at delivery |
| NSO | none (when no readily determinable value) | none | wages equal to share value minus exercise price; payroll tax and withholding apply | capital gain or loss from the value at exercise |
| ISO | none | none | no regular-tax income; AMT adjustment equal to share value minus exercise price | qualifying sale: all gain is capital; disqualifying sale: ordinary income up to the exercise spread, the rest capital |
| ESPP (qualified plan) | none | none | none at purchase | qualifying sale: ordinary income is the smaller of the grant-date discount or the actual gain; the rest is capital |
| Restricted stock, no 83(b) | none | wages equal to value at vest minus amount paid | not applicable | capital gain or loss from the value at vest |
| Restricted stock, 83(b) | wages equal to value at transfer minus amount paid, if any | none | not applicable | capital gain or loss from the value at transfer; later vesting is not taxed |

Source for the option, ESPP and 83(b) rows: IRS Publication 525 (2025) and Topic 427 (page reviewed 2026-09-24). The RSU row follows from the restricted-property rule in the same publication and from the IRS withholding rules for supplemental wages (Publication 15, 2026).

### ISO rules

- Qualifying sale: sell no earlier than the later of 2 years after the grant and 1 year after the exercise. Missing either date makes it a disqualifying disposition.
- A yearly cap applies to options first exercisable: the part above $100,000 of share value at grant, per calendar year, is treated as an NSO (Treasury Regulation 1.422-4).
- Exercise creates an AMT adjustment on Form 6251, line 2i, equal to the spread. Form 3921 arrives after an ISO exercise and carries the dates and values.
- AMT paid because of an ISO spread can produce a minimum tax credit carried forward on Form 8801.
- AMT exemption figures change yearly; take them from the `finance-tax-year-anchors` skill. For 2026 the exemption is $90,100 single and $140,200 joint, phased out from $500,000 and $1,000,000 of AMT income (IRS, 2025-10-09).
- Exercise-and-hold in a high-spread year is the classic AMT trap: tax is due on paper gain with no cash from a sale. Test the AMT effect with a draft return or software before exercising, not after.

### ESPP rules

- The plan may set the purchase price at no less than 85% of the share value at grant or at purchase (Internal Revenue Code section 423). Many plans use the lower of the two ("lookback").
- A purchase cap of $25,000 of grant-date share value per calendar year applies (section 423(b)(8)).
- Qualifying sale: the later of 2 years after the grant and 1 year after the purchase. Otherwise a disqualifying disposition makes the purchase-date discount (share value at purchase minus price paid) ordinary income, and that amount is added to basis.
- Form 3922 arrives after the first transfer. Check whether the 1099-B basis includes the ordinary income already taxed; if it does not, correct the basis on Form 8949.

### RSU rules

- Employers often sell or withhold shares to cover tax at a flat supplemental rate. For 2026 that rate is 22% on supplemental wages up to $1 million in a calendar year and 37% above it (IRS Publication 15, 2026). The real marginal rate can be higher, so a large vest can leave a balance due. Compare the withholding with a projected return after each vest.
- The 1099-B for a share sale after vest often shows a basis of zero or the wrong amount. Basis is the value taxed at delivery.
- Double-trigger RSUs at private companies vest for tax at the liquidity event, which can produce a large wage bill with shares that cannot yet be sold. Ask for the withholding method and the sale rules before the event.

### 83(b) election

- Filed within 30 days of the transfer of restricted property (written statement or Form 15620). It cannot be revoked without IRS consent, given only for a mistake of fact. It usually cannot be made when an option is granted, because options rarely have a readily ascertainable value; it can be made on the shares when an option is exercised for restricted stock (IRS Publication 525; Revenue Procedure 2012-29).
- It makes sense mainly when the shares are worth little at transfer, because the income recognized is small and later growth is capital gain. Ask a professional what happens to the tax paid if the shares are later forfeited.
- The 30 days run from the transfer date, not the vesting date. If day 30 is a weekend or legal holiday, the next business day counts (Form 15620 instructions, IRC 7503); no other extension. Send a missed 83(b) to a professional at once.

### When to stop and send to a professional

| Situation | Why |
|---|---|
| Exercising ISOs in a year with a large spread | AMT and credit tracking need a return projection |
| Early exercise with an 83(b) | The valuation and deadline have no recovery path |
| Concentrated position or a 10b5-1 sale plan | Legal and insider-trading rules apply |
| Private company liquidity event | Withholding, secondary sales, and tax-year timing interact |
| Qualified small business stock (section 1202) | Eligibility tests are technical |
| Moving countries with unvested grants | Source rules split the income between countries |
| Leaving the company | Post-termination exercise windows are short and written in the grant |

## Examples

Bad: "Your ISOs aren't taxed, so exercise as many as you can."

Good: "Exercising ISOs creates no regular tax, but the spread (share value at exercise minus strike price) is an AMT adjustment on Form 6251, line 2i. For 2026 the AMT exemption for a single filer is $90,100, phasing out from $500,000. With a large spread you can owe AMT on shares you cannot yet sell. Run your numbers through tax software before exercising, and take Form 3921 and your exercise dates to a CPA."

## Checklist

- [ ] The grant type was read from the plan document or grant notice, not assumed.
- [ ] Income, basis and holding-period start were stated for the user's type.
- [ ] Thresholds were taken from a dated source (see the anchors skill) and the tax year named.
- [ ] The RSU or ESPP basis correction on Form 8949 was mentioned where it applies.
- [ ] Any 30-day or exercise-window deadline was named with its start date.
- [ ] The answer ends with the question list for a CPA or Enrolled Agent.

## References

- IRS Topic 427, stock options: https://www.irs.gov/taxtopics/tc427
- IRS Publication 525, statutory stock options and restricted property: https://www.irs.gov/publications/p525
- IRS Form 6251 instructions (ISO adjustment): https://www.irs.gov/instructions/i6251
- IRS Publication 15, supplemental wages: https://www.irs.gov/publications/p15
- Treasury Regulation 1.422-4, ISO $100,000 limit: https://www.law.cornell.edu/cfr/text/26/1.422-4
- Internal Revenue Code section 423, ESPP: https://www.law.cornell.edu/uscode/text/26/423
- Same-domain companions: `finance-tax-year-anchors` skill.
