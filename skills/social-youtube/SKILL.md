---
name: social-youtube
title: "YouTube Publishing Playbook"
description: "Ground-truth 2026 playbook for YouTube packaging and structure — titles, thumbnails, hooks, retention editing, Shorts vs long-form. Built on the official mechanics ('the algorithm follows the audience', per-video ranking, satisfaction-weighted watch time), measured retention data (average 23.7%, 55% gone in the first minute, the 10–20s cliff), the packaging-first discipline (top creators spend 30% of time on ideation/packaging vs 5% for small ones), the 20–30x Shorts-vs-long-form RPM gap and what the Mohan parity quote actually said, the December 2024 egregious-clickbait enforcement, and the July 2025 inauthentic-content monetization rules. Activate when crafting anything destined for YouTube."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to YouTube (long-form, Shorts, titles, thumbnails, descriptions)."
domains: content
rules:
  - content(youtube)
  - match(\byt\s+(video|short|shorts|title|thumbnail|channel)\b)
---

## Overview

YouTube's own Creator Liaison stated the whole strategy in one line: "The algorithm follows the audience, so please the audience… and then the algorithm will take care of itself." Discovery is pull, not push — recommendations are fetched per viewer, ranked per video (not per channel), and watch time is weighted by satisfaction (surveys, return visits, session continuation), not raw duration. There is no penalty box: a flopped video limits that video, not the channel.

The measured reality most creators never see: average retention across 10,000+ videos is 23.7%, over 55% of viewers leave within the first minute, and only 16% reach the final ten seconds (Retention Rabbit 2025). Meanwhile the economics are lopsided — long-form median RPM ~$2.50 vs Shorts ~$0.05 (AIR, n=274 channels), a 20–30x per-view gap. This pack exists because packaging (idea, title, thumbnail) decides most of the outcome before a second is filmed: top creators spend ~30% of their time on ideation and packaging; small creators spend ~5% (Paddy Galloway).

Pair with `content-voice` for scripts. This pack owns the packaging and structure layer; production itself is a downstream concern owned by another domain.

## Instructions

### Packaging first — the workflow that separates tiers

Title and thumbnail are decided BEFORE the script is written. If the packaging can't win the click, the video doesn't get made in that form. "The difference between a million views and 28 million views is how you package it" (Galloway); a single thumbnail improvement has measured 40x daily views in a documented case.

- Ideation patterns that repeat: comparison structures ("$10 vs $1,000 …"), "familiar but unexpected" (proven format from an unrelated niche transplanted into yours), stakes escalation.
- Portfolio rule: 80% of uploads target the proven audience overlap, 20% experiment. When a format works, ride it until it stops working.
- YouTube's native Test & Compare runs up to three thumbnail/title variants (A/B/C, since 2025) — use it for real stakes uploads; don't call tests early (YouTube labels weak evidence "inconclusive" deliberately). Verify in Studio which metric the test optimizes before trusting a "winner" — historically it favors watch-share, not raw CTR.

### Titles

- 50–60 characters as the working band (mobile truncates around there); the keyword and the hook inside the first ~40.
- The title states the specific promise the video actually keeps — since December 2024 egregious clickbait (title/thumbnail promising what the video never delivers) is removal-eligible, not just demoted, with enforcement expanding globally.
- Curiosity gap yes, lie no: "I tested every AI coding tool so you don't have to" works; "AI just KILLED programming?!" on a tool review is enforcement bait and satisfaction poison.
- CTR sensitivity is real at tiny margins — YouTube itself notes a 0.5% CTR difference can be statistically significant at scale. Typical CTR runs 2–10% (directional; search traffic skews higher, browse lower) — judge against your own baseline per traffic source, not a universal number.

### Thumbnails

Honest evidence note: nearly all circulating thumbnail percentages are unsourced aggregator claims — treat them as craft heuristics, not measurements. The defensible rules:

