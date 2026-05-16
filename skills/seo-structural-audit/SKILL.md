---
name: seo-structural-audit
title: "Structural / Technical SEO Audit"
description: "Operational playbook for diagnosing the structural and technical layer of a site or page: crawlability (robots.txt), indexability (meta robots, canonicals), sitemap.xml validity, redirect chains, JSON-LD schema validation, Core Web Vitals interpretation, hreflang, JS-render parity, URL architecture, and internal-link topology. Encodes the fetch protocol (parallel webfetch + shell curl), the per-surface check rubric, the severity matrix (Critical / Moderate / Minor), and the unverified-check escalation rule. Use when auditing the technical layer of a URL, sitemap, or site. Output: prioritized structural findings with evidence and fix direction."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires webfetch (for HTML/JSON-LD/page response) and shell (for curl, sitemap parsing, optional Lighthouse/PSI). Optional: GSC and crawler-tool MCPs for richer signal."
domains: seo
rules:
  - session(seo)
  - session(audit)
  - content(audit)
  - content(crawlability)
  - content(indexability)
  - content(sitemap)
  - content(canonical)
  - content(schema)
  - content(robots.txt)
  - content(hreflang)
  - content(redirect)
  - match(\b(audit|diagnose|review|inspect)\s+.{0,40}(site|page|url|domain)\b)
  - match(\b(core\s+web\s+vitals|cwv|lcp|inp|cls)\b)
  - match(\b(schema|json-?ld|structured\s+data)\s+(audit|check|validate|review)?\b)
  - match(\b(crawl|index|render)\s+(issue|problem|error|gap|parity)\b)
  - match(\b(redirect\s+chain|canonical\s+(issue|tag)|hreflang)\b)
  - match(\b(technical\s+seo|structural\s+seo)\b)
  - semantic(diagnose technical SEO problems on this site)
  - semantic(check whether Google can crawl and index this page)
  - semantic(validate schema markup and structured data)
  - semantic(audit the technical layer for ranking blockers)
  - semantic(find structural SEO issues affecting visibility)
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

- `webfetch` the target URL — capture HTML, response headers, render the page if JS-heavy.
- `shell curl -sI <url>` — capture raw HTTP response and follow redirect chain (`-L` with `-w "%{redirect_url}\n%{http_code}\n"`).
- `shell curl -s <origin>/robots.txt` — fetch robots, parse `Allow` / `Disallow` / `Sitemap:` directives.
- `shell curl -s <origin>/sitemap.xml` — fetch sitemap; check for index file vs flat sitemap; spot-validate 5–10 URLs.
- `websearch site:<domain>` — sanity-check indexed page count and freshness.
- For JS-rendered sites: compare `webfetch` raw HTML vs a rendered fetch (skill `references/render-parity-check.md` if needed).

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
| 7 | Schema validity | JSON-LD parses; types match content (Article, FAQ, HowTo, Person, Organization, Product); required fields present | Moderate per missing/invalid type on eligible page |
| 8 | Core Web Vitals | LCP <2.5s (target <2.0s); INP <200ms; CLS <0.1 | Critical if any metric in Google's "poor" band; Moderate if "needs improvement" |
| 9 | hreflang | each variant points to the others bidirectionally; uses ISO codes | Moderate if asymmetric or broken; Critical if hreflang errors mean wrong region ranks |
| 10 | JS-render parity | primary content (title, H1, body) visible in raw HTML view-source | Critical if primary content only appears after hydration |
| 11 | URL architecture | descriptive slug, no query-string for canonical content, consistent trailing-slash policy | Minor unless duplicate content created |
| 12 | Internal-link topology | pillar links out to clusters in first section; cluster pages link back within first 100 words; ≤3 clicks from homepage | Moderate if orphan pages or broken pillar/cluster pattern |
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

- FAQ schema → check `mainEntity` array, each `Question` has `acceptedAnswer.Answer.text`. Highest single-impact schema for AI citation eligibility.
- Article schema → `headline`, `author` (Person with name + optional sameAs/url), `datePublished`, `dateModified`, `description`. Missing `author` on a YMYL page is a Critical-tier finding (March 2026 amplified author-credential signal — 73% of post-update YMYL top results display detailed author credentials, up from 58%).
- Person / Organization schema → required to anchor entity recognition for E-E-A-T. Missing `sameAs` outbound to LinkedIn / publication / org bio is Moderate.
- HowTo schema → `step` array with `name` + `text` per step. Cited for procedural queries.
- Review / AggregateRating → present only when genuine reviews back it; fake review-schema is a manual-action trigger.

### Core Web Vitals — interpretation, not measurement

This skill interprets CWV; it does not measure them. Source measurements:

- Field data: Google PageSpeed Insights, Search Console Core Web Vitals report, CrUX dataset.
- Lab data: Lighthouse CLI (`shell` capability), WebPageTest, browser DevTools.

When only lab data is available, flag the field-vs-lab gap; lab overstates good performance in many cases. INP needs field data — lab-only INP estimates are unreliable.

### Internal-link topology — what to look for

- Pillar pages should link out to every cluster article in their opening section (first 200 words).
- Cluster articles should link back to the pillar within the first 100 words.
- Cluster siblings should cross-link 2–3 times where topically relevant.
- Every indexable page should be reachable within 3 clicks from the homepage.
- Orphan pages (no internal inbound links) are a Moderate finding — they signal abandoned content or template gaps.
- The link graph should mirror the topic graph, not the navigation hierarchy.

### Output

Use the canonical output structure from the agent that runs this skill. Every finding includes: severity, evidence (URL + line / header / schema field / metric), why it matters, fix direction. Save as `seo-audit-[slug]-[YYYY-MM-DD].md` in working directory.

## Checklist

- [ ] All six fetch operations ran in parallel
- [ ] Every check in the rubric was evaluated or flagged as Unverified
- [ ] Each finding cites concrete evidence (URL, line, header, schema field, metric)
- [ ] Severity assigned by impact, not effort
- [ ] Unverified findings name the specific blocker and the unblock path
- [ ] Schema findings name the type and the missing/invalid field
- [ ] CWV findings name the source (field / lab / PSI) and the band (good / needs improvement / poor)
- [ ] Internal-link topology checked for pillar/cluster pattern and orphan pages
- [ ] Report saved to disk with timestamped filename

## Composition / References

Within-domain pairings:
- Pairs with the sibling SEO skill that audits on-page content quality (titles, meta, headings, intent match, AI-citability, E-E-A-T).
- Pairs with the sibling SEO skill that audits link profile (referring-domain quality, anchor distribution, toxic neighborhoods).

External authoritative sources:
- [Google Search Central — Crawling and indexing](https://developers.google.com/search/docs/crawling-indexing/overview)
- [Google Search Central — Structured data general guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)
- [Google Search Central — Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals)
- [Schema.org — full type vocabulary](https://schema.org/docs/full.html)
- [web.dev — INP](https://web.dev/articles/inp)
- [Google Search Central — hreflang](https://developers.google.com/search/docs/specialty/international/localized-versions)
