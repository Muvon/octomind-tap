---
name: ad-x
title: "X (Twitter) Ads Production Spec"
description: "What to produce for an X (Twitter) ad — Promoted Posts, Website Cards, App Cards, and Video Ads. Encodes the exact slots (post text, card title, card description, CTA enum), character limits (280 post, 70 card title, 200 card description), asset ratios, and the native-feel rules that decide whether the algorithm classes it as quality content or scroll-past. Use whenever the task is producing X ad copy or card assets. Strictly platform-specific — does not cover audience targeting, conversion tracking, or organic posting strategy."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to X/Twitter Ads."
domains: launch
rules:
  - content(twitter ads)
  - content(x ads)
  - content(promoted tweet)
  - content(promoted post)
  - match(\b(x|twitter)\s+ads?\b)
  - match(\bpromoted\s+(post|tweet)\b)
  - match(\bx\s+(website|app)\s+card\b)
  - match(\btwitter\s+(website|app)\s+card\b)
  - semantic(write an x ad)
  - semantic(promoted post for twitter)
  - semantic(x website card)
---

## Overview

This skill defines exactly what to produce for an X (Twitter) ad. It is platform-spec only: the slots X exposes for Promoted Posts, Website Cards, App Cards, and Video Ads, the character limits, asset ratios, and the CTA button enum.

## Instructions

### Ad Formats Covered

| Format | What You Produce |
|--------|------------------|
| Promoted Post | Post text (280 char), optional media, native append (no extra card) |
| Promoted Post + Website Card | Post text + image/video + card title + URL + CTA |
| Promoted Post + App Card | Post text + image/video + card title + app ID + CTA |
| Video Ad | Promoted Post with video + optional Website / App Card append |
| Image Carousel | 2–6 images, each with optional URL + CTA |
| Vertical Video Ad | Full-screen 9:16 video — runs in Immersive Media Viewer (Video tab) and dedicated placements |
| Spotlight Takeover | 24h top of Explore "For you" tab — premium |
| Timeline Takeover | 24h takeover on Home Timeline — premium |
| Trend Takeover / Trend Takeover+ | Premium trend sponsorship; Trend Takeover+ adds auto-playing video on tap |
| Amplify Pre-Roll | Pre-roll on publisher video across 15+ content categories; 1:1 recommended |
| Dynamic Product Ads (DPA) | Catalog-driven, requires X Pixel/CAPI + Shopping Manager; single/collection/carousel render |

### Promoted Post — Slots and Limits

| Slot | Limit | Notes |
|------|-------|-------|
| Post text | 280 chars | Same as organic; emojis count |
| Media | 1 image, up to 4 images, or 1 video, or 1 GIF | Image OR video, not both |
| Card append | Optional | If used, draws Website Card or App Card below post |

### Website Card — Slots and Limits

| Slot | Limit | Notes |
|------|-------|-------|
| Card title | 70 chars | Bold line below image/video |
| Card image | 1.91:1 (1200×628) or 1:1 (800×800) | Required if no video |
| Card video | 16:9, 1:1, or 9:16 | Up to 2:20 — sweet spot 15–60s |
| Destination URL | URL | Landing page |
| CTA button | Enum | See CTA section |
| Display URL | Auto-shortened | Cannot be customised |

### App Card — Slots and Limits

| Slot | Limit | Notes |
|------|-------|-------|
| App icon | Pulled from app store | Auto |
| App name | Pulled from app store | Auto |
| App rating | Pulled from app store | Auto |
| Card image | 1.91:1 or 1:1 | Required if no video |
| Card video | 16:9, 1:1, 9:16 | Up to 2:20 |
| CTA button | "Install", "Open", "Play", "Book" | Limited App CTA set |

### Image / Video Specs

| Asset | Spec | Notes |
|-------|------|-------|
| Promoted Post image | 1200×675 (16:9) or 1200×1200 (1:1) | JPG / PNG, max 5MB |
| Multi-image (carousel) | 2–6 images, each 800×800 (1:1) | Up to 6 images |
| Promoted Post video | 16:9 (1920×1080) or 1:1 (720×720) or 9:16 (720×1280) | MP4, max 1GB, up to 2:20 |
| Vertical Video Ad | 9:16 (1080×1920) | Full-screen Explore placement |
| GIF | Up to 15MB | Auto-loops |
| Video bitrate | 6,000–10,000 kbps | Higher for vertical |
| Video frame rate | 29.97 or 30 fps | 60 fps allowed |

### CTA Button Enum (Website Card / App Card — 2025+ Sales-Objective Link Preview)

X consolidated the CTA enum in 2025 alongside the new Sales-objective link preview format. Both Website Card and App Card now share this enum:

- Play
- Install
- Open
- Book
- Shop
- Connect
- Order

Legacy CTAs (Learn More, Sign Up, Buy Now, Visit Site, Subscribe, Get Quote, Shop Now) are deprecated in the new link preview but may still appear on older running campaigns. Do not use legacy values in new creative.

