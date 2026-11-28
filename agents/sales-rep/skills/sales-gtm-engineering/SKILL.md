---
name: sales-gtm-engineering
title: "GTM Engineering: Enrichment, Scoring and Routing Specs"
description: "Designs B2B lead enrichment, signal-driven plays, scoring and routing, outbound automation and deliverability setup as specs. Use to design the system."
license: Apache-2.0
compatibility: "Environment-independent. Web search and page fetch read vendor documentation; output is a Markdown spec."
capabilities: webfetch
rules:
  - match((?i)\b(enrichment (waterfall|workflow|pipeline)|lead scoring|lead routing|scoring model|routing logic)\b)
  - match((?i)\b(design|build|spec|specify|plan|map|draft)\b.{0,40}\b(signal[- ]based outbound|trigger[- ]based|outbound automation|automation (architecture|stack)|gtm (system|stack)|integration map|data flow|field (mapping|sync)|write-?back)\b)
  - match((?i)\b(sending domains?|mailbox warm-?up|domain warm-?up|email infrastructure|deliverability (setup|plan))\b)
  - match((?i)\b(outbound play|play spec\w*|spec\w*.{0,30}\bplay|experiment spec|kill (criteria|date))\b)
  - match((?i)\b(assigns?|route|routing)\b.{0,30}\b(scored )?(inbound )?leads\b|\bscored (inbound )?leads\b)
  - match((?i)\bgtm engineer\w*\b)
  - semantic(design a signal-driven outbound system with enrichment and routing, 0.70)
  - semantic(design lead scoring and routing rules for inbound leads)
  - semantic(spec an enrichment workflow that finds contacts and buying signals, 0.69)
  - semantic(set up sending domains and mailbox warmup for outbound email, 0.75)
---

## Overview

This skill designs the systems that generate pipeline: enrichment workflows, signal-driven outbound plays, lead scoring and routing, and the integrations that hold the revenue stack together. One well-built system outperforms a team running manual outbound, so the job is to spec that system so an operator can run it. The output is a written spec. Every play ships with its own success metric. It designs and documents; it never sends.

## Mental model

- A play is trigger, source, enrichment steps, score and route, sequence, owner, metric. A play missing any element is not a play.
- Signal first: every play starts from a trigger event, never a static list.
- Automate a working play, not a hope: the manual version must produce replies before it earns automation.

## Rules

### Workflow

1. Ingest the ICP and motion (from a GTM plan or the user) plus the current stack; remember "gtm system", "plays", "stack" and "deliverability".
2. Inventory the data sources, tools and integrations that already exist; reuse before adding.
3. Research in parallel searches: which buying signals are observable for this ICP, which tool categories cover them, current provider coverage claims. Read the vendor docs when specifics matter.
4. Design three to five candidate plays ranked by signal strength; spec each fully.
5. Spec the system: integration map, scoring and routing rules, deliverability setup.
6. Define the experiment: sample size, success threshold, kill date. Then memorize the play and stack decisions.

### Design rules

- A funding round, a job post naming the problem, or a competitor install beats any purchased list.
- Quality gates before volume: verified emails only, sending domains separate from the primary domain, authentication in place and domains warmed before campaign traffic, volume capped per mailbox, and complaint rate watched as the stop signal. A complaint spike kills the domain, not just the campaign. The thresholds, mailbox-provider rules and warmup schedule come from the `outreach-deliverability` skill; copy them into the spec from there.
- Measure replies and meetings booked. Opens and clicks are diagnostics, never targets.
- For the deliverability setup and consent flags in a spec, apply the `outreach-deliverability` and `outreach-compliance` skills instead of restating them.
- Tool-agnostic specs: name the category (enrichment platform, sequencer, CRM, intent provider), list current examples, never hard-wire one vendor into the design.

| Signal type | Typical source | Strength |
|-------------|---------------|----------|
| Job change (champion moves) | Enrichment provider or CRM change alerts (not LinkedIn scraping, banned by its User Agreement) | High: warm relationship |
| Hiring for the pain | Job boards | High: budget confirmed |
| Funding round | Registries, news | Medium: money, unclear priority |
| Tech install or removal | Install-data providers | Medium: stack fit known |
| Content intent | Intent-data providers | Low to medium: timing guess |

### Guards

Don't design spray-and-pray volume, recommend buying email lists, automate LinkedIn actions (bots for invites or messages violate its User Agreement §8.2), or skip opt-out and lawful-basis handling. Flag jurisdiction for legal review rather than guessing. Canada (CASL) and Germany need consent even for B2B email; don't spec cold email to them without it. Put the region rules from the `outreach-compliance` skill (email consent by country, calls, texts, call recording) into each play's spec.

Do keep every play runnable from the spec alone, and kill plays that miss their threshold by the kill date.

## Examples

- "We need more pipeline": ask for ICP and current stack, then design plays.
- "Build me an enrichment workflow": full play spec plus step-by-step build order.
- No ICP exists: get a GTM plan first; a system without an ICP automates noise.
- Existing play underperforming: diagnose in spec order: trigger quality, then data quality, then routing, then copy.

## Output format

Save as `gtm-system-[company].md`:

```markdown
# GTM System: [Company]

## Stack Map
[Current tools, gaps, additions by category, with the integration flow between them]

## Plays
| # | Trigger | Source | Enrichment | Route | Sequence owner | Target metric |
[Then one section per play with the full spec]

## Scoring & Routing
[Fit score + behavior score; thresholds and destinations]

## Deliverability Setup
[Domains, mailboxes, warmup schedule, volume caps]

## Experiment Plan
[Per play: sample, success threshold, kill date]
```

## Checklist

- [ ] Every play has trigger, source, enrichment, score and route, sequence, owner and metric?
- [ ] Every play starts from a signal, not a list?
- [ ] Deliverability thresholds copied from the deliverability skill, consent flags per region?
- [ ] Success threshold and kill date set per play?
- [ ] Spec is tool-agnostic and runnable without the author?

## Composition / References

- `outreach-deliverability` skill: authentication, mailbox-provider limits, warmup schedule.
- `outreach-compliance` skill: consent by region, calls, texts, call recording.
- `sales-outbound` skill: sequence copy and cadence coaching for the plays.
