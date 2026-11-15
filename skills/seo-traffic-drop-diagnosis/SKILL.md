---
name: seo-traffic-drop-diagnosis
title: "Organic Traffic Drop Diagnosis"
description: "Diagnoses a sudden organic traffic or ranking drop: data checks, Search Console segmenting, update alignment, cause table. Use before fixing anything."
license: Apache-2.0
compatibility: "Needs authorized Search Console access or a supplied export; GA4 export optional. Without them the diagnosis stays Unverified."
capabilities: websearch webfetch seo-data
domains: seo
rules:
  - match((?i)\b(traffic|clicks|impressions|rankings?)\s+(just\s+|suddenly\s+)?(drop\w*|fell|fall\w*|crash\w*|tank\w*|declin\w+|plummet\w*)\b)
  - match((?i)\b(traffic|clicks|impressions|rankings?|visibility)\s+(is|are|was|were|has|have|had)\s+(\w+\s+){0,2}(down|dropped|fallen|declined|halved|tanked)\b)
  - match((?i)\b(lost|losing|dropped|dropping)\s+(\w+\s+){0,2}(traffic|rankings?|visibility)\b)
  - match((?i)\b(core|spam|algorithm)\s+update\b.{0,60}\b(hit|drop|lost|recover\w*)\b)
  - match((?i)\b(recover|recovery)\b.{0,40}\b(core\s+update|penalty|manual\s+action|traffic)\b)
  - content(deindexed)
  - content(de-indexed)
---

## Overview

This skill finds why organic traffic fell before anyone changes the site. It returns one cause per segment of the drop, the evidence for each, and the next action. Most drops are not penalties: they are tracking breaks, technical faults, site moves, seasonality or lost demand. It stops at diagnosis. Rewriting pages belongs to `seo-content-refresh`; fixing a faulty template or redirect belongs to the people who own the code.

## Mental model

A drop is a difference between two windows, split by what changed. Work from the cheapest, most mechanical causes to the most uncertain: reporting, then technical, then site changes, then demand, then Google systems. Algorithmic cause is a conclusion reached by elimination plus date alignment, not a first guess. Google's own debugging procedure follows the same order (Google, debugging traffic drops, checked 2026-11-15).

## Rules

### Step 1: confirm the drop is real

1. Read the Search Console Data Anomalies page for logging or processing issues on the dates.
2. Compare Search Console clicks with analytics sessions from organic search for the same dates. Search Console down and analytics down: real. Search Console flat and analytics down: suspect tracking (tag removed, consent banner change, cross-domain or redirect stripping the referrer, a changed channel grouping). Name which tracking change you checked.
3. Confirm the window. Set the report to "Last 16 months" to see whether the same dip appears each year (Search Console keeps 16 months; use the API or bulk export to keep more).

### Step 2: segment the drop

Compare equal periods, and the same period last year for seasonal topics. Check every tab:

| Cut | Question |
|---|---|
| Search type (web, image, video, news) | Did the drop sit in one type? |
| Page group | Site-wide, a template, a folder, or single pages? Sort the Pages table by clicks difference. |
| Query group | Brand versus non-brand; head terms versus long-tail. |
| Country and device | One market or one device only? |
| Impressions versus clicks versus position | Impressions and clicks both down, or only clicks? |

Impressions held and clicks fell: the snippet, the title or a SERP feature changed; it is not a ranking loss. Search Console AI reports count impressions only, so don't attribute click loss to AI features without a dated live capture (`seo-google-policy-baseline`).

### Step 3: match the pattern to a cause

| Pattern | Likely cause | Evidence to collect |
|---|---|---|
| Sudden, site-wide, all queries | Server errors, robots.txt block, sitewide `noindex`, expired certificate | Crawl stats, Page indexing report, `curl -I` on sample URLs, robots.txt history |
| Gradual, some pages | Page-level `noindex`, canonical changes, pages dropped from the index | URL Inspection on a sample, Page indexing statuses |
| Starts the day URLs changed | Site move or migration fault | Redirect map, old URLs in logs; use `seo-site-migration` |
| Whole topic down across the web | Demand fell or season ended | Google Trends against your top queries |
| Small position drops (for example 2 to 4) across many queries, dated within a confirmed update window | Algorithmic re-evaluation | Update dates in the dashboard; competitor positions; page-quality review |
| Large position drops (for example 4 to 29) on a page group | Algorithmic, or a spam-policy action | Manual Actions report first; then update dates |
| Manual Actions report lists an action | Manual action | The report text; its listed pages |
| Malware or phishing warnings | Security issue | Security Issues report |
| Specific query groups lost to new URLs | Competitor displaced you | Live results capture before and after |

The position examples come from Google's debugging guide. A manual action shows in the Manual Actions report; if the report is empty, don't call the drop a penalty.

### Step 4: align with updates, carefully

Place the drop's start date against Google's confirmed update windows in `seo-google-policy-baseline`. An overlap alone is a hypothesis: also rule out the technical and site-change rows above. Google says changes can take a few days to several months to show and to wait a few weeks after a fix before re-analyzing; helpful-content improvements can take months to register (Google, debugging traffic drops). Google gives no recovery timetable and no "recovery update" trigger, so don't promise one.

### Step 5: decide

| Diagnosis | Action | Owner |
|---|---|---|
| Tracking fault | Fix tags; annotate the gap; restate the numbers | Analytics owner |
| Technical fault | Fix and request recrawl of key URLs | Developers |
| Site move fault | Repair redirects and canonicals | Developers, `seo-site-migration` |
| Seasonal or demand | No fix; set expectation with the prior-year line | Owner |
| Manual action | Fix the cause, submit a reconsideration request | Site owner |
| Algorithmic, page group | Brief per-page work with `seo-content-refresh` after a quality review with `seo-content-audit` | Content owner |
| Cause unknown | State what is missing and name the next data to pull | Requester |

## Examples

- Wrong: "A core update hit us; rewrite everything." Right: "Clicks fell 41 percent on 3 June across `/blog/`, impressions flat, Search Console and analytics agree; no technical change; the drop starts the day after the May update ended. Hypothesis: algorithmic. Next: review the top 20 lost pages against the current results."
- Wrong: "Traffic is down; disavow the links." Right: "Manual Actions report is empty and the drop is in one country only; check hreflang and redirects first."

## Checklist

- [ ] Data Anomalies page checked; Search Console and analytics compared.
- [ ] Equal windows compared, with last year's window for seasonal topics.
- [ ] Drop segmented by type, page group, query group, country, device.
- [ ] Manual Actions and Security Issues reports read, or marked Unverified.
- [ ] Technical and site-change causes ruled out before an update is named.
- [ ] Update overlap stated as a hypothesis with its dates.
- [ ] One cause, evidence, owner and next action per segment.
- [ ] No recovery timetable promised.

## Composition / References

- `seo-structural-audit` for the technical checks; `seo-content-refresh` for per-page decay briefs; `seo-google-policy-baseline` for update dates.
- [Google: debugging drops in Search traffic](https://developers.google.com/search/docs/monitor-debug/debugging-search-traffic-drops)
- [Google: Search Status Dashboard](https://status.search.google.com/)
- [Google: Manual actions report](https://support.google.com/webmasters/answer/9044175)
