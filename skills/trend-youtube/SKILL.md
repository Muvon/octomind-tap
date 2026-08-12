---
name: trend-youtube
title: "YouTube Trend Harvester Playbook"
description: "Platform-specific intel for harvesting YouTube trends after the July 2025 Trending-page removal — the replacement stack (category Charts, Studio Inspiration tab with content gaps, Hype, the experimental Research tab with outlier multipliers), outlier-hunting methodology (channel-relative multiples, never absolute views; format outliers over timing outliers; one is luck, three is a strategy), Google Trends' separate YouTube Search dataset, Shorts trend surfaces, and a scoring rubric built on views-vs-channel-baseline. Activates inside an octoweb:trend session whenever the user names YouTube."
license: Apache-2.0
compatibility: "Octoweb browser access. Charts and Google Trends work logged-out; Studio Inspiration tab and Hype data require the user's signed-in session; outlier tools (1of10, ViewStats, vidIQ) are third-party freemium."
capabilities: octoweb memory-read memory-write
domains: octoweb
rules:
  - session(trend) content(youtube)
  - match(\byoutube\s+(trend|trends|trending|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+youtube\b)
  - match(\boutlier\s+(video|videos|hunting)\b)
---

## Overview

This skill carries the YouTube-specific mechanics the `octoweb:trend` agent needs. YouTube killed the global Trending page in July 2025 ("more micro-trends than ever… discovery shifted to personalized recommendations"), so YouTube trend-harvesting is now outlier-hunting across niches plus the official replacement surfaces — there is no single chart to read. The agent owns the shared DNA loop (memory → harvest → score → cluster → DNA → hook bank → brief); this skill plugs in the YouTube parameters.

## Mental model

- Ranking is per-video and per-viewer ("the algorithm follows the audience"; discovery is pull, not push). A breakout is therefore a statement about audience demand, not channel authority — which is exactly what makes outliers harvestable: the demand transfers, the channel doesn't need to.
- The outlier is the unit of signal: a video doing 3–10x+ its own channel's baseline. Absolute view counts are meaningless across channels; multiples are comparable everywhere.
- Format outliers transfer; timing outliers don't. A repeatable format/structure that broke out is a strategy; a news-cycle or controversy spike is an expired lottery ticket. Classify before recommending.
- One outlier is luck; three similar outliers across independent channels is a repeatable pattern — the same 3-instance bar the agent applies on every platform, here it's the core method.
- Finding the outlier is not the win: the win is converting it into an original title/thumbnail/angle. Every recommendation carries its transformation, or it's a plagiarism instruction.
- Shorts and long-form are separate markets with separate surfaces (Shorts has its own Trends page) and wildly different economics (~$0.05 vs ~$2.50 median RPM) — label every finding with its format lane.

## Rules

### Harvest surfaces (run in parallel)

| Surface | URL / access | Yields |
|---|---|---|
| YouTube Charts | `https://charts.youtube.com` | Official category trends (music, podcasts, trailers) — the Trending page's replacement |
| Niche search, filtered | `https://www.youtube.com/results?search_query=<topic>&sp=CAISBAgCEAE%253D` (sort: view count, this week) | Current high-performers per topic; adjust filter tokens via the Filters UI |
| Anchor channels | `https://www.youtube.com/@<handle>/videos` | Grid shows views + age → channel baseline and outliers by eye |
| Shorts Trends page | Shorts feed → pause → Trends tab (app/web, signed-in) | Trending audio + formats for the Shorts lane |
| Google Trends, YouTube dataset | `https://trends.google.com/trends/explore?gprop=youtube&q=<term>` | Search demand INSIDE YouTube — a different dataset than web search; sort related queries by Rising |
| Studio Inspiration tab | user's Studio session → Inspiration | Search trends, Breakout clips, and content gaps ("Top searches for this topic" → Show all → Content gaps) |
| Hype | signed-in surface | Viewer-amplified emerging videos from sub-500K channels — early-signal pool |
| Outlier tools | 1of10 / ViewStats / vidIQ Outliers (freemium) | Pre-computed outlier multipliers when available |

Open 4–8 in one parallel block, snapshot, scrape, close. When the user's signed-in session is available, the Inspiration tab's content gaps (high search volume, low supply) are the highest-value single pull — it's YouTube telling you unmet demand directly. YouTube is also testing a Research tab with native outlier multipliers (4x–132x in the UI) and a "Watched by my Viewers" filter — use it when the account has access.

### Computing outliers by hand (when tools aren't available)

Channel baseline = median views of the channel's last ~10 uploads of the same format (Shorts and long-form baselines computed separately — the grids mix them). Outlier multiple = candidate views ÷ baseline. Thresholds: 3–5x notable, 5–10x strong, 10x+ exceptional. Recency-weight: an outlier from this month is an opportunity; one from last year is a format that may already be saturated — check whether recent imitators still outperform.

### Scoring rubric (YouTube-specific signals)

Virality axis 0–5:
- Outlier multiple vs channel baseline — the primary signal, never absolute views.
- Independent replication — the same format/topic breaking out on 3+ unrelated channels scores structurally higher than one 100x monster.
- Velocity — views ÷ days-since-upload against that channel's typical accumulation; recent-and-rising beats big-and-old.
- Demand corroboration — Google Trends (YouTube dataset) rising, or the topic appearing in Inspiration content gaps.

Niche-fit axis 0–5 — same scale the agent applies everywhere. Drop below 3 on either axis.

### Classification gates (apply to every cluster)

- Format vs topic vs timing: format outliers (structure/packaging pattern) transfer across niches and time; topic outliers transfer while search demand holds (check Trends trajectory); timing outliers (news, drama, platform moments) do not transfer — report them as context, never as recommendations.
- Lane: Shorts vs long-form, scored against lane-appropriate baselines and briefed separately (different economics: a Shorts trend feeds discovery; a long-form trend feeds revenue).
- Evergreen vs decaying: is the format's newest strong instance <30 days old? If all strong instances are old, the format is likely saturated — verify with one fresh imitator's numbers before recommending.

### The transformation requirement

Every recommended angle names: the source outlier(s) (URL + multiple), the extracted DNA (what structurally made it work — the packaging pattern, not the topic surface), and the original transformation for the user's niche. "Make a video like X" without the transformation line fails both YouTube's reused-content policy and the brief's quality bar. Titles/thumbnails are re-derived, never copied — egregious-clickbait enforcement (Dec 2024) also applies to inherited packaging that over-promises.

### Dead signals (discount when harvested)

- Timing/controversy spikes presented as formats — expired opportunities
- Mass-produced template channels (near-identical uploads) — "inauthentic content" demonetization class; their volume distorts baseline math, exclude them
- Clickbait-mismatch packaging — removal-eligible since Dec 2024; a breakout riding an undelivered promise is not a repeatable strategy
- AI-slop breakouts — measured ~70% lower retention class; a view spike with cratered satisfaction doesn't transfer
- Pre-July-2025 "Trending page" methodology in any source — the page no longer exists; treat advice built on it as stale

## Examples

### Example 1: Outlier write-up shape

```
Channel @midtier-dev (baseline ~8K views/video) — "I replaced our CI with 3 bash scripts" — 214K views, 11 days old → 26.7x outlier
Corroboration: same "boring tool replaces fancy stack" format at 9.4x (@platform-eng) and 6.1x (@sre-diaries) within 3 weeks; "CI alternatives" rising on Google Trends (YouTube dataset, US, 12mo)
Class: FORMAT outlier (contrarian simplification + named stack), long-form lane
DNA: specific cost/complexity number in title, before/after thumbnail split, first-person stakes
Transform for user niche: "I replaced our RAG pipeline with grep" — same skeleton, user's domain, packaging re-derived
```

### Example 2: Refusing a timing outlier

Harvest finds a 130x outlier reacting to a platform outage. Trends shows the query already collapsing; no second channel sustains the format a week later. Verdict: timing outlier — reported in the brief's context section as evidence of audience interest in reliability topics, explicitly NOT recommended as a video to imitate.

## Checklist

Before returning the YouTube section of the brief:
- [ ] Charts + niche search + anchor channels harvested; Inspiration content gaps pulled when a signed-in session exists
- [ ] Google Trends checked on the YOUTUBE dataset (gprop=youtube), not web search
- [ ] Every cited video has channel, baseline, outlier multiple, age, lane (Shorts/long-form), and URL
- [ ] Multiples computed vs same-format channel baseline — no absolute-view comparisons anywhere
- [ ] Every cluster classified format/topic/timing; timing outliers excluded from recommendations
- [ ] 3+ independent instances behind every recommended pattern (one outlier = luck)
- [ ] Every recommendation carries source DNA + original transformation — no "copy this video"
- [ ] Template-farm channels excluded from baselines and clusters
- [ ] Outlier records (channel, multiple, date) logged to memory for cross-session velocity
- [ ] All background harvest tabs closed before returning the brief

## Composition / References

- Pairs with `social-youtube` (content domain) for packaging/structure once the brief lands — the DNA extracted here plugs into its title/thumbnail/hook rules.
- Trending-page removal + Charts replacement: YouTube announcement July 2025 (TechCrunch/Tubefilter coverage); Hype + Inspiration tab: official Studio features; experimental Research tab with outlier multipliers: Tubefilter, Aug 2026 — in limited testing, re-check availability.
- Google Trends YouTube filter: official Google Search Central tutorials (Sept 2024).
- Outlier tools landscape (third-party, freemium): 1of10, ViewStats, vidIQ Outliers, OutlierKit, TubeLab. Methodology (channel-relative multiples, format-vs-timing, 3-instance rule) is practitioner consensus — directional by nature; the harvest itself is the evidence.
- Beware fabricated "algorithm update timelines" circulating in outlier-tool marketing content — verify any claimed YouTube change against YouTube's own blog/Creator Insider before citing.
- Use the agent's universal output schema; this skill only supplies the parameters that go into it.
