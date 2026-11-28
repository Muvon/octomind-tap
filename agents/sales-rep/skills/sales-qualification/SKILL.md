---
name: sales-qualification
title: "MEDDPICC, BANT and SPICED Sales Qualification"
description: "Sales qualification frameworks MEDDPICC, BANT, SPIN and SPICED: when to use each and exit criteria per deal stage. Use when scoring or advancing a deal."
license: Apache-2.0
compatibility: "Environment-independent. Works with any CRM or a plain notes file."
rules:
  - content(meddpicc)
  - content(meddic)
  - content(bant)
  - content(spiced)
  - match((?i)\b(economic buyer|paper process|mutual action plan)\b)
  - match((?i)\b(\d+% off|indecision|think it over|brush-?off|just send (me )?a (proposal|quote)|circle back)\b)
  - match((?i)\b(discovery|demo)s?\b.{0,40}\b(call|meeting|questions?|recap|feature tour)\b|\b(spin|gap selling)\b)
---

## Overview

A qualification framework is a checklist of facts a deal needs before it deserves more of the rep's time. This skill puts four of them in one place: MEDDPICC, BANT, SPIN and SPICED. It says when to pick each, what counts as evidence, and what must be true for a deal to leave each stage. The result is one qualification vocabulary across discovery, closing and CRM work.

## Mental model

The frameworks do different jobs, so they are not alternatives.

- BANT filters leads: is this worth a conversation at all.
- SPIN and SPICED shape the conversation that finds the facts.
- MEDDPICC records the facts and shows what is still unknown.

Use a conversation framework to ask, and MEDDPICC to write down. A gap in MEDDPICC is a first-call question for the next meeting, never a guess.

## Rules

### Framework table

| Framework | Origin | Elements | Use it when | Do not use it for |
|-----------|--------|----------|-------------|-------------------|
| BANT | IBM | Budget, Authority, Need, Timeline | First filter on inbound or list leads; short transactional deals | A first-call interrogation or a hard disqualifier: budget and authority are often created during a deal |
| SPIN | Rackham, 1988 | Situation, Problem, Implication, Need-payoff | Structuring discovery questions; large or complex sales | Recording deal state; it has no field for buyer, process or competitor |
| SPICED | Winning by Design | Situation, Pain, Impact, Critical Event, Decision | Recurring-revenue (subscription) deals; discovery notes and handoffs to customer success | Multi-department enterprise deals alone: it has no paper-process or competition element |
| MEDDIC | PTC, 1990s | Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion | Never as a separate choice: it is MEDDPICC without two letters | |
| MEDDPICC | MEDDIC plus Paper Process and Competition | Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, Competition | Complex deals with several stakeholders, legal or security review, or a named competitor | Simple deals that close in one call; the paperwork costs more than it protects |

One name per team. Write MEDDPICC for all eight letters. Do not mix MEDDIC and MEDDPICC in the same CRM.

### Choosing

1. Inbound or list lead, one stakeholder, price under what one person can approve: BANT as a quiet checklist, then SPIN or SPICED in the call.
2. Recurring-revenue product with a trial or a short sales cycle: SPICED for discovery, MEDDPICC fields once a second stakeholder appears.
3. Several stakeholders, legal or security review, or a named competitor: SPIN to ask, MEDDPICC to record, from the first call.

### Evidence rule

Each MEDDPICC element has a score:

- 0: unknown.
- 1: the rep says so, with no buyer statement or document behind it.
- 2: evidenced by the buyer's own words, an email, a document, or a named person confirmed on a call.

Write the evidence in the buyer's words next to the score. A score of 1 counts as a gap.

| Element | Evidenced (score 2) looks like |
|---------|-------------------------------|
| Metrics | A number with a unit and a baseline the buyer stated, such as "returns cost us 40 hours a month" |
| Economic Buyer | A named person who controls the budget and can sign; the rep has met them or has seen them approve something |
| Decision Criteria | The buyer's own written or spoken list of what the choice is judged on |
| Decision Process | Steps in order, with owners and dates, back to the signature |
| Paper Process | Who reviews legal terms, security and procurement, how long each took last time, who signs |
| Identify Pain | A problem the buyer says costs money, time or risk now, tied to a Metric |
| Champion | A person with influence and access to the Economic Buyer who has done something that costs them effort or risk, such as an introduction or sharing internal information; a friendly contact who only gives information is a coach, not a champion |
| Competition | Every alternative named, including the status quo, with the buyer's view of each |

### Stage exit criteria

A deal moves forward only when every item for its next stage scores 2. If an item cannot be reached, the deal stays where it is or is disqualified. These are working gates; adjust the stage names to the team's CRM and keep the logic.

| Move | Must be true |
|------|--------------|
| Lead to discovery call | BANT hypothesis: a role close to the problem and a plausible reason to talk. No need for confirmed budget |
| Discovery to qualified | Identify Pain and Metrics at 2; Economic Buyer named; a Champion candidate identified; next step booked with a date |
| Qualified to evaluation | Decision Criteria written down; Decision Process steps with dates; Competition named including the status quo; Champion has done one costly action |
| Evaluation to proposal | Economic Buyer has been met or has confirmed the criteria through the Champion; Decision Process dates match a Critical Event (a dated event that forces a decision, such as a contract expiry or a launch) |
| Proposal to close | Paper Process mapped with dates; mutual action plan agreed; signatory confirmed |

A clean disqualify is a valid exit. Write the reason in the CRM so the lead is not worked again for the wrong reason.

### SPIN and SPICED mapping

| Conversation framework | Fills this MEDDPICC field |
|------------------------|---------------------------|
| SPIN Problem | Identify Pain |
| SPIN Implication and SPICED Impact | Metrics |
| SPIN Need-payoff | Decision Criteria, in the buyer's words |
| SPICED Critical Event | Decision Process dates |
| SPICED Decision | Decision Process, Economic Buyer |

### Where it applies

- Discovery: choose the framework and run the conversation.
- Closing: check the paper process, the economic buyer and the champion before advising a move.
- CRM work: map each element to a CRM field and enforce the stage gates.
- Pipeline review: diagnose the real stage of a deal.

## Examples

Bad: "Champion: Dana, loves us." Score 1: no costly action recorded.

Good: "Champion: Dana, ops lead. Booked the CFO for the 14 Nov call and sent the current vendor contract. Score 2."

Bad stage move: deal to proposal with "Economic Buyer: probably the VP". Score 1.

Good stage move: deal stays in evaluation; next step is "ask Dana to put the CFO on the 14 Nov call".

## Checklist

- [ ] One framework name used across the team, MEDDPICC for all eight letters?
- [ ] Each element scored 0, 1 or 2, with the buyer's words next to the score?
- [ ] No stage advance with a score below 2 on that stage's items?
- [ ] BANT used as a quiet filter, never as a first-call interrogation?
- [ ] Gaps written as questions for the next meeting?
- [ ] Disqualified deals closed with a recorded reason?

## Composition / References

- Pair with `outreach-cold-copy` for first touches, and with `outreach-compliance` for call-recording consent before any discovery or demo call is recorded.
- MEDDPICC elements: https://www.exec.com/learn/meddpicc-the-complete-guide (checked 2026-11-15; vendor guide, no single authoritative standard exists).
- SPICED: https://winningbydesign.com/the-spiced-framework/ (checked 2026-11-15).
- SPIN: Rackham, "SPIN Selling", 1988.
