---
name: trend-hackernews
title: "Hacker News Trend Harvester Playbook"
description: "Platform-specific intel for harvesting Hacker News trends — point-velocity ranking, harvest URLs (front page, new, Show, Ask, Algolia), flag-tax mechanics, title rules from HN guidelines, Show HN / Ask HN / link-submission patterns, anchor commenters and dead patterns in 2026. Activates inside an octoweb:trend session whenever the user names HN / Hacker News."
license: Apache-2.0
compatibility: "Octoweb browser access. Logged-out works for all front-page and Algolia surfaces; logged-in needed to see [dead] posts and to submit."
capabilities: octoweb memory
domains: octoweb
rules:
  - session(trend) content(hackernews)
  - session(trend) content(hn)
  - match(\b(hacker\s*news|hn)\s+(trend|trends|harvest|brief|post|submit)\b)
  - match(\b(harvest|scan|analyze)\s+(hacker\s*news|hn)\b)
  - match(\bshow\s*hn\b)
  - match(\bask\s*hn\b)
---

## Overview

This skill carries the platform-specific mechanics the `octoweb:trend` agent needs to harvest Hacker News — current ranking signals (point velocity × comment depth × flag-tax × age-decay), harvest URLs, title rules from HN guidelines, Show HN / Ask HN / link-submission patterns, anchor commenters, dead patterns. The agent owns the shared DNA loop; this skill plugs the HN parameters in.

## Mental model

HN is one audience with one strict culture: skeptical, technical, anti-marketing, anti-listicle. The ranker is point velocity × comment depth × flag-tax × age-decay. Point velocity in the first 90 minutes is the entire game — a post is either on the front page or dead after that. Comments boost ranking sub-linearly but heavily — a post with 50 points and 80 comments often outranks one with 100 points and 5 comments. Flags are anonymous and powerful — 3–5 flags can sink a climbing post. A title that wins on Reddit dies on HN in 4 minutes if it editorializes or sounds like marketing.

## Rules

### Current ranking signals (2026)

| Signal | Effect |
|---|---|
| Points per hour, first 90 min | Primary signal. >30/h = front-page-bound, >60/h = breakout |
| Comment-to-point ratio | Discussion signal. >30% high, >50% contested |
| Survival past 90 min | Most posts die in new. Still on front page at 4h = winner |
| Flag tax | Visible `[flagged]` or sudden rank drop despite point accumulation |
| Domain authority bias | github.com / arxiv.org / personal blogs get small lift; SaaS company blogs get tax |
| Submitter karma band | Visible on profile; low-karma submitters get more flag-prone |

### Harvest surfaces (run in parallel)

| Surface | URL | Yields |
|---|---|---|
| Front page | `https://news.ycombinator.com/news` | Top 30 right now |
| Page 2–3 | `https://news.ycombinator.com/news?p=2` / `?p=3` | Decaying posts — what's losing velocity |
| New | `https://news.ycombinator.com/newest` | First-30-min submissions — most die here |
| Show HN | `https://news.ycombinator.com/show` | Show-format breakouts |
| Ask HN | `https://news.ycombinator.com/ask` | Discussion-format breakouts |
| Best (recent) | `https://news.ycombinator.com/best` | Highest-point posts of the day |
| Algolia, last 24h, by topic | `https://hn.algolia.com/?dateRange=last24h&query=<topic>&sort=byPopularity` | Topic-filtered by score |
| Algolia, last week, by topic | `https://hn.algolia.com/?dateRange=pastWeek&query=<topic>&sort=byPopularity` | 7-day niche window |
| Algolia all-time on topic | `https://hn.algolia.com/?query=<topic>&sort=byPopularity` | Durable-angle reference |

Run 5–8 in parallel.

### Scoring rubric (HN-specific signals)

Virality axis 0–5:
- Point velocity (pts/hour in first 4h) — primary
- Comment-to-point ratio
- Survival past 90 min on front page
- Flag-tax presence — visible `[flagged]` or rank drop
- Domain authority — github / arxiv / personal blog get bonus, SaaS-blog gets tax

Niche-fit axis 0–5 — universal scale. Note HN's niche shifts weekly; weight against last-week saturation.

### Title rules (HN guidelines + 2026 observed reality)

DO:
- Use the article's exact title for link submissions (HN guideline)
- Use precise, specific noun phrases
- Lead with the artifact, not the actor

DO NOT:
- ALL CAPS or excessive punctuation (auto-flags)
- Editorialize beyond the article's own phrasing
- Use marketing-speak ("revolutionary," "game-changer," "unleash," "groundbreaking")
- Add a year suffix unless the article is dated
- Use question titles unless Ask HN

Show HN pattern: `Show HN: <noun phrase, what it is> — <one-clause clarifier if needed>`
Ask HN pattern: `Ask HN: <direct question, no preamble>`

