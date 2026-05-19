---
name: social-x
title: "X (Twitter) Publishing Playbook"
description: "Ground-truth playbook for writing posts, threads, and replies on X. Encodes the actual mechanisms from the open-sourced Phoenix-based For You algorithm: predicted-action scoring, the Banger Initial Screen, video-quality-view duration threshold, per-feed author diversity decay, OON penalty, mutual-follow Jaccard ranking input, the 7 PTOS safety classifiers, brand-safety verdicts, and sticky hash-based embeddings. Plus hook formulas, single-post anatomy, thread structure, reply-first growth, trend research, and a pre-publish checklist. Activate whenever drafting anything destined for X."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to X/Twitter."
domains: content
rules:
  - content(tweet)
  - content(tweets)
  - content(twitter)
  - match(\b(twitter|x)\s+thread\b)
  - match(\btweetstorm\b)
  - match(\bpost\s+(on|to|for)\s+(x|twitter))
  - match(\b(x|twitter)\s+post\b)
  - match(\bviral\s+(tweet|thread|post)\b)
  - match(\bwrite.{0,40}for\s+(x|twitter)\b)
---

## Overview

This skill is the ground-truth recipe for writing anything that ships to X. It encodes what the 2026 algorithm rewards, what it suppresses, and the post-level craft that makes a piece actually get read — single posts, threads, replies, and bios.

Pair this with `content-voice` for human voice rules. This skill handles what wins on X; `content-voice` handles how you sound. If both are active, follow voice rules, then apply the X-specific structure below.

## Instructions

### The Algorithm — What Actually Matters for Writing

For You has two pools: posts from people the viewer follows (Thunder) and out-of-network posts retrieved by Phoenix — a transformer that embeds the viewer's last ~127 engagement actions and pulls the global posts whose embeddings are closest. Both pools merge into one ranker that predicts, per viewer × post pair, how likely each engagement action is. Sum × weights = score. Diversity and OON penalty multiply it. Safety classifiers can zero it.

Three things this means for how you write — the rest is implementation detail:

1. Phoenix predicts before engagement exists. It scores you on what this specific viewer probably does, given their history. So what wins is not "content that triggers engagement" — it's content that looks embedding-similar to what that audience already engages with. Write inside a recognisable niche, with recognisable artifacts, in your own voice. Generic content has no embedding neighborhood.

2. The valuable actions are depth + distribution, not taps. Replies, reposts, quotes, shares, follows, and dwell-time drive the score; likes are the cheapest, easiest-to-predict action and contribute the least per unit. Optimise for "what makes someone stop, send this to a friend, or go check who wrote it" — not for likes.

3. Scroll-past is a negative signal, not neutral. The ranker penalises predicted scroll-past explicitly. Posts that don't earn at least a second of dwell don't just fail to score — they actively cost score for everyone in your audience cluster. Visual density (line breaks, a sharp first line, an image worth looking at) is the cheapest dwell insurance.

### High-Leverage Levers Most People Don't Know

These mechanisms live in the code and are nearly invisible in public X advice. Each one changes a writing or posting decision. Treat as the actual rulebook.

Pass the Banger Initial Screen (or lose the boost track). Every post is scored 0–1 by a vision-language model on quality, and separately on a `slop_score`. Posts ≥ 0.4 get into extra boosted candidate pools on top of normal retrieval; slop-flagged posts are penalised even if engagement looks fine.
- DO: write something visibly specific — a real artifact, a named thing, a number, a moment. Make the image worth opening.
- AVOID: anything that looks templated — listicles with parallel bullet structure, generic motivational frames, AI-cliché phrasing, the same hook shape you used last week. The model is reading for slop, not just for "is this spam."

Scroll-past is a negative score, not zero. The ranker explicitly penalises predicted non-dwell. A post that fails to slow people down doesn't just earn nothing — it actively costs you score across the audience cluster.
- DO: lead with one short, sharp line. Use line breaks every 1–2 sentences. Attach a visual worth lingering on. Make the first half-second pay off.
- AVOID: walls of text, throat-clearing intros, unbroken paragraphs, "Today I want to talk about…" openers.

Video has a binary duration floor. Sub-threshold clips score zero on the video axis — they don't count as video at all. Same for video inside quote posts.
- DO: clear the floor (a few seconds minimum) or use an image instead.
- AVOID: 2-second meme clips when you wanted "video boost." You got "image with no expand signal," which is worse.

