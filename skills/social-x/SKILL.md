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

**Three things this means for how you write — the rest is implementation detail:**

1. **Phoenix predicts before engagement exists.** It scores you on what *this specific viewer* probably does, given their history. So what wins is not "content that triggers engagement" — it's content that **looks embedding-similar** to what that audience already engages with. Write inside a recognisable niche, with recognisable artifacts, in your own voice. Generic content has no embedding neighborhood.

2. **The valuable actions are depth + distribution, not taps.** Replies, reposts, quotes, shares, follows, and dwell-time drive the score; likes are the cheapest, easiest-to-predict action and contribute the least per unit. **Optimise for "what makes someone stop, send this to a friend, or go check who wrote it"** — not for likes.

3. **Scroll-past is a *negative* signal, not neutral.** The ranker penalises predicted scroll-past explicitly. Posts that don't earn at least a second of dwell don't just fail to score — they actively cost score for everyone in your audience cluster. Visual density (line breaks, a sharp first line, an image worth looking at) is the cheapest dwell insurance.

### High-Leverage Levers Most People Don't Know

These mechanisms live in the code and are nearly invisible in public X advice. Each one changes a writing or posting decision. Treat as the actual rulebook.

**Pass the Banger Initial Screen (or lose the boost track).** Every post is scored 0–1 by a vision-language model on quality, and separately on a `slop_score`. Posts ≥ 0.4 get into extra boosted candidate pools on top of normal retrieval; slop-flagged posts are penalised even if engagement looks fine.
- DO: write something visibly specific — a real artifact, a named thing, a number, a moment. Make the image worth opening.
- AVOID: anything that looks templated — listicles with parallel bullet structure, generic motivational frames, AI-cliché phrasing, the same hook shape you used last week. The model is reading for slop, not just for "is this spam."

**Scroll-past is a negative score, not zero.** The ranker explicitly penalises predicted non-dwell. A post that fails to slow people down doesn't just earn nothing — it actively costs you score across the audience cluster.
- DO: lead with one short, sharp line. Use line breaks every 1–2 sentences. Attach a visual worth lingering on. Make the first half-second pay off.
- AVOID: walls of text, throat-clearing intros, unbroken paragraphs, "Today I want to talk about…" openers.

**Video has a binary duration floor.** Sub-threshold clips score *zero* on the video axis — they don't count as video at all. Same for video inside quote posts.
- DO: clear the floor (a few seconds minimum) or use an image instead.
- AVOID: 2-second meme clips when you wanted "video boost." You got "image with no expand signal," which is worse.

**Author diversity is per-feed-render, not per-day.** Your first post in a viewer's feed render scores full; the next one is decayed; subsequent ones decay further toward a floor. There is no daily cap. The cost is in clustering, not in count.
- DO: post 1–3× a day, spaced. If you have two posts to ship, leave a real gap between them so they hit different feed renders.
- AVOID: two posts within a few minutes; you're cannibalising your own slot in every render that catches both.

**Low-follower accounts get a dedicated extra spam classifier.** Posts from small accounts go through `SpamEapiLowFollowerClassifier` (a VLM) that bigger accounts skip. The early-growth phase is also the period of maximum scrutiny.
- DO: write tightly. Personal, specific, defensible content reads as not-spam.
- AVOID: link-stuffed posts, reply-bait copy, repeated phrasing across consecutive posts, anything that pattern-matches mass-produced templates. Reset your account's spam embedding with a stretch of obviously-human writing if you feel reach has dropped.

**`MediumRisk` brand-safety verdict = quiet reach loss.** The ads system refuses to place ads next to your post, which shrinks the feed surfaces you appear on. You won't see a notification — reach just sags.
- DO: edgy is fine. Specific is fine. Defensible is fine.
- AVOID: crude language, gore-adjacent imagery, profanity-heavy hooks, anything an ad-buyer wouldn't want their logo beside. Edgy + monetisation-safe is the sweet spot.

