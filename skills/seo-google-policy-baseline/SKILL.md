---
name: seo-google-policy-baseline
title: "Google Search Policy Fact Log"
description: "Dated log of Google Search facts: core and spam updates, site reputation policy, FAQ and HowTo status, AI report, llms.txt. Cite it, don't recall."
license: Apache-2.0
compatibility: "Requires web fetch to re-check the sources below. Facts are as of 2026-11-15."
capabilities: websearch webfetch
domains: seo
rules:
  - match((?i)\b(core|spam)\s+update\b)
  - match((?i)\bsite\s+reputation\s+(abuse|policy)\b)
  - match((?i)\b(faq|howto|how-to)\s+(rich\s+results?|schema|markup)\b)
  - match((?i)\bllms?\.txt\b)
  - match((?i)\b(generative\s+ai|ai\s+overviews?|ai\s+mode)\s+(report|performance|clicks|impressions)\b)
  - match((?i)\bscaled\s+content\s+abuse\b)
---

## Overview

Several SEO skills and agents quote Google policy and update facts. This skill holds one dated copy of each fact with its source, so the other files point here and do not carry their own. Use it to answer "what did Google say" and to date a claim before repeating it. Every fact below was read on the named Google page or on a news report of the status dashboard on 2026-11-15.

## Mental model

A policy fact has a value, a date and a source. When any of the three is missing, the fact is a rumor. Google announces on developers.google.com/search and on the Search Status Dashboard; third-party sites describe the effects. Keep the two apart: quote Google for what changed, label outside readings as readings.

## Rules

- Quote a fact from the log with its as-of date. When the task depends on it and a web tool is available, re-fetch the source first; the log is not live.
- A fact absent from this log is unverified. Look it up on a Google page before stating it.
- Don't turn a Google statement into a promise. "Not needed" means Google Search does not require it, not that other engines ignore it.

### Fact log (as of 2026-11-15)

| Topic | Fact | Source |
|---|---|---|
| Core updates 2026 | March update ran 27 March to 8 April; May update ran 21 May to 2 June. Google gave no specifics on what changed. Outside analyses that saw aggregation-model sites (comparison, directory, job board) lose are readings, not Google statements. | Search Status Dashboard; SEJ and Search Engine Roundtable completion reports |
| Spam updates 2026 | Dashboard-reported runs: March (24 to 25 March, under a day), June (24 to 26 June), August (18 to 21 August), September (24 September to 8 October). The August update was described as a normal update with no new policy. | Search Status Dashboard history as reported by Search Engine Roundtable, Search Engine Journal |
| Site reputation policy | Third-party content published mainly to use the host site's ranking signals breaks the policy. Since 30 August 2026 a manual action under it does not affect results shown in the EEA; the section may be treated separately and rank on its own merits. Outside the EEA a manual action affects results. Owners are still notified in Search Console. Post dated 28 August 2026. | Google Search Central blog 2026-08-28; spam policies |
| FAQ rich results | Stopped showing in Google Search from 7 May 2026; the feature documentation was removed 15 June 2026. Since August 2023 they had shown only for well-known government and health sites. `FAQPage` markup stays valid schema.org; leaving it is harmless. | Google structured data changelog; Search Central blog 2023-08-08 |
| HowTo rich results | Not shown on any device since 13 September 2023. | Search Central blog 2023-08-08 (updated) |
| Other retired rich results | Check the Search Central structured data changelog and search gallery live before calling any other type retired; this log verifies only FAQ and HowTo. | developers.google.com/search/docs/appearance/structured-data/search-gallery |
| Search Console AI report | The Generative AI performance reports launched 3 June 2026 and reached all sites by 31 August 2026. They count impressions of a site's URLs in generative AI features in Search and Discover; the post mentions no clicks. Dimensions: pages, countries, devices (Search only), dates. The data also stays in the overall performance report, so Web totals are not organic-only. | Google Search Central blog 2026-06-03 |
| AI features guidance | Google's guide "Optimizing your website for generative AI features on Google Search" (published 2026-05-15 per the Search Central documentation updates page; the guide page itself shows no date) says: no new machine-readable or AI text files, markup or Markdown are needed to appear, and Google Search ignores them, so an `llms.txt` neither helps nor hurts there; no content chunking; no special schema.org markup; seeking inauthentic mentions "isn't as helpful as it might seem"; many pages made to manipulate rankings or AI answers violate the scaled content abuse policy. | developers.google.com/search/docs/fundamentals/ai-optimization-guide; developers.google.com/search/updates |
| Scaled content abuse | Many pages generated mainly to manipulate rankings, "regardless of how" they are made; examples include generative AI pages with no added value, stitched or scraped content, and spreading it over several sites. | Google spam policies |
| Link spam | Names paid links, link exchanges, automated links, and optimized-anchor links in guest posts or press releases; paid links need `rel="sponsored"`. | Google spam policies, link spam |

## Examples

- Wrong: "Google's AI guide says llms.txt is useless." Right: "Google Search ignores `llms.txt` (AI features guide, May 2026); this says nothing about other engines."
- Wrong: "EEA sites are exempt from the site reputation policy." Right: "Since 2026-08-30 a manual action under it does not apply to EEA searchers; the policy and notifications remain."
- Wrong: "Search Console shows AI Overview clicks." Right: "The Generative AI report shows impressions; clicks sit inside the overall Web totals."

## Checklist

- [ ] Each fact quoted carries its date or "as of" month.
- [ ] A fact not in the log was checked on a Google page first, or marked unverified.
- [ ] Outside readings of updates are labeled as readings.
- [ ] No claim that Google ranks or ignores something that the sources do not state.
- [ ] Time-sensitive tasks re-fetched the source before relying on the log.

## Composition / References

- Used by `seo-structural-audit`, `seo-content-audit`, `seo-link-audit`, `seo-keyword-research`, `seo-backlink-prospecting`, `seo-guest-posting`, `seo-content-refresh`, `seo-programmatic`, `seo-traffic-drop-diagnosis`.
- [Google: AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: site reputation policy update, 2026-08-28](https://developers.google.com/search/blog/2026/08/update-site-reputation-policy)
- [Google: Generative AI performance reports, 2026-06-03](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)
- [Google: FAQ structured data](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [Google: FAQ and HowTo changes, 2023-08-08](https://developers.google.com/search/blog/2023/08/howto-faq-changes)
- [Google: spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [Google Search Status Dashboard](https://status.search.google.com/)
- [SEJ: March 2026 core update complete](https://www.searchenginejournal.com/google-confirms-march-2026-core-update-is-complete/)
- [Search Engine Roundtable: May 2026 core update done](https://www.seroundtable.com/google-may-2026-core-update-done-41435.html)
