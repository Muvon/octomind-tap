---
name: marketing-growth
title: "Growth Strategy: Activation, PQLs and Experiments"
description: "Plans product-led and hybrid SaaS growth: activation milestones, PQL scoring, funnel diagnosis, growth loops, unit economics and ICE-ranked experiments."
license: Apache-2.0
compatibility: "Needs the user's funnel and cohort numbers; web search helps compare how similar products solved the same leak. Plans only. Any OS."
domains: marketer
rules:
  - match((?i)\bactivation\s+(rate|milestone|metric|funnel|event)s?\b)
  - match((?i)\b(PQLs?|product[- ]qualified\s+leads?|PLG|product[- ]led\s+growth)\b)
  - match((?i)\bgrowth\s+(loops?|plans?|experiments?|backlog|strategy|ideas)\b|\b(experiment|test)\s+(backlog|ideas)\b)
  - match((?i)\b(NRR|net revenue retention|CAC payback)\b|\bICE\b.{0,40}\b(scor\w+|rank\w*|backlog)\b|\b(scor\w+|rank\w*)\b.{0,40}\bICE\b)
  - match((?i)\b(trial-to-paid|free[- ]trial|trial)\b.{0,40}\bconver\w*|\b(where|why)\b.{0,40}\b(people|users)\s+drop\s+off\b)
  - match((?i)\bpredicts?\b.{0,40}\b(conversion|retention|churn)\b|\b(pricing[- ]page|upgrade path)\b.{0,40}\b(tests?|conversion)\b)
  - match((?i)\bchurn\w*\b.{0,80}\b(win-?back|expansion|plan)\b)
  - semantic(define the activation milestone and score product qualified leads, 0.70)
  - semantic(rank growth experiments by impact and ease for our product, 0.72)
  - semantic(explain our churn and expansion numbers and what to do about them)
---

## Overview

Use this skill for what happens after launch: whether signups activate, which users are sales-ready, why accounts expand or churn, and which experiments deserve the next cycle. The outcome is a growth plan file that names the binding constraint, defines activation and PQLs, and ranks the experiments. The work runs from funnel data and cohort behavior, not tactic lists.

## Mental model

Fixing activation usually beats buying traffic, and retention sets the ceiling on everything else. Traffic into a leaky activation flow is acquisition spend set on fire. Find the one constraint (acquisition, activation, retention or monetization) and tie every play to it.

## Rules

### Workflow

1. Ingest: product, funnel numbers, cohort data if any. Recall earlier work on activation, PQL, experiments and the growth plan from memory.
2. Diagnose: locate the binding constraint. Demand real numbers; if none exist, the first deliverable is an instrumentation plan (the events to track and why), not experiments.
3. Define activation: the behavior that correlates with retention (the "aha" milestone), stated as measurable events within a time window.
4. Design plays for the constraint only. Run parallel web searches for how comparable products solved the same leak.
5. Backlog: score candidates with ICE (impact, confidence, ease), sequence the top 5, park the rest.
6. Deliver the plan file, then memorize the activation definition, PQL threshold and backlog.

### Principles

- A PQL (product-qualified lead) needs both scores: product behavior (activation events, usage depth) and fit (ICP match). Behavior without fit is a free-tier tourist; fit without behavior is a cold lead. When the hybrid motion applies, PQLs crossing both thresholds route to sales.
- A growth loop must output its own input: user-created content brings signups who create content; referred users refer. If the chain breaks, it is a channel, which is still fine, but plan its CAC.
- Four lifecycle plays exist from day one, even with 50 customers: onboarding, adoption, renewal, win-back. Specify them here (trigger, audience, goal, success metric); building and sending the emails is separate email work, which the `marketing-email` skill covers.
- Experiments follow the `marketing-experiments` skill: a sample-size check before they run. At low traffic, prefer bigger swings (pricing, onboarding redesign) over button tests that will never reach significance.
- Quantify churn cost before designing expansion: NRR below about 100% means retention plays outrank upsell plays.
- Customer reviews, testimonials and advocacy requests use the `marketing-review-program` skill; confirm the activation milestone first.
- Pre-launch products are not a growth problem yet; growth work starts when users exist.

### Unit economics

Compute per channel and per cohort, with every input labeled measured or assumed:

- CAC = channel spend (ads, tools, and the people time you can attribute) divided by new paying customers from that channel in the same period. Report blended CAC and paid CAC separately.
- CAC payback in months = CAC divided by (monthly revenue per account x gross margin). A common planning threshold for small SaaS is under 12 months; treat it as a benchmark, not a rule.
- LTV = monthly revenue per account x gross margin divided by monthly logo churn. LTV to CAC of about 3 or more is a common benchmark. With fewer than 12 months of cohort data, say LTV is an estimate.
- NRR over 12 months = (starting MRR of the cohort + expansion - contraction - churn) divided by starting MRR, new customers excluded. Gross revenue retention is the same without expansion and cannot exceed 100%.
- Activation milestone method: compare retention at week 8 for users who did event X within N days against those who did not, for several candidate events. Pick the event with the largest gap that most users can reach, then confirm it with an experiment, because the gap alone is correlation.

### Legal floor for trial, renewal and cancellation tests

The FTC's 2024 click-to-cancel rule was vacated by the Eighth Circuit on 2025-07-08, but the FTC enforces the Restore Online Shoppers' Confidence Act (ROSCA) against hard-to-cancel subscriptions (Amazon settled for $2.5 billion in September 2025) and opened a new negative-option rulemaking in March 2026 (as of 2026-11). State auto-renewal laws also apply; California's amendments in force since 2025-07-01 require express consent to the renewal terms, an online cancellation route and annual reminders. Don't test cancellation friction. Flag the jurisdiction question for legal review, and look up the current status before relying on any of this.

## Examples

- "How do we grow?": ask for funnel numbers first, then diagnose before prescribing.
- "Signups don't convert": activation diagnosis plus onboarding play specs.
- "Which users should sales call?": PQL definition with scoring and routing.
- No analytics in place: instrumentation plan.

## Output format

Save as `growth-plan-[product].md`:

```markdown
# Growth Plan: [Product]

## Diagnosis
[The binding constraint, with the numbers that prove it]

## Activation Milestone
[Events + time window, and the retention correlation or hypothesis behind it]

## PQL Definition
[Behavior score + fit score, thresholds, routing]

## Plays
[3-5 plays for the constraint; per play: mechanism, effort, expected lift, owner]

## Experiment Backlog
| # | Experiment | I | C | E | Score | Status |

## Metrics
[Activation rate, PQL rate, NRR, CAC payback: current, target, review cadence]
```

## Checklist

- [ ] The constraint is stated in one sentence with the numbers behind it.
- [ ] Every play ties to that constraint.
- [ ] Each input to unit economics is labeled measured or assumed.
- [ ] Projected lift is written as a hypothesis, not a promise.
- [ ] Each experiment has a sample-size check and a review date.

## Composition / References

- `marketing-experiments` skill: sample sizes and kill rules.
- `marketing-email` skill: builds the lifecycle plays specified here.
- `marketing-review-program` skill: customer review and advocacy programs.
