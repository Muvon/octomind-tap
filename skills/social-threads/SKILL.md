---
name: social-threads
title: "Threads (Meta) Publishing Playbook"
description: "Ground-truth 2026 playbook for writing posts and replies on Meta Threads. Covers the 2026 algorithm (For You feed surfaces accounts you don't follow, early engagement critical, keyword search works, no hashtag ranking), the tone split from X (conversational, lighter, less contrarian, relatable), the 500-character limit, reply-chain culture, and how to avoid X-ported posts that flop. Activate when drafting for Meta Threads specifically — not for X/Twitter threads."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Meta Threads (threads.net)."
domains: content
rules:
  - match(\bmeta\s+threads\b)
  - match(\bthreads\s+(app|post|meta)\b)
  - match(\bpost\s+(on|to|for)\s+threads\b)
  - match(\bthreads\.net\b)
  - match(@threads\b)
---

## Overview

Threads is Meta's text-first social app — launched July 2023, reached 400M MAU by 2026, and by now a distinct platform with its own tone, algorithm, and culture. It looks like Twitter but does not behave like Twitter. Posts that crush on X often flop on Threads, and vice versa.

This skill is not about X/Twitter threads (multi-post chains on X) — that's `social-x`. This is about the Meta Threads app specifically. If ambiguous, assume the user means X threads unless they explicitly say "Threads app," "Meta Threads," "threads.net," or reference the platform mechanics.

Pair with `content-voice` for human voice.

## Instructions

### The 2026 Algorithm — What's Different From X

Threads' For You feed aggressively surfaces posts from accounts you don't follow. This is the single most important difference from X:

