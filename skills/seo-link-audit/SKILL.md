---
name: seo-link-audit
title: "Link Profile SEO Audit"
description: "Operational playbook for diagnosing the off-page link surface of a site: referring-domain quality distribution, unique-root-domain count, anchor-text distribution and over-optimization risk, toxic-neighborhood detection, paid-link risk patterns, link gap vs named competitors, and community/forum presence (Reddit / niche communities, now a 2026 ranking signal). Encodes the fetch protocol (parallel websearch + webfetch + competitor backlink discovery), the per-check rubric, the severity matrix, and the unverified-check escalation rule. Use when auditing the link profile of a site or a specific URL. Output: prioritized link-profile findings with cited evidence and fix direction."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires websearch + webfetch. Free path covers 80% via SERP operators, site: queries, and competitor public-link discovery. Paid path (Ahrefs / SEMrush / Majestic / Moz Link Explorer) provides referring-domain census and anchor-distribution data at scale."
domains: seo
rules:
  - session(seo)
  - session(audit)
  - content(audit)
  - content(backlinks)
  - content(backlink)
  - content(referring domain)
  - content(referring domains)
  - content(anchor text)
  - content(link profile)
  - content(link gap)
  - content(toxic links)
  - match(\b(audit|review|inspect)\s+.{0,40}(backlinks?|link\s+profile|referring\s+domains?)\b)
  - match(\b(anchor|anchor\s+text)\s+(distribution|profile|audit|review)\b)
  - match(\b(toxic|spammy|low[\s-]quality)\s+(links?|domains?|backlinks?)\b)
  - match(\b(link\s+gap|backlink\s+gap)\b)
  - match(\b(disavow|penalty|manual\s+action|spambrain)\b)
  - match(\b(off-?page)\s+seo\s+(audit|review|check)\b)
  - semantic(audit the backlink profile for risks and gaps)
  - semantic(check for toxic or paid link patterns)
  - semantic(diagnose link profile against competitors)
  - semantic(review anchor text distribution for over-optimization)
---

## Overview

A link profile is a portfolio. The audit asks four questions: how many distinct authoritative voices vouch for the site, how natural does the anchor distribution look to an algorithm, how much penalty exposure is hiding in the long tail, and where do credible competitors get links that this site doesn't. The answer is a prioritized finding list — not a vanity count of "total backlinks." Raw inbound count has been an inferior signal since 2019; unique referring root domains, topical fit, and authentic-mention sources are what compound in 2026.

The March 2026 core update sharpened this: 80% of top-3 results shifted, intermediary pages were demoted, and algorithmic link-spam detection moved from "months to take effect" to "minutes." Paid-link risk got worse, not better. The audit identifies risk patterns before they become algorithmic suppression.

## Mental model

Three lenses, applied in order:

1. Authority surface — how many unique referring root domains, what's their topical fit, what's the DR/DA distribution? Diversity compounds; concentration on a few high-DR sources is brittle.
2. Risk surface — anchor distribution health, toxic-neighborhood exposure, paid-link patterns, velocity spikes, manufactured-mention signals. Risk is now scored by algorithms in minutes; manual actions are rare but algorithmic suppression is near-instant.
3. Gap surface — what links credible niche competitors have that this site doesn't. Topical-fit competitors at the same DR tier are the right comparison set; off-niche high-DR sites are noise.

Audit walks the lenses in order. Authority surface tells you what's working; risk surface tells you what could collapse; gap surface tells you what to chase next.

## Instructions

### Fetch protocol (parallel, ONE block)

- `websearch site:<domain>` — sanity-check indexed pages and any indexed off-domain mentions.
- `websearch "<brand>"` — capture brand mentions across SERP (linked + unlinked).
- `websearch "<brand>" site:reddit.com` — capture Reddit presence (post Feb-2024 Google–Reddit deal, Reddit is structurally important for both organic and AI-search visibility).
- `websearch link:<competitor.com>` operators or paid-tool competitor backlink lists — for link-gap analysis.
- `webfetch` 5–10 known referring pages to verify links exist and are dofollow.
- If paid tools available: pull referring-domain census, anchor distribution, and toxic-domain flags via the relevant MCP.

