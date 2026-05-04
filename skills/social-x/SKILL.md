---
name: social-x
title: "X (Twitter) Publishing Playbook"
description: "Ground-truth 2026 playbook for writing posts, threads, and replies on X (Twitter). Covers algorithm signals (Grok ranking, reply weight, time decay), hook formulas, single-post anatomy, thread structure, reply-first growth, trend research for a niche, and a pre-publish checklist. Activate whenever drafting anything destined for X."
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

# X (Twitter) Publishing Playbook

## Overview

This skill is the ground-truth recipe for writing anything that ships to X. It encodes what the 2026 algorithm rewards, what it suppresses, and the post-level craft that makes a piece actually get read — single posts, threads, replies, and bios.

Pair this with `content-voice` for human voice rules. This skill handles *what wins on X*; `content-voice` handles *how you sound*. If both are active, follow voice rules, then apply the X-specific structure below.

---

## Instructions

### The 2026 Algorithm — What Actually Matters

Since the January 2026 Grok update, X's ranking pipeline reads every post for tone and quality, then scores it on predicted engagement. The weights below are the public leak + post-Grok adjustments. Optimise for the top of this list, not the bottom.

| Signal | Weight vs. a like | Why it matters |
|---|---|---|
| Reply with author-reply | **~150×** | Conversation that loops back is the strongest positive signal |
| Reply | **~27×** | Any reply still dominates |
| Repost | **~20×** | Shows distribution intent |
| Bookmark | **~10×** | "Save for later" = high quality; bookmark-bait works |
| Quote post | **~20×** | Creates a second ranked object |
| Profile click after reading | **high** | Reader wants more from you |
| Like | 1× (baseline) | Cheap signal, low weight |
| Mute | **–74** | Kills reach |
| Report | **–369** | Account-level damage |
| "Not interested" | **–10** | Enough of these and the post is dead |

**Other levers that move the needle:**
- **Time decay** — a post's score halves every ~6 hours. The first 30 minutes decide whether it's amplified or buried.
- **Engagement velocity** — 10 replies in 15 minutes beats 10 replies in 3 hours. Post when your audience is awake.
- **External links** — suppressed roughly by half. **Never put a link in the root post.** Reply to your own post with the link.
- **Premium / Premium+** — 2–4× base reach, up to ~10× in some niches. Premium+ replies surface first in conversations.
- **Grok tone read** — snark is fine; pure negativity/attack content is suppressed. Constructive contrarian > cynical.
- **Hashtags** — dead. Use at most one, and only if it's a genuine community tag. Two or more triggers spam detection.
- **Account reputation (TweepCred)** — low-rep accounts are invisible even to their own followers. Build rep with consistent replies and author-reply conversations.

### What Kills Posts in 2026 (deprecated patterns)

These all trigger suppression or just bounce off the modern feed. Do not produce any of them:

