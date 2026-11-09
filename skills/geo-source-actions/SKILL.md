---
name: geo-source-actions
title: "Get Cited by AI: Source Action Records"
description: "Turns AI citation findings into ranked per-source actions for Reddit threads, listicles, review sites and videos. Records only. Use after a GEO audit."
license: Apache-2.0
compatibility: "Requires web search and page fetching. Connected SERP data is optional. Produces records only; posting and outreach need separate authorization."
capabilities: websearch webfetch seo-data
domains: seo
rules:
  - match(\bsource[ -]actions?\b)
  - match(\bcited\s+(sources?|pages?|urls?|threads?|domains?)\b)
  - match(\b(get|getting|be|featured|included|listed|placed)\b.{0,40}\b(listicles?|best[ -]of\s+(lists?|roundups?|pages?))\b)
  - match(\b(listicles?|best[ -]of\s+(lists?|roundups?|pages?))\b.{0,60}\b(cit(ed|ing|es?|ations?)|ai\s+answers?|chatgpt|perplexity|gemini|claude)\b)
  - match(\b(cit(ed|ing|es?|ations?)|ai\s+answers?|chatgpt|perplexity|gemini|claude)\b.{0,60}\b(listicles?|best[ -]of\s+(lists?|roundups?|pages?))\b)
  - match(\breddit\s+(threads?|repl(y|ies)|comments?)\b)
  - match(\b(get|getting|be)\b.{0,40}\b(mentioned|listed|recommended|cited)\b.{0,40}\b(ai|chatgpt|perplexity|gemini|claude|copilot|llms?|answers?)\b)
  - match(\b(brand|product)\s+mentions?\b.{0,60}\b(ai|chatgpt|perplexity|gemini|claude|llms?|answers?)\b)
  - match(\b(ai|chatgpt|perplexity|gemini|claude|llms?)\b.{0,60}\b(brand|product)\s+mentions?\b)
  - match(\b(review\s+sites?|youtube\s+videos?)\b.{0,60}\b(cit(ed|ing|es?|ations?)|ai\s+answers?|chatgpt|perplexity|gemini|claude)\b)
  - match(\b(cit(ed|ing|es?|ations?)|ai\s+answers?|chatgpt|perplexity|gemini|claude)\b.{0,60}\b(review\s+sites?|youtube\s+videos?)\b)
---

## Overview

AI answers cite a small set of third-party pages: forum threads, best-of lists, review sites and videos. This skill turns citation findings into a short list of per-source actions: which page to work on, what to say, which evidence supports it, which rules apply, and who acts. It produces action records only. It never posts, emails, or edits a profile; execution belongs to another domain and needs its own authorization.

## Mental model

Ahrefs found branded web mentions correlate 0.66-0.71 with AI visibility across ChatGPT, AI Mode and AI Overviews, and YouTube mentions about 0.737 (75,000 brands, Brand Radar, Ahrefs, 2025-12-12). In its earlier AI Overviews study, backlinks correlated 0.218 (Ahrefs, 2025-05-26). These are correlations, and larger brands have more of everything. Google's AI optimization guide says seeking inauthentic mentions across the web isn't as helpful as it might seem.

So the goal is accurate presence where buyers and engines already look, not a mention count. A citation is a displayed source, not proof of influence. Action classes come from `geo-visibility-audit`: OWN (brand-controlled), CLAIM (claimable profile), EARN (independent source), CONTEST (demonstrably wrong statement).

## Rules

### Input

1. Preferred: source-action records from a visibility audit, with finding, question and trial IDs.
2. Otherwise: a product plus buyer questions. Label visibility Unverified and ask for answer captures. Never write "cited by ChatGPT" without a capture.

### Choose sources in this order

1. URLs actually cited in captured AI answers (observed citation).
2. Pages ranking for the buyer's search query, from connected SERP data or web search. Label them discovery evidence, never an observed AI citation.
3. Recent community questions with no good answer.

Weight by citation share for the engines this buyer uses, and re-check every run. Reddit's share of Perplexity citations fell from 25% to 7% between February and April 2026 (Tinuiti, reported by Shopifreaks and MediaPost; Tinuiti's own report page shows only January). Reddit was 0.1% of Gemini citations in January 2026 (Tinuiti Q1 2026 report), against 24% on Perplexity then. Shares vary by prompt set, so measure on the buyer's own questions.

### Per source type

