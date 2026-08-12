---
name: social-devto
title: "DEV Community (dev.to) Publishing Playbook"
description: "Ground-truth 2026 playbook for publishing articles and comments on dev.to (DEV Community). Covers the tag-follow feed mechanics, the reaction system (hearts, unicorns, bookmarks), measured title patterns from the live top surface, discussion-post culture (the platform's strongest format), canonical-URL cross-posting, series, cover images, and why dev.to rewards community voice where Hacker News punishes it. Activate when drafting anything destined for dev.to."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to DEV Community (dev.to and Forem-based communities)."
domains: content
rules:
  - match(\bdev\.to\b)
  - match(\bDEV\s+Community\b)
  - match(\bforem\b)
  - match(\bpost\s+(on|to|for)\s+dev\.to\b)
  - match(\bdevto\b)
---

## Overview

dev.to (DEV Community) is a blogging platform for developers built on Forem — but treating it as "a blog host" misses what actually performs. It is a community first: discussion posts, career reckonings, and honest journey pieces outperform polished tutorials on the top surface. The register sits between Reddit's casualness and a personal blog's considered voice.

The inverse of Hacker News in three ways: emoji in titles are accepted, listicles work, and first-person community talk is the winning register — the exact moves that get you flagged on HN. Don't port content between them unchanged.

Pair with `content-voice` for human voice. dev.to has no aggressive AI-automod layer like Reddit, but the community reads a lot of AI-generated tutorial spam and rewards the opposite: lived experience with named specifics.

## Instructions

### Feed Mechanics 2026

- The Relevant feed (default) ranks by tags the reader follows + reactions + recency + author follows. There is no single front page; your reach is the union of your tags' audiences.
- Reactions come in three flavors: heart, unicorn (roughly "exceptional"), and bookmark. Bookmarks are the strongest quality signal — how-to and reference content lives on bookmarks; opinion lives on hearts and comments.
- Comments drive the Top surface. The measured top posts pair high reaction counts with high comment counts; a post that starts a conversation outranks a post that ends one.
- Tags are the distribution: up to 4 per article. Mix reach and niche — one or two broad (`webdev`, `ai`, `programming`), one format (`discuss`, `showdev`, `devchallenge`), one niche that names your actual topic.
- The `discuss` tag is a format, not a topic — it marks a question to the community and gets its own audience of people who like answering.
- Weekly official surfaces (Top 7 email, badge awards, challenges) amplify winners. Challenges and platform series occupy much of the top surface — organic winners have to be genuinely engaging.

### Measured Patterns From the Live Top Surface (public API, top 40 of ~30 days, Aug 2026)

- Community discussion beats tutorials at the top: roughly half the top posts carry `discuss` — direct questions ("How would you decide whether the content is good or bad?" — 178 reactions, 129 comments), career reckonings, and AMAs.
- Winning title shapes, in order of prevalence:
  1. The reckoning claim: `The Junior Developer Pipeline Is Broken... And AI Broke It` (267 reactions, 212 comments). A debatable assertion about the profession, stated plainly.
  2. Myth-busting: `Stop Calling Everything Impostor Syndrome: The Myth of "Just Push Harder"` (175). Names a thing everyone repeats, then dismantles it.
  3. First-person journey with numbers: `From Silent Reader to 25 Articles: What 3 Months on DEV Taught Me + AMA` (106 reactions, 97 comments). Time period + count + lesson.
  4. Humor listicle: `8 Things Developers Confidently Explain After Watching One YouTube Video` (160). Listicles are alive here — when the list is a joke the reader recognizes, not SEO filler.
- Emoji in titles are normal (🍲 🚀 🐍 ❤️ all appear in top posts). Use at most one, and only when it fits the register.
- Career anxiety and AI-reckoning topics dominate the organic top: code ownership, AI-generated-code debt, "does learning to code still make sense". Honest ambivalence outperforms both hype and doom.
- Non-English community content reaches the top (Portuguese `braziliandevs` posts in the sample) — language-community tags are real distribution.

### Title Craft

- State a position someone could disagree with, or ask a question someone wants to answer. The two strongest measured shapes.
- Specifics carry: version numbers (`TypeScript 7 Went Native`), counts, timeframes.
- Sentence flow beats keyword-stuffing. `I Stopped Debugging at My Desk. Here's What Changed` reads like a person; `Debugging Tips and Tricks for Productivity 2026` reads like SEO.
- "Here's What Changed" / "What X Taught Me" framings are native and fine here — unlike HN, where they read as blogspam.
- Under ~80 characters; front-load the claim.

### Body Craft

- Open with the situation, not the throat-clearing. First paragraph earns the scroll: the moment, the number, or the claim.
- Code blocks with language hints, headers to segment, images where they carry information. dev.to renders rich markdown and supports embeds (liquid tags) — use them for repos, CodePens, tweets.
- Cover image matters: articles with covers get measurably more clicks from the feed card. A simple typographic cover beats none; a screenshot of the actual thing beats both.
- 3–8 minute read (roughly 800–2,000 words) is the native band. Longer works when it's a genuine reference piece people will bookmark.
- End with a question to the comments when you genuinely want answers. On dev.to this is native culture, not engagement bait — but it has to be a real question.
- A discussion post (`discuss` tag) is short by design: state the question, give your own partial answer or context in 2–4 paragraphs, get out of the way.

