---
name: trend-x
title: "X (Twitter) Trend Harvester Playbook"
description: "Platform-specific intel for harvesting X (Twitter) trends — current ranking signals (Phoenix out-of-network retrieval, Grox content classifier, media-weighted scoring, replier-reputation reply weights, Author Diversity Scorer, 4000-char long-form weight), harvest URLs with min_faves/min_retweets filters, scoring rubric on view ratios, hook taxonomy that's currently winning, and dead patterns the algorithm suppresses. Activates inside an octoweb:trend session whenever the user names X / Twitter."
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

The For You feed is a two-source system: in-network (Thunder, accounts you follow) plus out-of-network (Phoenix retrieval over a global corpus). Phoenix is a Grok-based transformer that predicts P(like)/P(reply)/P(repost)/P(click) per post; the weighted combination is the final score. Hydrators feed media detection, mutual-follow scores, brand-safety, and engagement counts straight into the ranker. The Grox content-understanding pipeline classifies spam, post category, and recycled hook shapes. The Author Diversity Scorer attenuates repeated authors in one feed.

What this means for harvesting:
- Time decay halves the score every ~6 hours; the first 30 minutes decide amplification.
- Reply-with-author-reply is ~150× a like, and replies are now weighted by replier reputation — count alone is no longer a fair signal.
- Media-attached posts now carry a structural ~2× weight via the media hydrator; text-only posts are penalised relative to text+media.
- Out-of-network retrieval (Phoenix) means small accounts can break out without in-network traction — sub-10k accounts now get roughly 3× more out-of-network than in-network reach.
- External links in the root post are suppressed ~50%.
- Optimize for replies-that-trigger-author-replies, paired with media, from a consistent daily cadence.

## Rules

### Current engagement weights

| Signal | Weight vs like | Implication |
|---|---|---|
| Reply with author-reply | ~150× | Loop-back conversation is the dominant signal |
| Reply | ~27× (replier-rep weighted) | Replies are now weighted by replier reputation, not raw count — reply farming dies |
| Quote post | ~20× | Creates a second ranked object |
| Repost | ~20× | Distribution intent |
| Media attached (image/video) | ~2× signal boost | Media-detection hydrator feeds the ranker directly; text-only is structurally penalised |
| Bookmark | ~10× | "Save for later" — bookmark-bait works honestly |
| Profile click | high | Reader wants more |
| Like | 1× | Cheap signal |
| Mute | –74 | Kills reach |
| Report | –369 | Account damage |
| "Not interested" | –10 | Enough kills the post |

Other levers:
- Author Diversity Scorer: 4+ posts/day from one author get attenuated in-feed — cap 2/day. Harvest signal: discount accounts spamming 5+/day, their per-post weight is suppressed.
- Out-of-network (Phoenix retrieval): sub-10k accounts now reach ~3× more out-of-network than pre-May. Micro-breakouts are real signal, not noise — weight them heavily.
- Grox content classifier: detects recycled viral templates, generic AI-tool roundups, motivational fluff without specifics — they get demoted even with high raw engagement.
- Mutual-follow / engagement-pod reweighting: mutual-follow scores are a diversity signal now, not a boost. Pod-pumped posts no longer rank.
- External links in root post: ~50% reach penalty. Always put links in a self-reply.
- 2+ hashtags: spam-classified. Zero or one community tag.
- Premium / Premium+: 2–4× base reach; Premium+ replies surface first.
- Account reputation (TweepCred) gates everything — low-rep accounts are invisible.
- Consistency over volume: Phoenix uses engagement-history embeddings, so daily cadence beats bursts.

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

- Text-only posts (no media) — structurally lower signal than text+media
- Recycled viral templates — Grox classifier flags hook shapes used 50× this week
- Generic AI-tool roundups without an original POV
- Motivational fluff without specifics (no numbers, names, or proof)
- "What do you think?" / "Thoughts?" / "Agree?" closers — engagement-bait closers are flagged
- Engagement pods / mutual-follow pumping — pod amplification no longer ranks
- 4+ posts/day from one author — Author Diversity Scorer attenuates
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

| Goal | Format | Length / spec |
|---|---|---|
| State a take, get replies | Single post + media | 71–100 chars (17% higher engagement) OR 240–259 chars (max likes). Media required for full weight |
| Deep breakdown of a trending topic | Long-form post (Premium, up to 4000 chars) | Heavier signal weight than threads for evergreen explainers |
| Teach / narrate / list | Thread with narrative arc | 4–8 posts; Phoenix reads full thread context now, so setup → friction → resolution wins over disconnected hits |
| Tactical playbook | Hook + 5–8 numbered steps + closer | Currently outperforming generic threads; pair with media |
| Personal proof | "$X → $Y in Z weeks" + breakdown + screenshot | Highest-converting format for follower growth |
| Visual story | Image carousel | 3–7 slides, one bold claim per slide |
| Show real work | Short video (<90s) | Media weight + dwell time |
| Grow from zero | Reply under 20k–200k anchor accounts in niche | 1 post, high specificity. Out-of-network discovery 3× boost amplifies strong replies |
| Link to external content | Root post hook + media (no link) + reply with link | Standard |
| Signal boost | Quote post with commentary | Commentary must add, not echo |

For users <10k followers, weight reply-under-anchor plays AND original posts with media equally — out-of-network Phoenix retrieval now gives micro-accounts ~3× more reach for strong originals.

### Timing

- Best windows: Tue–Thu 8–10 AM and 5–6 PM local. Breaking-news niches skew 7–8 AM.
- Frequency: hard cap 2 posts/day (Author Diversity Scorer attenuates 4+/day). 1 strong post + 20 substantive replies beats 5 mediocre posts.
- Consistency over volume — daily 1–2 posts every day beats bursts of 5/day twice a week. Phoenix uses engagement-history embeddings to build a reader-profile match.
- Author-reply window — reply to every comment in the first 30 minutes; author-reply is the ~150× signal and stacks velocity during amplification.
- Never burst — even 2 posts within 10 minutes dilute each other.
- One thread OR one long-form per day max.

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
- X Search operators reference: `min_faves`, `min_retweets`, `min_replies`, `lang:en`, `since:`, `until:`, `filter:replies`, `-filter:replies`, `filter:media`, `filter:images`, `filter:videos` (use the media filters to harvest the current winning formats).
- X For You feed algorithm (Phoenix retrieval, Grox classifier, media hydrators, Author Diversity Scorer): https://github.com/xai-org/x-algorithm
- Use the agent's universal output schema; this skill only supplies the parameters that go into it.