**Seven kill-switch safety classifiers run per post.** Each runs its own policy-prompted LLM: ViolentMedia, AdultContent, Spam, IllegalAndRegulatedBehaviors, HateOrAbuse, ViolentSpeech, SuicideOrSelfHarm. A hit drops you completely — not soft suppression, total removal from feeds.
- DO: write so a careful LLM read against each policy comes back clean. Make context (sarcasm, criticism, reportage) unambiguous.
- AVOID: dehumanising language, calls to harm even when "obviously joking," explicit sexual content, dosage/method specifics for self-harm topics, instructions for regulated activities. The classifier doesn't have a sense of humor.

**Topic specificity = inclusion in more topic feeds.** Posts are classified into specific topic IDs that expand UP to supertopics. Specific posts ride into both narrow topic feeds and the broad ones. Vague posts only land in saturated supertopics.
- DO: name the specific thing — "NBA," "NFL," "Premier League," "AI," "Crypto," "Formula 1." Not "sports," "tech," "finance."
- AVOID: hedged generality like "thoughts on the industry" or "the future of work."

**Who replies and quotes you is a direct ranking input.** Your post enters more viewers' feeds when accounts those viewers follow reply to it (and when mutual-follow overlap is high). One reply from a graph-relevant account does more than 100 from disconnected ones.
- DO: cultivate 5–15 high-overlap accounts in your exact niche. Make replying-to-you valuable to them — ask interesting questions in DMs, send them work they'd want to engage with publicly, build the relationship before you need it.
- AVOID: reply pods of random accounts. They don't share an embedding neighborhood with your target audience, so their replies don't cascade.

**Your account's embedding is sticky.** Phoenix identifies you via hashed slots whose vector is shaped by your engagement history. Your first few hundred posts permanently anchor where you live in embedding space.
- DO: pick your niche before you grow. Post consistently in it. Engage publicly with the accounts you want to be embedded near.
- AVOID: erratic niche switches, "experimenting" with unrelated content in your main account. If you need to pivot hard, expect a multi-month re-embedding period. New niches → new accounts.

**Freshness is a cutoff, not a continuous decay.** No "halves every 6 hours" — there's an age filter that removes posts past a threshold from the candidate pool. Inside the window you compete on score; outside, you're gone.
- DO: front-load engagement so the post is alive (high score) when peak feed-renders happen — early reply rate matters because it shapes Phoenix's predictions, not because it beats a decay curve.
- AVOID: scheduling a post and disappearing. You don't need to babysit for 24h — just make sure the post is sharp in its first few hours, which is when it has to win the embedding contest.

**Each viewer sees you at most once.** Bloom-filtered "previously seen" means once a viewer was served your post, they're filtered out of future renders.
- DO: write each post for first-impression reach. Repost a strong piece sparingly — it'll mostly only reach new viewers.
- AVOID: "give it another shot" reposts to the same audience. They're filtered out.

**The "new user OON boost" belongs to the viewer, not the author.** Viewers with young accounts see more out-of-network content. There is no follower-count-based boost to small authors.
- DO: target audiences likely to include new X users (broad topics, accessible language, low-jargon explainers).
- AVOID: assuming sub-10k accounts get magic reach. They don't. Phoenix is account-agnostic except via your sticky embedding.

---

### What Kills Posts in 2026 (deprecated patterns)

These all trigger suppression, classifier penalties, or just bounce off the modern feed. Do not produce any of them:

