---
name: seo-link-audit
title: "Link Profile SEO Audit"
description: "Operational playbook for diagnosing the off-page link surface of a site: referring-domain quality distribution, unique-root-domain count, anchor-text distribution and over-optimization risk, toxic-neighborhood detection, paid-link risk patterns, link gap vs named competitors, and community/forum presence (Reddit and niche communities, which hold many SERP and AI-answer citations). Encodes the fetch protocol (parallel web search + page reads + competitor backlink discovery), the per-check rubric, the severity matrix, and the unverified-check escalation rule. Use when auditing the link profile of a site or a specific URL. Output: prioritized link-profile findings with cited evidence and fix direction."
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

Google's link spam policy (updated through 2026) still names paid links, link exchanges, automated links, and optimized-anchor links in guest posts and press releases. Google gave no specifics for the March 2026 (Mar 27–Apr 8) or May 2026 (May 21–Jun 2) core updates; third-party analyses saw aggregation-model sites lose. Spam updates in 2026 rolled out in days (March's in under 24 hours). The audit identifies risk patterns before they become algorithmic suppression or a manual action.

## Mental model

Three lenses, applied in order:

1. Authority surface — how many unique referring root domains, what's their topical fit, what's the DR/DA distribution? Diversity compounds; concentration on a few high-DR sources is brittle.
2. Risk surface — anchor distribution health, toxic-neighborhood exposure, paid-link patterns, velocity spikes, manufactured-mention signals. Most damage is algorithmic devaluation (SpamBrain neutralizes links); manual actions are rarer but still issued.
3. Gap surface — what links credible niche competitors have that this site doesn't. Topical-fit competitors at the same DR tier are the right comparison set; off-niche high-DR sites are noise.

Audit walks the lenses in order. Authority surface tells you what's working; risk surface tells you what could collapse; gap surface tells you what to chase next.

## Instructions

### Fetch protocol (parallel, ONE block)

