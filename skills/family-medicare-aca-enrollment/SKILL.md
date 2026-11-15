---
name: family-medicare-aca-enrollment
title: "Medicare & ACA Open Enrollment: Plan Comparison"
description: "Medicare and ACA open-enrollment dates, official plan finders, drug-list plan comparison, Medicaid retroactive and renewal changes, screening limits."
license: Apache-2.0
compatibility: "Requires: web search and web fetch for the official plan finders and state pages. US only; figures change yearly."
domains: family
rules:
  - content(open enrollment)
  - content(Medicare Advantage)
  - content(Part D)
  - content(marketplace plan)
  - content(healthcare.gov)
  - content(retroactive coverage)
  - content(Medicare plan)
  - content(ACA)
  - content(Obamacare)
  - content(Extra Help)
  - match((?i)(compare|choose|pick).*(medicare|marketplace|aca) plan)
---

## Overview

Two enrollment windows decide a household's health coverage for the next year: the ACA marketplace and Medicare's annual election. The agent prepares the comparison and the user enrolls. Figures below are as of 2026-11; look up the current value before relying on any of them.

## Mental model

A plan is cheapest or best only against a specific person: their drugs, their doctors, their income. So collect those three inputs first, run the official finder with them, and compare total yearly cost, not the monthly premium alone.

## Rules

Dates (check the official page; state-run marketplaces set their own)

| Program | Window | Source |
|---------|--------|--------|
| HealthCare.gov, plan year 2027 | November 1, 2026 to January 15, 2027 | CMS, 2026-10-30 |
| State-run marketplaces | Dates vary by state; some end earlier or later than HealthCare.gov | The state exchange |
| Medicare annual election (join, drop or switch Medicare Advantage or a drug plan) | October 15 to December 7; coverage starts January 1 | Medicare.gov |
| Medicare Advantage open enrollment (already in a Medicare Advantage plan) | January 1 to March 31: switch Medicare Advantage plans or return to Original Medicare with a drug plan | Medicare.gov |

A rule that would have shortened HealthCare.gov open enrollment to nine weeks was vacated (KFF, 2026-11-06). If a marketplace page shows an earlier deadline, trust the page and say so.

ACA subsidies

- The enhanced premium tax credits expired at the end of 2025; above 400% of the federal poverty level there is no premium tax credit, and the finalized average benchmark premium rose 13% for 2027 (KFF, 2026-11-06). Run HealthCare.gov's estimate with the user's projected income for the coverage year, not last year's.
- Cost-sharing reductions apply to household income up to 250% of the federal poverty level, only on silver plans: the lower the income, the larger the reduction. HealthCare.gov's estimate shows whether a silver plan carries one.

Medicare plan comparison, steps

1. List every drug with dose and form, and the pharmacy used. Enter all of them in Medicare Plan Finder (Medicare.gov/plan-compare); Medicare says this gives a more accurate yearly cost estimate.
2. List the doctors and hospitals the person must keep. Check each plan's network.
3. Compare Original Medicare plus a drug plan against Medicare Advantage plans by total estimated yearly cost: premium plus estimated drug cost plus out-of-pocket maximum exposure.
4. Check that each drug is on the plan's formulary and note any prior authorization or step therapy.
5. Help with Medicare Savings Programs and Extra Help (below) before the person picks a drug plan.
6. Offer free one-to-one counseling from the State Health Insurance Assistance Program (SHIP), which is not connected to any insurance company or health plan.

Licensed-broker line

You compare and organize; you do not recommend a specific plan as the best choice, sell, or enroll anyone. For a personal recommendation, point to SHIP or a licensed broker or agent, and tell the user the finder's result is theirs to act on.

Medicare Savings Programs and Extra Help (2026 monthly income and resources; states may use higher limits)

