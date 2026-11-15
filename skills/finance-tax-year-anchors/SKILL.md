---
name: finance-tax-year-anchors
title: "401(k), IRA & Standard Deduction Limits by Tax Year"
description: "Dated US and UK figures by tax year: contribution limits, deductions, 1099 thresholds, UK rates and allowances. Use to quote or check a limit."
license: Apache-2.0
compatibility: "Needs web search or fetch to confirm a year not listed. Works offline for the listed years."
domains: finance
rules:
  - match((?i)(401\(?k\)?|\bira\b|\bhsa\b).{0,40}(limit|max|cap|contribut))
  - match((?i)(limit|max|cap|contribut).{0,40}(401\(?k\)?|\bira\b|\bhsa\b))
  - match((?i)\bquarterly (update|deadline)s?\b)
  - match((?i)standard deduction)
  - match((?i)(isa|personal) allowance)
  - match((?i)1099-(nec|k|misc))
---

## Overview

Contribution limits, deductions and thresholds change every year. This skill holds them once, in one table per tax year, each row with its source and the date it was checked. Agents name this skill instead of copying figures. The table was last checked on 2026-11-15; the UK change rows for the cash ISA limit and savings and property income rates were read in the gov.uk Budget 2026 document (published 2026-10-28).

## Mental model

A figure is only true for a named tax year. Each row below is one year of one jurisdiction. A year with no row is a year to look up, not a year to estimate. A projection published by a payroll vendor or a benefits firm is not an official figure and must be labeled as a projection.

## Rules

- Name the tax year and the source with every figure you quote.
- If the user's year has no row, search the tax authority for the current figure and say it is newly found.
- A figure marked "secondary" was confirmed in several reputable summaries but not read on the authority's own page; say so, and point to the authority page.
- Rows marked "look up" have no official figure as of the check date. Do not fill them from last year plus a guess.
- Statutory (not indexed) amounts such as the HSA catch-up are stated once and do not change with the year.

### US, tax year 2026

| Item | Figure | Source |
|---|---|---|
| 401(k), 403(b), 457(b) employee deferral | $24,500 | IRS IR-2025-111, 2025-11-13 |
| Catch-up, age 50+ / ages 60-63 | $8,000 / $11,250 | IRS IR-2025-111 |
| Roth-only catch-up if prior-year FICA wages from that employer exceeded | $150,000 | IRS Notice 2025-67; final regulations T.D. 10033 |
| IRA, plus catch-up age 50+ | $7,500, plus $1,100 | IRS IR-2025-111 |
| HSA self-only / family, plus age 55+ | $4,400 / $8,750, plus $1,000 | Rev. Proc. 2025-19 (secondary) |
| HDHP minimum deductible / out-of-pocket maximum (self-only; family) | $1,700; $3,400 / $8,500; $17,000 | Rev. Proc. 2025-19 (secondary) |
| Standard deduction single / married joint / head of household | $16,100 / $32,200 / $24,150 | IRS IR-2025-103, 2025-10-09 |
| AMT exemption single / joint; phase-out starts | $90,100 / $140,200; $500,000 / $1,000,000 | IRS IR-2025-103 |
| Estate basic exclusion; annual gift exclusion | $15,000,000; $19,000 | IRS IR-2025-103 |
| Foreign earned income exclusion; health FSA | $132,900; $3,400 | IRS IR-2025-103 |
| SALT deduction cap (half for married filing separately) | $40,400, reduced above $505,000 MAGI, floor $10,000, back to $10,000 from 2030 | IRS 2026 Form 1040-ES correction; 2026 Schedule A draft |
| Qualified tips deduction; overtime deduction | up to $25,000; up to $12,500 ($25,000 joint), phase-out above MAGI $150,000 ($300,000 joint) | IRS FS-2025-03, 2025-07-25 |
| Senior deduction (age 65+); car-loan interest | $6,000 each, phase-out above MAGI $75,000 ($150,000 joint); up to $10,000, phase-out above $100,000 ($200,000 joint) | IRS FS-2025-03 |
| Years the four deductions above apply | 2025 through 2028 | IRS FS-2025-03 |
| Form 1099-NEC / 1099-MISC reporting threshold | $2,000 for payments made in 2026, indexed from 2027 | IRS Publication 1099 (2026) |
| Form 1099-K threshold | over $20,000 and over 200 transactions (third-party networks) | IRS 1099-K FAQs |
| Social Security wage base; self-employment tax rate | $184,500; 15.3% | IRS self-employment tax page, updated 2026-10-30 |
| One-time federal deposit for a child born 2025-2028 (Form 4547 election) | $1,000 | IRS Form 4547 instructions, 12/2025 |

### US, tax year 2027

