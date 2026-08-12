---
name: social-medium
title: "Medium Publishing Playbook"
description: "Ground-truth 2026 playbook for publishing stories on Medium. Covers the Boost curation system (human editors route most distribution, ~50% via publication nominations), member-reading-time economics (completion ratio beats views), the four-legs story structure from real publication-editor data, the 7–10% CTR title target, the 3-specific-tags rule, publications vs solo publishing, and Medium's hard ban on AI-generated content in the Partner Program. Activate when drafting anything destined for Medium."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Medium (medium.com and Medium publications)."
domains: content
rules:
  - match(\bmedium\.com\b)
  - match(\bmedium\s+(article|post|story|publication)\b)
  - match(\bpost\s+(on|to|for)\s+medium\b)
  - match(\bmedium\s+partner\s+program\b)
  - match(\bboost\s+nomination\b)
---

## Overview

Medium in 2026 is a human-curated platform wearing an open-platform costume. Anyone can publish, but distribution is routed by a small group of editors and Medium's curation team through Boost — and roughly half of Boosted stories arrive via publication-editor nominations. The platform pays for the attention of paying members, measured in reading time, not views.

Two consequences shape everything: publications are the distribution lever (a solo profile under ~5,000 followers has minimal reach), and AI-generated content is a policy violation, not just a style problem — undisclosed AI writing gets stories removed from the Partner Program, and a single flagged piece damages the entire publication's Boost standing.

Pair with `content-voice`. On most platforms AI-shaped prose costs reach; on Medium it costs the account.

## Instructions

### Distribution Mechanics 2026

Three tiers, in descending reach:

| Tier | Who decides | What it takes |
|---|---|---|
| Boost | Human curators + publication editor nominations (~50% of Boosts) | Original insight, lived experience, clean craft; strong editors hit ~87% nomination acceptance by knowing the bar |
| General Distribution | Algorithmic — topic pages, followed tags, follower feeds | Baseline for compliant human-written stories |
| Network only | Nobody | Disclosed-AI stories cap here; undisclosed AI risks removal |

- Member reading time is the currency. A story with 2,000 views at 85% completion outearns one with 5,000 views at 40%. Write to be finished, not clicked.
- Partner Program pays from member reading time, claps, highlights, and responses. Top niche writers earn $1K–$10K+ monthly; the median is near zero — treat Medium as top-of-funnel to your newsletter/consulting (the CEO says this himself), not as the income.
- Paywall math: about two-thirds of Medium stories aren't paywalled. Paywalling enters you into a smaller, higher-quality pool read by paying professionals. Paywall your strongest work, keep discovery pieces free.
- External SEO is real: Medium domains rank well; evergreen how-tos earn search traffic for years regardless of Boost.

### The AI Content Policy (hard constraint)

- Undisclosed AI-generated writing violates Partner Program terms. Enforcement tightened through 2026: AI filler is demoted or removed, and human curation is explicitly Medium's strategic defense against it.
- Disclosed AI writing may exist but is ineligible for Boost and cannot be paywalled.
- Detection looks for the familiar markers: "delve", "unlock", parallel tricolons, template-like headers, uniform paragraph rhythm. See `content-voice` for the full kill-list.
- Publication-level blast radius: one AI-flagged story damages the whole publication's Boost status. Editors reject anything that smells like AI to protect their pipeline — the bar you must clear is the editor's paranoia, not just the classifier.

### Title Craft — the CTR Loop

Real numbers from a major publication editor: click-through under 2–3% means the title is unclear — rewrite it; 7–10% is the sweet spot. Titles are editable after publishing — rewrite underperformers within 48 hours instead of abandoning the piece.

- Clear, arguable positions beat curiosity gaps. `7 Python Libraries That Replaced All My AI Engineering Boilerplate` and `NVIDIA Just Dropped the Most Efficient Reasoning Model of 2026` are real high-performers — both state exactly what the piece claims.
- Numbers, named tools, and recency markers pull professionals; vague intrigue ("This Changed How I Think About Code") pulls nobody who finishes.
- Subtitle (the kicker) is part of the click decision — use it to state the payoff, not to repeat the title.

### Story Structure — the Four Legs (from measured publication data)

Every high-performing piece contains all four; pieces missing any leg underperform regardless of writing quality:

1. A debatable claim in the headline — something a reader could disagree with.
2. Recent proof — news, release, or data from roughly the last 30 days that makes it timely.
3. Named specifics — tools, people, version numbers, dates. Generic ≈ unfinished.
4. An actionable takeaway — a checklist, framework, or Monday-morning task the reader leaves with.

Craft rules:

- 1,500–2,500 words is the measured band. Long enough to earn reading time, short enough to be finished.
- The read-ratio test: every section must survive "would a reader stop here?" Cut the section that answers a question nobody asked.
- Formatting: meaningful subheads, short paragraphs, one idea each; images and diagrams where they carry information. Medium's editor rewards clean typographic flow — no markdown-header spam.
- Personal experience is structural, not decorative: what you ran, what broke, what you measured. This is also the anti-AI signal editors look for.

