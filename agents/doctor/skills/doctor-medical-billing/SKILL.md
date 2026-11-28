---
name: doctor-medical-billing
title: "Dispute a Medical Bill: Line-by-Line Audit and Scripts"
description: "Audits hospital and clinic bills line by line to dispute a medical bill: finds errors, applies No Surprises Act and charity-care rules, drafts disputes."
license: Apache-2.0
compatibility: "Requires: filesystem write for letters and case files, web search for current codes and thresholds, memory tools for case state. US billing rules by default."
capabilities: filesystem-write memory-read memory-write
rules:
  - match((?i)\b(medical|hospital|ambulance|surgery|clinic|lab|er)\s+bills?\b)
  - match((?i)\b(itemi[sz]ed|surprise)\s+(bill|billing|statement)\b)
  - match((?i)\b(dispute|negotiate|reduce|audit|challenge)\b.{0,30}\b(bill|charges?|collections?)\b)
  - match((?i)\b(charity care|financial assistance|no surprises act|good faith estimate|medical debt|balance billing)\b)
  - semantic(check my hospital bill line by line for errors and overcharges)
  - semantic(I got a surprise medical bill and want to dispute it)
  - semantic(help me ask for charity care or financial assistance on a hospital debt)
---

## Overview

A patient has a hospital, clinic or lab bill and wants it checked, disputed or reduced. The outcome is a line-by-line audit, the protections that apply, the deadlines, and ready-to-send letters and call scripts. Hospital bills are frequently wrong and most people never check; this makes checking systematic. The skill works provider-side (hospital, clinic, lab bills) and is US-centric by default: billing codes, the No Surprises Act, and charity-care rules are US constructs, so say so when the user is elsewhere. Insurer-side claim denials and appeals, clinical questions about whether care was appropriate, insurance product choice, and lawsuits or bad-faith claims are not covered here.

## Rules

Workflow:
1. Ingest: the bill, the visit story (what actually happened, dates, who treated), insurance status, and country; recall earlier context with `remember(["medical bills", "disputes", "financial assistance"])`.
2. Get the itemized bill: if the user has a summary bill only, the first deliverable is the request script for an itemized statement with CPT codes for the visit date. No audit without line items.
3. Audit: walk every line against the visit story; sanity-check each CPT and HCPCS code, and web-search unfamiliar ones; flag each suspect line with error type and the question to ask.
4. Check protections: surprise-billing scenario? Estimate exceeded significantly? Nonprofit hospital (charity care duty)? Which deadlines apply?
5. Build the plan: dispute letter for errors, negotiation script for the remainder, financial-assistance application if eligible, escalation ladder if stonewalled.
6. `memorize()` the case state: bills in play, deadlines, what was sent when.

Error taxonomy to audit for: duplicate charges (same code, same date, twice); upcoding (billed complexity above what happened, for example an ER visit coded critical for a sprain); unbundling (components billed separately that belong to one bundled procedure, common in surgical bills); phantom charges (cancelled or never-rendered services); quantity errors; wrong patient or date. Code sets change yearly (CPT on January 1, ICD-10-CM on October 1): check a code against the set in force on the date of service.

Billing audit tests: NCCI procedure-to-procedure (PTP) edits flag code pairs that should not be reported together, and medically unlikely edits (MUEs) flag an implausible number of units for one code; CMS updates both files quarterly, so check the edit table for the date of service before calling a pair unbundled. Emergency department visits are billed with one of five level codes, 99281 to 99285, chosen by the complexity of medical decision-making only, not by time (CMS E/M guidance, as of 2026-11; look up the current CPT code range and level count), so ask what decision-making supports a top-level code on a minor visit. Whether a modifier legitimately overrides an edit is the coder's answer: ask for the documentation, don't assert it.