| Item | Figure | Source |
|---|---|---|
| Standard deduction single / married joint / head of household | $16,600 / $33,200 / $24,925 | IRS IR-2026-133, 2026-11-05 |
| AMT exemption single / joint; phase-out starts | $93,000 / $144,700; $515,950 / $1,031,900 | IRS IR-2026-133 |
| Estate basic exclusion; annual gift exclusion | $15,480,000; $20,000 | IRS IR-2026-133 |
| Foreign earned income exclusion; health FSA | $137,300; $3,500 | IRS IR-2026-133 |
| HSA self-only / family; HDHP out-of-pocket maximum | $4,500 / $9,000; $8,700 / $17,400 | Rev. Proc. 2026-24 (secondary) |
| 401(k) deferral, catch-ups, IRA, Roth catch-up wage threshold | look up: no official IRS notice found as of 2026-11-15; published numbers are projections | irs.gov newsroom, retirement cost-of-living notice |
| SALT cap, QBI thresholds, Social Security wage base | look up | irs.gov |

### UK, tax year 2026-27 (6 April 2026 to 5 April 2027)

| Item | Figure | Source |
|---|---|---|
| Personal allowance; taper | £12,570; falls £1 for each £2 of adjusted net income over £100,000, nil at £125,140 | gov.uk income-tax-rates |
| Basic / higher / additional rate bands (England, Wales, Northern Ireland) | 20% to £50,270; 40% to £125,140; 45% above | gov.uk income-tax-rates |
| Threshold freeze | personal allowance, higher-rate and additional-rate thresholds frozen until April 2031 | gov.uk Budget 2025 |
| Dividend allowance; dividend rates basic / higher / additional | £500; 10.75% / 35.75% / 39.35% | gov.uk tax-on-dividends |
| ISA allowance | £20,000 | gov.uk individual-savings-accounts |
| Class 4 National Insurance | 6% on profits £12,570 to £50,270, 2% above | gov.uk self-employed NI rates |
| Class 2 National Insurance | treated as paid at profits of £7,105 or more | gov.uk self-employed NI rates |
| Making Tax Digital for Income Tax | from 6 April 2026 if qualifying income (self-employment plus property turnover, before expenses) over £50,000 | gov.uk MTD pages, updated 2026-10 |
| Making Tax Digital for Income Tax quarterly update deadlines (standard periods) | 7 August, 7 November, 7 February, 7 May | gov.uk send quarterly updates |

### UK, dated changes after 2026-27

| Date | Change | Source |
|---|---|---|
| 6 April 2027 | Making Tax Digital threshold £30,000 (judged on 2025-26 qualifying income) | gov.uk MTD guidance |
| 6 April 2027 | Cash ISA limit: the planned cut to £12,000 for under-65s was dropped; the cash ISA limit stays £20,000 for all ages | gov.uk Budget 2026 document, 2026-10-28 |
| 6 April 2027 | Most unused pension funds and death benefits count in the estate for Inheritance Tax; personal representatives report and pay | gov.uk Inheritance Tax unused pension funds |
| 6 April 2027 | Savings and property income tax rates rise by 2 percentage points at the basic, higher and additional rate, on top of the 2-point rise announced in Budget 2025: 24% / 44% / 49% on the 20 / 40 / 45% base. Confirm the legislated rates and which nations apply (property: England, Wales and Northern Ireland) on gov.uk | gov.uk Budget 2025 and Budget 2026 document, Table 6.1, 2026-10-28 |
| 6 April 2028 | Making Tax Digital threshold £20,000 (judged on 2026-27 qualifying income) | gov.uk MTD guidance |
| 6 April 2029 | Employee pension contributions through salary sacrifice above £2,000 a year lose the National Insurance exemption | gov.uk salary sacrifice reform |

The pension Inheritance Tax, salary sacrifice and threshold-freeze rows come from gov.uk pages and the Budget 2025 documents; the Budget 2026 document was not read for them, so confirm them on gov.uk before quoting.

### Adding a year

- Add a new table for the year when the authority publishes its notice: IRS newsroom and the cost-of-living notice for retirement limits; gov.uk rates and allowances pages for the UK.
- Keep the prior year's table until its filing deadline has passed.
- Update the check date in Overview.

## Examples

Bad: "The 401(k) limit is $25,500 next year." This is a projection, not an official figure.

Good: "For 2026 the 401(k) deferral limit is $24,500 (IRS, 2025-11-13). The IRS had not published the 2027 limit when this table was last checked on 2026-11-15; check irs.gov before planning around a number."

## Checklist

- [ ] Every figure quoted carries a tax year and a source.
- [ ] A year without a row was looked up on the authority's page, not guessed.
- [ ] Rows marked secondary or look up are labeled as such in the answer.
- [ ] UK figures name the nation when Scotland differs (Scotland sets its own income tax bands).

## References

- IRS newsroom: https://www.irs.gov/newsroom
- IRS Notice 2025-67 (2026 retirement limits): https://www.irs.gov/pub/irs-drop/n-25-67.pdf
- IRS tax year 2027 inflation adjustments, IR-2026-133: https://www.irs.gov/newsroom/irs-releases-tax-inflation-adjustments-for-tax-year-2027-taxpayers-continue-to-benefit-from-the-working-families-tax-cuts
- IRS Publication 1099: https://www.irs.gov/publications/p1099
- gov.uk income tax rates: https://www.gov.uk/income-tax-rates
- gov.uk Making Tax Digital for Income Tax thresholds: https://www.gov.uk/guidance/find-out-if-and-when-you-need-to-use-making-tax-digital-for-income-tax
- Same-domain companions: `finance-self-employed-tax` skill, `finance-equity-compensation` skill.
