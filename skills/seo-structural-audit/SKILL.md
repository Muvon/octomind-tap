---
name: seo-structural-audit
title: "Structural / Technical SEO Audit"
description: "Technical SEO audit: robots.txt, canonicals, sitemap, redirects, JSON-LD, Core Web Vitals, hreflang. Use when auditing the technical layer of a site."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires webfetch (for HTML/JSON-LD/page response) and shell (for curl, sitemap parsing, optional Lighthouse/PSI). Optional: GSC and crawler-tool MCPs for richer signal."
domains: seo writer
rules:
  - match((?i)\b(technical|structural)\s+seo\b)
  - match((?i)\b(audit|check|review|inspect|diagnose|find|validate|analy[sz]e)\b.{0,60}\b(robots\.txt|sitemap\.xml|hreflang|redirect\s+chains?|canonical\s+tags?|json-?ld|structured\s+data|schema\s+markup|indexation|raw\s+html)\b)
  - match((?i)\b(core\s+web\s+vitals|cwv)\b)
  - match((?i)\b(crawl|index|render)\w*\s+(issues?|problems?|errors?|gaps?|parity)\b)
  - semantic(diagnose technical SEO problems on this site)
  - semantic(check whether Google can crawl and index this page)
  - semantic(validate schema markup and structured data)
  - semantic(audit the technical layer for ranking blockers)
---

## Overview

Most "SEO problems" that look like content problems are actually structural — a missing canonical, a sitemap that 404s, a hero rendered only after JS hydration that Googlebot can't see, schema that fails validation, a redirect chain that drains link equity. This skill is the diagnostic playbook for that layer: a fetch protocol that gets the evidence in parallel, a per-surface check rubric that turns the evidence into a finding, and a severity matrix that says what to fix first. Output is a prioritized list with cited evidence — never inference where evidence could have been fetched.

## Mental model

Structural SEO is a chain of pass-throughs:

