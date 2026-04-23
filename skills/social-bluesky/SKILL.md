---
name: social-bluesky
title: "Bluesky Publishing Playbook"
description: "Ground-truth 2026 playbook for writing posts, replies, and threads on Bluesky. Covers the three feeds (Discover, Following, Custom), why custom feeds and starter packs are the dominant 2026 growth levers, the 300-grapheme limit, quote-post culture, self-reply threads, labelers and stackable moderation, and why X-ported posts flop. Activate when drafting for Bluesky — not for X/Twitter threads."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Bluesky (bsky.app / AT Protocol)."
domains: content
rules:
  - content(bluesky)
  - content(bsky)
  - match(\bbsky\.app\b)
  - match(\bat\s+protocol\b)
  - match(\bpost\s+(on|to|for)\s+bluesky\b)
  - match(\bstarter\s+pack\b)
---

# Bluesky Publishing Playbook

## Overview

Bluesky in 2026 is **not late-era Twitter with a blue logo**. It's a federated AT Protocol network where the user — not the platform — picks the algorithm. Discovery happens through **custom feeds** and **starter packs**, not a single opaque For You feed. The culture skews more technical, more skeptical of hype, and more willing to punish AI-slop and engagement-bait than X.

Port a post verbatim from X and it usually lands dead. The ranking surface, the humor, and the trust signals are different. This skill adapts tone and structure to how Bluesky actually distributes content.

## Platform Mechanics 2026

### The Three Feeds

| Feed | How it ranks | What that means for you |
|---|---|---|
| **Following** | Strictly chronological, only accounts you follow | Timing matters less than on X; a great post from 6 hours ago still shows |
| **Discover** | Algorithmic, Bluesky-run, based on engagement + graph proximity | The closest thing to an FYP, but it's one of many feeds, not THE feed |
| **Custom feeds** | User-created, curated by hashtag, keyword, account list, or custom logic | The real growth lever — getting onto a popular niche feed beats going "viral" on Discover |

Users pick which feeds appear in their app. Popular niche feeds (e.g. "Science," "Dev," "Art," "Bookstodon-on-Bluesky") have thousands of subscribers and curators who add accounts they like. **Optimize to be picked up by curators**, not to trick an algorithm.

### Starter Packs (the #1 discovery mechanism in 2026)

Starter packs are shareable lists of 7–150 accounts. They're how new users fill their Following feed on day one. Getting onto a well-shared starter pack in your niche is worth more than a week of viral posts.

- Be findable. A clear bio + consistent topic = curator adds you.
- Create your own pack for your niche. Gives back to the community and brands you as a curator.
- Appearing on packs multiplies: every pack you're on that someone new joins → follows → Following feed.

### Hard Limits

- **300 graphemes per post** (not bytes, not codepoints — a single emoji or CJK character is one). URLs count as the characters they display, not the target.
- **4 images per post** (or 1 video, 1 GIF, 1 link card).
- **Alt text up to 2000 characters** per image. Use it — accessibility is a cultural norm here, not a nicety.
- **Threads = self-replies.** There is no native "thread" object; you chain by replying to your own post.
- **Quote posts exist and are the preferred amplification move** — see below.

### Labelers and Moderation

Moderation is stackable. Users subscribe to community-run **labelers** that tag content (NSFW, spoilers, AI-generated, specific topics). This means:
- AI-generated images without a self-label may get community-labeled and hidden.
- Spoilers without CW-style framing get flagged by book/TV labelers and collapsed.
- Bluesky itself filters much less than X; user-side labeling does the work.

Implication: **self-label anything a labeler would catch.** Add "AI image," "book 3 spoiler," "US politics" in-line or at the top of the post. Pre-empting a label keeps the post fully visible.

## Tone: What Bluesky Actually Rewards

Bluesky's 2024–2025 migration was driven by people **leaving** X, not joining a new X. The resulting culture punishes moves that work on X:

- **Hype and absolutes flop.** "This is insane." "Everything changed today." Gets ignored or mocked.
- **Self-promo without substance is visible.** The platform is small enough that the same "grow your audience" bro posts get screenshot-dunked.
- **Reply-guy engagement farming is obvious.** 1-line "100%" replies under big accounts die. Substance or silence.
- **Politeness is the default.** Sharp disagreement is fine; contempt reads as imported X behavior.
- **AI slop gets labeled and hidden.** Anything that reads as ChatGPT-default prose (em-dashes everywhere, "delve," "multifaceted," "landscape") gets caught.
- **Specific > clever.** A concrete observation beats a witty one-liner. The audience is more "technical conference" than "comedy club."

