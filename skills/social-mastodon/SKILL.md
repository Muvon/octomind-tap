---
name: social-mastodon
title: "Mastodon Publishing Playbook"
description: "Ground-truth 2026 playbook for writing posts, replies, and threads on Mastodon and the wider Fediverse. Covers the strictly chronological timelines (no algorithm), hashtags as the sole discovery mechanism, the content-warning (CW) conventions, alt-text as a cultural norm, boost vs favorite semantics, instance selection, the local vs federated timeline, and why X/Bluesky tactics don't transfer. Activate when drafting for Mastodon or Fediverse-compatible servers (Pleroma, Akkoma, GoToSocial, Firefish, etc.)."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Mastodon and ActivityPub-compatible Fediverse servers."
domains: content
rules:
  - content(mastodon)
  - content(fediverse)
  - content(activitypub)
  - content(toot)
  - match(\bpost\s+(on|to|for)\s+mastodon\b)
  - match(\bthe\s+fediverse\b)
---

# Mastodon Publishing Playbook

## Overview

Mastodon (and the wider Fediverse) runs on **ActivityPub**, not a single company. There is **no algorithm**. Timelines are strictly chronological. Posts don't get "boosted" by the platform — they get boosted by humans, or they don't move at all. Discovery is powered by **hashtags, boosts, and instance-local curation** — in that order.

This means the writing game is completely different from X, Threads, or Bluesky. You can't optimize for early engagement velocity because nothing amplifies early engagement. You can't trick a ranker. The only levers are: **be findable (hashtags), be worth boosting (substance), and be followed by people whose followers read chronologically.**

## Platform Mechanics 2026

### The Three Timelines

| Timeline | Contents | Your reach here |
|---|---|---|
| **Home** | Posts + boosts from accounts you follow, plus posts tagged with hashtags you follow | Where your followers see you. Chronological. |
| **Local** | Every public post from every account on your instance | Your instance-mates see you here. Picking your instance = picking your local audience. |
| **Federated** | Every public post from every account your instance "knows about" (anyone followed by anyone on your instance) | Firehose. Almost no one reads it end-to-end; some power users sample it. |

**No algorithmic feed.** The closest thing is the Explore / Trends tab, which surfaces hashtags and posts trending across the local instance based on boost counts. Different per instance.

### Hashtags: the Actual Discovery Mechanism

This is the single most important thing to internalize. On Mastodon:

- **Users can follow hashtags.** Someone who follows `#rust` sees every post tagged `#rust` in their Home timeline, forever.
- **Searching is hashtag-first.** Full-text search is off by default per-user; opt-in only. Hashtag search is universal.
- **Untagged posts are roughly invisible to non-followers.** A brilliant post with zero tags reaches only your current followers.

Consequence: **tag every post that touches a followable topic.** Not 10 tags — 1 to 3 real ones. Use the tags people actually follow, not made-up ones.

Conventions:
- **CamelCase your multi-word tags** (`#RustLang`, not `#rustlang` or `#rust_lang`). Screen readers read CamelCase correctly; lowercase runs letters together.
- **Lowercase single-word tags is fine** (`#rust`, `#linux`).
- **Tags go at the end** of the post, or woven into the last sentence if natural.
- **Avoid gratuitous tags.** `#life #thoughts #musings` gets you blocked by tag-hygiene filters on some instances.

### Content Warnings (CW)

A CW collapses the post behind a short label. Users click to expand.

**What a CW is for** (community consensus 2026):
- Spoilers (movie, book, game)
- Graphic content (violence, gore, medical imagery)
- NSFW
- Instance-specific conventions (politics, food, alcohol, US/UK news — varies by instance culture)
- Long posts (some instances ask for CWs on >500-char posts as a courtesy)

**What a CW is NOT for** (controversial, will generate pushback):
- Hiding any mildly opinionated take
- Marketing posts
- Generic "long thread" unless your instance culture asks for it

**Format of a CW label**: short, specific, descriptive. The label is what people use to decide whether to open the post.

