---
name: trend-linkedin
title: "LinkedIn Trend Harvester Playbook"
description: "Platform-specific intel for harvesting LinkedIn trends — dwell-and-comment ranking signals, harvest URLs, scoring on comment-to-reaction ratio and reshare-with-commentary, hook taxonomy that earns the 210-char expand-click in 2026, format-mix shifts (carousel rising / video / text), and dead patterns. Activates inside an octoweb:trend session whenever the user names LinkedIn."
license: Apache-2.0
compatibility: "Octoweb browser access. Signed-in LinkedIn session required for feed and content-search surfaces."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(linkedin)
  - match(\blinkedin\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+linkedin\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest LinkedIn — current algorithm signals, harvest URLs, scoring on dwell-and-comment economics, hook taxonomy engineered for the 210-char fold, dead patterns, timing. The agent owns the shared DNA loop; this skill plugs the LinkedIn parameters into it.

## Mental model

LinkedIn's 2026 ranker is dwell-time + comment-quality + reshare-with-commentary on top of a 48–72h feed lifetime (10× longer than X). Likes are decorative. Comments and reshares are amplification. The 210-char fold ("...see more") is the entire game — a post that doesn't earn the expand click is dead. Native uploads (PDF carousel, native video) beat external links ~3–5× on reach. External links in the root post drop reach 40–60% — link in first comment.

## Rules

### Current ranking signals (2026)

| Signal | Effect |
|---|---|
| Comment-to-reaction ratio | Primary signal. >5% strong, >10% breakout |
| Reshare with commentary | Weighted higher than empty reshare |
| Author replies to comments in first 60 min | Keeps post in feed longer |
| Dwell time (proxied by post length + paragraph rhythm) | Heavily weighted |
| Reaction diversity (Like + Celebrate + Insightful + Support) | Multi-audience reach signal |
| External link in body | ~40–60% reach penalty |
| Native PDF carousel | ~3–5× reach vs text-only |
| Native video (<90 sec, auto-captioned) | High lift |
| Creator Mode / Top Voice badge | +10–25% baseline reach |
| Posted from company page | ~1/4 the reach of same content posted personally |

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Content search, relevance | `https://www.linkedin.com/search/results/content/?keywords=<topic>&sortBy=%22relevance%22` | Algorithm's pick of top posts on topic |
| Content search, date | `https://www.linkedin.com/search/results/content/?keywords=<topic>&sortBy=%22date_posted%22` | Last-week live posts |
| Hashtag feed | `https://www.linkedin.com/feed/hashtag/?keywords=<tag>` | Topic communities (LinkedIn does use hashtags) |
| Creator recent activity | `https://www.linkedin.com/in/<handle>/recent-activity/all/` | Last 30 days per anchor creator |
| Signed-in feed | `https://www.linkedin.com/feed/` | Personalized algorithmic surface for the user |

Run 4–6 in parallel. LinkedIn lazy-loads aggressively — scroll 3–5× between snapshots to surface enough posts.

### Scoring rubric (LinkedIn-specific signals)

Virality axis 0–5:
- Comment-to-reaction ratio — primary. >5% strong, >10% breakout.
- Absolute reshare count — >50 reshares in 72h means it's escaping the author's network.
- Reaction breakdown — diverse spread (Insightful + Celebrate + Like) beats mono-Like.
- Author-comment density — creator replying to 30%+ of comments extends feed life.
- Account band — micro creator (<5k) hitting 100 comments is a stronger structural signal than mega creator doing same.

Niche-fit axis 0–5 — universal scale.

Drop everything below 3 on either axis.

### Hook taxonomy (must fit above the 210-char fold)

1. Counter-intuitive claim — "I just fired our top-performing SDR."
2. Specific artifact — "Day 47 of zero meetings. Here's the cost sheet:"
3. Belief rejection — "Stop writing job descriptions. They're the reason your funnel is broken."
4. Moment of realization — "I lost a $40k deal last week. The post-mortem is ugly."
5. Pattern callout — "Every Series A founder I meet has the same broken hiring loop."

The hook must (a) sit fully above the 210-char fold and (b) create a gap the reader must close to keep reading.

### Dead patterns

- Press-release openers: "Thrilled to announce...", "Humbled to share..."
- Hustle-grindset clichés: "5AM club", "Comfort zones kill", "Mindset is everything"
- Rocket-emoji stacks (🚀🚀🚀)
- "Agree?" / "Thoughts?" closing — engagement bait
- AI vocabulary in hook: delve, leverage, harness, unlock, seamless, cutting-edge, unveil
- Humble-brags wearing story clothes — apply the strip-test (if removing the company/title kills the lesson, it's a brag)
- Numbered listicle hooks ("10 lessons...") unless paired with a sharp specific opening

### Format and length

| Goal | Length | Format |
|---|---|---|
| Virality | 150–300 chars | Single, sharp, no expand needed |
| Depth (sweet spot) | 1300–2000 chars | Story / framework, must earn expand |
| Authority | 2000–3000 chars | Long-form thinking, dwell-time bait |
| Carousel (PDF) | 8–12 slides | Strongest reshare format in 2026 |
| Native video | 30–90 sec, auto-captioned | High reach lift |

The 1300–2000 char band is the dwell-time sweet spot. Shorter posts can go viral but rarely generate the comment volume LinkedIn rewards.

### Closing CTA

Replace "Agree?" / "Thoughts?" with a real question. "Has anyone tried X in production? Did it actually behave the way I'm describing?" wins comments. Vague closings get scroll-past.

### Timing

- Best windows: Tue–Thu 8–10 AM and 11 AM–12 PM local; second wind 5–6 PM
- Mon and Fri ~30% lower reach. Weekends near-dead for B2B.
- Optimal frequency: 3–5 quality posts/week. Daily dilutes engagement.

### Saturated-take detection

LinkedIn's tech-niche saturated takes in 2026 cluster around: "AI will replace developers," "Engineering hiring is broken because of AI," "I built X in a weekend with Claude/Cursor," "AGI will arrive by ...," generic "founders should learn to code" / "founders shouldn't code" cycles. Verify saturation live before flagging.

## Examples

### Example 1: Hook + format DNA call

Bad — count without DNA:
```
This LinkedIn post about hiring got 800 reactions.
```

Good — fold analysis, DNA labeled:
```
{{Creator}} (Series B founder, 24k followers) — 812 reactions / 94 comments / 38 reshares
Comment-to-reaction ratio: 11.6% — breakout.
Reaction breakdown: 412 Like / 198 Insightful / 142 Support / 60 Celebrate — diverse.
Hook (first 187 chars, above fold):
> I just fired our top-performing SDR.
> He hit 140% of quota three quarters running. Here's why letting him go was the single best hiring decision I made this year.
Hook type: counter-intuitive claim + specific stake.
Length: 1,580 chars (dwell-time sweet spot).
Format: text-only, three paragraphs in body each starting with the lesson, no external link, link in first comment.
Author replied to 27 of 94 comments within 2h — feed life extended.
```

### Example 2: Strip-test on a humble-brag

A post by a CMO announcing a $500k pipeline win, framed as "lessons":
- Strip the company name and the dollar figure → does the lesson still teach? No → it's a brag in story clothes → flag and exclude from recommendations.

## Checklist

Before returning the LinkedIn section of the brief:
- [ ] Every cited post has creator name, follower band, reaction count, comment count, reshare count, URL, and posted-time
- [ ] Comment-to-reaction ratio computed and used as primary signal
- [ ] Reaction breakdown noted on top cluster posts (diversity signal)
- [ ] First 2–3 lines (above the 210-char fold) quoted verbatim for every cited post
- [ ] Strip-test applied to any cited post that mentions a company / title / milestone
- [ ] Format mix this window noted (text-only / carousel / video / poll percentages)
- [ ] (Opt-in mode only) Hook bank entries each fit ≤210 chars and use a taxonomy type from this skill
- [ ] Dead-pattern list applied — no recommended hook uses press-release opener, hustle clichés, rocket-stacks, or AI vocabulary
- [ ] (Opt-in mode only) Timing recommendation falls in Tue–Thu 8–10 AM / 11 AM–12 PM / 5–6 PM local
- [ ] (Opt-in mode only) Closing CTA recommended is a real specific question, not "Agree?"
- [ ] All background tabs closed

## Composition / References

- Pairs with `social-linkedin` (content domain) for writing the actual post from the brief.
- LinkedIn content-search URL parameters: `sortBy="relevance"` vs `sortBy="date_posted"`.
- Use the agent's universal output schema.
