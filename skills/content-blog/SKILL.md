---
name: content-blog
title: "How to Write a Blog Post: Opinionated Short-Form"
description: "Write 600-1500 word opinionated blog posts with a strong hook, a clear point of view, light SEO, and Markdown output. Use for short-form posts."
license: Apache-2.0
compatibility: "Needs web search and page fetch for quick research. Saves Markdown to the working directory."
capabilities: webfetch variety
domains: writer
rules:
  - match((?i)\b(write|draft|produce|do|give)\b.{0,40}\b(blog\s*post|hot\s+take|opinion\s+(post|piece)|reaction\s+(blog\s+)?post|take[- ]style)\b)
  - match((?i)\b(opinionated|punchy|spicy|contrarian|snarky)\b.{0,40}\b(post|piece|take)\b)
  - match((?i)\b\d{3,4}[- ]word\b.{0,30}\b(post|take|piece)\b)
  - match((?i)\b(600|800|1000|1200|1500)[-\s]?(word)?\s*blog\b)
  - semantic(write a short opinionated blog post with a strong hook, 0.72)
  - semantic(turn this idea into a punchy blog post, 0.72)
  - semantic(draft a short blog post with a clear opinion about this, 0.72)
  - semantic(write a four hundred word post for our company blog, 0.72)
---

## Overview

Write short-form, opinionated posts (about 600 to 1500 words) that people finish: a hook, a point of view, no corporate fluff, no AI-sounding filler. The outcome is a Markdown post saved to disk and returned in full. Write for humans first; SEO is a byproduct of good writing. Long-form researched articles, raw-notes-to-draft work, edits of existing copy, and scoring use other skills (`content-article`, `source-to-draft`, `content-edit`, `content-audit`). Posting the approved post is a separate step done from the approved copy.

## Rules

### Workflow

1. Clarify the topic, audience, tone, and the author's first-hand material (what they did, numbers, screenshots). Ask once. With no audience given, ask "Who's this for?" once, then default to smart-general.
2. Quick research: two or three targeted searches in one parallel block. Cover the current conversation around the topic (news, debates, hot takes); a surprising stat, counterintuitive fact, or hook angle; and what the top-ranking posts say and which format the results reward (`content-formats`), so the post can say something different. A post needs a point of view, not a literature review.
3. Draft the full post with no outline approval; blog posts move fast.
4. Save to disk as Markdown and return the full post in the final message.

Before writing, recall brand voice, target audience, writing style, tone preferences, and past posts from memory. After, memorize tone decisions, audience notes, and recurring topics.

### Voice

- Conversational but smart: a knowledgeable friend, not a textbook. Opinionated: have a take and defend it. Direct: say the thing, then explain it.
- Specific: "3 hours" not "a long time", "47% of marketers" not "many marketers". That is style only; every number must be sourced.
- Human: contractions where the register allows, occasional rhetorical questions, real examples.
- Break grammar rules on purpose: start sentences with "And", "But", "So". Use fragments for punch and parenthetical asides (like this).
- Don't rotate synonyms. If "users" is the right word, keep saying "users"; "users/customers/clients/patrons" reads as AI.

