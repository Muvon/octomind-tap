---
name: content-geo
title: "GEO & AI Citation Optimization"
description: "Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) patterns for getting content cited by AI search engines. Answer-first structure, schema markup, extractable passages, and crawler setup."
license: Apache-2.0
compatibility: "Octomind content agents."
domains: content
rules:
  - content(seo)
  - content(geo)
  - match(\b(rank|ranking)\s+(in|on)\s+(google|search|serps?)\b)
  - match(\bschema\.org\b)
  - match(\bmeta\s+(description|title|tags?)\b)
  - match(\bserps?\b)
  - match(\bai\s+overview\b)
  - match(\b(llm|ai)\s+citation\b)
  - match(\bgenerative\s+engine\s+optimization\b)
  - match(\bsearch\s+engine\s+optimization\b)
---

## Overview

AI search engines (ChatGPT, Perplexity, Google AI Overviews) don't rank pages — they cite them. Two disciplines layer on top of traditional SEO:
- AEO (Answer Engine Optimization) — getting cited in Google AI Overviews
- GEO (Generative Engine Optimization) — getting cited in ChatGPT, Perplexity, Gemini, Claude, Copilot

AI-referred traffic is growing +527% YoY with 4.4x higher conversion rates than standard organic. But 97% of AI Overview citations come from pages already in the top 20 organic results — traditional SEO remains the foundation, GEO layers on top.

### The 2026 zero-click reality (why GEO matters now, not later)

- 64.82% of all Google searches end without a click (up from 50% in 2019).
- On AI-Overview-triggered queries the zero-click rate jumps to ~83%.
- In Google's AI Mode, 93% of searches end without a single click to any external site.
- Pew Research field study: organic CTR drops -46.7% (15% → 8%) when AI Overviews appear.
- Seer Interactive: organic CTR -61% on triggered queries (1.76% → 0.61%).
- Search Engine Journal-cited field study: outbound organic clicks -38% on AI-Overview queries, with zero-click rising from 54% to 72%, effects strongest when AIO appears at the top.

The new primary metric is **citation share** — how often your brand appears as a source inside the generative answer — not blue-link rank. Tools tracking citation frequency, share of voice, and AI referral traffic: Otterly.ai, Semrush AI Toolkit, Ahrefs Brand Radar, Rankability. Probe manually too: 10 fixed niche queries logged monthly across ChatGPT / Perplexity / Claude / Gemini reveals citation drift early.

## Instructions

### Platform Differences

| Platform | Source | Key fact |
|---|---|---|
| Google AI Overviews | Google's own top-20 organic results | Tightly coupled to traditional SEO |
| ChatGPT | Bing's index | Only ~14% overlap with Google top-10. Bing matters. |
| Perplexity | Real-time web search | Correlates with Google top-10 results 91% of the time |

ChatGPT accounts for 87.4% of all AI referral traffic — Bing Webmaster Tools submission is critical.

### The Seven Pillars of GEO

Combining these improves AI visibility by 30–40%:

1. Direct response — answer the question immediately, don't bury the answer
2. Numerical data — specific numbers, percentages, statistics get cited more
3. Authoritative quotations — expert quotes with named attribution and credentials
4. Extractable structure — clear headings, lists, tables that AI can parse
5. Original expertise — first-hand experience, unique insights, proprietary data
6. Technical infrastructure — schema markup, proper crawl access, fast loading
7. Fresh content — AI-surfaced URLs are 25.7% fresher than traditional search results

### Information Gain (2026 ranking gate)

Every piece must add something the top 10 results don't already say. Google's 2026 systems reward novel contribution; generic summaries get demoted as AI-derivable filler.

Before drafting, identify the gain:
- Original data, survey, internal benchmark, or measurement
- First-hand case study with specifics (numbers, screenshots, timestamps)
- Contrarian take supported by evidence
- Synthesis across sources nobody else has combined
- Practitioner detail the ranking pages skip (edge cases, gotchas, real cost)

If the draft could be reconstructed by an LLM reading the top 10 alone, it has no information gain. Send it back to research, not to publish.

### Experience signals (the "E" Google amplified in 2026)

Google's March 2026 core update (rolled out March 27 → April 8) made first-hand Experience outweigh comprehensive-but-impersonal content. The update's measured impact: 80% of top-3 results shifted, nearly 1 in 4 top-10 pages fell out of the top 100, and **73% of post-update YMYL top results now display detailed author credentials** (up from 58% before the cycle). Visibility flowed to primary sources, official institutions, and specialist publishers — and away from intermediary "list/aggregator" pages that rephrase the existing top results without adding original signal. Bake at least one of these into every article that allows it:

- "From the Field" block — original photos, screenshots (blur sensitive data), short video, or a captioned step-through of the team actually doing the thing
- Time-boxed case study framing — "I tried this for 30 days", "We ran this for one quarter across 12 clients", "Here's the dashboard at week 6"
- Named-tool specifics — exact versions, exact settings, exact error messages encountered, not abstracted summaries
- Failure honesty — what didn't work, what we'd do differently, where the data is mixed

Stock photos, AI-illustrated heroes, and "Admin" bylines actively work against this. Every article needs a real human author with credentials, bio, and outbound LinkedIn/publication link.

### Content Structure Rules

Answer-first sections
Lead every section with the key takeaway in 1–2 sentences, then elaborate. 44.2% of all AI citations come from the first 30% of text. If an AI engine reads only the first sentence of each section, the reader should still get the full answer.