- Follower count matters less. A 100-follower account can reach millions on a single post. The ceiling is genuinely open.
- The For You feed is the main feed for most users — the Following feed is opt-in and under-used.
- Early engagement decides distribution — and speed beats volume. 15 replies in 30 minutes trigger wider distribution; the same 15 spread over an afternoon don't. Measured guides put the cutoff around 30+ reactions in the first hour before reach gets capped.
- Recency is heavily weighted. Posts older than a day rarely get amplified, even high-performing ones. There's no "evergreen" on Threads.
- Keyword search works in 2026 (didn't in 2023–2024) — people now find posts by topic. You can be searched into, not just followed.
- One topic tag per post aids search discovery — Meta's own data shows tagged posts get more views. Pick the most specific tag that names your niche, not the broadest. It is NOT a distribution multiplier: never stack tags, and classic hashtags do nothing.
- Media lifts initial distribution. 2026 measurements: median engagement ~5.5% for native video, ~4.6% image, ~2.8% text-only, ~2.3% link posts (algorithmically the weakest type). Attach a screenshot or image when it adds information — decorative graphics underperform clean text. If the link isn't the point of the post, move it to a reply.
- Reply chains are native culture. Long reply threads stay in the feed; the algorithm rewards conversations that keep going.
- Cross-posting from Instagram gets a small boost but looks lazy and often flops on tone.
- Fediverse federation is live as of 2026 — your posts can be seen on Mastodon. It's rarely a distribution driver but removes your account from platform lock-in.

### Signal weights (approximate, 2026)

| Signal | Weight vs. a like |
|---|---|
| Reply | ~12–15× |
| Reply-to-your-reply (author loop) | very high; compounds |
| Repost (Threads' retweet) | ~8–10× |
| Quote post | ~10× |
| Like | 1× (baseline) |
| Follow after read | strong positive |
| External link click | modest; Threads is less link-hostile than X but still prefers on-platform |

Three measured refinements (2026):
- Reply weight is length-sensitive — a one-word "same" counts far less than an 8+ word reply. Write posts that provoke sentences, not emoji.
- Reshares from accounts with more reach than yours count more than raw reshare volume — one reshare by a big account beats fifty from tiny ones.
- Rule of thumb: a post with 200 replies and 80 likes travels further than one with 600 likes and 12 replies. Optimize for conversation, not applause.

### The Tone Split — Threads vs X

This is the single biggest mistake cross-posters make. Do not port X posts verbatim.

| Dimension | X (Twitter) | Threads |
|---|---|---|
| Register | Sharp, opinionated, contentious | Casual, conversational, relatable |
| Humor | Dry, sarcastic, often mean | Warm, silly, observational |
| Hot takes | Central currency | Polarizing takes underperform |
| Debate | Expected, rewarded | Tolerated, not sought |
| Personal stories | Welcome but compete with tech/news/politics | Welcome and often dominate |
| Self-promotion | Tolerated if earned | Disliked more than on X — softer sell required |
| Length | 71–100 chars or 240–259 chars | Natural conversation-length, often 80–250 chars |
| Emoji | Dead as formatting; OK as tone | More alive; emoji as tone-punctuation works |
| Political content | Central to the feed | Meta down-ranks; topic-based reach is real |

Threads' vibe in 2026 is often described as "early Twitter but friendlier" — less drama, more actual conversation, more willingness to reply to strangers.

### The Post Anatomy

Threads posts are short (500-char limit) and the front of the feed favors:

```
[HOOK / OBSERVATION]          ← 1–2 lines, often an observation or small take
[OPTIONAL CONTEXT OR TWIST]   ← 1–2 lines
[OPTIONAL SOFT CTA / QUESTION] ← invites reply; not required
```

The first sentence must stop the scroll on its own — readers decide in ~8–10 words. Openers from measured high performers: "We got 4,000 new followers in 48 hours. This is the one thing we changed." / "The thing nobody tells you about going viral is that the post you spent an hour writing usually doesn't." A stacked-lines format (each short line building on the previous, rhythm over full sentences) is a native Threads pattern for takes with a punchline.

Key differences from X:

- Questions actually work. On X, "What do you think?" reads as engagement bait. On Threads, a genuine question often outperforms a statement because the platform rewards replies.
- "Hot take:" prefix is mostly fine on Threads — the platform is less saturated with it. Not dead the way "unpopular opinion:" is dead on X.
- Emoji as tone-punctuation is alive — not emoji bullets, but a single emoji at the end of a line for tone reads normal. Don't overdo it.
- Shorter posts often win. A 80–150 char observation beats a 450 char argument more often than on X.
- No thread markers needed for reply chains — users naturally scroll replies.

### Post Types That Work on Threads

| Type | Why it works on Threads specifically |
|---|---|
| Observational micro-take | Matches the casual register; low-stakes agreement |
| Honest question | Platform rewards replies; earnest questions get answered |
| Relatable moment | Shared experience content performs above X baseline |
| "Small brain" confession | Self-deprecation lands better than on X |
| Soft hot take | Opinion without the edge; "I think X" works here |
| Scene-based story (2–3 lines) | More room for vibes than X's punch-line style |
| Reply chain starter | Post designed to spin into a conversation, not to close one |
| Counter-intuitive specific | Violates a reader assumption, then grounds it in one concrete detail — top reshare driver in 2026 measurements |
| Data point + sharp take | A number readers didn't know plus a one-line interpretation; reshared as "did you know" |

What flops on Threads:
- Aggressive contrarian posts that would win on X
- Tech-twitter style one-liners — too terse for Threads register
- "Build in public" revenue screenshots — occasionally land but often feel out of place
- Political dunks — Meta actively throttles
- Pure news commentary — Threads is not where news breaks or gets analyzed
- Cross-posted X threads with thread markers ("1/5", "🧵") — obvious and ignored

### Reply Culture (the core of the platform)

Threads is built around reply chains in a way X isn't. People actually read 20-reply conversations between strangers.

- Reply to strangers. It's normal and expected. Not the growth-hack it is on X — just culture.
- The fastest discovery path in 2026: an early, substantive reply on a high-reach account in your niche. It stays near the top of their thread for hours, and their audience is pre-filtered to your topic.
- Publish-to-reply ratio: reply to ~3 other posts for every post you publish. This mirrors how the platform actually converses and builds recognition before you need it.
- On your own posts: answer every reply within the first 30 minutes and ask follow-up questions — comment depth is a ranking factor, and the author-loop compounds.
- Reply length is flexible. 1-line quips work; 3-line substantive replies also work.
- Reply chains can go 50+ deep and still stay in people's feeds.
- Quote posts are rarer and often read as slightly aggressive — use sparingly.
- Author reply to your own post as a follow-up is welcome — treat it like thinking out loud, not thread continuation.
- Don't @-tag the OP in your reply — already threaded.
- Disagreement is fine but stays softer than X. "I see it differently because…" beats "That's wrong."

### What Kills Posts on Threads

- Cross-posted X posts with X-specific references ("the algo," "based on replies to my pinned")
- "Follow for more" CTAs — read as desperate on Threads
- Bookmark bait — "Save this thread" feels off-register
- Engagement bait — "Retweet this if you agree" translated to Threads = "Repost this if…" → dead
- Explicit political takes — throttled by Meta
- Rage-bait / karma-farming — suppressed faster than on X
- Long threads of 8+ posts — people scroll off; Threads is not built for that
- Heavy technical content — often better on X; on Threads it looks like you're posting to the wrong app
- Emoji bullets (💡✨🚀 as list markers)
- AI vocabulary (same list as `content-voice`)

### Timing

- Best windows: weekday evenings 7–10 PM local, and weekend mornings 9 AM–12 PM local.
- Threads skews younger and more international than X; peak activity is not the 9–5 business window.
- Post daily for growth. Threads rewards consistency more than volume; 1 post a day beats 5 posts once a week.
- 2026 measured guidance ranges from 3–7 posts/week (brands) up to a few per day (established accounts); new accounts benefit from higher frequency while the algorithm learns what the account is about. Consistency builds algorithmic confidence in your categorization.
- Don't burst-post — multiple posts within 30 minutes fragments engagement.

### Cross-Platform Strategy

If you're posting on both X and Threads:
- Rewrite, don't re-post. Same idea, different register.
- X first if the take is sharp/contrarian/technical, then soften for Threads.
- Threads first if the content is a question/relatable observation, then tighten for X.
- Don't cross-post threads/chains at all — they almost always flop on the receiving platform.
- Instagram → Threads cross-post is fine for photo/memory content; for text content rewrite.

### Thread-Vibe Matching

Threads is built around reply chains — people read 20+ reply conversations between strangers. Before replying, read the existing chain. The vibe is set fast and deviating from it reads as tone-deaf.

What to scan:
- Capitalization — is the chain all lowercase? Match it. A properly capitalized reply in an all-lowercase chain reads robotic.
- Length — 1-line quips or 2–3 line thoughts? Match the median.
- Warmth level — warm/silly/supportive vs. more analytical? Threads skews warm by default.
- Emoji usage — is the chain using tone-emoji? Match the density (0–1 per reply is normal; 3+ is too much).
- Humor register — is there a running joke or absurdist thread? You can lean into it or stay neutral; don't fight it.

Vibe calibration by post type:

| Post type | Reply vibe |
|---|---|
| Observational micro-take | Match the casual register; 1–2 lines, lowercase fine |
| Honest question | Earnest, direct answer or "same here" + your version |
| Relatable moment | Warm, personal, first-person |
| Soft hot take | Agree/extend or gentle pushback; no aggression |
| Silly/absurdist post | Match the absurdity or don't reply — forced serious replies kill the vibe |

### Human Imperfection Protocol

Threads is the most casual platform in this set. Imperfections aren't just anti-detection — they're part of fitting the register. The platform already rewards casual; imperfections are about matching the vibe, not just surviving AI detection.

Imperfection level by content type:

| Content type | Level | What that means |
|---|---|---|
| Original post | Low | 0–1 imperfection; posts are still considered, just casual |
| Reply in a casual/warm chain | Medium | 1–2 imperfections natural; lowercase, no punctuation fine |
| Reply in a silly/absurdist chain | Medium-high | Match the chaos; lowercase, run-ons, emoji mid-sentence all fine |
| Reply to a personal/vulnerable post | Low | Warmer and more careful; imperfections feel careless here |

Imperfection menu for Threads (pick 1–2 per reply, calibrate to chain):

- All lowercase — the most common Threads pattern; entire reply in lowercase reads native
- No closing punctuation — end without a period; extremely common on Threads
- Comma splice — `i tried this, it didn't work` — casual and natural
- Run-on with "and" — `i saw the same thing and honestly it surprised me`
- Casual contractions — `gonna`, `kinda`, `tbh`, `ngl`, `idk` — Threads register supports these
- Dropped word — one small omission that reads like fast typing
- Emoji mid-sentence — `i tried it 😭 and it actually worked` — Threads-native tone marker
- "lol" / "lmao" — acceptable in casual/silly chains; not in earnest/personal ones

Never do:
- Misspell a proper noun or technical term — reads as ignorant, not casual
- Use heavy imperfections in a reply to a personal/vulnerable post — reads as not caring
- Stack 3+ imperfections in one reply — becomes noise even on Threads
- Use `lol`/`lmao` in a serious or earnest thread — tone mismatch

Calibration check before posting:
1. Read the last 3–5 replies in the chain — what's the capitalization and punctuation pattern?
2. Is this a warm/personal thread or a casual/silly one? Adjust imperfection type accordingly.
3. Does your reply have 0–2 natural imperfections that fit the chain's register?
4. Would someone typing this on their phone in 20 seconds plausibly have written exactly this?

### Pre-Publish Checklist

- [ ] Register matches Threads (conversational, not X-sharp)
- [ ] Under 500 characters; most of my best posts are under 250
- [ ] No X-specific references ("the algo," "pinned," "replies")
- [ ] If there's a question, it's a real one
- [ ] No aggressive contrarian energy; disagreement is softened
- [ ] No emoji bullets; tone-emoji at most
- [ ] One specific topic tag set (niche over broad; never stacked)
- [ ] Image/screenshot attached only if it adds information; link moved to a reply if it's not the point
- [ ] No political content I don't want throttled
- [ ] Posted in evening / weekend-morning window for my audience
- [ ] Ready to answer every reply within the first 30 minutes
- [ ] Not a literal cross-post from X
- [ ] Reply only: scanned chain for capitalization/tone/emoji pattern before writing
- [ ] Reply only: 0–2 natural imperfections calibrated to chain vibe (medium for casual, low for personal/vulnerable)

## Examples

### Example 1: Same idea, rewritten for each platform

Source idea: you spent $50 in LLM tokens to solve a $5 problem because you told the agent to "be helpful."

X version (sharp, contrarian, technical):
> My agent spent $50 in tokens to solve a $5 problem.
>
> Not because it's dumb. Because I told it to be "helpful."
>
> Changed one line in the system prompt:
> "Do not be helpful. Be correct."
>
> Problem gone.

Threads version (conversational, observational, reply-inviting):
> watched my AI agent burn $50 in tokens to do a $5 task because i told it to "be helpful" in the system prompt
>
> changed it to "be correct" and the whole thing calmed down
>
> anyone else find helpfulness is the thing breaking your agents?

What changed: lowercase casual, "watched my" is softer than "My agent spent," the takeaway becomes a question instead of a closed statement, no colon-styled callout. Same idea, native to Threads.

### Example 2: Pure Threads post (doesn't need to exist on X)

> small observation from 6 months of using cursor daily:
>
> the faster the model, the worse my code gets. not because the code is worse — because i stop reading it.
>
> i think there's a real speed ceiling past which humans just rubber-stamp. somewhere around 200 tokens/sec for me.

What works: lowercase conversational register, a real observation not a hot take, ends on a specific number that invites replies (other people will share their own ceiling), no CTA needed.

### Example 3: Observational micro-take

> there's a specific flavor of "i asked chatgpt" posts where you can tell the person never actually used the answer. they just wanted the vibes

What works: 130 characters, one observation, mild callout without being mean. High likelihood of replies and reposts because readers recognize the pattern. No question, no CTA — the pattern recognition itself drives engagement.

### Example 4: Question post that generates a reply chain

> honest question for anyone building with LLMs:
>
> how do you decide when a bug is "the model is wrong" vs "your prompt is wrong"?
>
> i've been burning hours on the wrong side of that line

What works: earnest tone, names a specific common pain, admits own weakness ("burning hours"), ends with no canned CTA. This type of post routinely generates 30+ replies on Threads — the platform's native conversation mode.

### Example 5: What NOT to post on Threads

Ported from X (fails on Threads):
> 1/ Thread on why most AI agents fail 🧵
>
> After building 40+ agents in production I've noticed 5 failure modes nobody talks about:
>
> (continues with 5 numbered posts)

Why it fails on Threads: thread markers ("1/"), the 🧵 emoji, "40+ agents" credential flex, "nobody talks about" hot-take framing, the 5-numbered-points structure. All of this reads as X culture. On Threads the same idea would be one soft-take post inviting replies, not a broadcasted thread.

### Example 6: Thread-vibe matching (casual chain)

Post: "there's a specific flavor of 'i asked chatgpt' posts where you can tell the person never actually used the answer. they just wanted the vibes"

Reply chain vibe: all lowercase, no punctuation, 1–2 lines, slightly absurdist.

Bad reply (ignores vibe — reads robotic):
> This is an astute observation. Many users engage with AI outputs as a form of social signaling rather than as a practical tool, which creates a disconnect between stated and actual utility.

Good reply (matches chain vibe, medium imperfection):
> the vibes are the product at this point
>
> nobody's reading the output they're just screenshotting the prompt

What works: all lowercase, no periods, matches the 2-line casual pattern, extends the observation with a specific behavior (screenshotting the prompt) that readers will recognize.

### Example 7: Reply with calibrated imperfection (personal/vulnerable thread)

Post: "honest question for anyone building with LLMs: how do you decide when a bug is 'the model is wrong' vs 'your prompt is wrong'? i've been burning hours on the wrong side of that line"

Reply chain vibe: earnest, personal, lowercase but thoughtful, 2–3 lines.

Bad reply (over-imperfected for a personal/earnest thread):
> omg same lmao i literally have no idea half the time tbh its just vibes at this point lol

Good reply (low imperfection, matches earnest register):
> i usually blame the prompt first because its cheaper to fix
>
> but if i've rewritten it 3 times and it's still wrong, that's usually the model

What works: lowercase throughout (matches chain), missing apostrophe in `its` (one natural imperfection), earnest and specific answer, no over-casual slang that would feel dismissive of the person's real frustration.

## References

- AgentSkills spec: https://agentskills.io/specification
- Threads help center: https://help.instagram.com/threads
- "Measured" figures in this skill (engagement rates by format, velocity thresholds, signal refinements) are consolidated from 2026 third-party platform studies — Threads has no public ranking source, so treat them as directional, not exact. Re-validate periodically.
- Companion skill: `content-voice` — voice rules still apply
- Companion skill: `social-x` — different platform; don't confuse Threads (Meta) with threads-on-X
