---
name: content-formats
title: "Blog Formats: Choosing by Search Intent"
description: "Blog post formats by search intent: a playbook for articles and blog posts. Read the live results page, classify intent, and pick the format: how-to, best-of list, X vs Y comparison, alternatives page, single review, guide or pillar, glossary entry, original data study, case study, FAQ page, template or checklist, calculator-style page, news update, or opinion piece. Each format comes with its required elements and failure modes. Also covers collecting first-hand experience from the author instead of inventing it, methodology and disclosure notes, depth without word-count targets, titles and intros, honest dates, and refreshes. Use when planning, outlining, drafting, or refreshing a piece meant to rank in Google and Bing and be cited by AI answer engines."
license: Apache-2.0
compatibility: "Web search and page fetch for competitor and source pages; Google-only results features need a user screenshot, Search Console data, or a SERP-data tool."
domains: content
rules:
  - session(article)
  - session(blog)
  - content(listicle)
  - content(glossary)
  - content(pillar)
  - content(tutorial)
  - content(alternatives)
  - match(\b(search|user|query)\s+intent\b)
  - match(\b(which|what|right|best)\s+(content\s+|article\s+|post\s+)?format\b)
  - match(\bhow[-\s]to\s+(guide|article|post|tutorial)\b)
  - match(\b\w+\s+(vs\.?|versus)\s+\w+\b)
  - match(\b(best|top)\s+\d+\b)
  - match(\b(comparison|case\s+study|data\s+study|original\s+research|product\s+review|buying\s+guide)\b)
  - semantic(which format should this article use)
  - semantic(write a comparison of two products)
  - semantic(refresh an outdated article so it ranks again)
  - semantic(write a how-to guide for this task)
---

## Overview

Pick the page format the searcher expects before writing a word. Google, Bing, and the AI answer engines that build on their indexes reward the page that does the searcher's task best, and the task decides the shape: steps for a how-to, a verdict and a table for a comparison, a definition in the first sentence for a glossary entry. Use this skill when planning, outlining, drafting, or refreshing an article or blog post meant to rank and be cited. Answer-first passage craft and crawler setup live in `content-geo`; claim verification lives in `content-grounding`.

## Mental model

Three questions settle a piece: what the searcher wants to do (know, compare, decide, do, go), what shape the current results page rewards, and what this author can add that the ranking pages lack. Format follows the first two; whether to publish at all follows the third. Google's AI guide frames the third as commodity versus non-commodity content: a page "based on common knowledge, which could originate from anyone" competes with every other page and with the AI answer itself, while "unique expert or experienced takes" give engines a reason to cite it. Experience is evidence the author holds (tests, photos, data, decisions, failures), never a tone the writer adds.

## Rules

### Read the results page first

1. Classify intent from the query and its results, not the keyword alone: Know (explain), Know Simple (one-line answer), Do (task, download, calculate), commercial investigation (compare, choose), Website (a specific brand or page), Visit (local). A query can carry two.
2. In the top 10, note the dominant content type (guide, list, product page, tool), format (steps, table, list, essay), and angle (for beginners, cheapest, tested, this year). Match the type and format; differ on the angle.
3. Note the features: AI Overview, People Also Ask, Discussions and forums, video, shopping, Top stories. The web search tool is not Google; Google-only features stay unverified without a screenshot, Search Console data, or a SERP-data tool.
4. Note the dates on ranking pages. Breaking news, recurring events, current prices, and product models need fresh pages; evergreen explanations do not.
5. Name the gain this piece adds in one sentence. If you can't, report that before drafting instead of writing a commodity page.

### Format by intent

