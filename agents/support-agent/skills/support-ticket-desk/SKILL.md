---
name: support-ticket-desk
title: "Support Desk: Queue Triage & Reply Drafts"
description: "Works an email or Slack support queue: severity triage, error context, tickets, reply drafts for approval, help articles, macros, taxonomies, scorecards."
license: Apache-2.0
compatibility: "Needs a connected support channel (email or Slack), a knowledge base, and ideally error tracking and a task tracker. Replies and tickets are drafts until the user approves them."
capabilities: messaging-slack error-tracking task-management variety
rules:
  - match((?i)\b(triage|sweep|rank|work|clear|flag)\b.{0,60}\b(queue|inbox|slack\s+(support\s+)?channel|open\s+(requests?|tickets?)|today'?s\s+\w+\s+tickets?)\b)
  - match((?i)\b(file|create|open|update|link|merge)\b.{0,40}\b(engineering\s+|tracker\s+)?tickets?\b)
  - match((?i)\bwrite\s+up\s+a\s+ticket\b)
  - match((?i)\b(sentry|error[- ]tracking|stack\s+trace|error\s+events?)\b)
  - match((?i)\bescalation\s+(case|note|acknowledg\w+|handoff)\b)
  - match((?i)\b(status\s+update|reply)\b.{0,60}\b(waiting|friendly|approve|send|bug)\b)
  - match((?i)\b(help[- ]?(center\s+)?articles?|kb\s+articles?|knowledge[- ]?base\s+articles?|macros?|ticket\s+taxonomy|qa\s+scorecards?)\b)
  - semantic(go through the support inbox and triage the tickets by severity, 0.78)
  - semantic(write a reply to this customer ticket for my approval, 0.75)
  - semantic(turn this bug report into an engineering ticket with error context)
  - semantic(triage the open requests in our support channel by severity, 0.74)
---

## Overview

This skill runs the reactive side of customer support: the incoming queue (email and Slack), answered the way a senior support engineer would. The outcome is a triaged queue with a status per item, reply drafts and tickets ready for approval, and, when asked, help articles, macros, ticket taxonomies and QA scorecards saved as files the user loads into the helpdesk. Replies go out only after the user approves each draft.

## Mental model

The first response is the strongest single predictor of satisfaction. Everything else follows from three habits: classify the fault separately from the urgency, answer only what the evidence supports, and keep the customer informed of where the issue stands.

## Rules

### Queue procedure

1. Sweep: pull new and unresolved items from the connected channels. Pull known-issue notes and customer history from memory and the knowledge base in parallel.
2. Triage with severity and priority as two separate calls. Severity is the technical fault: S1 outage or data loss, S2 core feature broken with no workaround, S3 degraded with a workaround, S4 question or cosmetic. Priority derives from severity plus customer tier and business impact; record which factor drove it. A customer's own "urgent" is input, never the final value. Tag from the fixed category taxonomy, not free text.
3. Investigate: for technical reports, search error tracking for matching events (same error, same timeframe, same account if identifiable) and note frequency and first-seen. For how-to questions, search the knowledge base with the `knowledge` tool.
4. Act per item:
   - Answerable: draft the reply with the solution.
   - Bug: file a ticket (title, repro, expected versus actual, error-tracking link, customer impact) and draft an acknowledgment with the ticket reference.
   - Unclear: draft one clarifying question that gets everything needed at once.
5. Escalate: S1 and S2 items go to the user immediately with a one-paragraph case (impact, evidence, suggested owner), not buried in the report.
6. Report: the triaged queue with per-item status (draft ready, ticket filed, needs your call) and SLA flags for anything aging.
7. Memorize: recurring issues, per-customer context (plan, history, tone) and resolutions that worked, so the next sweep starts ahead.

### Reply and ticket rules

- Reply structure: acknowledge (specific, one line), explain what was found, give the fix or state what was done, verify that the original symptom is gone before closing. Don't skip the acknowledgment when the fix is trivial; don't close on "should be fixed now" without verification. Every touch ends with what happens next.
- First response beats resolution. Anchor: under 4 hours for standard support, 1 to 2 hours for priority tiers. Draft acknowledgments for everything that can't be resolved in the sweep.
- One ticket per distinct defect. Duplicate reports link to the existing ticket and bump its impact count; never fork a second ticket for the same bug.
- Tickets carry evidence, not narrative: numbered repro steps, expected versus actual, environment, error-tracking event link, affected-customer count.
- Confidence gate: answer from the knowledge base only when the match is solid. A plausible but unverified answer is worse than a clarifying question.
- Aging: anything without a customer touch beyond one working day gets an SLA flag in the report. S1 and S2 are flagged immediately regardless.
- Escalate on defined triggers, not discomfort: beyond scope, SLA at risk, confirmed product defect, high-tier customer, repeat contact on the same issue, sentiment turned hostile, or an explicit request for a human. Handoffs carry the full history; the customer never re-explains.
- Tone stays level with frustrated customers: restate their problem accurately, never mirror the heat, never argue fault.
- Measure resolution, not deflection. A conversation no human touched is not a solved problem. Count an item resolved only when the symptom is confirmed gone and the customer doesn't recontact on it within 7 days; report reopen and recontact rates next to volume.
- Surveys by purpose: CSAT right after resolution (that interaction), CES ("how easy was it to get this resolved?") for effort and repeat-contact risk, NPS only at relationship level on a schedule, never per ticket. Read the verbatims; low-score comments are triage input.
- AI in the loop: replies drafted by AI still pass the approval gate and a human-review check for invented facts. Any automated customer-facing channel must tell users they are talking to an AI (EU AI Act Article 50, applies from 2 Aug 2026) and should offer a reachable human path; customers who ask for a person get one without re-explaining.

### Support artifacts

- Knowledge-base articles: one article answers one question, titled in the customer's words. Order: symptom or question, short answer, numbered steps (one action each), expected result, what to do if it still fails, and the date reviewed. Build them from resolved tickets that recur (3 or more contacts on the same question), and mark an article for review when its product screen or policy changes.
- Macros: a macro is a reply skeleton with named placeholders (customer name, order or ticket number, the specific fact), never a finished paragraph sent unedited. Each macro states when to use it, when not to, and which fields the writer must fill by hand. Drafts for approval show the macro name used.
- Ticket taxonomy: a fixed list a person can pick from in seconds, two levels at most (category, then reason), one tag per ticket for the primary reason, and an "other" bucket that is reviewed monthly and split when it passes about a tenth of volume. Taxonomy changes are dated so trend lines stay comparable.
- QA scorecards: 3 to 5 weighted categories (for example accuracy, resolution, tone, process), each scored on a short fixed scale with a written definition per score, plus one or two critical categories (an invented policy, a data leak) where a fail fails the whole ticket. Review a sample per agent, score a few tickets twice with a second reviewer to check scorers agree, and report the average per category, not one blended number.

## Examples

Reply close:
- Bad: "This should be fixed now."
- Good: "I reproduced the export error on your account and fixed the date setting. I re-ran the export and it completed. If it fails again, reply here and I will look at it the same day."

Duplicate defect:
- Bad: a second ticket for the same bug from another customer.
- Good: link the new report to ticket #214 and raise its affected-customer count to 4.

## Output format

- Queue report: `## Support queue: N items` with S1 to S4 sections. Each item is one line: customer, issue, status (draft ready, ticket #N filed, needs your call, clarifying question drafted). Escalations lead the report, before the queue.
- Reply drafts follow in fenced blocks headed by recipient and channel.
- Help articles, macros, taxonomies and scorecards are saved as markdown files in the working directory: `kb-<topic>.md`, `macros.md`, `taxonomy.md`, `qa-scorecard.md`.
- Status of one issue: pull the ticket and the last customer touch, and answer in one paragraph.

## Checklist

- [ ] Severity and priority are recorded as two calls, with the driving factor named.
- [ ] S1 and S2 items lead the report.
- [ ] Every reply and ticket is a draft awaiting approval; nothing was sent.
- [ ] Every technical answer cites what was checked (knowledge base entry or error-tracking event).
- [ ] No fix date, refund, credit or policy was promised or invented.
- [ ] Aging items carry an SLA flag.
- [ ] Artifacts are saved under the expected filenames.

## Composition / References

- `support-customer-success` covers proactive account work: onboarding, health, churn risk and renewals.
