---
name: launch-gtm-plan
title: "Go-to-Market Plan: Beachhead ICP, Motion and Channels"
description: "Write a go-to-market plan: beachhead ICP, sales motion, channel tests, launch gates and metric stack with kill thresholds. Use to decide who to sell to."
license: Apache-2.0
compatibility: "Needs web search for category and channel research. Any OS."
rules:
  - match((?i)\b(go[- ]to[- ]market|gtm)\b)
  - match((?i)\b(beachhead|ICP|ideal\s+customer\s+profile)\b)
  - match((?i)\b(plg|product[- ]led|sales[- ]led)\b)
  - match((?i)\b(channel\s+mix|test\s+budgets?|acquisition\s+channels?|marketing\s+channels?)\b)
  - match((?i)\blaunch\s+(gates?|phases?|sequence)\b|\b(entry|exit)\s+(and\s+(entry|exit)\s+)?gates?\b|\b(beta|early\s+access)\b.{0,40}\bGA\b)
  - match((?i)\bkill\s+thresholds?\b|\bsales\s+motion\b|\bmotion\s+fits?\b)
  - match((?i)\bsegment\w*\b.{0,60}\b(first|attack|prioriti\w+)\b|\b(self[- ]serve|sales\s+reps?)\b.{0,40}\b(or|versus)\b)
  - semantic(who should we sell to first and through which channels)
  - semantic(write a go-to-market plan with launch gates and success metrics, 0.76)
  - semantic(pick our ideal customer profile and the sales motion that fits, 0.69)
  - semantic(which segment should we attack first and what channel tests to run)
---

## Overview

Turn a validated product into a plan: who to sell to first, which sales motion carries the deal, which channels earn priority, how launch phases sequence, and which numbers prove or kill the plan. Reason from segment economics and buyer behavior, not fashion or analogy. Every recommendation names the assumption it rests on and the trigger that would change it. The plan does not write messaging, copy or creative, publish or send outreach, or validate an idea; zero-budget organic launch execution is covered by the `organic-launch` skill.

## Mental model

Commit to one beachhead and one lead motion; don't bury the plan in hedges. A motion nobody has run by hand can't be systematized, so founders close the first ten deals manually before hiring or automating. Keep the plan executable by whoever writes the brand, pitch and ads without the strategist in the room.

## Rules

### Process

1. Ingest: product, stage, pricing or ACV hypothesis, time-to-value, and any exploration or validation findings. remember(["ICP", "GTM plan", "sales motion", "channels"]) for prior decisions. If pricing is undecided, state the ACV assumption the motion will rest on and flag it as the first thing to validate.
2. Research with independent web searches in parallel: how comparable products go to market, where the buyers actually gather, typical ACV and sales-cycle length for the category, and what the current alternative (incumbent, spreadsheet, doing nothing) costs the buyer.
3. Segment: score 2-4 segments on pain severity, reachability, willingness to pay and a compelling event (something that forces a purchase this quarter). Pick one beachhead and say why the others wait.
4. Choose the motion: apply the motion matrix to their ACV, time-to-value and buyer shape; state the trigger that would change the answer. Sales-led: map the buying committee (champion, economic buyer, technical evaluator, likely blocker). Product-led: define the activation event and the PQL threshold.
5. Pick channels: list every plausible channel, shortlist three cheap tests with a budget and a success bar each, and commit to concentrating on the one that clears its bar. Coordinate channels around shared account triggers so paid, outbound and content hit the same accounts in the same window instead of running as silos.
6. Sequence and instrument: phase the launch with entry and exit criteria, and set the metric stack with targets and pre-committed kill thresholds.
7. Deliver the plan file, then memorize() the ICP, motion, channel and threshold decisions.

### Motion matrix

| Signal | Lead motion |
|--------|-------------|
| ACV under ~$5k/yr, value felt within minutes of signup, individual or small-team buyer | Product-led: free tier or trial carries acquisition; sales touches PQLs only |
| ACV ~$5-50k, some configuration or integration, a manager signs | Hybrid: PLG generates PQLs, inside sales converts and expands |
| ACV over ~$50k, months-long cycle, committee buys, procurement and security review | Sales-led: outbound and ABM, demo gated; founder-led until the win pattern repeats |
| Buyer lives inside an ecosystem (Shopify, Salesforce, AWS, HubSpot) | Partner-led lane alongside the primary motion |

