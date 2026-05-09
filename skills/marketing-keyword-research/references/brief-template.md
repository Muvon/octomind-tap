# Keyword Brief Template

Canonical output format for Stage 6. Fill every section; mark "n/a" only when genuinely inapplicable.

```markdown
# Keyword Research Brief: [Site / Topic]

## Site Profile
- Niche: [one sentence]
- Audience: [specific segment]
- Current DR / authority: [estimate]
- Existing topical coverage: [summary]
- Commercial position: [informational / SaaS / e-commerce / local-services / affiliate]
- Geo + language: [scope]

## Method Notes
- Seed sources used: [list — product nouns, problem phrases, GSC mining, competitor gap, etc.]
- Tools used: [Ahrefs / SE Ranking / Serpstat / SEMrush / GSC / Lowfruits / free-only]
- Total candidates evaluated: [N]
- Survived qualification: [N]

## Priority Keywords

### P0 — Quick wins (ship first month)
| Keyword | Volume | KD (tool) | SERP realism | Intent | GEO | AIO present? | Content type | Cluster |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### P1 — High value (next sprint)
| Keyword | Volume | KD | SERP realism | Intent | GEO | AIO present? | Content type | Cluster |
|---|---|---|---|---|---|---|---|---|

### P2 — Cluster fillers
| Keyword | Volume | KD | SERP realism | Intent | GEO | AIO present? | Content type | Cluster |
|---|---|---|---|---|---|---|---|---|

### P3 — Monitor
| Keyword | Reason for deferral | Re-evaluate when |
|---|---|---|

## Topical Clusters

### Cluster 1: [Pillar topic]
- Pillar: [pillar keyword] — volume, KD, content type, target month
- Entity coverage: [list of named entities / sub-topics that the pillar must cover for topical authority]
- Cluster pages:
  - [long-tail 1] — volume, KD, intent, content type
  - [long-tail 2] — volume, KD, intent, content type
  - [...]

### Cluster 2: [Pillar topic]
[...]

## GEO Notes
- Question-format keywords: [list — earn AI citations when written answer-first with extractable passages]
- Definition keywords: [list]
- Comparison keywords: [list]
- AI-Overview presence detected on: [list — flag for the GEO content optimization downstream]
- Reddit-dominated SERPs: [list — community engagement is the play, not just publishing]
- Bing-Webmaster-Tools-priority queries: [list — ChatGPT visibility uses Bing's index]

## Algorithmic Risk Notes
- "Best [thing] [year]" listicle keywords flagged as Site-Reputation-Abuse risk: [list — Forbes/CNN-style brand pages may dominate; assess realism conservatively]
- Helpful-Content-System risk areas: [list — keywords where the only winning angle requires original data the user does not have]
- AI-Overview cannibalization risk: [list — informational queries with persistent AIO; expect 30–40% organic CTR drop even at rank 1]

## Existing-Content Audit
- Cannibalization flags: [keyword X is targeted by both /page-A and /page-B — pick one, redirect or distinguish intent]
- Page-2 quick wins from GSC: [keyword + URL + current position; usually a 200-word section addition or H2 alignment lifts to top 10 within 4–8 weeks]

## Open Items (downstream concerns — owned by other domains)
- Content briefs per P0 keyword
- Internal link map (pillar ↔ cluster pages)
- On-page schema (FAQ, Article, HowTo) + meta tag wiring
- GEO content optimization (extractable passages, FAQ schema, answer-first structure)
- Backlink prospecting for pillar pages (especially those competing in DR > user DR + 15)
- AI search visibility tracking setup (Profound / Otterly / AthenaHQ / Peec) for the GEO-flagged keywords
- Bing Webmaster Tools sitemap submission (if not already done)
```

## Field definitions

| Field | What it captures |
|---|---|
| Volume | Monthly search volume from the chosen tool. Note "0 (real)" for zero-volume kept via Reddit/PAA validation. |
| KD (tool) | Tool-reported difficulty score. Treat as a starting estimate, not a verdict. |
| SERP realism | 1–5 score from Stage 4 — how beatable the actual top 10 are vs the user's DR. |
| Intent | informational / navigational / commercial / transactional. |
| GEO | Question / Definition / Comparison / List / None — drives AI-citation potential. |
| AIO present? | Yes/No — Google AI Overview detected on the SERP. If Yes, expect organic CTR drag even at rank 1. |
| Content type | Blog post / Pillar page / Comparison / Listicle / Case study / Tutorial / Glossary / Tool page. |
| Cluster | The pillar this keyword sits under, or "standalone" if no cluster fit. |
