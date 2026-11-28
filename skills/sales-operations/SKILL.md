---
name: sales-operations
title: "Sales Operations: CRM Hygiene, Research and Pipeline Math"
description: "Sales operations: lead research, CRM dedup and stage gates, outreach drafts, meeting setup, pipeline and forecast math. Every send waits for approval."
license: Apache-2.0
compatibility: "Needs a CRM, email and calendar connection for live updates; works on exported lists and notes otherwise."
capabilities: customer-management messaging-email calendar
domains: sales-rep
rules:
  - match((?i)\b(clean\s?up|dedup\w*|audit|sweep)\b.{0,20}\b(crm|pipeline|contacts)\b)
  - match((?i)\b(pipeline (review|report|coverage)|forecast (accuracy|categories)|weighted pipeline|stale deals?)\b)
  - match((?i)\b(research|look up|find info on)\b.{0,20}\b(lead|prospect|account)\b)
  - match((?i)\b(draft|write)\b.{0,20}\b(outreach|follow[- ]?up|intro email)\b.{0,30}\b(to|for)\b)
  - match((?i)\b(log|update|record)\b.{0,30}\bcrm\b)
  - semantic(clean up duplicate contacts and stale deals in our CRM)
  - semantic(research this lead and draft a follow up for my approval, 0.71)
  - semantic(log my meeting notes in the CRM and schedule the next call, 0.69)
  - match((?i)\b(research|look up|pull|draft|write)\b.{0,60}\b(first-touch|intro|invite|confirmation|connection note)\b.{0,80}\b(approv\w+|look over|before it goes out|review)\b)
  - match((?i)\b(propose|set up|schedule)\b.{0,40}\b(meeting|call)\b.{0,60}\b(slots?|times?|invite|confirmation)\b)
  - match((?i)\b(open deals?|deals)\b.{0,40}\b(no (scheduled )?next step|closed this week|untouched)\b)
---

## Overview

This skill executes the sales motion: research leads, keep the CRM truthful, draft personalized outreach for email and LinkedIn, log activity, report on the pipeline and set up meetings. It does the legwork; the user makes the calls and approves every outbound message and every deal-stage or value change.

## Mental model

- A CRM record shows what happened, not what is hoped.
- Each active deal has exactly one concrete, dated next step.
- Research separates sourced fact from labeled inference; a wrong fact in an outreach email burns the lead.

## Rules

### Workflow

1. Context: pull the account or lead from the CRM and memory. Note stage, history, last touch and any open next step before doing anything.
2. Research: for new leads, find the company, role and two or three recent, specific signals worth referencing (funding, launches, hiring) via web search. Record findings on the CRM record, separating fact from inference.
3. Qualify: with the framework that fits the deal, per the `sales-qualification` skill (BANT as a filter for simple deals, MEDDPICC with all eight letters for complex ones). Each letter maps to a CRM field checked for emptiness. Record evidence in the prospect's own words, not rep summaries; mark gaps as first-call questions, never guesses.
4. Draft: outreach grounded in one specific researched signal per message. Short, plain, one clear ask. Follow-ups add value (new angle, relevant proof), never "just bumping this".
5. Log: every completed touch, reply and meeting goes into the CRM with date and outcome. Every active deal keeps exactly one concrete next step with a date.
6. Report: what was researched, drafted (awaiting approval), updated, and which deals need the user's attention.

### CRM discipline

- No stage advances without a real buyer action to point to.
- One next step per deal, always dated. A deal with no next step is flagged, not ignored.
- Dedup before create: block creation on an exact email match; flag fuzzy company or name matches for review. Merge with field-level survivorship; never delete the record carrying activity history.
- Stage gates enforce completeness: a deal does not advance (for example to Proposal) with its framework fields empty. That beats retroactive cleanup.

### Outreach drafting

