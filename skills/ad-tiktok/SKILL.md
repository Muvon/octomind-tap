---
name: ad-tiktok
title: "TikTok Ads Production Spec"
description: "Specifies what to produce for a TikTok ad: In-Feed Ads, Spark Ads, TopView, Branded Effect, and Branded Mission, with the exact slots (caption, display name, CTA), character limits, the 9:16 vertical asset spec, sound-on requirements, the safe-zone map that decides what is visible on phones, and the native-feeling creative rules that decide whether the algorithm pushes or buries. Use whenever the task is producing TikTok ad copy or video briefs; strictly platform-specific, so it does not cover audience setup or pixel events."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to TikTok Ads."
domains: launch
rules:
  - content(tiktok ads)
  - content(tiktok ad)
  - match(\btiktok\s+ads?\b)
  - match(\bin.feed\s+ads?\b)
  - match(\bspark\s+ads?\b)
  - match(\btopview\s+ads?\b)
  - match(\bbranded\s+effect\b)
  - match(\bbranded\s+mission\b)
  - semantic(write a tiktok ad)
  - semantic(produce tiktok ad script)
  - semantic(tiktok spark ad)
---

## Overview

This skill defines exactly what to produce for a TikTok ad. It is platform-spec only: the slots TikTok exposes, the limits per format, the 9:16 safe zone, the CTA enum, and the native-feel rules that decide whether the platform pushes the ad or buries it.

2026 context: in the US, TikTok runs under the USDS joint venture since January 2026. Ads Manager, Smart+, TopView, and In-Feed formats continued through the transition, but delivery may shift as the US recommendation system is retrained — re-check baselines and targeting approvals for US campaigns.

## Instructions

### Ad Formats Covered

| Format | What You Produce |
|--------|------------------|
| In-Feed Ad | Vertical video + caption + display name + CTA — runs in For You feed |
| Spark Ad | Boosted version of an existing organic post — uses the original creator's account. Caption is inherited and NOT editable in Ads Manager |
| TopView | First impression a user sees on opening TikTok — premium placement |
| Brand Takeover | Largely consolidated into TopView since 2023-24 — treat as legacy |
| Branded Effect | Custom AR effect / filter built via Effect House, ≤5 MB, safety review (5-10 business days) |
| Branded Mission | UGC challenge — brand briefs creators to make videos |
| Carousel Ads | 2–35 images, swipeable, with caption + CTA. ONE shared CTA across all cards. 9:16 or 1:1, 720×720 min |
| Lead Gen | In-Feed Ad + native Instant Form, ≤10 questions, privacy URL required |
| TikTok Shop — Video Shopping Ads (VSA) | 9:16, ≤10 min. GMV Max became the default (and for most sellers only) campaign type for Shop ads in July 2025 — verify live. Product Card pops in bottom — safe zone bottom must be 450px |
| TikTok Shop — LIVE Shopping Ads | Promote active livestream; ad asset = vertical thumbnail/clip + headline |
| TikTok Shop — Product Shopping Ads (PSA) | Catalog-driven, product-image-led, no required video. Image: 1:1 or 4:5, ≥600×600. Served on Shop tab + search + For You |
| TikTok Search Ads | Keyword-bid, served on the Search Results Page. Spec mirrors In-Feed; show keywords as on-screen text or overlays and put keywords in the ad title and description (official, TikTok Search Ads creative tips, 2026-01). Keyword minimums and match types change — verify in Ads Manager |
| Pulse Suite (Premiere/Core/Mentions/Tastemakers) | Contextual placement adjacent to premium content. Standard In-Feed video spec; copy/tone must match the lineup context |

### In-Feed Ad — Slots and Limits

