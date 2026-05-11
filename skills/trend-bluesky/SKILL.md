---
name: trend-bluesky
title: "Bluesky Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Bluesky trends — AT-Proto repost-driven amplification, custom-feed targeting, harvest URLs, scoring on repost-to-like ratio (no view counts), hook taxonomy tuned to Bluesky's technical / anti-marketing audience, and dead patterns in 2026. Activates inside an octoweb:trend session whenever the user names Bluesky."
license: Apache-2.0
compatibility: "Octoweb browser access. Signed-in Bluesky session needed for Discover and Following surfaces; logged-out works for search and tag pages."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(bluesky)
  - match(\bbluesky\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+bluesky\b)
  - match(\bbsky\.app\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest Bluesky — current AT-Proto ranking signals, harvest URLs including custom feeds, scoring on repost paths (no view counts), hook taxonomy for Bluesky's technical / anti-marketing audience, dead patterns, timing. The agent owns the shared DNA loop; this skill plugs the Bluesky parameters in.

## Mental model

Bluesky is repost-graph + custom-feed driven, not algorithmic-feed driven. There is no global For You by default — Discover is opt-in and most niche users live on community-curated custom feeds. Reach is built by reposts (Bluesky's term for shares) and by getting picked up by curator-maintained feeds. View counts aren't surfaced. Anchor accounts and curators drive >50% of niche post amplification — one repost from an anchor can dwarf algorithmic reach. The audience skews more technical, more left-leaning, more dev/foss-heavy, and more skeptical of marketing than X. Marketing voice gets ignored or muted fast.

## Rules

### Current ranking and amplification signals (2026)

| Signal | Effect |
|---|---|
| Reposts | Primary amplification mechanism (no algorithmic feed by default) |
| Repost-to-like ratio | >0.10 strong distribution, >0.20 breakout |
| Quote-post with commentary | Highest-quality amplification — preserves context + adds new audience |
| Cross-feed surfacing | Posts in 3+ custom feeds simultaneously = real federation amplification |
| Hashtag follows | 1–2 relevant hashtags help discovery; 3+ reads spam |
| External link in root | NOT suppressed — Bluesky treats links normally |
| Anchor-account repost | Single repost from a well-followed niche account = significant lift |
| View counts | Not surfaced — do not score on them |

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Discover (signed-in) | `https://bsky.app/feed/discover` | Algorithm-mixed surface |
| Following | `https://bsky.app/` | User's peers (only if follow-graph exists) |
| Topic search | `https://bsky.app/search?q=<topic>` | Last-day live posts |
| Hashtag pages | `https://bsky.app/hashtag/<tag>` | Topic communities (Bluesky uses real hashtags) |
| Custom feeds (niche) | `https://bsky.app/profile/<curator>/feed/<feed>` | Curator-maintained niche surfaces |
| Anchor profiles | `https://bsky.app/profile/<handle>` | Last 7 days per anchor |

For the user's AI / agents / LLM / RAG / startup niche, identify and harvest 3–5 niche custom feeds at runtime via search before relying on them. Custom-feed names rotate quarterly.

Run 5–7 surfaces in parallel. Scroll 2–3× per tab before snapshotting.

### Scoring rubric (Bluesky-specific signals)

Virality axis 0–5:
- Repost-to-like ratio — primary federation signal
- Absolute repost count (>20 reposts in 48h on a <5k account = climbing)
- Quote-post density — highest-quality amplification
- Reply-thread depth — top-level replies that themselves get replies
- Cross-feed surface — same post in 3+ custom feeds = federation-viral

Niche-fit axis 0–5 — universal scale.

Do not score on view counts — Bluesky doesn't surface them.

### Hook taxonomy currently winning

1. Honest technical observation — "After X weeks running Y, here's what surprised me"
2. Contrarian-but-substantive — "Everyone says X. I tried it. Here's where it fails."
3. Specific artifact + receipt — image / chart / code + 1–2 lines
4. The honest admission — "I was wrong about X. Here's why I changed my mind."
5. The reasoned recommendation — "Switched from A to B. Specific tradeoffs:"
6. The thoughtful question with context — Bluesky audience replies seriously
7. The quote-post commentary — adds substantive view to existing post

### Dead patterns

- X / Twitter residue ("RTs appreciated", "via X user @...")
- Engagement bait ("Drop a 🔥")
- Hashtag stacks (>2 hashtags)
- Marketing voice — Bluesky filters this fast
- AI vocabulary in hook line
- "Birdsite" complaining — dead pattern as of 2024+

### Format and length

| Goal | Length (cap 300) | Format |
|---|---|---|
| Quick take | 100–250 chars | Single |
| Thread / chain | 3–6 self-replies | Native threads, no markers needed |
| Image-attached | 200–280 chars + image | Strong lift |
| Quote-post commentary | 100–250 chars | High amplification |

### Custom-feed targeting

For each recommended post, name 2–3 custom feeds it's likely to surface in. Increase odds by:
- Including topic vocabulary the feed's algorithm filters on
- Adding 1–2 hashtags that the feed targets
- Posting when the feed's curator is active (some are manually curated)

### Anchor accounts

Identify 5–10 niche-relevant well-followed accounts whose repost would amplify the user's post. Note follower band and recent repost behavior on each.

### Timing

- Best windows (US/EU mix): Tue–Thu 9 AM–12 PM ET and 4–7 PM ET
- Slower than X — give a post 24–48h to develop before judging it dead
- One thread per day max

### Saturated-take detection

Bluesky's tech-niche saturated takes in 2026 cluster around: "AT-Proto vs ActivityPub," generic "Why I left Twitter" posts, "AI is a bubble" / "AI is the new electricity" cycles, anti-OpenAI / anti-Anthropic tribal posts. Verify saturation live.

## Examples

### Example 1: Full DNA + amplification-path call

Bad — count without path:
```
@dev.bsky.social got 80 reposts on a post about RAG.
```

Good — repost path, custom-feed surfacing, anchor noted:
```
@dev.bsky.social (4.1k followers) — 412❤ / 87🔁 / 38💬 / 14🗨
Repost-to-like ratio: 0.21 — breakout
Surfaced via: Discover (initial) → reposted into 2 niche custom feeds (Tech feed by @curator-a, LLM feed by @curator-b)
Reposted by anchor @ml-anchor.bsky.social (38k followers) at the 4h mark — drove ~60% of total amplification
> Six weeks of running a RAG eval harness against real customer queries. The retrieval recall numbers everyone quotes are measured wrong.
Hook type: honest technical observation + receipt promise
Length: 224 chars
Format: single post + chart screenshot reply with alt-text
DNA: dev-tone + specific timeframe + named-counterpoint to common belief
```

### Example 2: Marketing-voice rejection

Surface a post that has high counts but fails the audience-fit gate:
```
@brand.bsky.social — 850❤ / 12🔁 (repost ratio 0.014, far below 0.10 floor)
Hook: "Unlock the power of next-gen AI agents with our cutting-edge platform 🚀"
Failure: marketing voice, AI-vocabulary in hook, rocket emoji, near-zero repost ratio.
The like count is shallow (likely company employees + bot accounts). Bluesky's audience is filtering this. Exclude from recommendations and avoid the pattern.
```

## Checklist

Before returning the Bluesky section of the brief:
- [ ] Every cited post has full federated handle (`@user.bsky.social`), like count, repost count, reply count, quote count, URL
- [ ] Repost-to-like ratio computed and used as primary signal
- [ ] Amplification path noted on every cited example (Discover / custom feed / anchor repost)
- [ ] No score depends on view counts
- [ ] (Opt-in mode only) Custom-feed targeting prescribed for every recommended angle (2–3 feed names, verified at runtime)
- [ ] Anchor-account repost-path list included (5–10 accounts with follower bands) — research output: shows who currently amplifies in this niche, not who the user should target
- [ ] (Opt-in mode only) Hook bank entries each tagged to a taxonomy type from this skill
- [ ] Dead-pattern list applied — no recommendation uses X-residue, hashtag stacks (>2), marketing voice, or rocket emojis
- [ ] (Opt-in mode only) No more than 2 hashtags prescribed per recommended post
- [ ] All background tabs closed

## Composition / References

- Pairs with `social-bluesky` (content domain) for writing the actual post from the brief.
- AT-Proto handles include the instance: always cite `@user.bsky.social` (or custom domain handle) — not bare `@user`.
- Use the agent's universal output schema.
