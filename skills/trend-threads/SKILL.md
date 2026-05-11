---
name: trend-threads
title: "Threads Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Threads trends — current conversation-weighted ranking signals, harvest URLs, scoring rubric using reply-to-like ratio and author-reply density (views aren't surfaced), hook taxonomy that's currently winning, and dead patterns in 2026. Activates inside an octoweb:trend session whenever the user names Threads."
license: Apache-2.0
compatibility: "Octoweb browser access. Signed-in Threads session recommended for For You / Following surfaces; logged-out works for search and tag pages."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(threads)
  - match(\bthreads\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+threads\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest Threads — current algorithm signals, harvest surface URLs, scoring on conversation depth (not views), hook taxonomy, dead patterns, timing. The agent owns the shared DNA loop; this skill supplies the Threads parameters that plug into it.

## Mental model

Threads is conversation-first by design. View counts are not reliably surfaced to authors or harvesters — the visible signals are likes, replies, reposts, and quote-posts. The algorithm weighs replies and time-in-feed heavily. A post with 200 thoughtful replies outranks a post with 50k likes. Author replying to their own post extends timeline life. Reach is built by reply-loop depth, not by raw distribution intent.

## Rules

### Current ranking signals (2026)

| Signal | Effect |
|---|---|
| Reply-to-like ratio | Primary signal. >0.10 strong, >0.20 breakout |
| Author replies on own post | Multiplier — boosts the whole thread |
| Repost-to-like ratio | Distribution intent; >0.05 is unusual on Threads |
| Image / carousel attachment | ~30–60% reach lift |
| Long-form post with paragraph breaks | Dwell-time bonus |
| External link in root | ~20–30% suppression. Put link in self-reply |
| Cross-post-from-Instagram residue | Read as a tell; reach penalty |
| Topic tags (bare-text, no #) | Discovery surface — one focused tag per post |

There is no surfaced "engagement weights" leak the way X has. Calibrate by what's visible on the page.

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Topic search, top | `https://www.threads.net/search?q=<topic>&serp_type=top` | Algorithm-picked top performers |
| Topic search, recent | `https://www.threads.net/search?q=<topic>&serp_type=default` | Last-day live posts |
| Tag pages | `https://www.threads.net/tag/<tag>` | Topic communities (Threads uses bare-text tags) |
| For You (signed-in) | `https://www.threads.net/` | Personalized algorithmic surface |
| Anchor profiles | `https://www.threads.net/@<handle>` | Last 7 days per anchor |
| Following feed | `https://www.threads.net/?feed=following` | Niche peers if user has built a graph |

Run 4–6 in parallel. Threads infinite-scrolls — scroll 2–3× via `browser_scroll` before snapshotting to load enough posts.

### Scoring rubric (Threads-specific signals)

Virality axis 0–5:
- Reply-to-like ratio — primary. >0.10 strong, >0.20 breakout.
- Absolute reply count — >100 replies in <24h is a genuine break.
- Author-reply density — does the OP reply to their own thread? Multiple self-replies = algorithm boost and extended life.
- Repost ratio — repost/like >0.05 indicates strong distribution.
- Account band — micro account hitting 500 replies is a stronger structural signal than mega doing same.

Niche-fit axis 0–5 — universal scale.

Drop everything below 3 on either axis.

Do not score on view counts — Threads doesn't surface them reliably. If a post's metadata shows a view count anyway, treat it as auxiliary, not primary.

### Hook taxonomy currently winning

1. Conversation-starter opinion — bold take that invites disagreement
2. The honest admission — "I was wrong about X. Here's why I changed my mind."
3. The specific question — only when narrow enough to invite reply (not "thoughts?")
4. The micro-story — 2–3 lines, specific moment, ends on tension
5. The contrarian observation — "Everyone says X. Nobody says Y."
6. The receipt — screenshot + 1–2 lines of context
7. The list of three — three specifics, quick rhythm, no expansion

### Dead patterns

- Instagram-style emoji bullets (🔥 ✨ 💎 as line starters)
- Hashtag stacks (Threads uses tags differently — bare text, max 1)
- "Drop a 🔥 if you agree" engagement bait
- Visible cross-post tells — "Link in bio", IG-caption residue
- AI vocabulary in hook line
- "Hot take:" / "Unpopular opinion:" prefixes — just state it
- Self-promotional opener with no hook

### Format and length

| Goal | Length | Format |
|---|---|---|
| Hot take, single | 100–250 chars | Single |
| Story / setup | 400–500 chars | Single, near Threads' post cap |
| Chain | 3–5 self-replies, ~300 chars each | Self-reply chain |
| Image post | 200–400 chars + image | Strong default in 2026 |

For any take longer than 250 chars, default to "post + 1–3 self-replies." Self-reply chains extend timeline life — the algorithm re-surfaces the original post each time a reply lands.

### Timing

- Mixed mobile-heavy audience — 9 AM–12 PM ET and 6–9 PM ET work best for tech niches
- Slower than X — give a post 24–48h to develop replies before judging it dead
- Self-reply timing — drop reply 1 within 30–60 minutes of the root post, reply 2 a few hours later when the first wave of comments lands

### Saturated-take detection

Threads' tech-niche saturated takes in 2026 cluster around: "AI is the new electricity," "GPTs are sentient" / "GPTs are dumb" hot-take cycles, generic LLM benchmark complaints, "Just use Claude" / "Just use ChatGPT" tribal posts. Verify saturation live before flagging.

## Examples

### Example 1: Hook taxonomy + reply-pattern labeling

Bad — raw count, no DNA:
```
@dev_handle got 800 likes and 150 replies on a Threads post about Claude.
```

Good — labeled, DNA called out, reply pattern named:
```
@dev_handle (8.2k followers) — 820❤ / 187💬 / 41🔁
> I tried 3 agent frameworks this week. The one that worked least is the one with the most stars.
Hook type: contrarian observation + specific count.
Length: 122 chars.
Author replied 4 times in own thread (one re-stating the claim, three answering specific replies) — extended timeline life ~3×.
DNA: short hook + invited disagreement + author-reply discipline.
```

### Example 2: Dead-pattern call

Surface a post that LOOKS viral but fails the dead-pattern gate:
```
@handle — 1.4k❤ but only 11💬 (reply-to-like 0.008, far below 0.10 floor)
Hook: "🔥 Hot take: AI agents are dead. Drop a 💀 if you agree."
Failure: engagement bait + emoji bullet + zero conversation. The like count is shallow; the post is a write-off for niche transplant.
```

## Checklist

Before returning the Threads section of the brief:
- [ ] Every cited post has handle, like count, reply count, repost count, URL, and posted-time
- [ ] Reply-to-like ratio computed and used as primary virality signal — not raw likes
- [ ] Author-reply density noted for every top cluster
- [ ] Account-size band tagged on every cited post
- [ ] No score depends on view counts
- [ ] (Opt-in mode only) Format prescription per recommended angle includes self-reply count (post + N self-replies)
- [ ] Saturated-take list surfaced — at least one per recommended angle
- [ ] No recommended hook uses cross-post tells, hashtag stacks, "Hot take:" prefixes, or emoji bullets
- [ ] (Opt-in mode only) Hook bank entries each tagged to a taxonomy type from this skill
- [ ] Self-reply timing recommended (reply 1 within 30–60 min of root, reply 2 a few hours later)
- [ ] All background tabs closed before returning brief

## Composition / References

- Pairs with `social-threads` (content domain) for writing the actual post from the brief.
- Threads search URL pattern: `serp_type=top` for algorithm-picked, `serp_type=default` for recency.
- Use the agent's universal output schema.
