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

# GEO & AI Citation Optimization

## Overview

AI search engines (ChatGPT, Perplexity, Google AI Overviews) don't rank pages — they **cite** them. Two disciplines layer on top of traditional SEO:
- **AEO** (Answer Engine Optimization) — getting cited in Google AI Overviews
- **GEO** (Generative Engine Optimization) — getting cited in ChatGPT, Perplexity, Gemini, Claude, Copilot

AI-referred traffic is growing +527% YoY with 4.4x higher conversion rates than standard organic. But 97% of AI Overview citations come from pages already in the top 20 organic results — traditional SEO remains the foundation, GEO layers on top.

---

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

1. **Direct response** — answer the question immediately, don't bury the answer
2. **Numerical data** — specific numbers, percentages, statistics get cited more
3. **Authoritative quotations** — expert quotes with named attribution and credentials
4. **Extractable structure** — clear headings, lists, tables that AI can parse
5. **Original expertise** — first-hand experience, unique insights, proprietary data
6. **Technical infrastructure** — schema markup, proper crawl access, fast loading
7. **Fresh content** — AI-surfaced URLs are 25.7% fresher than traditional search results

### Content Structure Rules

**Answer-first sections**
Lead every section with the key takeaway in 1–2 sentences, then elaborate. 44.2% of all AI citations come from the first 30% of text. If an AI engine reads only the first sentence of each section, the reader should still get the full answer.

**Extractable passages (~150 words)**
Each major point should be a self-contained 134–167 word unit that works as a standalone answer. If someone read only that paragraph, they'd get the complete answer.

**Data density**
At least one concrete number, percentage, or statistic per major section. Numerical data gets cited more. Flag data-free sections.

**FAQ sections**
Include a FAQ for informational and commercial intent pages. Pages with FAQ sections are 2.8x more likely to be cited in AI answers. Each answer: 2–4 sentences, direct and self-contained.

**Listicle format for commercial keywords**
100–200 word overviews per item, "Best For" tags, 3–4 pros, 2–3 cons, pricing indication. Listicles are the #1 AI-cited format (21.9% of all citations). Each item must work as a standalone answer.

**Semantic completeness**
Cover topics comprehensively from multiple angles. Content scoring 8.5/10+ on semantic completeness is 4.2x more likely to be cited. Depth over breadth.

**E-E-A-T amplification**
Author bylines with real credentials, first-hand examples, expert quotes with attribution, citations to reputable studies. AI engines apply multi-source corroboration before citing.

---

### Schema Markup

Pages with comprehensive JSON-LD schema are 2–3x more likely to be cited by AI. Apply in order of impact:

**1. FAQ Schema** — highest single impact, directly extracted by AI:
```json
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"...","acceptedAnswer":{"@type":"Answer","text":"..."}}]}
```

**2. Article Schema** — establishes content authority:
```json
{"@context":"https://schema.org","@type":"Article","headline":"...","author":{"@type":"Person","name":"..."},"datePublished":"...","dateModified":"...","description":"..."}
```

**3. HowTo Schema** — cited for procedural queries:
```json
{"@context":"https://schema.org","@type":"HowTo","name":"...","step":[{"@type":"HowToStep","name":"...","text":"..."}]}
```

**4. Organization Schema** — builds entity recognition:
```json
{"@context":"https://schema.org","@type":"Organization","name":"...","url":"...","logo":"...","sameAs":["..."]}
```

Always use JSON-LD (not microdata). Apply all applicable schemas together for maximum citation probability.

---

### AI Crawler Setup

**robots.txt** — allow AI search bots (they cite and link back):
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

**Bing Webmaster Tools** — submit sitemap to Bing, not just Google Search Console. Critical for ChatGPT visibility.

**llms.txt** — emerging standard for AI crawlers. Low adoption (~10% of domains), no proven citation impact yet. Nice to have, not critical.

---

## Examples

### Answer-first section (correct)

> **Why answer-first structure matters**
> AI engines extract opening sentences first — 44.2% of citations come from the first 30% of text. Writing the key takeaway at the start of every section maximises the chance of being cited, and also makes the content easier for human readers to scan.

### Answer-first section (wrong)

> **Why answer-first structure matters**
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
