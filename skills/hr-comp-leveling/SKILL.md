---
name: hr-comp-leveling
title: "Job Levels, Pay Bands & Offer Math for HR"
description: "Builds job levels, pay bands, benchmarks and offer packages, with US pay-transparency posting rules by state. Use for pay structure or offer questions."
license: Apache-2.0
compatibility: "Needs web access for current pay-transparency and overtime rules. Market pay data comes from a survey or source the user supplies; it is never invented."
capabilities: websearch
domains: hr
rules:
  - match((?i)\b(pay|salary|compensation)\s+(bands?|ranges?|transparency|benchmark\w*|structure|grades?)\b)
  - match((?i)\b(job|career)\s+(architecture|levels?|leveling|levelling|ladder|framework)\b)
  - match((?i)\b(compa[- ]?ratio|range\s+penetration|offer\s+(letter\s+)?(math|package|comp\w*)|total\s+(comp|compensation))\b)
  - match((?i)\bflsa\b.{0,30}\bexempt\w*\b)
  - match((?i)\bsalary\s+range\b.{0,40}\b(posting|job\s+ad|job\s+description)\b)
---

## Overview

A small company usually sets pay one offer at a time, and the results drift: two people in the same role earn different amounts for no recorded reason. This skill builds the structure that prevents that: job families and levels, a pay band per level, a market benchmark behind each band, and a method for pricing an offer inside it. It also lists the pay-transparency rules that decide whether a band must appear in a job posting. It structures decisions. It does not state market pay without a source, and it does not rule on the law.

## Mental model

Pay has three layers that must not be mixed. The level says how big the job is. The band says what the company pays for that size, from the market. The individual's place in the band says what this person's skills and track record add. Pay equity problems come from skipping the first two layers.

## Rules

### Job architecture

1. List jobs as families (for example Engineering, Customer Support, Finance) and levels inside each family. Keep to the number of levels the headcount can support: a ten-person company needs three or four, not nine.
2. Write one level guide per family. Each level gets the same four tests: scope (what the person owns), autonomy (who decides), complexity (how unclear the problems are) and impact (what changes if they succeed). A level description states what the person does today, not what they hope to do.
3. Title follows level. Gender-neutral titles, no inflated titles as a substitute for pay.
4. Map every current employee to a level from the guide, in a meeting with the manager. Record the evidence for each placement.

### Benchmark and build the band

1. Ask the user for the data source: a compensation survey, a vendor dataset or published ranges for comparable roles. Don't use remembered figures. Record source, date, region, company size and the percentile pulled.
2. Choose the pay position as a policy: the percentile of the market the company wants to pay (for example the 50th, or the 75th for hard-to-fill roles). Write it down.
3. Set the band around that figure:
   - Midpoint = the market figure at the chosen percentile for the level.
   - Spread = (max minus min) divided by min. The user chooses the spread; there is no published standard.
   - Min = midpoint divided by (1 + spread/2). Max = min times (1 + spread).
   - Example arithmetic only: midpoint 100,000 and spread 40% give min 83,333 and max 116,667.
4. Check overlap: the max of one level should sit above the min of the next so a strong person at one level can out-earn a weak one at the next, but a midpoint step of under about 10% between levels makes levels meaningless. Both numbers are conventions, not rules; test against the data.
5. Adjust by location only as a written policy: one geographic differential per zone, from a stated source, applied to every employee in that zone.

### Measure where people sit

| Measure | Formula | Reading |
|---|---|---|
| Compa-ratio | pay divided by band midpoint | Below 0.90 or above 1.10 needs a recorded reason |
| Range penetration | (pay minus min) divided by (max minus min) | Shows room left to grow |
| Pay gap by group | average (or median) pay of one group divided by another, inside the same level | Large gaps inside one level need an explanation based on objective criteria |

The 0.90 and 1.10 flags are working conventions. Set the flags in the policy before running the numbers.

### Offer math

1. Start from the band for the level, not from the candidate's current pay. Ask for the expected range, never the pay history: several jurisdictions ban asking.
2. Place the offer by evidence from the scorecard: usually between the minimum and the midpoint for a person who meets the level, above the midpoint only for proven over-delivery against the level guide.
3. Total package = base + target bonus + annualised equity (grant value divided by vesting years) + sign-on spread over the first year. Show each part and the total in the same currency and period.
4. Check internal equity: compare the offer with the compa-ratios of current people at the same level. An offer that lands above a better-performing peer opens a pay-equity problem; raise the peer or lower the offer, and record why.
5. Offer letter states base, bonus rules, equity terms, start date and conditions. The user's employment lawyer reviews contract terms.

### Pay transparency (as of 2026-11; read the state page before posting)

