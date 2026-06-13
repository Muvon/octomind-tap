---
name: trend-reddit
title: "Reddit Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Reddit trends across niche subreddits — upvote-velocity ranking, harvest URLs per-sub (hot/rising/top/new), mod-rules pre-flight that prevents removed posts, per-sub culture map for tech / AI / startup niches, title patterns and dead patterns in 2026. Activates inside an octoweb:trend session whenever the user names Reddit."
license: Apache-2.0
compatibility: "Octoweb browser access. Logged-out works for most surfaces; logged-in needed for personalized feeds."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(reddit)
  - session(trend) content(subreddit)
  - match(\breddit\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+reddit\b)
  - match(\br/[a-zA-Z0-9_]+\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest Reddit — current ranking signals (upvote velocity + comment depth + flag tax), per-sub harvest URLs, the mod-rules pre-flight that prevents wasted recommendations, per-sub culture map for the AI / dev / startup niches, title patterns, dead patterns, timing. The agent owns the shared DNA loop; this skill plugs the Reddit parameters in.

## Mental model

Reddit is not one audience. Each subreddit has its own ranker quirks, allowed formats, mod culture, and reader expectations. A title that crushes in r/Entrepreneur dies on r/MachineLearning. The hot ranker rewards first-hour velocity heavily — the first 60 minutes decide whether a post hits the sub's top or dies in new. The brief must be per-sub, not pan-Reddit. Mod-rules pre-flight is non-negotiable — recommending a post that violates a sub's rules wastes the user's submission and risks bans.

## Rules

### Current ranking signals (2026)

| Signal | Effect |
|---|---|
| Upvotes per hour, first 4h | Primary signal. >100/h in a 100k sub = climbing, >500/h = breakout |
| Comment-to-upvote ratio | Discussion signal. >10% high engagement, >20% controversial-or-deep |
| Upvote ratio (% upward) | Quality signal. 90% / 200 upvotes outranks 60% / 400 |
| OP comment in first 30 min | ~2× comment-count multiplier on average |
| Crossposts to multiple subs (organic) | Amplification candidate |
| Flagged or shadow-removed | Visible as `[removed]` / `[deleted]` — surface as teaching example |

### Harvest surfaces per sub (run in parallel)

For EACH target sub:

| Surface | URL | Yields |
|---|---|---|
| Hot | `https://www.reddit.com/r/<sub>/hot/` | What's surfacing now |
| Rising | `https://www.reddit.com/r/<sub>/rising/` | Early-climb signal; small upvotes, fast velocity |
| Top — day | `https://www.reddit.com/r/<sub>/top/?t=day` | Last-24h winners |
| Top — week | `https://www.reddit.com/r/<sub>/top/?t=week` | 7-day winners — recurring DNA |
| New (sample) | `https://www.reddit.com/r/<sub>/new/` | What's being posted now (saturation check) |
| Rules | `https://www.reddit.com/r/<sub>/about/rules/` | Mod restrictions — mandatory pre-flight |

Plus pan-Reddit:
- Topic search: `https://www.reddit.com/search/?q=<topic>&t=week`
- Crossover: `https://www.reddit.com/r/all/top/?t=day`

Cap parallel tabs at 8–12. Run multiple harvest passes if more subs needed.

If a feed lazy-loads slowly, scroll incrementally and wait for posts to render before extracting — stay on `www.reddit.com`.

### Mod-rules pre-flight (mandatory)

For every target sub, navigate to `/r/<sub>/about/rules/` (or sidebar) BEFORE making recommendations. Flag:
- Self-promotion ratios (9:1 rule is common)
- AI-generated content disclosure requirements
- Required post tags / flair
- Restricted post types (no link posts, no image posts)
- Weekly thread requirements ("ask all questions in the weekly thread")
- New-account / low-karma posting limits

If the user's planned angle clearly violates a sub's rules, do not recommend that sub for that angle. Say so explicitly in the brief.

### Scoring rubric (Reddit-specific signals)

Virality axis 0–5:
- Upvotes per hour in first 4h — primary signal
- Comment-to-upvote ratio
- Upvote ratio (visible on post page)
- OP-comment density in first hour
- Crosspost reach when present

Niche-fit axis 0–5:
- Sub-fit — does the user's angle match this sub's actual culture?
- Topic-fit — direct / adjacent / format-transplant / off

Score per sub, not pan-Reddit. A 4×4 in r/MachineLearning matters more than 5×2 in r/all.

### Per-sub culture map (verify each at runtime — rules drift quarterly)

| Sub | Culture | What wins | What gets removed |
|---|---|---|---|
| r/MachineLearning | Academic, gatekept | Paper discussion, novel results, deep technical. Tag with [R] / [D] / [P] / [N] | Marketing, AGI hype, no-paper "discussion" |
| r/LocalLLaMA | Practitioner, hardware-aware | Model benchmarks, quantization tricks, hardware setups, local-runtime tips | SaaS marketing, closed-model hype with no local angle |
| r/programming | Skeptical, language-agnostic | Blog posts with depth, war stories, "I read the source of X" | Listicles, "10 tools every dev needs", AI slop |
| r/startups | Bootstrappers + funded | Honest revenue posts, MRR breakdowns, lessons from failure | "I built X in 3 hours" wrappers, low-effort idea validation |
| r/SaaS | Indie SaaS, transparent | Real metrics, churn experiments, pricing experiments | Fake success stories, growth-hack listicles |
| r/Entrepreneur | Mixed quality, hustle-friendly | Specific operator playbooks | Generic motivation, "how I made $1M in 30 days" |
| r/ChatGPT | Casual, mainstream | Cool prompts, weird outputs, image gens | Technical depth goes ignored |
| r/ClaudeAI | Small, technical-curious | Workflow comparisons, system prompt tactics, Claude-specific tips | Open-and-shut "Claude vs X" posts |
| r/singularity | Speculative | Big-picture takes, frontier model commentary | Hands-on technical posts |

### Title patterns that work

1. Specific result + setup — "Ran [X] on [Y]: here's the [Z] result"
2. Contested claim — "I think [X] is wrong. Here's my [data/setup/code]"
3. Honest failure — "[X] didn't work. Here's what I tried and what broke"
4. Novel artifact — "[New thing] I built / paper I read — sharing for discussion"
5. Targeted question with context — "How do you handle [specific thing]? Here's my current approach and where it fails"

### Dead title patterns

- ALL CAPS or excessive punctuation
- "[Question for the community]" / "[Help]" / "[Question]" prefixes
- Vague titles ("Help" / "Anyone else?")
- Marketing slogans ("The [adj] way to [verb]")
- "Am I the only one who..." engagement bait
- ShowHN-style "I built X" without specifics — wrong platform tell

### Timing

- US-skewed subs: Tue–Thu 9–11 AM ET and 7–9 PM ET. Weekend mornings for hobby subs.
- EU/global subs (r/MachineLearning, r/programming): morning ET captures EU evening. Avoid 2–6 AM ET.
- Posting late = new-queue bury. Velocity must hit in the first 30 minutes.

### Saturated-take detection per sub

Always run a `/new/` sample on each target sub. If 5+ recent posts hit the same angle in the last 48h and most are underperforming, mark the angle saturated for that sub.

## Examples

### Example 1: Per-sub recommendation with mod-clearance

Bad — pan-Reddit recommendation, no mod check:
```
Submit a post about your new RAG framework to r/MachineLearning and r/SaaS.
```

Good — per-sub, mod-cleared, format-prescribed:
```
Target: r/LocalLLaMA (412k subscribers)
Mod-rules flags checked: no AI-content disclosure required; self-promo allowed if technical depth is genuine; flair required (choose "Discussion" or "Resources").
Format mix this week: text 62% / link 28% / image 10%.

Angle: "Quantization tradeoffs we measured for {{niche model}} at 4-bit vs 8-bit on consumer GPUs"
- Format: text post with embedded chart screenshot
- Flair: Resources
- Title pattern: specific result + setup
- Why it's open: 3 quantization posts in last week, all anecdotal; gap is rigorous measurement
- Mod-clearance: passes
- Survival probability: high — OP-engagement readiness is critical (be ready to answer hardware questions in first hour)

DO NOT submit to r/MachineLearning — mod rules require paper / arxiv link for the [R] flair, anecdote-based posts get removed.
```

### Example 2: Flagged post as teaching example

```
r/programming — "AI will replace developers in 2 years"
3.2k upvotes, 487 comments, 62% upvote ratio. Now [removed by mods].
Reason inferred: low-effort hot take, no technical content, breaks rule 1 (must be programming content).
Lesson: this sub will surface low-effort hot takes briefly via upvote velocity, then remove them. Do not target this angle.
```

## Checklist

Before returning the Reddit section of the brief:
- [ ] Every recommended sub had its rules / sidebar checked at runtime
- [ ] Every cited post has subreddit, title (verbatim), upvotes, upvote ratio, comments, OP karma band, URL, age
- [ ] Removed / flagged posts surfaced when visible — they teach what the sub rejects
- [ ] Scored per sub, not pan-Reddit
- [ ] Format mix per sub noted (text / link / image / video percentages this week)
- [ ] Per-sub culture map applied — recommendations match sub's actual norms
- [ ] (Opt-in mode only) Title bank entries each fit one of the title patterns from this skill
- [ ] Dead-title-pattern list applied — no recommended title uses ALL CAPS, vague help asks, engagement bait, or marketing slogans
- [ ] (Opt-in mode only) OP-engagement plan included — what top comments to anticipate in first hour
- [ ] (Opt-in mode only) Crosspost order recommended if relevant (smaller niche sub first for velocity, then larger)
- [ ] All background tabs closed

## Composition / References

- Pairs with `social-reddit` (content domain) for writing the actual submission body from the brief.
- Use the agent's universal output schema.
