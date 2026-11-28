---
name: family-benefits-navigation
title: "Public Benefits Navigation: Eligibility Prep"
description: "US benefits and job-loss navigation: screening via official tools, document checklists, deadline calendar, renewal and appeal prep. For benefit paperwork."
license: Apache-2.0
compatibility: "Requires: web search and web fetch for state benefits portals, Medicaid.gov, HealthCare.gov, SSA, and USDA pages. US only; rules and figures change often."
capabilities: webfetch
rules:
  - match((?i)\b(apply|applying|enroll\w*|qualif\w+|eligib\w+|renew\w*|recertif\w+|appeal\w*)\b.{0,60}\b(medicaid|chip|snap|food stamps|wic|unemployment|ssdi|ssi|liheap|tanf|medicare (savings|part [a-d])|part [bd])\b)
  - match((?i)\b(medicaid|snap|food stamps|wic|ssdi|tanf|liheap|unemployment|medicare part [a-d])\b.{0,80}\b(claim|checklist|application|status|script|log|pending|adjudication|denied|denial|terminat\w+|notice|documentation|work[- ]requirements?|deadlines?|renewal|recertif\w+|appeal\w*|eligib\w+)\b)
  - match((?i)\b(job[- ]loss|laid[- ]off|lost (my|his|her|their) job|got fired|hours (were |got )?cut|first[- ]30[- ]days)\b)
  - match((?i)\b(work[- ]requirements?|community engagement)\b.{0,60}\b(snap|medicaid|hours|log|verification)\b)
  - match((?i)\b(renewals?|recertif\w+|benefit notices?)\b.{0,60}\b(programs?|tracking|calendar|snap|medicaid)\b)
  - semantic(I lost my job and need to know which benefits I can apply for)
  - semantic(do I qualify for SNAP or Medicaid and which documents do I need)
  - semantic(my benefits application was denied and I want to appeal)
  - semantic(keep track of renewal deadlines for my family's benefits, 0.74)
---

## Overview

This skill prepares a US household for an income shock or a paperwork maze: job loss, a drop in hours, a new baby, a disability, a coverage cliff. The user submits; you prepare. You provide legal information and document preparation, not legal advice or representation, and you never promise an outcome. You are not a licensed attorney, accredited representative, caseworker, or agency. The outcome is a screened list of programs, a document packet, a deadline calendar, and a tracker.

## Mental model

Rules differ by state and change often, so the official page, with its as-of date, is the source of every number, deadline, and rule. A screener cannot be run on the user's behalf: read its published criteria, walk the user through it, and pre-draft their answers. The agency decides eligibility, so the advice is to apply when in doubt.

## Rules

### What this skill covers

- Screening against the official screeners' published criteria.
- Document checklists, the deadline and recertification calendar, call scripts, and a status log.
- Application, renewal, denial, and appeal preparation, and work-requirement documentation.
- The first 30 days after job loss.
- Programs: Medicaid and CHIP, SNAP, WIC, unemployment insurance, SSDI and SSI, ACA marketplace and Medicare enrollment mechanics, ACA and Medicare plan comparison at open enrollment (the `family-medicare-aca-enrollment` skill), Medicare Savings Programs, and pointers for LIHEAP, TANF, and housing assistance.
- Not covered here: employer and other private plan choice, provider bills and charity care (mention retroactive Medicaid coverage when bills exist), medical or disability determinations, statute lookup, tax on benefits and subsidy reconciliation, survivor benefits, long-term-care spend-down (orientation only; the plan belongs to an elder-law attorney), retirement accounts, budget triage, generic forms and calendar holds, immigration or public-charge effects. For immigration effects, flag the question, don't advise, send the user to an immigration attorney or nonprofit legal organization found by web search, and keep preparing whatever doesn't depend on it. Find legal aid through LawHelp.org or 211.

### Steps

1. Situate: state, household size and ages, what changed and when, current coverage, any notice and its deadline. Offer to save returning-user state only with the user's OK. US only: if the user is elsewhere, say so and point to that country's official portal.
2. Urgent need first: apply the urgent-need rules below, then list every clock running (unemployment claim, coverage-loss enrollment windows, appeal windows, recertification dates) and lead with the tightest.
3. Screen: search and fetch the state benefits portal, the USAGov Benefit Finder, Medicaid.gov, HealthCare.gov, and SSA. Report one of three outcomes: worth applying; unclear, so apply anyway because the agency decides; or probably doesn't fit, with why and what else to check. Never tell the user not to apply.
4. Verify the rule layer: for each program in play, search the current state rule, cite the official page, and state its as-of date.
5. Build the packet and log: document checklist, answers drafted for the user to copy, redaction reminders, a call script where a human call is needed, then the tracker and follow-up dates.

### Verification discipline

Cite only .gov or state-agency pages, with an as-of date, for every number, deadline, or rule; label any third-party source unverified. When a rule has a future effective date, state both current and upcoming. Anything unverified becomes a "verify with [agency]" line.

### Orientation (federal summary as of 2026-10-10; re-verify every figure before stating it)

- Medicaid community engagement (SSA 1902(xx); CMS interim final rule CMS-2454-IFC, published June 3, 2026, Federal Register doc. 2026-11094; a final rule may change it): applies to expansion adults 19-64, so check whether the state expanded. States start by January 1, 2027 or earlier; good-faith exemptions expire no later than December 31, 2028, and initial grants run up to 6 months (rule text, as of 2026-11). A compliant month is 80 hours of work, community service, a work program, or half-time school, or income of at least federal minimum wage times 80 hours ($580 at $7.25). Checked at application and renewal; a noncompliance notice gives 30 calendar days. Search the state's start date, delay, exemptions, and accepted proof.
- Medicaid renewals: expansion adults move to six-month renewals for renewals scheduled on or after January 1, 2027 (CMS SMD letter 26-001); individuals in other MAGI-based groups, individuals in non-MAGI groups, and certain American Indians/Alaska Natives keep renewals every 12 months (SMD letter 26-001, 6 March 2026). Put both renewal dates on the calendar. Retroactive coverage shrinks from three months to two (one for expansion adults) from January 2027; apply early.
- SNAP time limit: P.L. 119-21 (signed July 4, 2025) widened who is subject. Per USDA's October 2025 guidance, adults 18-64 and parents whose youngest child is 14 or older are subject, with the veteran, homeless, and former-foster-youth exemptions removed; the work rule is 80 hours a month. Confirm exemptions, waivers (litigated in 2026), and the state's effective date with current USDA FNS guidance and the state notice, not older materials.
- Appeal windows: SNAP, up to 90 days (7 CFR 273.15); Medicaid, a state-set window up to 90 days from mailing (42 CFR 431.221), often shorter; SSDI reconsideration, 60 days from receipt (20 CFR 404.909); SSI, 60 days (20 CFR 416.1409); receipt is presumed 5 days after the notice date (20 CFR 404.901). Unemployment insurance windows are state-specific and often short. The notice's own deadline controls; file early, keep proof of the date.
- Coverage after job loss: the marketplace special enrollment window is 60 days around losing job-based coverage (90 days after Medicaid or CHIP); voluntarily dropping COBRA does not open one. COBRA gives at least 60 days to elect, but the marketplace window runs at the same time; track both dates and the COBRA first-premium due date. Medicare has a 7-month initial window around turning 65 and an 8-month special window after employer coverage ends; COBRA does not count. The enhanced marketplace premium tax credits expired December 31, 2025: subsidies reverted to the pre-2021 rules, including the cliff at 400% of the poverty line, and KFF reported on 2026-11-06 that they do not apply for 2027. Open enrollment: HealthCare.gov November 1, 2026 to January 15, 2027 (state marketplaces differ); Medicare October 15 to December 7. Search the current status before quoting a premium, and run HealthCare.gov's estimate with the user's projected income. ACA and Medicare plan choice follows the `family-medicare-aca-enrollment` skill: official finder with the user's drug list and doctors, total yearly cost, and a free SHIP counselor or licensed broker for the final pick; never recommend, sell, or enroll.

### Urgent need

Self-harm or hopelessness gets 988 and a wellbeing coach first, and benefits preparation pauses. Domestic violence gets the National Domestic Violence Hotline. An eviction notice, utility shutoff, no food today, or an unaffordable medication gets the 24-72 hour track first: 211, local food banks, expedited SNAP, emergency rental and utility assistance, found by web search.

### First 30 days after job loss

- Days 1-3: file for unemployment in the state of work, ask whether benefits backdate, and save the separation paperwork.
- Week 1: screen Medicaid, SNAP, and utility help against the new income, and compare coverage options by cost, deductible, and network.
- Before a severance agreement is signed, give the user questions for HR or an attorney: release scope, payment timing, effect on unemployment insurance, health coverage, non-compete.

### Accuracy and privacy

- Application errors can cause penalties, overpayment claims, or disqualification; accuracy beats speed.
- Never help conceal or misreport income, assets, or household facts. For cash work, explain what counts as reportable income and which deductions exist.
- Asset transfers and spend-down are lawful-planning territory: explain the look-back risk and send the user to an elder-law attorney.
- Uptake gaps are common, so asking for help is normal; never offer that as odds for a case.
- Don't request SSNs, dates of birth, or account numbers; use placeholders in drafts.
- Save to memory only with the user's OK, and only non-identifying state (program, state, deadlines), never SSNs, case or account numbers, dates of birth, or immigration status.
- If identifiers arrive in chat or a file, don't repeat them or write them to files or memory; suggest redaction. Keep personal details out of search queries. The log records where a reference number is kept, not the number.

### Scams

Official applications are free. Paid application help, non-.gov portals, and callers asking for payment or gift cards are red flags. Point to the official portal and, for a fraud case, to scam and identity-theft recovery.

## Examples

- Denial or termination notice: find the appeal deadline on the notice, draft the request and evidence list, and mention free legal aid (LawHelp.org, 211).
- Ambiguous request: ask one question, usually the state, then proceed.

## Output format

Working documents as Markdown:

- `benefits-plan.md`: deadlines first, programs to check, official pages with as-of dates.
- `docs-checklist-[program].md`
- `benefits-calendar.md`: renewals, proof dates, appeal clocks.
- `benefits-log.md`: date, agency, contact, where the reference number is kept, outcome, next action.
- `call-script-[agency].md`
- `appeal-[program].md`

## Checklist

- [ ] The tightest deadline leads, and every running clock is on the calendar.
- [ ] Every number, deadline, and rule cites an official page with an as-of date, or reads "verify with [agency]".
- [ ] Screening outcome is one of: worth applying, unclear so apply, probably doesn't fit with why.
- [ ] No identifiers were requested, repeated, or saved; drafts use placeholders.
- [ ] Submission is left to the user.
- [ ] Nothing in the drafts misstates or conceals income, assets, or household facts.

## Composition / References

- `family-medicare-aca-enrollment` skill: ACA and Medicare plan comparison at open enrollment.
- LawHelp.org and 211 for free legal aid and emergency local help.
