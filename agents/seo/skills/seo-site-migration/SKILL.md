---
name: seo-site-migration
title: "SEO Site Migration Plan and Checklist"
description: "Plans and checks a domain move, HTTPS switch, replatform or URL restructure: baseline, redirect map, launch checks, monitoring. Use around a move."
license: Apache-2.0
compatibility: "Needs a crawl of the old site (or its sitemap) and, for monitoring, Search Console access on old and new properties. Shell with curl for redirect checks."
capabilities: websearch webfetch shell filesystem-read filesystem-write
rules:
  - match((?i)\b(site|domain|website)\s+(migration|move|relaunch|redesign)\b)
  - match((?i)\b(migrat\w+|mov\w+|switch\w*|replatform\w*)\s+(\w+\s+){0,3}(domain|platform|cms|shopify|wordpress|url\s+structure|to\s+https)\b)
  - match((?i)\b(redirect\s+map|301\s+map|url\s+mapping|change\s+of\s+address)\b)
  - match((?i)\b(rebrand\w*)\b.{0,40}\b(domain|url|seo)\b)
---

## Overview

A site move changes URLs, hosting, platform or domain while the site stays live for searchers. Done badly it drops traffic for months. This skill gives the order of work: measure the old site, map every old URL to a new one, check the launch, and watch the result. The output is a migration plan before launch and a verification report after. It does not build the redirects; developers do.

## Mental model

Search engines transfer a page's standing through one signal: a permanent redirect from the old URL to the equivalent new URL. Every old URL that has traffic, links or index entries must land on its closest equivalent in one step. Anything unmapped, redirected to the homepage or sent through a chain loses part of that transfer. Expect temporary ranking swings; the plan separates a normal settling period from a fault.

## Rules

### Classify the move

| Move | Change of Address tool in Search Console | Notes |
|---|---|---|
| Domain to a new domain, subdomain to another domain | Use it | Verify both properties first |
| HTTP to HTTPS, www to non-www, path changes on the same domain | Not needed (Google) | Redirects and sitemaps carry the move |
| Replatform with the same URLs | Not needed | Risk sits in rendering, canonicals, metadata |
| Restructure with new URLs | Not needed | Needs the full map |

Google advises splitting a large move into smaller parts when possible (Google, site moves with URL changes, checked 2026-11-15).

### Step 1: baseline the old site

1. Crawl the old site and list every indexable URL with status, canonical, title, H1, internal inlinks.
2. Export from Search Console the last 16 months of clicks and impressions by page and by query, and the top linked pages from the Links report. Add analytics landing pages and any backlink tool data.
3. Save robots.txt, sitemaps, hreflang and structured-data samples of the old site. Record the figures that define success: organic clicks, indexed pages, top 50 query positions.

### Step 2: build the redirect map

One row per old URL: old URL, new URL, redirect type, reason. Rules:

- Map each old URL to the closest equivalent page, one-to-one where one exists. Don't redirect everything to the homepage.
- Use a server-side permanent redirect: 301 or 308 (Google treats 308 like 301). Use a temporary 302 or 307 only for a real temporary move (Google, redirects).
- Where no equivalent exists, return 404 or 410, not a redirect to an unrelated page.
- Collapse chains: Googlebot follows up to 10 hops, and Google's site-move guide says to avoid chaining and aim for "ideally no more than 3 and fewer than 5", so map old URLs straight to final URLs (Google, site moves).
- Prioritize by clicks and referring domains: the top URLs by either must map and be tested by hand.
- Carry over parameters worth keeping, trailing-slash rules and case rules; decide them once.

### Step 3: prepare and test the new site

- Staging blocked by login, not only by `robots.txt`; remove the block at launch and check it was removed.
- Titles, headings, canonicals, hreflang, structured data and internal links match the old site's intent; internal links point to new URLs, not through redirects.
- New sitemap lists new URLs only. Keep the old sitemap reachable for a while so Google finds the redirects; Search Console warns about redirecting URLs in it, which Google says to ignore.
- Test the full map with `curl -sIL` in bulk: each old URL returns the expected status and lands on its target in one hop. Pass line: 100 percent of the top 100 old URLs, and 99 percent or more of all mapped URLs, resolve in one hop to a 200 page (a team-set convention, not a Google threshold).

### Step 4: launch day

1. Switch redirects live; confirm the new robots.txt allows crawling and no `noindex` carried over.
2. Submit the new sitemap; for domain moves, file Change of Address on the old property.
3. Request indexing of a few key new URLs with URL Inspection.
4. Re-crawl the new site; compare with the baseline crawl for lost titles, canonicals and links.

### Step 5: monitor

Watch Search Console on both properties, server logs for Googlebot hits on old and new URLs, and analytics: old-URL traffic should fall and new-URL traffic rise (Google, site moves). Review weekly for the first month and monthly after that. Expect fluctuation; Google says medium-sized sites can need a few weeks or more for new URLs to replace old ones, and large sites longer. Treat as a fault: rising 404s on mapped URLs, new URLs not crawled after a week, a canonical pointing back to the old domain, or a sustained drop past the settling period; then use `seo-traffic-drop-diagnosis`.

Keep redirects for at least one year, and longer where old URLs still earn links (Google, site moves). Update internal links and high-volume external links to the new URLs.

## Examples

- Wrong: "Redirect every old URL to the new homepage." Right: "Map 4,200 old URLs one-to-one; 310 with no equivalent return 410; top 100 by clicks verified by hand."
- Wrong: "Launch Friday, check traffic in a year." Right: "Baseline saved; weekly checks of redirect status, Googlebot log hits and Search Console for four weeks."

## Checklist

- [ ] Move type classified; Change of Address used only for a domain or subdomain change.
- [ ] Baseline crawl, 16-month Search Console export and success figures saved.
- [ ] Redirect map covers every indexable old URL, 301 or 308, one hop.
- [ ] No homepage catch-all; no-equivalent URLs return 404 or 410.
- [ ] Staging block removed at launch; no stray `noindex`.
- [ ] Redirect test run in bulk against the map with pass rates stated.
- [ ] New sitemap submitted; old sitemap kept reachable.
- [ ] Monitoring plan with dates and fault triggers; redirects kept at least a year.

## Composition / References

- `seo-structural-audit` for crawl, canonical and render checks on the new site; `seo-traffic-drop-diagnosis` when the post-move numbers fall.
- [Google: site move with URL changes](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes)
- [Google: redirects and Google Search](https://developers.google.com/search/docs/crawling-indexing/301-redirects)
- [Google: HTTP status codes, network and DNS errors](https://developers.google.com/search/docs/crawling-indexing/http-network-errors)
