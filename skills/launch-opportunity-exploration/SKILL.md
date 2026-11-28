---
name: launch-opportunity-exploration
title: "Opportunity Exploration: Pain Mining and Gap Ranking"
description: "Mine Reddit, Hacker News and review sites for user pain, map competitor gaps and rank scored product opportunities. Use for open market discovery."
license: Apache-2.0
compatibility: "Needs web search and a browser for reading full threads and reviews. Any OS."
capabilities: browser
domains: founder
rules:
  - match((?i)\b(explore|discover|mine|scan|research)\b.{0,40}\b(opportunit\w+|pain\s+points|blue[- ]ocean|market\s+gaps?|unmet\s+needs?)\b)
  - match((?i)\bwhat\s+(should|could|can)\s+(i|we)\s+(build|make|create)\b)
  - match((?i)\b(find|generate|suggest)\b.{0,20}\b(startup|product|saas|app)\s+ideas?\b)
  - match((?i)\b(pain\s+points?|workarounds?|frustrations?|complain\w*|unmet\s+needs?|underserved)\b.{0,80}\b(rank\w*|gaps?|opportunit\w+|openings?|niches?)\b)
  - match((?i)\b(rank\w*|scored?)\b.{0,40}\b(opportunit\w+|gaps?|niches?|unmet\s+needs?)\b)
  - match((?i)\b(reddit|hacker\s+news|trustpilot|g2|app\s+store)\b.{0,80}\b(reviews?|threads?|complain\w*|frustrat\w*|hate)\b)
  - match((?i)\bblue[- ]ocean\b|\bwhat\s+(users|people)\s+(hate|complain)\b|\bcompetitor[- ]gap\b|\bgap\s+(map|matrix)\b)
  - semantic(find unmet needs in a market that a small team could build for, 0.72)
  - semantic(scan reddit and review sites for what people complain about in this space, 0.69)
  - semantic(rank product opportunities by how underserved the pain points are, 0.69)
  - semantic(what gaps do competitors leave that I could build a product for, 0.71)
---

## Overview

Discover opportunities from a vague problem space, market or rough idea: the gaps between what people need and what exists, especially blue-ocean angles a small team can win. Mine real conversations, extract pain signals (recurring complaints, unmet needs, workarounds), map who serves the space and what users hate about it, then score and deliver a ranked set of evidenced opportunities, never one idea. This skill discovers; it does not render a go/no-go verdict on a single chosen idea.

## Mental model

Think like an indie hacker with a researcher's discipline: obsess over real user language, meaning the exact words of frustration, the workarounds built and the money thrown at bad solutions. Past behavior is the only currency (Mom Test).

## Rules

### Process

Fire independent searches and browser actions in parallel in one tool-call block.

Phase 1, landscape scan. Run 5-8 parallel searches: "[space] biggest frustrations site:reddit.com", "[space] problems site:news.ycombinator.com", "[space] complaints / sucks / alternatives", "[space] market size / trends [current year]", "[space] startups / tools / software", "what I wish [space] had" and "[space] feature request".

Phase 2, deep conversation mining (browser). From Phase 1 leads, browse 5-10 high-value pages, not 50: full Reddit and HN threads (the gold is in replies, which snippets miss), Product Hunt launch comments, G2, Capterra and Trustpilot reviews, niche domain forums, GitHub issues and discussions of open-source tools, competitor pricing pages, feature lists, changelogs, and any promising result whose snippet is incomplete. Navigate straight to the target URL, extract key quotes and data points (never raw HTML), and screenshot competitor pricing or key UI for reference.

Phase 3, sentiment and pattern analysis. Extract: pain frequency; pain intensity (mildly annoyed versus desperately seeking); willingness to pay (already paying for bad solutions, asking for paid tools); workarounds (spreadsheets, scripts, manual processes); underserved segments (small teams, specific industries, non-technical users, geographies); timing signals (new regulations, technology or platform shifts).

Phase 4, competitive gap analysis. Per promising area: list all existing solutions (commercial, open-source, workarounds); what they do well and what users hate; the unserved feature, audience and price combination; competitive density (red ocean: crowded, big players; blue ocean: underserved, fragmented); zombie competitors, meaning abandoned, outdated or poorly maintained tools.

Phase 5, scoring (1-5 each). Problem severity (hair-on-fire to nice-to-have), market evidence (strong signals to speculation), competition gap (wide open to saturated), indie-friendliness (solo-buildable to needs a team of 50), monetization clarity (obvious willingness to pay to unclear), timing (perfect moment to too early or late).

Memory: before starting, remember(["market research", "product opportunities", "competitor analysis", "user pain points", "blue ocean"]). After completing, memorize() all findings, opportunity scores, key sources and competitive intelligence.

### Sources

- Primary (highest signal): Reddit (subreddit searches, complaint threads, "what tool do you use for X"); HN (Show HN launches and their comments, Ask HN, "Who is hiring" for market signals); Product Hunt (comment sentiment, upvote patterns); 1-3 star G2 and Capterra reviews (exact pain points); Twitter/X ("[tool] sucks", "[space] frustrating", indie maker discussions).
- Secondary (context and sizing): industry reports, blogs, trend analyses; Stack Overflow, Quora and specialized forums for technical pain; GitHub trending, issues and discussions; Indie Hackers and Show HN for what is being built; app store reviews for mobile-adjacent opportunities.
- Tertiary (validation): Google Trends (demand trajectory), job postings (growing needs), VC funding announcements (market heat: opportunity and competition), patent filings (big-player interest).

### Gap patterns

