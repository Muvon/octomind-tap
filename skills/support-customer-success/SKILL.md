---
name: support-customer-success
title: "QBR Prep, Health Scores and Churn Risk for CS"
description: "Onboards customers to first value, scores account health, runs churn-risk save plays, prepares quarterly business reviews (QBRs) and T-90 renewals."
license: Apache-2.0
compatibility: "Needs a customer record (CRM or supplied account data). Outbound email and calendar holds are drafts until the user approves them."
capabilities: customer-management calendar filesystem-read filesystem-write
domains: support-agent
rules:
  - match((?i)\b(churn\w*|at[- ]risk|save\s+plan)\b.{0,60}\b(save|plan|risk|accounts?|play|renew\w*)\b)
  - match((?i)\b(renewals?\s+(brief|forecast|readiness|prep\w*|checklist|plan)|forecast\w*.{0,30}renewals?|t-90|renew\w*\s+(in|due|ends?))\b)
  - match((?i)\b(qbr|ebr|business\s+review|health\s+scor\w+|score\s+the\s+health|account\s+health|voice[- ]of[- ]customer)\b)
  - match((?i)\b(onboarding\s+plan|first\s+value|30-60-90)\b)
  - match((?i)\bexpansion\s+(conversation|timing|ready\w*)\b|\bready\s+for\s+(an\s+)?expansion\b)
  - match((?i)\b(usage|logins?|adoption)\b.{0,40}\b(dropp\w+|declin\w+|fell|tanking|lagging|down)\b)
  - match((?i)\b(champion|sponsor|admin)\b.{0,40}\b(left|quit|moved)\b)
  - semantic(score the health of my customer accounts and find who might churn, 0.77)
  - semantic(prepare a quarterly business review and renewal brief for this client)
  - semantic(build an onboarding plan so new customers reach first value fast, 0.74)
---

## Overview

This skill runs the proactive side of support for recurring-revenue businesses. Instead of waiting for tickets, it makes sure paying customers reach the value they bought: onboarding to first value fast, spotting churn risk while it is still saveable, preparing renewal and expansion conversations, and telling the truth about account health. Retention is earned in the boring weeks, not in the panicked renewal month. The outcome is a verdict with evidence, plays with owners and dates, and drafts for approval.

## Mental model

A health score is a claim with evidence, never a gut feeling laundered through a number. Health opinions without account data are astrology, so every judgment starts from the customer record.

## Rules

### Procedure

1. Ground in the account: pull the customer record from the connected CRM plus memory before any judgment: plan, tenure, contacts, past issues, available usage signals.
2. Segment the motion: high-touch (named CSM rhythm), low-touch (scheduled checkpoints) or tech-touch (automated with human triggers) by revenue and complexity. High-touch rituals on a thousand small accounts kill the team; tech-touch on the biggest account kills the account.
3. Onboard to value: define first value in the customer's terms (their measurable outcome, not "completed setup"), the shortest path to it, and owners and dates on both sides. Time-to-first-value is one of the strongest leading indicators of renewal; track it per account.
4. Score health honestly, using the components below.
5. Run the plays: risk signals trigger save plays; healthy usage growth triggers expansion timing; every renewal is prepared 90 days out, not 9. All customer-facing emails are drafted for approval; calendar holds for check-ins and business reviews are created only on approval.
6. Close the loop: recurring themes go to a voice-of-customer summary (what to build, what confuses, what delights). Account facts and play outcomes go to memory with the user's confirmation.

### Health score components

Weight them by what predicts this business's churn.

- Usage breadth (seats active over seats bought) and depth (core feature adoption, not logins).
- Engagement: responds to check-ins, attends reviews.
- Relationship coverage: at least 2 champions; single-threaded is fragile.
- Support sentiment: ticket tone and recurrence, not just count.
- Billing hygiene: late payments are a leading indicator.

Trend beats level: 60 and rising outranks 80 and falling. A vendor- or AI-generated health score is a hypothesis: check it against these raw signals before acting, and back-test weights against accounts that actually churned.

### Churn signals, ranked by urgency

1. Champion left or went quiet (the number one killer): re-establish coverage within two weeks.
2. Usage decline of 30% or more over 30 days.
3. The gap between seats bought and seats active widening.
4. Renewal-adjacent silence: unanswered outreach in the 90-day window.
5. A competitor mentioned in tickets.
6. A sponsor-level org change: a new executive means re-selling the value.

Every signal maps to a play with an owner and a date. A flagged risk without a next step is just anxiety.

### Save plays

Diagnose before medicating: is the problem value (never reached it), usage (reached it, then drifted), relationship (people changed) or budget (value fine, money gone)? The play differs:

| Problem | Play |
|---|---|
| Value | Restart onboarding on their outcome |
| Usage | Re-embed the workflow with their team |
| Relationship | Multi-thread and re-sell up the chain |
| Budget | Right-size honestly: a smaller live account beats a churned logo, and honesty here buys the win-back |

Discounts are the last lever, not the first: a discount that papers over absent value churns anyway, a year later and cheaper. When value truly isn't there, "let them go well" is a valid outcome.

### Business review preparation

Use their outcomes, not our features: what they wanted, what the data shows, gaps and the joint plan, then what is coming that maps to their goals. Produce a deck-ready summary with the customer's numbers in it. If there has been no measurable value, the review says so and becomes a recovery plan: customers respect honesty and smell theater.

### Renewals and expansion

- Renewal prep at T-90: health verdict, value evidence assembled, risks with plays running, pricing-change context.
- Forecast in three honest buckets: safe, at-risk (with the risk named) and likely-lost (with the lesson).
- Report gross revenue retention (churn and downgrades only) next to net revenue retention. Expansion must not hide a leaking base.
- Time expansion by value evidence (usage at plan ceiling, a new team asking, outcome achieved), never by quarter-end. Pushing expansion on an unhealthy account converts one churn into two.

## Examples

Health claim:
- Bad: "The account looks healthy."
- Good: "Watch, trending down: 62 of 100 seats active (was 81 in March), one champion, two late invoices. Play: re-embed with the finance team by 15 Dec, owner Sam."

Cancellation request:
- Bad: "Offer 30% off to keep them."
- Good: "Diagnose first. Usage is steady but the sponsor left in October: this is a relationship problem. Multi-thread to the new VP before any pricing talk."

## Output format

- Account review: verdict (healthy, watch or at-risk, plus trend), evidence lines, then plays with owners and dates.
- Onboarding plan: `onboarding-<account>.md` with both-sides owners and the first-value definition on top.
- Business review prep: `qbr-<account>-<date>.md`.
- Portfolio review: a table with account, score, trend, top signal, play and renewal date.
- Customer-facing drafts in fenced blocks headed by recipient, awaiting approval.

## Checklist

- [ ] The verdict rests on account data, and the data used is named.
- [ ] Health components and trend are shown, not a bare score.
- [ ] A churn risk is diagnosed as value, usage, relationship or budget before a play is chosen, and no play leads with a discount.
- [ ] Every signal has a play with an owner and a date.
- [ ] Renewals are prepared at T-90 and the forecast uses the three honest buckets.
- [ ] Expansion is proposed only for demonstrably healthy accounts.
- [ ] No message was sent and no calendar hold created without approval.

## Composition / References

- `support-ticket-desk` covers reactive queue work: triage, replies and tickets.
