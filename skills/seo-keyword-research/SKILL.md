---
name: seo-keyword-research
title: "Long-Tail Keyword Research: Low-Competition Discovery"
description: "Operational funnel for discovering high-intent, low-competition long-tail keywords (4+ word phrases with weak SERP defenders), the keyword class that actually ranks for new and mid-authority sites without massive backlink spend. Encodes the discovery method (seed to modifier expansion to Google autocomplete + 'People Also Ask' + Reddit/forum mining + competitor SERP-gap), the qualification rubric that goes beyond KD scores (top-10 SERP authority profile, content-fit gap, intent match, traffic-potential vs ranking-realism, query freshness), the 2026 GEO overlay (definition + question + comparison queries that earn AI-search citations), and the kill-rules (head-term traps, fake-volume keywords, branded-SERPs, paid-ads-dominated SERPs). Use BEFORE writing any content brief, calendar, or pillar-cluster plan. Stays in the SEO lane: produces a keyword brief; content writing, on-page wrapping, and link-building are downstream concerns owned elsewhere."
license: Apache-2.0
compatibility: "Requires web search and page fetching. Authenticated SEO providers additionally require their documented credentials and API access; Search Console needs a private service-account JSON file."
capabilities: seo-data
domains: seo
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

Most keyword research dies at the head term. A DR-25 site chasing "project management software" (KD 72) loses to Asana and Monday.com forever, but the same audience also searches "free task tracker for two-person agencies" (KD 8, weak SERPs, transactional intent), the keyword class that converts on month-three traffic instead of year-three. This skill is the funnel that finds those reliably: seed, modifier expansion, SERP-mined patterns, and competitor gap, then a SERP-authority rubric that beats raw KD, then a prioritized brief mapped to content types and intent.

## Mental model

Long-tail wins on four compounding axes that head-term chasing loses:

1. SERP authority profile beats KD. KD is a dumb average; what matters is whether the actual top 10 are beatable. A "KD 35" keyword topped by three generic 1,500-word AI posts is more winnable than a "KD 18" one held by Wikipedia, a 5-year-old definitive guide, and the official product page.
2. Intent specificity is the conversion lever. "[head term] for [audience] under [constraint]" attracts only buyers. A 100-volume long-tail at 8% conversion beats a 10,000-volume head term at 0.2%.
3. Long-tail clusters earn topical authority. Five 200-volume long-tails on one sub-topic, internally linked to a pillar, signal more expertise than one head-term page. Google's core ranking (which absorbed the Helpful Content System in March 2024) rewards original information, depth, and entity-coverage breadth, not surface listicles.
4. Query fan-out rewards coverage, not page count. Google's AI features issue concurrent related sub-queries (Google AI optimization guide, May 2026). A cluster that genuinely answers them gets surfaced; a page per variation built to manipulate AI answers is scaled content abuse, and Google says AI search needs no extra long-tail keywords. Map fan-out questions to sections first, new pages only for distinct intents.

### 2026 algorithmic context (kill-rules upstream of the funnel)

| Reality | Implication for keyword selection |
|---|---|
| Core updates: March 2026 (Mar 27–Apr 8), May 2026 (May 21–Jun 2); Helpful Content signals in core ranking since March 2024 | Google gave no specifics; third-party analyses saw aggregation-model sites (comparison, directory, job board) lose. Pick keywords where your unique angle, data, or experience fills a gap. |
| Site reputation policy (enforced since May 2024; manual actions no longer apply to EEA searchers since Aug 30, 2026) | "Best [X] [year]" third-party sections on big publishers still rank in some markets. Score these SERPs conservatively unless DR ≥ 50 or a niche-brand-page play. |
| AI Overviews / AI Mode can change informational search journeys; published CTR studies describe their own samples, not this site's expected change | Search Console Web performance includes these features; verify live dimensions and don't assume an AI-only report. Keep actual engine captures and scoped vendor samples separate from search totals. |
| Branded web mentions correlate with AI Overview visibility more than backlinks (Ahrefs 2025; correlation, not cause) | Long-term, brand + modifier keywords become a defensive cluster. Short-term, long-tails still convert. |
| Reddit / forum threads hold many SERP slots and AI-answer citations (shares vary widely by study) | When the top 5 organic results are Reddit threads, the keyword is community-owned; engage there in parallel with publishing. |

