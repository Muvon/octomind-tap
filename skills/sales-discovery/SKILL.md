---
name: sales-discovery
title: "Sales Discovery: SPIN, Gap Selling and Demo Framing"
description: "B2B discovery calls and demos: pre-call prep, SPIN questions, quantified pain, MEDDPICC gaps, battlecards. Use to prepare or review a discovery call."
license: Apache-2.0
compatibility: "Environment-independent. Web search and memory help with account research and deal notes."
domains: sales-rep
rules:
  - match((?i)\bdiscovery (call|calls|questions?|meeting|process)\b)
  - match((?i)\b(prep\w*|plan|structure|frame|improve)\b.{0,30}\bdemos?\b)
  - match((?i)\b(tire[- ]?kickers?|happy ears)\b)
  - match((?i)\b(battlecards?|talk[- ]to[- ]listen)\b)
  - semantic(find the buyer's real pain and qualify the prospect on a first call, 0.72)
  - semantic(plan the demo so it focuses on the buyer's quantified pain, 0.70)
  - semantic(which MEDDPICC fields are still missing on this opportunity)
  - semantic(build a battlecard against a competitor the prospect is considering)
  - semantic(write SPIN implication questions to uncover and quantify the buyer's pain, 0.71)
  - semantic(coach a rep on a recorded discovery call transcript, 0.69)
---

## Overview

Discovery stops reps from burning cycles on deals that were never real. It uncovers quantified pain, qualifies the deal against a hard checklist, and turns the demo into a recap of the buyer's own problem instead of a feature parade. A clean disqualify is a good outcome, not a failure.

## Mental model

- Be diagnostic and buyer-centric: listen more than you talk.
- Push past the rep's first label; the first stated problem is rarely the real one.
- Pain counts only when the buyer has put a number on it.

## Rules

### Call workflow

1. Pre-call prep: research the account and persona so you skip basic Situation questions. Set one or two hypotheses about likely pain and the job to be done. Expect the buyer to arrive pre-researched (Gartner, 2026: 45% used GenAI in a recent purchase, and most want a rep to validate what it told them). Plan to ask what they have already concluded and correct it with evidence.
2. Open: state an agenda and get confirmation. Establish the buyer's role: are they the economic buyer or a path to one.
3. Diagnose (the core, more than half of it listening): SPIN. Ask minimal Situation questions, then Problem, then Implication to quantify the business cost, then Need-payoff to let the buyer voice the value. Map current state against the buyer's self-described future state and size the gap. Chase the why behind the why.
4. Qualify: use the `sales-qualification` skill. Score each MEDDPICC element 0, 1 or 2 against the buyer's own words, flag gaps as risk, and check the stage exit criteria before deciding advance or disqualify.
5. Advance and demo: lock a concrete, calendared next step. When demoing, use Tell-Show-Tell: lead with the worst pain you found, show only the three to five features that resolve it, and recap the value in the buyer's numbers.

Carry deal context and qualification gaps between calls in memory.

### Frameworks

| Framework | Originator | Use it for |
|-----------|------------|------------|
| SPIN, MEDDPICC, SPICED, BANT | Rackham 1988; PTC 1990s; Winning by Design; IBM | Elements, when to use each, and stage exit criteria: the `sales-qualification` skill. SPIN structures the questions; MEDDPICC records the answers |
| Gap Selling | Keenan, 2018 | Current state (problem, impact, root cause, emotion) against future state; size the gap; diagnose root cause |
| Jobs To Be Done | Moesta and Spiek; Christensen | Forces of Progress: push plus pull must beat anxiety plus habit for a deal to move |
| Tell-Show-Tell | Riefstahl | Demo: set up the pain, show the one capability that resolves it, recap the value |

### Talk time and happy ears

Gong's 2016 analysis found top performers talk about 43% of the call. Its 2025 analysis of 326,000 calls found won deals averaged 57% rep talk time against 62% on lost deals. Track talk time per call and coach to the pattern in your own won deals, not to a fixed ratio.

Happy ears means treating nodding and enthusiasm as buying signals; it is how reps misforecast. A champion (power plus influence) is not the same as a friendly coach who only gives information.

### Battlecard

Keep one page per named competitor, the status quo included, with:

- when they win and when they lose;
- the buyer's stated view of them;
- three discovery questions that expose their weak spots without naming them;
- proof points with source;
- claims we must not make about them;
- a last-reviewed date.

Replace a card that is older than one quarter, or after any lost deal against that competitor.

### Recording

On any recorded call or AI notetaker, follow the call-recording consent rule in the `outreach-compliance` skill before recording starts.

### Guards

- Don't open with a budget or authority interrogation; it feels like a survey and kills rapport.
- Don't catch happy ears: positive nodding is not a buying signal until pain is quantified and objections surface.
- Don't feature-dump or give a full product tour; an unfocused demo overwhelms and is forgotten.
- Don't supply the buyer's future state for them; if you tell them their outcome, you are pitching, not selling.
- Don't end a call without a concrete, scheduled next step.
- Do listen more than you talk, quantify pain with Implication questions, and confirm the economic buyer and a real champion.
- This is process coaching, not legal or procurement advice. Benchmark numbers are directional, not guarantees. Use discovery to diagnose fit honestly, never to manipulate.

## Examples

- "Demo went great, then they ghosted": happy ears. Quantify the pain and confirm the economic buyer.
- "How do I spot tire-kickers early?": quantify pain with Implication questions and qualify with MEDDPICC.
- "Discovery feels like an interrogation": run SPIN conversationally, not as a BANT checklist.

## Output format

Per deal or call, deliver:

- Pain: what was quantified, and what was not yet.
- Qualification: the MEDDPICC elements still unknown.
- Risk: the single riskiest gap.
- Next step: the exact, calendared next-step ask.

Save to `deal-[name-slug].md` in the working directory when asked.

## Checklist

- [ ] Pain has a number, a unit and a baseline in the buyer's words?
- [ ] Every MEDDPICC element scored, with gaps written as questions for the next call?
- [ ] The demo shows only the features that resolve the quantified pain?
- [ ] A dated next step is booked?
- [ ] Call-recording consent handled before recording?

## Composition / References

- `sales-qualification` skill: framework definitions, evidence scores, stage exit criteria.
- `outreach-compliance` skill: call-recording consent.
- `sales-closing` skill: objections and negotiation once the deal is qualified.
