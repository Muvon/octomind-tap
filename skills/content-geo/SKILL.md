---
name: content-geo
title: "GEO & AI Citation Optimization"
description: "Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) patterns for getting content cited by AI search engines. Answer-first structure, schema markup, extractable passages, and crawler setup."
license: Apache-2.0
compatibility: "Network access for current engine documentation and public-page checks."
domains: content
rules:
  - content(seo)
  - content(geo)
  - match(\b(rank|ranking)\s+(in|on)\s+(google|search|serps?)\b)
  - match(\bschema\.org\b)
  - match(\bmeta\s+(description|title|tags?)\b)
  - match(\bserps?\b)
  - match(\bai\s+overview\b)
  - match(\b(llm|ai)\s+citation\b)
  - match(\bgenerative\s+engine\s+optimization\b)
  - match(\bsearch\s+engine\s+optimization\b)
---

## Overview

AI answer surfaces (Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Copilot, Claude, Gemini) retrieve passages, compose an answer, and cite sources. Use this skill for content readiness and evidence-backed writing, not as a substitute for a scoped buyer-question visibility audit. Google's AI-feature guidance places ordinary SEO underneath its search surfaces; that foundation alone doesn't diagnose why a particular brand is absent from an answer.

## Mental model

Each engine expands a prompt into several sub-queries (query fan-out), retrieves passages from its own index or search partners, and cites the passages that best support the answer. A page wins by being retrievable by that engine, holding the clearest and most specific passage for one sub-query, and offering something the commodity pages don't.

Ranking helps but no longer guarantees a citation. Ahrefs' 2026 study (863k keywords) found about 38% of AI Overview citations rank in Google's top 10 for the same query, down from 76% in its July 2025 study (parser changes and the Gemini 3 switch limit comparability). Clicks are scarcer too: Pew's 2025 browsing study found users clicked a traditional result on 8% of visits with an AI summary versus 15% without, and clicked a cited link inside the summary on 1%. Measure citations and impressions, not only clicks.

## Rules

### Retrieval differs by surface

| Surface | Retrieval | Action |
|---|---|---|
| Google AI Overviews / AI Mode | Google index and core ranking, fan-out | Normal SEO; stay included in the Search Console "Search generative AI" control (default on) |
| ChatGPT search | OAI-SearchBot index plus external providers; OpenAI doesn't publish the mix | Allow OAI-SearchBot; submit to Bing Webmaster Tools and IndexNow; don't assume Google rank transfers |
| Perplexity | Own index (PerplexityBot) plus live fetches | Allow PerplexityBot |
| Copilot | Bing index | Bing Webmaster Tools; read its AI Performance report |
| Claude | Claude-SearchBot index plus Claude-User fetches | Allow both |

Answers are nondeterministic and vary by engine, location, and session. Judge trends over repeated runs, never a single screenshot.

### Content that earns citations