## Instructions

### Core rules

- Long-tail = 4+ words OR a clear intent-specific modifier on a head term. "Best CRM" is short-tail; "best CRM for solo financial advisors" is long-tail. Specificity matters, not word count.
- SERP review is non-negotiable. Inspect the actual top 10 for every keyword that survives expansion. KD from any tool (Ahrefs, SEMrush, SE Ranking, Serpstat) is a starting estimate, not a verdict.
- Realism rule (heuristic): target keywords whose top-10 average DR is within roughly +15 of your DR. A DR-25 site can credibly rank against DR 10–40; a top 10 averaging DR 60+ is a multi-year project. Widen the band when the top 10 are weak or old, narrow it when they are definitive.
- Information gain is the on-page kill rule (Google's self-assessment asks for "original information, reporting, research, or analysis"; "information gain" itself is patent language, not a documented ranking system). If you can't name what the new piece adds over the top 10 (data, perspective, structure, freshness), the keyword isn't yours yet; picking it without an angle is the same mistake as picking a head term without DR.
- Intent must match the site's commercial position. Informational keywords on a transactional product page, or commercial-investigation keywords on a thin glossary page, neither rank nor convert. Classify intent before assigning content type.
- Five+ candidates per sub-topic, not one. Single-keyword targeting anchors to whatever came first; even if four are dead ends, the comparison clarifies why the survivor wins.
- Zero-volume keywords are a real 2026 category. AI search shifts demand to long-tails that tools mark "0"; one ranking for 12 related semantic queries can earn 200+ visits/month. Check related-keyword overlap instead of auto-striking.
- GEO requests start from buyer decisions, not a keyword score. Use the `geo-visibility-audit` skill for question discovery, observed citation gaps, or retests; DR and keyword volume aren't prerequisites. Conventional keywords may carry a provisional AI-answer relevance note, not a predicted citation score. Google AI-feature eligibility follows indexing and snippet eligibility, with no additional technical requirements.
- Output a brief, not a verdict (see Stage 6); writing, schema, internal-link wiring, and outreach are downstream.
- `seo-data` defaults to keyless DuckDuckGo search plus public-page inspection; it supplies no measured volume, difficulty, backlink metrics, or DR. Optional providers include DataForSEO, Ahrefs, Semrush, SE Ranking, Serpstat, and authorized Search Console. Inspect the connected provider's tools/docs, confirm scope/budget before billable calls, and record provider, endpoint, locale, timestamp, and returned cost. Only Ahrefs data establishes Ahrefs DR. Search Console is first-party performance, not competitor intelligence; unofficial autocomplete/Trends sources provide suggestions and relative interest, not measured volume. Missing credentials leave the public-evidence path available.
- Compound over spike. Trend keywords decay within 12 months; "how to [permanent task]" compounds for years.

### The funnel

#### Stage 1 — Profile the site (kill or proceed)

This funnel qualifies conventional Google keywords. For a GEO/AEO request, use the GEO skill's bounded mode instead of forcing this funnel or its DR gate; an overlapping activation doesn't change the requested deliverable.

Get concrete answers before generating any list; if unclear, stop and ask.

1. Niche: one sentence, plus sub-niche.
2. Audience: the specific segment that buys, not "small businesses."
3. Current DR: rough estimate (Ahrefs free tool, Moz Link Explorer, or "we're new"). Sets the realism cap.
4. Existing content: count and coverage. For an existing site, check what already ranks (Search Console queries) before generating overlap.
5. Commercial position: informational, affiliate, SaaS, e-commerce, local services. Decides which intent classes to prioritize.
6. Geo + language: global English, US-only, multi-region, non-English. Affects SERP review and modifier set.

If the user can't name DR or commercial position, kill here; qualification would be blind: "I'd be guessing whether the top 10 are beatable. Get a DR estimate (Ahrefs free Backlink Checker takes 30 seconds) and tell me what conversion looks like, then I'll run the funnel."

#### Stage 2 — Generate seed keywords (parallel)

Fire all seed sources in ONE parallel block:

- Core product/service nouns, in buyer language, not internal jargon.
- Problem phrases: "[problem] when [context]", "[symptom] in [audience]", "stop [bad thing]".
- Solution phrases: "how to [task]", "[task] without [obstacle]", "alternative to [incumbent]".
- Audience qualifiers: "[product] for [segment / team size / use case]".
- Industry / vertical terminology from the buyer's world.
- Existing-content mining: Search Console queries pulling impressions but ranking page 2–5; each seeds related long-tails.
- Competitor SERP gaps: 3 competitors at the same DR tier, their top-200 ranking keywords (Ahrefs Site Explorer / SE Ranking competitor research / SEMrush Domain Overview), filtered to those the user's site doesn't rank for.

Output: 30–80 seed terms, unqualified.

#### Stage 3 — Expand to long-tail (modifier patterns + SERP mining)

Generate 5–15 variants per seed, all seeds in parallel, from the modifier buckets in `references/modifier-library.md`: question (highest GEO value), intent (commercial/transactional), constraint (highest yield for low-DR sites; every constraint kills a competing page), outcome, comparison (mid-funnel, AI-citation-friendly), and problem-trigger (error messages, support-forum phrasings; highest conversion when the product solves the pain).

Fire the SERP-mined sources listed there (autocomplete a–z, PAA, Related searches, Trends rising, Reddit/forums, Lowfruits, Glimpse / Exploding Topics) in one block. The web search tool isn't Google: autocomplete, PAA, and Related searches come from the user, a connected SERP tool, or public PAA tools; list any source you couldn't reach as unused in Method Notes.

Output: 200–500 candidates, deduped at Stage 4.

#### Stage 4 — Qualify each long-tail (SERP-first rubric)

This separates winnable keywords from KD-low-but-unwinnable ones. Walk top to bottom and STRIKE on the first failure; it's a kill list, not a score.

| # | Check | How to verify | Strike condition |
|---|---|---|---|
| 1 | Intent match | What does the searcher actually want? | Mismatch with the site's commercial position |
| 2 | Volume realism | Tool estimate + Google Trends sanity check | Volume 0 AND no related-keyword cluster |
| 3 | SERP authority profile | Top 10: domain DRs, word counts, content age, brand vs independent | Top-10 average DR > user DR + 15 AND no obvious content gap |
| 4 | Top-10 content quality | Read 3–5 results: comprehensive, recent, structured? | Already definitive (a perfect Wikipedia page, official docs, a 5k-word evergreen pillar) |
| 5 | Content-fit gap | Sub-angle the top 10 miss (audience, constraint, use case)? | Every angle covered well |
| 6 | Paid ads dominance | Count ads above organic | 4 ads above organic; organic CTR drops below 20% |
| 7 | AI Overview presence | Only from an actual dated capture or an explicitly documented SERP-data field; Search Console Web aggregates and ordinary web search don't establish query-level presence | Record observed presence or Unverified; don't forecast this site's CTR loss from another study |
| 8 | Site reputation risk | Top 3 are third-party sections on Forbes/CNN-style publishers? | Yes AND user DR < 50: demote (outside the EEA these sections face manual actions, so re-check periodically) |
| 9 | Branded SERP | Top 10 mostly one brand's pages? | Searcher wants a specific brand, not a category answer |
| 10 | Featured snippet | Who holds it? | Holder DR 70+ with strong content; a weak holder is a snippet-steal opportunity |
| 11 | Trend direction | Google Trends 5-year view | Sharp decline |
| 12 | Cluster fit | Fits a planned cluster? | Orphan with no internal-link path |

Survive all 12 or strike. For zero-volume candidates, replace check 2 with "appears in 5+ Reddit threads OR in PAA / autocomplete?": yes means a real query with no tool data, keep; no means strike.

#### Stage 5 — Cluster, map entity coverage, prioritize

1. Pick pillar candidates: broad seeds with the most survivors around them.
2. Group survivors under pillars by sub-topic (one pillar + 4–8 cluster pages).
3. Map entity coverage per cluster: named entities, sub-topics, and concepts the pillar must cover, from the top-10 pages' H2/H3 structure (n-gram-mined), Wikipedia "See also" for the seed, and knowledge-panel related entities. A pillar missing 3+ entities the whole top 10 covers signals shallow coverage.
4. Score each survivor:
   - Realism: top-10 authority vs user DR (1 = unwinnable, 5 = clearly beatable).
   - Intent value: informational 1, navigational 1, commercial 2, transactional 3, multiplied by relevance to the site's commercial position.
   - GEO potential: definition / how-to / comparison / list, 1 each (max 4).
   - Cluster fit: pillar 5, primary cluster page 4, secondary 3, orphan 1.
   - AIO discount: subtract 2 only when an AI Overview is observed on an informational keyword AND the page has no information-gain angle. Unknown presence stays Unverified, not a negative observation.

   Composite priority = (realism × 3) + (intent × 2) + GEO + cluster_fit − AIO_discount. Range 9–35.
5. Bucket: P0 quick wins (≥ 28, publish first month), P1 high-value (22–27, next sprint), P2 cluster fillers (16–21, batch with pillar), P3 monitor (< 16, not this quarter). Realism 1 forces P3 regardless of total.

#### Stage 6 — Output the keyword brief

Fill every section of `references/brief-template.md` (P0–P3 tables with intent, content type, and calendar slot; clusters with entity coverage, GEO notes, risk notes, existing-content audit, downstream open items). The brief is the deliverable; anything outside it is downstream.

### Decision guide — common edge cases

| Situation | Action |
|---|---|
| No DR estimate and no Search Console | Kill at Stage 1; ask for an Ahrefs free Backlink Checker number. |
| Top 10 includes Wikipedia | Strike; cluster around adjacent long-tails. |
| Volume 0 but 12 Reddit threads on the question | Keep; score realism normally. |
| User pushes a head term ("just give me 'project management software'") | Refuse and explain: a 24-month project at their DR. Offer P0 long-tails in the same cluster as the first target. |
| Top 10 are 4+ years old and thin (under 1,000 words) | Quick win; fresh, comprehensive content leapfrogs. |
| Featured snippet held by DR 70+ with strong content | Strike, unless it's wrong/incomplete and the user can demonstrably do better. |
| 4+ paid ads | Demote (organic CTR 15–20%); pick a less-monetized adjacent long-tail or pay. |
| Non-English market | Re-run Stages 2–4 with native-language seeds on the local Google domain. |
| Brand names in seeds | Treat separately: brand terms convert at 5–10× organic, but the play is brand defense + comparison content. |

### Tools

Free-vs-paid tool table: `references/modifier-library.md`. Use a connected SEO-data MCP (Ahrefs, SE Ranking, Serpstat, Search Console) for volume, KD, and SERP features if present; none is assumed. Paid tools never replace the manual Stage 4 SERP review.

## Examples

### Example 1: SaaS, mid-authority, finds quick wins

Open-source self-hosted CRM, DR 28: the rubric keeps "self-hosted CRM for sales teams under 10" (KD 14, top-10 avg DR 22) as P0 and zero-volume "CRM Docker compose" as P1, strikes "best CRM software" (KD 78) and "CRM" (branded), and clusters survivors under a "Self-hosted CRM: complete guide" pillar. Full walkthrough: `references/brief-template.md` (worked example).

### Example 2: New site, no DR — refuse the head term

User: "We just launched. We sell project management software. Find me 50 keywords."

> Stop. At a brand-new domain (DR ~0–5), 80% of "project management software" keywords are unwinnable for 12+ months; Asana, Monday, ClickUp, and Notion own them with decade-old backlink graphs. Fifty generic PM keywords would waste your first quarter. Two questions first:
>
> 1. Which segment converts that the incumbents underserve (e.g. "construction subcontractors with 3–15 person crews", "law firms doing matter management")? Narrower segment, more long-tail surface.
> 2. What's the 1–2-sentence reason to switch (feature gap, pricing model, integration, vertical workflow)? That becomes the Stage 3 modifier set.
>
> If "we don't know yet", positioning is upstream of keyword research: pick the niche, then run the funnel.

### Example 3: GSC mining for free quick wins

For any site live ≥ 3 months with Search Console, run this first; it's the highest-ROI single source. Pull queries with impressions > 100 and average position 8–20 (page 2), confirm intent against the existing page, and SERP-review for room to climb. Matching intent: a 200-word section plus an intent-aligned H2 typically lifts it into the top 10 in 4–8 weeks. Mismatched intent or incidental overlap: a new dedicated page that outranks the parent.

## Checklist

- [ ] Stage 1 profile captured: niche, audience, DR, existing coverage, commercial position, geo
- [ ] DR and commercial position confirmed before any keyword generation (kill-gate)
- [ ] Seeds from ≥ 4 of the 7 source categories, run in parallel
- [ ] 5–15 variants per seed from the modifier library
- [ ] Manual SERP review for every candidate surviving volume + intent (rubric check 3)
- [ ] Realism rule applied: top-10 average DR within ~+15 of user DR, banded by content-quality gap
- [ ] AIO presence recorded from real evidence or marked Unverified; informational AIO keywords without an information-gain angle demoted
- [ ] Site Reputation Abuse risk flagged on "best [thing] [year]" keywords dominated by Forbes/CNN/Times brand pages
- [ ] Information gain articulated per P0 keyword
- [ ] Zero-volume candidates kept with Reddit/PAA validation or struck, never auto-skipped
- [ ] Survivors clustered into pillar-and-cluster structures, not flat lists
- [ ] Entity coverage mapped per cluster (top-10 H2/H3 mining, Wikipedia "See also", knowledge-panel entities)
- [ ] P0–P3 bucketing via the composite formula incl. AIO discount; realism 1 demotes to P3
- [ ] GEO potential noted per keyword (question / definition / comparison / list)
- [ ] Brief follows `references/brief-template.md`; downstream concerns listed as Open Items
- [ ] Cannibalization checked: any P0 keyword already targeted by an existing page?
- [ ] AI search visibility tracking listed in Open Items for GEO-flagged P0/P1 keywords

## Composition / References

In-skill references (load on demand):
- `references/modifier-library.md` — full modifier library, SERP-mined sources, and free-vs-paid tool table for Stage 3
- `references/brief-template.md` — canonical Stage 6 brief template, field definitions, and the full Example 1 walkthrough

Within-domain pairings:
- The sibling SEO skill that prospects backlinks for cluster pillar pages (priority for any P0 cluster lacking link equity).
- `geo-visibility-audit` — buyer-question discovery, captured-answer diagnosis, and retests; its scope and no-DR gate take precedence for GEO requests.
- The sibling SEO skill that validates free-tool ideas: a cluster surfacing a recurring user problem (calculator, checker, generator) is a tool-build trigger.

Downstream concerns (other domains):
- GEO content writing (clear answers, information gain, crawlable text); the brief only flags GEO-eligible keywords.
- Content briefs, internal-link wiring, on-page schema, outreach copy consume this brief.
- AI search visibility tracking setup (Profound / Otterly / AthenaHQ / Peec); the brief lists which keywords to track.

External authoritative sources:
- [Ahrefs — long-tail keyword research](https://ahrefs.com/blog/long-tail-keywords/)
- [Backlinko — keyword research definitive guide](https://backlinko.com/keyword-research)
- [Google Search Central — Helpful Content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google Search Central — Site Reputation Abuse policy](https://developers.google.com/search/docs/essentials/spam-policies#site-reputation)
- [SparkToro — zero-volume keyword research framework](https://sparktoro.com/blog/keyword-research-in-2024-the-3-rules-i-follow/)
- [Search Engine Journal — SERP analysis for keyword qualification](https://www.searchenginejournal.com/serp-analysis-seo/)
- [Search Engine Land — AI Overviews CTR impact studies 2024–2026](https://searchengineland.com/google-ai-overviews-traffic-loss-440873)
- [Google Search Central — AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) — eligibility and AI-feature traffic within Search Console Web performance.
- [Google Search Central — Optimizing for generative AI features (May 2026)](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) — query fan-out, scaled content abuse, mythbusting
- [Princeton/Georgia Tech — GEO research paper (Aggarwal et al)](https://arxiv.org/abs/2311.09735) — original framework for AI-citation optimization
