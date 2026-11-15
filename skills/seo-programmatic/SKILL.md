---
name: seo-programmatic
title: "Programmatic SEO Quality Gate and Rollout"
description: "Tests whether a template-page set (locations, integrations, comparisons) is worth building, then sets the rollout and kill rule. Use before scaling pages."
license: Apache-2.0
compatibility: "Needs the planned data source and template, or a live page set to review. Search Console access is needed for the rollout and kill checks."
capabilities: websearch webfetch seo-data filesystem-read filesystem-write
domains: seo
rules:
  - match((?i)\bprogrammatic\s+seo\b)
  - match((?i)\b(template|templated)\s+pages?\b)
  - match((?i)\b(thousands|hundreds)\s+of\s+(landing\s+)?pages\b)
  - match((?i)\b(pages?\s+at\s+scale|scale\s+(content|pages)|mass[\s-]generated?\s+pages?|pseo)\b)
  - match((?i)\b(location|city|integration|comparison|alternatives?)\s+pages?\s+(at\s+scale|template|generator)\b)
  - match((?i)\b(page|pages)\s+(for|per)\s+(every|each)\s+(city|location|integration|keyword)\b)
  - match((?i)\b(city|location)\s+pages\b)
---

## Overview

Programmatic SEO builds many pages from one template and a data set: a page per city, per integration, per product pair. It works when each page answers a real query with data that other pages lack. It fails, and risks Google's scaled content abuse policy, when pages differ only by a swapped word. This skill gives four gates a page set must pass before building, a rollout in batches, and a rule for stopping. It returns a go, fix or stop verdict with evidence.

## Mental model

A page set is a bet that many queries share one answer shape. Value comes from the data, not the template. Google's policy is about intent and value, not tooling: scaled content abuse is "many pages generated for the primary purpose" of manipulating rankings, "regardless of how" they are made, and it lists generative AI pages with no added value, stitched or scraped content, and synonymized feeds (Google, spam policies, checked 2026-11-15). The test is therefore: would each page earn a visit if search did not exist?

## Rules

### Gate 1: demand

Sample 20 pages from the planned set. For each, find the real query, its intent and its current top results. Pass line: at least 70 percent of the sample has a query with measurable demand (from a keyword-data tool or Search Console) and a results page where a page of this kind appears. The 70 percent line is a practitioner convention. Where demand data is unavailable, mark the gate Unverified, not passed.

### Gate 2: data source

| Check | Pass |
|---|---|
| Proprietary, licensed or first-party data | Yes; or a transformation of public data that adds a computed field or analysis |
| Scraped or copied from competitors or feeds | Fail |
| Data updated on a schedule | Owner and refresh date named |
| Each page has facts unavailable on sibling pages | At least three fields that differ in substance, not in name |

### Gate 3: template uniqueness

Render five pages from different parts of the set. Remove the swapped terms (city, product name) and compare the remaining text. Pass line: more than half of each page's main content is data or text specific to that entry, and a reader can use it without reading a sibling. Pages that read the same after the swap fail. Add per-entry elements the data supports: local figures, comparisons, ranges, charts, user-sourced facts. Adding a generated paragraph of filler is not uniqueness.

### Gate 4: site fit and crawl

- The set is reachable through links from category and hub pages, not only sitemaps; each page has a unique title and `<h1>`.
- URLs are stable, one per entry; filters and sort orders don't make new indexable URLs (Google: faceted navigation guidance recommends robots.txt rules or fragments for filters, and a 404 for combinations with no results).
- Crawl budget matters for sites with 1 million or more unique pages changing weekly, or 10,000 or more changing daily (Google, crawl budget guide); smaller sets mainly need clean internal linking.
- Pagination: each page has its own URL and canonical, linked with real `<a href>` links; Google no longer uses `rel=next` and `rel=prev`.

### Rollout

1. Ship a pilot of 50 to 200 pages from the strongest demand cluster. Batch sizes are a team convention.
2. Submit them in their own sitemap so the Page indexing report can be filtered to the set.
3. Review after 4 to 8 weeks (convention; extend for slow-crawled sites): indexed share, impressions, clicks, and the Page indexing statuses "Crawled - currently not indexed" and "Discovered - currently not indexed".
4. Expand by the next batch only if the pilot passes the kill rule below.

### Kill rule

Pause the rollout and fix, merge or remove pages when, after the review period, either holds: under half of the pilot pages are indexed, or most indexed pages have no impressions. Unindexed template pages can signal Google judged the set low in value; improve the data and content before adding pages. Remove pages with no demand or no unique data: noindex or delete them and, if they have links, redirect to the closest hub. Don't use `noindex` as a way to hide a set you still link to and submit.

### Measurement

Track at set level: pages published, indexed, receiving impressions, clicks, conversions, and the manual-action and Page indexing status. Don't claim a lift from a before and after without equal windows and a control.

## Examples

- Wrong: "Generate 20,000 'plumber in {city}' pages from one paragraph." Right: "Pilot 60 cities where the business has jobs, each with local pricing data, photos and named staff; hold the rest."
- Wrong: "Use an LLM to rewrite each page so they differ." Right: "Differences must come from data; reworded filler still fails Gate 3."
- Wrong: "Add all 3,000 integration pages to one sitemap and wait." Right: "Pilot 100 in a separate sitemap, review in 6 weeks, then decide."

## Checklist

- [ ] 20-page demand sample drawn; pass rate stated, or gate marked Unverified.
- [ ] Data source named, with owner, license and refresh date.
- [ ] Five rendered pages compared with the swapped terms removed.
- [ ] Hub and category links exist; filters do not create indexable duplicates.
- [ ] Pilot batch, separate sitemap and review date set.
- [ ] Kill rule agreed before launch.
- [ ] Verdict given as go, fix or stop with the failing gate named.

## Composition / References

- `seo-keyword-research` for per-page demand; `seo-structural-audit` for crawl and index diagnosis; `seo-google-policy-baseline` for the policy facts; `seo-local` for location pages.
- [Google: spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google: faceted navigation](https://developers.google.com/search/docs/crawling-indexing/crawling-managing-faceted-navigation)
- [Google: managing crawl budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget)
- [Google: pagination and incremental loading](https://developers.google.com/search/docs/specialty/ecommerce/pagination-and-incremental-page-loading)
- [Google: Page indexing report](https://support.google.com/webmasters/answer/7440203)
