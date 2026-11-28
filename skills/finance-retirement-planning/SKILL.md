---
name: finance-retirement-planning
title: "Retirement and Pensions: On-Track Math by Country"
description: "Decodes any country's pensions into three pillars, runs on-track and drawdown math, covers late-start and self-employed playbooks, and flags pension scams."
license: Apache-2.0
compatibility: "Needs web search for official pension rules and limits."
domains: financial-planner
rules:
  - match((?i)\bretire(ment|d)?\b.{0,40}(plan|planning|math|enough|on track|savings|pot|income|age|account))
  - match((?i)(am i|are we|will i|do i have) (saving|on track|have).{0,30}(enough|retire)|(saving|save) enough.{0,20}retire)
  - match((?i)\b(pension|annuity|drawdown|decumulation|sipp|rrsp|superannuation|state pension|defined benefit|db transfer)\b)
  - match((?i)(safe withdrawal|4% rule|four percent rule|fire number|roth conversion|required minimum distribution|\brmds?\b))
  - semantic(am I saving enough for retirement and what if I started late)
  - semantic(how much can I withdraw each year once I retire)
  - semantic(explain how the pension system works in my country)
  - semantic(is this pension transfer offer a scam)
---

## Overview

Retirement systems everywhere are the same three pillars wearing different names. This skill decodes any country's pension system into its universal parts, verifies the local numbers against official sources, runs the honest am-I-on-track math, and prepares people for a professional when one is needed. Pension advice is a regulated activity in many countries: educate and compute scenarios, never give personal regulated advice, and give the licensed-adviser handoff for the big irreversible moves.

It covers the user's country system through the three-pillar frame, state-pension mechanics (contribution years, claiming ages, deferral), employer-plan mechanics (DB vs DC, matches, auto-enrolment), private tax-advantaged account patterns, on-track math and scenarios, fee impact, late-start and self-employed playbooks, cross-border pension orientation, decumulation concepts, and scam recognition. It does not cover regulated personal advice (which fund, transfer or not, buy this annuity), tax filing specifics, investment selection, or DB-transfer and pension-cash-out blessings; those are professional territory by law in many places, and the answer says so plainly.

## Mental model

Three DIY-safe moves outrank everything clever: capture the full employer match, find the fee, and check the state record for gaps. The savings rate and time dominate every other choice. Time math for the young, dignity math for the late starter: show the numbers, never moralize.

## Rules

### Method

1. Situate: country, age, target retirement age, income, and what exists already (state contribution record, employer plans past and present, private accounts, property), and the employment shape (employed or self-employed). Recall returning users from memory; retirement planning is a multi-session journey.
2. Decode the system: map the country onto the three pillars with local names, then search the official layer: state-pension rules and the user's projection route (most countries have an online statement or forecast portal; finding it is step one), current contribution and allowance limits, claiming ages. Never quote limits, ages or rates from memory; they change yearly.
3. Run the math visibly: the on-track check with their real numbers, shown so they can re-run it. Scenarios (retire at X vs Y, save Z more) beat single verdicts.
4. Prioritize the moves: the universal order adapted to their system, each labeled DIY-safe or adviser-required.
5. Hand off cleanly: DB transfers, annuity purchases, cross-border consolidation and drawdown design near retirement go to a licensed adviser (fee-only or fiduciary pattern; IFA UK, Honorarberater DE, fee-only CFP US; verify on the register), with the prepared question list.

### The three pillars

1. State pension: pay-as-you-go, earned by contribution years. Know the qualifying-years rule, check the record for gaps (career breaks, years abroad; many systems sell voluntary top-ups that are spectacular value; verify locally), the claiming age (rising nearly everywhere), and deferral bonuses.
2. Employer/occupational: DB (defined benefit: the employer promises income; rare now, gold if held) vs DC (defined contribution: a pot you invest; the modern default; the risk moved to you). Auto-enrolment patterns put minimums in; minimums are rarely enough. The first rule everywhere: capture the full employer match before any other saving; it is an instant guaranteed return.
3. Private/personal: tax-advantaged account patterns. Tax-later (deduct now, taxed in retirement: 401k/traditional-IRA/RRSP pattern) vs tax-now (taxed now, tax-free later: Roth/ISA/TFSA pattern). Annual limits and catch-up allowances are local and yearly; always verify.

### Anchors for the two most-asked systems

- Contribution limits, catch-ups, allowances and the dated UK tax changes come from the `finance-tax-year-anchors` skill, each with its tax year. Look up any year the skill does not list on irs.gov, ssa.gov or gov.uk.
- US: Social Security full retirement age is 67 for anyone born on or after 2 January 1960; claiming at 62 cuts the benefit about 30%, each year of delay to 70 adds 8%. RMDs start at 73 (75 if born 1960 or later).
- UK: unused pension pots fall into inheritance tax from 6 April 2027, which changes the old "spend the ISA first, leave the pension" order. State pension: check the forecast and the National Insurance record on gov.uk; gaps are often worth buying.

### On-track math (universal, show your work)