- **Burst posting** — two posts within minutes will cannibalise each other's slots within the next feed render (author diversity decay). Spread your posts across the day.
- **Text-only walls** — earn `not_dwelled`, the negative signal. Always pair text with image, screenshot, chart, short video, or aggressive line breaks so the post is at least visually skim-friendly.
- **Sub-threshold video** — clips below `MIN_VIDEO_DURATION_MS` earn zero on the video signal axis. Either clear the floor or use an image.
- **Slop-shaped content** — content the Banger Initial Screen's `slop_score` flags: templated structure, recycled formats, AI-cliché phrasing, generic motivational frames. Quality_score < 0.4 means no banger boost.
- **Reply farming on volume** — Phoenix scores `reply` once per predicted reply, but the cascade benefit (your post entering other viewers' feeds via `following_replied_users_hydrator`) requires replies from accounts with mutual-follow overlap to the target audience. 50 disconnected replies do less than 5 connected ones.
- **Generic AI-tool roundups without an original POV** — slop-classifier territory
- **"What do you think?" / "Thoughts?" / "Agree?" closers** — predict to `not_dwelled` rather than engagement; readers register them as low-information closers
- **Motivational fluff without specifics** — no numbers, names, or proof → slop_score climbs, dwell drops
- **Engagement bait** — "retweet if you agree", "like if you relate"
- **Lead-in pointers** — "This 👇", "Read this 🧵", "Thread 👇"
- **Emoji bullets** as formatting — 🚀 ⚡ 💎 at the start of lines
- **Numbered thread markers** — "1/12", "2/12"
- **Hashtag stacks** (#ai #tech #startup #marketing) — read by the LLM spam classifier as low-quality
- **"Unpopular opinion:" prefix** — just state the opinion
- **"Here's a thread on…" intros** — start with the hook
- **"I think…" / "In my opinion…" openers** — just say it
- **AI vocabulary** — delve, leverage, unlock, harness, unveil, seamless, cutting-edge (full list in `content-voice`) — direct slop_score triggers
- **Uniform long paragraphs** — mobile dwell fails, `not_dwelled` fires
- **Anything that could trip a PTOS classifier** — the 7 categories above are full-removal kill-switches, not soft suppression
- **Posts that earn `MediumRisk` brand-safety verdict** — ad-eligible feed surfaces skip you; reach shrinks invisibly

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

These are skeletons. Fill with specifics from your actual experience. Never leave the template visible.

1. The broken expectation — "My X did Y. It wasn't Z." → "My agent spent $50 in tokens to solve a $5 problem. Not because it's dumb."
2. The contrarian rule — bold imperative stating the opposite of default advice → "Do not be helpful. Be correct."
3. The specific artifact — an exact number or moment → "Day 3. Server broke. Here's why:"
4. The pattern callout — naming a thing everyone sees but no one says → "Most LLMs start doing when they're not sure."
5. The lost money / lost time — stakes first → "I burned 40 hours on a config bug. The fix was one line."
6. The cost comparison — reframing scale → "Claude wrote 12,000 lines of code for me last month. I reviewed 400."
7. The anti-credential — puncturing authority → "Seven-figure founders don't write better code. They ship more of it."
8. The observed asymmetry — someone is doing X, nobody's doing Y → "Everyone's tuning prompts. Nobody's tuning tool descriptions."

Never start with: a question to the reader, a greeting, a disclaimer, "I think," a quote from someone famous, or "Today I want to talk about."

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

For accounts under ~10k followers, 20 thoughtful replies > 1 original post. Profile visits from a viral reply convert 3–10× better than from a viral root post.

How to do it:

1. Pick 5–10 anchor accounts in your exact niche. Not too big (200k+ replies disappear), not too small (no traffic). The sweet spot is usually 20k–200k.
2. Get to replies within 15 minutes of their post. Post notifications + scheduled blocks. Late replies are invisible.
3. Add, disagree, or extend. Never:
   - "Great post!"
   - "100%"
   - "This."
   - "Totally agree"
   - A summary of what they just said
4. Do add: a specific counter-example, an extension of the idea to a different domain, a number they didn't have, a name they should know, a gentle contradiction backed by experience.
5. Stay on-topic with the root post. Irrelevant replies get muted.
6. Be the first or second substantive reply — later replies are buried unless they're quote-worthy.

Reply template that works (not a script — a shape):
- 1 line reacting to their specific claim
- 1 line of your own specific experience or data
- Optional: 1 line of implication

#### Reply Craft (micro-rules)

A reply is its own post in miniature. Same ranking pipeline, less patience. Every extra word is a tax.

- Open on content, not courtesy. No "Great point," "Interesting take," "Love this." Start on the substance.
- Reference a specific phrase from the root post. Don't quote it back whole — lift the key word. Shows you read, not skimmed.
- 2–4 lines max. Longer replies look like blog posts and get skipped. If it needs more, it's a quote post, not a reply.
- Never address the author by @handle inside the reply — it's already threaded.
- Disagree clean. "That's not quite right — here's the thing we saw…" beats "Wrong." Aggression gets muted; specificity gets quoted.
- One move per reply. Add a number, a counter-case, a name, or an extension — pick one. Stacking all four reads defensive.
- No links in top-level replies to big accounts. External links in replies are also suppressed, just less severely. If you need to share one, post it as a reply-to-your-own-reply.
- Images earn replies. A screenshot of code, a chart, a DM exchange — they stop the scroll inside a reply chain. Alt text is free ranking.
- Skip the CTA. "Check my pinned" / "Follow for more" in a reply reads desperate and kills the reply's amplification.
- If your reply goes big, reply to yourself with a follow-up thought. Author-reply loops are the 150× signal.

### Trend Research — What's Going on in a Field

Before writing on any topic, run this 10-minute research pass. This is what separates "post that fits the moment" from "post that feels six months late."

1. Anchor accounts — pull the last 7 days of posts from 5–10 accounts who define the niche. Note which broke 50k+ views and which flopped. Pattern-match.
2. Emerging vocabulary — new terms, acronyms, or product names appearing in multiple accounts the same week. Using them early signals you're paying attention; using them late signals you're not.
3. Contested claims — two camps publicly disagreeing about the same question. This is reply territory; it's also where a strong single post can earn quote posts.
4. Under-covered angles — high-volume topic (many people posting) with mostly low-quality takes. Gap for a specific, well-argued post.
5. Dead takes — what's been said 50 times this month. Avoid. If you must write on a saturated topic, the only move is a hard contrarian or a much more specific lens.
6. Timing — is there news? A release? A launch? Posts that attach to live events within 6 hours have ~5× the ceiling of evergreen posts on the same topic.

Output of the research pass, before writing:
- Niche: _______
- Current saturated takes: _______
- Current contested claims: _______
- Gap angle chosen: _______
- Event to attach to (if any): _______
- Working hook: _______

### Timing & Frequency

- **Cadence over volume.** Phoenix's embedding of you sharpens with consistent daily activity. 1–2 posts every day beats 5 posts on Tuesday and nothing else. Skipping days softens your embedding.
- **Spread, don't burst.** Author diversity decays your second post in the same feed render. Two posts a few minutes apart cannibalise each other. Leave hours between posts.
- **No hard daily cap exists in the code.** Posting 3 times a day is fine if they're spaced. The cap people quote ("2/day") is folklore.
- **Best windows** — Tue–Thu mornings and evenings local time are still strong, but the algorithm's recency window is what matters: post when your target audience will load their feed within the next few hours.
- **Reply to your own post early.** Your replies become first-class candidates for the same conversation surface, and replies from connected accounts cascade your post into their followers' feeds. Stay present for the first hour after publishing.
- **One thread OR one long-form per day.** Threads compete for the same author-diversity slot multiple times.

### Tone of Voice That Wins

Grok reads tone; the classifier flags abstract/motivational/aggregator content. Calibrate:

- First-person specific — "I built X / shipped Y / burned Z" beats "founders should…"
- Concrete numbers and names — "Claude wrote 12k lines, I reviewed 400" beats "AI helps with coding"
- Builder energy over motivational fluff — show the artifact, not the inspirational frame
- One strong opinion per post, not three hedged ones — hedging reads as low-confidence
- "Here's what I shipped" over "here's what's possible" — proof beats prediction
- Direct second-person ("you") over generic third person ("founders", "people", "we")
- Contrarian only with personal proof you can defend in replies

### The Daily Play

1. **Post 1–2 specific, defensible takes per day, spaced hours apart.** Specific = a real number, name, artifact, or moment. Defensible = you can argue it in replies if challenged.
2. **Pair text with something that earns dwell.** Image, screenshot, chart, carousel, or video over the duration floor — but only if the visual is worth opening. Generic stock imagery hurts more than it helps (slop).
3. **Stay present for the first hour.** Reply to substantive comments. Your replies become candidates in those repliers' followers' feeds.
4. **One bold opinion per post, written in your voice.** Slop classifier flags templated content. First-person specific kills templates.
5. **Stay inside your niche embedding.** Don't whiplash topics. If you must pivot, expect the embedding to drag.
6. **Reply daily to 5–15 high-overlap accounts in your niche.** This is the dominant growth mechanic for sub-50k accounts. Their reply boosts you into their followers' feeds; your reply on their posts puts you in front of their audience.

### Bios, Pinned Posts, and the Profile

New readers come from a viral post or reply and decide in ~3 seconds whether to follow. The profile must pay off the post.

- Bio: one line saying exactly what you do + what they'll get from following. No emoji stack. No "dad, husband, coffee."
- Pinned post: your single best-performing post or a purpose-built "start here." Update quarterly.
- Handle + display name: searchable. If your niche is known by a keyword, have it in one of them.
- Header image: the one place a link is safe. Use it as a CTA billboard.

### Thread-Vibe Matching

Before writing a reply, read the existing reply chain — not just the root post. X reply chains develop their own micro-culture within minutes. Match it or your reply reads out of place.

What to scan:
- Length — are replies 1 line or 3? Match the median, not the outlier.
- Tone — dry/technical, punchy/hot-take, casual/jokey? Mirror the dominant register.
- Punctuation style — if the chain is all lowercase no-period, a perfectly punctuated reply reads robotic.
- Slang / vocabulary — if the thread is using specific jargon or a running joke, you can reference it. Don't force it.
- Energy level — a heated debate vs. a quiet technical thread need different entry points.

Vibe calibration by context:

| Context | Vibe to match |
|---|---|
| Reply to a hot take (100+ replies, fast-moving) | Short, punchy, no hedging |
| Reply to a technical thread (10–30 replies, slow) | Specific, measured, can be 3–4 lines |
| Reply to a personal story | Warmer, first-person, shorter |
| Reply to a joke/meme post | Match the absurdity level or don't reply |
| Original post (no reply chain) | Your own voice; no vibe to match |

### Human Imperfection Protocol

X is a mobile-first platform. Replies are typed fast, often on a phone, often in the middle of something else. Perfect grammar in a reply chain reads like a press release. Calibrate imperfections to context.

Imperfection level by content type:

| Content type | Level | What that means |
|---|---|---|
| Original post (single) | Low | 0–1 subtle imperfection max; posts are more considered |
| Thread post | Low | Same as single post — each is a standalone piece |
| Reply to big account | Medium | 1–2 natural imperfections; mobile-typed feel helps |
| Reply in fast-moving thread | Medium | Lowercase opener, missing apostrophe, run-on fine |
| Reply to a personal story | Low-medium | Warmer, slightly more careful |

Imperfection menu for X (pick 1–2 max per reply, never stack all):

- Missing apostrophe — `dont`, `cant`, `wont`, `its` (possessive vs contraction confusion) — most natural on mobile
- Lowercase opener — start the reply with lowercase when the chain is already doing it
- Run-on sentence — two thoughts joined with `and` or `but` without a period between them
- Dropped word — `that's the [the] thing about` — one small omission that reads like fast typing
- Comma splice — `I tried this, it didn't work` — common in casual writing
- Casual contraction — `gonna`, `kinda`, `sorta`, `tbh`, `ngl` — only if the thread register supports it
- No closing punctuation — end a reply without a period; common in casual X replies

Never do:
- Misspell a proper noun, brand name, or technical term — reads as ignorant, not human
- Stack more than 2 imperfections in one reply — becomes noise
- Add imperfections to original posts unless the post is intentionally casual/personal
- Use imperfections in a reply where you're citing data or making a technical claim — precision matters there

Calibration check before posting:
1. Read the reply chain one more time
2. Does your reply match the length and tone of the 2–3 replies above it?
3. Does it have 0–2 natural imperfections appropriate to the context?
4. Would a fast-typing human plausibly have written exactly this?

### Pre-Publish Checklist

Before shipping any post, go through this. Fail on any one → rewrite.

**Earns the dwell signal (avoids `not_dwelled` penalty)**
- [ ] First line stops a scroll — gap, number, named thing, broken expectation
- [ ] Visually skim-friendly — line breaks every 1–2 sentences, no wall of text
- [ ] If media is attached, it's worth opening (not generic stock; not sub-threshold video)

**Passes the Banger Initial Screen / slop_score**
- [ ] Hook shape is not a template you (or your niche) used recently
- [ ] Specific over generic — real numbers, names, moments, artifacts
- [ ] First-person specific ("I built/shipped/burned X"), not abstract third-person
- [ ] Reads like you talking, not writing — no AI vocabulary (delve, leverage, unlock, harness, unveil, seamless, cutting-edge)
- [ ] Not a motivational frame, not an AI-tool roundup, not a hot-take template

**Stays out of the 7 PTOS kill-switches and `MediumRisk` brand-safety verdict**
- [ ] An LLM reading each policy prompt would not flag it (ViolentMedia / AdultContent / Spam / Illegal / HateOrAbuse / ViolentSpeech / SuicideOrSelfHarm)
- [ ] Defensible: context (sarcasm, criticism, reportage) is unambiguous
- [ ] Edgy is OK; ad-buyer-hostile is not — no gore, no crude profanity, no anything that screams "MediumRisk verdict"

**Gives Phoenix a clean topic embedding**
- [ ] Specific enough to be classified into a narrow topic (e.g., "NBA," "AI," "Crypto") not just a supertopic ("sports," "tech")
- [ ] Inside your established niche embedding — not a random topic-pivot from your usual content

**Structure**
- [ ] Exactly one idea — not two, not three
- [ ] Active voice, present tense where possible
- [ ] Stakes visible: what was lost / gained / avoided
- [ ] One bold opinion per post, defensible in replies
- [ ] No engagement-bait closers ("Thoughts?", "Agree?", "What do you think?")
- [ ] No hashtag stacks, no thread markers (1/, 🧵), no "This 👇" lead-ins, no emoji bullets
- [ ] Under ~150 words for a single; under 8 posts for a thread; threads have a setup → friction → resolution arc; posts #2 and #3 re-hook independently
- [ ] Hashtags: zero or one community tag, not a stack

**Timing & cadence**
- [ ] Not within a few minutes of your last post (author diversity decay)
- [ ] Plan to be present for the first hour to reply to substantive comments
- [ ] One thread OR one long-form per day, not both

**Reply only**
- [ ] Scanned the reply chain for length / tone / vibe before writing
- [ ] 0–2 natural imperfections calibrated to context (medium for fast threads, low for technical)
- [ ] Adds something specific (number, counter-case, name, extension) — not "Great point!"

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

### Example 6: Thread-vibe matching in a fast reply chain

Root post (82k followers): "Shipping fast is a skill. Most teams treat it like a personality trait."

Reply chain vibe: short, punchy, lowercase, no periods, 1–2 lines each.

Bad reply (ignores vibe — reads robotic):
> This is an excellent observation. Shipping velocity is indeed a learnable skill that can be cultivated through deliberate practice and the right organizational structures.

Good reply (matches chain vibe, medium imperfection):
> yeah and its almost always a process problem not a people problem
>
> slow teams usually have 3 approval layers where 1 would do

What works: lowercase opener, missing apostrophe in `its`, matches the 2-line chain pattern, adds a specific counter-point.

### Example 7: Reply with calibrated imperfection (technical thread)

Root post: "Hot take: most RAG pipelines fail because of chunking strategy, not retrieval."

Reply chain vibe: technical, measured, 3–5 lines, mostly proper punctuation.

Bad reply (over-imperfected — reads careless in a technical thread):
> yeah chunking is def the thing, we tried like 5 diff approaches and its always the same lol

Good reply (low imperfection, matches technical register):
> Chunking + overlap settings, in our case. Switched from fixed 512-token chunks to semantic sentence boundaries and recall jumped ~30%.
>
> The retrieval model was fine the whole time.

What works: one small imperfection (no period after "boundaries" before the line break), specific number, technical precision maintained, matches the thread's measured tone.

## References

- AgentSkills spec: https://agentskills.io/specification
- Companion skill: `content-voice` (human voice rules — always co-activate)
- Companion skill: `content-humanize` (AI-detection diagnostic if rewriting AI-generated drafts)
- X For You feed algorithm (Phoenix retrieval, Grox classifier, media hydrators, Author Diversity Scorer): https://github.com/xai-org/x-algorithm