| Source type | Eligibility check | Action | Guardrail | Success check |
|---|---|---|---|---|
| Reddit or forum thread | Thread open, not archived or locked; subreddit rules read, with rule URL and access date; promotion permitted there | Reply that answers the asker's stated constraints first, then fits the product with evidence | Affiliation disclosed beside the recommendation; AI assistance disclosed where required; one reply per thread; no identical text across subreddits; no vote requests or coordinated accounts | Reply stays up and is not removed; asker or others engage |
| Best-of listicle | Record: product listed or not, position, factual accuracy, competitor treatment, editorial or pay-to-play, last-updated date, author contact | Factual fit case with verifiable access for testing, or a correction citing a dated primary source | Don't ask or pay for a rank; a position can't be promised; paid slots must be labelled and links carry rel="sponsored" | Page updated with the correct fact or an inclusion decision; any position is the editor's |
| YouTube video | Video is cited in a capture or ranks for the buyer query; creator reachable | Offer product access to the creator | Disclose the material connection; no scripted claims | Creator publishes or declines; mention accuracy checked |
| Review site | Profile exists and is claimable | CLAIM: verify ownership, correct facts (EARN or CONTEST for third-party text) | Don't suppress accurate criticism; collecting reviews is owned by another domain | Profile facts match the dated primary source |
| Owned page | Exact URL checked against the question | OWN: improve the existing page | No overlapping new page | Retest per the audit |

Reddit rules, listicle standards and paid-placement handling stay consistent with `seo-backlink-prospecting` and the best-of standards in the content-format guidance: stated selection criteria, per-pick drawback, dated prices.

YouTube: Ahrefs reported YouTube mentions as the strongest correlate of AI visibility (~0.737, Ahrefs 2025-12-12). That is a correlation, so prefer videos that are cited or ranking over cold outreach to any video.

Material connection: the FTC says free or discounted products from a brand count and must be disclosed (FTC, Disclosures 101).

### Community question to content brief

A question with no adequate owned page becomes a brief: buyer wording, thread URLs, evidence needed, and the existing-URL check (inventory, sitemap, targeted search; absence from a `site:` query doesn't prove the page is missing). Deduplicate by decision. Don't write a page per phrasing; that is scaled content abuse (Google spam policies). Drafting belongs to another domain.

### Keep the list short

Default about 10 actions per run (a practitioner convention). Rank by decision importance, evidence, confidence, then effort. Cut the rest to a backlog.

### Output record

File: `geo-actions-[slug]-[YYYY-MM-DD].md`. One record per action:

```text
Action ID:
Linked finding / question / trial IDs:
Exact URL:
Source type:
Class: OWN | CLAIM | EARN | CONTEST
Eligibility: pass | fail | unknown, with rule URL and access date
Message points, each tied to evidence (URL, date):
Disclosure text:
Owning domain:
Authorization required:
Success check:
Review date:
```

Unreadable rules mean eligibility unknown and no recommendation to act.

## Examples

- Wrong: "Post our link in 12 subreddits." Right: "A.03: one disclosed reply in the open thread, rules read 2026-11-09, answers the asker's budget limit first; owner: community domain; needs approval."
- Wrong: "Pay the listicle site to rank us first." Right: "A.05: send the editor a factual fit case and trial access; if a paid slot is offered, it must be labelled and carry rel="sponsored"."
- Wrong: "Reddit gets 25% of Perplexity citations, so prioritize it." Right: "Reddit's measured share on this buyer's engine is re-checked this run; the thread ranks only after a capture cites it."

## Checklist

- [ ] Each URL is tagged observed citation, discovery evidence, or community question.
- [ ] Reddit and other community rules read, with rule URL and access date.
- [ ] Each message point has dated evidence; disclosure text written.
- [ ] No rank promises, paid rank requests, or vote requests.
- [ ] Briefs deduplicated by decision; existing URLs checked.
- [ ] List ranked and capped; each record names owner and authorization.
- [ ] Nothing was posted, sent, or edited.

## Composition / References

- `geo-visibility-audit`: produces the source-action records and retests the outcome.
- `seo-backlink-prospecting`: listicle prospecting and paid-placement screening.
- [Ahrefs: brand visibility correlations, 2025-12-12](https://ahrefs.com/blog/ai-brand-visibility-correlations)
- [Ahrefs: AI Overview brand correlation, 2025-05-26](https://ahrefs.com/blog/ai-overview-brand-correlation/)
- [Tinuiti: AI Citation Trends Report Q1 2026](https://tinuiti.com/research-insights/research/ai-citation-trends-report-q1-2026/)
- [Shopifreaks on Tinuiti Feb-Apr Perplexity data](https://www.shopifreaks.com/reddits-share-of-perplexity-ai-citations-collapsed-from-25-to-7-between-february-and-april-tinuiti-report-finds/)
- [Google: optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)
- [Google: qualify outbound links](https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links)
- [Google: spam policies](https://developers.google.com/search/docs/essentials/spam-policies)
- [FTC: Disclosures 101 for influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)

Sources checked 2026-11-09. Source ordering, the 10-action cap and the sampling approach are conventions, not published ranking rules.
