---
name: ad-google
title: "Google Ads Production Spec"
description: "Specifies what to produce for a Google Ads creative: Search RSA, Performance Max, and Display, with the exact slots (headlines, descriptions, paths, long headline, long description), character limits, pinning rules, asset ratios, and policy constraints so copy fits before it is pasted into Google Ads Editor. Use whenever the task is producing Google Ads ad copy or assets; strictly platform-specific, so it does not cover bidding, keywords selection, audience setup, or attribution."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to Google Ads."
domains: launch
rules:
  - content(google ads)
  - content(google ad)
  - content(adwords)
  - match(\bgoogle\s+ads?\b)
  - match(\bRSA\b)
  - match(\bresponsive\s+search\s+ads?\b)
  - match(\bperformance\s+max\b)
  - match(\bpmax\b)
  - match(\bgoogle\s+display\b)
  - semantic(write google ads copy)
  - semantic(produce a responsive search ad)
  - semantic(headlines for performance max)
---

## Overview

This skill defines exactly what to produce for a Google Ads creative. It is platform-spec only: the slots Google exposes, the limits they enforce, and the assets they expect. It does not cover keyword strategy, bidding, audience signals, or conversion tracking — those are separate concerns.

Use this skill whenever the deliverable is the actual ad copy or asset set that will be pasted into Google Ads Editor or uploaded to a Performance Max asset group.

## Instructions

### Campaign Types Covered

| Type | What You Produce |
|------|------------------|
| Search (RSA) | Headlines × 15, descriptions × 4, paths × 2, sitelinks (optional), callouts |
| Performance Max | Headlines, long headlines, descriptions, business name, images, logos, videos |
| Demand Gen | Headlines (40 char), long headlines, descriptions, images incl. 9:16, videos, carousel |
| Display | Responsive display assets — headlines, long headline, descriptions, images, logo, video |

2026 context (verify live in Google Ads Help before relying on dates): AI Max for Search adds search term matching, text customization, and final URL expansion to Search campaigns; Google announced in April 2026 that Dynamic Search Ads, automatically created assets, and campaign-level broad match upgrade into AI Max from September 2026. With text customization on, Google generates extra headlines and descriptions from your site and landing pages, so your supplied copy sets the tone it imitates. Search, Shopping, and PMax ads can also serve in AI Overviews and AI Mode.

Out of scope for this skill: keyword lists, negative keywords, bid strategy, audience signals, conversion goals.

### Responsive Search Ads (RSA) — Slots

| Slot | Count | Hard Limit | Notes |
|------|-------|-----------|-------|
| Headline | up to 15 | 30 chars each | Google picks 3 to show per impression |
| Description | up to 4 | 90 chars each | Google picks 2 to show per impression |
| Path | 2 | 15 chars each | Display URL only — does not affect destination |
| Final URL | 1 | URL | The actual landing page |
| Sitelink | 0–6 | Headline 25, description 35×2 | Optional extension |
| Callout | 0–10 | 25 chars each | Optional extension |
| Structured snippet | 0–2 | 25 chars per value | Optional extension |

### RSA Production Rules

- Produce at least 8 headlines and 3 descriptions. Fewer reduces the ad strength signal.
- Pin only when policy or brand requires it. Pinning H1 forces it to position 1 every impression, which kills Google's optimisation surface. Final URL expansion overrides RSA pins.
- Include the primary keyword in at least 3 headlines. Search intent match drives quality score.
- Vary headline angles: benefit, feature, social proof, urgency, question. Repeating the same angle across all 15 wastes slots.
- Descriptions complement headlines — do not restate the same benefit twice.
- Display path is brand surface only. Use it to reinforce the click target (`/pricing`, `/demo`, `/free-trial`).
- Final URL must contain the offer named in the ad. No bait-and-switch.

### Performance Max — Slots

2026 spec (Google Ads Help, "Performance Max campaigns specs" — verify live):