Rule of thumb: **if the post would work on Hacker News, it'll work on Bluesky. If it would work on 2023-era X, it probably won't.**

## Post Shapes That Land

### 1. The Specific Observation

A single noticed detail, written plainly. No thread, no hook.

```
The new Bluesky firehose changed its JSON envelope yesterday
and three of my feed generators silently stopped emitting.
Quiet break — no deprecation notice, no changelog entry.
Worth checking if yours went dark.
```

Why it works: specific, useful, signals technical attention, invites replies from people who also noticed.

### 2. The Link + Why It Matters

Link previews render well on Bluesky and there's no documented suppression. But the link alone is noise — say why it's worth the click.

```
New paper on ActivityPub bridge latency under federation pressure.
Headline: median round-trip tripled past 100k active users per instance.
Methodology section is the interesting part — they measure
from the recipient's inbox, not the sender's outbox.

[link card]
```

### 3. The Self-Reply Thread

Threading on Bluesky is a chain of self-replies. Each post must stand alone (they often get surfaced individually by custom feeds).

```
1/ Re-reading the AT Protocol spec and something clicked
about why it scales differently than ActivityPub.

2/ ActivityPub is push-based: your server pushes each post
to every follower's server. Federation cost grows with followers.

3/ AT Protocol is pull-based: followers read your repo.
Your cost is constant; aggregation cost scales with reach.

4/ The implication: a Bluesky "mega account" costs the platform
roughly what a small one does. Different ceiling.
```

No hook post, no "🧵👇," no "a thread:". The chain speaks for itself.

### 4. The Question to the Feed

The Discover feed rewards replies. A sharp, specific question draws them.

```
For people who've run feed generators:
what's your actual p99 for posts-to-inclusion?
Mine hovers around 4 minutes and I can't tell
if that's slow or normal.
```

## Replies

Reply culture is calmer than X. You don't need to ship a dunk in the first 15 minutes to be seen; the Following feed is chronological, so your reply shows for your followers regardless of timing. Specific & substantive still wins.

- Open on content, no courtesy preamble.
- 2–4 sentences is the right range.
- Quote posts > replies for amplification — see below.
- Don't @-mention the author in a direct reply (it's already threaded).
- If you disagree, say what specifically. Contempt doesn't transfer well.

## Quote Posts (the preferred amplification move)

On Bluesky, **quote posts are the main way ideas spread**. Plain reposts exist but carry less signal — a quote post says "I had something to add." Curators watch quote posts to find new voices.

Good quote post:
- Adds one specific thing — a counter-example, an extension, a number, a historical parallel.
- Stands alone for someone who can't see the quoted post yet.
- Doesn't say "this" or "exactly this." That's a plain repost; do that instead.

```
[Quoting: "New AT Protocol version drops the proxy header and
breaks all third-party feed generators that relied on it."]

Small but important: this also breaks the CORS shim that most
web-based feed editors used. If your editor stops loading this
week, that's why. Fix is to move proxy validation server-side.
```

## Custom Feed Strategy

Want to be discovered? Work backwards from feeds.

1. **Find the 3–5 custom feeds** that cover your niche. Search in-app for your topic; look at which feeds appear.
2. **Read each feed's "about" text.** Most feeds publish their criteria: specific hashtags, keywords, or account lists.
3. **Match the criteria naturally.** If the "Dev" feed keys on `#dev` or `#programming`, use them when relevant. Don't stuff.
4. **Talk to curators.** Curators of human-curated feeds accept suggestions. A polite "I think my posts on X fit your feed — worth a look?" works far better than on X.
5. **Run your own feed.** The best accounts in a niche often curate a feed for it. It's free distribution and credential.

## Hashtag Use

Bluesky has hashtags but they matter less than on Mastodon. They're useful for:
- Being picked up by hashtag-based custom feeds.
- Marking a post as on-topic for a known event or campaign.