✅ `book 3 spoiler`, `us politics`, `loud image`, `food (meat)`, `medical`
❌ `sensitive`, `opinion`, `CW`, `read at own risk`

**Instance culture varies.** Mastodon.social is CW-light. Art-focused and marginalized-community instances are CW-heavy. Read the instance's local timeline for 15 minutes before assuming defaults.

### Alt Text: Mandatory Culture

The Fediverse has a **strong, widely-enforced** norm: every image gets alt text. Not a nice-to-have. Some instances block posts without alt text by default. Accounts that habitually omit it get blocked and muted — a real reach penalty.

- **Write for a screen reader.** Describe what's in the image, not what it means.
- **Keep it functional**, 1–3 sentences usually enough.
- **Charts and code screenshots** need the actual content: "Bar chart showing X axis = months, Y axis = requests/sec, peaks at 14k in June."
- **Memes**: describe the image AND transcribe the text.

### Boost vs Favorite

These are not the same thing, and confusing them reads as new-arrival behavior.

- **Favorite (⭐)** = private acknowledgment. Does not amplify. Does not notify your followers. Think: "I saw this and appreciated it." Largely for the author.
- **Boost (🔁)** = amplification. Equivalent to a retweet. Puts the post into every one of your followers' Home timelines. **This is the only way posts travel.**

If something is good, **boost it, don't just fav it.** Favs without boosts = the Fediverse equivalent of silent applause; the post doesn't move.

Consequence for writers: **every post is a boost-or-die.** Your reach past your current followers depends entirely on boosts. Write things people actually want to boost.

### Quote Posts: Historically Absent, Now Optional

Mastodon long opposed quote posts on the grounds that they enable pile-ons. In 2025–2026 an opt-in quote-post feature landed, but the cultural default is cautious:
- **Many users have them disabled on their own posts.**
- **Quote-to-dunk is frowned on more than on X/Bluesky.**
- **Quote-to-add** is welcome if substantive.

Default: if you're unsure, reply with the link rather than quote. "Responding to @user@instance.tld's point about X…"

### Links

There is **no algorithmic link penalty** on Mastodon — a refreshing difference. Post links freely. Link cards render if the target site has Open Graph tags. Still:
- Say why the link matters in 1–2 sentences before dropping it.
- Prefer original sources over aggregators — the Fediverse is archive-conscious.
- Don't paywall-spam. `archive.ph` links or non-paywalled versions are appreciated.

### Character Limit

- **Default: 500 characters.** Most instances.
- **Variable: 1500 to 5000.** Some instances (fosstodon.org, mstdn.social config varies). Know your instance.
- **Cross-instance posts**: a 2000-char post from a custom-limit instance renders fully on a 500-char instance. It does not truncate.

But the cultural expectation is calibrated to 500. Longer posts read as heavy. If a post exceeds 500, consider:
- Splitting into a thread of self-replies (preferred, each post stands alone).
- Putting it on a blog and linking.
- Adding a CW (`long post` or topic-specific) as courtesy.

### Threads

No native thread object. Thread by replying to your own post. Each post should stand alone (people read self-replies out of context from hashtag timelines).

Mark threading subtly if useful:
- `(1/4)` at the start of each post.
- Or let the reply chain speak for itself (common in smaller threads).

Don't write a "hook post" that tells people to read the thread. Mastodon readers find it spammy. Lead with substance.

## Instance Choice: A Writing Decision

Your instance is part of your voice. It affects:
- **Who sees you on the local timeline** — your first-ring audience.
- **Which other instances federate heavily** with yours.
- **Perceived alignment.** Being on `queer.af` or `infosec.exchange` or `mstdn.jp` says something before you post.
- **CW/content culture** norms.
- **Character limit** and any custom features.

Rule of thumb:
- **General**: `mastodon.social`, `mastodon.online`, `mstdn.social`. Largest, broadest.
- **Technical**: `fosstodon.org`, `hachyderm.io`, `infosec.exchange`, `techhub.social`.
- **Creative**: `mastodon.art`, `writing.exchange`.
- **Journalistic**: `journa.host`, `newsie.social`.