| Intent signal | Format | Must include | Fails when |
|---|---|---|---|
| "how to", "set up", "fix" (Do) | How-to / tutorial | Prerequisites, numbered steps with the expected result after each, troubleshooting for the errors people actually hit, versions tested | Setup prose before step 1; steps nobody on the team ran |
| "best", "top N" (commercial) | Best-of list | Selection criteria and a how-we-chose or how-we-tested note; per pick: who it suits, key facts, price with an as-of date, one drawback, first-hand evidence | Paraphrased manufacturer specs; your own product ranked first without disclosed criteria |
| "X vs Y" (commercial) | Comparison | Verdict in the first screen, comparison table, "choose X if / choose Y if", where each loses, test data or sourced specs | A hedged no-verdict ending; undisclosed affiliation |
| "alternatives to X" (switching) | Alternatives page | Why people leave X, criteria, X's real strengths, when not to switch, disclosure of who wrote it | One templated page per competitor |
| "[product] review" | Single review | Own photos or screenshots, measurements, benefits and drawbacks from own use, comparison to rivals and to the previous model, who should skip it | Reviewing a product nobody on the team used |
| Broad topic, many sub-questions (Know) | Guide / pillar | One section per real sub-question, each answering first and standing alone; table of contents; links to deeper cluster pages | Padding to a length target; duplicating what cluster pages cover in full |
| "what is X" (Know Simple) | Glossary / definition | Definition in the first sentence, then what the one-line answer can't give: example, misconception, edge case, related terms | A page that is only the definition; mass-produced term pages |
| "statistics", "benchmark", "survey" | Data study | Method up front: sample, dates, tools, limits; key numbers in HTML text and tables; charts with a text summary; downloadable data; a named author | Data shown only in images or PDFs; numbers without a denominator |
| "case study", "how [company] did X" | Case study | Starting point, what was done, measured result with timeframe, what failed, named customer with permission, what results are typical | Exceptional results presented as typical; undisclosed incentives |
| Many short related questions | FAQ page | Real customer or support questions; each answer's first sentence stands alone | Boilerplate questions written to hold keywords |
| "template", "checklist", "example" (Do) | Template / checklist | The usable artifact in HTML, a filled-in example, how to adapt it | Core content only inside a PDF or image |
| "calculator", "estimate", "how much" (Do) | Calculator-style page | Your own logic with formula, assumptions, and sources visible; a worked example; limits; expert review on money or health topics | An embedded third-party widget with nothing added; near-identical variants per city or number |
| Recent event or release | News / update | Visible date and byline, what changed and when, what it means for the reader, link to the primary announcement | Re-dated old posts; speculation stated as fact |
| Contested question, strategy | Opinion / analysis | Clear thesis, the author's credentials or stake, evidence per claim, the strongest counterargument | Generic takes; claimed expertise the author lacks |

Mixed results page: serve the dominant format and cover the runner-up in a section. Forum threads on top: searchers want lived experience, so lead with the author's own account or recommend joining those communities over another explainer.

### Experience comes from the author

- First-hand claims ("we tested", "I ran", "in our account") need the author's record: notes, data, screenshots, logs, or that person's explicit account. Researching a product is not using it. Google's rater guidelines rate a page built on "a false claim of personal, independent testing" Lowest and overstated experience Low; the FTC's 2024 rule bans reviews from people without actual experience.
- Before drafting a format that needs experience (review, comparison, best-of, how-to, case study), ask the author once, as a short list: what they did and when, versions and settings, numbers, what went wrong, photos or screenshots, who else was involved.
- If the author can't supply it, change the format (reported synthesis, interview, labelled opinion), add a named expert's input with consent, or leave a placeholder such as `[FIRST-HAND: result of the 30-day test]` in internal drafts. Placeholders never ship.
- Tests, rankings, and reviews carry a methodology note: who tested, what was bought or provided free, how long, the weighted criteria, what was excluded, when it was last re-checked.
- Images: write a shot list of original screenshots or photos, captioned with what each proves. Stock images prove nothing; alt text describes the image, not keywords.
- How the piece was made: Google suggests AI or automation disclosure where readers would reasonably ask "How was this created?" Be specific about what the AI did, what a human checked, and which sources were used; in trust studies, vague AI labels cost more reader trust than disclosures that list sources.
- Bylines name a real person with a bio page and credentials that fit the topic; money and health topics need fitting credentials or a named expert reviewer. Never invent authors, credentials, or headshots.

### Depth, titles, and intros

