---
name: marketing-keyword-research
title: "Long-Tail Keyword Research — Low-Competition Discovery"
description: "Operational funnel for discovering high-intent, low-competition long-tail keywords (4+ word phrases with weak SERP defenders) — the keyword class that actually ranks for new and mid-authority sites without massive backlink spend. Encodes the discovery method (seed → modifier expansion → Google autocomplete + 'People Also Ask' + Reddit/forum mining + competitor SERP-gap), the qualification rubric that goes beyond KD scores (top-10 SERP authority profile, content-fit gap, intent match, traffic-potential vs ranking-realism, query freshness), the 2026 GEO overlay (definition + question + comparison queries that earn AI-search citations), and the kill-rules (head-term traps, fake-volume keywords, branded-SERPs, paid-ads-dominated SERPs). Use BEFORE writing any content brief, calendar, or pillar-cluster plan. Stays in the marketing lane: produces a keyword brief — content writing, on-page wrapping, and link-building belong to other domains."
license: Apache-2.0
compatibility: "Stack-agnostic. Free path requires websearch + webfetch (Google autocomplete, 'People Also Ask' scrape, Reddit search, competitor SERP review). Optional MCP data sources: Ahrefs, SE Ranking, Serpstat, Google Search Console for volume + KD numbers."
domains: marketing
rules:
  - session(seo)
  - content(keyword)
  - content(keywords)
  - content(longtail)
  - content(SERP)
  - match(\blong[\s-]?tail\b)
  - match(\bkeyword\s+(research|ideas?|opportunit\w+|gap|gaps|cluster\w*|map\w*)\b)
  - match(\blow[\s-](competition|comp|kd|difficulty)\s+keyword\w*)
  - match(\b(zero|low)[\s-]?volume\s+keyword\w*)
  - match(\bsearch\s+(intent|volume|demand)\b)
  - match(\bpeople\s+also\s+ask\b)
  - match(\bseed\s+keyword\w*)
  - match(\b(serp|serps)\s+(analy\w+|gap|review)\b)
  - match(\bcontent\s+(gap|brief|calendar|cluster\w*)\b)
  - semantic(find low competition keywords we can actually rank for)
  - semantic(long tail keyword opportunities for our niche)
  - semantic(what should we write about to rank without backlinks)
  - semantic(keyword research focused on easy wins not head terms)
  - semantic(SERP gap analysis for content opportunities)
---

## Overview

Most keyword research dies at the head term. A site with DR 25 chasing "project management software" (KD 72) loses to Asana and Monday.com forever — but the same audience also searches "free task tracker for two-person agencies" (KD 8, weak SERPs, transactional intent) and that's the keyword class that converts on month-three traffic instead of year-three. This skill is the funnel that finds those keywords reliably: it forces the seed → modifier expansion → SERP-mined patterns → competitor-gap pass, then qualifies survivors against a SERP-authority rubric that beats raw KD scores, and outputs a prioritized brief mapped to content types and intent.

Use BEFORE any content brief, calendar, or pillar-cluster plan. The deliverable is a keyword brief; writing, on-page wrapping, schema, and link-building are out of scope and belong to other domains.

## Mental model

Long-tail wins on three compounding axes that head-term chasing loses:

1. SERP authority profile beats KD score. KD is a dumb average — what matters is whether the actual top-10 are beatable. A "KD 35" keyword with three 1,500-word generic AI posts on top is more winnable than a "KD 18" keyword where the top 3 are a Wikipedia page, a 5-year-old definitive guide, and the official product page.
2. Intent specificity is the conversion lever. "[head term]" attracts everyone; "[head term] for [audience] under [constraint]" attracts only buyers. A 100-volume long-tail with 8% conversion beats a 10,000-volume head term with 0.2%.
3. Long-tail clusters earn topical authority. Five 200-volume long-tails covering the same sub-topic, internally linked to a pillar, signal expertise more than one head-term page. The Helpful Content System (folded into core algorithm 2024) and information-gain scoring both reward depth, original data, and entity-coverage breadth — not surface listicles.