- One readable idea at a glance: a face with a real expression, an object with clear stakes, or a bold visual contrast — not all three competing.
- Three to five words of text maximum, complementing (never repeating) the title; must survive mobile size.
- High contrast against YouTube's white/dark UI; adjacent evidence from Netflix's artwork testing puts color contrast among the strongest click predictors.
- Design title + thumbnail as one unit: thumbnail poses the tension, title sharpens it (or vice versa) — together they must promise exactly what the video delivers.

### The hook and the retention architecture

The measured retention curve dictates structure: the steepest cliff is between seconds 10 and 20, 55%+ are gone by 60 seconds, and a clear value proposition in the first 15 seconds measures +18% retention at the one-minute mark.

- 0–5s: pattern interrupt — cold-open on the most interesting frame/claim of the whole video. No branded intros, no "welcome back to the channel" (slow intros cost casual audiences ~60% of viewers in 30 seconds).
- 5–15s: the specific promise — what the viewer gets and why it's credible ("I ran all seven, three broke, one 10x'd").
- 15–30s: commitment hook — the roadmap or the stakes that make leaving feel like a loss.
- Then re-hook every 30–45 seconds: new question, tonal shift, visual change, mini-payoff. Plant one deliberately at 25–35s where the post-hook slump hits. Videos holding >65% past minute one measure 58% higher average view duration for the rest.
- Match structure to audience mode: casual/entertainment audiences need faster cuts and earlier payoffs than dedicated-learner audiences — a measured 35% of channels use the wrong structure for their audience type.
- Bridge, don't reset: the classic failure is a strong hook followed by "okay so first, some background" — the energy cliff shows up in every retention graph.

### Length, chapters, and the session

- No universal ideal length: retention peaks at 5–10 minutes in the broadest measured dataset (31.5%), and 8+ minutes unlocks mid-roll ads — a monetization threshold, not an algorithm one. The rumored "4-minute dead zone" has no evidence; a dense 6-minute video at 80% retention beats a padded 20-minute one at 30%.
- Long videos (10min+) show a secondary exodus around the 55–65% mark — plant your strongest mid-video payoff there.
- Chapters help navigation, surface in Google results, and matter most on 30min+ content; keyword the chapter names.
- End screens and playlists feed session-continuation signals — always give the finished viewer a next step from your own catalog (linked series outperform orphan uploads).
- Descriptions: first two lines carry the search keywords and the reason to click "more"; the transcript is indexed, so say the key terms out loud too.

### Shorts — different game, different economics

- The Shorts feed's first gate is Viewed vs Swiped Away (official Studio metric): the first frame IS the thumbnail. Healthy swipe-away runs 10–30%; over 40% means the packaging or audience match failed (directional benchmarks).
- Length: sub-60s is the proven zone — measured analyses of 35B views found 13s and 50–60s both perform (bimodal); 3-minute Shorts (allowed since Oct 2024) remain unproven. Loop endings inflate percentage-viewed above 100%, which the feed reads well.
- Economics honestly: Shorts median RPM ~$0.05 vs long-form ~$2.50 — a million Shorts views ≈ $50. The Mohan "parity" quote (May 2025) was revenue per WATCH-HOUR, not per view; both facts are true. Shorts are a discovery and top-of-funnel tool, not the business.
- The Shorts→long-form bridge is not automatic: Shorts-acquired subscribers convert to long-form at measurably lower rates — use the persistent related-video link, explicit CTAs, and make Shorts that trailer your long-form pillar.
- Official: Shorts don't hurt long-form ranking; measured counterpoint: large channels saw long-form view declines after adopting Shorts (n=250, significant for 5M+ subs). Keep formats strategically separate; judge each on its own funnel.

### Cadence — the honest three-way evidence

Official: upload frequency is NOT a ranking factor, no penalty, no magic cadence. Measured correlations: channels posting 12+/month grew views ~4x faster than <1/month (vidIQ, n=10.2M channels — correlation, explicitly not causation), while Metricool (n=800K videos) finds 2–4 long-form/week is where the benefit caps. Synthesis: consistency builds audience habit and portfolio surface; volume that costs quality backfires. Pick the maximum cadence at which every upload clears your packaging bar.

