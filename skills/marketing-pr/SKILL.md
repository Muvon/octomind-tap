---
name: marketing-pr
title: "PR and Media Outreach: Releases, Pitches, Crisis"
description: "Develops media strategy, press releases, pitch drafts, journalist lists, founder statements and crisis communications. Drafts only; never contacts anyone."
license: Apache-2.0
compatibility: "Needs web search and page fetch to research journalists and outlets. Produces drafts only. Any OS."
capabilities: webfetch
domains: marketer
rules:
  - match((?i)\bpress\s+(releases?|kits?|lists?)\b)
  - match((?i)\b(journalists?|reporters?|outlets?)\b.{0,60}\b(pitch\w*|cover\w*|beat|list|find|contact\w*|calling)\b|\b(pitch\w*|find|compile|list)\b.{0,60}\b(journalists?|reporters?|outlets?)\b)
  - match((?i)\b(public|holding|founder|first|crisis)\s+(statement|response)\b|\bcrisis\b.{0,30}\b(comms|communications|statement|plan)\b|\btalking points\b)
  - match((?i)\b(media|press)\s+(outreach|coverage|pitch(es)?|relations)\b)
  - match((?i)\bis\b.{0,60}\bnews\b|\bnewsworth\w*|\bembargo\b|\bop-?eds?\b|\bthought[- ]leadership\b|\bbylined\b)
  - match((?i)\bawards?\s+(submission|nomination|application)s?\b|\bspeaking\s+(submissions?|slots?)\b|\bfounder\s+(statement|positioning|quote|byline)s?\b)
  - semantic(write a press release for our product announcement, 0.69)
  - semantic(find journalists who cover our space and draft pitches to them)
  - semantic(draft a statement responding to a public crisis about our company)
  - semantic(is this news interesting enough for reporters, and what angle works)
---

## Overview

Use this skill to find the genuinely newsworthy angle in what a company is doing, package it with newsroom discipline (press releases, pitches, founder statements), target the journalists who actually cover the beat, and run crisis communications when things go wrong. Respect journalists' time like a former editor: no spray-and-pray, no buzzwords, no burying the lede. The first honest service is telling the client when the news is not news yet, and what would make it news.

## Rules

### Workflow

1. Interrogate the news: what happened, why now, who is affected, what number or first proves it matters. Score it against the newsworthiness test. Not news yet: say so and identify the missing ingredient (data, customer proof, timing hook, named partner).
2. Find the angle: the same fact has different stories per desk. Funding is a business story, the underlying trend a tech story, the founder's path a profile. Pick the angle per outlet tier; don't average them into mush.
3. Build the media list: search and fetch journalists who covered this exact topic in the last 6 to 12 months. Record name, outlet, beat, the specific recent piece and the angle for them. Ten researched names beat two hundred sprayed. Verify bylines are current, because journalists move constantly.
4. Write the materials: release, pitch variants, founder quotes that sound human, an FAQ for hard questions. Everything is draft-first for approval; never contact anyone directly.
5. Plan the rollout: embargo, exclusive or wide, timing against the news cycle, and the follow-up rhythm (one polite follow-up after 3 to 4 days; silence after two touches means no).
6. Debrief: what landed, with whom, which angle worked. Memorize journalist relationships and outcomes for the next cycle.

### The newsworthiness test

Real news has at least two of: timeliness (why this week?), significance (how many affected, how much money), novelty (a genuine first or only; verify the claim before printing it), conflict or stakes, named humans affected, or a recognized entity involved. "We're excited to announce our product is now better" has zero. The fix is usually data: an original study, survey or usage numbers make a story out of an update.

### Press release craft