- Web search `site:<domain>` — rough check of indexed pages and off-domain mentions (the search tool isn't Google).
- Web search `"<brand>" -site:<domain>` — capture brand mentions (linked + unlinked).
- Web search `"<brand>" site:reddit.com` — capture community presence; Reddit isn't a ranking signal, but forum threads hold many SERP slots and AI-answer citations.
- Competitor backlink lists from a backlink tool or its free checker — Google retired the `link:` operator in 2017, so search can't produce them.
- Read 5–10 known referring pages with `knowledge(command="read", source="<url>")`, or `shell curl` the raw HTML, to verify the link exists and its `rel`.
- If the user grants access: Search Console Links report (own site) and Bing Webmaster Tools backlinks; if a backlink-data MCP is connected, pull the referring-domain census, anchors, and toxicity flags.

Run in one block. Free-path covers the 80% case; paid-tool data adds census-level accuracy.

### Check rubric

| # | Check | How to verify | Severity if failed |
|---|---|---|---|
| 1 | Unique referring root domains | Count distinct root domains linking to the site (not URLs, not subdomains) | Note as baseline; flag if <30 for sites older than 12 months in a competitive niche |
| 2 | Topical fit distribution | Sample 20 referring domains; categorize as in-niche / adjacent / off-topic | Critical if >50% off-topic (reasonable-surfer discount); Moderate if >70% adjacent |
| 3 | DR/DA distribution | Sample distribution across DR bands; no single source contributing >30% of total link equity | Moderate if concentration risk (one DR-80 + a long tail of DR-10) |
| 4 | Anchor-text distribution | Practitioner heuristic, not a Google threshold: branded/URL majority, partial-match and natural phrases next, exact-match a small minority | Critical if exact-match dominates commercial anchors; Moderate if branded is a minority |
| 5 | Toxic-neighborhood exposure | Sample referring domains; check for casino/pharma/adult/foreign-language farms or sites that link to those | Critical per identified toxic referrer; recommend disavow only after exhaustion of removal-request path |
| 6 | Paid-link risk patterns | Look for: dofollow links from sites with "sponsored" / "advertorial" navigation, sites in known paid-link networks, niche-edit/link-insertion services | Critical per pattern detected — paid links without rel="sponsored" violate Google's link spam policy |
| 7 | Velocity profile | Look for unnatural spikes — 50+ links in a week from disparate sources is fine ONCE on a newsworthy basis; sustained spikes trigger SpamBrain | Moderate if recent spike unexplained; Critical if pattern is ongoing |
| 8 | Manufactured-mention signals | Look for bulk-purchased "brand mention" patterns — same wording across many sites, low-quality directories, AI-generated guest-post farm placements | Critical per pattern — Google's May 2026 AI optimization guide says seeking inauthentic mentions isn't helpful and its AI features depend on its spam systems |
| 9 | Link gap vs niche competitors | Identify 3 same-niche same-DR-tier competitors; list referring domains they have and this site doesn't | Document as opportunity, not deficit; rank by topical fit × authority |
| 10 | Community / forum presence | Reddit (relevant subreddits), Stack Exchange, niche forums — is the brand mentioned naturally and recently? | Moderate if absent in niches with active communities (forums take many SERP slots and AI-answer citations) |
| 11 | Brand-mention trend | Brand search interest and web mentions — growing? Ahrefs (2025) found branded web mentions correlate more with AI Overview visibility than backlinks do (correlation, not cause) | Moderate if brand interest is flat/down while backlink count grows fast (suggests inorganic link-building) |
| 12 | Unlinked-mention surface | Sites that mention the brand without linking — reclamation opportunity | Document as opportunity |
| 13 | Site reputation policy exposure | Are inbound links from third-party sections of big publishers ("best [X] [year]" coupon/review folders)? Google may treat those sections separately and issue manual actions — except for EEA searchers since Aug 30, 2026 | Note as fragile, not durable authority |
| 14 | Primary-source pass-through | Links from intermediary aggregator pages vs primary-source publications | Moderate if portfolio skews to aggregators |

### Severity matrix

- Critical — active algorithmic or manual-action risk: exact-match anchor saturation, toxic-neighborhood exposure, paid-link patterns, manufactured-mention campaigns, sustained velocity spikes.
- Moderate — degrades signal or creates concentration risk: anchor distribution off-target but under thresholds, single-source concentration, sparse topical fit, absent community presence in niches that have active ones, intermediary-heavy portfolio.
- Minor — polish opportunities: unlinked mentions to convert, weak anchor diversity on otherwise healthy profiles.

### Anchor-text distribution — practitioner heuristic

Google publishes no anchor ratios; its policy targets optimized anchors in paid, exchanged, or distributed content. Use this mix as a smell test, not a target to engineer:

- Branded — 40–50% (e.g., "Acme")
- URL-only — 5–10% (e.g., "acme.com")
- Generic — 5–10% (e.g., "this resource", "read more")
- Semantic / long-tail — 15–25% (descriptive natural phrases)
- Partial-match — 20–30% (contains the keyword in a longer phrase)
- Exact-match — <10% (the keyword alone or near-alone)

Exact-match concentration on links the site controlled (guest posts, partner pages, releases) is the most common over-optimization pattern.

### Paid-link detection patterns

- Same dofollow placement available across many unrelated sites for a published rate card
- Site navigation includes "Sponsored Posts" / "Advertorial" / "Write for Us (paid)"
- Footer or sidebar links to many unrelated commercial sites with exact-match anchors
- Anchor inserted mid-paragraph in pre-existing content (niche-edit / link-insertion signature)
- "Vetted networks" charging $200–500 per placement — almost always disguised PBNs
- Modern variant: paid-tool-directory tiers that bundle a "dofollow link" into the $97–$197/yr listing

Any of these without `rel="sponsored"` is a Critical finding. Google's policy text covers "links with optimized anchor text in articles, guest posts, or press releases distributed on other sites" and "sending someone a product in exchange for them writing about it and including a link"; mass AI-written placements also fall under scaled content abuse.

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
- [ ] Anchor distribution compared with the practitioner heuristic (labeled as heuristic in the report)
- [ ] Toxic-neighborhood scan performed on referring domains
- [ ] Paid-link patterns explicitly checked, including modern paid-directory variants
- [ ] Velocity profile reviewed for spikes
- [ ] Manufactured-mention patterns checked (bulk wording, low-quality directories, guest-post farms)
- [ ] Link-gap analysis run against 3 same-niche same-DR-tier competitors
- [ ] Community / forum presence (Reddit, niche communities) audited
- [ ] Brand-mention trend cross-referenced against backlink growth (inorganic-link tell)
- [ ] Site reputation policy exposure noted for third-party publisher sections (with EEA caveat)
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