- No word-count targets. Google's self-assessment asks whether you write to a word count because Google prefers one, and answers "(No, we don't.)" Cover what the task needs, match the scope of pages that satisfy the query, add the gain, and cut sections that only restate them.
- Title tag: the page's real promise, specific, not exaggerated, with a year only if the content was re-checked for that year. Google sets no length limit but truncates by width and rewrites boilerplate, inaccurate, or stuffed titles. Keep the H1 close to the title.
- Meta description: a unique one- or two-sentence summary of what the page delivers. Google builds most snippets from page content, so the intro matters more.
- Intro: the answer, verdict, or result first, then who it's for and why to trust it, in a few sentences. Bing's guidelines ask for essential information near the top, and usability research shows readers scan the first lines and headings.
- Headings say what the section answers; specific beats clever.
- Internal links go only to real pages the user supplied or the sitemap lists, with descriptive anchors. Never invent internal URLs; write `[internal link: topic]` when the URL is unknown.

### Dates and refreshes

- Show "Published" and, after a substantive change, "Last updated"; keep `datePublished` and `dateModified` in sync with them. Google's self-assessment flags changing dates "when the content has not substantially changed."
- Refresh when facts, prices, versions, screenshots, or the results-page format have changed, or when impressions hold while clicks fall. Keep the URL and the original intent, re-verify every dated claim, add what changed, and list the changes.
- Prefer updating or consolidating a weak page over publishing a near-duplicate; Google's core-update guidance calls deleting content a last resort.

## Examples

Query "notion vs obsidian for research notes". Wrong: a long explainer of each app ending "it depends on your needs". Right: a two-sentence verdict; a table of sync, offline use, price with an as-of date, plugins, and export; "choose Notion if / choose Obsidian if"; where each failed in the author's own six-week trial, with screenshots; a no-affiliation disclosure.

Query "what is a canary deployment". Wrong: the definition restated five ways to reach a length. Right: the definition first, then the rollout percentages and rollback trigger the team actually uses and the two failures they hit.

Experience. Wrong: "We tested 12 VPNs for 30 days" when the brief contains no test. Right: ask the author for the test log; if none exists, retitle as "12 VPNs compared on published audits and pricing" with sources and an as-of date.

## Checklist

- [ ] Intent classified; dominant type, format, and angle of the top results noted; Google-only features marked unverified without evidence.
- [ ] Format chosen from the table, its must-include elements present, its failure modes absent.
- [ ] The gain over ranking pages named in one sentence and visible in the first screen.
- [ ] Every first-hand claim traces to the author's record; missing experience led to a format change or a placeholder, never invention.
- [ ] Tests, rankings, and reviews carry a methodology note; affiliations and AI assistance disclosed where readers would ask.
- [ ] No word-count padding; title, H1, intro, and headings state the real promise.
- [ ] Internal links point only to known URLs.
- [ ] Dates visible and honest; a refresh re-verified facts and listed what changed.

## Composition / References

Same-domain skills: `content-geo` (answer-first passages, crawlers, AI citation), `content-grounding` (claim triage and sources), `content-voice` (register and first-person ownership). Keyword selection and clustering belong to the SEO domain; this skill starts from a chosen query.

Reviewed 2026-10-24. This is a review date, not a publication date for the sources below.

- [Google: people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) (updated 2026-10-05): word count, dates, bylines, AI disclosure, fabricated creator profiles.
- [Google: optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) (published 2026-05-15, updated 2026-07-10): commodity content, no ideal page length.
- [Google: Write high quality reviews](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews) (updated 2025-12-10).
- [Google Search Quality Rater Guidelines](https://static.googleusercontent.com/media/guidelines.raterhub.com/en//searchqualityevaluatorguidelines.pdf) (2025-09-11): 3.4 experience, 4.5.3 false testing claims, 4.6.6 low-effort AI content, 5.6 overstated experience, 12.7 intent, 18 freshness.
- Google [title links](https://developers.google.com/search/docs/appearance/title-link), [snippets](https://developers.google.com/search/docs/appearance/snippet), [byline dates](https://developers.google.com/search/docs/appearance/publication-dates), [link anchors](https://developers.google.com/search/docs/crawling-indexing/links-crawlable), and [core updates](https://developers.google.com/search/docs/appearance/core-updates).
- [Microsoft: Optimizing your content for inclusion in AI search answers](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers) (2025-10-08) and [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a).
- [FTC rule banning fake reviews and testimonials](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials) (2024).
- [NN/g: F-shaped reading](https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/); [Toff and Simon 2024, AI labels and trust](https://doi.org/10.1177/19401612241308697).

Re-validate when Google's people-first, reviews, or AI guidance, the rater guidelines, or Bing's guidelines change.