### Copy Rules — Promoted Post Must Read Native

- 280 chars is the hard cap, but the sweet spot is 70–150. Walls of text scroll past in milliseconds.
- First line carries the post. The image or hook line must stop the thumb in ≤1 second.
- No hashtags unless they're real topic tags (X's topic system, not arbitrary #marketing).
- 1 link per post — if you append a Website Card, do NOT also put the URL in the text. Pick the card.
- Emojis: 0–2, and only if they replace a word or anchor an idea. Decorative emoji strings (✨🚀💯) flag as low-quality.
- Avoid "Click the link below" — readers know.
- Avoid "Hey [audience]," openers — algorithmic cold-start penalty.
- Brand-safety verdict: edgy is fine if defensible. Crude language drops `MediumRisk` → ads system pulls placements → reach collapses.

### Algorithm Touchpoints (for ad-as-post)

X's ad surface ranks against the same For You ranker (Phoenix-era) as organic. Promoted Posts pass through:

- Banger Initial Screen — VLM scores quality + slop. Templated copy gets flagged. Make it look like a real artifact.
- Scroll-past as negative signal — failing to earn dwell costs score across the audience cluster.
- 7 PTOS safety classifiers — a single hit zeroes the post. Ad disapproval is the visible form; reach loss is the invisible form.

Takeover surfaces (Timeline, Trend, Spotlight) bypass the auction but still hit safety classifiers.

### Audience Reach Caveat (Premium / Premium+)

- Premium+ users see NO ads in feeds
- Premium tier users see ~50% fewer ads in For You / Following
- Material consequence: organic-feeling creative compounds harder because the in-feed surface skews toward less-subscribed users
- Char-count gotcha: if a URL is embedded in post text (not card-attached), each URL consumes 23 chars of the 280 budget — usable copy drops to 257 chars

### Policy Constraints

- Trademark / copyrighted material without authorisation — disapproval
- Misleading metrics ("10M users" without proof) — manual review
- Crypto (Feb 2026 update) — exchanges, wallets, kiosks/ATMs, debit/credit cards permitted in SA, KW, TR, IE, HK, KR, UK, FR, DE only. Singapore removed in 2026. Other crypto products still gated. All paid promotional crypto content (including influencer shilling) requires machine-readable disclosure or account suspension
- Gambling — restricted, country-specific certification required
- Adult content — banned in ads even though organic permits some under the Adult Content Creator (ACC) program
- Political / issue ads (2026) — reinstated under structured disclosure across 38 eligible countries. Required: certified advertiser status + machine-readable "Paid For By" disclosure. Targeting an ineligible country = auto-reject
- Personal attributes targeting in copy — disapproval risk
- Sensitive personal events (illness, bereavement) — restricted
- Adjacency exclusion — ads will not serve adjacent to 12 categories (adult, violence, political conflict, profanity, drugs, spam, misinfo, hate, terrorism, self-harm, gambling, obscenity). Affects reach in regulated verticals

### Output Format

```markdown
# X Ads — [Product] [Campaign Name]

## Format
[Promoted Post / Website Card / App Card / Video Ad / Carousel / Vertical Video]

## Destination URL
[Landing page URL]

## Promoted Post Text (≤280, ≤150 ideal)
> [Copy — first line is the hook]

Char count: [N]/280

## Website Card (if attached)
- Card title (≤70 char): [title] — [chars]
- CTA: [from enum]
- Image / video: see visual spec

## Visual Spec
- Asset type: [Image / Video / GIF / Carousel]
- Ratio: [16:9 / 1:1 / 9:16]
- Shot: [concrete scenario]
- Text overlay (video): "[per-scene captions]"
- First frame (video): [what's visible at 0s — must hook]

## Carousel (if used)
| # | Image (1:1) brief | URL | CTA |
|---|-------------------|-----|-----|
| 1 | [shot] | [URL] | [enum] |
| 2 | ... | ... | ... |

## Variant Set
| # | Angle | Post Text (≤280) | Card Title | CTA |
|---|-------|------------------|------------|-----|
| 1 | [angle] | [hook line + rest] | [≤70] | [enum] |
| 2 | ... | ... | ... | ... |

## Pre-Submit Checklist
- [ ] Post reads native — could pass as organic
- [ ] Post text ≤280 char (ideally ≤150)
- [ ] First line hooks in ≤1 second of read
- [ ] No "click the link below" or "Hey [audience]"
- [ ] One link OR one card — not both
- [ ] Emojis ≤2 and load-bearing, not decorative
- [ ] No hashtag spam
- [ ] CTA from correct enum (Website vs App card)
- [ ] Video captioned for silent autoplay
- [ ] Brand-safety: crude language out, defensible edgy in
- [ ] Visual ratio matches placement
```

## When NOT to Use This Skill

- Audience targeting / tailored audiences → out of scope
- Conversion tracking / Pixel setup → out of scope