| Slot | Limit | Notes |
|------|-------|-------|
| Caption | No character cap on the specs page; Spark captions display max 4 lines | Overlays bottom-left on video; front-load the hook. Non-Spark ad captions don't support hashtags, @mentions or clickable links (official, TikTok video ads specifications, 2026-06) |
| Display name | 2–20 chars | The advertiser name shown |
| Profile image | 1:1, ≥98×98 px | Round-cropped on display |
| Video | 9:16, 5–60s (up to 3 min available) | MP4 or MOV; 540×960 minimum, 1080×1920 recommended |
| CTA button | Enum | See CTA section |
| Landing URL | URL | Where the click goes |

### Video Asset Specs

| Spec | Value | Notes |
|------|-------|-------|
| Aspect ratio | 9:16 recommended; 1:1 and 16:9 supported | Use 9:16 unless you have a specific reason |
| Resolution | ≥540×960 (9:16); ≥640×640 (1:1); ≥960×540 (16:9). 1080×1920 production target | Higher quality preferred |
| File format | MP4, MOV, MPEG, AVI | MP4 strongly recommended. GIF dropped. |
| Duration | 5–60s typical, up to 10 minutes allowed | Choose length by payoff; the proposition lands in the first 3s |
| File size | ≤500 MB | Compress without losing motion |
| Bitrate | ≥516 kbps | Higher recommended |
| Audio | Required — sound-on platform | Music + voiceover + captions (all three) |

### Safe Zones (9:16 Canvas)

The TikTok UI overlays the bottom and right edges. Critical copy must stay in the safe zone.

| Region | Use |
|--------|-----|
| Top 130px | Mostly safe; status bar overlays first ~80px on some devices |
| Right 270px | Reserved for Like / Comment / Share / Profile icons — never put copy here |
| Bottom 480px | Reserved for caption, display name, CTA, and music attribution — never put critical copy here |
| Effective safe zone | Center, top ~130px to bottom ~480px, left edge to ~810px from left | Where headline + product reveal must live |

### CTA Button Enum

- Download
- Shop Now
- Sign Up
- Watch More
- Learn More
- Apply Now
- Book Now
- Contact Us
- Get Quote
- Get Showtimes
- Install Now
- Listen Now
- Order Now
- Play Game
- Read More
- Subscribe
- View Now
- Visit Store
- See Menu

### Caption Rules

- Front-load the hook and CTA; the specs page lists no character cap, so keep it short and test truncation in the Ads Manager preview
- Lead with the hook, not the brand
- Specificity wins — "5 mins to set up" beats "easy to use"
- No hashtags, @mentions or links in non-Spark ad captions (unsupported); Spark captions inherit from the organic post
- Avoid "link in bio" copy — the CTA button is right there
- Use vowel-light shorthand only if it reads natural on TikTok (e.g., "POV:", "tell me you…")

### Native-Feel Rules — What Wins on TikTok

- Founder voice or UGC creator > polished studio voice. Selfie-cam outperforms tripod cinematography.
- Put the proposition in the first 3 seconds and test creatives that differ visually from each other (official, TikTok creative best practices, 2025-06). Visual + text overlay + spoken word all hit in second 0.
- Sound-on platform; caption everything anyway for accessibility and clarity.
- Show, don't pitch. The product must appear and demonstrate value, not be described.
- Use trending audio when it fits — but only via Spark Ads or with proper licensing. Stolen trending audio = take-down.
- Avoid HD studio polish, drone shots, brand-jingle outro. They scream "ad."
- 1 message per video. Multi-product or multi-feature videos underperform.
- End on action — what to do next must be the last beat.

### Spark Ad Rules

Spark Ads boost an existing organic post — either yours or a creator's (with permission). Specs match In-Feed Ad. The advantage: comments, likes, shares accumulate to the original post, building social proof.