### Cross-Posting and Canonical URLs

- dev.to supports `canonical_url` — publish on your own blog first, cross-post to dev.to with canonical pointing home. Full SEO safety, full community reach. This is the platform-blessed pattern; use it by default when you own a blog.
- Series feature chains multi-part content with automatic navigation — use it instead of "Part 3 (see my profile for parts 1–2)".
- Don't dump an RSS firehose. Auto-cross-posted feeds with unedited relative links and missing images read as abandonware and get unfollowed.

### What Dies on dev.to

- AI-generated tutorial filler — the "Complete Guide to X in 2026" with no lived detail. The community has seen thousands; zero reactions is the norm.
- Pure product promotion without a builder's story. `showdev` exists for launches, but the post must be the story of building, not the landing-page copy.
- Keyword-stuffed SEO titles, hashtag stacks in the body, "In this article, we will discuss…" openers.
- Recycled listicles without a voice ("Top 10 VS Code Extensions" for the 400th time).
- Aggressive cross-linking to your paid course/newsletter in every section. One link in a bio-style outro is accepted.

### Comments

- Comments are long-form-friendly — 2–6 sentences with a specific experience is the native register. Markdown works; code blocks in comments are normal.
- The author is expected to reply. Top authors answer most substantive comments; discussion posts where OP vanishes die early.
- Same human rules as everywhere: open on content, add a specific, disagree politely with reasons. The community is beginner-heavy — condescension reads worse here than on HN.
- Zero to one structural imperfection; typos in code or tool names cost credibility. dev.to is proofread-casual, not typed-fast-casual.

### Timing and Cadence

- The feed is recency-weighted but forgiving — tag followers see posts for a day or more. Weekday mornings US time perform best for English content, but the effect is smaller than on velocity-gated platforms.
- Consistency compounds: followers accumulate per article, and the follow relationship feeds the Relevant feed. Weekly beats daily-then-nothing.
- Badges (streaks, challenges) exist and the community plays along — an 8-week writing streak is a legible, respected goal.

### Pre-Publish Checklist

- [ ] Title states a position or asks a real question; specifics front-loaded; under ~80 chars
- [ ] 4 tags: broad + format + niche mix; `discuss` only if it's genuinely a question post
- [ ] Cover image set; code blocks have language hints; embeds used where richer than links
- [ ] Opens with the situation, not "In this article…"
- [ ] Lived detail present: a named tool, version, number, or moment from actual experience
- [ ] Canonical URL set if this also lives on your own blog
- [ ] Ends with a real question only if you'll be in the comments answering
- [ ] No SEO-filler shape: would a developer bookmark or argue with this?
- [ ] Ready to reply to substantive comments for the first day

## Examples

### Example 1: Discussion post that works

> Title: How do you decide when a bug is "the model is wrong" vs "your prompt is wrong"?
> Tags: discuss, ai, programming, agents
>
> I've been burning hours on the wrong side of this line. Last week I rewrote a prompt four times before accepting the model just couldn't do the task.
>
> My current rule: I blame the prompt twice, then blame the model. It's arbitrary and I don't love it.
>
> What's your actual heuristic? Especially interested if you've got something better than "rewrite it N times and give up."

Why it works: real question, own partial answer given first, invites experience not opinion, author is clearly going to be in the comments.

### Example 2: Title comparison

Dead on arrival (SEO shape, no voice):
> The Complete Guide to Debugging AI Agents in 2026: Tips, Tricks and Best Practices

Native (position + lived specifics):
> I Stopped Trusting My Agent's Logs. Debugging Got Faster.

The first promises coverage; the second promises an experience with a lesson. The top surface is full of the second shape and has never once shown the first.

### Example 3: showdev launch that survives

> Title: I built a CLI that finds which of your node_modules you actually import
> Tags: showdev, node, javascript, opensource
>
> Started as a shell one-liner after a 4 GB node_modules broke our CI cache. Grew into a proper tool when the one-liner missed dynamic imports.
>
> [what it does, 2 paragraphs, with a terminal screenshot]
>
> Honest limits: monorepos with custom resolvers confuse it, and I haven't tested on Windows. Repo: [link]. If you try it on a weird setup, tell me what breaks.

Why it works: origin story with a number, screenshot of the real thing, named limitation, asks for failure reports not stars.

## References

- AgentSkills spec: https://agentskills.io/specification
- dev.to editor guide: https://dev.to/p/editor_guide
- dev.to public API (measured patterns source): https://developers.forem.com/api — top-surface pull, Aug 2026. Re-derive periodically.
- Companion skill: `content-voice` — the community rewards lived voice and punishes tutorial-mill tone
- Companion skill: `social-hackernews` — the inverse register; never port content unchanged between HN and dev.to