Most B2B products run hybrid. The question is which motion leads, not which exists.

Buyers research before they talk (Gartner, 2026: 67% of B2B buyers prefer a rep-free experience and 45% used GenAI in a recent purchase, yet most still want a rep to validate what AI told them). Every motion therefore needs self-serve proof: public pricing or a pricing logic, docs, comparisons, a trial or sandbox, written so AI assistants describe the product accurately, with reps placed at validation and risk-removal moments rather than at first contact.

### Beachhead ICP

A beachhead ICP is narrow enough to name 50 real accounts and specific enough that the current alternative is the same for all of them. If you can't, narrow it. Define the segment through firmographics plus live signals (hiring, funding, tech installed, compelling events), and tier the accounts.

### Launch gates

- Beta exits when design partners reach the activation event and keep using the product (retention, not enthusiasm).
- Early access exits when the chosen motion has closed several ICP accounts the same way (a repeatable win pattern) and pricing has survived real objections.
- General availability requires packaging frozen, onboarding and support ready, and the metric stack live.

### Metric stack

Four layers: pipeline quality (ICP-fit share of pipeline and of closed-won), conversion velocity (stage-to-stage rate and days per stage), retention economics (net and gross revenue retention, CAC payback in months), and channel mix (CAC and win rate by channel). Kill thresholds are written before launch, not after a bad month. Vanity counts (impressions, raw signups, followers) never appear as targets.

### Estimates and conduct

- Label every market figure an estimate with its assumption; flag anything you could not source. Name the assumption under every number and define the trigger that would change each decision.
- Don't pick a motion by analogy to a famous company, and don't promise channel results without a test budget and success bar.
- Raw unvalidated idea: validate it first; strategy on an unvalidated idea is fiction.
- "Who should we sell to?": segmentation plus a beachhead with named example accounts.
- "PLG or sales-led?": apply the motion matrix to their numbers; ask for ACV and time-to-value if missing.
- Traction data shared: recalibrate the plan against actuals before extending it.
- Vague request: ask one question, "What's the product, and what does one paying customer look like today?"

## Output format

Save the plan as `gtm-plan-[product].md`.

```markdown
# GTM Plan: [Product]

## Positioning Assumed
[One line: for <beachhead>, facing <situation>, the product is the <category> that <key outcome>, unlike <current alternative>. Messaging itself belongs to the brand identity work.]

## Beachhead ICP
[Segment, firmographics, live signals, compelling event, current alternative, 10 example accounts; which segments wait and why]

## Motion
[Lead motion plus supporting motions, with the economics that justify them; buying committee (sales-led) or activation event and PQL threshold (product-led)]

## Channel Mix
| Channel | Role | Test budget and success bar | Who executes | First 90 days |

## Launch Sequence
[Beta -> early access -> GA: entry and exit criteria per phase]

## Metric Stack
[Four layers, targets, kill thresholds]

## Assumptions & Risks
[Every estimate with its source or its flag; the ACV assumption first if pricing is undecided]

## Handoffs
[What the brand, pitch and ad work take from this plan, with inputs for the organic launch playbook, plus the inputs for outbound-system, partner and growth work]
```

## Checklist

- [ ] One beachhead named with 10 example accounts and the reason the other segments wait?
- [ ] One lead motion chosen from the matrix with a stated change trigger?
- [ ] Each channel test has a budget and a success bar?
- [ ] Entry and exit criteria for every launch phase, and kill thresholds written before launch?
- [ ] Every number carries its assumption; the ACV assumption flagged first if pricing is undecided?
- [ ] Plan saved as `gtm-plan-[product].md`?

## Composition / References

- `organic-launch` skill: turns the chosen strategy into a zero-budget launch playbook.
- `launch-brand-identity` skill and `launch-pitch-pricing` skill: take the segment and positioning assumption from this plan.
- `launch-idea-validation` skill: comes first when the idea is unvalidated.
