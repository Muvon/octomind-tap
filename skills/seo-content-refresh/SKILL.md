---
name: seo-content-refresh
title: "Content Refresh: Decaying Page Queue"
description: "Finds decaying pages, picks update, merge, redirect or remove, and briefs each refresh. Use to prioritize existing content and judge whether it helped."
license: Apache-2.0
compatibility: "Requires web search and page fetching. Decay diagnosis needs authorized Search Console access or a supplied performance export."
capabilities: websearch webfetch seo-data
domains: seo
rules:
  - match(\b(refresh|update|rewrite|republish|revamp)\w*\s+(\w+\s+){0,3}?(old|stale|existing|outdated|out-of-date)\s+(\w+\s+)?(content|posts?|pages?|articles?)\b)
  - match(\b(old|stale|existing|outdated|out-of-date)\s+(content|posts?|pages?|articles?)\b.{0,40}\b(refresh|update|rewrite|republish)\w*)
  - match(\bcontent\s+(decay|pruning|refresh)\b)
  - match(\b(decaying|decayed)\s+(content|pages?|posts?|articles?)\b)
  - match(\b(losing|lost|declining|dropping|falling)\s+(\w+\s+)?(traffic|clicks|rankings?)\b)
  - match(\b(traffic|clicks|rankings?)\s+(are\s+|is\s+|have\s+|has\s+)?(drop\w*|declin\w+|decay\w*|loss|fall\w*|fell)\b)
---

## Overview

This skill decides which existing pages need work, what kind of work, and how to tell whether it helped. It returns a prioritized refresh queue and, when planning, a brief per page. It never edits site files; writing the revision belongs to whoever owns the content. For judging a single page's quality, use `seo-content-audit`; this skill decides which pages deserve that effort.

## Mental model

Decay signal → cause → decision → priority → page brief → implemented change → logged review. Content decay means a page's clicks, impressions or rankings fall over time. A refresh is a change to what the page says, not to the date it shows. A traffic drop is an observation; the cause is a separate finding.

## Rules

### Data and its limits

- Primary input is authorized Search Console access or a supplied export (URL, query, clicks, impressions, CTR, position, date).
- Without it, audit public evidence only: dated claims, old statistics, prices, versions, screenshots, dead links. Mark decay Unverified. Missing data is Unknown, not zero.
- Search Console Web results include AI Overviews and AI Mode, so Web totals are not organic-only (Google, AI features, checked 2026-11-09). Don't infer AI-specific clicks from them.

### Find decay and separate causes

Compare two equal windows. For seasonal topics, also compare the same window last year. Flag a page when clicks fall by more than 20 percent across windows and the drop is not seasonal (practitioner default, not a Google threshold). Then split the cause:

| Pattern | Likely cause | Check |
|---|---|---|
| Impressions down | Demand fell, or indexing/canonical problem | Trends for the topic, URL inspection |
| Position down | Competitors improved, or the page aged or drifted from intent | Current top results, intent re-check |
| CTR down, position stable | SERP features or AI features take clicks, or snippet is weak | Live results capture, title and description |
| All flat but facts wrong | Hidden accuracy risk | Source check |

These are hypotheses until the evidence for the named cause is shown.

### Decide per page

| Decision | Evidence needed |
|---|---|
| Update | Page is the right target; facts or coverage have aged; intent unchanged |
| Expand a section | One named question in the current results is answered poorly or missing |
| Merge | Two or more pages compete for one intent in the queries data; name the survivor |
| Redirect | Page is obsolete but a close replacement exists |
| Remove | No traffic, links or purpose, and no replacement; confirm in backlinks and analytics first |
| Leave alone | Healthy, seasonal dip, or accurate evergreen page |

### What counts as a refresh

A refresh has at least one of: facts re-verified against primary sources, information added, intent re-checked against the current results. Changing only the date is not a refresh. Google lists "changing the date of pages to make them seem fresh when the content has not substantially changed" among signs of search-engine-first content (Google, helpful content, checked 2026-11-09). Change the visible date, `dateModified` and sitemap `lastmod` only when the main content changes; Google uses `lastmod` only if it is consistently and verifiably accurate, and counts main content, structured data and link updates as significant but a copyright-year change as not (Google, sitemaps, checked 2026-11-09). Visible and structured dates must match (Google, publication dates, checked 2026-11-09).

