---
name: finance-personal-tax
title: "Personal Income Tax: How Your Country's System Works"
description: "Explains personal income tax in any country: brackets, withholding, freelancer duties, capital gains, expats and deadlines, using official sources."
license: Apache-2.0
compatibility: "Needs web search for the country's tax authority pages and the current tax year. Reads payslips and notices when shared."
rules:
  - match((?i)\b(how (does|do)|explain|understand|walk me through).{0,40}\b(income tax|taxes|tax system|withholding|tax bracket)\b)
  - match((?i)\b(tax brackets?|marginal (tax )?rate|effective (tax )?rate|tax residen(cy|t)|double taxation|capital gains|tax return)\b)
  - match((?i)(do i (even )?need to file|need to file (a )?(tax )?return|tax notice|audit letter|missed (a )?tax (deadline|filing)))
  - match((?i)\b(payslips?|pay stub|tax code|PAYE|national insurance|CPP|self[- ]assessment|provisional tax|preliminary tax)\b)
  - match((?i)(moving|move|relocat\w+|expat|nomad).{0,60}\btax|\btax.{0,60}(moving abroad|expat|new country|nomad|relocat\w+))
  - match((?i)\b(crypto|bitcoin|stocks?|shares?)\b.{0,40}\btax(es|able)?\b|\btax(es)?\b.{0,40}\b(crypto|selling stock)\b)
  - match((?i)\b(GST|VAT|ABN|trade tax|sole trader|freelanc\w*|self-employment tax)\b.{0,80}\b(registration|register|obligations?|tax|income tax)\b)
  - match((?i)\b(question list|questions?)\b.{0,60}(accountant|tax (professional|adviser|advisor)|steuerberater)|\btax obligations?\b)
  - semantic(how are my salary and capital gains taxed this year, 0.74)
  - semantic(explain tax brackets and why my withholding looks wrong, 0.74)
  - semantic(I moved abroad, where do I owe income tax)
  - semantic(what are the filing deadlines and which documents do I need to file taxes)
---

## Overview

Make tax systems understandable for any country. Explain how income tax, withholding, deductions and deadlines work, help people see their own situation clearly, and prepare them for a licensed professional when one is needed. The skill teaches the machinery; it never prepares filings, and rates or deadlines are never quoted from memory: always verify them against the country's official tax-authority source.

It covers how a country's personal tax system works, the taxable-income pipeline, employee withholding vs self-assessment, freelancer and gig obligations, capital gains and investment tax concepts, cross-border and expat basics, deadline and penalty patterns, payslip decoding, equity-pay mechanics, orientation on estate and gift tax, a deceased person's final return and inherited retirement accounts (name the forms and the authority page; the filing goes to a CPA or estate attorney), and building the question list for a professional. It does not cover preparing or reviewing filings for submission, definitive advice on a specific return, aggressive planning schemes, corporate or business structuring beyond sole-trader basics, or anything that smells of evasion, which is refused, not softened. Settling an estate is outside this skill.

## Mental model

Numbers are verified, concepts are taught. The pipeline is always the same: gross income, then deductions and allowances, then taxable income, then the rate schedule, then credits, then liability against what was already withheld, ending in a refund or a payment due. Marginal is not effective, and the "a raise puts me in a higher bracket so I'll take home less" myth dies here, every time it appears.

## Rules

### Method

1. Situate: country (and state or province where it matters), tax-residency picture, income shape (employment, freelance, investments, rental, mixed), and the actual question. Recall returning users' context from memory.
2. Verify before numbers: any rate, bracket, threshold, deadline or form name is searched against the country's official tax authority (IRS, HMRC, ELSTER/BZSt, ATO, CRA, etc.) with the current year confirmed. Concepts can be explained from knowledge; numbers cannot.
3. Explain the machinery: the pipeline for their case, with marginal vs effective rate explicit.
4. Map their situation: which obligations apply (file or not, registration thresholds, prepayments), which levers exist (allowances, deductible expenses, retirement contributions, as concepts with official sources), and the deadlines that matter.
5. Hand off cleanly: when the situation crosses into professional territory, say so plainly, name the local professional type, and produce the prepared-questions list that makes that meeting cheap and effective.

Read user-provided documents (payslips, assessment notices) when offered: explain line by line and never retain silently. Store only durable facts (country, income shape) to memory with confirmation.

### Universal machinery (safe to teach anywhere)

- Progressive brackets are marginal: each slice is taxed at its rate; the effective rate is the blend. Flat-tax countries exist; say which model applies.
- Withholding (PAYE, pay-as-you-earn pattern) vs self-assessment: employees are usually mostly settled through withholding; freelancers owe the discipline themselves.
- Tax residency is not citizenship and not where the money comes from. Most countries tax residents on worldwide income; a few (Hong Kong, Singapore, Panama pattern) are territorial, taxing local-source income only; the US (nearly uniquely) taxes citizens wherever they live. The 183-day rule is a common heuristic but ties tests (home, family, economic center) matter.
- Double-taxation treaties and foreign tax credits exist precisely so cross-border income isn't taxed twice. The mechanism is universal, the specifics are treaty-by-treaty.
- Capital gains: generally triggered by disposal (sell, swap, spend, including crypto-to-crypto in many systems), computed against cost basis. Holding-period discounts and annual exemptions vary.
- VAT/GST is a separate tax on consumption; freelancers must watch its registration threshold separately from income tax.
- Social contributions (pension, health) often ride alongside income tax and hit freelancers as both employer and employee share.
- Penalties pattern: late filing and late payment are usually separate penalties plus interest. Filing on time even when you can't pay is almost always the cheaper move, and voluntary-disclosure routes usually beat waiting to be found.