| Program | Pays | Individual | Couple |
|---------|------|------------|--------|
| QMB | Part A premium if any, Part B premium, deductibles, coinsurance | $1,350 / $9,950 | $1,824 / $14,910 |
| SLMB | Part B premium | $1,616 / $9,950 | $2,184 / $14,910 |
| QI | Part B premium | $1,816 / $9,950 | $2,455 / $14,910 |

Apply through the state Medicaid office, even when the person thinks they may not qualify. QMB, SLMB and QI recipients also get Extra Help with prescription drug costs; QI must be reapplied for every year (Medicare.gov).

Medicaid changes with dates

- Retroactive coverage: today Medicaid can cover up to three months before the application month. From January 2027, P.L. 119-21 shortens it to two months before the application month for most applicants and one month for adults in the expansion group. Mention it whenever medical bills exist; apply early.
- Six-month renewals: expansion adults renew every six months for renewals on or after January 1, 2027 (CMS SMD 26-001); states choose whether to re-date everyone or apply it at each person's 2027 renewal, and state plan amendments are due March 31, 2027. Look up the state's choice and put both dates on the calendar.
- Work requirement: CMS interim final rule CMS-2454-IFC (Federal Register, 2026-06-03); comments closed 2026-07-31 and no final rule was found as of 2026-11-15. Check for one.

Stable screening tests (check the current year)

| Test | Figure | Source |
|------|--------|--------|
| Medicaid expansion adults 19-64 | Income up to 138% of the federal poverty level, in states that expanded | HealthCare.gov |
| SSI countable resources | $2,000 for one person, $3,000 for a couple (2026) | SSA |
| SSDI cash wait | Five full consecutive calendar months of disability, counted from the first month in which the person is insured and disabled (as of 2026-11) | 20 CFR 404.315 |
| Medicare after SSDI | Medicare Part A starts with the 25th month of disability benefit entitlement, that is, after 24 months of benefits (as of 2026-11); ALS and end-stage kidney disease have their own Medicare rules, so look them up | 42 CFR 406.12 |

## Examples

Bad: "The Plan X premium is $0, so it is best."
Good: "Entered your 4 drugs and pharmacy in Plan Finder: Plan X totals about $A a year including drugs, Plan Y $B. Plan X does not list your cardiologist. Verify both on Medicare.gov before December 7, or talk to your SHIP counselor, free."

## Checklist

- [ ] Drug list, doctors and income collected before comparing.
- [ ] Deadline stated with its source and as-of date.
- [ ] Total yearly cost compared, not premium alone.
- [ ] Savings programs and Extra Help screened.
- [ ] SHIP or a licensed broker named for the final choice.
- [ ] Anything not verified is marked "verify with the agency".

## References

- Medicare enrollment periods: https://www.medicare.gov/basics/get-started-with-medicare/get-more-coverage/joining-a-plan
- Medicare Savings Programs: https://www.medicare.gov/basics/costs/help/medicare-savings-programs
- CMS plan year 2027 fact sheet (2026-10-30): https://www.cms.gov/newsroom/fact-sheets/plan-year-2027-marketplace-plans-prices-fact-sheet-0
- KFF, 9 things to watch for 2027 (2026-11-06): https://kff.org/affordable-care-act/9-things-to-watch-for-the-2027-aca-open-enrollment-period/
- Medicaid expansion: https://www.healthcare.gov/medicaid-chip/medicaid-expansion-and-you/
- Medicaid work requirement rule: https://www.federalregister.gov/documents/2026/06/03/2026-11094/medicaid-program-community-engagement-requirement-for-certain-individuals
- Retroactive coverage change (CMS summary of P.L. 119-21): https://www.medicaid.gov/medicaid/downloads/wftc-legsltn-overview-slide.pdf
- Six-month renewals (CMS SMD 26-001, 2026-03-06): https://www.medicaid.gov/federal-policy-guidance/downloads/smd26001.pdf
- SSDI waiting period: https://www.ecfr.gov/current/title-20/part-404/section-404.315
- Medicare entitlement of disabled people: https://www.ecfr.gov/current/title-42/part-406/section-406.12