The funnel below operationalizes those three axes. Skip any stage and you're back to keyword-research-as-brainstorm — picking what feels obvious, missing what's winnable.

### 2026 algorithmic context (kill-rules upstream of the funnel)

| Reality | Implication for keyword selection |
|---|---|
| Helpful Content System is core algorithm | Topical depth and original perspective beat breadth. Generic AI-summary content is actively suppressed; pick keywords where your unique angle / data / experience fills a gap. |
| Information-gain reward (Google patent + observable behavior) | New content needs to add something the existing top 10 doesn't have. If you can't articulate the new info, the keyword isn't yours yet. |
| Site Reputation Abuse update (Aug 2024, expanded) | "Best [X] [year]" listicles on Forbes / CNN / Times brand pages now rank artificially. Score realism conservatively on these SERPs unless the user has DR ≥ 50 or a niche-brand-page play. |
| AI Overview proliferation (~30% of informational SERPs in 2026) | Even at rank 1, expect 30–40% organic CTR drop on AIO-saturated queries. Either weight transactional / commercial-investigation higher, or write to win the AI citation (extractable answer + schema) instead of the click. |
| Brand search volume now outweighs backlinks as an LLM-citation predictor | Long-term: brand-building keywords (your-brand + modifier) become a defensive cluster. Short-term: long-tails still convert. |
| Reddit / community SERPs are now load-bearing for AI citations (~40% of LLM citations) | When the top 5 organic results are Reddit threads, the keyword is community-owned — engage there in parallel with publishing. |

## Instructions

### Core rules

- Long-tail = 4+ words OR a clear intent-specific modifier on a head term. "Best CRM" is short-tail. "Best CRM for solo financial advisors" is long-tail. The shift to specificity is what matters, not raw word count.
- SERP review is non-negotiable. For every keyword that survives expansion, look at the actual top 10. KD scores from any tool (Ahrefs, SEMrush, SE Ranking, Serpstat) are a starting estimate, not a verdict. The SERP tells you whether the keyword is beatable for THIS site.
- Realism rule (heuristic, not gospel): target keywords where the top-10 average DR is roughly within +15 of your DR. A DR-25 site can credibly rank against DR-10 to DR-40 sites; chasing keywords where the top 10 average DR 60+ is a multi-year project, not a quick win. Adjust the +15 band by content-quality gap (top-10 are weak/old → push higher; top-10 are definitive → push lower).
- Information gain is the on-page kill rule. If you cannot name what the new piece adds that the top 10 doesn't have (data, perspective, structure, freshness), the keyword isn't yours yet. Picking the keyword without an angle is the same mistake as picking a head term without DR.
- Intent must match the site's commercial position. Informational keywords on a transactional product page = mismatch (won't rank, won't convert). Commercial-investigation keywords on a thin glossary page = mismatch. Always classify intent BEFORE assigning content type.
- Five+ candidates per sub-topic, not one. Single-keyword targeting anchors to whatever came first. Always generate five long-tails per sub-topic and rank — even if four are dead ends, the comparison clarifies why the survivor wins.
- Zero-volume keywords are a real category in 2026. AI-search shifts demand to long-tail queries that traditional volume tools mark "0". A "0-volume" keyword that ranks for 12 related semantic queries can earn 200+ visits/month. Don't auto-strike on volume = 0; check related-keyword overlap.
- GEO is not a separate discipline anymore — it's the second axis of every modern keyword. Definition / question / comparison / list queries that produce extractable answers earn AI-search citations even when traditional rank is mid-page. Note GEO potential per keyword; the on-page execution (answer-first, FAQ schema, extractable passages) is owned by another domain.
- Output a brief, not a verdict. The deliverable is a written keyword brief covering: prioritized list, intent + content-type mapping, cluster grouping, entity-coverage notes, and content-calendar slot. Writing, schema, internal-link wiring, and outreach belong to downstream domains.
- Compound over spike. Prefer evergreen long-tails (definitions, how-tos, tool-fit comparisons) over trend-cycle keywords. A 2026-trend keyword decays in 12 months; "how to [permanent task]" compounds for years.

### The funnel

#### Stage 1 — Profile the site (kill or proceed)

