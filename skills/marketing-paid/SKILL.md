---
name: marketing-paid
title: "Paid Media Planning: Campaign Build and Tracking"
description: "Plans paid ads: campaign structure, bids, audiences, budget split, conversion tracking, test rules. Use when setting up or fixing ad accounts."
license: Apache-2.0
compatibility: "Needs web search to check current platform help pages. No ad-platform API is connected; the plan is applied by hand in the ad accounts. Any OS."
domains: marketer
rules:
  - match((?i)\b(set up|build|structure|plan|audit|fix)\b.{0,30}\b(google ads|meta ads|facebook ads|linkedin ads|tiktok ads|paid (search|social|media|ads)|ppc|ad campaigns?|ad account)\b)
  - match((?i)\b(target CPA|tROAS|ROAS|break-?even CPA|bid strateg\w+|ad budget|media plan)\b)
  - match((?i)\b(conversion tracking|conversions? api|enhanced conversions|consent mode)\b.{0,40}\b(ads?|paid|campaigns?)\b)
  - match((?i)\b(CPA|cost per acquisition)\b.{0,20}\b(high|too high|rising|up)\b)
  - semantic(plan paid ad campaigns, bids and budget split, 0.73)
  - semantic(set up google ads campaigns with the right bids and budget, 0.70)
  - semantic(my cost per acquisition is too high on paid social, fix the account, 0.70)
  - semantic(plan conversion tracking and test rules for our ad accounts, 0.73)
---

## Overview

Use this skill to decide how an ad account is built and measured: campaign and ad-group structure, bid strategy, audiences, budget split, conversion tracking, attribution and the numbers that end a test. The outcome is a campaign build sheet and a measurement plan the user applies by hand. The work runs from unit economics and event volume, not platform defaults.

## Mental model

Every decision refers back to two written numbers: break-even cost per acquisition (CPA) and the target CPA. No ad-platform API is connected, so produce settings and plans, and never claim to have changed an account.

## Rules

### Workflow

1. Ingest: product, price, gross margin, customer lifetime value or best estimate, current conversion rate, platforms already used, monthly budget, and what exists in tracking. Recall earlier plans from memory.
2. Set the economics: break-even CPA (gross profit per customer over the payback window) and the target at or below it. Write both numbers.
3. Choose platforms: one or two. Pick where the buyer already is and where a click costs less than the target allows. Use the `ad-google`, `ad-meta`, `ad-linkedin`, `ad-bing`, `ad-tiktok`, `ad-reddit`, `ad-x` and `ad-youtube` skills for the slots and policies of each platform.
4. Build the structure: campaigns by objective, ad groups or ad sets by audience or intent, creative angles per group, naming convention, UTM scheme.
5. Set bids and budgets by the rules below. Check platform help pages with web search because names and thresholds change.
6. Write the measurement plan: events, tracking method, consent handling, attribution window, and how to judge incrementality.
7. Set test and scale rules with the `marketing-experiments` skill. Save both files, then memorize the economics and the structure.

### Economics first

- Break-even CPA = gross profit per customer over the payback period you accept. Target CPA = break-even divided by a safety factor you state (for example 1.5).
- A common benchmark is lifetime value at least 3 times CAC. Treat it as a starting check, not a law, and show the user's own number.
- If the target CPA is below what the channel's cost per click and conversion rate allow (CPC divided by conversion rate), the channel does not fit. Say so before building.

### Bid strategy by data volume

| Conversions in the last 30 days (campaign) | Bid approach |
|---|---|
| None, new account | Maximize clicks or a manual cap with a low daily budget, to collect the first conversions |
| Under about 30 | Maximize conversions without a cost target, or a high target; judge on a higher-funnel event |
| About 30 or more | Target CPA or target ROAS at or near the economics above |

Google guides evaluating a Target CPA setup on at least 30 conversions over 30 days. Meta flags ad sets that fall short of roughly 50 optimization events a week as limited in learning. Confirm both in the current help pages.

### Budget allocation

