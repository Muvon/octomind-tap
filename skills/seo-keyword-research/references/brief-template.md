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
- Question-format keywords: [list — map to sections that answer them clearly; Google says no special AI phrasing or chunking is needed]
- Definition keywords: [list]
- Comparison keywords: [list]
- AI-Overview presence detected on: [list with evidence source — screenshot / Search Console / SERP tool; else "unverified"]
- Reddit-dominated SERPs: [list — community engagement is the play, not just publishing]
- Bing-priority queries: [list — Bing's index feeds Copilot and, historically, ChatGPT search]

## Algorithmic Risk Notes
- "Best [thing] [year]" listicle keywords flagged as site-reputation risk: [list — third-party sections on Forbes/CNN-style publishers may dominate; assess realism conservatively]
- Helpful-Content-System risk areas: [list — keywords where the only winning angle requires original data the user does not have]
- AI-Overview cannibalization risk: [list — informational queries with persistent AIO; expect a large organic CTR drop even at rank 1]

## Existing-Content Audit
- Cannibalization flags: [keyword X is targeted by both /page-A and /page-B — pick one, redirect or distinguish intent]
- Page-2 quick wins from GSC: [keyword + URL + current position; usually a 200-word section addition or H2 alignment lifts to top 10 within 4–8 weeks]

## Open Items (downstream concerns — owned by other domains)
- Content briefs per P0 keyword
- Internal link map (pillar ↔ cluster pages)
- On-page schema (Article, Product, Organization) + meta tag wiring — FAQ/HowTo no longer earn Google rich results
- GEO content optimization (clear answers, information gain, crawlable text)
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

## Worked example: SaaS, mid-authority, finds quick wins

Profile: open-source self-hosted CRM; small B2B sales teams (2–10 reps) wanting data ownership; DR 28; 14 blog posts, mostly product-feature explainers; SaaS (free open source + paid managed hosting tier); global English.

Stage 2 seeds (pulled in parallel from product nouns + Search Console queries + competitor gap): self-hosted CRM, open source CRM, CRM data ownership, lightweight CRM, simple CRM, CRM for small teams, CRM alternative, CRM without subscription, CRM under $X, GDPR compliant CRM, [competitor] alternative, [competitor] vs [user product].

Stage 4 qualification (sample):

| Long-tail | Vol | KD | SERP realism | Top-10 gap | Verdict |
|---|---|---|---|---|---|
| self-hosted CRM for sales teams under 10 | 70 | 14 | top-10 avg DR 22, half are forum threads | yes — no proper article | P0 |
| Hubspot alternative open source self-hosted | 320 | 28 | top-10 avg DR 38, 2 generic listicles | yes — listicles are 2024, missing self-hosted angle | P0 |
| how to migrate from Hubspot to self-hosted CRM | 40 | 12 | top-10 avg DR 24, mostly Reddit + GitHub issues | yes — no how-to exists | P0 |
| best CRM software | 22,000 | 78 | top-10 avg DR 78, all incumbents | none | strike (head term, unwinnable) |
| CRM | 90,000 | 95 | branded + Wikipedia + incumbents | none | strike (head term + branded) |
| GDPR compliant CRM for European startups | 50 | 18 | top-10 avg DR 31, two are abandoned | yes — recent regulation angle | P1 |
| CRM Docker compose | 0 (tool) | n/a | 4 GitHub issues + 2 blog posts in top 10 | yes — no tutorial | P1 (zero-volume, real demand) |

Stage 5 clustering (excerpt):

- Pillar: "Self-hosted CRM: complete guide" (target keyword "self-hosted CRM" — KD 38, target month 4–6)
- Cluster pages (P0 / P1):
  - "Self-hosted CRM for sales teams under 10" (P0)
  - "Hubspot alternative: open source self-hosted CRMs ranked" (P0)
  - "How to migrate from Hubspot to a self-hosted CRM" (P0)
  - "GDPR-compliant CRM options for European startups" (P1)
  - "Self-hosted CRM with Docker compose: 30-min setup" (P1)

Stage 6: brief per the template above. Internal-link map noted as a downstream task; on-page wiring, schema, and outreach handed to other domains.
