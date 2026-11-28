---
name: finance-self-employed-tax
title: "Self-Employment Tax: Quarterly Estimated Taxes, QBI"
description: "US self-employment tax, quarterly estimated payments, safe harbor and QBI, plus UK payments on account. Use to size a tax set-aside and a payment calendar."
license: Apache-2.0
compatibility: "US federal and UK rules. Needs web search to confirm current-year figures. Other countries differ; say so."
rules:
  - match((?i)estimated (tax|payment)s?)
  - match((?i)self[- ]employment tax)
  - match((?i)(set aside|set-aside).{0,30}tax)
  - match((?i)payments? on account)
  - match((?i)freelanc)
  - match((?i)quarterly tax)
  - content(1099)
  - content(QBI)
---

## Overview

An employee has tax withheld from each paycheck. A freelancer or sole trader pays the tax in person, on a schedule, and also pays the employee and employer halves of the pension and health payroll taxes. This skill turns "set aside about 25 to 35 percent" into a calculation, a payment calendar and a penalty rule. It teaches the mechanics and prepares the numbers for a professional; it does not prepare a filing.

## Mental model

Three bills arrive from one profit number.

1. Payroll-type tax on the profit: self-employment (SE) tax in the US, Class 4 National Insurance in the UK.
2. Income tax on the profit after deductions.
3. A schedule: tax is due during the year, not only at filing.

The set-aside is the sum of the first two bills divided by profit, not a fixed percentage. The schedule decides how much cash must be held and when.

## Rules

### US: self-employment tax