1. The crawler can reach the URL (robots.txt allows; no infinite redirect; status 200).
2. The renderer can see the content (raw HTML carries primary content OR pre-rendered; JS hydration doesn't hide it).
3. The indexer can understand the page (meta robots indexable; canonical self-referential or correctly assigned; schema validates).
4. The ranking system can compare it (Core Web Vitals within thresholds; internal-link topology lets PageRank flow; hreflang resolves correctly per locale).

Break any link in the chain and rankings collapse downstream regardless of how good the content is. Audit walks the chain in order; the first broken link is the highest-priority finding.

## Instructions

### Fetch protocol (parallel, ONE block)

Before scoring anything, get the evidence:

- Read the target URL with `knowledge(command="read", source="<url>")` — HTML content, headings, JSON-LD.
- `shell curl -sI <url>` — capture raw HTTP response and follow redirect chain (`-L` with `-w "%{redirect_url}\n%{http_code}\n"`).
- `shell curl -s <origin>/robots.txt` — fetch robots, parse `Allow` / `Disallow` / `Sitemap:` directives.
- `shell curl -s <origin>/sitemap.xml` — fetch sitemap; check for index file vs flat sitemap; spot-validate 5–10 URLs.
- Web search `site:<domain>` — rough indexed-page sanity check only; the search tool is not Google, so Google index coverage needs Search Console.
- For JS-rendered sites: raw HTML from `shell curl -s <url>` shows what non-rendering crawlers and most AI fetchers see; true render parity needs a headless browser or Search Console URL Inspection — otherwise mark it Unverified.

Run all six in one tool block. Don't serialize. If any fetch fails, the result becomes an "Unverified" finding — never inferred.

### Check rubric (per surface)

| # | Check | How to verify | Severity if failed |
|---|---|---|---|
| 1 | Crawlability | robots.txt does not Disallow the URL; no soft-404 | Critical if blocked |
| 2 | HTTP status | curl returns 200 (or 301 → 200 within 1 hop) | Critical if 4xx/5xx; Moderate if redirect chain >1 hop |
| 3 | Indexability | meta robots is index, follow (or absent) | Critical if noindex on a page meant to rank |
| 4 | Canonical | canonical tag present, points to self or correct alternate | Critical if canonical points to a different page incorrectly |
| 5 | Sitemap inclusion | URL appears in sitemap.xml, last-modified valid | Moderate if absent; Critical if sitemap itself 404s |
| 6 | Redirect chain | chain length ≤1 hop, no loops, terminal is 200 | Moderate at 2 hops; Critical at 3+ or any loop |
| 7 | Schema validity | JSON-LD parses; types match visible content (Article, Product, Organization, Person, BreadcrumbList, Review where genuine); required fields present | Moderate per invalid type or markup contradicting visible text; missing markup matters only where a live rich result is at stake |
| 8 | Core Web Vitals | Field data at the 75th percentile: LCP ≤2.5s; INP ≤200ms (replaced FID March 2024); CLS ≤0.1 | Critical if any metric in Google's "poor" band; Moderate if "needs improvement" |
| 9 | hreflang | each variant points to the others bidirectionally; uses ISO codes | Moderate if asymmetric or broken; Critical if hreflang errors mean wrong region ranks |
| 10 | JS-render parity | primary content (title, H1, body) visible in raw HTML view-source | Critical if primary content only appears after hydration |
| 11 | URL architecture | descriptive slug, no query-string for canonical content, consistent trailing-slash policy | Minor unless duplicate content created |
| 12 | Internal-link topology | practitioner convention, not a Google rule: pillar links out to clusters in first section; cluster pages link back within first 100 words; ≤3 clicks from homepage | Moderate if orphan pages or broken pillar/cluster pattern |
| 13 | Mobile parity | mobile viewport, responsive content, no separate m. subdomain serving different content | Critical if content differs materially mobile-vs-desktop |

### Severity matrix

- Critical — blocks indexing, blocks rendering, creates indexability conflict, or hits the "poor" CWV band. Fix before anything else.
- Moderate — degrades signal (chain too long, schema missing on eligible page, "needs improvement" CWV). Fix in current cycle.
- Minor — polish (slug aesthetics, alt-text on decorative images, sitemap last-modified timestamp accuracy). Fix when convenient.

A Critical finding stays Critical even when "it's just one tag." Severity is impact-weighted, not effort-weighted.

### Unverified checks — escalation rule

If a check could not run:

- 403 on robots.txt or sitemap → "Unverified: server blocks unauthenticated fetch; ask for crawler-allowed IP or share via GSC export."
- JS-render parity untestable (no headless browser available) → "Unverified: render parity needs headless render; recommend a Lighthouse run or rendered-fetch sample."
- GSC data needed (impressions, indexed-page count, crawl errors) → "Unverified: GSC access required; share read-only access or paste a coverage report."

Never infer a finding from absence of evidence. "Could not fetch" is its own finding type — it tells the user what to unblock, and it preserves trust in the rest of the report.

### Schema validation notes

- Google AI features need no special schema, `llms.txt` or content chunking, and FAQ and HowTo rich results are retired (dated facts and sources in `seo-google-policy-baseline`). Score schema for rich-result eligibility and entity clarity, not as a Google AI-citation lever. Microsoft's retail guide to AEO and GEO recommends `Product`, `Offer`, `AggregateRating`, `Review`, `Brand`, `ItemList` and `FAQ` markup for Copilot and Bing shopping; on retail pages with that scope, report missing types as a Copilot/Bing readiness gap and name the source.
- Retired rich results — don't report missing markup as lost visibility for FAQ or HowTo; leaving the markup in place is harmless. For any other type, check Google's search gallery and structured-data changelog live before calling it retired.
- Article schema → `headline`, `author` (Person with name + sameAs/url), `datePublished`, `dateModified`, `image`. Missing author identity on a YMYL page is Critical-tier as an E-E-A-T gap, schema or not.
- Person / Organization schema → anchors entity recognition. Missing `sameAs` to LinkedIn / publication / org bio is Moderate.
- Review / AggregateRating → present only when genuine reviews back it; self-serving reviews on LocalBusiness/Organization aren't eligible, and fake review markup risks a manual action (and the FTC reviews rule in the US).

### Core Web Vitals — interpretation, not measurement

This skill interprets CWV; it does not measure them. Source measurements:

- Field data: Google PageSpeed Insights, Search Console Core Web Vitals report, CrUX dataset.
- Lab data: Lighthouse CLI (`shell` capability), WebPageTest, browser DevTools.

When only lab data is available, flag the field-vs-lab gap; lab overstates good performance in many cases. INP needs field data — lab-only INP estimates are unreliable.

### Internal-link topology — what to look for

The link counts and click depths below are practitioner conventions, not Google rules; Google publishes no such thresholds. Report them as heuristics.
- Pillar pages should link out to every cluster article in their opening section (first 200 words).
- Cluster articles should link back to the pillar within the first 100 words.
- Cluster siblings should cross-link 2–3 times where topically relevant.
- Every indexable page should be reachable within 3 clicks from the homepage.
- Orphan pages (no internal inbound links) are a Moderate finding — they signal abandoned content or template gaps.
- The link graph should mirror the topic graph, not the navigation hierarchy.

### Index status, parameters, pagination, crawl budget, logs

Run when pages are missing from Google or the site has many URL variants. Needs Search Console (Page indexing report) or a supplied export; without it mark these checks Unverified.

| Status or pattern | What it means (Google) | Check and fix direction |
|---|---|---|
| Crawled - currently not indexed | Crawled, not added to the index; common and not necessarily a problem | For important pages, run URL Inspection and compare with indexed siblings: thin or duplicate content, weak internal links, a canonical elsewhere |
| Discovered - currently not indexed | Known but not crawled; Google likely postponed the crawl to avoid overloading the site | Confirm a link from a known page or a sitemap entry; allow weeks for new pages; look for server slowness and URL bloat |
| Duplicate without user-selected canonical, or Google chose a different canonical | Google clustered the page with another | Compare the two pages; set a consistent canonical, redirect or differentiate |
| Faceted or parameter URLs in the index | Filter and sort combinations create near-duplicates | Prevent crawling with robots.txt rules or URL fragments for filters; return 404 for combinations with no results; `rel=canonical` and `nofollow` are weaker (Google, faceted navigation) |
| Paginated series | Each page needs its own URL and a canonical to itself, linked with `<a href>`; Google no longer uses `rel=next` and `rel=prev` | Flag the first page used as the canonical of the series, and fragment-based page numbers |
| Crawl budget | Matters for sites of 1 million or more unique pages changing weekly, or 10,000 or more changing daily, or with many "Discovered - currently not indexed" URLs (Google) | On smaller sites don't raise it as a finding; fix URL inventory first |

Log analysis: with server logs, count Googlebot requests by URL type (templates, parameters, redirects, error codes) and compare with the URLs that should rank. Confirm a request is genuine Googlebot with Google's verification method before counting it. Without logs mark it Unverified; Search Console's Crawl stats report is the first-party substitute.

### Output

Use the report structure of the `seo-site-audit` skill. Every finding includes: severity, evidence (URL + line / header / schema field / metric), why it matters, fix direction. Save as `seo-audit-[slug]-[YYYY-MM-DD].md` in working directory.

## Checklist

- [ ] All six fetch operations ran in parallel
- [ ] Every check in the rubric was evaluated or flagged as Unverified
- [ ] Each finding cites concrete evidence (URL, line, header, schema field, metric)
- [ ] Severity assigned by impact, not effort
- [ ] Unverified findings name the specific blocker and the unblock path
- [ ] Schema findings name the type and the missing/invalid field; retired rich-result types (FAQ, HowTo, etc.) are not reported as lost visibility
- [ ] CWV findings name the source (field / lab / PSI) and the band (good / needs improvement / poor)
- [ ] Internal-link topology checked for pillar/cluster pattern and orphan pages
- [ ] Report saved to disk with timestamped filename

## Composition / References

Within-domain pairings:
- Pairs with the sibling SEO skill that audits on-page content quality (titles, meta, headings, intent match, AI-citability, E-E-A-T).
- Pairs with the sibling SEO skill that audits link profile (referring-domain quality, anchor distribution, toxic neighborhoods).

- Redirect and domain moves: `seo-site-migration`. Template page sets: `seo-programmatic`. Traffic that already fell: `seo-traffic-drop-diagnosis`.

External authoritative sources:
- [Google Search Central — Faceted navigation](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation)
- [Google Search Central — Managing crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google Search Central — Pagination](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading)
- [Google Search Console — Page indexing report](https://support.google.com/webmasters/answer/7440203)
- [Google Search Central — Crawling and indexing](https://developers.google.com/search/docs/crawling-indexing/overview)
- [Google Search Central — Structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Google Search Central — Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Google Search Central — Optimizing for generative AI features (May 2026)](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Schema.org — full type vocabulary](https://schema.org/docs/full.html)
- [web.dev — INP](https://web.dev/articles/inp)
- [Google Search Central — hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
