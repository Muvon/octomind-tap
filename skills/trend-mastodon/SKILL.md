---
name: trend-mastodon
title: "Mastodon Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Mastodon trends across federation — boost-driven amplification, per-instance culture map, hashtag-following discovery, harvest URLs across home + niche instances, content-warning conventions, alt-text expectations, and dead patterns in 2026. Activates inside an octoweb:trend session whenever the user names Mastodon."
license: Apache-2.0
compatibility: "Octoweb browser access. Signed-in session on the user's home instance recommended for federated timeline; logged-out works for instance trends pages and hashtag pages."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(mastodon)
  - session(trend) content(fediverse)
  - match(\b(mastodon|fediverse|fedi)\s+(trend|trends|harvest|brief|post|toot)\b)
  - match(\b(harvest|scan|analyze)\s+(mastodon|fediverse)\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest Mastodon — current federation ranking signals, per-instance harvest URLs, scoring on boost paths, hashtag-following targeting, content-warning conventions, alt-text expectations, dead patterns, timing. The agent owns the shared DNA loop; this skill plugs the Mastodon parameters in.

## Mental model

Mastodon has no global feed and no algorithmic ranker — reach happens through boosts (its term for reposts) and through the hashtag-following feature. Each instance has its own local culture, content-moderation rules, and trends page. What you see depends on which instance you queried. Federation is slow — give posts 48–72h to develop boost chains. Marketing voice is detected and muted within seconds on tech instances. Image alt-text is expected — posts with images lacking alt-text get scolded and lose boost potential on dev/tech instances. Calibrate per instance.

## Rules

### Current ranking and amplification signals (2026)

| Signal | Effect |
|---|---|
| Boosts | Primary amplification mechanism (no algorithmic feed) |
| Boost-to-favourite ratio | >0.20 strong federation, >0.40 breaking through to other instances |
| Hashtag follows | Underused growth lever — users follow hashtags directly |
| Cross-instance reach | Same post appearing in 3+ instance trends pages = federation-viral |
| Image alt-text quality | Expected; lacking alt-text loses boost potential on dev/tech instances |
| External links in root | NOT suppressed — Mastodon treats links normally |
| Content warnings (CWs) | Required by culture on politics / NSFW / long-thread / hot-take; not on ordinary tech posts |
| Cross-post-from-X residue | Detected and muted |

### Harvest surfaces (run in parallel)

For the user's home instance:

| Surface | URL | Yields |
|---|---|---|
| Home trends | `https://<home-instance>/explore` | What the home instance's algorithm-light surface pushes |
| Home local | `https://<home-instance>/public/local` | Posts originating on the home instance (culture signal) |
| Federated timeline | `https://<home-instance>/public` | All federated posts the instance has seen |
| Home hashtag | `https://<home-instance>/tags/<tag>` | Federation-aware topic feed |

For 2–4 niche-relevant instances (for AI / agents / LLM / RAG / Codex / startup niche, common candidates include `hachyderm.io` for devs, `fosstodon.org` for FOSS, `mastodon.social` for general, `tech.lgbt`, `mas.to`):

| Surface | URL | Yields |
|---|---|---|
| Niche-instance trends | `https://<niche-instance>/explore` | Where dev/tech trends actually surface |
| Niche-instance local | `https://<niche-instance>/public/local` | Local culture of that instance |
| Niche-instance hashtag | `https://<niche-instance>/tags/<tag>` | Hashtag followers on tech-heavy instances |

Anchor profiles:
- `https://<instance>/@<handle>` — last 7 days per anchor

Run 5–8 in parallel. Mastodon paginates traditionally — usually one snapshot per tab surfaces enough posts.

### Scoring rubric (Mastodon-specific signals)

Virality axis 0–5:
- Boost-to-favourite ratio — primary federation signal
- Absolute boost count (>20 boosts in 48h on a <5k account = climbing the federation graph)
- Reply-thread depth — top-level replies that get replies
- Cross-instance reach — same post in 3+ instance trends pages = federation-viral
- Hashtag-follow surfacing — posts on hashtags with many followers reach more eyes; verify hashtag size at runtime

Niche-fit axis 0–5 — universal scale.

Do not score on view counts — Mastodon doesn't surface them.

### Hook taxonomy currently winning

1. Honest technical observation
2. Earnest question with specific context
3. First-person story with technical detail
4. Careful contrarian — backed by experience, not vibes
5. Receipt — image / chart / screenshot + 1–2 lines + thoughtful alt-text
6. Reasoned recommendation between two tools / approaches
7. Thoughtful pull-quote with brief commentary (a quote toot)

### Dead patterns

- "Follow for more!" / X-style growth-hack closing
- Hashtag stacks (>3 hashtags reads as spam faster than on X)
- Cross-post tells from X ("RT @...", "via Twitter")
- Marketing voice
- Images without alt-text
- "Birdsite" complaining (dead pattern as of 2024+)
- AI vocabulary in hook line
- Skipped CW on a politically charged or NSFW post

### Format and length

| Goal | Length (default cap 500) | Format |
|---|---|---|
| Quick take | 100–300 chars | Single |
| Thread | 3–6 self-replies, each substantive | Native — depth over chain length |
| Image post | 300–500 chars + 1–4 images with alt-text | Strong default |
| Long post | 1000–5000 chars on instances with raised caps | Sparingly — CW it |

### Hashtag prescription

For each recommended post, prescribe 1–3 hashtags:
- One niche-specific (e.g. `#LLM` `#RAG` `#AIAgents` `#Rust` `#FediVerse`)
- Optionally one community-cultural (e.g. `#TechHire`, `#100DaysOfX`)
- Optionally one timing-tied tag for live events

Verify hashtag size at runtime via `/tags/<tag>` — empty hashtag pages are dead tags. Recommend only tags with active recent posts.

### Content warning (CW) conventions

- Politics / NSFW / hot-take / very-long-thread → CW required
- Ordinary technical posts → no CW
- Skipped CW on politically charged content = quiet hide by reader defaults
- Misused CW on ordinary tech content = looks performative, kills boost potential

### Anchor accounts

Identify 5–10 niche-relevant accounts whose boost would amplify the user's post. Note follower band, instance, and recent boost behavior. Cross-instance anchors (e.g. a hachyderm.io anchor for a fosstodon post) drive federation reach faster than same-instance anchors.

### Timing

- Best windows (mixed timezone): Tue–Thu 8 AM–12 PM ET (catches Europe afternoon + US morning); second wind 4–7 PM ET
- Federation is slow — give posts 48–72h to develop
- Weekend mornings work for personal / technical writing

### Saturated-take detection

Mastodon's tech-niche saturated takes in 2026 cluster around: "ActivityPub vs AT-Proto," generic "Why I left X" posts (still common 3 years in), "FOSS ethics" debates, repeated "AI is theft" / "AI is fine" cycles. Verify saturation live.

## Examples

### Example 1: Full DNA + boost-path call

Bad — count without federation context:
```
@dev got 40 boosts on a post about RAG.
```

Good — federated handle, boost-path, alt-text quality noted:
```
@dev@hachyderm.io (3.8k followers) — 92⭐ / 47🔁 / 18💬
Boost-to-favourite ratio: 0.51 — federation breakout
Boost path: originated on hachyderm.io → boosted into fosstodon.org local trends within 6h → cross-surface in 2 other instance trends pages by 24h
Anchor @ml-anchor@fosstodon.org boosted at 5h mark, drove second-instance amplification
> Spent two weeks reading the actual RAG papers everyone cites. Three out of five contradict the benchmark methodology people quote them for.
Hook type: receipt-promise + named contrarian observation
Length: 217 chars
Format: single post + image (chart) with 3-line alt-text explaining the methodology gap
Hashtags: #LLM #RAG (2 — within limit, both with active follower coverage)
No CW (correctly — pure technical content)
DNA: technical-tone + first-person artifact + cross-instance anchor amplification
```

### Example 2: Alt-text rejection

```
@handle@instance — 200⭐ / 8🔁 (boost ratio 0.04, far below 0.20 floor)
Image attached: chart, no alt-text
Replies: 3 of 18 are alt-text scolds asking for description
Lesson: alt-text-less image posts get scolded into low boost-ratio. Always prescribe alt-text quality on image-attached recommendations.
```

## Checklist

Before returning the Mastodon section of the brief:
- [ ] Home instance + 2–4 niche-relevant instances queried
- [ ] Every cited post has full federated handle (`@user@instance.tld`), boost count, favourite count, reply count, URL, CW state
- [ ] Boost-to-favourite ratio computed and used as primary signal
- [ ] Boost path noted on every cited example (origin instance → instances it spread to)
- [ ] No score depends on view counts
- [ ] (Opt-in mode only) Hashtag prescriptions verified at runtime via `/tags/<tag>` — no dead tags
- [ ] (Opt-in mode only) CW prescribed for politics / NSFW / hot-take / long-thread; explicitly NOT for ordinary tech posts
- [ ] (Opt-in mode only) Alt-text quality requirement included for any image-attached recommendation
- [ ] Anchor-account boost-path list (5–10 accounts, instance noted, follower band) — research output: shows who currently amplifies, not who to target
- [ ] Dead-pattern list applied — no recommendation uses X-residue, hashtag stacks (>3), marketing voice, or skipped-CW patterns
- [ ] (Opt-in mode only) Instance-targeting plan included (primary home instance + 2–3 niche instances to escape into)
- [ ] All background tabs closed

## Composition / References

- Pairs with `social-mastodon` (content domain) for writing the actual post from the brief.
- Mastodon handles include the instance: always cite `@user@instance.tld` — never bare `@user`.
- Use the agent's universal output schema.