### What Dies on YouTube

- Egregious clickbait — removal-eligible since Dec 2024 (promise not delivered in the video).
- Mass-produced/templated content — "inauthentic content" monetization policy (July 2025): near-identical slideshows, generic-template AI output without original insight.
- AI personas on health/legal/finance/politics — flat monetization ban.
- Reused content without transformation — clips with no commentary/narrative, pitch-shifted songs, downloads with cosmetic edits.
- Undisclosed realistic synthetic media — mandatory disclosure since May 2025; YouTube can apply the label itself.
- AI-slop production values — measured: heavily AI-generated videos show ~70% lower retention; monotonous AI narration loses 35% of viewers within 45 seconds. AI as a tool is fine and monetizable; AI as the product dies on satisfaction.
- Over-produced intros and channel-branding sequences — the retention data's most consistent killer.

## Pre-publish Checklist

- [ ] Packaging decided before scripting; title + thumbnail work as one unit and the video keeps the promise
- [ ] Title ≤60 chars, keyword + hook in the first 40, no undelivered claims
- [ ] Thumbnail: one idea, ≤5 words, survives mobile size, contrasts with the UI
- [ ] Cold open in 0–5s; value proposition by 15s; re-hooks every 30–45s; no branded intro
- [ ] Structure matches audience mode (casual vs learner pacing)
- [ ] Length is what the content needs — 8min+ only if it stays dense (mid-roll is a bonus, not a target)
- [ ] Strongest mid-payoff planted at the 55–65% position on 10min+ videos
- [ ] Description front-loads keywords; chapters named with search terms; end screen links your next video
- [ ] Shorts: first frame stops the swipe, sub-60s default, loop considered, long-form bridge CTA present
- [ ] Realistic synthetic content disclosed; nothing template-mass-produced
- [ ] Test & Compare running on high-stakes packaging; judged on the metric it actually optimizes

## Examples

### Example 1: Packaging-first applied

Idea as filmed-first: "My review of the new Claude coding features" → generic, packaging ceiling low. Packaging-first pass: thumbnail = split screen, red "$4,100" over one half, "$12" over the other; title = "I ran the same startup on Claude and on interns for a month". Same underlying content, but now there's a claim to deliver, stakes in the thumbnail, a comparison structure — and the script gets written to pay off that exact promise.

### Example 2: Retention surgery on a real curve

Analytics show 62% at 0:30 (fine), cliff to 31% by 1:10. Diagnosis: the hook promised the result, then minute one delivered channel branding + background. Fix: cold-open on the result footage, compress background to one sentence over b-roll at 0:20, move the first payoff to 0:45, add a re-hook question at 1:00. The promise-to-payoff gap, not the content, was the leak.

## References

- Official mechanics: YouTube Creator Liaison / Todd Beaupré interviews 2024–2025 ("algorithm follows the audience", per-video ranking, satisfaction weighting, frequency-not-a-factor); Creator Insider (Shorts Viewed vs Swiped Away).
- Policies: egregious clickbait enforcement (Google blog, Dec 2024), inauthentic-content monetization + AI-persona ban (July 2025), synthetic-content disclosure (mandatory May 2025).
- Measured: Retention Rabbit 2025 (n=10K+ videos — retention curve figures), vidIQ frequency study 2026 (n=10.2M channels, correlational), Metricool YouTube 2026 (n=800K videos), AIR Media-Tech RPM data (n=274 channels), Nate Black Shorts analysis (35B views), Inflow (n=5,400 Shorts). Thumbnail percentages circulating online are largely unsourced — treated here as heuristics only.
- Practitioner: Paddy Galloway (Colin & Samir interview) — time-allocation split, packaging quotes.
- Re-validate periodically: Test & Compare's winning metric, 3-minute Shorts distribution, clickbait enforcement scope, Shorts RPM by region.
- Companion skills: `content-voice` (scripts that don't sound generated), `trend-youtube` (octoweb domain) for harvesting what's working now.
