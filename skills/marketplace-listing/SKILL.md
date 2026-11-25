---
name: marketplace-listing
title: "Marketplace Listing Fields and Claims"
description: "Draft fact-grounded listing titles, descriptions, bullets, and attributes for Shopify, Etsy, eBay, and Amazon using verified channel rules."
license: Apache-2.0
domains: commerce
rules:
  - session(tap-commerce-copywriter-)
  - match((?i)\b(draft|write|rewrite|edit)\b.{0,45}\b(shopify|etsy|ebay|amazon)\b.{0,30}\b(listing|product (title|description)|listing bullets)\b)
  - match((?i)\b(product (title|description)|listing (title|copy|bullets))\b.{0,45}\b(shopify|etsy|ebay|amazon)\b)
---

## Overview

Map supplied product evidence into the fields of the selected marketplace. Keep the result in draft form.

## Rules

### Listing anatomy and natural SEO
- Title: product type + defining feature + relevant size/count, ordered for the buyer; use the primary search phrase naturally, without repeated synonyms or unrelated brands.
- Bullets: benefit grounded in a concrete fact, then fit, contents, care and limitations; don't force a fixed bullet count where the channel differs.
- Description: short opening, practical detail and objections answered; no boilerplate that could describe any product.
- Shopify: separate title, body and requested search-preview fields; Etsy: prioritize readable titles and relevant tag suggestions; eBay: keep item specifics distinct; Amazon: distinguish title, bullets and description, checking category-specific restrictions live.
- Don't invent field limits or ranking guarantees; if current documentation cannot be read, label the constraint unverified and avoid claiming compliance.

### Channel field limits (as of 2026-11; re-read the channel page before citing a limit)
- Etsy: title up to 140 characters; up to 13 tags, each up to 20 characters, using letters, numbers and spaces (Etsy Help Center). Shoppers see only the opening words of a title in search results, so lead with what the item is.
- eBay: title up to 80 characters; paid subtitle up to 55; fill the category's item specifics and product identifiers, and keep identifiers matching the product exactly (eBay developer and seller documentation).
- Amazon: in most categories the title may not exceed 200 characters including spaces (rule effective 21 January 2025), may not use the same word more than twice (prepositions, articles and conjunctions exempt), and may not use ! $ ? _ { } ^ ¬ ¦ unless part of the brand name. Bullet and description limits differ by category: read the category style guide or template, and mark them unverified if it cannot be read.
- Shopify: search-engine page title up to 70 characters (about 60 avoids truncation); Shopify's guidance suggests about 160 characters for the meta description (Shopify Help Center).

## Checklist

- [ ] Each benefit and specification traces to the supplied product facts.
- [ ] Field constraints were checked in current official documentation, or the draft flags them as unverified.
- [ ] Copy and source notes are separate.
