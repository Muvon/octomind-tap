---
name: sales-closing
title: "Handling Sales Objections and Sales Negotiation"
description: "B2B closing: handling sales objections, negotiation, stalled deals, mutual action plans, concession trades, win/loss review. Use for late-stage deals."
license: Apache-2.0
compatibility: "Environment-independent. Memory helps track a deal and what was tried."
rules:
  - match((?i)\b(close|closing|advance|save|rescue|unstick)\b.{0,30}\b(deal|opportunity|contract)\b)
  - match((?i)\b(handle|overcome|respond to|deal with)\b.{0,20}\bobjections?\b)
  - match((?i)\bnegotiat(e|ing|ion)\b.{0,30}\b(price|pricing|terms|contract|deal|discount)\b)
  - match((?i)\b(wants?|asks? for|asking for|demands?)\b.{0,20}\b(a )?(discount|\d+% off)\b)
  - match((?i)\b(stalled|stuck|ghosted)\b.{0,30}\b(deal|buyer|prospect|opportunity)\b|\b(went quiet|gone dark|needs? to think about it)\b)
  - match((?i)\bwin[/ -]?loss\b.{0,15}\b(review|interview|analysis)\b)
  - semantic(the buyer wants a discount, how should I negotiate the terms, 0.77)
  - semantic(handle this objection from the buyer about price and timing, 0.69)
  - match((?i)\b(prospect|buyer|customer|procurement|cfo|vp)\b.{0,60}\b(circle back|maybe next quarter|think (it )?over|too high|\d+% off|just send (me )?a (quote|proposal))\b)
  - match((?i)\b(respond|reply|answer|counter|push back)\b.{0,40}\b(discount|price objection|too high|too expensive|brush-?off|circle back|think (it )?over)\b|\b(jolt|indecision|brush-?off|mutual action plan|concession)\b)
---

## Overview

This skill turns late-stage stalls, indecision and "send me a proposal" brush-offs into signed contracts while protecting margin instead of reflexively discounting. It stops reps from talking themselves out of deals. High-pressure closing lowers win rates on complex deals, so the approach is honest and gives the rep verbatim words plus the buyer's likely counter.

## Mental model

- Protect margin: trade concessions, never give them away.
- The real blocker is usually not the stated one. Objection, stall, indecision, terms negotiation and single-threading need different moves.
- A buyer who is indecisive fears making a mistake. Reduce that risk instead of re-selling.

## Rules

### Workflow

1. Diagnose the deal: stage, last interaction, who is in the room, the exact words the buyer used, and what the rep wants (advance, negotiate or close).
2. Name the blocker: an objection (price, value, timing, authority, risk), a stall, indecision or no-decision, a terms negotiation, or a single-threading gap. Don't accept the rep's first label.
3. Map the process: confirm the economic buyer, the compelling event, the decision steps and the paper process (legal, security, procurement, signatory) using the `sales-qualification` skill's MEDDPICC evidence scores and stage exit criteria. Identify what a mutual action plan would expose.
4. Prescribe the move: the specific technique and the actual words, such as a calibrated question, a label, an up-front contract for the next call, a concession trade or a JOLT de-risking offer.
5. Role-play: give the verbatim phrasing, the buyer's likely counter and the rep's response, so it is rehearsed, not improvised.
6. Define the next commitment: never end without a concrete next step the rep will secure, such as a dated milestone, a signed mutual action plan or an exec intro.

Track the deal and what has been tried in memory.

### Frameworks

| Framework | Originator | Use it for |
|-----------|------------|------------|
| LAARC | Castleberry and Tanner | Objection: Listen, Acknowledge, Assess (diagnose the real one), Respond, Confirm |
| Sandler | David Sandler | Up-front contract (agree the meeting's decision); pain funnel; no free consulting |
| Mutual action plan | Enterprise-sales practice | Co-built plan working back from a compelling event, with named owners, dates and legal, security and procurement steps |
| JOLT effect | Dixon and McKenna, 2022 (2.5M+ recorded sales conversations) | Beat indecision: Judge it, Offer a recommendation, Limit options, Take risk off the table (pilots, opt-outs) |
| Tactical empathy | Chris Voss | Labeling, mirroring, accusation audit, calibrated how and what questions; never split the difference |
| Challenger | Dixon and Adamson, 2011 | Teach a reframing insight, tailor to the stakeholder, take control of the money conversation |
| SPIN (prevention) | Rackham, 1988 | Implication and Need-payoff questions build value early so fewer objections arise at close; the `sales-qualification` skill holds the full SPIN and MEDDPICC definitions |
| Win/loss review | Win-loss research practice | After a closed-won, closed-lost or no-decision deal, ask the buyer why, in the buyer's words (below) |

In the JOLT research, re-selling value or raising fear of missing out on an already-intent but indecisive buyer usually backfires: the fear is of making a mistake, so reduce that risk instead. Create urgency only from a real compelling event, never fabricated scarcity.

### Win/loss review

- Interview the buyer, not the rep, soon after the decision. Prefer someone who was not on the deal, because buyers soften criticism to the seller.
- Ask the same questions each time: what problem started the search, who was involved, which options were considered, what decided it, what nearly changed the decision, what the seller got wrong.
- Code each answer to a reason (price, product gap, trust, timing, champion, no-decision, competitor) and count by reason across deals.
- One vendor guide suggests 15 to 20 interviews per outcome per quarter before treating a pattern as real (vendor guidance, not a rule).
- Feed patterns to discovery questions, battlecards and pricing, not to individual rep reviews.

### Recording

On any recorded call or AI notetaker, follow the call-recording consent rule in the `outreach-compliance` skill before recording starts.

### Guards

- Don't reflexively discount to save a deal; it trains buyers to expect it and erodes margin across the pipeline.
- Don't use hard-close gimmicks (takeaway, "sign today or the price goes up") on sophisticated B2B buyers; pressure lowers win rates on complex deals.
- Don't keep re-litigating value or pushing harder on an indecisive buyer; de-risk instead.
- Don't manufacture fake urgency or false scarcity, and don't single-thread the deal around one friendly champion.
- Do diagnose the real objection before responding, trade every concession, and build a mutual action plan.
- This is sales coaching, not legal advice. Contract terms, opt-outs and discount thresholds go through legal, finance and deal desk. Keep urgency honest (real compelling events only). Cited win-rate statistics come from specific research populations and won't transfer identically to every deal.

## Examples

- "They loved it, then ghosted": happy ears. Qualify the economic buyer and recruit a champion.
- "I need to think about it": an up-front contract next time, plus a JOLT recommendation and a way to take risk off the table.
- "They want 20% off": trade, don't give. "I can do that if we move to a 24-month term." Anchor on value.

## Output format

- Diagnosis: the real blocker behind the rep's stated one.
- The move: the specific technique and why it fits.
- The words: verbatim phrasing, plus the buyer's likely counter and the response.
- Next commitment: the concrete next step the rep will secure.

Save to `deal-close-[name-slug].md` in the working directory when asked.

## Checklist

- [ ] The real blocker is named, not the rep's first label?
- [ ] Economic buyer, compelling event, decision steps and paper process confirmed?
- [ ] Every concession is traded for something?
- [ ] Verbatim words and the buyer's likely counter are included?
- [ ] A dated next commitment and a second contact are set?

## Composition / References

- `sales-qualification` skill: MEDDPICC evidence scores and stage exit criteria.
- `outreach-compliance` skill: call-recording consent.
- `sales-discovery` skill: building value early so fewer objections arise at close.
