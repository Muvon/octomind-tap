---
name: marketing-experiments
title: "A/B Testing for Marketing: Sample Size and Stop Rules"
description: "One rule set for marketing tests: hypothesis, sample size per arm, run length, stop rule, kill and scale table. Use for A/B, email, ad and growth tests."
license: Apache-2.0
compatibility: "No tools required. Any OS. Produces test plans and verdicts only; runs nothing."
domains: marketing launch
rules:
  - match((?i)\ba/?b\s+tests?\b)
  - match((?i)\bsplit\s+tests?\b)
  - match((?i)\bsample\s+size\b)
  - match((?i)\b(statistical(ly)?\s+)?significan(t|ce)\b)
  - match((?i)\b(kill|scale)\b.*\b(ad|variant|creative|campaign)s?\b)
  - content(experiment)
  - content(experiments)
---

## Overview

This skill is the single rule set for any marketing test: a subject line, a landing page, an ad creative, an onboarding change. It gives the plan to write before the test starts, the sample size each arm needs, and the rule that ends the test. It plans and judges tests; it does not run them.

## Mental model

A test answers one question with a number set in advance. Three things decide whether the answer can be trusted: one changed variable, a sample large enough to see the lift you care about, and a stop rule written before the first result arrives. Peeking and stopping on the first good-looking day produces false winners.

## Rules

### Plan before launch

Write these down; a test without all seven is not started.
1. Hypothesis: "Changing X for audience Y will raise metric M".
2. One variable. Two changes in one variant make the result unreadable.
3. Primary metric, one only, closest to money you can measure (click, reply, signup, activation, purchase). Opens do not count: Apple Mail Privacy Protection inflates them.
4. Baseline rate, from the last 4 to 8 weeks.
5. Minimum lift worth acting on, as a relative change (for example +20%).
6. Sample size per arm from the table below, and the run length that reaches it.
7. Decision date and the action for each outcome (kept, killed, inconclusive).

### Sample size per arm

Formula (Lehr's rule, two-sided 5% significance, 80% power): n per arm is about 16 x p x (1 - p) / d^2, where p is the baseline rate and d is the absolute difference you want to detect (p times the relative lift). The rule is an approximation; a calculator gives exact figures.

| Baseline rate | Detect +20% relative | Detect +50% relative |
|---|---|---|
| 1% | about 39,600 | about 6,300 |
| 2% | about 19,600 | about 3,100 |
| 5% | about 7,600 | about 1,200 |
| 10% | about 3,600 | about 580 |
| 30% | about 930 | about 150 |

Counts are visitors, recipients or impressions per arm, matching the denominator of the metric. For a 50/50 split, double the figure for the total.

### Run length and stop rule

- Run whole weeks (minimum 7 days; 14 if traffic is below 100 per day) so weekday effects balance out.
- Do not stop early on a good result. Look only at the planned sample size or the decision date, whichever comes first.
- Reached the sample size: pick the winner only if the lift clears your minimum lift in step 5 and the primary metric moved; otherwise call it no difference.
- Decision date arrives before the sample size: the verdict is inconclusive. Write it down, then either fund a dated continuation or drop the idea. Do not extend a weak test with no end.
- Several variants multiply the sample needed; test two or three, not eight.

### Low volume

If the table asks for more visitors than the channel delivers in 4 weeks, test a bigger change (price, offer, onboarding redesign, a new angle) so the lift you hope for is +50% or more, or use a proxy metric higher in the funnel and label it as a proxy. Button-color tests at low volume only produce noise.

### Paid ads: kill and scale table

These are default thresholds, not platform rules; adjust them to the account and state the change.

| Situation | Action |
|---|---|
| A variant has spent 3 times your target cost per conversion with zero conversions | Kill it |
| Click-through test, each arm below the impressions in the table for its baseline | Keep running; no verdict |
| Each arm at its sample size, the lower arm is not worse than the minimum lift | Keep the cheaper one; call it a tie |
| A variant beats control by the minimum lift at sample size and cost per conversion is at or under target | Scale |
| Scaling | Raise budget by at most 20% per step, wait 3 to 7 days between steps, and stop if cost per conversion rises above target for 3 days |
| Edits during the test (new creative, targeting, bid change) | Restart the count; the old data no longer compares |

Platform learning matters: Google recommends judging a Target CPA setup on at least 30 conversions over 30 days, and Meta reports ad sets as "Learning limited" when they fall short of roughly 50 optimization events in 7 days. Read the current thresholds in the platform help pages before relying on them. A creative test that cannot reach those counts should be judged on a higher-funnel metric and labeled that way.

### Email and lifecycle tests

Same table. Split by recipient, not by send time. Measure clicks or conversions, never opens. A list of fewer than 2,000 recipients rarely supports a subject-line test; use the send for your best guess and test the next one.

## Examples

Subject line test, baseline click rate 3%, goal +50%: d = 0.015, n = 16 x 0.0291 / 0.000225, about 2,070 per arm. A list of 4,000 split in two is just short; call the result directional or double the sends.

Landing page test, baseline signup 5%, goal +20%: about 7,600 visitors per arm. At 200 visitors a day that is 76 days, so test a larger change instead.

## Checklist

- Seven plan items written before launch.
- One variable, one primary metric, a baseline from the last 4 to 8 weeks.
- Sample size from the table, run length in whole weeks.
- Verdict recorded as kept, killed or inconclusive, with the number and the date.
- Edits mid-test restarted the count.
- Lifts are reported as measured results, never as promises.

## References

- Lehr's rule: Lehr R, "Sixteen S-squared over D-squared: a relation for crude sample size estimates", Statistics in Medicine 11(8):1099-1102, 1992. https://jhanley.biostat.mcgill.ca/c607/ch07/16_s_sq_over_d_sq.pdf (checked 2026-11-15)
- Google Ads Help, About Target CPA bidding (30 conversions over 30 days for evaluation). https://support.google.com/google-ads/answer/6268632 (checked 2026-11-15)
