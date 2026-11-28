---
name: seo-site-audit
title: "SEO Site Audit: Prioritized Evidence Report"
description: "Runs an SEO audit over technical, on-page and link surfaces and saves a severity-ranked, evidence-cited report. Use when asked to audit a site or URL."
license: Apache-2.0
compatibility: "Requires web fetch and web search; shell with curl for headers, redirect chains, robots.txt and sitemaps. Search Console data is optional and must be supplied or authorized."
capabilities: shell
rules:
  - match((?i)\b(audit|diagnos\w+|triage|analy[sz]e|inspect|perform|check|review)\b.{0,90}\b(json-?ld|markup|schema|robots\.txt|sitemap|hreflang|redirect|title\s+tags?|meta\s+descriptions?|anchor|backlinks?|link[- ]profile|referring|crawl|indexation|rendering|raw\s+html|seo|content\s+decline|visibility\s+gap|cited|citations?)\b)
  - match((?i)\b(diagnos\w+|audit|analy[sz]e)\b.{0,60}\b(ai[- ]search|ai\s+answers?|captured\s+(ai\s+)?answers?|perplexity|chatgpt)\b)
  - match((?i)\b(run|perform|do)\s+an?\s+(full\s+)?(seo|site|website)\s+audit\b)
  - match((?i)\b(redirect\s+chains?|crawl\s+budget|core\s+web\s+vitals|orphaned|js-render|referring-domain|backlink\s+profile|technical\s+seo\s+audit|on-page\s+content\s+audit)\b)
  - match((?i)\b(pasted|captured)\b.{0,30}\b(chatgpt|perplexity|gemini|ai)\s+(generated\s+)?answers?\b|\b(brand|we|our)\b.{0,60}\b(missing|misrepresented|described\s+incorrectly)\b.{0,60}\b(ai|answers?|cited)\b|\bmisrepresented\b.{0,60}\bai\b)
  - match((?i)\bwhat('?s|\s+is)\s+wrong\s+with\s+(my|our|the)\s+(seo|site|website|page)\b)
  - match((?i)\b(dropped|lost|fell|declin\w+)\b.{0,50}\b(google|page\s+one|traffic|rankings?)\b.{0,80}\b(technical\w*|on-page|why|cause)\b)
  - semantic(check redirects, sitemap, robots and structured data on this domain, 0.71)
  - semantic(audit our backlink profile and on-page titles and descriptions, 0.69)
  - semantic(check page speed, crawlability and mobile rendering for my website, 0.69)
---

## Overview

This skill runs the ordinary audit of an existing asset: a URL, a sitemap, a set of pages or a whole site. The outcome is a prioritized list of what is broken, why it matters and what to fix first, saved as one report. Every finding ties to something fetched or measured. The skill produces findings only: strategy briefs, content drafts, outreach copy and implementation patches are separate work.

## Mental model

An audit without evidence is an opinion. Observation and consequence stay separate: a missing keyword is observable, but it is not by itself proof of a ranking problem. A check that could not run is reported as unverified, with the way to unblock it.

## Rules

### Choose the mode

| Request | Mode |
|---|---|
| GEO, AEO, AI visibility, missing recommendations, citation gaps | Apply the `geo-visibility-audit` skill in audit mode. Scope to the buyer questions and surfaces requested, check existing pages before proposing new ones, and return its GEO report with fix directions and retest conditions. If no question set exists, derive a small provisional set from the buyer decision and label the hypotheses. Without actual engine captures, report visibility as Unverified and audit only the public evidence. Do not run the three-surface procedure below unless asked. |
| Old, decaying or out-of-date content | Apply the `seo-content-refresh` skill in diagnostic mode and return its queue with cause, decision and fix direction per page. Without Search Console data, mark decay Unverified and check public evidence only. |
| Sudden or site-wide loss of traffic or rankings | Apply `seo-traffic-drop-diagnosis` before any page-level work. |
| Domain move, replatform, HTTPS switch, URL restructure | Apply `seo-site-migration` to check the redirect map, launch state and monitoring. |
| Business with a storefront or service area | Apply `seo-local`. |
| Live set of template-generated pages | Apply `seo-programmatic`. |
| Anything else | The ordinary audit below. |

Dated Google policy facts come from the `seo-google-policy-baseline` skill; don't quote them from memory.

### Ordinary audit procedure

1. Parse the target: single URL, sitemap, set of URLs or full site. If unclear, ask one question. A sitemap or site given without coverage instructions means sampling 5 to 10 representative URLs.
2. Decide which surfaces apply. Most audits run all three: structural (see `seo-structural-audit`), on-page content (`seo-content-audit`) and link profile (`seo-link-audit`). If the user names a surface ("just structural", "just link profile"), scope to it.
3. Fetch the evidence in parallel: `knowledge(command="read", source="<url>")` for the pages and competitor pages, shell curl for headers, redirect chains, robots.txt and sitemap.xml, web search for the ranking competitors. Google-only SERP features (AI Overviews, AI Mode, People Also Ask, featured snippets, ad counts) stay Unverified unless the user supplies a screenshot or Search Console data.
4. Run the checks: structural (validate JSON-LD, parse headers, walk the redirect chain, raw-HTML content check if JavaScript-heavy), on-page (heading, intent, answer-placement and E-E-A-T rules), link profile (site: patterns, competitor discovery, anchor sampling).
5. Score each finding: Critical is ranking-blocking or an indexability failure; Moderate is signal degradation; Minor is polish.
6. Write the report and save it.

Memory: before auditing, `remember` the site profile, past audits, known issues and fixes already attempted, so the report does not re-flag what the user knows. Afterwards `memorize` issue patterns, recurring weak spots, the audit date and the severity distribution.

### Evidence and severity rules

- If a check fails to run (403, JavaScript render blocked, no Search Console access, rate limit), flag it as unverified. Do not infer or guess.
- Prioritize by demonstrated buyer impact, demand evidence, confidence and dependencies, not ease or warning count. Issue severity stays separate from scheduling priority: a Critical issue stays Critical even if it is one tag.
- One issue per finding; cite the affected passage and consequence. Don't turn character counts or exact-match keyword placement into automatic defects.
- Core Web Vitals: LCP 2.5 s or less, INP 200 ms or less (INP replaced FID in March 2024), CLS 0.1 or less, judged on field data at the 75th percentile (CrUX or Search Console). Lab-only numbers are directional; say which you have.
- Information gain on on-page audits: if an LLM reading the current top 10 could reconstruct the page, flag it as information-gain-zero. This is a practitioner heuristic: Google asks for helpful, first-hand content but documents no information-gain ranking system, so label the finding that way.
- Primary-source bias: a page that only summarizes other sources is a Critical content finding by this heuristic. Third-party readings of the 2026 core updates saw aggregation-model sites lose, but Google gave no specifics.
- Schema: Google AI features need no special schema, `llms.txt` or chunking, and FAQ and HowTo rich results are retired. Check the search gallery live for other types. Flag invalid markup or markup that contradicts visible text; missing schema is Moderate only where a live rich result is at stake or Copilot or Bing shopping is in scope.
- Inauthentic mentions: flag manufactured-mention patterns as risk, not strength.
- Reddit and forums are not a ranking signal, but they hold many SERP slots and AI-answer citations. Audit community presence as visibility inside the link-profile surface.
- Any dofollow placement that should carry rel=sponsored is Critical: Google's link spam policy names paid links and optimized-anchor links in guest posts and press releases.
- Site reputation policy: its manual actions no longer apply to EEA searchers; name the region when flagging.
- Search Console's Generative AI report counts impressions, not clicks, and Web totals include those impressions. Don't label Web totals organic-only or infer AI-specific clicks. Keep actual answer captures and publisher or vendor reports separate.
- Never fabricate competitor URLs, DR numbers or backlink counts: verify through live search or mark as estimate.

## Examples

Unverified check:
- Bad: "The sitemap is probably fine."
- Good: "Could not fetch /sitemap.xml (403). Flagged as unverified; unblock by allowing the fetch or supplying the file."

Severity:
- Bad: "Minor: noindex on the pricing page, easy fix."
- Good: "Critical: meta robots noindex on /pricing (fetched HTML, line 14). Ranking-blocking; the fix being one tag does not lower the severity."

## Output format

For GEO work use the report and filename from the `geo-visibility-audit` skill; for a content refresh use the report and filename from `seo-content-refresh`. The template below is for ordinary SEO audits. Save it as `seo-audit-[slug]-[YYYY-MM-DD].md` in the working directory.

```markdown
# SEO Audit: [URL or Site]
Date: YYYY-MM-DD
Surfaces audited: Structural ✅ / On-page ✅ / Link Profile ✅

## 🔴 Critical (ranking-blocking — fix first)
1. [Issue] — [evidence: URL, line, schema field, status code] — [why it matters] — [fix direction]

## 🟡 Moderate (signal degradation — fix soon)
1. [Issue] — [evidence] — [why it matters] — [fix direction]

## 🟢 Minor (polish — fix when convenient)
1. [Issue] — [evidence] — [fix direction]

## ✅ What's Working
- [Strength with evidence]

## ❓ Unverified (check could not run)
- [Check] — [reason: 403, JS-render block, no GSC access, etc.] — [how to unblock]

## Surface Detail

### Structural / Technical
- Crawlability: [robots.txt allows: yes/no/partial]
- Sitemap: [present at /sitemap.xml ✅/❌] — [N URLs, last-modified valid yes/no]
- Indexability: [meta robots: index, follow ✅/❌] — [canonical tag: self-referential ✅/❌]
- Redirect chains: [N hops detected on URL X, terminal Y]
- Schema markup: [JSON-LD types found: Article/FAQ/etc] — [validation: pass/fail per type]
- Core Web Vitals: [LCP X.Xs, INP XXXms, CLS X.X] — [source: PSI / field / lab]
- hreflang: [present ✅/❌ — N variants validated]
- JS-render parity: [primary content visible in raw HTML ✅/❌]
- Internal-link topology: [pillar/cluster pattern present ✅/❌] — [N orphan pages]

### On-Page Content
- Title: [served text; accurate, concise, and distinct? cite any mismatch]
- Meta description: [served summary; page-specific and faithful to content?]
- H1 / H2 structure: [H1 present and unique ✅/❌, headings describe their sections ✅/❌]
- Intent match: [page intent vs SERP-dominant intent]
- Answer placement: [key answer stated early in its section: N of M]
- E-E-A-T: [author byline + credentials + outbound link ✅/❌] — [experience proof: original media / time-boxed case / named tools+versions ✅/❌]
- Information gain vs top 10: [novel data / contrarian take / original synthesis — present or reconstructable-from-top-10]
- Schema: [types found] — [valid ✅/❌, matches visible text ✅/❌, live rich result at stake: list]

### Link Profile
- Referring domains (unique root): [N] — [DR distribution, topical-fit assessment]
- Anchor distribution: [branded %, partial-match %, exact-match %, generic %]
- Toxic-neighborhood flags: [N suspect domains, evidence]
- Link gap vs [competitor]: [N domains link to them, not you — top 10 listed]
- Community / forum presence: [Reddit + relevant communities — present/absent]
```

## Checklist

- [ ] The mode matches the request (GEO, refresh, traffic drop, migration, local, programmatic or ordinary).
- [ ] Every finding cites a URL, line, schema field, header, status code, metric or SERP reference.
- [ ] Every check that did not run is listed under Unverified with a way to unblock it.
- [ ] Severity follows the Critical, Moderate and Minor definitions, not ease of fix.
- [ ] No competitor figure, DR number or backlink count is unverified or unmarked as an estimate.
- [ ] The report is saved under the expected filename and the path is returned.
- [ ] No fix, content draft or strategy was drifted into: findings only.

## Composition / References

- `seo-structural-audit`, `seo-content-audit` and `seo-link-audit` hold the per-surface checks.
- `geo-visibility-audit`, `seo-content-refresh`, `seo-traffic-drop-diagnosis`, `seo-site-migration`, `seo-local` and `seo-programmatic` cover the special modes in the table above.
- `seo-google-policy-baseline` is the source for dated Google facts.