Run in one block. Free-path covers the 80% case; paid-tool data adds census-level accuracy.

### Check rubric

| # | Check | How to verify | Severity if failed |
|---|---|---|---|
| 1 | Unique referring root domains | Count distinct root domains linking to the site (not URLs, not subdomains) | Note as baseline; flag if <30 for sites older than 12 months in a competitive niche |
| 2 | Topical fit distribution | Sample 20 referring domains; categorize as in-niche / adjacent / off-topic | Critical if >50% off-topic (reasonable-surfer discount); Moderate if >70% adjacent |
| 3 | DR/DA distribution | Sample distribution across DR bands; no single source contributing >30% of total link equity | Moderate if concentration risk (one DR-80 + a long tail of DR-10) |
| 4 | Anchor-text distribution | 40–50% branded, 20–30% partial-match, 15–25% semantic/long-tail, 5–10% generic, <10% exact-match (data-backed: 68% manual-action reduction with diversification) | Critical if exact-match >15%; Moderate if branded <30% |
| 5 | Toxic-neighborhood exposure | Sample referring domains; check for casino/pharma/adult/foreign-language farms or sites that link to those | Critical per identified toxic referrer; recommend disavow only after exhaustion of removal-request path |
| 6 | Paid-link risk patterns | Look for: dofollow links from sites with "sponsored" / "advertorial" navigation, sites in known paid-link networks, niche-edit/link-insertion services | Critical per pattern detected — 2026 algorithmic devaluation is minutes, not months |
| 7 | Velocity profile | Look for unnatural spikes — 50+ links in a week from disparate sources is fine ONCE on a newsworthy basis; sustained spikes trigger SpamBrain | Moderate if recent spike unexplained; Critical if pattern is ongoing |
| 8 | Manufactured-mention signals | Look for bulk-purchased "brand mention" patterns — same wording across many sites, low-quality directories, AI-generated guest-post farm placements | Critical per pattern (Google's 2026 AI optimization guide is explicit: manufactured mentions trigger the same discount as cheap directories) |
| 9 | Link gap vs niche competitors | Identify 3 same-niche same-DR-tier competitors; list referring domains they have and this site doesn't | Document as opportunity, not deficit; rank by topical fit × authority |
| 10 | Community / forum presence | Reddit (especially relevant subreddits), Stack Exchange, niche forums — is the brand mentioned naturally and recently? | Moderate if absent in niches with active communities (Reddit is now ~37% of AI Overview citations from social/forum sources) |
| 11 | Brand search volume signal | Search volume on "<brand>" and "<brand> + [modifier]" — is it growing? Brand search now outweighs backlinks as an LLM citation predictor. | Moderate if brand search trending flat/down while backlink count is growing (suggests inorganic link-building) |
| 12 | Unlinked-mention surface | Sites that mention the brand without linking — reclamation opportunity | Document as opportunity |
| 13 | Site Reputation Abuse exposure | Are any inbound links from "best [X] [year]" listicles on Forbes/CNN/Times brand subdomains? Aug 2025 update made enforcement algorithmic; decay is 6–8 weeks. | Note as time-bounded link, not durable authority |
| 14 | Primary-source pass-through | When links come from intermediary aggregator pages, weigh discounted vs links from primary-source publications (March 2026 update demoted intermediaries) | Moderate if portfolio skews to aggregators |

### Severity matrix

- Critical — active algorithmic risk: exact-match anchor saturation, toxic-neighborhood exposure, paid-link patterns, manufactured-mention campaigns, sustained velocity spikes. These suppress rankings in minutes under 2026 systems.
- Moderate — degrades signal or creates concentration risk: anchor distribution off-target but under thresholds, single-source concentration, sparse topical fit, absent community presence in niches that have active ones, intermediary-heavy portfolio.
- Minor — polish opportunities: unlinked mentions to convert, weak anchor diversity on otherwise healthy profiles.

### Anchor-text distribution — the data-backed targets

Targets (from manual-action correlation studies and Google's own guidance through link-spam updates):

- Branded — 40–50% (e.g., "Acme")
- URL-only — 5–10% (e.g., "acme.com")
- Generic — 5–10% (e.g., "this resource", "read more")
- Semantic / long-tail — 15–25% (descriptive natural phrases)
- Partial-match — 20–30% (contains the keyword in a longer phrase)
- Exact-match — <10% (the keyword alone or near-alone)

Diversification reduces manual-action exposure by ~68%. The exact-match cap is the single most-violated rule in link-building campaigns; over-optimization here is a leading penalty trigger.

### Paid-link detection patterns

- Same dofollow placement available across many unrelated sites for a published rate card
- Site navigation includes "Sponsored Posts" / "Advertorial" / "Write for Us (paid)"
- Footer or sidebar links to many unrelated commercial sites with exact-match anchors
- Anchor inserted mid-paragraph in pre-existing content (niche-edit / link-insertion signature)
- "Vetted networks" charging $200–500 per placement — almost always disguised PBNs
- Modern variant: paid-tool-directory tiers that bundle a "dofollow link" into the $97–$197/yr listing

Any of these without `rel="sponsored"` is a Critical finding. The Oct-2025 update made guest-post farm placements (AI-generated content + paid embedded link) a distinct violation category; the March 2026 update made algorithmic devaluation near-instant.

### Unverified checks — escalation rule

- No backlink-tool access (free path only) → "Unverified: full referring-domain census needs Ahrefs/SEMrush/Majestic; current findings cover SERP-visible links and sampled referrers only."
- Anchor distribution sample too small (<50 links) → "Unverified: anchor distribution requires a larger sample; flag as estimate."
- Cannot reach a referring page to confirm dofollow status → "Unverified per referrer; flag with `[needs confirmation]`."

Never claim "no toxic links found" — claim "no toxic links found in sample of N."

### Output

Use the canonical output structure from the agent that runs this skill. Every finding includes: severity, evidence (referring domain, anchor text, page context, capture date), why it matters, fix direction. Save as `seo-audit-[slug]-[YYYY-MM-DD].md` in working directory.

## Checklist

- [ ] All fetch operations ran in parallel
- [ ] Unique referring root domains counted (not URLs)
- [ ] Topical-fit distribution sampled across at least 20 referrers
- [ ] Anchor distribution measured against the data-backed targets
- [ ] Toxic-neighborhood scan performed on referring domains
- [ ] Paid-link patterns explicitly checked, including modern paid-directory variants
- [ ] Velocity profile reviewed for spikes
- [ ] Manufactured-mention patterns checked (bulk wording, low-quality directories, guest-post farms)
- [ ] Link-gap analysis run against 3 same-niche same-DR-tier competitors
- [ ] Community / forum presence (Reddit, niche communities) audited
- [ ] Brand search trend cross-referenced against backlink growth (inorganic-link tell)
- [ ] Site Reputation Abuse exposure noted for time-bounded brand-page placements
- [ ] Primary-source vs intermediary share scored
- [ ] Every finding cites concrete evidence (referring domain, anchor, page context, capture date)
- [ ] Report saved to disk with timestamped filename

## Composition / References

Within-domain pairings:
- Pairs with the sibling SEO skill that audits the structural / technical layer.
- Pairs with the sibling SEO skill that audits on-page content quality.

External authoritative sources:
- [Google Search Central — Link spam policy](https://developers.google.com/search/docs/essentials/spam-policies#link-spam)
- [Google Search Central — Qualifying outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
- [Google Search Central — Site Reputation Abuse policy](https://developers.google.com/search/docs/essentials/spam-policies#site-reputation)
- [Ahrefs — Referring domains vs backlinks](https://ahrefs.com/blog/referring-domains-vs-backlinks/)
- [Search Engine Journal — Anchor text distribution research](https://www.searchenginejournal.com/anchor-text-seo/)
- [Backlinko — Link audit guide](https://backlinko.com/link-audit)