Author diversity is per-feed-render, not per-day. Your first post in a viewer's feed render scores full; the next one is decayed; subsequent ones decay further toward a floor. There is no daily cap. The cost is in clustering, not in count.
- DO: post 1–3× a day, spaced. If you have two posts to ship, leave a real gap between them so they hit different feed renders.
- AVOID: two posts within a few minutes; you're cannibalising your own slot in every render that catches both.

Low-follower accounts get a dedicated extra spam classifier. Posts from small accounts go through `SpamEapiLowFollowerClassifier` (a VLM) that bigger accounts skip. The early-growth phase is also the period of maximum scrutiny.
- DO: write tightly. Personal, specific, defensible content reads as not-spam.
- AVOID: link-stuffed posts, reply-bait copy, repeated phrasing across consecutive posts, anything that pattern-matches mass-produced templates. Reset your account's spam embedding with a stretch of obviously-human writing if you feel reach has dropped.

`MediumRisk` brand-safety verdict = quiet reach loss. The ads system refuses to place ads next to your post, which shrinks the feed surfaces you appear on. You won't see a notification — reach just sags.
- DO: edgy is fine. Specific is fine. Defensible is fine.
- AVOID: crude language, gore-adjacent imagery, profanity-heavy hooks, anything an ad-buyer wouldn't want their logo beside. Edgy + monetisation-safe is the sweet spot.

Seven kill-switch safety classifiers run per post. Each runs its own policy-prompted LLM: ViolentMedia, AdultContent, Spam, IllegalAndRegulatedBehaviors, HateOrAbuse, ViolentSpeech, SuicideOrSelfHarm. A hit drops you completely — not soft suppression, total removal from feeds.
- DO: write so a careful LLM read against each policy comes back clean. Make context (sarcasm, criticism, reportage) unambiguous.
- AVOID: dehumanising language, calls to harm even when "obviously joking," explicit sexual content, dosage/method specifics for self-harm topics, instructions for regulated activities. The classifier doesn't have a sense of humor.

Topic specificity = inclusion in more topic feeds. Posts are classified into specific topic IDs that expand UP to supertopics. Specific posts ride into both narrow topic feeds and the broad ones. Vague posts only land in saturated supertopics.
- DO: name the specific thing — "NBA," "NFL," "Premier League," "AI," "Crypto," "Formula 1." Not "sports," "tech," "finance."
- AVOID: hedged generality like "thoughts on the industry" or "the future of work."

Who replies and quotes you is a direct ranking input. Your post enters more viewers' feeds when accounts those viewers follow reply to it (and when mutual-follow overlap is high). One reply from a graph-relevant account does more than 100 from disconnected ones.
- DO: cultivate 5–15 high-overlap accounts in your exact niche. Make replying-to-you valuable to them — ask interesting questions in DMs, send them work they'd want to engage with publicly, build the relationship before you need it.
- AVOID: reply pods of random accounts. They don't share an embedding neighborhood with your target audience, so their replies don't cascade.

Your account's embedding is sticky. Phoenix identifies you via hashed slots whose vector is shaped by your engagement history. Your first few hundred posts permanently anchor where you live in embedding space.
- DO: pick your niche before you grow. Post consistently in it. Engage publicly with the accounts you want to be embedded near.
- AVOID: erratic niche switches, "experimenting" with unrelated content in your main account. If you need to pivot hard, expect a multi-month re-embedding period. New niches → new accounts.

Freshness is a cutoff, not a continuous decay. No "halves every 6 hours" — there's an age filter that removes posts past a threshold from the candidate pool. Inside the window you compete on score; outside, you're gone.
- DO: front-load engagement so the post is alive (high score) when peak feed-renders happen — early reply rate matters because it shapes Phoenix's predictions, not because it beats a decay curve.
- AVOID: scheduling a post and disappearing. You don't need to babysit for 24h — just make sure the post is sharp in its first few hours, which is when it has to win the embedding contest.

Each viewer sees you at most once. Bloom-filtered "previously seen" means once a viewer was served your post, they're filtered out of future renders.
- DO: write each post for first-impression reach. Repost a strong piece sparingly — it'll mostly only reach new viewers.
- AVOID: "give it another shot" reposts to the same audience. They're filtered out.