### Prioritize

1. Accuracy-sensitive pages first, whatever their traffic: pricing, policy, health, legal, security, version-specific.
2. Pages tied to buyer decisions, and pages cited in AI answers, especially citations graded Outdated or Contradicted in `geo-visibility-audit`.
3. Pages with measured traffic loss.

Within a tier rank by value, evidence, confidence, then effort. State each as high, medium or low with the reason; these are judgments.

### Freshness and AI answers

Evidence is correlational. Ahrefs (2025-07-28) analyzed about 17 million cited URLs: those cited by AI assistants averaged 1,064 days since publication against 1,432 for organic Google results, and 909 against 1,047 days since update. ChatGPT preferred newer pages most; Google AI Overviews cited pages slightly older than organic. Ahrefs notes cited pages still averaged about 2.9 years old and that low-quality pages gain nothing from frequent updates. Seer Interactive (2026-07-24) found 75 percent of dateable pages cited in ChatGPT, Gemini and Perplexity answers had been updated within a year. It studied cited pages only, with no uncited comparison group, covered four brands over four months, and could not tell minor edits from real ones. Neither study shows that updating a page raises its chance of citation. Both are vendor studies. Justify a refresh by accuracy and buyer value; treat any AI-freshness effect as unproven.

### Cadence

Refresh on triggers: a product, price or regulation change; a decay flag; a citation graded Outdated. For fast-moving topics a calendar check is a convention, not a requirement. Set no fixed monthly rewrite quota.

### Measurement log

Per refreshed page record: URL, change date, what changed, baseline windows, concurrent changes (site, algorithm, seasonality, other edits), review date, outcome. Allow time to recrawl before reviewing; 4 to 8 weeks is a convention, so say so and extend it for slow-crawled sites. Compare against equal windows and, when possible, against similar unrefreshed pages. An uncontrolled before/after supports no causal claim.

### Output

Respect the host role. In diagnostic mode, return a queue table (URL, evidence, cause, decision, priority, owner, review date) with one fix direction per page. In planning mode, start from an existing queue or supplied findings and add one brief per page: what is wrong with passage references; facts to re-verify with primary-source pointers; what to add; what to remove; what must stay (ranking sections, working links, accurate claims). Pages with no diagnosis go back for one. Save as `seo-refresh-[slug]-[YYYY-MM-DD].md`.

## Examples

- Wrong: "Traffic fell on 40 posts; update all of them monthly." Right: "Eleven posts lost over 20 percent of clicks in equal 90-day windows; nine show position loss to newer results, two show CTR loss at stable position. Brief the nine, test titles on the two."
- Wrong: "Set `lastmod` to today on every page so Google sees fresh content." Right: "Change `lastmod` and the visible date only on the three pages whose main content changed."
- Wrong: "No Search Console access, so decay is zero." Right: "Decay Unverified. Public evidence: the pricing table cites 2023 plans. Request a 16-month export to confirm."

## Checklist

- [ ] Data source named; absent data marked Unverified, not zero.
- [ ] Equal windows compared, with last year's window for seasonal topics.
- [ ] Cause stated separately from the drop, with its evidence.
- [ ] Each page has one decision from the table and its required evidence.
- [ ] Accuracy-sensitive pages ranked before traffic-loss pages.
- [ ] Dates change only where main content changes.
- [ ] No claim that freshness raises AI citations.
- [ ] Review dates and concurrent changes logged; no causal claim from before/after.
- [ ] Output saved with the dated filename; no site files edited.

## Composition / References

- `seo-content-audit` for page-quality scoring of a queued page; `geo-visibility-audit` for citation grading that feeds the queue.
- [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: creating helpful content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Google: publication dates](https://developers.google.com/search/docs/appearance/publication-dates)
- [Google: build a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Ahrefs: do AI assistants prefer to cite fresh content](https://ahrefs.com/blog/do-ai-assistants-prefer-to-cite-fresh-content/)
- [Seer Interactive: content recency and AI visibility](https://www.seerinteractive.com/insights/study-content-recencys-impact-on-ai-visibility-in-2026)

Sources reviewed 2026-11-09. The 20 percent threshold, the 4 to 8 week wait and calendar checks are practitioner conventions, not published rules.