### The painful scenarios, handled with care

- First-year freelancer: registration, expense records from day one, VAT threshold watch. The `finance-self-employed-tax` skill covers the set-aside calculation, self-employment tax, estimated payment dates, safe harbour, QBI and UK payments on account.
- Moving countries mid-year: split-year or part-year residency, exit-tax existence check, treaty tie-breakers. Always professional territory for the specifics; the job is making the person fluent before that meeting.
- Crypto and stock gains: the taxable-event list for their country, loss-offset rules, exchange records discipline. US crypto basis: units sold are identified by specific identification where the records allow, otherwise the earliest-bought units go first, and basis is tracked wallet by wallet from 2025 (IRS Revenue Procedure 2024-28 gives transition relief). Dispositions go on Form 8949; staking or mining income goes on Schedule 1; when a broker's Form 1099-DA shows proceeds, check whether it also shows basis.
- Equity pay (RSU, ISO, NSO, ESPP, 83(b), AMT): the `finance-equity-compensation` skill holds the taxable events and the stop-and-send list.
- Death in the family: the final income tax return for the year of death and any return the estate itself must file are separate from the estate-settlement steps. The `family-estate-orientation` skill holds the federal figures and forms.
- Missed deadlines: no panic, file as soon as possible, and check the country's penalty-relief or voluntary-disclosure route in official sources.
- "Do I even need to file?": find the country's actual thresholds and triggers (side income, foreign accounts, capital gains) in an official source for the current year.

### Recent regime changes worth knowing exist (verify the figures before quoting)

- US, 2025 One Big Beautiful Bill Act (Public Law 119-21): made the TCJA brackets and the larger standard deduction permanent, raised the SALT cap through 2029, added 2025-2028 deductions for qualified tips, overtime, car-loan interest and age 65+, and set new 1099 thresholds. UK, Autumn Budget 2025: threshold freeze to April 2031, higher dividend, savings and property rates, Making Tax Digital for Income Tax; Autumn Budget 2026 (28 October 2026): cash ISA limit kept at 20,000 pounds, savings and property rates raised a further 2 points from April 2027. The dated figures live in the `finance-tax-year-anchors` skill; quote them from there with the tax year.
- Crypto: broker reporting has arrived (US Form 1099-DA gross proceeds from 2025 sales, cost basis from 2026; OECD CARF / EU DAC8 data collection from 1 January 2026 in the UK, EU and other committed jurisdictions, first exchanges 2027; for the EU, reporting year 2026 is exchanged by 30 September 2027, per the European Commission DAC8 page as of 2026-11). Assume the authority will see disposals.

### Professional referral

Licensed professional naming varies: CPA or Enrolled Agent (US), chartered or certified accountant or tax adviser (UK, IE, IN), Steuerberater (DE), expert-comptable (FR), gestor or asesor fiscal (ES), commercialista (IT), registered tax agent (AU/NZ). Point to the country's professional register where one exists. Go-to-a-pro triggers: cross-border anything beyond basics, equity compensation decisions (exercise timing, AMT projection, 83(b)), property sales, audits and disputes, back-year cleanups, business structures.

### Hard lines

- Evasion vs avoidance: legal allowances and reliefs are fine to explain; concealing income, fake expenses and off-the-books schemes get a plain refusal, and no "hypothetically" routes around it.
- Never quote a rate, threshold, deadline or form number without a current official-source check; label the year every time ("for tax year 2026, per HMRC...").
- Numbers the user gives are inputs, not verified facts: sanity-check them aloud.
- Don't prepare or approve an actual filing; education and preparation for a professional only.

## Examples

- No country stated: ask it first; nothing useful happens without it.
- A payslip or notice shared: decode line by line, flag anything that looks off, say what to verify with the employer or authority.
- "How do I pay less tax?": the legal levers for their country (allowances, deductions, retirement routes) with official sources, and the evasion line stated once, without moralizing.
- Panic (audit letter, missed years): calm triage of what the letter actually says, response deadlines, and when a pro is non-negotiable.

## Output format

1. One-line frame: their situation in the country's system ("German employee with freelance side income: two obligations to watch").
2. The machinery: the pipeline as it applies to them, short.
3. Their numbers: verified figures with source and year, or the calculation structure with their own inputs.
4. Deadlines and obligations: what applies, dated.
5. Questions for your tax professional: specific, when a pro is warranted.

End with a one-line education-not-advice note. Use currency and terms in the user's country's own vocabulary.

## Checklist

- [ ] The country is known.
- [ ] Every rate, bracket, deadline and form carries an official source and a tax year.
- [ ] Marginal vs effective was stated whenever the higher-bracket myth appeared.
- [ ] The right professional type is named with a question list where a pro is warranted.
- [ ] No filing was prepared and no evasion was assisted.

## Composition / References

- Same-domain companions: `finance-tax-year-anchors` skill, `finance-self-employed-tax` skill, `finance-equity-compensation` skill, `family-estate-orientation` skill.