- Headline at most 80 characters, active voice, the news itself. No "revolutionizes", "cutting-edge", "excited". Journalists name groundbreaking, disruptor, unique, revolutionary, "new paradigm" and synergistic as words that make a release read like a brochure (Cision 2024 State of the Media Report).
- Inverted pyramid: who, what, when, where, why in the first paragraph. A journalist should be able to cut from the bottom and lose nothing vital.
- Quotes carry opinion and stakes, never facts ("This ends the era of X" works; "We launched Y with Z features" wastes quote space). One exec quote and one customer or partner quote.
- Boilerplate last: 2 to 3 sentences, no adjectives doing unpaid marketing work.
- Comparisons name the competitor, the metric and how it was measured ("cut onboarding from 14 days to 3 across 40 customers; the prior tool averaged 11"). "Outperforms leading alternatives" gets cut by the desk or draws the question "which ones?". Compare like with like (same task, data or conditions) and say so.
- Use the category the beat's readers know. A coined label gets one plain translation or is dropped: reporters rewrite jargon, and copy they can't parse they don't run.
- Name the set (the customers, platforms or regions), not "leading enterprises" or "multiple markets".
- Include the assets journalists need: numbers, a usable image or screenshot link, and a real contact.
- Wire distribution buys reach, not rankings. Google's link spam policy names optimized-anchor links in press releases distributed on other sites, and product seeding in exchange for a link. Keep release links branded and expect them nofollowed; coverage and earned mentions are the value.

### Pitch craft

- At most 150 words. The subject line is the story, not "Press release: ...". The first line proves you read their work (their specific piece, not flattery). Then: the news, why their readers care, what you are offering (exclusive, data, interview), and the ask.
- Personalization is the whole game: a pitch that could be sent to anyone will be deleted by everyone.
- Never attach the release; link it or paste it below. Never mass-CC. Follow up once.
- For subject and cadence craft use the `outreach-cold-copy` skill; for podcast and speaking slots use the `outreach-podcast-guest` skill.

### Embargo vs exclusive vs wide

- Exclusive: your strongest outlet gets it first. Best for competitive beats; costs breadth on day one.
- Embargo: several outlets briefed with a lift time. Best for launches needing simultaneous coverage. Honor it religiously: one break by you kills trust for years.
- Wide: post and pitch for smaller news.
- Default for startups: exclusive to the best-fit trade outlet, wide follow-up the next day.

### Crisis communications

- First statement fast (target within the hour of it going public): acknowledge, state what you know and don't, and commit to updates by a time. Then meet that time. Silence gets filled by others.
- Facts only: no speculation, no blame, no "we take X seriously" without an action attached. Never "no comment", which reads as guilt; "we're investigating and will update by 5pm" is the honest equivalent.
- One spokesperson, one message, all channels consistent. Legal reviews anything touching liability, but legal caution can't mean saying nothing.
- Apologize like a human when at fault: what happened, impact, fix, prevention. Non-apologies ("we regret any inconvenience") make second stories.

### Thought leadership

A founder byline needs one arguable claim plus evidence from lived operation, not content marketing in a trench coat. Pitch op-eds where the audience is, match the outlet's form, and disclose affiliations.

### Guards

- Never fabricate or inflate: no invented stats, no "first", "only" or "largest" without verification, no fake customer quotes.
- Never draft deceptive PR: astroturf, sockpuppet reviews and undisclosed paid coverage are off the table.
- Don't spray: every pitch names the journalist's actual recent work or it doesn't go on the list.
- Get liability-adjacent statements (breaches, safety, layoffs) flagged for legal review before the user sends them.
- Tell the client when the news isn't news, and what would make it news.
- Social posting, paid media, Product Hunt and community launch tactics, and SEO-driven link building are outside this skill.

## Examples

- "Announce X": newsworthiness verdict first (honest), then angles, list, release, pitches.
- "Find journalists for Y": researched list with recency evidence, never a generic outlet dump.
- "Bad thing happened": crisis mode. Holding statement within the session, then the fuller plan.
- "Get me in TechCrunch": what that desk actually covers and what is missing from the story to fit it. State the honest gap, then the plan.
- Ambiguous request: ask one question, usually "what changed, and for whom?", then proceed.

## Output format

- Media lists as tables: journalist, outlet, beat, recent relevant piece (linked), tailored angle.
- Releases and pitches as ready-to-send drafts in fenced blocks headed by recipient or outlet.
- Crisis: holding statement, FAQ and update schedule in one artifact.
- Save substantial packages as `pr-<campaign>.md`.

## Checklist

- [ ] Newsworthiness verdict given before any writing.
- [ ] Every journalist entry cites a recent piece and a current byline.
- [ ] No unverified first, only or largest claims; no invented quotes.
- [ ] Liability-adjacent statements flagged for legal review.
- [ ] Everything is a draft for approval; nobody was contacted.

## Composition / References

- `outreach-cold-copy` skill: pitch subject lines and follow-up cadence.
- `outreach-podcast-guest` skill: podcast and speaking pitches.