- Minimum weekly budget per ad set or campaign = target CPA x events the platform needs per week (about 50 on Meta). If the budget is below that, optimize for an earlier event in the funnel or run fewer ad sets, not more.
- Split by marginal CPA, not by habit: start about 70% on the platform with the best expected CPA and about 30% on one test, then move budget toward the lower realized CPA after each readout. Move no more than 20% of a budget per step.
- Branded search first on search platforms; it is cheap and protects the name. Retargeting gets a small, capped share because it harvests demand other campaigns created.

### Audiences

- Start broad with strong creative where the platform's automation is built for it. Add narrow audiences only when volume or compliance requires. Exclude existing customers and employees. Build lookalike or similar audiences only from a list of real customers large enough for the platform.
- Upload customer lists only with documented consent. Follow each platform's customer-list policy and flag legal questions for review.

### Tracking and attribution

- Track one primary conversion that matches money (paid, qualified lead, activated trial) and secondary events higher in the funnel. Count each conversion once.
- Use both the browser tag and the server-side route the platform offers (Conversions API on Meta, enhanced conversions on Google, the platform's equivalent elsewhere) with a shared event ID so duplicates are dropped.
- Consent: where visitors are in the EEA or UK, tags fire according to the consent banner (Google Consent Mode). State what is lost and that conversions will be modeled.
- Every ad URL carries source, medium, campaign and content tags in one naming scheme. The platform's own numbers and the analytics numbers will differ: reconcile weekly against the order or CRM record and trust the record.
- Pick an attribution window up front and keep it. For decisions that move more than 20% of budget, run a holdout or geo split to measure incrementality instead of trusting last-click.

### Test and scale

Apply the `marketing-experiments` skill: one variable, sample size from its table, kill and scale table, restart the count after any edit.

### Spend safety

Every plan states a daily cap, a monthly cap and an owner. Budgets in the plan are the user's confirmed numbers, never assumed ones.

### Guards

- Don't claim to have changed any ad account; hand over settings to apply.
- Don't plan spend without a stated cap, and don't invent budgets, margins or conversion rates.
- Don't judge a variant before its sample size or conversion count is reached.
- Don't recommend uploading customer lists without documented consent.
- State which numbers are the user's, which are benchmarks and which are assumptions. Tell the user when volume is too low for the structure they asked for.
- Ad copy, visual briefs and landing-page copy are outside this skill; the build sheet supplies the angles and slots they need.

## Examples

- "Set up my Google, Meta or LinkedIn campaigns": ask for monthly budget and what a customer is worth, then build.
- "Why is my CPA high?": check tracking and event volume first, then structure, then creative.
- "Is my tracking right?": produce the measurement plan and a verification checklist for the user to run.
- Autonomous or non-interactive brief: ask nothing; state assumptions for budget and customer value in one line and continue.

## Output format

Save two files.

`paid-build-[product].md`:

```markdown
# Campaign Build Sheet: [Product]
## Economics
[gross profit per customer, break-even CPA, target CPA, caps]
## Platforms and Budget Split
[platform, monthly budget, share, why]
## Campaign Structure
| Campaign | Objective | Ad groups or ad sets | Audience or keywords | Bid strategy | Daily budget | Creative angles |
## Naming and UTM Scheme
## Test and Scale Rules
[from the experiments skill, with this account's numbers]
```

`paid-measurement-[product].md`:

```markdown
# Measurement Plan: [Product]
## Events
| Event | Meaning | Where fired | Browser | Server | Value |
## Consent Handling
## Attribution Window and Source of Truth
## Weekly Readout
[metrics, thresholds, owner, review day]
## Open Items
```

## Checklist

- [ ] Break-even CPA and target CPA are written and used in every later decision.
- [ ] Bid strategy matches the conversion volume.
- [ ] Weekly budget per ad set meets the minimum for its optimization event.
- [ ] One primary conversion, deduplicated with a shared event ID.
- [ ] Daily cap, monthly cap and owner stated.
- [ ] Each number is labeled as the user's, a benchmark or an assumption.

## Composition / References

- `marketing-experiments` skill: test, kill and scale rules.
- `ad-google`, `ad-meta`, `ad-linkedin`, `ad-bing`, `ad-tiktok`, `ad-reddit`, `ad-x`, `ad-youtube` skills: platform slots and policies.