| Asset Group Slot | Count Range | Limit | Notes |
|------------------|-------------|-------|-------|
| Headline | 3–15 (aim for 11+) | 30 chars | At least one ≤15 chars |
| Long headline | 1–5 (aim for 2+) | 90 chars | Used in display/video placements |
| Description | 2–5 (aim for 4+) | 90 chars | Standard description |
| Business name | 1 | 25 chars | Must match your domain or verified legal business name |
| Display path | 0–2 | 15 chars each | Optional |
| Image — landscape 1.91:1 | 1–20 (aim for 4+) | 1200×628 rec, 600×314 min | Required |
| Image — square 1:1 | 1–20 (aim for 4+) | 1200×1200 rec, 300×300 min | Required |
| Image — portrait 4:5 | 0–20 (aim for 2+) | 960×1200 rec, 480×600 min | Optional; helps mobile placements |
| Logo — square 1:1 | 1–5 | 1200×1200 rec, 128×128 min | Prefer a non-white background |
| Logo — landscape 4:1 | 0–5 | 1200×300 rec, 512×128 min | Optional |
| Video | up to 15 per orientation | 16:9, 1:1, 9:16; ≥10s | Without uploads Google may auto-generate videos; supply all three orientations to avoid that |
| CTA | 1 | Automated by default or picked from a list | |
| Sitelinks / callouts | recommended | Standard limits | Improve coverage on Search inventory |

### Demand Gen — Slots (Replaced Discovery Ads in 2024)

Demand Gen serves across YouTube (In-Stream, In-Feed, Shorts), Discover, Gmail, and Maps; it also absorbed Video Action Campaigns in 2025. The biggest pitfall is reusing PMax/RSA copy — Demand Gen has DIFFERENT char limits. 2026 specs per Google Ads Help; verify live.

| Slot | Count | Limit | Notes |
|------|-------|-------|-------|
| Headline | up to 5 (3+ unique recommended) | 40 chars | NOT 30 — most common reuse error |
| Long headline (video ads only) | up to 5 | 90 chars | |
| Description | up to 5 | 90 chars | |
| Business name | 1 | 25 chars | |
| CTA | 1 | Enum OR ≤10 char custom | Demand Gen exposes CTA explicitly |
| Image 1.91:1 | up to 20 | 1200×628 | |
| Image 1:1 | up to 20 | 1200×1200 | |
| Image 4:5 | up to 20 | 960×1200 | |
| Image 9:16 (optional, for Shorts) | up to 20 | 1080×1920 rec, 600×1067 min | Use 9:16 safe zones; may be rejected via Display & Video 360 |
| Logo | up to 5 | 1:1, min 128×128 | |
| Video | 1-5 per aspect ratio | 16:9 / 1:1 / 9:16 | 5s min (10s+ for in-stream), MP4 |
| Carousel | 2-10 cards | Ratios must match across cards | |
| Product feed | optional | Merchant Center linkage | For commerce |
| Sitelinks (video ads) | up to 4 | Standard sitelink limits | |

Demand Gen CTA enum (subject to vertical eligibility): Apply Now, Book Now, Contact Us, Download, Get Quote, Learn More, Order Now, Shop Now, Sign Up, Subscribe, Visit Site, Watch Now.

### Demand Gen vs PMax vs Search RSA — When to Use Which

| Campaign | When |
|----------|------|
| Search RSA | High-intent, branded, bottom funnel. Quality-score driven |
| Performance Max | Conversion goal + creative assets + all-surface reach. Best for eCom with feed |
| Demand Gen | Demand creation, visual story, YouTube/Discover/Gmail surfaces, top/mid funnel |
| Display | Remarketing or cheap reach only — not a primary spend channel in 2026 |

### Display — Responsive Display Slots