Rules:
- **1–2 tags max**, placed naturally or at the end.
- Lowercase is the convention (`#dev`, not `#Dev`).
- Don't tag every word. Multi-tag posts read as X-imported.

## Cross-Posting from X

Most cross-posts fail because:
- Hooks that work on X ("This one trick," "Read till the end") read as spam on Bluesky.
- The 280→300 char difference doesn't save a post that was built for a different audience.
- Quote-tweet energy doesn't map to quote-post energy.

If you must cross-post, rewrite these:
- Strip "🧵" / "a thread:" / "thread below" framing.
- Cut emoji count in half.
- Remove "🚀 🔥 💯" hype emoji entirely.
- Rewrite hook posts as standalone posts or delete them.
- Convert CTAs ("RT if you agree") to questions.

Better rule: **post to Bluesky first** for at least a week. Get a feel for what lands. Then cross-post the rare post that works on both.

## Profile & Bio

Bluesky profiles are search-indexed and curators read them.

- **Handle matches purpose.** A `@yourname.bsky.social` is fine; a custom domain (`yourname.com`) is a mild trust signal.
- **Bio says what you post about**, not who you are. "I write about Rust async internals and distributed systems" beats "Engineer. Coffee. Dad." Curators match bios to feeds.
- **Pinned post = your best recent work.** Starter-pack inclusions increase when the pinned post is strong.

## Anti-Patterns (will hurt reach)

- **"Follow for more" / "Like and repost"** — Bluesky users find this especially grating.
- **Posting the same thread daily.** Low signal; curators drop you.
- **Ratio-bait politics without local context.** The platform's political center is not X's; takes calibrated to X get ignored, not dunked on.
- **Unmarked AI content.** Even when not flagged, it tanks trust. Always self-label.
- **Huge link-card posts with no text.** Looks like a feed bot. Add one sentence of framing.
- **Reply-guy behavior on mega accounts.** The platform is small enough that regulars recognize it.

## Examples

### Example 1 — Launching a side project

❌ X-imported:
```
🚀 Just launched Feedly-Killer! 🔥
The fastest feed reader for Bluesky.
Check it out 👇
[link]
RT if you're tired of slow feeds!
```

✅ Bluesky-native:
```
Shipped Feedly-Killer, a keyboard-first feed reader for Bluesky.
Scratches an itch I had: jumping between 14 custom feeds
without losing my place.

Still rough around profile viewing. Feedback on that part especially welcome.

[link card]
```

### Example 2 — Reacting to platform news

❌ Hyped:
```
THIS CHANGES EVERYTHING. Bluesky just announced video!!
The Twitter killer is officially here. 🎬🚀
```

✅ Grounded:
```
Video in the Bluesky announcement is interesting
because it lands on the AT Protocol, not a separate silo.
Which means third-party clients get it too from day one.
That's a different story than "video on X" ever was.
```

### Example 3 — Quote post adding a specific detail

```
[Quoting: "Custom feed generators just got a 10x cost reduction
in the new SDK."]

The 10x is real but worth reading the release notes carefully:
it's on indexing, not serving. If your feed is serve-heavy
(lots of subscribers, few posts) the numbers you'll see
are more like 1.5–2x. Still welcome, just not 10x for everyone.
```

### Example 4 — A thread done right

```
1/ Ran the AT Protocol firehose through a week of our traffic.
Three things surprised me, posting in case they save someone time.

2/ The `commit` records carry a lot more metadata in 2026 than
the 2024 docs suggest. Budget 2x the bandwidth you'd estimate
from the tutorial.

3/ Backfill is expensive. Starting from genesis costs ~6 hours
of CPU on a mid-sized box. Most apps don't need it; start
from "now" and add history selectively.

4/ Labelers fire on both new posts and edits. If your pipeline
dedups on post ID, you'll miss labels added after the fact.
Dedup on (post ID, rev) instead.
```

## Composition

Use with:
- **content-voice** — carry your brand voice across a longer run.
- **content-humanize** — strip AI tells (em-dashes, "delve," hedge stacks). Bluesky catches these faster than X.
- **social-x** — if cross-posting, run both skills and let the differences drive the rewrite.

## References

- AT Protocol spec: https://atproto.com
- Bluesky API docs: https://docs.bsky.app
- Fedi.Tips Bluesky guide: https://fedi.tips/bluesky/
