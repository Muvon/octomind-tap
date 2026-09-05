---
name: trend-instagram
title: "Instagram Trend Harvester Playbook"
description: "Harvest Instagram post, carousel, Reel, and audio patterns into a sourced trend brief with observed metrics, original adaptation angles, and uncertainty. Activate in trend sessions mentioning Instagram or Reels, or on explicit Instagram trend, scan, analysis, or harvest requests."
license: Apache-2.0
compatibility: "Browser and network access. An authorized Instagram session may be needed; app-only observations require supplied evidence."
capabilities: browser memory-read memory-write
domains: browser
rules:
  - session(trend) content(instagram)
  - session(trend) content(reels)
  - match(\binstagram\s+(trend|trends|trending|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+instagram\b)
---

## Overview

Collect current Instagram patterns that a writer can adapt to the supplied audience and business purpose. Return observations with sources and uncertainty; distinguish a visible successful post from evidence that a pattern transfers. Publishing and drafting finished posts are downstream work.

## Mental model

Mosseri named watch time, likes, and sends as leading signals and advised monitoring average watch time, likes per reach, and sends per reach (official, Mosseri via Social Media Today, 2025-01). Average watch time isn't a per-reach ratio. This dated guidance doesn't reveal a complete current ranker or establish that reach without engagement hurts.

Treat Feed, Explore, Reels, Stories, and profile observations as different contexts. Explore placement alone doesn't establish engagement velocity or its cause. Treat Stories as relationship-pattern samples, not proof of discovery performance (directional).

Total Reel watch time includes replays (official, Meta Reels Insights, 2023-04). A high view count doesn't prove unique viewers, recommendation traffic, sales, or artificial looping. Never estimate private sends or saves from public comments (directional).

## Harvest procedure

### Establish scope and recover prior observations

Record the audience, niche, language, geography, objective, and formats requested. Retrieve relevant previous observations when available; retain their capture dates. Don't describe old notes as current trend evidence. Record the browsing account context and whether supplied evidence came from the app or browser (directional).

### Navigate actual surfaces

Start at `https://www.instagram.com/` or a supplied post permalink. Follow visible navigation and copy the resulting URL. Prefer observed links over constructed keyword, tag, or audio routes; the exact deep-link templates aren't verified here. When access fails, record the failure and continue with accessible sources instead of guessing what the surface contains (directional).

| Surface to attempt | Navigation and evidence to capture |
|---|---|
| Explore | Follow the current Explore control if present; record returned URL and capture context. Treat results as an account-specific sample. |
| Reels | Follow Reels navigation or a supplied Reel; record post permalink, opening visual, caption, and displayed counters. |
| Audio | Follow the sound attribution on a Reel; copy its actual URL, title, owner, and any visible use count. |
| Keyword search | Use visible search with the buyer's topic language; log exact query, selected result type, and resulting URL. |
| Hashtag results | Follow an actual tag link; record available sorting and date information. Don't assume Top/Recent tabs exist. |
| Anchor profiles | Visit supplied or discovered niche accounts; follow their current Reel or post controls and compare recent output. |
| Stories or app-only features | Use authorized accessible views or supplied captures. Record missing surfaces explicitly; don't invent dashboard or leaderboard output. |

Use separate background tabs for independent sources only when the browser supports that safely. Avoid competing navigation calls on the same page. Snapshot observations, preserve source URLs, and close only tabs opened for the harvest (directional).

Hashtag following ended in December 2024, and the verified feature report describes a five-hashtag cap for posts and Reels (official, Instagram via Metricool Trends, 2026-06). Use tag results as topic samples; don't prescribe hashtag stacks as distribution strategy.

### Capture comparable records

For every candidate, record the permalink and handle; publication date or displayed age; capture timestamp and timezone; format and runtime if visible; follower count if available; exact displayed metric names and values; opening copy; visual sequence; audio URL; CTA destination; and apparent authorship or collaborator context (directional).

Mark unavailable fields as unknown. Treat displayed rounded counts as approximate. Calculate views relative to followers and comments relative to views only when both inputs exist, and label them analyst calculations with the source and capture time. Prefer comparison with the same account's similar-format, similar-age posts. Follower ratios aren't evidence that non-followers supplied the views (directional).

Return illustrative counts only in examples, never as harvested observations. Don't rename shares as private sends, infer saves from a checklist shape, or declare that impressions and plays no longer exist everywhere (directional).

### Track audio and pattern movement

Log a sound's displayed use count with its timestamp, then compare repeated observations. Record any visible trending indicator without assigning an unverified threshold, leaderboard size, or refresh interval. Cross-platform sound activity can supply a candidate to inspect; don't assert a fixed TikTok-to-Reels delay or trend lifespan (directional).

Compare independent accounts using a similar hook, visual structure, sound, or buyer concern. Separate permissioned reuse, shared ownership, paid amplification, and independent adoption when evidence permits. Don't classify a repost-heavy account's views as follower inertia or prove recommendation ineligibility from its profile appearance (directional).

| Assessment | Evidence to seek | Decision |
|---|---|---|
| Emerging | Fresh independent examples and rising repeated observations | Recommend a bounded test if the buyer fit is clear |
| Established | Recurring successful executions across comparable accounts | Identify the repeatable structure and what must be original |
| Saturated | Near-identical executions with weakening recent comparisons | Require a useful new angle; otherwise omit |
| Uncertain | Isolated post, missing ages, hidden metrics, or conflicting samples | Report uncertainty and the observation needed next |

These are qualitative research judgments, not platform thresholds (directional).

### Apply platform constraints to recommendations

The reported Reel maximum is 20 minutes; those over 3 minutes aren't recommended to non-followers through Explore or the Reels tab (official, Instagram Help via Socialinsider, 2026-07). Separate long existing-audience examples from discovery candidates. For narrative experiments, 45–60 seconds led Socialinsider's length analysis, without establishing a universal optimum (measured, Socialinsider, n=Reels length analysis; sample size unstated, 2026-07).

Carousels can resurface on another frame after an unengaged exposure (official, Instagram behavior reported by Socialinsider, 2026-02). Capture how opening frames stand alone; don't promise a fixed repeat exposure. Trial Reels are non-followers-first and were announced available to everyone (official, Meta Creativity, 2025-06). Don't label another account's post a trial without evidence or attach unsupported eligibility gates and testing windows.

Accounts primarily reposting unoriginal Reels, photos, or carousels can lose recommendation distribution; licensed publishers are exempt and followers may still see content (official, Instagram via TechCrunch, 2026-04). For each recommendation, name an original contribution and required source assets. A copied post with cosmetic changes isn't a useful adaptation; don't classify all participation in a shared format as a violation (directional).

## Brief assembly

Return a concise account of scope and inaccessible surfaces, followed by candidate records, pattern clusters, and recommended tests. For each recommendation, include buyer relevance, original contribution, required proof, suggested format, audio context, CTA-path observation, and confidence. Keep observed performance separate from editorial inference (directional).

Preserve contradictory evidence and unsuccessful comparable executions. State whether an apparent trend concerns awareness, useful conversation, or a visible conversion path. Don't turn view totals into predicted leads or repeat vendor case-study outcomes as expected results (directional).

## Examples

### Audio candidate with incomplete evidence

Illustrative record, not a real harvest:

“Sound [observed title], [copied URL]. Use count [earlier count] at [earlier timestamp], then [current count] at [current timestamp]. Recent independent accounts use it for repair demonstrations. Private sends and paid distribution are unknown.”

Recommendation: “Test the structure with a supplied repair recording and the author's explanation of the diagnosis. Confirm soundtrack rights. Confidence is provisional until comparable fresh posts are observed.”

This records change without inventing an adoption window or claiming algorithmic causation.

### Large count without a transferable pattern

Illustrative record, not a real harvest:

“Reel [permalink] has [displayed views]. Publication age is unavailable; surrounding posts mix unrelated topics. No independent recent examples were found in the searched sample.”

Decision: “Keep as an isolated example. We can't infer recommendation traffic, private engagement, or current demand from the visible count. Recheck age and comparable accounts before recommending the format.”

This preserves the evidence instead of declaring the account demoted or the views fake.

## Checklist

- [ ] Scope, capture context, timezone, and searched surfaces are recorded.
- [ ] Explore, Reels, search, relevant profiles, and audio were attempted where applicable; blocked or app-only surfaces are identified.
- [ ] Links came from visible navigation or supplied permalinks; no assumed deep routes or sorting tabs remain.
- [ ] Every candidate distinguishes observed values, unknown fields, and calculated ratios.
- [ ] Repeated audio observations retain timestamps; no fixed lifecycle or cross-platform lag is asserted.
- [ ] Pattern confidence uses comparable independent examples, including contradictory evidence.
- [ ] Recommended angles specify original contribution, buyer relevance, proof needs, and an observed or testable action path.
- [ ] Runtime, Trial Reels, carousel, hashtag, and originality statements retain their scope and dates.
- [ ] Only harvest-created tabs were closed; the brief doesn't imply publication occurred.

## References

- [Mosseri signals](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/), 2025-01-22.
- [Meta Reels Insights](https://about.fb.com/news/2023/04/instagram-reels-trending-audio-and-gifts-updates/), 2023-04-14.
- [Metricool Trends](https://metricool.com/instagram-trends/), 2026-06-16.
- [Socialinsider length](https://www.socialinsider.io/blog/instagram-reels-length/), 2026-07-14; [benchmark](https://www.socialinsider.io/social-media-benchmarks/instagram), 2026-02-20, Q2 update.
- [Meta Creativity](https://about.fb.com/news/2025/06/inspiring-creativity-that-brings-people-together/), 2025-06-12.
- [Instagram originality announcement reporting](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/), 2026-04-30.
- Re-validate when: navigation paths or surface names change; feature eligibility or runtime limits change; ranking or originality guidance updates; new vendor reports arrive.
Validated: 2026-09