Tone by audience: developers get dry and technical with no fluff; marketers get energetic, data-driven, practical; a general audience gets warm, accessible, relatable; executives get direct, strategic, ROI-focused; creators get enthusiastic, personal, story-driven (only with the author's own log; see experience rules).

### The hook

Great hooks: a counterintuitive claim ("The best blog posts aren't written, they're edited."), a sourced surprising stat ("[Verified number] of readers never reach your second paragraph."), a relatable frustration ("You've read a hundred posts about productivity. None of them worked."), a bold opinion ("Most SEO advice is wrong, and here's why.").

Bad hooks: "In today's fast-paced world...", "Have you ever wondered...", "X is very important in modern times...".

### Paragraphs and transitions

- At most three or four sentences per paragraph, one idea each; readers scan.
- Rhythm follows the argument: a long sentence can land on a short one; fragments and one-sentence paragraphs are for emphasis, not a quota.
- No paragraph starts with "I" twice in a row.
- Skip the transition when the logic is obvious. When needed: "But here's the thing:" / "So." / "And yet." / "The catch?" / "Here's where it breaks down." / "Plus," / "On top of that,". Never "Furthermore," "Moreover," "Additionally," "Consequently," "It's worth noting," "Moving on...", or "As we discussed...".

### Grounding

Before writing any specific (tool, version, price, person, stat, quote, URL), classify it (full protocol: `content-grounding`):

- Common knowledge or familiar: write it.
- Unfamiliar entity: stop, research, then write.
- Time-sensitive (versions, prices, "latest", recent events): stop and verify by web search.
- Speculative: write it as opinion ("I'd argue"), never as fact.

When research fails after two or three targeted queries, escalate with a precise forked question: "(a) share a source, (b) drop the claim, (c) mark it `[needs verification]`." Shipping fast does not mean shipping fake.

### Avoid

- Hedging everything ("might", "could potentially", "in some cases"): commit to the point.
- Listicle padding, or padding to hit a word count: every item earns its place.
- Dead conclusions: never open one with "In conclusion," "Overall," "In summary," "To summarize," or "To wrap up." End with a question, a prediction, a callback to the opening, or just stop.
- A generic intro that could be about anything, or a conclusion that only summarizes.

### SEO and AI search (light touch)

- Primary keyword in the title and the first 100 words, then two or three natural uses.
- Descriptive subheadings (H2s with keyword variants), in question or spoken phrasing when natural ("How I cut...", "Why X doesn't work", "What changed when we...").
- A one- or two-sentence direct answer to the post's core question early in the intro. Google says AI Overviews and AI Mode need no special markup or llms.txt; `content-geo` has the answer-first patterns.
- A meta description of about 150 to 160 characters (Google may rewrite it), compelling, with the keyword.
- An author byline with real name and credentials where readers expect one. Never "Admin" or an invented persona; Google treats fabricated authorship as deceptive.

### Experience over volume

Google's guidance asks for first-hand experience and original information. Experience is evidence the author holds, not a tone you add.

- Write first-person tests ("I tried this for 30 days") only when the author supplied the log, numbers, or account.
- Screenshots, dashboards, named tools and versions, and real error messages come from the author's material; otherwise write a captioned shot list for them to fill.
- One honest failure or "here's where the data is mixed" beats five hedged generalities.
- No first-hand material on this exact topic: frame the post as opinion ("Here's what I'd argue"), reported synthesis, or interview. Never pretend authority.

A generic explainer an LLM could rebuild from the top results adds nothing, and mass-producing such posts is what Google's scaled content abuse policy targets.

### Interaction

- Topic with audience: research and draft immediately, no outline.
- Topic without audience: ask once, then draft.
- Revision request: a targeted edit only; don't rewrite the whole post.
- "Make it shorter" or "longer": cut or expand without changing the voice.
- Autonomous, non-interactive brief, or a self-contained brief where nobody can answer mid-run: use the brief's audience (or smart-general), draft, list assumptions, and mark unverifiable claims `[needs verification]` inline instead of asking the forked question.

### Never

- Write first-person tests, results, or anecdotes the author didn't supply.
- Fabricate any specific the `content-grounding` skill marks as zero-exception (function signatures, versions, prices, URLs, person names, quotes, statistics, command flags, product features). Search or escalate.
- Prefer secondary blog summaries over primary sources.

## Output format

Pick the format from the query's intent with the `content-formats` skill and include its must-haves:

```
# [Title: specific, curiosity-driven, or a bold claim]

[Hook paragraph, 2-3 sentences max. Earn the scroll.]

[Answer paragraph: core thesis, 1-2 sentences. This is what AI engines extract first.]

[Context paragraph: why this matters, why now]

## [First key point, most important: 3-5 paragraphs, one idea fully developed]

## [Second key point: 3-5 paragraphs]

## [Third key point or counterpoint: 2-4 paragraphs]

## [Conclusion: not a summary, a landing. What to do with this, what it means, what's next.]
```

Adapt freely; match the format to the topic:

- Listicle: numbered, self-contained items, each with a "best for" or takeaway; selection criteria stated.
- How-to: numbered steps with the expected result after each, no fluff between steps.
- Opinion or hot take: a strong thesis up front, evidence, the best counterargument, then double down.
- Case study: starting point, what was done, measured result and timeframe, what failed.
- Explainer: answer first, why it matters, how it works, what to do.

Save as `[post-slug].md` in the working directory, with optional frontmatter when the user asks:

```
---
title: "..."
date: YYYY-MM-DD
description: "..."
author: "..."
updated: YYYY-MM-DD
tags: [tag1, tag2]
schema: [article]
---
```

## Checklist

- [ ] The hook is specific and the thesis appears early.
- [ ] Every specific is common knowledge, verified, or marked as opinion or `[needs verification]`.
- [ ] No first-person claim without author material.
- [ ] The conclusion lands; it does not summarize.
- [ ] Post saved as Markdown and returned in full.

## Composition / References

- `content-formats` (format by intent), `content-geo` (answer-first patterns), `content-grounding` (claim triage), `content-voice` and `content-humanize` (prose checks), `content-audit` (scoring).
