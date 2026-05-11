---
name: trend-x
title: "X (Twitter) Trend Harvester Playbook"
description: "Platform-specific intel for harvesting X (Twitter) trends — current ranking signals (Grok-era weights), harvest URLs with min_faves/min_retweets filters, scoring rubric on view ratios, hook taxonomy that's currently winning, and dead patterns the algorithm suppresses in 2026. Activates inside an octoweb:trend session whenever the user names X / Twitter."
license: Apache-2.0
compatibility: "Octoweb browser access. Requires signed-in X session in the user's browser for For You / Explore surfaces; logged-out works for search."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(x)
  - session(trend) content(twitter)
  - session(trend) match(\btweet)
  - match(\b(x|twitter)\s+(trend|trends|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+(x|twitter)\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest X (Twitter) — current algorithm weights, harvest surface URLs, scoring signals, hook taxonomy, dead patterns, timing. The agent owns the shared DNA loop (memory → harvest → score → cluster → DNA → hook bank → brief). This skill plugs the X-specific parameters into that loop.

## Mental model

The 2026 X algorithm is a Grok-tone-reading + engagement-weighted ranker on top of an aggressive time-decay curve. A post's score halves every ~6 hours. The first 30 minutes decide whether it gets amplified or buried. Reply-with-author-reply is weighted ~150× a like — conversation that loops back is the dominant positive signal. External links in the root post are suppressed ~50%. Optimize for replies-that-trigger-author-replies, not likes.

## Rules

### Current engagement weights (Grok-era, 2026)

| Signal | Weight vs like | Implication |
|---|---|---|
| Reply with author-reply | ~150× | Loop-back conversation is the dominant signal |
| Reply | ~27× | Any reply still dominates likes |
| Quote post | ~20× | Creates a second ranked object |
| Repost | ~20× | Distribution intent |
| Bookmark | ~10× | "Save for later" — bookmark-bait works honestly |
| Profile click | high | Reader wants more |
| Like | 1× | Cheap signal |
| Mute | –74 | Kills reach |
| Report | –369 | Account damage |
| "Not interested" | –10 | Enough kills the post |

Other levers:
- External links in root post: ~50% reach penalty. Always put links in a self-reply.
- 2+ hashtags: spam-classified. Zero or one community tag.
- Premium / Premium+: 2–4× base reach; Premium+ replies surface first.
- Account reputation (TweepCred) gates everything — low-rep accounts are invisible.

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Topic search, high-engagement | `https://x.com/search?q=<topic>%20min_faves%3A500&f=live` | Last-day niche posts with ≥500 likes |
| Topic search, breakouts | `https://x.com/search?q=<topic>%20min_faves%3A5000&f=live` | Outliers — what actually broke out |
| Topic search, top tab | `https://x.com/search?q=<topic>&f=top` | Algorithm-picked best performers |
| Explore (signed-in) | `https://x.com/explore/tabs/trending` | What X is amplifying globally right now |
| Anchor account | `https://x.com/<handle>` | Last 7 days for each anchor |
| Niche list timeline | `https://x.com/i/lists/<id>` | Curated niche timeline if user has one |
| Event hashtag (when relevant) | `https://x.com/hashtag/<tag>?src=hashtag_click&f=live` | Live event coverage |

Open 4–8 in a single parallel block of `browser_navigate` calls. Use `min_faves` and `min_retweets` operators aggressively — the unfiltered firehose wastes context. Snapshot, scrape, close.

### Scoring rubric (X-specific signals)

Virality axis 0–5:
- Engagement-to-view ratio = (replies + reposts + bookmarks) / views. >3% strong, >5% breakout.
- Reply count vs follower count — replies/followers >0.5% means the post escaped the author's bubble.
- First-2h velocity vs total — front-loaded engagement = algorithm picked it up.
- Author tier — a <10k account hitting 100k views is a stronger structural signal than a 1M account doing 100k. Weight micro breakouts higher.

Niche-fit axis 0–5 — same scale the agent applies on every platform.

Drop everything below 3 on either axis.

### Hook taxonomy currently winning

1. Broken expectation — "My X did Y. It wasn't Z." ("My agent spent $50 in tokens to solve a $5 problem. Not because it's dumb.")
2. Contrarian rule — bold imperative against default advice ("Do not be helpful. Be correct.")
3. Specific artifact — exact number/moment ("Day 3. Server broke. Here's why:")
4. Pattern callout — naming a thing everyone sees but no one says ("Most LLMs start doing when they're not sure.")
5. Lost money / lost time — stakes first ("I burned 40 hours on a config bug. The fix was one line.")
6. Cost comparison — reframing scale ("Claude wrote 12,000 lines for me last month. I reviewed 400.")
7. Anti-credential — puncturing authority ("Seven-figure founders don't write better code. They ship more of it.")
8. Observed asymmetry — "Everyone's doing X. Nobody's doing Y."

### Dead patterns (suppressed or read as AI tells in 2026)

- "This 👇" / "Read this 🧵" / "Thread 👇" lead-ins
- Numbered thread markers ("1/12", "2/12")
- "Unpopular opinion:" prefix — just state the opinion
- Emoji bullets (🚀 🔥 ⚡ as line starters)
- Hashtag stacks (2+ hashtags)
- AI vocabulary in hook: delve, leverage, unlock, harness, unveil, seamless, cutting-edge
- "Here's a thread on..." intros
- Engagement bait ("RT if you agree", "Like if you relate")
- Uniform long paragraphs (mobile read fails instantly)

### Format prescriptions

| Goal | Format | Length |
|---|---|---|
| State a take, get replies | Single post | 71–100 chars (17% higher engagement) OR 240–259 chars (max likes) |
| Teach / narrate / list | Thread | 4–8 posts; threads earn ~2.1–3× engagement over singles |
| Grow from zero | Reply under 20k–200k anchor accounts in niche | 1 post, high specificity |
| Link to external content | Root post hook (no link) + reply with link | Standard |
| Signal boost | Quote post with commentary | Commentary must add, not echo |

For users <10k followers, weight reply-under-anchor plays higher than original-post plays.

### Timing

- Best windows: Tue–Thu 8–10 AM and 5–6 PM local. Breaking-news niches skew 7–8 AM.
- Frequency: 3–5 posts/day spaced 2–3 hours apart for growth accounts. Sub-10k: 1–2 posts + 20 replies beats 5 posts alone.
- Never burst — 5 posts in 10 minutes dilutes engagement across all of them.
- One thread per day max.

### Saturated-take detection

When you cluster posts and find 5+ near-identical takes in the same window, mark it saturated. Common 2026 saturated takes in the agents / LLM / startup niches: "AGI is closer than you think," "Prompt engineering is dead," "Just use Claude / Cursor / Codex," "Vibe coding is the future," generic "AI will replace junior devs" hot takes. Verify saturation live before flagging.

## Examples

### Example 1: Hook taxonomy labeling

Bad — generic, no taxonomy label, no DNA signal:
```
This post got 2M views. It's about AI agents.
```

Good — labeled, DNA called out:
```
@handle (12k followers) — 2.1M views, 8,400 replies, 1,900 quote posts
> Most agent frameworks start retrying when they shouldn't. They keep silent when they should ask.
Hook type: pattern callout (everyone sees but no one says).
Length: 92 chars (single-post sweet spot).
DNA: contrarian observation + specific subject + zero preamble.
Posted 10:14 AM ET Tue — peak window.
```

### Example 2: Saturated-take detection

You harvest 50 posts on "RAG is dead" in the last 72h. Of those, 31 use the same hook shape (declarative rejection + cherry-picked benchmark). All recent ones underperform — average engagement-to-view ratio is 0.4%, down from 4% for the earliest 5 posts in the cluster.

Flag: `Saturated take — "RAG is dead" hook is in late-stage saturation, engagement ratio decayed 10×. Avoid this angle unless paired with a hard-contrarian re-rebuttal or a much narrower technical lens.`

## Checklist

Before returning the X section of the brief:
- [ ] Every cited post has handle, view count, reply count, repost count, quote count, URL, and posted-time visible
- [ ] Engagement-to-view ratios computed and used as the primary virality signal — not raw likes
- [ ] Account-size band tagged on every cited post (micro / mid / mega)
- [ ] First 30-min velocity considered for any top cluster
- [ ] At least one cluster has 3+ independent posts before being named a trend
- [ ] Saturated-take list surfaced — at least one per recommended angle
- [ ] Dead-pattern list applied — no recommended hook uses thread markers, "This 👇", hashtag stacks, or AI vocabulary
- [ ] (Opt-in mode only) Hook bank entries each tagged to a hook taxonomy type from this skill
- [ ] (Opt-in mode only) Format prescription per recommended angle uses the table here (length band + single/thread/quote/reply)
- [ ] (Opt-in mode only) Timing recommendation falls inside Tue–Thu 8–10 AM or 5–6 PM local unless event-attached
- [ ] All background harvest tabs closed before returning the brief

## Composition / References

- Pairs with `social-x` (content domain) for the actual post writing once the brief is in hand — same algorithm knowledge, applied to drafting instead of harvesting.
- X Search operators reference: `min_faves`, `min_retweets`, `min_replies`, `lang:en`, `since:`, `until:`, `filter:replies`, `-filter:replies`.
- Use the agent's universal output schema; this skill only supplies the parameters that go into it.
