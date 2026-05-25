---
name: ad-google
title: "Google Ads Production Spec"
description: "What to produce for a Google Ads creative — Search RSA, Performance Max, and Display. Encodes the exact slots (headlines, descriptions, paths, long headline, long description), character limits, pinning rules, asset ratios, and policy constraints so copy fits before it's pasted into Google Ads Editor. Use whenever the task is producing Google Ads ad copy or assets. Strictly platform-specific — does not cover bidding, keywords selection, audience setup, or attribution."
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
| Performance Max | Headlines, long headlines, descriptions, long descriptions, business name, images, logos, videos |
| Display | Responsive display assets — headlines, long headline, descriptions, images, logo, video |

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
- Pin only when policy or brand requires it. Pinning H1 forces it to position 1 every impression, which kills Google's optimisation surface.
- Include the primary keyword in at least 3 headlines. Search intent match drives quality score.
- Vary headline angles: benefit, feature, social proof, urgency, question. Repeating the same angle across all 15 wastes slots.
- Descriptions complement headlines — do not restate the same benefit twice.
- Display path is brand surface only. Use it to reinforce the click target (`/pricing`, `/demo`, `/free-trial`).
- Final URL must contain the offer named in the ad. No bait-and-switch.

### Performance Max — Slots

| Asset Group Slot | Count Range | Limit | Notes |
|------------------|-------------|-------|-------|
| Headline | 3–15 | 30 chars | Same as RSA headlines |
| Long headline | 1–5 | 90 chars | Used in display/video placements |
| Description | 1–5 | 90 chars | Standard description |
| Long description | 1 | 90 chars | Used in some display formats |
| Business name | 1 | 25 chars | Brand surface across placements |
| Image — landscape | up to 20 | 1.91:1 | 1200×628 recommended |
| Image — square | up to 20 | 1:1 | 1200×1200 recommended |
| Image — portrait | up to 20 | 4:5 | 960×1200 recommended (≥3 portraits lifts mobile placement significantly) |
| Logo — square | up to 5 | 1:1 | 1200×1200, min 128×128 |
| Logo — landscape | up to 5 | 4:1 | 1200×300 (optional) |
| Video | 0–5 per aspect ratio (15 total max) | 16:9, 9:16, or 1:1 | 10s minimum, YouTube-hosted. ≥1 9:16 vertical (10-60s) required for Shorts placement |
| CTA | 1 | ≤10 char custom override OR enum | Custom CTA now exposed in Editor 2.12+ |
| Sitelink | 2+ | Standard sitelink limits | Required for full eligibility |
| Callout | 2+ | 25 chars | Required for full eligibility |

### Demand Gen — Slots (Replaced Discovery Ads in 2024)

Demand Gen serves across YouTube (In-Stream, In-Feed, Shorts), Discover, Gmail, and Maps. The biggest pitfall is reusing PMax/RSA copy — Demand Gen has DIFFERENT char limits.

| Slot | Count | Limit | Notes |
|------|-------|-------|-------|
| Headline | up to 5 | 40 chars | NOT 30 — most common reuse error |
| Long headline (video ads only) | up to 5 | 90 chars | |
| Description | up to 5 | 90 chars | |
| Business name | 1 | 25 chars | |
| CTA | 1 | Enum OR ≤10 char custom | Demand Gen exposes CTA explicitly |
| Image 1.91:1 | up to 20 | 1200×628 | |
| Image 1:1 | up to 20 | 1200×1200 | |
| Image 4:5 | up to 20 | 960×1200 | |
| Image 9:16 (NEW for Shorts) | up to 20 | 1080×1920 | |
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

Google does not expose a CTA button field for RSA — the CTA lives in the headline/description copy. For Performance Max and Display, an auto-generated CTA appears based on the ad copy and conversion action; the agent does not set it directly. So:

- Write the CTA INSIDE a headline or description ("Start free trial", "Get the demo", "See pricing")
- Do not waste a slot on a generic CTA-only line like "Click here" — every slot must contain product/value
- For PMax/Display, ensure at least one headline contains the conversion verb you want the auto-CTA aligned to

### Policy Constraints (Common Disapprovals + 2025-2026 Updates)

- Trademark in headline without authorisation — auto-disapproval
- Superlatives without verifiable claim ("#1", "best", "cheapest") — manual review trigger
- Exclamation points: max 1 per ad total across headlines and descriptions
- ALL CAPS words: not allowed except for acronyms (CRM, SEO, API). LLM enforcement now catches evasion ("B-E-S-T")
- Punctuation: no repeated punctuation ("Save!! Now!!"), no symbols replacing letters ("S@ve")
- Restricted categories (healthcare, finance, gambling, alcohol, dating) — additional certification required
- Personal pronouns in display URL paths look spammy: `/you-need-this` will flag

2025-2026 Policy Updates:

- Asset-level disapprovals (April 2026, PMax + Demand Gen) — Google now disapproves individual assets, not the whole group. Submit 8-10 assets per slot as buffer.
- AI-generated content disclosure (March 2026) — Any AI-generated creative element (image, video, voice) must carry "AI Generated" label. Deepfake-style human likeness banned outright.
- LLM semantic review — Text assets parsed by LLM, not regex. False-positive trigger categories: healthcare imagery (15-25%), before/after (20-30%), superlatives (10-15%), testimonials (15-20%), financial charts (10-20%).
- Predictive enforcement — Google flags ads before they violate based on account history + vertical. New accounts in regulated verticals see pre-emptive limited serving.
- Hidden-fees rule (auto retail Oct 2025, spillover expected) — All-in pricing required in vehicle ads; subscription/SaaS likely next.

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
- Long description: [copy] — [chars/90]
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