| Slot | Count Range | Limit |
|------|-------------|-------|
| Headline | up to 5 | 30 chars |
| Long headline | 1 | 90 chars |
| Description | up to 5 | 90 chars |
| Business name | 1 | 25 chars |
| Image — landscape | 1–15 | 1.91:1, 1200×628 |
| Image — square | 1–15 | 1:1, 1200×1200 |
| Logo — square | 1 | 1:1 |
| Logo — landscape | 0–5 | 4:1 |
| Video | 0–5 | YouTube-hosted, 30s max recommended |

### CTA Behavior

Google does not expose a CTA button field for RSA — the CTA lives in the headline/description copy. Performance Max picks a CTA automatically unless you choose one from its list; Display auto-selects based on the ad copy and conversion action. So:

- Write the CTA INSIDE a headline or description ("Start free trial", "Get the demo", "See pricing")
- Do not waste a slot on a generic CTA-only line like "Click here" — every slot must contain product/value
- For PMax/Display, ensure at least one headline contains the conversion verb you want the auto-CTA aligned to

### Policy Constraints (Common Disapprovals + 2025-2026 Updates)

- Trademark in headline without authorisation — disapproval on complaint
- Superlatives without verifiable claim ("#1", "best", "cheapest") — manual review trigger
- Punctuation: no repeated or gimmicky punctuation ("Save!!"), no symbols replacing letters ("S@ve"); exclamation marks are banned in callouts and sitelinks — house rule: none in headlines, at most one per description
- ALL CAPS words: not allowed except for acronyms (CRM, SEO, API) and trademarks
- Restricted categories (healthcare, finance, gambling, alcohol, dating) — additional certification required
- Personal pronouns in display URL paths look spammy: `/you-need-this` will flag

2025–2026 policy context (verify live):

- AI content labels (July 2026) — a new setting labels image and video assets made or edited with AI. Google's own generative tools label automatically; declare third-party AI assets yourself. Campaigns targeting the EU, India, or New York may show a visible disclosure. The label alone doesn't guarantee legal compliance; the EU AI Act's transparency duties for deepfakes apply from August 2026.
- EU political ads — Google stopped serving political ads in the EU from October 2025 (TTPA regulation).
- All-in pricing — the US FTC fees rule (May 2025) requires total price up front for live-event tickets and short-term lodging; several states go further. Don't advertise a price that excludes mandatory fees.
- Consent — EEA/UK traffic needs Consent Mode v2 signals for personalized ads and remarketing (out of scope here, but it changes which audiences an asset can reach).

### Output Format

```markdown
# Google Ads — [Product] [Campaign Name]

## Campaign Type
[Search RSA / Performance Max / Display]

## Final URL
[Landing page URL]

## Headlines ([N]/15)
1. [Headline] — [chars/30]
2. [Headline] — [chars/30]
...

## Descriptions ([N]/4)
1. [Description] — [chars/90]
2. [Description] — [chars/90]
...

## Paths (RSA only)
- Path 1: [path] — [chars/15]
- Path 2: [path] — [chars/15]

## Pinning Map (only if required)
| Position | Pinned Headlines | Reason |
|----------|------------------|--------|
| H1 | #1, #3 | Brand name required |

## PMax / Display Additions
- Long headline: [copy] — [chars/90]
- Business name: [name] — [chars/25]

## Visual Asset Specs (PMax / Display)
- Landscape 1.91:1 — [scenario brief]
- Square 1:1 — [scenario brief]
- Portrait 4:5 — [scenario brief, mobile lift]
- Logo square 1:1 — [supplied]
- Video 16:9 — [hook timing + scene plan if produced]

## Extensions
- Sitelinks: [list with link text + URL]
- Callouts: [list of 25-char callouts]

## Pre-Submit Checklist
- [ ] At least 8 headlines, 3 descriptions
- [ ] Primary keyword in 3+ headlines
- [ ] No ALL CAPS, no repeated punctuation, ≤1 "!"
- [ ] No unauthorised trademark
- [ ] Final URL matches the ad's promise
- [ ] Pinning only where strictly required
```

## When NOT to Use This Skill

- Keyword research → out of scope
- Audience or signal selection → out of scope
- Bid strategy or budget setup → out of scope