The "new user OON boost" belongs to the viewer, not the author. Viewers with young accounts see more out-of-network content. There is no follower-count-based boost to small authors.
- DO: target audiences likely to include new X users (broad topics, accessible language, low-jargon explainers).
- AVOID: assuming sub-10k accounts get magic reach. They don't. Phoenix is account-agnostic except via your sticky embedding.

### Dead-shape shortlist (format-level patterns to never produce)

Algorithmic reasons covered in the levers above. These are the visible patterns that signal "this post is one of those":

- Thread markers — "1/12", "🧵", "Thread 👇", "This 👇"
- Engagement-bait closers — "Thoughts?", "Agree?", "RT if you agree", "Like if you relate"
- Hashtag stacks (#ai #tech #startup) — one community tag max
- Emoji bullets as line starters — 🚀 ⚡ 💎
- "Unpopular opinion:", "Hot take:", "I think…", "In my opinion…", "Here's a thread on…" preambles
- AI vocabulary in hooks — delve, leverage, unlock, harness, unveil, seamless, cutting-edge (full list in `content-voice`)
- Uniform long paragraphs without line breaks

### Post Types — Pick the Right One

| Goal | Format | Length / spec |
|---|---|---|
| State a take, get replies | Single post + media | 71–100 chars (17% higher engagement) or 240–259 chars (max likes). Attach an image |
| Deep breakdown of a trending topic | Long-form post (Premium) | Up to 4000 chars; heavier weight than threads for evergreen explainers |
| Teach / narrate / list | Thread with narrative arc | 4–8 posts; Phoenix reads full thread context — setup → friction → resolution beats disconnected bangers |
| Tactical playbook | Hook + 5–8 numbered steps + closer | One post or thread; numbered steps are winning right now |
| Personal proof | "$X → $Y in Z weeks" + breakdown + screenshot | Highest-converting format for follower growth |
| Visual story | Image carousel | 3–7 slides, one bold claim per slide; gets out-of-network amplification |
| Show real work | Short video (<90s) | Real work, not promo. Media weight + dwell time |
| Grow from zero | Reply under 20k–200k anchor accounts | 1 post, high specificity. Out-of-network 3× boost amplifies strong replies |
| Link to external content | Root hook + media + no link + reply with link | Standard |
| Pure signal boost | Quote post with commentary | Commentary must add, not echo |

### Single Post — The Anatomy

Every single post has 4 parts. Drop any part and the post dies.

```
[HOOK]            ← first line, creates a gap the reader must close
[PROBLEM/SETUP]   ← 1–2 lines, raw, specific, stakes visible
[TWIST/REVEAL]    ← the counter-intuitive thing; the payoff
[TAKEAWAY]        ← one line the reader can quote, bookmark, or steal
```

Rules per part:

- Hook — first line is the whole game. Specific number, named thing, unexpected claim, or broken expectation. No preamble. No "I'd like to share…". If line 1 doesn't make the reader need line 2, throw it out.
- Problem/Setup — active voice, present tense. One idea. Stakes must be clear: what was lost, gained, or nearly lost.
- Twist — the thing everyone else isn't saying. Contrarian, counter-intuitive, or a number that breaks a common assumption. This is what gets bookmarked and quoted.
- Takeaway — short. Poster-able. Something the reader wants to keep. Not a moral, not a summary — a distilled rule.

White space is structural. One sentence per paragraph is fine and often correct. Mobile reads in short chunks.

### Hook Formulas (use, don't parrot)

Skeletons — fill with specifics from your experience; never leave the template visible.

- Broken expectation: "My X did Y. It wasn't Z." → "My agent spent $50 in tokens to solve a $5 problem. Not because it's dumb."
- Contrarian rule: bold imperative against default advice → "Do not be helpful. Be correct."
- Specific artifact: exact number or moment → "Day 3. Server broke. Here's why:"
- Pattern callout: name a thing everyone sees but no one says → "Most LLMs start doing when they're not sure."
- Lost money / time: stakes first → "I burned 40 hours on a config bug. The fix was one line."
- Cost comparison: reframe scale → "Claude wrote 12k lines last month. I reviewed 400."
- Anti-credential: puncture authority → "Seven-figure founders don't write better code. They ship more of it."
- Observed asymmetry: "Everyone's doing X. Nobody's doing Y."

Never start with: a question to the reader, a greeting, a disclaimer, "I think", a famous quote, or "Today I want to talk about."

### Thread Structure (4–8 posts)

Each post in a thread is ranked independently. Post #2 must re-hook. Post #3 must re-hook. A great post #1 with a weak #2 dies at #2.

```
Post 1 — HOOK. Stand-alone. Must work even if no one reads the thread.
Post 2 — The setup. What was the situation before.
Post 3 — The turn. What broke / what you noticed / the insight.
Post 4 — The specifics. Code, numbers, the actual thing.
Post 5 — The implication. Why this matters beyond your case.
Post 6 — (optional) Counter-cases. When this wouldn't apply.
Post 7 — Takeaway. One poster-able line.
Post 8 — (optional) CTA: "Follow for more notes on X." + quote of post 1.
```

Rules:

- No thread markers. No "1/", no "🧵", no "thread 👇". Just start.
- No mid-thread filler. If a post doesn't earn its place, cut it. 5 strong posts > 10 with filler.
- Bookmark bait works when honest. Post 7 can be "Save this if you're building agents — it's the rule I wish I'd known." Don't use if the content doesn't actually deserve saving.
- Screenshots beat text for anything that's code, numbers, error logs, or DMs. They bypass link suppression and increase dwell time. Include alt text.
- Link outside — if the thread has a destination URL (blog post, repo, video), put it in a reply under the final thread post, not in any thread post itself.

### Reply-First Growth (the actual growth engine)

For accounts under ~10k followers, 20 thoughtful replies > 1 original post. Profile visits from a viral reply convert better than from a viral root post because the reader has already seen the substance.

Pick 5–10 anchor accounts in your exact niche — sweet spot is usually 20k–200k followers. Smaller accounts have no traffic; bigger ones bury you under hundreds of replies. Get there within 15 minutes; late replies are invisible. Be the first or second substantive reply.

Reply craft — each reply is a post in miniature, with less patience:

- Open on content, not courtesy. No "Great post!", "Interesting take," "Love this." Lift a specific phrase from the root and react to it.
- 2–4 lines max. Longer reads as a blog post and gets skipped. If you need more, write a quote post instead.
- One move per reply — add a number, a counter-case, a name, or an extension. Pick one. Stacking reads defensive.
- Disagree clean — "That's not quite right — here's what we saw…" beats "Wrong." Aggression gets muted; specificity gets quoted.
- Skip the CTA ("Check my pinned", "Follow for more"). Reads desperate, kills amplification.
- Images earn replies — a screenshot, chart, or DM cap stops the scroll inside the reply chain. Alt text is free ranking.
- If your reply takes off, reply to yourself with the follow-up thought. Author-reply loops cascade into more feeds via the connected-account hydrator.

Reply shape that works (not a script): one line reacting to their specific claim, one line of your own experience or data, optional one line of implication.

### Trend Research — What's Going on in a Field

10-minute research pass before writing on any topic. Separates "post that fits the moment" from "post that feels six months late."

- Anchor accounts — pull last 7 days from 5–10 accounts that define the niche. Note which broke and which flopped; pattern-match.
- Emerging vocabulary — new terms or product names appearing in multiple accounts same week. Use early.
- Contested claims — two camps publicly disagreeing. Reply territory + strong-single-post territory.
- Under-covered angles — high volume of posts, mostly low quality. Gap for a specific, well-argued post.
- Dead takes — anything said 50× this month. Avoid unless you have a hard contrarian or a much narrower lens.
- Timing — news / release / launch? Live-event attachment lifts ceiling significantly over evergreen.

Before writing, capture: niche / saturated takes / contested claims / gap angle / event to attach to / working hook.

### Timing & Frequency

- Cadence over volume. Phoenix's embedding of you sharpens with consistent daily activity. 1–2 posts every day beats 5 posts on Tuesday and nothing else. Skipping days softens your embedding.
- Spread, don't burst. Author diversity decays your second post in the same feed render. Two posts a few minutes apart cannibalise each other. Leave hours between posts.
- No hard daily cap exists in the code. Posting 3 times a day is fine if they're spaced. The cap people quote ("2/day") is folklore.
- Best windows — Tue–Thu mornings and evenings local time are still strong, but the algorithm's recency window is what matters: post when your target audience will load their feed within the next few hours.
- Reply to your own post early. Your replies become first-class candidates for the same conversation surface, and replies from connected accounts cascade your post into their followers' feeds. Stay present for the first hour after publishing.
- One thread OR one long-form per day. Threads compete for the same author-diversity slot multiple times.

### Tone of Voice That Wins

The slop classifier flags abstract/motivational/aggregator content. Calibrate:

- First-person specific — "I built X / shipped Y / burned Z" beats "founders should…"
- Concrete numbers and names beat vague aggregates
- Builder energy — show the artifact, not the inspirational frame
- One strong opinion per post, not three hedged ones
- Proof beats prediction — "Here's what I shipped" over "here's what's possible"
- Direct second-person ("you") over generic ("founders", "people", "we")
- Contrarian only with personal proof you can defend in replies

### The Daily Play

1. Post 1–2 specific, defensible takes per day, spaced hours apart. Specific = a real number, name, artifact, or moment. Defensible = you can argue it in replies if challenged.
2. Pair text with something that earns dwell. Image, screenshot, chart, carousel, or video over the duration floor — but only if the visual is worth opening. Generic stock imagery hurts more than it helps (slop).
3. Stay present for the first hour. Reply to substantive comments. Your replies become candidates in those repliers' followers' feeds.
4. One bold opinion per post, written in your voice. Slop classifier flags templated content. First-person specific kills templates.
5. Stay inside your niche embedding. Don't whiplash topics. If you must pivot, expect the embedding to drag.
6. Reply daily to 5–15 high-overlap accounts in your niche. This is the dominant growth mechanic for sub-50k accounts. Their reply boosts you into their followers' feeds; your reply on their posts puts you in front of their audience.

### Bios, Pinned Posts, Profile

New readers decide in ~3 seconds. Profile must pay off the post.

- Bio: one line — what you do + what they get from following. No emoji stack, no "dad, husband, coffee."
- Pinned post: single best-performing post or a purpose-built "start here." Update quarterly.
- Handle + display name: searchable. Niche keyword in one of them.
- Header image: the safe place for a link. Use it as a CTA billboard.

### Thread-Vibe Matching

Before writing a reply, read the chain — not just the root. Reply chains develop micro-culture within minutes; match it or read out of place.

Scan for: length (match the median), tone (dry/technical vs. punchy/hot-take vs. casual), punctuation style (lowercase-no-period chain → don't be perfectly punctuated), shared slang or running jokes (reference, don't force), energy level (heated debate vs. quiet technical).

Calibration: hot take with 100+ replies → short, punchy, no hedging. Technical thread with 10–30 replies → specific, measured, 3–4 lines OK. Personal story → warmer, first-person, shorter. Joke/meme → match the absurdity or don't reply. Original post → your own voice; no vibe to match.

### Human Imperfection Protocol

X is mobile-first. Replies typed fast on a phone. Perfect grammar in a reply chain reads like a press release. Calibrate imperfections to context — low for original posts (0–1 max), medium for replies in fast threads (1–2), zero on technical claims and proper nouns.

Imperfection menu (pick 1–2 max per reply, never stack all):

- Missing apostrophe — `dont`, `cant`, `wont`, `its` — most natural on mobile
- Lowercase opener when the chain is already doing it
- Run-on sentence — two thoughts joined with `and` or `but` without a period
- Comma splice — "I tried this, it didn't work"
- Casual contraction — `gonna`, `kinda`, `tbh`, `ngl` — only if thread register supports it
- No closing punctuation — end without a period; common in casual X replies

Never: misspell a proper noun, brand, or technical term (reads as ignorant); stack 3+ imperfections (reads as noise); apply imperfections to data claims or technical precision; apply to a considered original post.

### Pre-Publish Checklist

Fail on any one → rewrite.

- [ ] First line stops a scroll (gap, number, named thing, broken expectation); visually skim-friendly with line breaks
- [ ] If media: worth opening (not generic stock, not sub-threshold video)
- [ ] Hook shape isn't a template you or your niche used recently
- [ ] Specific over generic — real numbers, names, moments; first-person ("I built/shipped/burned X") not third-person
- [ ] Reads like you talking — no AI vocabulary, no motivational frame, no roundup template
- [ ] An LLM reading each PTOS policy prompt comes back clean (the 7 categories); edgy is OK, ad-buyer-hostile (gore, crude profanity) is not
- [ ] Specific enough to land in a narrow topic feed ("NBA", "AI", "Crypto") not just a supertopic ("sports", "tech")
- [ ] Inside your established niche embedding — not a random topic-pivot
- [ ] One idea, one bold opinion, defensible in replies; active voice; stakes visible
- [ ] No engagement-bait closers; no hashtag stacks; no thread markers; no "This 👇" lead-ins; no emoji bullets
- [ ] Under ~150 words single; under 8 posts thread; threads have setup → friction → resolution + each post re-hooks
- [ ] Not within minutes of your last post (author diversity decay); planning to be present for first-hour replies; one thread OR one long-form per day max
- [ ] Reply only: matched length/tone/vibe of recent replies; 0–2 imperfections calibrated to context; adds a specific (number / counter-case / name / extension), not "Great point!"

## Examples

### Example 1: Single post, broken-expectation hook

Bad (generic, no stakes, dead vocabulary):
> Today I want to share an interesting insight about LLMs. It's important to note that they often struggle when they're uncertain. This is a crucial aspect of prompt engineering that developers should leverage to build better systems.

Good (hook → setup → twist → takeaway):
> My agent spent $50 in tokens to solve a $5 problem.
>
> Not because it's dumb. Because I told it to be "helpful."
>
> Changed one line in the system prompt:
> "Do not be helpful. Be correct."
>
> Problem gone.

What works: specific dollar amount, active voice, one idea, contrarian takeaway that is poster-able on its own.

### Example 2: Pattern-callout hook

> Most LLMs start doing when they're not sure.
>
> Humans stop. Ask. Check.
>
> Models confabulate a path and commit.
>
> The fix isn't smarter models. It's a system prompt that punishes silent guessing.

What works: observation everyone has seen, nobody named. Short paragraphs. Final line is a concrete handhold, not a moral.

### Example 3: Thread (5 posts, no markers)

```
[Post 1]
I watched a senior eng debug a CI failure for 4 hours.

The bug was in the commit message.
```
```
[Post 2]
The repo had a pre-commit hook that parsed commit messages.

A trailing space in the conventional-commit prefix broke the parser.

Silent failure. Non-zero exit. CI red.
```
```
[Post 3]
What made it 4 hours instead of 4 minutes:

He trusted the logs.

The logs said "test failed." The test hadn't run.
```
```
[Post 4]
The real skill wasn't debugging.

It was the moment he stopped reading logs and ran the test manually.

That took 3 hours to get to.
```
```
[Post 5]
Rule I stole from it:

If a system says it failed, check whether the system actually ran.

Most "bugs" are things that never executed.
```

What works: post 1 stands alone as a hook. Each post re-hooks. No thread markers. No filler. Post 5 is quotable on its own.

### Example 4: Reply that earns a profile visit

Someone with 80k followers posts: "Every AI startup will need to solve the context window problem eventually."

Bad reply:
> So true! Context windows are the biggest bottleneck for sure.

Good reply:
> Disagree slightly — it's not context size, it's context relevance.
>
> We tested 200k-token Claude vs. 32k-token GPT on the same codebase. The 32k model won on bug-fix accuracy because we forced better retrieval upstream.
>
> The problem is selection, not storage.

What works: disagrees specifically, has a number, names a concrete test, ends with a poster-able reframing. Profile visits from this type of reply convert several times better than from a viral root post.

### Example 5: Trend research output before writing

Niche: AI coding agents
Saturated takes this week: "Claude Code is replacing junior devs" (seen 40+ times)
Contested claims: Whether agents should have unrestricted shell access (two camps, both loud)
Gap angle: Nobody's writing about eval harnesses for agent output quality — high search volume, almost no supply
Event to attach to: Anthropic released a new tool-use API yesterday
Working hook: "Agents are shipping code faster than teams can review it. Nobody's built the review layer yet."

This research step is the difference between posts that land and posts that feel stale on arrival.

## References

- AgentSkills spec: https://agentskills.io/specification
- Companion skill: `content-voice` (human voice rules — always co-activate)
- Companion skill: `content-humanize` (AI-detection diagnostic if rewriting AI-generated drafts)
- X For You feed algorithm (Phoenix retrieval, Grox classifier, media hydrators, Author Diversity Scorer): https://github.com/xai-org/x-algorithm
