---
name: trend-x
title: "X (Twitter) Trend Harvester Playbook"
description: "Platform-specific intel for harvesting X (Twitter) trends — current ranking mechanisms verified against the open-sourced Phoenix For You algorithm (Banger Initial Screen / slop classifier, predicted-action scoring incl. negative-weighted scroll-past, per-feed author diversity decay, mutual-follow Jaccard as ranking input, 7 PTOS kill-switches, sticky hash embeddings, video duration floor), harvest URLs with min_faves/min_retweets filters, scoring rubric on view ratios, hook taxonomy that's currently winning, and dead patterns the algorithm suppresses. Activates inside an octoweb:trend session whenever the user names X / Twitter."
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

For You has two candidate pools: in-network (Thunder, posts from followed accounts) and out-of-network (Phoenix two-tower retrieval over a global corpus, similarity-matched to the viewer's last ~127 engagement actions). Both feed into one transformer ranker that predicts per-action probabilities per viewer × post pair. Score = Σ(weight × P(action)), attenuated by per-feed author diversity decay, multiplied by OON penalty if out-of-network, and gated by safety classifiers.

What this means for harvesting (the parts that matter, not the parts you read in blog posts):

- Engagement is predicted, not observed. Phoenix scores a post based on what each specific viewer's embedding suggests they'll do. So virality = "post embedding matches lots of viewers' embedding clusters," not "post got lots of likes." Account-tier × engagement ratios still tell the story, but adjust your interpretation accordingly.
- Scroll-past is a negative signal. Posts that fail to earn dwell are actively penalised, not neutral. A post with 100k views and a 0.5% engagement ratio is worse-than-average; the viewers it reached mostly scrolled past it, dragging the author's predicted-engagement profile down.
- Author diversity is per-feed-render, not per-day. Accounts that burst-post (multiple in minutes) cannibalise their own slots in any given feed render; daily volume is fine. Don't discount accounts on daily volume alone — look at gap-between-posts.
- Mutual-follow Jaccard and "following-replied-users" are direct ranking inputs. A reply from a high-graph-overlap account cascades the post into more feeds. Big breakouts often correlate with a high-overlap account quoting/replying within the first hour.
- Banger Initial Screen + slop_score decide which posts get extra boosted candidate pools. AI-templated or recycled-shape posts get demoted regardless of raw engagement. When you cluster harvested posts, flag the ones that look like templates — they're operating below their apparent reach.
- Freshness is a hard age cutoff, not a continuous decay. Inside the freshness window, posts compete freely on embedding match; outside, they're filtered out. "Time-decayed score" is the wrong mental model.
- Video has a binary duration floor. Sub-threshold clips score zero on the video axis. Cluster video posts by duration when harvesting.
- 7 PTOS kill-switches (ViolentMedia, AdultContent, Spam, Illegal&Regulated, HateOrAbuse, ViolentSpeech, SuicideOrSelfHarm) drop posts entirely. `MediumRisk` brand-safety verdict quietly excludes posts from ad-eligible feed surfaces.

## Rules

### What the ranker actually scores (harvest interpretation guide)

The ranker sums positive-weighted predicted actions and subtracts negative-weighted ones. Exact weights are runtime params — these are the structural facts, not invented multipliers.

Positive-weighted (in the scorer's canonical order — higher up = lower marginal value):
- `favorite` (like) → cheap, easy to predict, lowest signal per unit. Discount raw likes when assessing breakouts.
- `reply`, `retweet`, `quote`, `quoted_click` → distribution-intent actions. Posts heavy on these are doing the real work.
- `share`, `share_via_dm`, `share_via_copy_link` → rare and high-signal. DM/copy-link shares are nearly invisible in public metrics but matter to the ranker.
- `click`, `profile_click`, `photo_expand` → depth signals. Profile clicks are the highest-intent of the three.
- `vqv` / `quoted_vqv` (video quality view) → only counts if video > duration floor. Discount short clips.
- `dwell` (binary), `dwell_time`, `click_dwell_time` → attention scored both as a flag and continuously.
- `follow_author` → highest-intent action; the actual growth lever.

Negative-weighted (these subtract):
- `not_interested`, `block_author`, `mute_author`, `report` → hostile actions.
- `not_dwelled` → scroll-past is a negative score, not neutral. A high-view, low-engagement-ratio post is in the red, not in the gray.

Bookmarks are not in the scored set in the open code. Treat bookmark counts as a soft proxy for "save-worthy" content but don't weight them as a ranking signal.

### Harvest implications

- Read engagement-to-view ratio as a "post survived `not_dwelled`" check. Anything under ~2% on a high-view post implies most viewers scrolled past — algorithmically a negative outcome regardless of absolute view count.
- Weight reply/quote/share counts above likes by an order of magnitude when ranking what to study. Like-heavy posts with low reply-and-share are often Phoenix mis-fires, not signal.
- Flag posts with high follow-conversion (followers gained per impression, when visible) — this is the action Phoenix weights highest in the positive direction.
- Author diversity is per-feed-render. Don't discount accounts on daily count alone; discount accounts on burst pattern (multiple posts within minutes).
- Banger / slop classifiers: when you cluster posts and find shapes that look templated — same skeleton, parallel bullets, AI-cliché phrasing — flag them as below-ceiling content. They under-perform even when raw numbers look fine.
- Mutual-follow Jaccard cascade: when a post breaks out, check which connected accounts replied or quoted in the first hour. That's the cascade mechanism, not raw reply count.
- Premium / TweepCred / 2× reach for blue-checks / "engagement pods don't work": none of these are in the open code as stated by public X advice. Don't propagate them as facts.

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

### Dead patterns (algorithmically penalised or below-ceiling)

- Wall-of-text posts — earn `not_dwelled` (negative weight); high views ≠ amplification
- Sub-threshold video — scores zero on video axis; treat as image-without-expand
- Recycled viral templates — Banger Initial Screen / slop_score flags hook shapes; below 0.4 quality_score = no boost track
- Generic AI-tool roundups without an original POV — slop-classifier territory
- Motivational fluff without specifics (no numbers, names, or proof) — slop + low dwell combo
- "What do you think?" / "Thoughts?" / "Agree?" closers — predict to scroll-past, not engagement
- Burst posting (multiple posts within minutes) — author diversity decays second-and-onwards in any feed render. Daily volume is fine; clustering is not.
- Posts in the 7 PTOS categories — full removal from feeds (not soft suppression)
- `MediumRisk` brand-safety verdict — quiet exclusion from ad-eligible feed surfaces
- "This 👇" / "Read this 🧵" / "Thread 👇" lead-ins
- Numbered thread markers ("1/12", "2/12")
- "Unpopular opinion:" prefix — just state the opinion
- Emoji bullets (🚀 🔥 ⚡ as line starters)
- Hashtag stacks (2+ hashtags) — read as low-quality by the LLM spam screen
- AI vocabulary in hook: delve, leverage, unlock, harness, unveil, seamless, cutting-edge — direct slop_score triggers
- "Here's a thread on..." intros
- Engagement bait ("RT if you agree", "Like if you relate")
- Off-niche posts — Phoenix's hash-based embedding for an account is sticky; off-niche posts hit the wrong embedding neighborhood and underperform structurally

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

For users <10k followers, weight reply-under-anchor plays equally with original posts that pass the Banger Initial Screen. The "small-account OON boost" people quote is folklore — the new-user OON multiplier in the code belongs to the viewer's account age, not the author's. Small accounts grow through embedding fit and connected-account cascades, not a follower-count multiplier.

### Timing (for inferring posting cadence from harvested accounts)

- Best windows: Tue–Thu mornings and evenings local are still strong, but the algorithm's freshness window is what actually matters — posts succeed when target audiences load feeds in the few hours after publication.
- Daily cadence beats bursts. Phoenix's embedding sharpens with consistent activity. 1–2 posts every day beats 5 posts on Tuesday + nothing else.
- No daily-count cap in code. Discount accounts on burst pattern, not volume.
- Never burst — two posts within minutes cannibalise each other inside any single feed render (author diversity decay).
- Reply presence in the first hour matters. Connected replies cascade the post into more feeds. When you cluster breakouts, check whether the author was replying in the first hour vs. absent.
- One thread OR one long-form per day — both compete for the same author-diversity slot.

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
