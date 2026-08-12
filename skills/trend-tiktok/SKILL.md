---
name: trend-tiktok
title: "TikTok Trend Harvester Playbook"
description: "Platform-specific intel for harvesting TikTok trends — Creative Center as the primary instrument (Trends tabs for hashtags/songs/creators/videos with country+industry filters, Keyword Insights, Symphony Assistant), the measured 10-day content lifespan (96% of reach) as the urgency anchor, sound-vs-format lifecycle asymmetry, scoring built on views-to-follower ratios (follower count is officially not a ranking factor), the fabricated-stat blacklist, and dead patterns from the For You eligibility standards. Activates inside an octoweb:trend session whenever the user names TikTok."
license: Apache-2.0
compatibility: "Octoweb browser access. Creative Center (creativecenter.tiktok.com) is public and free but heavily JS-rendered — needs a live browser session, not fetch; TikTok web works logged-out for search/tags/sounds."
capabilities: octoweb memory-read memory-write
domains: octoweb
rules:
  - session(trend) content(tiktok)
  - match(\btiktok\s+(trend|trends|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+tiktok\b)
  - match(\bcreative\s+center\b)
---

## Overview

This skill carries the TikTok-specific mechanics the `octoweb:trend` agent needs — harvest surfaces (Creative Center first), scoring signals, lifecycle timing, dead patterns, and a fabrication warning unique to this platform's data ecosystem. The agent owns the shared DNA loop (memory → harvest → score → cluster → DNA → hook bank → brief); this skill plugs in the TikTok parameters.

## Mental model

- Distribution is interest-cluster matching: the For You feed drives 72.7% of video views (Metricool 2026, n=2.31M posts) and TikTok states verbatim that follower count and past viral hits are "not direct factors" in recommendations. Consequence for harvesting: a micro account's breakout is pure algorithm signal — there is no follower-inertia to discount, unlike Instagram or X.
- The urgency anchor is measured: 96% of a post's lifetime reach and ~98% of its interactions land within the first 10 days (Metricool). A "trending" post older than ~10 days is an archaeology find, not a live trend.
- The feed deliberately diversifies (won't show two same-sound videos in a row) — saturation hits distribution mechanically, not just aesthetically.
- Completion is the strong indicator per TikTok's only official weighting statement (finishing a longer video outweighs weak signals). High view counts on hyper-short loops are cheaper than the same counts on 60s+ videos — weight accordingly.
- Sound-driven trends have a narrow participation window; format/meme-driven trends last materially longer (consistent practitioner observation, no measured study). Classify every trend as sound-locked or format-locked before recommending timing.
- 2026 context: volume +72% YoY, views −31% — everything is more saturated than the same signal would have meant a year ago. Raise the bar.

## Rules

### Harvest surfaces (Creative Center first, then in-platform)

| Surface | URL | Yields |
|---|---|---|
| Creative Center — trending hashtags | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en` | Ranked hashtags, filter by country + industry + period |
| Creative Center — trending songs | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en` | Rising vs peaked sounds; "Approved for Business Use" filter |
| Creative Center — trending videos | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en` | What TikTok itself showcases as working now |
| Creative Center — keyword insights | `https://ads.tiktok.com/business/creativecenter/keyword-insights/pc/en` | Search-demand signals for topic angles |
| TikTok search | `https://www.tiktok.com/search?q=<term>` | Niche posts as ranked by TikTok search |
| Tag page | `https://www.tiktok.com/tag/<tag>` | Post volume + top posts per hashtag |
| Sound page | `https://www.tiktok.com/music/<slug>-<id>` | Videos using a sound, recency spread |
| Anchor profile | `https://www.tiktok.com/@<handle>` | Niche anchors' recent output, view counts on grid |

Set the country and industry filters FIRST in Creative Center — trends vary sharply by both, and unfiltered global charts are noise for niche work. Pages are heavily JS-rendered: navigate in the browser, wait for render, snapshot, scrape, close. Symphony Assistant (in Creative Center, logged-in) answers "show me top-performing <industry> content in <market>" in natural language — use it when charts are ambiguous.

### Timing — use in-product state, not day-counts

No measured trend-lifecycle study exists; circulating day ranges disagree (5–14 days peak; one claim of 72-hour peaks). Don't fabricate a window. The checkable rule: enter while the sound/hashtag is still RISING in Creative Center's trend charts and before it plateaus — chart trajectory is observable in-product on every harvest. Combine with the measured 10-day content lifespan: if the top posts on a sound are mostly >10 days old, its live phase is over regardless of chart rank. Sound-locked trends get "this week or skip"; format-locked trends tolerate later, better-crafted entries.

### Scoring rubric (TikTok-specific signals)

Virality axis 0–5:
- Views-to-follower ratio on the poster — the cleanest signal on any platform here, since followers officially don't drive distribution. A 5K-follower account at 2M views is a maximal structural signal. Tag account bands (micro <50K / mid / mega).
- Comments-to-views — likes are the weak indicator; comment density marks the content that provoked. The measured comment asymmetry (questions +26% comments) means question-shaped winners are repeatable, not lucky.
- Completion proxy — length × views: sustained views on 60s+ videos outrank the same views on 8s loops (completion is the official strong indicator).
- Chart trajectory — rising in Creative Center beats absolute rank.

Niche-fit axis 0–5 — same scale the agent applies on every platform; the algorithm matches interest clusters, so off-niche trend-chasing underperforms structurally (relevance outweighs follower count — Metricool's small-account growth finding). Drop everything below 3 on either axis.

### Trend taxonomy (maps to Creative Center's own tabs)

Sounds/songs · formats and memes · challenges · effects · hashtags. Classify every cluster; the class determines the window (sounds narrow, formats long) and the brief's original-layer requirement (see below).

### The originality gate

TikTok's For You eligibility standards exclude "reproduced or unoriginal content… without any new or creative edits," and enforcement escalated 15 September 2025 (hits earnings AND visibility). Every recommended angle must name its original layer — the niche translation, take, or creative edit. Recommending "do this trending format" verbatim is recommending ineligible content. Watermarked cross-posts (including other editing apps' logos) are dead on arrival.

### Data hygiene — this platform's special hazard

A large fraction of 2026 "TikTok statistics" is AI-generated stat-farm content with fabricated figures under fake attributions to real firms (Sprout, Later, even TikTok itself). Known-fabricated families: hook-retention thresholds ("60% past 3s = 4x reach"), duet/stitch uplift percentages, per-video watch-time averages, AI reach penalties, numeric batch-test thresholds ("200-view jail"). Rule: figures enter a brief only from the platform's primary pages, the named measured studies (Metricool, Socialinsider, Buffer, Rival IQ/Quid), or the harvest itself. When citing a number in the brief, name its source or drop the number.

### Dead patterns (don't recommend, discount when harvested)

- Watermarked re-uploads and unedited imports — For You-ineligible verbatim
- Extremely short clips / GIF-only videos / QR codes — named in the eligibility standards
- Like-begging content — measured −60% interactions plus bait policy
- 0%-volume trending-sound trick — audio analysis reads actual sound; the trick does nothing
- Delete-and-repost accounts — duplicate detection flags reuploads; erratic view patterns on such accounts are artifacts
- Low-effort AI slop — dies on quality/originality grounds; note AI content per se is labeled, not throttled, and can go enormous — judge the content, not the tool

### Saturation detection

A sound/format is saturated when: Creative Center rank has plateaued or fallen, 5+ near-identical executions cluster in the harvest, and the youngest breakout is older than ~5 days. The feed's same-sound diversification means late entrants compete for rationed slots. Recommend saturated trends only with a hard niche-twist, and label them as such in the brief.

## Examples

### Example 1: Sound classification driving the recommendation

```
Sound: "<track>" — Creative Center songs chart #14 and rising (was #31 two days ago per memory), country=US, industry=tech
Top videos: 4 of 6 under 5 days old; two micro accounts at 40x and 85x views/follower
Class: sound-locked (audio joke, no format skeleton)
Verdict: BUY THIS WEEK — rising pre-plateau, micro-driven. Original layer required: niche-specific scenario over the audio, not a lip-sync.
```

### Example 2: Rejecting a polluted stat

A harvested "insight" claims duets get "+40% interactions per TikTok's early-2025 data." No such TikTok publication exists — the figure traces to aggregator farms. The brief describes the duet mechanic and its strategic logic (borrowing an anchor video's audience for commentary) with no percentage attached, and the source-hygiene note logs the rejected claim to memory.

## Checklist

Before returning the TikTok section of the brief:
- [ ] Creative Center harvested with country + industry filters set first; charts trajectory (rising/plateau) recorded, not just rank
- [ ] At least one keyword-insights pull and one tag/sound page per candidate trend
- [ ] Every cited post has handle, account band, views, comments, age, and URL
- [ ] Views-to-follower and comments-to-views computed; completion proxy noted for length outliers
- [ ] Every trend classified sound-locked vs format-locked, with the matching window in the brief
- [ ] Every recommended angle names its original layer (For You originality gate)
- [ ] The 10-day lifespan applied — nothing older recommended as "live"
- [ ] No figure in the brief without a named primary source or harvest evidence
- [ ] Chart states + sound trajectories logged to memory for next-session velocity
- [ ] All background harvest tabs closed before returning the brief

## Composition / References

- Pairs with `social-tiktok` (content domain) for drafting once the brief is in hand — same mechanics, applied to creation.
- How TikTok recommends videos (official): https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- For You eligibility standards: https://www.tiktok.com/community-guidelines/en/fyf-standards
- Creative Center: https://ads.tiktok.com/business/creativecenter — free, public; Symphony Assistant and product insights need login
- Measured anchors: Metricool 2026 (n=2.31M posts — the 10-day lifespan, 72.7% FYP share), Socialinsider 2026, Buffer 2026. Lifecycle day-ranges are deliberately absent — use in-product chart trajectory; re-validate the eligibility standards and Creator Rewards terms periodically.
- Use the agent's universal output schema; this skill only supplies the parameters that go into it.
