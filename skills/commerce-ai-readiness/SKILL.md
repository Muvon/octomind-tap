---
name: commerce-ai-readiness
title: "AI Shopping Optimization: Product Catalog Audit"
description: "Audits product feeds, markup and live pages for AI shopping assistants, then lists exact fixes. Use to make a store catalog readable to AI shoppers."
license: Apache-2.0
compatibility: "Needs web access for channel documentation and live product pages. Connected store data is optional. Proposes changes only."
capabilities: webfetch
domains: commerce
rules:
  - match(\b(ai|llm)[ -](shopping|shoppers?|visibility|discovery|ready|readiness|readable|search)\b)
  - match(\b(chatgpt|copilot|gemini|perplexity)\b.{0,40}\b(shopping|recommend\w*|visibility|discover\w*)\b)
  - match(\b(recommend\w*|listed|visib\w*|show\s+up|appear\w*)\b.{0,40}\b(chatgpt|copilot|gemini|perplexity)\b)
  - match(\bshopping\s+(assistants?|agents?)\b)
  - match(\b(aeo|geo)\b.{0,40}\b(store|shop|catalog|catalogue|products?|ecommerce|e-commerce|retail\w*)\b)
  - match(\b(product|catalog|catalogue|merchant)\s+feeds?\b)
  - match(\bmerchant\s+center\b)
  - match(\bagentic\s+(commerce|checkout|shopping)\b)
  - match(\b(product|offer)\s+schema\b)
---

## Overview

An AI assistant, AI browser or shopping agent can only recommend what it can read and trust. This skill checks a store's catalog against the three places those systems get product data, and returns a gap report with exact before and after fixes. It proposes changes only; nothing goes live without approval. Most rules come from Microsoft Advertising's retail guide, cited below by page. It speaks for Copilot and Bing and publishes no test data, so treat it as a platform's stated advice, not a measured result.

## Mental model

| Data source | What it gives the system | What breaks it |
|---|---|---|
| Crawled data | Brand position, category understanding and reputation, from training and indexed pages | Thin or unindexed pages. AI systems run live web searches throughout the journey, so ordinary SEO still matters (p. 10) |
| Product feeds and APIs | Current price, availability and key specs for comparisons | Missing attributes, stale price or stock |
| Live website | Reviews, media, dynamic price, promotions, delivery estimates, and the ability to buy | A broken cart or checkout: "the sale fails even if your feed and crawled data were perfect" (p. 9) |

In Microsoft's terms, answer engine optimization (AEO) drives clarity with enriched, real-time data, and generative engine optimization (GEO) drives credibility (p. 6). Audit both: what the product is, and why it can be trusted.

## Rules

### Scope the channels

Name the AI channels this store can reach, such as Microsoft Merchant Center or Shopify Catalog, and read each channel's current feed documentation. Field names and eligibility differ, so don't carry one channel's rules to another. Google says its AI features need no special schema, so justify schema work by Copilot, Bing and rich results, not by Google AI answers. Sample before scaling: top sellers plus one product per category (a convention).

### Make the catalog machine-readable (p. 12)

- Ship JSON-LD on product pages: `Product`, `Offer`, `AggregateRating`, `Review`, `Brand`. Use `ItemList` on collection and category pages, and `FAQ` only for questions actually shown on the page.
- Include price, availability, color, size, SKU, GTIN and `dateModified`.
- For multi-region stores, express localized pricing and language with `inLanguage` and `priceCurrency`.
- Give promotions and limited-time offers explicit start and end dates.
- Fill the attributes buyers filter on first. Microsoft's summary post says products with more filled-in fields rank higher, with no figures. Never invent a value; list a missing fact as a question.

### Check that every surface agrees (p. 12-13)

This is the core test. For each sampled product, compare price, availability, variants and promotion dates across the feed, on-page schema, rendered DOM, visible page and mobile view. Report each mismatch with both values and where each was read. Microsoft asks for real-time price and inventory sync between feeds and on-site schema, and for mobile and voice experiences to expose identical structured data. Don't serve different HTML to bots.