- Engagement bait: "retweet if you agree," "like if you relate"
- Lead-in pointers: "This 👇", "Read this 🧵", "Thread 👇"
- Emoji bullets as formatting: 🚀 ⚡ 💎 at the start of lines
- Numbered thread markers: "1/12," "2/12"
- Hashtag stacks (#ai #tech #startup #marketing)
- "Unpopular opinion:" prefix — just state the opinion
- "Here's a thread on…" intros — start with the hook
- "I think…" / "In my opinion…" openers — just say it
- AI vocabulary: delve, leverage, unlock, harness, unveil, seamless, cutting-edge (full list in `content-voice`)
- Uniform long paragraphs — mobile reads fail instantly

---

### Post Types — Pick the Right One

| Goal | Format | Length |
|---|---|---|
| State a take, get replies | Single post | 71–100 chars (17% higher engagement) or 240–259 chars (max likes) |
| Teach / narrate / list | Thread | 4–8 posts (sweet spot); threads get ~2.1–3× engagement over singles |
| Grow from zero | Reply under bigger accounts in your niche | 1 post, high specificity |
| Link to external content | Root post with hook + no link + reply with link | Standard |
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

- **Hook** — first line is the whole game. Specific number, named thing, unexpected claim, or broken expectation. No preamble. No "I'd like to share…". If line 1 doesn't make the reader need line 2, throw it out.
- **Problem/Setup** — active voice, present tense. One idea. Stakes must be clear: what was lost, gained, or nearly lost.
- **Twist** — the thing everyone else isn't saying. Contrarian, counter-intuitive, or a number that breaks a common assumption. This is what gets bookmarked and quoted.
- **Takeaway** — short. Poster-able. Something the reader wants to keep. Not a moral, not a summary — a distilled rule.

**White space is structural.** One sentence per paragraph is fine and often correct. Mobile reads in short chunks.

---

### Hook Formulas (use, don't parrot)

These are skeletons. Fill with specifics from your actual experience. Never leave the template visible.

1. **The broken expectation** — "My X did Y. It wasn't Z." → *"My agent spent $50 in tokens to solve a $5 problem. Not because it's dumb."*
2. **The contrarian rule** — bold imperative stating the opposite of default advice → *"Do not be helpful. Be correct."*
3. **The specific artifact** — an exact number or moment → *"Day 3. Server broke. Here's why:"*
4. **The pattern callout** — naming a thing everyone sees but no one says → *"Most LLMs start doing when they're not sure."*
5. **The lost money / lost time** — stakes first → *"I burned 40 hours on a config bug. The fix was one line."*
6. **The cost comparison** — reframing scale → *"Claude wrote 12,000 lines of code for me last month. I reviewed 400."*
7. **The anti-credential** — puncturing authority → *"Seven-figure founders don't write better code. They ship more of it."*
8. **The observed asymmetry** — someone is doing X, nobody's doing Y → *"Everyone's tuning prompts. Nobody's tuning tool descriptions."*

**Never** start with: a question to the reader, a greeting, a disclaimer, "I think," a quote from someone famous, or "Today I want to talk about."

---

### Thread Structure (4–8 posts)

Each post in a thread is ranked **independently**. Post #2 must re-hook. Post #3 must re-hook. A great post #1 with a weak #2 dies at #2.

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

- **No thread markers.** No "1/", no "🧵", no "thread 👇". Just start.
- **No mid-thread filler.** If a post doesn't earn its place, cut it. 5 strong posts > 10 with filler.
- **Bookmark bait works when honest.** Post 7 can be "Save this if you're building agents — it's the rule I wish I'd known." Don't use if the content doesn't actually deserve saving.
- **Screenshots beat text** for anything that's code, numbers, error logs, or DMs. They bypass link suppression and increase dwell time. Include alt text.
- **Link outside** — if the thread has a destination URL (blog post, repo, video), put it in a reply under the final thread post, not in any thread post itself.

---

### Reply-First Growth (the actual growth engine)

For accounts under ~10k followers, **20 thoughtful replies > 1 original post**. Profile visits from a viral reply convert 3–10× better than from a viral root post.

How to do it:

1. **Pick 5–10 anchor accounts** in your exact niche. Not too big (200k+ replies disappear), not too small (no traffic). The sweet spot is usually 20k–200k.
2. **Get to replies within 15 minutes** of their post. Post notifications + scheduled blocks. Late replies are invisible.
3. **Add, disagree, or extend.** Never:
   - "Great post!"
   - "100%"
   - "This."
   - "Totally agree"
   - A summary of what they just said
4. **Do add:** a specific counter-example, an extension of the idea to a different domain, a number they didn't have, a name they should know, a gentle contradiction backed by experience.
5. **Stay on-topic with the root post.** Irrelevant replies get muted.
6. **Be the first or second substantive reply** — later replies are buried unless they're quote-worthy.

Reply template that works (not a script — a shape):
- 1 line reacting to their specific claim
- 1 line of your own specific experience or data
- Optional: 1 line of implication

#### Reply Craft (micro-rules)

A reply is its own post in miniature. Same ranking pipeline, less patience. Every extra word is a tax.

- **Open on content, not courtesy.** No "Great point," "Interesting take," "Love this." Start on the substance.
- **Reference a specific phrase from the root post.** Don't quote it back whole — lift the key word. Shows you read, not skimmed.
- **2–4 lines max.** Longer replies look like blog posts and get skipped. If it needs more, it's a quote post, not a reply.
- **Never address the author by @handle inside the reply** — it's already threaded.
- **Disagree clean.** "That's not quite right — here's the thing we saw…" beats "Wrong." Aggression gets muted; specificity gets quoted.
- **One move per reply.** Add a number, a counter-case, a name, or an extension — pick one. Stacking all four reads defensive.
- **No links in top-level replies** to big accounts. External links in replies are also suppressed, just less severely. If you need to share one, post it as a reply-to-your-own-reply.
- **Images earn replies.** A screenshot of code, a chart, a DM exchange — they stop the scroll inside a reply chain. Alt text is free ranking.
- **Skip the CTA.** "Check my pinned" / "Follow for more" in a reply reads desperate and kills the reply's amplification.
- **If your reply goes big, reply to yourself** with a follow-up thought. Author-reply loops are the 150× signal.

---

### Trend Research — What's Going on in a Field

Before writing on any topic, run this 10-minute research pass. This is what separates "post that fits the moment" from "post that feels six months late."

1. **Anchor accounts** — pull the last 7 days of posts from 5–10 accounts who define the niche. Note which broke 50k+ views and which flopped. Pattern-match.
2. **Emerging vocabulary** — new terms, acronyms, or product names appearing in multiple accounts the same week. Using them early signals you're paying attention; using them late signals you're not.
3. **Contested claims** — two camps publicly disagreeing about the same question. This is reply territory; it's also where a strong single post can earn quote posts.
4. **Under-covered angles** — high-volume topic (many people posting) with mostly low-quality takes. Gap for a specific, well-argued post.
5. **Dead takes** — what's been said 50 times this month. Avoid. If you must write on a saturated topic, the only move is a hard contrarian or a much more specific lens.
6. **Timing** — is there news? A release? A launch? Posts that attach to live events within 6 hours have ~5× the ceiling of evergreen posts on the same topic.

Output of the research pass, before writing:
- Niche: _______
- Current saturated takes: _______
- Current contested claims: _______
- Gap angle chosen: _______
- Event to attach to (if any): _______
- Working hook: _______

---

### Timing & Frequency

- **Best windows (2026 data)** — Tue–Thu, 8–10 AM local and 5–6 PM local. Breaking-news niches skew earlier (7–8 AM).
- **Frequency** — 3–5 posts/day spaced 2–3 hours apart is the documented sweet spot for growth accounts. Sub-10k: 1–2 posts/day + 20 replies is more effective than 5 posts/day alone.
- **Do not post in bursts.** Five posts in ten minutes dilutes engagement across all of them.
- **One thread per day max.** Threads consume reply budget; posting two threads in a day caps both.

---

### Bios, Pinned Posts, and the Profile

New readers come from a viral post or reply and decide in ~3 seconds whether to follow. The profile must pay off the post.

- **Bio**: one line saying exactly what you do + what they'll get from following. No emoji stack. No "dad, husband, coffee."
- **Pinned post**: your single best-performing post or a purpose-built "start here." Update quarterly.
- **Handle + display name**: searchable. If your niche is known by a keyword, have it in one of them.
- **Header image**: the one place a link is safe. Use it as a CTA billboard.

---

### Thread-Vibe Matching

Before writing a reply, read the existing reply chain — not just the root post. X reply chains develop their own micro-culture within minutes. Match it or your reply reads out of place.

**What to scan:**
- **Length** — are replies 1 line or 3? Match the median, not the outlier.
- **Tone** — dry/technical, punchy/hot-take, casual/jokey? Mirror the dominant register.
- **Punctuation style** — if the chain is all lowercase no-period, a perfectly punctuated reply reads robotic.
- **Slang / vocabulary** — if the thread is using specific jargon or a running joke, you can reference it. Don't force it.
- **Energy level** — a heated debate vs. a quiet technical thread need different entry points.

**Vibe calibration by context:**

| Context | Vibe to match |
|---|---|
| Reply to a hot take (100+ replies, fast-moving) | Short, punchy, no hedging |
| Reply to a technical thread (10–30 replies, slow) | Specific, measured, can be 3–4 lines |
| Reply to a personal story | Warmer, first-person, shorter |
| Reply to a joke/meme post | Match the absurdity level or don't reply |
| Original post (no reply chain) | Your own voice; no vibe to match |

---

### Human Imperfection Protocol

X is a mobile-first platform. Replies are typed fast, often on a phone, often in the middle of something else. Perfect grammar in a reply chain reads like a press release. Calibrate imperfections to context.

**Imperfection level by content type:**

| Content type | Level | What that means |
|---|---|---|
| Original post (single) | Low | 0–1 subtle imperfection max; posts are more considered |
| Thread post | Low | Same as single post — each is a standalone piece |
| Reply to big account | Medium | 1–2 natural imperfections; mobile-typed feel helps |
| Reply in fast-moving thread | Medium | Lowercase opener, missing apostrophe, run-on fine |
| Reply to a personal story | Low-medium | Warmer, slightly more careful |

**Imperfection menu for X (pick 1–2 max per reply, never stack all):**

- **Missing apostrophe** — `dont`, `cant`, `wont`, `its` (possessive vs contraction confusion) — most natural on mobile
- **Lowercase opener** — start the reply with lowercase when the chain is already doing it
- **Run-on sentence** — two thoughts joined with `and` or `but` without a period between them
- **Dropped word** — `that's the [the] thing about` — one small omission that reads like fast typing
- **Comma splice** — `I tried this, it didn't work` — common in casual writing
- **Casual contraction** — `gonna`, `kinda`, `sorta`, `tbh`, `ngl` — only if the thread register supports it
- **No closing punctuation** — end a reply without a period; common in casual X replies

**Never do:**
- Misspell a proper noun, brand name, or technical term — reads as ignorant, not human
- Stack more than 2 imperfections in one reply — becomes noise
- Add imperfections to original posts unless the post is intentionally casual/personal
- Use imperfections in a reply where you're citing data or making a technical claim — precision matters there

**Calibration check before posting:**
1. Read the reply chain one more time
2. Does your reply match the length and tone of the 2–3 replies above it?
3. Does it have 0–2 natural imperfections appropriate to the context?
4. Would a fast-typing human plausibly have written exactly this?

---

### Pre-Publish Checklist

Before shipping any post, go through this. Fail on any one → rewrite.

- [ ] First line creates a gap the reader has to close
- [ ] Exactly one idea — not two, not three
- [ ] Specific over generic — real numbers, names, moments
- [ ] Active voice, present tense where possible
- [ ] Stakes visible: what was lost / gained / avoided
- [ ] Under 150 words for a single post; under 8 posts for a thread
- [ ] No dead AI vocabulary, no engagement bait, no thread markers
- [ ] No hashtags (or at most one community tag)
- [ ] No external link in the root post; link goes in reply
- [ ] Reads like you talking, not writing
- [ ] If contrarian: you actually believe it and can defend it in replies
- [ ] For threads: post #2 and #3 re-hook independently
- [ ] Scheduled for a peak window for your audience
- [ ] **Reply only:** scanned the reply chain for length/tone/vibe before writing
- [ ] **Reply only:** 0–2 natural imperfections calibrated to context (medium for fast threads, low for technical)

---

## Examples

### Example 1: Single post, broken-expectation hook

**Bad (generic, no stakes, dead vocabulary):**
> Today I want to share an interesting insight about LLMs. It's important to note that they often struggle when they're uncertain. This is a crucial aspect of prompt engineering that developers should leverage to build better systems.

**Good (hook → setup → twist → takeaway):**
> My agent spent $50 in tokens to solve a $5 problem.
>
> Not because it's dumb. Because I told it to be "helpful."
>
> Changed one line in the system prompt:
> "Do not be helpful. Be correct."
>
> Problem gone.

What works: specific dollar amount, active voice, one idea, contrarian takeaway that is poster-able on its own.

---

### Example 2: Pattern-callout hook

> Most LLMs start doing when they're not sure.
>
> Humans stop. Ask. Check.
>
> Models confabulate a path and commit.
>
> The fix isn't smarter models. It's a system prompt that punishes silent guessing.

What works: observation everyone has seen, nobody named. Short paragraphs. Final line is a concrete handhold, not a moral.

---

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

---

### Example 4: Reply that earns a profile visit

Someone with 80k followers posts: *"Every AI startup will need to solve the context window problem eventually."*

**Bad reply:**
> So true! Context windows are the biggest bottleneck for sure.

**Good reply:**
> Disagree slightly — it's not context size, it's context *relevance*.
>
> We tested 200k-token Claude vs. 32k-token GPT on the same codebase. The 32k model won on bug-fix accuracy because we forced better retrieval upstream.
>
> The problem is selection, not storage.

What works: disagrees specifically, has a number, names a concrete test, ends with a poster-able reframing. Profile visits from this type of reply convert several times better than from a viral root post.

---

### Example 5: Trend research output before writing

Niche: AI coding agents
Saturated takes this week: "Claude Code is replacing junior devs" (seen 40+ times)
Contested claims: Whether agents should have unrestricted shell access (two camps, both loud)
Gap angle: Nobody's writing about eval harnesses for agent output quality — high search volume, almost no supply
Event to attach to: Anthropic released a new tool-use API yesterday
Working hook: "Agents are shipping code faster than teams can review it. Nobody's built the review layer yet."

This research step is the difference between posts that land and posts that feel stale on arrival.

---

### Example 6: Thread-vibe matching in a fast reply chain

Root post (82k followers): *"Shipping fast is a skill. Most teams treat it like a personality trait."*

Reply chain vibe: short, punchy, lowercase, no periods, 1–2 lines each.

**Bad reply (ignores vibe — reads robotic):**
> This is an excellent observation. Shipping velocity is indeed a learnable skill that can be cultivated through deliberate practice and the right organizational structures.

**Good reply (matches chain vibe, medium imperfection):**
> yeah and its almost always a process problem not a people problem
>
> slow teams usually have 3 approval layers where 1 would do

What works: lowercase opener, missing apostrophe in `its`, matches the 2-line chain pattern, adds a specific counter-point.

---

### Example 7: Reply with calibrated imperfection (technical thread)

Root post: *"Hot take: most RAG pipelines fail because of chunking strategy, not retrieval."*

Reply chain vibe: technical, measured, 3–5 lines, mostly proper punctuation.

**Bad reply (over-imperfected — reads careless in a technical thread):**
> yeah chunking is def the thing, we tried like 5 diff approaches and its always the same lol

**Good reply (low imperfection, matches technical register):**
> Chunking + overlap settings, in our case. Switched from fixed 512-token chunks to semantic sentence boundaries and recall jumped ~30%.
>
> The retrieval model was fine the whole time.

What works: one small imperfection (no period after "boundaries" before the line break), specific number, technical precision maintained, matches the thread's measured tone.

---

## References

- AgentSkills spec: https://agentskills.io/specification
- Companion skill: `content-voice` (human voice rules — always co-activate)
- Companion skill: `content-humanize` (AI-detection diagnostic if rewriting AI-generated drafts)
- X algorithm open source: https://github.com/twitter/the-algorithm