US state posting rules, read in Clockspot's tracker (fact-checked 2026-05-27) and Cooley's alert (2026-07-06). Thresholds are employer headcounts. The Minnesota (Minn. Stat. 181.173), Connecticut (Governor's office announcement of Public Act 26-12), Hawaii (HRS 378-2.8), District of Columbia (Code 32-1453.01), Maryland (Labor and Employment 3-304.2) and Maine (26 MRSA 622-A) rows were read on a state source as of 2026-11; the statute pages confirm the threshold and the posting rule but not the effective dates, which rest on the two secondary sources. The other rows rest on the two secondary sources only, so read each state's labour department page before posting.

| Jurisdiction | Effective | Threshold | Rule |
|---|---|---|---|
| Hawaii | 2024-01-01 | 50+ | Range in every posting |
| District of Columbia | 2024-06-30 | any | Range in every job listing and position description; existence of healthcare benefits disclosed before the first interview |
| Maryland | 2024-10-01 | any | Range and a general description of benefits in every posting, for work physically performed at least in part in Maryland |
| Illinois | 2025-01-01 | 15+ | Pay scale and benefits in every posting, including third-party |
| Minnesota | 2025-01-01 | 30+ | Range and benefits in every posting |
| New Jersey | 2025-06-01 | 10+ | Range and benefits in every posting |
| Vermont | 2025-07-01 | 5+ | Range in every public posting |
| Massachusetts | 2025-10-29 | 25+ in MA | Range in every posting, and on request to employees |
| Virginia | 2026-07-01 | any | Range in every posting; 15-business-day cure period |
| Maine | 2026-07-29 | 10+ | Range in every posting, including third-party postings |
| Connecticut | 2026-10-01 (Public Act 26-12) | any | Range and general benefits description in postings, all employer sizes |
| Rhode Island | 2023-01-01 | any | Range on applicant request |
| Delaware | 2027-09-26 | more than 25 | Good-faith range in every posting |

California, Colorado, New York (state and New York City) and Washington also require ranges in postings and each has its own thresholds; read the state page before relying on a figure. Nevada was not confirmed by either source. Pay-range rules can reach remote roles open to residents of these places: check where the candidate may sit, not only where the company sits.

EU Pay Transparency Directive 2023/970: applicants have the right to information about the initial pay or its range, based on objective gender-neutral criteria. A joint pay assessment is required when reported pay differs by 5% or more in any category of workers, is not justified by objective gender-neutral reasons, and is not fixed within six months. Employers with 250 or more workers report every year from June 2027; coverage of reporting starts at 100 workers. Member states transposed on different dates: check the country's own law.

### US overtime: the salary floor

An employee can be exempt from overtime only if paid a salary of at least $684 per week, and meets a duties test. Highly compensated employees need $107,432 total annual compensation. The Department of Labor restored these figures in a technical amendment announced 2026-05-14 and published in the Federal Register on 2026-05-15, after courts vacated the 2024 increase. Some states set higher floors: check the state. Contractor versus employee status depends on the facts of the work, not the contract's label: send classification questions to an employment lawyer.

## Examples

- Wrong: "A senior engineer earns about 150,000." Right: "No source supplied. Please give the survey, region and percentile; I will build the band from it."
- Wrong: offer 20% above the candidate's current pay. Right: "Level 3 band midpoint 100,000; candidate meets the level guide; offer 96,000 (compa-ratio 0.96); two current Level 3 peers sit at 0.92 and 1.01."
- Wrong: post a job in Maine without a range. Right: "Posting reaches Maine residents and the company has 10 or more employees; add the range."

## Checklist

- [ ] Levels have a written guide with the four tests, and each person is mapped with evidence.
- [ ] Every benchmark has a source, date, region and percentile; no remembered figures.
- [ ] Bands show midpoint, spread, min and max; the spread is the user's choice.
- [ ] Offers use total package and an internal-equity check.
- [ ] The posting jurisdiction was checked against the pay-transparency table and the state page.
- [ ] Contracts, classification and dismissal questions went to a qualified employment lawyer.

## Composition / References

- [Clockspot: pay transparency laws by state, fact-checked 2026-05-27](https://www.clockspot.com/research/pay-transparency-laws-by-state)
- [Cooley: new state pay transparency laws, 2026-07-06](https://www.cooley.com/news/insight/2026/2026-07-06-show-me-the-money-or-the-wage-range-new-state-pay-transparency-laws)
- [EUR-Lex: Directive (EU) 2023/970](https://eur-lex.europa.eu/eli/dir/2023/970/oj/eng)
- [European Commission: Pay Transparency Directive FAQ](https://commission.europa.eu/document/download/828ecf2a-e13d-4346-bdca-7eccbbfe28d3_en)
- [US Department of Labor: executive, administrative and professional exemptions, 2026-05-14](https://www.dol.gov/newsroom/releases/whd/whd20260514)