- Rate 15.3%: 12.4% Social Security plus 2.9% Medicare. The Social Security part stops at a wage base ($184,500 for 2026, IRS page updated 2026-10-30); the Medicare part has no cap.
- Schedule SE applies the rate to net earnings, which are net profit reduced by a factor (0.9235, from the employer-equivalent adjustment; confirm the factor on the year's Schedule SE).
- Net earnings of $400 or more trigger Schedule SE.
- Additional Medicare Tax of 0.9% applies above $200,000 single, $250,000 joint, $125,000 married filing separately (IRS, page updated 2026-10-30).
- The employer-equivalent half of SE tax is an income deduction, not a credit; it lowers income tax only.
- An S corporation owner's pass-through income is not subject to SE tax, but a reasonable salary is payroll. That is entity and payroll territory; send it to a CPA.

### US: estimated payments

| Rule | Detail | Source |
|---|---|---|
| Who pays | Anyone who expects to owe $1,000 or more after withholding and credits | IRS estimated taxes page, 2026-09-25 |
| 2026 due dates | April 15, June 15, September 15 2026, and January 15 2027; a weekend or holiday moves the date to the next business day | Form 1040-ES; Publication 505 (2026) |
| Skipping the January payment | Allowed if the return is filed and the balance paid by the cutoff date in early 2027; take the date from the form for that year | Form 1040-ES |
| Safe harbor, penalty avoided if paid by installment dates | the smaller of 90% of this year's tax or 100% of last year's tax (last year must cover 12 months) | Publication 505 (2026) |
| Higher income | 110% of last year's tax instead of 100% when last year's AGI was over $150,000 ($75,000 married filing separately) | Publication 505 (2026) |
| Uneven income | The annualized income installment method (Form 2210, Schedule AI) can lower early payments for seasonal income | Publication 505 (2026) |

- The safe harbor on last year's tax is the lowest-risk plan: pay one quarter of last year's tax (or 110%) each quarter and the penalty does not apply, even if this year's profit is much higher. The balance is due with the return.
- Payments can go through IRS Direct Pay, the online account, or EFTPS; check the current options on irs.gov.
- A state usually has its own estimated-tax dates and rules; look them up for the user's state.

### US: qualified business income (QBI) deduction

- A deduction of up to 20% of qualified business income, limited by taxable income (IRS QBI page, updated 2026-10-30).
- For tax years beginning after 2025 the law adds a minimum deduction for active qualified business income and widens the phase-in range. The sunset was removed (Public Law 119-21; the permanence is confirmed in secondary summaries).
- Thresholds, the specified-service-business limit and the wage and property limits change each year. Look them up on the Form 8995 instructions for the year; do not quote them from memory.

### US: the set-aside calculation

1. Net profit (income minus ordinary business expenses).
2. SE tax = profit times the Schedule SE factor times 15.3% (up to the wage base for the Social Security part).
3. Income tax base = profit minus half of SE tax minus the standard or itemized deduction minus QBI deduction (if eligible).
4. Income tax on that base from the year's bracket table (use the `finance-tax-year-anchors` skill for the deduction).
5. Add state tax.
6. Set-aside rate = (2 + 4 + 5) divided by profit. Round up; reconcile each quarter.

Illustration (2026 rates, below the wage base, no QBI, no state): profit $80,000 gives net earnings $73,880 and SE tax $11,304; half of that, $5,652, comes off taxable income. The result is an SE-tax-only share of 14.1% of profit before any income tax.

### Information returns

- 1099-NEC and 1099-MISC reporting starts at $2,000 for payments made in 2026; 1099-K starts above $20,000 and 200 transactions on third-party networks (see the anchors skill). The threshold limits forms, not taxability: every dollar of income counts.

### UK: payments on account

- Self Assessment payments on account are two instalments, due by midnight on 31 January and 31 July. Each is usually half of the prior year's bill, including Class 4 National Insurance (gov.uk, Understand your Self Assessment bill).
- No payments on account if last year's bill was under £1,000 or if more than 80% of last year's tax was already paid outside Self Assessment (for example through PAYE).
- The balancing payment is the total owed minus the payments on account, due by midnight on 31 January after the tax year. It can include capital gains tax.
- A drop in profit can justify reducing the payments through the online account or form SA303; if the final bill is higher than expected, interest runs on the difference.
- The first year includes a 31 January bill that is the first-year tax plus the first payment on account, so the cash needed is about 150% of the first-year tax. Plan for that bill before the first return.
- Making Tax Digital for Income Tax changes how records and updates are sent, not how payments on account work. Thresholds and dates are in the anchors skill.
- Class 4 and Class 2 rates and the income tax bands are in the anchors skill under UK, 2026-27.

### Other countries

The same three bills exist almost everywhere (social contribution, income tax, prepayments). Name the country's tax authority page, the prepayment dates, and the penalty rule; do not apply the US or UK numbers.

## Examples

Bad: "Put aside 30% and you will be fine."

Good: "For a US freelancer with $80,000 net profit in 2026, SE tax is about $11,304 (15.3% on $73,880 of net earnings). Income tax then applies to profit minus half of SE tax minus the standard deduction minus any QBI deduction. Add that to the SE tax, add your state's tax, and divide by $80,000 for your set-aside rate. To avoid the penalty, pay at least one quarter of last year's total tax (110% if last year's AGI was over $150,000) by each of April 15, June 15, September 15 and January 15."

## Checklist

- [ ] Country and tax year named; US versus UK rules not mixed.
- [ ] SE tax (or Class 4) and income tax were computed separately and then added.
- [ ] Payment dates were given with the year, plus the safe-harbor choice.
- [ ] A first-year UK taxpayer was warned about the 150% January bill.
- [ ] Figures that change yearly came from the anchors skill or a dated authority page.
- [ ] The answer ends with the questions to bring to a CPA, Enrolled Agent or accountant.

## References

- IRS estimated taxes: https://www.irs.gov/businesses/small-businesses-self-employed/estimated-taxes
- IRS Publication 505 (2026): https://www.irs.gov/publications/p505
- IRS self-employment tax: https://www.irs.gov/businesses/small-businesses-self-employed/self-employment-tax-social-security-and-medicare-taxes
- IRS qualified business income deduction: https://www.irs.gov/newsroom/qualified-business-income-deduction
- gov.uk payments on account: https://www.gov.uk/understand-self-assessment-bill/payments-on-account
- Same-domain companions: `finance-tax-year-anchors` skill.