Negotiation order matters: errors first (deleted, not negotiated), then eligibility (charity care can wipe the bill), then price (benchmark against the Medicare rate from the CMS Physician Fee Schedule lookup, the hospital's own CMS-required price-transparency file, or FAIR Health Consumer, then ask for a self-pay or prompt-pay discount), then terms (interest-free payment plan). Never negotiate a bill you haven't audited.

Charity care (IRS 501(r), nonprofit hospitals): a written financial-assistance policy; patients can apply for 240 days from the first post-discharge bill; no extraordinary collection actions (lawsuits, liens, credit reporting, debt sale) before 120 days and a 30-day written notice; collection pauses while an application is pending; eligible patients can't be charged more than amounts generally billed to insured patients. Many states add their own charity-care rules.

No Surprises Act levers: emergency care, air ambulance, and out-of-network clinicians at in-network facilities can't balance-bill (ground ambulance is not covered federally; some states cover it). Uninsured or self-pay patients can use the patient-provider dispute process when a bill is ≥ $400 above that provider's or facility's Good Faith Estimate, started within 120 days of the bill (CMS, current 2026). Verify thresholds and fees by web search: they change.

Collections defense: dispute in writing within the 30-day validation period of the collector's validation notice (Regulation F); collection on the disputed amount must pause until the collector verifies. Credit reporting: the CFPB's 2025 rule removing medical debt from credit reports was vacated by a federal court; what remains is voluntary bureau policy (paid medical collections, those under $500, and those under a year old aren't reported) plus state laws that go further: check the user's state.

Everything in writing after the first phone call: date, name, reference number, summary letter. Verbal promises from billing departments evaporate.

Deadlines are real: appeal and dispute windows are short; establish every applicable deadline in step 4 and lead with the tightest one.

Medical paperwork requests (letters of medical necessity, prior-authorization packets, records requests, leave forms) follow the `doctor-medical-paperwork` skill, starting from its fact-to-source table.

Boundaries:
- Don't give clinical opinions on whether care was needed.
- Don't guarantee outcomes, and don't advise ignoring bills (deadlines make things worse).
- Don't help dispute charges the user knows are legitimate by misrepresenting facts. Disputing charges for care actually received as described is refused only when the user wants to lie; honest disputes are the whole job.
- Escalate to a lawyer when collections turn into a lawsuit.

### Situations

- "This bill seems huge": visit story and itemized bill request; audit when line items arrive.
- "Write the letter for this denial" or "fill in this form": document type, who signs, then the fact-to-source table before any draft; point the appeal route itself to the plan's internal appeal and external review.
- "Can they charge this?": check against protections and the visit story; answer with the specific lever if not.
- "I can't pay this": eligibility path first (charity care, assistance), then negotiation, then payment plan, in that order.
- Insurance denied the claim: that is an insurer appeal; point to the plan's internal appeal and external review rights, then take back whatever remains patient responsibility.
- Outside the US: general principles (itemize, audit, negotiate, escalate) plus a web search for the country's patient-billing rights; flag that US specifics don't apply.

## Examples

Bad: "Your bill is wrong, just refuse to pay it."
Good: "Request the itemized statement with CPT codes for 2026-09-12. Line 4 repeats code 71046 on the same date: ask whether two chest X-rays were taken. Send the dispute in writing within the collector's 30-day validation window."

## Output format

Working documents as Markdown:
- Audit: `bill-audit-[provider]-[date].md`: line table of charge, code, amount, flag, error type, question
- Letters: `dispute-[provider].md`, `assistance-application-[provider].md`: ready to send, blanks marked
- Scripts: `negotiation-script-[provider].md`: call flow with branch responses
- Case log: `case-[provider].md`: timeline, contacts, deadlines, next action
- Paperwork: `medical-doc-[type]-[date].md` (the letter or form text, clinician blocks left blank) with `fact-source-[type].md` (fact, source document, location, status) and a missing list at the end

## Checklist

- [ ] Itemized bill in hand before any audit.
- [ ] Every flagged line carries an error type and a question.
- [ ] Protections and deadlines checked; tightest deadline first.
- [ ] Current law and thresholds verified by web search.
- [ ] Every dispute in writing; case log and memory updated.

## Composition

- `doctor-medical-paperwork`: drafts of medical necessity letters, prior-authorization packets, records requests and leave forms.
