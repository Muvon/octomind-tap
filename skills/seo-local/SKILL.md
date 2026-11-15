---
name: seo-local
title: "Local SEO and Google Business Profile"
description: "Audits and plans local search: Google Business Profile eligibility and completeness, NAP consistency, citations, reviews, location pages, markup."
license: Apache-2.0
compatibility: "Public evidence works without access. Profile edits and insights need the owner's Business Profile access; this skill never edits a profile."
capabilities: websearch webfetch
domains: seo
rules:
  - match((?i)\b(local\s+seo|local\s+pack|map\s+pack|3-?pack|local\s+search|local\s+ranking)\b)
  - match((?i)\b(google\s+(business|my\s+business)\s+profile|gbp|gmb)\b)
  - match((?i)\b(nap\s+consistency|citations?\s+(audit|building|cleanup)|business\s+listings?)\b)
  - match((?i)\bnear\s+me\b)
  - match((?i)\b(google\s+)?reviews?\b.{0,40}\b(ranking|local|profile|get\s+more)\b)
  - match((?i)\bget\s+more\s+(google\s+)?reviews\b)
---

## Overview

Local SEO covers searches where Google shows nearby businesses on a map, and the pages that serve one place or area. This skill checks whether a business qualifies for a Google Business Profile, how complete and consistent its listings are, whether its reviews follow Google's rules, and whether its site has pages and markup for each location. It returns findings with evidence and a fix order. It never edits a profile and never asks customers for reviews on the owner's behalf.

## Mental model

Google states that local results rest on three factors: relevance (how well the profile matches the search), distance (from the searcher), and prominence (how well known the business is; links, review count and ratings contribute). The business controls relevance and part of prominence; distance is fixed. No one can pay for a better local ranking (Google, local ranking, checked 2026-11-15). Everything below serves those three factors or protects the profile from suspension.

## Rules

### Step 1: eligibility

| Case | Rule (Google Business Profile guidelines) |
|---|---|
| Storefront | Real staffed address where customers are served |
| Service-area business | One profile for the base location with a defined service area; hide the street address; keep the area to roughly two hours of driving from the base |
| Virtual office, rented mailbox, remote P.O. box | Not eligible |
| Co-working space | Eligible only with clear signage, customers received in business hours and your own staff |
| Several locations | One profile per eligible location, each with its own page and phone |

An ineligible listing is Critical: it risks suspension, and fixes elsewhere do not matter.

### Step 2: profile completeness

Check against the live profile: primary category (the most specific true one), secondary categories, services or products, opening hours including holidays, phone, website URL for that location, photos, description, attributes. Business name is the real-world name only: no keywords, taglines, hours or phone numbers added (Google, representing your business). Keyword-stuffed names are Critical.

### Step 3: name, address, phone consistency and citations

NAP means business name, address and phone number as written on each listing. Record the profile's NAP as the reference, then compare the website, social profiles, and the top directories relevant to the niche and country. Flag mismatches in suite numbers, abbreviations, old phone numbers and duplicate listings. Duplicates and wrong data are Moderate; treat consistency as hygiene, not as a proven ranking lever, because Google's local ranking page names no citation count.

### Step 4: reviews

Reviews feed prominence, so review handling is part of the audit. Google's contributions policy forbids:

- offering rewards for reviews, or reviews tied to an incentive;
- review gating: soliciting only happy customers, or discouraging negative reviews;
- reviews from staff, owners or competitors; one person on several accounts;
- unusual volumes or patterns that look like rating manipulation.

Allowed: asking genuine customers without incentive or wording requests, and replying to every review. Check: review count and recency against the nearest competitors in the pack, response rate, response tone, any pattern of bursts in dates. Flag bursts as risk. Recommend one review link on receipts, email and signage, with no filter on who receives it.

### Step 5: website

- One indexable page per location or service area with unique content: services, address and map, local proof, staff, opening hours. Don't clone a page and swap the city name; Google's scaled content abuse policy covers pages generated mainly to manipulate rankings (see `seo-programmatic`).
- Same NAP as the profile, shown in text, not only in an image.
- `LocalBusiness` markup (a subtype where one fits): `name` and `address` are required; `geo` (at least five decimal places), `openingHoursSpecification`, `telephone` and `url` are recommended (Google, local business structured data). Add `aggregateRating` and `review` only for sites that collect reviews of other local businesses; self-serving review markup is ineligible.
- The profile links to the matching location page, not always the homepage.

### Step 6: measure

Use profile insights from the owner for calls, direction requests and website clicks; use Search Console for the site; use a rank check from fixed grid points only with dated, located captures. Web search from one machine is not what a nearby searcher sees: mark pack positions Unverified without a located capture.

## Examples

- Wrong: "Add the city and 'best plumber' to the profile name." Right: "Name stays the real-world name; add services and the service area."
- Wrong: "Send the review link only to customers who rated 5 on our survey." Right: "Send the link to every customer; that gating breaks the policy."
- Wrong: "Use one 'Plumber in {city}' page for 40 towns." Right: "Pages only for towns served, each with local jobs, photos and named staff; the rest listed on one service-area page."

## Checklist

- [ ] Eligibility checked per location; virtual offices and mailboxes flagged.
- [ ] Name, categories, hours, phone and URL compared with the real business.
- [ ] NAP reference set and the main listings compared; duplicates listed.
- [ ] Review practices checked against the policy; incentives and gating flagged.
- [ ] Competitor review counts and recency compared, with dates.
- [ ] One unique page per location; `LocalBusiness` fields valid and matching visible text.
- [ ] Pack positions marked Unverified unless captured with location and date.
- [ ] No profile edit, review request or listing change made without the owner's yes.

## Composition / References

- `seo-structural-audit` for schema and crawl checks; `seo-programmatic` for many location pages; `seo-google-policy-baseline` for spam-policy facts.
- [Google: improve your local ranking](https://support.google.com/business/answer/7091)
- [Google: guidelines for representing your business](https://support.google.com/business/answer/3038177)
- [Google: prohibited and restricted content (reviews)](https://support.google.com/contributionpolicy/answer/7400114)
- [Google: LocalBusiness structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business)