- Target: the roughly 70% replacement-rate heuristic (of pre-retirement income, less if the mortgage dies first), or 25x annual spending as the pot target (the 4% rule inverted; a planning heuristic, not a guarantee: Morningstar puts the fixed real safe starting rate at 3.9% for 2026 retirees, higher with flexible guardrail spending, and sequence-of-returns risk is why). Saving about 15% of income including the match is the standard working target.
- Checkpoint pattern: about 1x salary saved by 30, 3x by 40, 6x by 50, 8-10x by 60. Coarse, but honest orientation.
- The two numbers that dominate everything: the savings rate (dwarfs fund selection) and time (money doubles roughly every decade at about 7%; starting at 25 vs 35 roughly halves the required rate; show this to every young user).
- Fees compound in reverse: a 1% annual fee eats roughly a quarter of a 40-year pot vs 0.2% trackers. Have them find their plan's fee; it's the highest-value question most savers never ask.
- State pension counts: subtract the (verified) state entitlement from the income target before sizing the pot. Ignoring it overstates the gap and demoralizes.

### Decumulation and real returns

- Work in real terms: real return = (1 + nominal return) / (1 + inflation) - 1. Show nominal return, inflation and fee as inputs the user can change; never present one return as a forecast. Look up the regulator's or a named planner's current published projection assumptions and cite them.
- Pot formula: pot = (annual spending - guaranteed income such as the state pension) / withdrawal rate. For a fixed horizon of n years at real return r: pot = spending x (1 - (1 + r)^-n) / r. Show both and the gap between them.
- US drawdown order is a heuristic, not a rule: taxable accounts first, tax-deferred next, Roth last, adjusted to fill low brackets and to meet required distributions. Roth conversions belong in low-income years, with the tax paid from outside the account. Medicare Part B and D premium surcharges (IRMAA) use modified AGI from two years earlier (SSA), so a large conversion at 63 can raise premiums at 65; look up the current IRMAA brackets on medicare.gov.
- Other countries: name the local withdrawal wrappers and their order, and verify them.

### The playbooks

- Late starter (45+): no shame, arithmetic. Max catch-up allowances, capture every match, push the claiming age later (each deferral year is a permanent raise in most systems), plan housing (downsizing equity is a pillar for many), and set expectations honestly rather than chasing returns.
- Self-employed: no employer pillar, so the discipline must be manual: the local personal-pension vehicle plus automatic monthly contributions. Check whether state contributions accrue automatically or need voluntary payments (a nasty country-specific trap; verify).
- Scattered across countries: each country's state record usually keeps earned rights (totalization or social-security agreements aggregate qualifying years; pattern, verify per pair). Private pots can sometimes consolidate; cross-border consolidation is adviser territory. Step one is the inventory: track down every pot (pension-tracing services exist in many countries).
- Pension vs mortgage payoff: compare the guaranteed after-tax mortgage rate against the expected net return plus forgone match and tax relief. The match almost always wins over prepayment; after that it's closer and personal.
- Near retirement (5 years out): shift from growth math to decumulation. Annuity (guaranteed income, inflexible) vs drawdown (flexible, market and longevity risk) vs blend; claiming-age optimization. This design phase is exactly what a one-off fee-only adviser is for.

### Scam radar

Pensions are where life savings die.

- Pension "liberation" or early-access offers (access before the legal age "through a loophole") are fraud plus a tax catastrophe, near-universally.
- Cold-call "free pension reviews", guaranteed high returns, overseas property, crypto or storage-unit schemes inside pensions, and pressure to transfer out of a DB scheme. The UK ran a national scandal on exactly this; DB transfers are adviser-mandated there for good reason. Giving up a DB promise is almost always wrong; anyone pushing it earns commission.
- Verify any adviser on the national register (the regulator's public list) before money moves.

### Limits

- Never give regulated personal advice: fund picks, transfer blessings and annuity choices go to a licensed adviser (named register, prepared questions).
- Don't let a DB transfer, early-access scheme or cold-call "review" pass without the scam and regulated-advice warning.

## Examples

- "Am I saving enough?": run the math with real numbers; give the honest verdict with the lever that matters most.
- "Should I transfer my DB pension or cash out?": the risks plainly, the near-universal answer (don't, without mandated advice), and the adviser route; never a blessing.
- Panic at 50 with nothing: the late-starter playbook, arithmetic over shame; it is fixable more often than people fear.
- A statement or plan document shared: read it, extract the fee and the match, translate it line by line.
- No country: ask first; pillars decode differently everywhere.

## Output format

1. Your system decoded: the three pillars with their local names and where the user stands in each.
2. The math: the on-track check with their numbers, shown, with scenarios where useful. Figures verified via official sources, dated, year named.
3. The moves: prioritized (match, high-interest debt check, tax-advantaged room, fees audit), each labeled DIY-safe or adviser-required.
4. Verify list: the official portals to check (state-pension forecast, plan statements, fee disclosures).
5. Adviser handoff, when triggered: the professional type, the register, the prepared questions.

End with a one-line education-not-advice note. Use local terms and currency throughout.

## Checklist

- [ ] The country is known and the three pillars are named locally.
- [ ] Every limit, age and rate is dated and sourced.
- [ ] The math shows its inputs and offers scenarios.
- [ ] Match, fee and state-record gaps were each addressed.
- [ ] Any transfer, annuity or cash-out question carries the adviser and scam warning.

## Composition / References

- Same-domain companions: `finance-tax-year-anchors` skill for dated limits, `finance-budget-debt-payoff` skill for the priority order before retirement saving.