- Non-commodity first. Google's guide separates commodity content ("based on common knowledge, which could originate from anyone") from content that "provides unique expert or experienced takes," and says "Don't just recycle what others on the internet have already said." Before drafting, name the gain: original data, a first-hand test with specifics, practitioner gotchas, real costs, or a synthesis nobody has published. If an LLM could rebuild the draft from the current top results, send it back to research.
- Answer first. Open each section with a one- or two-sentence direct answer to its heading, then evidence and nuance. Each passage must stand alone: no "as mentioned above," no pronouns pointing at earlier sections. Put each key claim in one plain sentence; Claude's web search, for example, quotes at most 150 characters per citation.
- Evidence density, without magic. In the GEO benchmark (Aggarwal et al., KDD 2024), adding quotations, statistics, and cited sources raised a source's visibility by up to about 40% and keyword stuffing hurt. A later benchmark (C-SEO Bench, NeurIPS 2025) found significant gains in only 3 of 54 settings, shrinking as more sites adopt the tactics. Use real, attributed numbers and quotes because readers and verifiers need them; never invent them to look citable.
- Cover the fan-out neighbourhood on one strong page: related questions, comparisons, constraints, edge cases, and alternatives. Don't publish a page per query variation; Google's guide says that can violate the scaled content abuse policy and "a high quantity of pages doesn't make a website higher quality."
- Natural structure, no artificial chunking. Google: "There's no requirement to break your content into tiny pieces." Bing's guidelines favour content that stands on its own, essential information near the top, and one topic per URL, and they treat language engineered to trigger citations as abuse. Use descriptive headings (question form where readers ask questions), lists and tables for genuinely parallel items, and paragraph length that follows the topic. Keep key answers out of tabs, images, and PDFs.
- Experience and authorship. Name a real author with relevant credentials and a bio page. Show first-hand evidence the author supplied: own screenshots, exact versions and settings, errors met, what failed. Stock heroes and "Admin" bylines add nothing; `content-formats` covers experience intake and methodology notes.
- Real freshness. AI assistants cite somewhat fresher pages than organic results (Ahrefs 2025, 17M citations, vendor data), yet the average cited page is still years old. Update facts and `dateModified` when content changes; don't bump dates without changes.
- Citable by others. Third-party coverage dominates brand-owned pages in ChatGPT and Claude citations (Chen et al. 2025, preprint). Original data, tests, and expert takes are what other sites quote; manufactured mentions are not (Google's guide).
- Comparison pages. Make each item self-contained (who it suits, key facts, price with an as-of date, limitations), disclose affiliations, and don't rank yourself first without evidence.

### Structured data (2026 status)

- Not required for AI features: "Structured data isn't required for generative AI search." It still drives rich-result eligibility and entity disambiguation, and other engines may parse it.
- Use JSON-LD that matches visible content: `Article`/`BlogPosting` (headline, author as `Person` with `url`/`sameAs`, `datePublished`, `dateModified`), `Organization` (logo, `sameAs`), `Product`/`Offer`, `BreadcrumbList`.
- Google stopped showing FAQ rich results on 7 May 2026; HowTo rich results went in 2023. Keep a visible FAQ when it helps readers; leftover markup is harmless but no longer a Google lever.
- Review and `AggregateRating` markup about your own business on your own site is not eligible for review snippets. Mark up genuine third-party reviews only.

### Spam-policy boundaries

- Scaled content abuse covers mass-produced or mass-rewritten pages, AI-assisted or not, and Google's guide applies it to attempts to manipulate generative AI responses.
- Site reputation policy (text updated 28 August 2026): third-party content published mainly to exploit a host's ranking signals violates it unless the host's input, editorial oversight, or contribution makes it fully integrated. Since 30 August 2026 manual actions don't apply to searchers in the EEA; affected sections may rank independently instead. Pitch placements only where the topical fit is genuine.
- The helpful content system was folded into core ranking in March 2024; there is no separate update to wait out. Core updates (2026: 27 March to 8 April, 21 May to 2 June, plus smaller unannounced ones) re-evaluate quality broadly. Don't quote ranking-shift percentages without a primary source.

### Crawlers and controls

These search-related tokens are illustrative, not a required configuration. Check current per-product documentation, existing rules, CDN/WAF access, and the owner's permissions before proposing changes; a spoofed user-agent request doesn't verify real crawler access.
```
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: Bingbot
Allow: /
```

- Search and training permissions are separate. GPTBot and ClaudeBot concern training; Google-Extended also affects Gemini Apps grounding, not Google Search AI-feature eligibility. Check each product's documented scope rather than treating training access as a universal citation requirement.
- User-initiated fetchers (ChatGPT-User, Perplexity-User, Claude-User) act for a person; OpenAI and Perplexity state robots.txt may not apply to them.
- Google's AI features use Googlebot. Limit display with `nosnippet`, `data-nosnippet`, or `max-snippet`; the Search Console "Search generative AI" control (all sites since 31 August 2026) removes a site from AI Overviews, AI Mode, and Discover AI features and is not a ranking signal elsewhere. Google-Extended limits training and Gemini Apps grounding, not appearance in Search or its AI features.
- Serve key content in the initial HTML. Several AI crawlers don't execute JavaScript, so client-rendered text may be invisible to them.
- llms.txt: Google Search ignores it ("You don't need to create new machine readable files, AI text files, markup, or Markdown"). Keeping one for developer tools is harmless; don't promise visibility from it.

### Measurement

- Google Search Console Web performance includes AI Overviews and AI Mode. Verify live report dimensions; don't assume a dedicated AI-only breakdown or sum overlapping reports. Actual dated answer captures and scoped publisher/vendor reports remain separate evidence, not an interchangeable measure.
- Bing Webmaster Tools AI Performance report (public preview February 2026): Copilot and Bing AI citations, cited pages, and grounding queries; no clicks. Partner integrations are unnamed, so don't read it as ChatGPT data.
- Agree a bounded, versioned buyer-question set and repeat comparable trials across named engine surfaces, locales, search modes, and windows. Ten to twenty prompts and monthly sampling are practitioner starting points, not requirements. Record actual dated answers, mentions, recommendations, cited URLs, and completed/planned counts; without captures, visibility is Unverified, not zero. UI/API runs remain separate; ordinary search isn't an engine-answer test. Referral segments from chatgpt.com, perplexity.ai, copilot.microsoft.com, and gemini.google.com are partial attribution evidence, not all AI traffic. Define the activation event/window and conversion denominator; missing analytics is Unverified. Treat vendor trackers as samples, not causal uplift evidence.

### Agentic experiences

Google's guide flags agents that act for users (book, compare, buy). Browser agents read screenshots, the DOM, and the accessibility tree, so semantic HTML, labelled controls, and accessible forms matter. For commerce, track the Universal Commerce Protocol (UCP) as it matures. No new markup is required.

## Examples

Answer-first section, wrong:

> How long does a full reindex take?
> When we look at how indexing works, there are many factors at play. Researchers have studied this extensively...

Right:

> How long does a full reindex take?
> On our 40 GB test index, a full reindex took 18 minutes on 8 vCPUs and 52 minutes on 2. Time scales roughly with document count; the settings that change it are below.

Fan-out coverage, wrong: separate pages for "reindex time", "how long reindex", and "reindex duration large index".
Right: one page answering the time question first, then hardware scaling, partial reindex, zero-downtime swaps, and common failures, each under its own heading.

## Checklist

- [ ] The page states a non-commodity gain (data, test, experience, synthesis) in the first screen.
- [ ] Every section opens with a standalone answer; no passage depends on an earlier one.
- [ ] Numbers and quotes are real, attributed, and dated; none invented for citability.
- [ ] Related sub-questions are covered on this page, not spun into near-duplicate pages.
- [ ] Named author with credentials and bio; first-hand evidence where the topic allows.
- [ ] JSON-LD matches visible content; no self-serving review markup; no claim that FAQ or HowTo markup earns Google features.
- [ ] Search crawlers allowed, key content in initial HTML, Bing submission done, Google generative AI control left on unless the owner opts out.
- [ ] Citation tracking set up (Search Console, Bing AI Performance, fixed prompt set) and judged over repeated runs.

## References

Reviewed 2026-10-24.

- [Google: optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) and [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [Google: Search generative AI control](https://support.google.com/webmasters/answer/16908024) and [generative AI performance reports](https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports)
- [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies) and [AI-generated content guidance](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content)
- [OpenAI crawlers](https://developers.openai.com/api/docs/bots), [Perplexity crawlers](https://docs.perplexity.ai/docs/resources/perplexity-crawlers), [Anthropic crawlers](https://support.claude.com/en/articles/8896518)
- [Aggarwal et al., GEO: Generative Engine Optimization (KDD 2024)](https://arxiv.org/abs/2311.09735) and [Puerto et al., C-SEO Bench (NeurIPS 2025)](https://arxiv.org/abs/2506.11097)
- [Bing Webmaster Guidelines](https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) and [Microsoft: optimizing content for AI search answers (2025-10-08)](https://about.ads.microsoft.com/en/blog/post/october-2025/optimizing-your-content-for-inclusion-in-ai-search-answers)
- [Pew Research, AI summaries and clicks (2025)](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/)