Force concrete answers before generating any keyword list. If unclear, stop and ask.

1. Niche — one sentence. Sub-niche if applicable.
2. Audience — who actually buys/converts? Specific segment, not "small businesses."
3. Current DR / authority — rough estimate (Ahrefs free tool, Moz Link Explorer, or "we're new"). This sets the realism cap.
4. Existing content — count and topical coverage. New site = greenfield. Existing site = check what already ranks (Search Console queries) before generating overlap.
5. Commercial position — informational/affiliate/SaaS/e-commerce/local-services. Determines which intent classes to prioritize.
6. Geographic + language targeting — global English, US-only, multi-region, non-English. Affects SERP review and modifier set.

If the user can't name DR or commercial position, kill the engagement at this stage. Without those, qualification is blind: "I'd be guessing whether the top 10 are beatable. Get a DR estimate (Ahrefs free Backlink Checker takes 30 seconds) and tell me what conversion looks like, then I'll run the funnel."

#### Stage 2 — Generate seed keywords (parallel)

PARALLEL-FIRST: fire all seed sources simultaneously in ONE block. Don't serialize.

Seed sources:

- Core product/service nouns — what the site actually sells, in the language buyers use (not internal jargon).
- Problem-focused phrases — "[problem] when [context]", "[symptom] in [audience]", "stop [bad thing]".
- Solution-focused phrases — "how to [task]", "[task] without [obstacle]", "alternative to [incumbent]".
- Audience qualifiers — "[product] for [audience segment]", "[product] for [team size]", "[product] for [use case]".
- Industry / vertical terms — terminology specific to the buyer's world.
- Existing-content mining — Search Console "queries" report → keywords already pulling impressions on existing pages but ranking page 2–5. Each is a seed for related long-tails.
- Competitor SERP gaps — pick 3 competitors at the same DR tier; pull their top-200 ranking keywords (Ahrefs Site Explorer / SE Ranking competitor research / SEMrush Domain Overview); filter for keywords where the user's site does NOT rank. Each is a seed.

Output of Stage 2: a flat list of 30–80 seed terms. Don't qualify yet — qualification comes after expansion.

#### Stage 3 — Expand to long-tail (modifier patterns + SERP mining)

For each seed, generate 5–15 long-tail variants. Run in parallel; don't expand one seed at a time.

Modifier buckets (full library + SERP-mined sources in `references/modifier-library.md`):

- Question modifiers — `how to`, `what is`, `why`, `when`, `which` × seed. Highest GEO value.
- Intent modifiers — `best`, `top`, `free`, `cheap`, `vs`, `alternative to`, `under $X`. Commercial/transactional layer.
- Constraint modifiers — `for [audience size]`, `for [vertical]`, `in [year]`, `without [obstacle]`, `with [feature]`. Highest-yield for low-DR sites — every constraint kills a competing page.
- Outcome modifiers — `in [time bound]`, `without [obstacle]`, `roi / cost`, `mistakes to avoid`.
- Comparison modifiers — `vs`, `or`, `difference between`, `when to use A vs B`. Mid-funnel + AI-citation-friendly.
- Problem-trigger modifiers — `why is my [thing] broken`, error messages, support-forum phrasings. Highest conversion when product solves the pain.

SERP-mined sources (free, parallel — fire all in one block):

- Google autocomplete (incognito) — type seed + each letter a–z, capture suggestions.
- Google "People Also Ask" — expand 2–3 PAA branches per seed; each yields 3–5 related questions.
- Google "Related searches" — bottom-of-SERP carousel.
- Google Trends "Related queries (rising)" — momentum signals before tools assign volume.
- Reddit / forum mining — `site:reddit.com [seed]` for real user phrasing; Quora, Stack Exchange, niche forums for verticals where Reddit is thin.
- Lowfruits — purpose-built tool for low-competition discovery (identifies SERPs dominated by weak/forum content).
- Glimpse / Exploding Topics — emerging keywords pre-volume.

Output of Stage 3: 200–500 long-tail candidates. Dedup at Stage 4.

#### Stage 4 — Qualify each long-tail (SERP-first rubric)