- Overserved mainstream, underserved niche: enterprise tools, nothing for freelancers or small teams.
- Feature bloat: "I just need X, not this monster tool".
- Price gap: expensive tools with no affordable alternative, or free tools with no premium option.
- Workflow gap: two tools that should talk to each other but don't.
- Platform shift: a new platform, API or regulation creating needs old tools miss.
- Geographic gap: built for the US market, nothing for another region.
- Persona gap: tools for developers, nothing for designers doing the same task, or vice versa.
- Time gap: tools not updated in years, users begging for modern alternatives.

### Evidence bar

- Hierarchy, strongest first: a workaround already built (spreadsheet, script, hired help) or money and time already spent, then repeated specific complaints, then stated preferences. Compliments and hypothetical "I'd totally use that" are worthless.
- Triangulation: a pain counts only when it appears unprompted across independent sources and communities, weighted to the last 6-12 months. A single viral post is noise. In review mining, a theme in at least 15% of an incumbent's negative reviews is a real weakness.
- Hunt disconfirmation deliberately: the graveyard check (who tried this and died, and why), the solved-problem check, and "do nothing" as the default competitor. If every signal you found is positive, you searched wrong.
- Frame every opportunity as: segment, struggling moment, current workaround, and what better looks like.
- Separate strong signal (many people) from weak (one mention). Use real quotes from real people with source links. Never fabricate quotes or statistics; if no evidence is found, say so, and "I found limited data on this" beats false confidence.
- Note whether each opportunity is growing, stable or shrinking, and offer multiple approaches per opportunity.

### Red flags

A free tool with strong network effects dominates; it needs massive data or infrastructure (not indie-friendly); regulatory complexity requiring legal expertise; a vitamin, not a painkiller (no urgency); it requires changing deeply ingrained behavior; winner-take-all dynamics (marketplace, social network); big tech is likely to build it as a feature. Don't recommend markets dominated by well-funded incumbents without flagging the risk, and don't wave competitors away.

### Willingness-to-pay signals

Already paying for inferior solutions; "I'd pay $X for something that just does Y"; workarounds involving paid tools (Zapier, spreadsheets, manual labor); a B2B tool saving employee time (easy ROI); a compliance or legal requirement driving the purchase; "shut up and take my money" on Product Hunt or HN.

### Ask or assume

- Problem space described: run the full 5-phase exploration. Ask at most 1-2 clarifying questions, and only if the space is too broad to research ("software" is too broad; "project management for construction teams" is right).
- "Go deeper on opportunity X": more user quotes, competitors and approaches for that one.
- "Compare X vs Y": a head-to-head opportunity comparison with evidence.
- "What about [niche]?": a focused exploration of that niche within the broader space.
- Vague input ("I want to build something"): ask which domains interest them, what skills they have and which audience they understand; explore from their strengths.

## Output format

Deliver at least 3 ranked options, each scored per dimension with evidence and judged on indie-friendliness. Save the full report as `explore-[space-slug].md` and, if extensive, raw notes as `explore-[space-slug]-raw.md`.

```markdown
# Opportunity Exploration: [Problem Space / Market]

## Executive Summary
[2-3 sentences: what you explored, what you found, top recommendation]

## Research Coverage
Sources analyzed: [count of threads, reviews, launches] · Communities explored: [subreddits, forums, sites] · Competitors mapped: [count] · Date: [current date]

## Top Opportunities (Ranked)

### Opportunity 1: [Name / Description]
Opportunity Score: [X/30]
| Dimension | Score | Evidence |
|-----------|-------|----------|
| [one row per Phase 5 dimension] | X/5 | [specific evidence] |

The Pain: [the specific problem, in actual user quotes]
User Voices (2-3 real quotes, one showing willingness to pay or a workaround):
> "[Exact quote from Reddit/HN/forum]" - [source link]
Current Landscape:
| Existing Solution | What It Does | Why It Falls Short | Pricing |
The Gap: [what is NOT being served: the blue-ocean angle]
Who It's For: [specific persona, not "everyone" but "freelance designers who manage 5-15 clients and track invoices in spreadsheets"]
Why Now: [what changed: technology, regulation, market shift, competitor neglect]
Possible Approaches: A: [product concept + differentiation angle]; B: [alternative angle on the same gap]
Risks & Concerns: [each risk + mitigation]
Estimated Effort: [Solo weekend project / 2-4 week MVP / Multi-month build]

### Opportunity 2 and Opportunity 3: [same structure]

## Honorable Mentions
[2-4 more worth noting, 2-3 sentences each]

## Anti-Patterns Detected
[Ideas that look promising but hide traps]
- [Trap]: looks good because [X], but [fatal flaw]

## Raw Research Notes
### Key Reddit Threads · Key HN Discussions · Product Hunt Launches Analyzed · Competitor Reviews Analyzed (G2/Capterra)
- [Title](URL): [key insight / upvotes and comment themes / key complaints]

## Methodology
[Search queries used, communities explored, how opportunities were scored]
```

## Checklist

- [ ] At least 3 ranked opportunities, each scored on all six dimensions?
- [ ] Every opportunity backed by real quotes with source links, and weak signals marked as weak?
- [ ] Disconfirming evidence (graveyard, solved problem, do-nothing) searched and reported?
- [ ] Competitors listed for each opportunity, including zombie tools and workarounds?
- [ ] Red flags and anti-patterns stated, with indie-friendliness judged?
- [ ] Report saved under the file names above?

## Composition / References

- `launch-idea-validation` skill: takes one chosen opportunity to a go or no-go verdict.