### Body / first-comment patterns

Show HN — first author comment with:
- 3–5 line context (what it is, what problem it solves, why you built it)
- Pricing transparency if commercial (free for X, paid for Y) — opacity flags
- Tech stack mention if relevant
- Honest limits ("doesn't yet do X") — preempts critical comments

Ask HN — body sets up the question with 3–6 lines of concrete context (specific situation, what you tried, where you're stuck). Vague Ask HN dies.

Link submissions — no body needed. First-comment from submitter sometimes worth it if the article is dense.

### Dead patterns (flagged / killed reliably)

- "I built X with AI" without substantive demo
- Listicle blog posts ("10 tools for ...")
- LinkedIn-style motivational
- Recycled OpenAI / Anthropic press releases without analysis
- Pure SaaS launch posts not in Show HN format
- Anything reading as "ChatGPT wrote this" / generative-content tells
- Self-promotional past Show HN format

### Anchor commenters

Specific high-karma users reliably comment on niche threads. Identify them during harvest — their participation often signals the post will survive the front-page filter. Do not @-mention them in the post (HN doesn't support that culturally) but note them for the user's awareness.

### Timing

- Best windows: Tue–Thu 8–11 AM ET. Weekend mornings work for personal-blog technical writing.
- Late Friday and weekends: slower for hard-tech, faster for opinion pieces.
- Post then be available — first 90 minutes the submitter must answer top comments.

### Saturated-angle detection

HN's tech-niche saturation cycles fast. Run Algolia "pastWeek" search on the user's topic terms. If 5+ front-page posts hit the same angle in the last 7 days, mark saturated. Common 2026 saturated angles in agents / LLM space: "Why we moved off OpenAI / off Anthropic," "Why we built our own RAG," "GPT-X benchmark results," generic "agent failure" post-mortems without specifics.

## Examples

### Example 1: Front-page post with full DNA call

Bad — count without context:
```
Show HN post got 400 points yesterday.
```

Good — velocity, flag-state, domain, anchor commenters labeled:
```
"Show HN: {{tool name}} – local agent eval harness"
412 pts / 187 comments / 5h on front page / 82% upvote-implied / not flagged
Submitter: {{handle}} (karma 3,400 — credible)
Domain: github.com — domain trust bonus
Front-page entry: 14 minutes after submission (very fast climb)
Points/hour first 4h: ~75/h (breakout band)
Anchor commenters participating: {{handle1}}, {{handle2}} — high-karma niche regulars
Title type: Show HN, noun phrase + one-clause clarifier
First-comment author post: 5 lines — what it is, problem it solves, stack, free / paid, known limits
DNA: github-hosted artifact + transparent pricing + honest-limit preempt
```

### Example 2: Flagged-cluster teaching example

```
{{Title}} — 84 pts in 35 min then [flagged] at 47 pts
Submitter karma: 120 (new account)
Domain: marketing-domain.com
Inferred flag reason: SaaS-launch tone + marketing domain + new-account submitter + non-Show-HN format
Lesson: do not submit a SaaS launch post outside the Show HN format from a low-karma account.
```

## Checklist

Before returning the HN section of the brief:
- [ ] Every cited post has title (verbatim), points, comments, hours-since-submit, domain, submitter handle and karma band, URL, flag-state
- [ ] Point velocity (pts/hour first 4h) computed and used as primary signal — not raw points
- [ ] Survival past 90 min noted
- [ ] Flagged-but-alive and outright-flagged posts surfaced as teaching examples
- [ ] Anchor commenters identified for the niche (not @-mentioned, just noted)
- [ ] Domain mix tabulated (% github / arxiv / personal-blog / news / SaaS) on front-page winners
- [ ] (Opt-in mode only) Title bank entries pre-cleared against HN title rules — no editorializing, no caps, no marketing speak
- [ ] (Opt-in mode only) Show HN / Ask HN format prescriptions match this skill's templates
- [ ] (Opt-in mode only) First-comment seed includes pricing transparency for Show HN if commercial
- [ ] Dead-pattern list applied — no recommendation matches "AI wrote this" / listicle / press-release patterns
- [ ] (Opt-in mode only) Submit-time recommendation falls in Tue–Thu 8–11 AM ET unless niche evidence shifts it
- [ ] All background tabs closed

## Composition / References

- Pairs with `social-hackernews` (content domain) for writing the actual submission body and first-comment from the brief.
- Algolia URL parameters: `dateRange=last24h|pastWeek|pastMonth`, `sort=byPopularity|byDate`, `query=<terms>`.
- HN guidelines: https://news.ycombinator.com/newsguidelines.html — title rules in particular.
- Use the agent's universal output schema.