- Personalization means researched specifics (their announcement, their stack, their hire), never template-swapped first names or flattery.
- Sequence length and spacing: follow the cadence in the `outreach-cold-copy` skill (its numbers are practitioner norms). First follow-up 2 to 3 business days after the initial send; each touch adds a new angle; end with a clean break-up note. Stop immediately on any opt-out signal and record it.
- LinkedIn register differs from email: shorter, no subject line, conversational. Keep connection notes short (free accounts get a tighter note length and a monthly cap on personalized notes; check the account). LinkedIn doesn't publish its weekly invitation cap; practitioners report roughly 100 per rolling week on most accounts, so stay well under it. Every LinkedIn action is manual and user-approved: its User Agreement (§8.2 "Don'ts", effective 2025-11-03) bans bots and automation for adding contacts or sending messages.
- Compliance: apply the `outreach-compliance` skill for the recipient's region, calls, texts and call recording; where it says counsel, flag it for the user rather than assuming. Canada (CASL) and Germany need consent even for B2B email; don't draft cold email to them without it. Accurate sender identity, a non-deceptive subject and a working opt-out belong in every message.
- Sending health: apply the `outreach-deliverability` skill for authentication, mailbox-provider limits and thresholds. Watch reply and spam-complaint rates as the stop signal for a sequence, not open rates; pause a sequence when complaints reach the skill's working target.
- Reply received: log it, classify it (interested, objection, not now, opt-out), and draft the response or the break-up accordingly.
- Meeting setup: propose slots from the calendar and draft the confirmation.

### Pipeline math

State it per segment and period.

- Coverage = open pipeline expected to close in the period / quota still to be closed. Required coverage = 1 / the segment's measured win rate over the last four quarters, plus a 10% to 20% buffer for slippage. Examples: a 33% win rate needs 3x, 25% needs 4x, 20% needs 5x. The 3x to 4x rule of thumb dates from higher win rates, so don't default to it.
- Count only live deals: remove any deal with no dated next step, or idle for longer than twice the median time in its stage (a house rule; tune it to the sales cycle).
- Weighted pipeline = sum of deal amount x historical win rate of the deal's stage. Report it beside the unweighted figure.
- Pipeline to create = (quota - closed - commit) / win rate on new deals, by the date the sales cycle length implies.
- Forecast categories: commit means every stage-gate item for proposal in the `sales-qualification` skill is evidenced and the paper process is dated inside the period; best case means qualified deals that could close in the period; the rest is pipeline. Report each category separately.
- Forecast accuracy = 1 - |forecast - actual| / actual, tracked weekly per rep. A rep who is always high or always low is mis-scoring stage gates.

### Guards

- Never send any outreach without explicit approval of that exact message.
- Never fabricate a personalization detail or credential; unverified claims burn leads and trust.
- Honor opt-outs immediately and permanently in the CRM.
- Don't advance deal stages or edit deal values without a stated buyer action behind it.

## Examples

- "Research Acme's head of ops": a research block with sourced signals and a suggested angle, recorded to the CRM.
- "Clean up the CRM" or "pipeline review": a hygiene sweep (dupes, stale deals, missing next steps), then the report.
- "Draft outreach to Dana": context pull, research if thin, one draft per channel requested.
- "Book it": propose slots from the calendar, draft the confirmation.

## Output format

- Per lead: a CRM-ready research block with Company, Person, Signals with sources, Qualification notes and Suggested angle.
- Outreach drafts in fenced blocks headed by channel and recipient.
- Pipeline reports as a table: deal, stage, last touch, next step, flag.

## Checklist

- [ ] Each draft rests on one sourced signal, with fact and inference separated?
- [ ] Drafts are marked as awaiting approval; nothing was sent?
- [ ] Every active deal has one dated next step?
- [ ] No stage moved without a recorded buyer action?
- [ ] Opt-outs recorded?
- [ ] Pipeline figures stated per segment and period, weighted beside unweighted?

## Composition / References

- `sales-qualification` skill: framework fields and stage exit criteria.
- `outreach-cold-copy`, `outreach-deliverability` and `outreach-compliance` skills: cadence, sending health, consent.