You can move instances later via account migration (followers + follows carry; posts don't). But the first impression sticks.

## Tone: What Mastodon Actually Rewards

The Fediverse culture is older than the 2022 Twitter exodus would suggest — lots of long-time FOSS, accessibility, and marginalized-community users. What they reward:

- **Craftsmanship.** A well-written observation with good alt text and a thoughtful CW reads as respectful.
- **Slowness.** No one expects hot takes within 15 minutes of news. A considered post 24 hours later is fine.
- **Accessibility.** Alt text, CamelCase tags, CWs where warranted. These are ethics-adjacent; getting them right is a trust signal.
- **FOSS / indie / privacy sensibility.** Drops of Twitter/Meta/TikTok-optimized language (influencer-speak) read as alien.
- **Kindness without saccharine.** Sharp disagreement fine; contempt or dunking imports poorly.

What doesn't work:
- Hooks, hustle-speak, growth-hacking framing. Instant mutes.
- "RT for reach" / "boost appreciated." Asking for boosts is a mild faux pas on most instances.
- AI-generated prose without a CW. Will get instance-labeled and defederated in repeat cases.
- Aggressive politics without local context. Instances have varying politics; the same post reads differently on different instances.

## Post Shapes That Land

### 1. The Tagged Substantive Observation

```
Discovered today that Gtk4 on Wayland exposes a new
compositor-side protocol for fractional scaling that avoids
the double-rounding bug we've been chasing since 2023.
It lands in glib 2.84 behind a flag.

One less reason to hate HiDPI on Linux.

#Linux #Gtk #Wayland
```

Works because: specific, useful to followers of those tags, boost-worthy for anyone in the niche.

### 2. The CW'd Long Post

```
cw: long post, photography

A whole write-up of how I'm reorganizing my lens kit around
a single 35mm prime for the year. Includes the thinking,
the gear I'm selling, and the workflow changes.

[... 800 chars of content ...]

#Photography
```

The CW is courtesy; the content earns the unfold.

### 3. The Reply Into a Hashtag

```
@friend@instance.tld worth noting that the Raku port
of this library is also interesting — it handles the same
memory layout but with slightly different guarantees
around cyclic references.

#Raku #Rust
```

Replying with a hashtag turns a private-feeling reply into a findable public contribution.

### 4. The Self-Reply Thread

```
1/ Been reading through the ActivityPub spec again
after three years and the ambiguities around Like
delivery finally make sense.

#ActivityPub

(reply)
2/ The spec never mandates that a Like MUST be delivered
to the original author's inbox. Most implementations do it,
but Pleroma historically didn't in one configuration,
which is why Like counts diverge across instances.

(reply)
3/ The fix isn't in the spec — it's in per-implementation
reconciliation protocols. Which explains why boost counts
are more reliable than fav counts across federation.
```

Each post stands alone, each is tagged, chronological timeline works with it.

## Replies

- **Always address the reply recipient with full handle on first reply** (`@user@instance.tld`) if replying out of a notification. Inside a thread, native threading handles it.
- **Unlisted visibility** (⇅ in composer) is a soft reply — doesn't hit local/federated timelines but still reaches the recipient and your followers' homes. Use for side-conversation replies you don't want to clutter local.
- **Substance, not reaction.** "100%" / "this" replies are especially lifeless here because there's no algorithmic reward for volume of interaction.

## Anti-Patterns (will cost you)

- **Posting without alt text repeatedly.** Auto-block lists exist for this.
- **Un-CW'd politics, food, or instance-sensitive topics.** Varies; check instance culture.
- **X-ported hype language** ("Game changer," "🚀🔥," "THIS is the future"). Reads as colonizer behavior to long-time users.
- **Cross-posting bot** that dumps every X post verbatim. Common instance rule violation; bot accounts get suspended.
- **Asking for boosts.** Soft taboo.
- **Screenshot-dunking.** The Fediverse remembers. Callout culture doesn't work the way it does on X — it rebounds.
- **Gratuitous tag stacking.** `#life #mood #thoughts #random` is a tell.

---

## Thread-Vibe Matching (Replies)

Mastodon reply culture is slower and more deliberate than X or Threads. Before replying, read the existing reply chain and the local timeline context. The vibe is set by the instance culture as much as by the individual thread.

**What to scan:**
- **Instance culture** — a reply on `infosec.exchange` reads differently than one on `mastodon.art`. Check the local timeline if you're new to an instance.
- **Length** — are replies 1–2 sentences or 3–4? Match the median.
- **Formality** — Mastodon skews more formal than Threads; full sentences and proper punctuation are common.
- **CW conventions** — if the thread has a CW, your reply should too (same or related CW label).
- **Hashtag practice** — if the thread is using hashtags in replies, match the pattern.

**Vibe calibration by post type:**

| Post type | Reply vibe |
|---|---|
| Technical observation | Match the depth; add a specific detail or counter-case |
| FOSS / project announcement | Substantive question or specific feedback; no hype |
| Personal / creative post | Warmer, shorter, first-person |
| CW'd sensitive topic | Match the care level; keep it measured |
| Accessibility-focused post | Especially careful; this community notices and values care |

---

## Human Imperfection Protocol

Mastodon values craftsmanship. The culture rewards care — in writing, in alt text, in CW labels. Imperfections should be about **informality of phrasing**, not typos. A typo in alt text is worse than a typo in prose here; accessibility is an ethical norm, not a nicety.

**Imperfection level by content type:**

| Content type | Level | What that means |
|---|---|---|
| Original post | Very low | 0–1 subtle imperfection; posts are considered artifacts |
| Alt text | Zero | Alt text is an accessibility artifact — zero imperfections |
| CW label | Zero | CW labels are functional — zero imperfections |
| Reply in a technical thread | Very low | 0–1 structural imperfection; precision still matters |
| Reply in a casual/personal thread | Low | 1 subtle imperfection; informal phrasing fine |

**Imperfection menu for Mastodon (pick 0–1 per reply, structural only):**

- **Informal opener** — `Been thinking about this since the glib 2.84 release.` instead of `I have been thinking about this.`
- **Casual aside in parentheses** — `(worth checking if yours went dark)` — reads as thinking-while-typing
- **Dropped subject** — `Tried the same approach, hit the same wall.` — common in technical writing
- **"though" / "honestly" / "actually"** — casual qualifiers that read as human hedging
- **No closing period** — end a reply without a period — common in casual Mastodon replies
- **Sentence fragment as emphasis** — `Not a bug. A feature of the spec.` — deliberate, reads as considered

**Never do on Mastodon:**
- Typos in technical terms, library names, or proper nouns — credibility damage
- Typos or errors in alt text — this is an accessibility failure, not just a style issue
- Errors in CW labels — these are functional; wrong labels break trust
- `lol`, `lmao`, `ngl` — too casual for most Mastodon threads
- Stack 2+ imperfections in one post — reads as careless in a culture that values care
- Hype language or emoji stacks even with imperfections — the register is wrong regardless

**Calibration check before posting:**
1. Is this a post, alt text, or CW label? Alt text and CW labels = zero imperfections.
2. Read the instance's local timeline — what's the general formality level?
3. Does your reply have 0–1 structural imperfections (informal phrasing, not typos)?
4. Would a thoughtful FOSS-community member typing this at their desk plausibly have written exactly this?

---

## Pre-Publish Checklist

- [ ] Alt text on every image — descriptive, functional, screen-reader-ready
- [ ] CW applied if the content warrants it (spoilers, sensitive topics, long post)
- [ ] CamelCase multi-word hashtags (`#RustLang`, not `#rustlang`)
- [ ] 1–3 relevant hashtags at the end (or woven in naturally)
- [ ] No X-ported hype language, no emoji stacks, no "boost appreciated"
- [ ] Links are to original sources, not aggregators or tracking URLs
- [ ] Under 500 characters (or CW'd if longer, or split into self-reply thread)
- [ ] Tone matches instance culture (check local timeline if unsure)
- [ ] For threads: each self-reply stands alone; tagged individually
- [ ] **Reply only:** scanned existing replies for length, formality, and CW conventions
- [ ] **Reply only:** 0–1 structural imperfection (informal phrasing, not typos); alt text and CW labels always zero

## Examples

### Example 1 — Announcing a blog post

❌ X-ported:
```
🔥 New blog post dropped! 🚀
Why ActivityPub will win the open social war.
Go read it now 👇

[link]

RT and comment if you agree!
```

✅ Fediverse-native:
```
Wrote a long post on where I think ActivityPub has the
structural advantage over AT Protocol long-term. Main
argument: the push model concentrates cost where growth
already exists, which makes moderation resource-scale
with the problem. Happy to hear pushback.

[link]

#ActivityPub #Fediverse
```

### Example 2 — Reacting to news

❌ Engagement-bait:
```
BREAKING: [platform] just announced [thing]. THIS changes everything
for the open web. Thoughts? 🤔
```

✅ Grounded:
```
The [platform] announcement is interesting mostly for what
it doesn't say. No mention of defederation policy, no mention
of which instances they're launching with. A launch without
those details means the interesting choices haven't been made yet.
Worth watching in a month.

#Fediverse
```

### Example 3 — A post with an image

```
Finally got the old ThinkPad running NetBSD current
with a working Wayland session. Screen's a bit yellowed
after 15 years but the keyboard still has the best travel
I've ever typed on.

[Image attached]
Alt text: Photo of a ThinkPad X61 laptop, open, showing
a NetBSD desktop with a tiling window manager. Three
terminal windows visible, running htop, vim, and tmux.
The screen tint is slightly yellow with age.

#NetBSD #ThinkPad #Retrocomputing
```

### Example 4 — A CW done right

```
cw: us politics, long

Some thoughts on the new court ruling and what it actually
changes at the federal level, which is less than the headlines
suggest...

[... content ...]

#USPolitics
```

The CW is honest about the content and length. Users who want it, expand. Users who are tired of US politics today, scroll past.

### Example 5 — Thread-vibe matching (technical thread)

Post: *"Discovered today that Gtk4 on Wayland exposes a new compositor-side protocol for fractional scaling that avoids the double-rounding bug we've been chasing since 2023."*

Reply chain vibe: technical, 2–4 sentences, proper punctuation, specific version numbers.

**Bad reply (ignores vibe — too casual):**
> omg finally lol, that bug has been driving me crazy for ages tbh

**Good reply (matches technical register, very low imperfection):**
> Been hitting this on a 2x HiDPI setup with a 1.5x secondary monitor. The double-rounding showed up as 1px misalignment in GTK dialogs.
>
> Good to know it's in 2.84 — will test against the flag this week.

What works: informal opener (`Been hitting`) is the only structural imperfection, specific hardware setup, concrete symptom, no typos, no casual slang, matches the technical depth of the thread.

---

### Example 6 — Reply with calibrated imperfection (personal/creative thread)

Post: *"Finally got the old ThinkPad running NetBSD current with a working Wayland session."*

Reply chain vibe: warm, personal, 1–3 sentences, casual but not sloppy.

**Bad reply (over-imperfected — reads careless in a warm personal thread):**
> omg thats so cool lol i love old thinkpads tbh, the keyboards are amazing ngl

**Good reply (low imperfection, matches warm-but-careful register):**
> The X61 keyboard is genuinely one of the best ever made. Still have mine from 2009 — the travel is something modern laptops just don't do.

What works: no imperfections here because the thread is warm but careful (Mastodon culture values craftsmanship), specific model name, personal connection, no hype language, reads as a thoughtful human response.

---

## Composition

- **content-voice** — carry voice across long-form posts and threads. Mastodon rewards consistency.
- **content-humanize** — strip AI tells. The Fediverse is faster to label and suspend AI-slop accounts than other platforms.
- **social-bluesky** — if you post to both, run both skills; the rewrites are meaningful, not cosmetic.

## References

- Mastodon user docs: https://docs.joinmastodon.org/user/
- Fedi.Tips (unofficial, excellent etiquette guide): https://fedi.tips
- ActivityPub spec: https://www.w3.org/TR/activitypub/