### Write for intent, from supplied facts (p. 13)

- Title: product name plus its key differentiator.
- Description: open with who it's for, what problem it solves, and what makes it better.
- Add use-case context an assistant can match to a query, such as "best for day hikes above 40 degrees", only when the seller can support it.
- Use headings and Q&A blocks that mirror real buyer questions ("Which size should I pick?"), specs as key and value pairs, comparison tables between models, and "goes well with" data for bundles.
- Write alt text and `ImageObject` descriptions of what the image shows, and provide video transcripts.

### Prove it (p. 14)

- Mark up genuine, verified product reviews with `Review` and `AggregateRating`, and show review volume and verified-purchase ratio. Keep this on product pages: Google's review-snippet rules exclude self-published reviews of a local business or organization.
- Summarize sentiment only from real reviews ("highly rated for comfort and fit").
- Add brand identifiers and official social or retailer links to structured data, and link expert reviews that feature the product.
- State certifications and partnerships as factual entities, only when a certificate or agreement exists.
- Cut exaggerated or unverifiable claims. Microsoft says AI systems penalize low-trust language, without data; advertising law is reason enough.
- Publish FAQ and help content that can ground an assistant's answer.

### Keep the buying path working (p. 9)

An agent can add to cart, apply a promo code, calculate shipping to the buyer's address, complete the purchase and return confirmation and tracking on the live site. Inspect what page reading can show: controls an agent couldn't identify, content missing from the fetched page, promotions shown after their end date. Don't attempt cart or checkout actions. Give the seller a short test script for the rest (add to cart, apply a code, calculate shipping, stop before payment) and mark those steps Unverified until the seller reports back.

### Limits

The guide is retail-first and has no measurement method; it only says to plan new metrics for AI-mediated journeys. Don't promise placement in any assistant. Measuring whether assistants name the product is owned by another domain, through fixed questions repeated over time.

### Output

Return a report; save it as `ai-readiness-[store]-[YYYY-MM-DD].md` only when asked and when the host can write files. It covers channels and documentation read with dates; products sampled; mismatch table (product, field, value per surface, source); missing attributes; content and trust fixes as exact before and after; buying-path result; open questions for the seller; checks that couldn't run, marked Unverified. Bulk edits and price changes wait for explicit approval.

## Examples

- Wrong: "Add FAQ schema to every product so Copilot ranks you." Right: "Twelve products answer sizing questions in visible text but have no `FAQ` markup; add it there for Copilot and Bing only, since Google no longer shows FAQ rich results. No ranking effect is promised."
- Wrong: "Price looks fine." Right: "SKU 4471: feed $179, schema $179, rendered page $199 after a promotion ended on 3 May. The feed and schema are stale."
- Wrong: "Best-rated jacket for any weather." Right: "Rated 4.6 from 812 verified buyers. Seam-sealed. 180-day returns." Every value comes from the seller's data.

## Checklist

- [ ] Channels named, with each feed specification read and dated.
- [ ] Price, availability, variants and promotion dates compared across feed, schema, rendered DOM, visible page and mobile.
- [ ] No invented attribute, rating, certification or use case.
- [ ] Review markup covers genuine product reviews only.
- [ ] Buying path inspected by reading pages; the seller's test script supplied and its steps marked Unverified until reported.
- [ ] No placement promised; failed checks marked Unverified.
- [ ] Fixes given as exact before and after; nothing changed without approval.

## Composition / References

- [Microsoft Advertising: From discovery to influence, a guide to AEO and GEO](https://aka.ms/ads/AeoGeo), PDF, 16 pages, summary post dated 2026-01-06: [blog](https://about.ads.microsoft.com/en/blog/post/january-2026/from-discovery-to-influence-a-guide-to-geo).
- [Google: optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
- [Google: review snippet structured data](https://developers.google.com/search/docs/appearance/structured-data/review-snippet).

Read in full 2026-11-09. The sampling approach is a convention, not a published rule.