### Tags and Profile

- Three specific tags beat five broad ones (Medium allows five; the measured advice is three that name the niche). `LangGraph` competes with hundreds; `AI` competes with millions.
- Profile completeness measurably affects follow-through: specific focus areas in the bio, external links, same headshot as your other platforms.

### Publications — the Actual Lever

- Getting into a Boost-enabled niche publication dramatically outperforms self-publishing: their followers + editor nominations + algorithmic amplification.
- Pitch process: read the publication's submission guide, submit 1–2 strong drafts, follow their formatting rules exactly. Editors reject on craft violations before content.
- The 90-day shape that works: publish 3–5 stories in a Boost-enabled publication tied to current developments, aggressively test titles → track CTR, read ratio, and reading time, double down on what works → pitch a recurring column or apply for Boost nomination access.
- Being a good citizen counts: thoughtful responses on top writers' stories in your niche put your name in front of the editors who nominate.

### What Dies on Medium

- AI-shaped prose — policy violation, not just a reach penalty (see above).
- Curiosity-gap clickbait ("You Won't Believe…", "The One Thing…") — high CTR, terrible completion; the reading-time economics punish it automatically.
- Recycled listicles with no lived detail — the 400th "10 Habits of Great Developers" earns neither Boost nor search.
- Hustle-culture and generic motivation — the paying-member audience is working professionals; they pay to skip that.
- Engagement-bait endings ("Clap if you agree! Follow for more!") — claps bought this way don't move reading time, and curators read endings.

### Responses (Comments)

- Responses are mini-stories — they have their own URL and can be distributed. 2–5 substantive sentences with a specific experience is the register.
- Respond to responses on your own stories; highlights + response threads feed the engagement metrics that pay you.
- Thoughtful responses on big stories in your niche are a legitimate discovery channel (profile clicks from readers and — more valuable — editors).

### Timing and Cadence

- Timing matters less than on velocity platforms: Boost and search are not clock-driven. Weekday US mornings help the first-day follower bump, nothing more.
- Cadence: 1–2 well-made stories a week beats daily output — every piece below your bar dilutes the profile editors evaluate you by.

### Pre-Publish Checklist

- [ ] Headline states a debatable claim; CTR plan: check at 48h, rewrite if under ~3%
- [ ] All four legs present: claim / recent proof / named specifics / actionable takeaway
- [ ] 1,500–2,500 words; every section survives the "would they stop here?" test
- [ ] Written from lived experience — zero AI-detection markers (run `content-voice` kill-list)
- [ ] Three specific tags naming the niche, not the category
- [ ] Submitted to a Boost-enabled publication if you have access; formatted to their guide
- [ ] Paywall decision deliberate: strongest work paywalled, discovery pieces free
- [ ] Subtitle states the payoff; cover image set
- [ ] Ready to respond to responses in the first days
- [ ] The piece would survive a human editor asking "what here could only this author have written?"

## Examples

### Example 1: Four-legs check applied

Draft headline: `Thoughts on AI Coding Assistants`

Fails leg 1 (no claim), leg 2 (no recency), leg 3 (nothing named), leg 4 (no takeaway). Rewrite:

> Headline: Claude Code Wrote 80% of Our Sprint. Here's the Review Process That Made It Safe
> Kicker: A working checklist after six weeks and one production incident

Claim (it can be safe), recency (six weeks, current tool), specifics (named tool, a percentage, an incident), takeaway (the checklist). Same knowledge, publishable shape.

### Example 2: Completion-ratio thinking

A 4,000-word "everything about vector databases" draft has a 40%-completion destiny — readers get their answer in section two and leave. Split it: one 1,800-word story per real question ("Why your RAG recall drops at 100k documents", "pgvector vs a dedicated store: the numbers that matter under 1M rows"). Each gets finished; finished is what pays.

### Example 3: Response that earns a profile visit

On a story about prompt engineering costs:

> We measured this across a 40-person team last quarter — the surprise wasn't token cost, it was review time. Engineers spent 3× longer reviewing AI code they didn't write than code they did. The "cheap" generation was the expensive part.
>
> Curious whether you saw review time move too, or just tokens.

Specific numbers, extends the author's point with a new angle, ends with a real question. This is the shape editors and authors click through on.

## References

- AgentSkills spec: https://agentskills.io/specification
- Medium Partner Program terms + AI policy: https://help.medium.com/hc/en-us (policy hardened 2024→2026; verify current text before advising on paywall/AI questions)
- Boost program: https://blog.medium.com/boosting-the-boost-d983f0552ab9
- Measured figures (CTR bands, four legs, reading-time economics, nomination rates): from a 2026 practitioner report by the editor of Medium's largest AI/ML publication, corroborated by 2026 platform studies. Directional — re-validate periodically.
- Companion skill: `content-voice` — on Medium, AI-shaped prose is a policy violation, not just a style problem