- Always seek creator permission via the Branded Content Toggle or paid arrangement before boosting
- Disclose the partnership via the Branded Content Toggle (TikTok's #ad equivalent)
- Engagement accumulates on the original post, so social proof builds there; don't promise a cost or click advantage over In-Feed

### Branded Mission Rules

Brand briefs creators to produce videos under a campaign tag. The brand pays a fixed pool, creators compete for top performance.

- Brief must be tight: hook idea + product moment + CTA — let creators handle the rest
- Sound-on, vertical, native creator voice — the whole point is creator authenticity
- Hashtag mandatory — the campaign tag is the search index

### Policy Constraints (Common Rejections)

- Misleading claims, before/after weight/fitness — auto-disapproval
- Trademark / copyrighted music without licensing — take-down
- Restricted verticals: alcohol, dating, financial, gambling, healthcare, weight loss — region-specific certification
- Personal attribute targeting in copy — Personal Attributes policy
- Shock content, violence, dehumanising language — disapproval + account risk
- Content claiming health benefits without certification — disapproval
- Ads aimed at users under 18 — strict content rules
- Realistic AI-generated people, voices, or scenes — label as AI-generated per TikTok's AIGC rules (assets from TikTok's own Symphony tools carry labels; verify the ad-side disclosure setting)
- Paid creator content — Branded Content toggle on; US FTC Endorsement Guides apply to the creator's disclosure

### Output Format

```markdown
# TikTok Ads — [Product] [Campaign Name]

## Format
[In-Feed / Spark / TopView / Branded Mission / Carousel]

## Landing URL
[URL]

## Caption (front-loaded, no hashtags/@mentions/links for non-Spark)
> [Caption text] — [chars]

## Display Name (2–20 char)
[Name] — [chars]

## CTA Button (from enum)
[Selected CTA]

## Video Spec
- Ratio: 9:16
- Duration: [Xs]
- Resolution: 1080×1920
- Audio: [music + VO / VO only / native sound]
- Captions: yes (every spoken line)

## Scene Plan
| Time | Scene | Spoken / VO | Text Overlay | Notes |
|------|-------|-------------|--------------|-------|
| 0:00–0:02 | Hook | "[opening line]" | "[overlay]" | First frame must stop scroll |
| 0:02–0:08 | Setup | "[VO]" | "[overlay]" | Problem or context |
| 0:08–0:18 | Reveal | "[VO]" | "[overlay]" | Product / solution moment |
| 0:18–0:25 | Proof | "[VO]" | "[overlay]" | Demo, metric, testimonial |
| 0:25–0:30 | CTA | "[VO]" | "[overlay]" | What to do next |

## Safe Zone Check
- [ ] Critical copy stays out of right-rail (icons) and bottom 480px (caption/CTA area)
- [ ] First frame hook is in center safe zone

## Variant Set
| # | Angle | Hook (first 2s) | Caption | CTA | Aesthetic |
|---|-------|-----------------|---------|-----|-----------|
| 1 | [angle] | "[opening]" | [caption] | [enum] | [founder POV / UGC / native] |
| 2 | ... | ... | ... | ... | ... |

## Pre-Submit Checklist
- [ ] 9:16 vertical, 1080×1920 minimum
- [ ] Hook in first 1–3 seconds
- [ ] Sound-on with captions
- [ ] Native feel — no studio polish, no jingle outro
- [ ] Caption front-loaded; no hashtags, @mentions or links (non-Spark)
- [ ] CTA from enum
- [ ] Safe zone respected
- [ ] Music licensed (or Spark Ad with permissions)
- [ ] No misleading claims, no restricted vertical issues
- [ ] Show, don't pitch
- [ ] One message per video
```

## When NOT to Use This Skill

- Audience setup, custom audiences → out of scope
- Pixel events, conversion tracking → out of scope
- Branded content disclosure rules → covered briefly, full compliance review separate

## References

- [Video ads specifications](https://ads.tiktok.com/help/article/video-ads-specifications), official, 2026-06; [Creative best practices](https://ads.tiktok.com/help/article/creative-best-practices), official, 2025-06; [Search Ads creative tips](https://ads.tiktok.com/help/article/search-ads-creative), official, updated 2026-01.
