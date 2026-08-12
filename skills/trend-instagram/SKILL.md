---
name: trend-instagram
title: "Instagram Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Instagram trends — per-surface ranking reality (Explore weights engagement velocity; the audio page visit is itself a ranked action), trending-audio discovery via the arrow icon / audio-page use counts / trending leaderboard, the TikTok 3–7-day arbitrage window, harvest surface URLs, a scoring rubric built on views/sends-era metrics, lifecycle heuristics (48-hour buy zone, 1–3 week lifespan), and the April 2026 originality rule that makes take-free trend-riding recommendation-ineligible. Activates inside an octoweb:trend session whenever the user names Instagram."
license: Apache-2.0
compatibility: "Octoweb browser access. Requires signed-in Instagram session in the user's browser for Explore/Reels feeds and audio pages; trending-audio leaderboard and Professional Dashboard are app-only surfaces — harvest their output via audio pages."
capabilities: octoweb memory-read memory-write
domains: octoweb
rules:
  - session(trend) content(instagram)
  - session(trend) content(reels)
  - match(\binstagram\s+(trend|trends|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+instagram\b)
---

## Overview

This skill carries the Instagram-specific mechanics the `octoweb:trend` agent needs — surface behavior, audio-trend discovery, scoring signals, lifecycle timing, dead patterns. The agent owns the shared DNA loop (memory → harvest → score → cluster → DNA → hook bank → brief); this skill plugs in the Instagram parameters.

## Mental model

Every Instagram surface runs its own ranker (official: Instagram Ranking Explained). What matters for harvesting:

- Explore weights engagement velocity more heavily than Feed/Stories — speed of early engagement, not accumulated totals. A post on Explore is there because it accelerated, so Explore is the primary breakout-detection surface.
- Reels ranking predicts: reshare probability (listed first), watch-through, like, and visiting the audio page. The audio-page visit being a ranked action is the mechanical reason audio trends exist as a growth vector — Instagram is literally optimizing for people tapping into sounds.
- Sends per reach is a top-3 creator ranking signal (Mosseri), but send counts are invisible in public UI. Proxy: content shaped for DM-forwarding (specific-recipient material) that also shows outsized comment/view ratios.
- Stories rank on relationship closeness — a Story trend is a retention pattern, not a discovery pattern. Don't harvest Stories for virality signals.
- The April 2026 originality policy demotes repost-shaped content from all recommendations (photos and carousels now included, not just Reels). Interpretation shift: an aggregator account showing big view counts is coasting on follower base, not algorithm favor — discount aggregator numbers when scoring what's actually being amplified.
- Views is the universal metric since 2025 (impressions/plays are dead), and it counts repeat views — loop-engineered Reels inflate views by design. Check comments/saves alongside.

## Rules

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Explore grid (signed-in) | `https://www.instagram.com/explore/` | What Instagram is accelerating for this account's embedding right now |
| Reels feed (signed-in) | `https://www.instagram.com/reels/` | Current Reels distribution winners; note recurring audio |
| Audio page | `https://www.instagram.com/reels/audio/<audio_id>/` | Use count (the saturation gauge), top Reels using the sound, recency spread |
| Keyword search | `https://www.instagram.com/explore/search/keyword/?q=<term>` | Niche posts ranked by Instagram search (captions/keywords, not tags) |
| Hashtag page | `https://www.instagram.com/explore/tags/<tag>/` | Topic sample — top vs recent tabs show peak vs current state |
| Anchor account Reels | `https://www.instagram.com/<handle>/reels/` | Last-weeks output of each niche anchor; view counts visible on grid |

Open 4–8 in one parallel block of `browser_navigate` calls; snapshot, scrape, close. The in-app trending-audio leaderboard (music icon → Trending, top ~50, refreshed every few days) and Professional Dashboard "Trending audio" panel are app-only — when the user can check them, have them feed you the shortlist, then harvest each sound's audio page in the browser.

### Audio-trend discovery and timing

- The arrow icon next to a track name on a Reel is Instagram's native "trending now" marker — fastest in-feed confirmation.
- The audio page's use count is the buy-signal: low-but-climbing count with fresh top Reels = early; six figures with stale top Reels = late. Log use count + timestamp on every harvested sound so the next session sees the velocity, not just the level.
- Cross-platform arbitrage: sounds trending on TikTok reach Reels roughly 3–7 days later (directional, consistently reported). If a TikTok harvest ran recently, its rising sounds are the Reels pre-list.
- Lifecycle heuristics (practitioner consensus, no published methodology — treat as heuristics): first ~48 hours after a sound starts rising is the strong-adoption window; typical trend lifespan 1–3 weeks; emotionally/culturally anchored sounds can run 2–3 months while format-locked memes die in days.

### Scoring rubric (Instagram-specific signals)

Virality axis 0–5:
- Views-to-follower ratio on the poster — a 20K-follower account with a 2M-view Reel is a structural breakout; a 5M-follower account with 2M views is baseline. Tag account bands (micro <50K / mid / mega).
- Comments-to-views — with likes cheap and sends invisible, comment ratio is the strongest public depth signal. Saves visible only to the owner; save-shaped content (frameworks, lists) earns an inference note, not a number.
- Velocity — post age vs current views; Explore placement of a young post is itself velocity evidence.
- Audio momentum — for sound-driven Reels, the audio page's use-count trajectory outranks the individual post's numbers.

Niche-fit axis 0–5 — same scale the agent applies on every platform. Drop everything below 3 on either axis.

### Cluster interpretation

- A trend is 3+ independent accounts on the same format/sound/angle with breakout ratios — one mega account is a post, not a trend.
- Discount aggregator/repost accounts entirely (originality demotion means their reach is follower-inertia, not amplification).
- Loop-inflated views: hyper-short Reels with huge views but thin comments are replay artifacts — score on comment ratio.
- Carousel trends exist too (Instagram's strongest format for saves): recurring carousel skeletons across accounts (same slide-1 hook shape) are harvestable DNA, and since April 2026 the skeleton must be re-fleshed, never re-posted.

### The originality gate on every recommendation

Any angle recommended from a trend must specify the original layer — the take, voiceover, niche translation, or commentary that clears Meta's "materially edited" bar. A brief that says "do this trending format" without the original-layer line is recommending recommendation-ineligible content. Watermark-swaps and re-cuts explicitly don't count.

### Dead patterns (don't recommend, discount when harvested)

- Repost/aggregator content of any format — no recommendations since Apr 2026
- TikTok-watermarked Reels — suppressed from Explore/recs since 2021
- Majority-text or muted Reels — named in Instagram's Recommendation Guidelines
- Hashtag-wall captions — measured −31.7% views correlation (Metricool, n=24.4M); hashtags can't even be followed since Dec 2024
- Engagement-bait formulas ("tag 3 friends", "comment YES") — account-level demotion, repeat-offender based
- Send-bait ("share this with someone who…") — Mosseri's explicit "don't force it" target
- Low-res, bordered, obviously-recycled production — recommendation-gate hygiene failures

### Saturated-trend detection

When 5+ near-identical executions of a sound/format cluster in the harvest AND the youngest high-performers are older than ~1 week, mark it saturated: late entrants are competing against the trend's own back catalog on a velocity-weighted surface. Recommend saturated trends only with a hard niche-twist or contrarian inversion, and say so in the brief.

## Examples

### Example 1: Audio-page read

```
Sound: "original audio — @nichecreator" — use count 8,400 (was ~3K when first seen per memory, 4 days ago)
Top Reels: 3 of 6 posted <48h, all micro accounts with 10–40x views/follower ratios
Verdict: early-mid window, rising velocity, micro-driven = algorithm-amplified not follower-driven. BUY for niche X with original voiceover layer.
```

### Example 2: Discounting a fake signal

Harvest finds a 4M-view Reel on a meme format — but the account is an aggregator (reposts across niches, no original commentary), comments run 0.01% of views, and the format's other instances are all 2+ weeks old. Verdict: follower-inertia artifact on a demoted account class, late-stage format. Excluded from the brief; logged to memory as saturated.

## Checklist

Before returning the Instagram section of the brief:
- [ ] Explore + Reels feed + at least one audio page and one keyword search harvested in parallel
- [ ] Every cited post has handle, account-size band, views, comments, post age, and URL
- [ ] Views-to-follower and comments-to-views ratios computed — likes not used as a primary signal
- [ ] Sounds logged with use count + timestamp to memory for velocity tracking across sessions
- [ ] Aggregator/repost accounts discounted; loop-inflation checked via comment ratios
- [ ] Every recommended angle names its original layer (the Apr 2026 originality gate)
- [ ] Saturation verdict given per trend, with the 48h/1–3-week heuristics labeled as heuristics
- [ ] TikTok-arbitrage cross-check noted when a recent TikTok harvest exists in memory
- [ ] All background harvest tabs closed before returning the brief

## Composition / References

- Pairs with `social-instagram` (content domain) for drafting the posts once the brief is in hand — same mechanics, applied to creation.
- Instagram Ranking Explained (official, per-surface signals): https://about.instagram.com/blog/announcements/instagram-ranking-explained
- Originality/aggregator policy (Apr 2026) + engagement-bait policy: https://transparency.meta.com
- Measured correlations: Metricool 2026 study (n=24.4M posts). Lifecycle windows are practitioner consensus — re-validate periodically; no Instagram equivalent of TikTok's Creative Center exists, which is why in-app surfaces + TikTok lead-time monitoring are the method.
- Use the agent's universal output schema; this skill only supplies the parameters that go into it.