This is the stage that separates winnable keywords from KD-low-but-unwinnable ones. Walk top-to-bottom; STRIKE on the first failure (it's a kill-rule list, not a score).

| # | Check | How to verify | Strike condition |
|---|---|---|---|
| 1 | Real intent match | Read the search query out loud — what does the searcher actually want? | Mismatch with site's commercial position (e.g. transactional query on an informational site) |
| 2 | Volume realism | Tool estimate (Ahrefs / SE Ranking / Serpstat / SEMrush) + Google Trends sanity check | Volume = 0 AND no related-keyword cluster — pure dead-air keyword |
| 3 | SERP authority profile | Manually inspect top 10. Note: domain DRs, page word counts, content age, brand vs independent | Top-10 average DR > (user DR + 15) AND no obvious content gap |
| 4 | Top-10 content quality | Read 3–5 of the top results. Are they comprehensive, recent, well-structured? | Top results are already definitive (1 perfect Wikipedia, 1 official docs page, 1 5k-word evergreen pillar) |
| 5 | Content-fit gap | Is there a sub-angle the top 10 miss? (specific audience, specific constraint, specific use case) | No gap — every angle is already covered well |
| 6 | Paid ads dominance | Count ads at top of SERP | 4 ads above organic = ad-saturated, organic CTR drops to <20% |
| 7 | AI Overview presence | Search the keyword; AIO present? | AIO present AND keyword is informational AND the user can't write to win the citation (no extractable answer / no schema plan) → expect 30–40% organic CTR drop even at rank 1 |
| 8 | Site Reputation Abuse risk | Are top 3 results brand-page subdomains/folders on Forbes/CNN/Times? | Yes AND user is < DR 50 → demote priority; the SERP is structurally rigged for big-brand pages |
| 9 | Branded SERP | Are top 10 mostly the searcher's own brand-mention candidates? | Yes — searcher wants a specific brand, not a category answer |
| 10 | Featured snippet | Is there a featured snippet? Who holds it? | Featured snippet exists AND holder is DR 70+ AND content is strong — hard to dislodge; if held by a weak page, it's a snippet-steal opportunity |
| 11 | Trend direction | Google Trends 5-year view | Sharp decline trajectory — keyword is dying |
| 12 | Cluster fit | Does this fit a topical cluster already planned, or stand alone? | Stand-alone keyword with no internal-link path — orphan content |

A long-tail that survives all 12 → eligible for the brief. Anything else → strike.

For zero-volume candidates: replace check #2 with "does this keyword appear in 5+ Reddit threads OR show up in PAA / autocomplete?" If yes, it's a real query with no tool data — keep. If no, strike.

#### Stage 5 — Cluster, map entity coverage, prioritize

Group survivors into topical clusters (one pillar + 4–8 cluster pages each), then layer entity-coverage onto each cluster:

1. Identify pillar candidates — broad seed terms with the highest survivor count clustered around them.
2. Group long-tail survivors under their pillar by sub-topic.
3. Map entity coverage per cluster — list the named entities, sub-topics, and related concepts the pillar must cover for topical authority. Source: top-10 ranking pages' H2/H3 structure (n-gram-mine them), Wikipedia "See also" sections for the seed, knowledge-panel related entities. A pillar that misses 3+ of the entities the top-10 all cover signals shallow coverage to ranking systems.
4. Score each survivor on:
   - Realism — top-10 SERP authority profile vs user DR (1 = unwinnable, 5 = clearly beatable)
   - Intent value — informational = 1, navigational = 1, commercial = 2, transactional = 3 (multiply by site's commercial position relevance)
   - GEO potential — definition / how-to / comparison / list = 1 each, none = 0 (max 4)
   - Cluster fit — pillar = 5, primary cluster page = 4, secondary cluster = 3, orphan = 1
   - AIO discount — if AI Overview present on the SERP for an informational keyword AND no plan to win the citation, subtract 2 (CTR floor risk)

   Composite priority = (realism × 3) + (intent × 2) + GEO + cluster_fit − AIO_discount. Range: 9–35.
5. Bucket into:
   - P0 — Quick wins (priority ≥ 28): publish first month
   - P1 — High-value (priority 22–27): queue for next sprint
   - P2 — Cluster fillers (priority 16–21): batch with related pillar
   - P3 — Monitor (priority < 16): not in the next quarter

A long-tail that scores 1 on realism is automatically demoted to P3 regardless of total — don't chase keywords you can't win.

#### Stage 6 — Output the keyword brief

Use the canonical template at `references/brief-template.md`. The brief covers: site profile, method notes, priority keywords (P0–P3 tables with volume / KD / SERP realism / intent / GEO / AIO presence / content type / cluster columns), topical clusters with entity-coverage notes, GEO notes (question / definition / comparison / Reddit-dominated / Bing-priority queries), algorithmic risk notes (Site Reputation Abuse, HCS, AIO cannibalization), existing-content audit (cannibalization, GSC page-2 quick wins), and open items handed to downstream domains (content briefs, internal linking, schema, GEO writing, backlink prospecting, AI search visibility tracking).

The brief is the deliverable. Anything not in the brief — content writing, schema wiring, internal-link execution, outreach copy — is downstream and belongs to other domains.

### Decision guide — common edge cases

| Situation | Action |
|---|---|
| User has no DR estimate and no Search Console access | Kill at Stage 1. Realism check is impossible; ask for an Ahrefs free Backlink Checker number. |
| Top 10 includes a Wikipedia page | Strike — cluster around adjacent long-tails instead. |
| Volume = 0 but Reddit has 12 threads on the question | Keep. Real demand, no tool data. Score realism normally. |
| User pushes head term ("just give me 'project management software'") | Refuse + explain. At user's DR this is a 24-month project. Surface P0 long-tails in the same cluster as the realistic first target. |
| Top 10 are 4+ years old and thin (sub-1000 words) | Quick win. New comprehensive content can leapfrog on freshness + depth. |
| Featured snippet held by DR 70+ with strong content | Strike — unless wrong/incomplete and user can demonstrably do better. |
| AI Overview present on informational SERP | Demote unless user has a citation-win plan (extractable answer + schema). 30–40% CTR drag at rank 1 is the default. |
| Top 3 are Forbes/CNN/Times brand pages on a "best [X] [year]" listicle | Site Reputation Abuse SERP. Demote unless user has DR ≥ 50 or a niche-brand-page play. |
| Ad-saturated SERP (4+ paid ads) | Demote — organic CTR is 15–20%. Pick a less-monetized adjacent long-tail or pay. |
| Non-English market | Re-run Stages 2–4 with native-language seeds; SERP review on the local Google domain. |
| Brand-name terms appear in seeds | Treat separately — brand terms convert at 5–10× organic, but the play is brand defense + comparison content, not generic long-tail. |

### Tools — free vs paid

| Tool | Tier | Use for |
|---|---|---|
| Google Search (incognito) + autocomplete | Free | Seed expansion, SERP review |
| Google Trends | Free | Volume sanity, trend direction, "Related queries (rising)" momentum |
| Google Search Console | Free | Existing query mining, page-2 quick wins, impression data |
| Bing Webmaster Tools | Free | Keyword data + ChatGPT citation potential (ChatGPT uses Bing's index) |
| Ahrefs Free Backlink Checker | Free | DR estimate for site + competitors |
| Moz Link Explorer free | Free (limited) | DA / spam-score estimates |
| Ubersuggest free | Free (limited) | Volume + KD spot checks |
| AlsoAsked / AnswerThePublic free | Free (limited) | PAA / question-modifier expansion |
| Reddit / forums | Free | Real user phrasing, zero-volume validation, AI-citation pre-mining |
| Lowfruits | Freemium | Purpose-built low-competition keyword discovery — flags SERPs dominated by weak/forum content |
| Glimpse / Exploding Topics | Freemium | Emerging keywords pre-volume; momentum signal before tools assign KD |
| SparkToro | Freemium | Audience research — what your buyers actually read/listen-to/follow (informs seed phrasing) |
| Ahrefs / SE Ranking / Serpstat / SEMrush | Paid | Full keyword databases, KD scores, competitor ranking lists, SERP overview |
| Surfer SEO / NeuronWriter / Frase | Paid | TF-IDF / NLP entity coverage — tells you which entities the top-10 cover that you're missing (Stage 5) |
| Profound / Otterly / AthenaHQ / Peec | Paid | AI search visibility tracking — measures share of citation across ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude. The measurement layer for the GEO claims in this brief. |

MCP-wired data sources available in this tap: `serpstat`, `ahrefs`, `seo-data` (SE Ranking), `search-console`. The free path covers the entire funnel for any user who's willing to do SERP review manually. Paid tools save time on volume + KD numbers, competitor gap analysis, and entity-coverage mining; they do NOT replace the manual SERP review in Stage 4.

## Examples

### Example 1: SaaS, mid-authority, finds quick wins

Profile:
- Niche: open-source self-hosted CRM
- Audience: small B2B sales teams (2–10 reps) who want data ownership
- DR: 28
- Existing content: 14 blog posts, mostly product-feature explainers
- Commercial: SaaS (free open-source + paid managed hosting tier)
- Geo: global English

Stage 2 seeds (sample — pulled in parallel from product nouns + Search Console queries + competitor gap):

- self-hosted CRM, open source CRM, CRM data ownership, lightweight CRM, simple CRM, CRM for small teams, CRM alternative, CRM without subscription, CRM under $X, GDPR compliant CRM, [competitor] alternative, [competitor] vs [user product]

Stage 3 expansion (sample of 60 long-tails generated):

- "self-hosted CRM for sales teams under 10"
- "best open source CRM 2026 self hosted"
- "CRM with data export to PostgreSQL"
- "Hubspot alternative open source self-hosted"
- "how to migrate from Hubspot to self-hosted CRM"
- "lightweight CRM for two-person agency"
- "GDPR compliant CRM for European startups"
- "CRM that works offline"
- "free CRM no subscription self-hosted"
- "self-hosted CRM Docker compose"

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

- Pillar: "Self-hosted CRM: complete guide" (target keyword: "self-hosted CRM" — KD 38, target month 4–6)
- Cluster pages (P0 / P1):
  - "Self-hosted CRM for sales teams under 10" (P0)
  - "Hubspot alternative: open source self-hosted CRMs ranked" (P0)
  - "How to migrate from Hubspot to a self-hosted CRM" (P0)
  - "GDPR-compliant CRM options for European startups" (P1)
  - "Self-hosted CRM with Docker compose: 30-min setup" (P1)

Stage 6 brief: produced per template above. Internal-link map noted as a downstream task; on-page wiring + schema + outreach handed to other domains.

### Example 2: New site, no DR — refuse the head term

User: "We just launched. We sell project management software. Find me 50 keywords."

Response:
> Stop. At a brand-new domain (DR ~0–5), 80% of "project management software" keywords are unwinnable for 12+ months. Asana, Monday, ClickUp, Notion own the head + shoulder with decade-old backlink graphs. 50 generic PM keywords would waste your first quarter.
>
> Two questions first:
>
> 1. Who specifically converts that's underserved by the incumbents? Name the segment (e.g., "construction subcontractors with 3–15 person crews", "law firms doing matter management"). Narrower segment = more long-tail surface area.
> 2. What's the 1–2-sentence reason to switch? (Feature gap, pricing model, integration, vertical workflow.) That reason becomes the Stage 3 modifier set.
>
> If "we don't know yet" → positioning is upstream of keyword research. Pick the niche, then run the funnel.

### Example 3: GSC mining for free quick wins

For any site live ≥ 3 months with Google Search Console connected: query GSC for queries with impressions > 100 and average position 8–20 (page 2 — the "quick win" zone). For each candidate, confirm intent matches the existing page (if not, it's a NEW page candidate) and run SERP review to confirm room to climb. Output two streams:

- Existing-page improvements: 200-word section additions + intent-aligned H2 typically lift page-2 to top 10 in 4–8 weeks.
- New-page candidates: queries the existing page ranks for via incidental overlap; a dedicated page outranks the parent.

GSC mining is the highest-ROI single source on this list. Always run it first when GSC is available.

## Checklist

- [ ] Stage 1 site profile captured: niche, audience, DR estimate, existing coverage, commercial position, geo
- [ ] DR / commercial position confirmed before any keyword generation (kill-gate)
- [ ] Seeds generated from ≥ 4 of the 7 source categories (parallel run)
- [ ] Long-tail expansion produced 5–15 variants per seed using the modifier library
- [ ] SERP review completed manually for every candidate that survives volume + intent filter (rubric step #3)
- [ ] Realism rule applied: top-10 average DR within ~+15 of user DR (banded by content-quality gap)
- [ ] AIO presence checked per keyword; informational keywords with AIO and no citation-win plan are demoted
- [ ] Site Reputation Abuse risk flagged on "best [thing] [year]" keywords where Forbes/CNN/Times brand pages dominate
- [ ] Information gain articulated per P0 keyword — what does the new piece add that the top 10 doesn't?
- [ ] Zero-volume candidates either kept (with Reddit/PAA validation) or struck — no auto-skip on volume = 0
- [ ] Survivors clustered into pillar-and-cluster structures, not flat lists
- [ ] Entity coverage mapped per cluster (top-10 H2/H3 mining, Wikipedia "See also", knowledge-panel related entities)
- [ ] Priority bucketing (P0/P1/P2/P3) applied with composite formula incl. AIO discount; realism = 1 demotes to P3
- [ ] GEO potential noted per keyword (question / definition / comparison / list)
- [ ] Brief uses the canonical template (`references/brief-template.md`); downstream concerns listed as Open Items
- [ ] Cannibalization check flagged: are any P0 keywords already targeted by an existing page?
- [ ] AI search visibility tracking listed in Open Items for any GEO-flagged P0/P1 keyword

## Composition / References

In-skill references (load on demand):
- `references/modifier-library.md` — full long-tail modifier library + SERP-mined sources for Stage 3
- `references/brief-template.md` — canonical Stage 6 brief output template + field definitions

Within-domain pairings:
- Pairs with the sibling marketing skill that prospects backlinks for the cluster pillar pages (priority for any P0 cluster that lacks link equity).
- Pairs with the sibling marketing skill that validates free-tool ideas — when a keyword cluster surfaces a recurring user problem (calculator, checker, generator), it's a tool-build trigger.

Downstream concerns (owned by other domains, not this skill):
- GEO content writing (answer-first structure, FAQ schema, extractable passages) — the brief flags GEO-eligible keywords; the writing pattern lives elsewhere.
- Content briefs, internal-link wiring, on-page schema, outreach copy — consume this brief, don't appear in it.
- AI search visibility tracking setup (Profound / Otterly / AthenaHQ / Peec) — the brief lists which keywords to track; configuration is downstream.

External authoritative sources:
- [Ahrefs — long-tail keyword research](https://ahrefs.com/blog/long-tail-keywords/)
- [Backlinko — keyword research definitive guide](https://backlinko.com/keyword-research)
- [Google Search Central — Helpful Content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central — Site Reputation Abuse policy](https://developers.google.com/search/docs/essentials/spam-policies#site-reputation)
- [SparkToro — zero-volume keyword research framework](https://sparktoro.com/blog/keyword-research-in-2024-the-3-rules-i-follow/)
- [Search Engine Journal — SERP analysis for keyword qualification](https://www.searchenginejournal.com/serp-analysis-seo/)
- [Search Engine Land — AI Overviews CTR impact studies 2024–2026](https://searchengineland.com/google-ai-overviews-traffic-loss-440873)
- [AI Platform Citation Source Index 2026](https://www.prnewswire.com/news-releases/5w-releases-ai-platform-citation-source-index-2026-the-50-websites-that-now-decide-what-brands-are-visible-inside-chatgpt-claude-perplexity-gemini-and-google-ai-overviews-302759804.html) — GEO citation distribution data
- [Princeton/Georgia Tech — GEO research paper (Aggarwal et al)](https://arxiv.org/abs/2311.09735) — original framework for AI-citation optimization