Featured snippet block (40–50 words after each H2)
Immediately after each H2, place a tight 40–50 word direct answer to the heading's question. This is the unit Google extracts for Position Zero and the unit AI Overviews quote verbatim. It sits before the longer ~150-word elaboration. Make it self-contained — no "as discussed above", no pronouns referring to earlier sections.

Extractable passages (~150 words)
Each major point should be a self-contained 134–167 word unit that works as a standalone answer. If someone read only that paragraph, they'd get the complete answer.

Voice-search H2s
Phrase H2s the way users actually speak the query, not the way SEO tools rank tokens. "What is topical authority?" beats "Topical Authority". "How to set up FAQ schema" beats "FAQ Schema Setup". Voice/AI assistants match conversational phrasing.

Data density
At least one concrete number, percentage, or statistic per major section. Numerical data gets cited more. Flag data-free sections.

FAQ sections
Include a FAQ for informational and commercial intent pages. Pages with FAQ sections are 2.8x more likely to be cited in AI answers. Each answer: 2–4 sentences, direct and self-contained.

Listicle format for commercial keywords
100–200 word overviews per item, "Best For" tags, 3–4 pros, 2–3 cons, pricing indication. Listicles are the #1 AI-cited format (21.9% of all citations). Each item must work as a standalone answer.

Semantic completeness
Cover topics comprehensively from multiple angles. Content scoring 8.5/10+ on semantic completeness is 4.2x more likely to be cited. Depth over breadth.

E-E-A-T amplification
Author bylines with real credentials, first-hand examples, expert quotes with attribution, citations to reputable studies. AI engines apply multi-source corroboration before citing.

### Schema Markup

Pages with comprehensive JSON-LD schema are 2–3x more likely to be cited by AI. Apply in order of impact:

1. FAQ Schema — highest single impact, directly extracted by AI:
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```

2. Article Schema — establishes content authority:
```json
{"@context":"https://schema.org","@type":"Article","headline":"...","author":{"@type":"Person","name":"..."},"datePublished":"...","dateModified":"...","description":"..."}
```

3. HowTo Schema — cited for procedural queries:
```json
{"@context":"https://schema.org","@type":"HowTo","name":"...","step":[{"@type":"HowToStep","name":"...","text":"..."}]}
```

4. Organization Schema — builds entity recognition:
```json
{"@context":"https://schema.org","@type":"Organization","name":"...","url":"...","logo":"...","sameAs":["..."]}
```

5. Person/Author Schema — author authority is now a ranking signal. Every byline needs credentials and outbound links:
```json
{"@context":"https://schema.org","@type":"Person","name":"...","jobTitle":"...","worksFor":{"@type":"Organization","name":"..."},"sameAs":["https://linkedin.com/in/...","https://twitter.com/..."],"alumniOf":"...","knowsAbout":["..."]}
```

6. Review / AggregateRating Schema — for any page that hosts user reviews, product comparisons, or testimonials. Drives star displays in SERPs and is consumed directly by AI Overviews to assess brand sentiment:
```json
{"@context":"https://schema.org","@type":"AggregateRating","ratingValue":"4.7","reviewCount":"312","bestRating":"5"}
```

Always use JSON-LD (not microdata). Apply all applicable schemas together for maximum citation probability.

### Helpful Content System — continuous, not occasional

The Helpful Content Update was folded into the main core ranking algorithm; in 2026 it is a **continuous real-time signal**, not a periodic refresh. There is no longer a "recovery window" to wait for — every change is evaluated as it indexes. Practical implication: don't ship content that fails the information-gain test "for now and refresh later" — Google sees the same demotion signal the day it goes live.

### Site Reputation Abuse — algorithmic since August 2025

What started as a manual-action-only policy in March 2024 became fully algorithmic with the August 2025 Spam Update. Google now detects when a section of a site is topically independent from the parent domain and treats it as a separate entity — stripping the parent's authority transfer. The lifespan of a spammy "parasite" page on a high-DA host has dropped from ~9 months to **6–8 weeks**. Treat any "rank by riding a DA-90 host's authority" idea as both unethical and short-lived; pitch placements only where the topical fit is genuine.

### AI Crawler Setup

robots.txt — allow AI search bots (they cite and link back):
```
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
```
Training crawlers (GPTBot, Google-Extended) are optional — they train models but don't cite.

Bing Webmaster Tools — submit sitemap to Bing, not just Google Search Console. Critical for ChatGPT visibility.

llms.txt — emerging standard for AI crawlers. Low adoption (~10% of domains), no proven citation impact yet. Nice to have, not critical.

## Examples

### Answer-first section (correct)

> Why answer-first structure matters
> AI engines extract opening sentences first — 44.2% of citations come from the first 30% of text. Writing the key takeaway at the start of every section maximises the chance of being cited, and also makes the content easier for human readers to scan.

### Answer-first section (wrong)

> Why answer-first structure matters
> When we look at how AI search engines process content, we can see that there are many factors at play. Researchers have studied this extensively. The way content is structured plays an important role...

### FAQ block (citable format)

```json
{
  "@type": "Question",
  "name": "How long should an extractable passage be?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "134–167 words. Each passage should work as a standalone answer — if someone read only that paragraph, they'd get the complete answer without needing surrounding context."
  }
}
```
