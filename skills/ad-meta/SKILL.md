---
name: ad-meta
title: "Meta Ads Production Spec (Facebook + Instagram)"
description: "What to produce for a Meta ad — Facebook Feed, Instagram Feed, Stories, Reels, and the CTA enum. Encodes the exact slots (primary text, headline, description, CTA button), character limits, asset ratios (1:1, 4:5, 9:16), policy filters, and the truncation behavior that decides whether anyone reads past the fold. Use whenever the task is producing Meta ad copy or asset briefs. Strictly platform-specific — does not cover audience setup, pixel events, or campaign objectives."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to Meta (Facebook + Instagram)."
domains: launch
rules:
  - content(meta ads)
  - content(facebook ads)
  - content(instagram ads)
  - match(\bmeta\s+ads?\b)
  - match(\bfacebook\s+ads?\b)
  - match(\binstagram\s+ads?\b)
  - match(\b(IG|FB)\s+ads?\b)
  - match(\breels\s+ads?\b)
  - match(\bstories\s+ads?\b)
  - semantic(write a facebook ad)
  - semantic(produce instagram reel ad copy)
  - semantic(meta ad primary text)
---

## Overview

This skill defines exactly what to produce for a Meta ad creative across Facebook and Instagram. It is platform-spec only: the slots Meta exposes, the truncation thresholds that decide what users see, the asset ratios per placement, and the CTA button enum. It does not cover audience setup, conversion events, Advantage+ settings, or attribution.

Meta is unusual: most copy fields have no hard cap, only truncation thresholds. Writing past the threshold is fine — but the text after the truncation point is read by almost no one. Treat thresholds as your real limits.

## Instructions

### Placements Covered

| Placement | What You Produce |
|-----------|------------------|
| Facebook Feed | Primary text, headline, description, image/video, CTA button |
| Instagram Feed | Primary text, image/video, CTA button (headline shows less prominently) |
| Stories (FB + IG) | Vertical video/image, optional sticker text, CTA |
| Reels (FB + IG) | Vertical video, primary text, CTA — sound-on but caption-required |
| Marketplace | Same as Feed, narrower visible primary text |
| Audience Network | Headline, description, image/video, CTA |
| Threads Ads (globally rolled out Jan 2026) | Must co-run with IG Feed; single image, single video, image-carousel; 1:1 or 4:5; 80-160 char primary text sweet spot |
| Carousel Ads | 2-10 cards with per-card image/headline/URL; shared primary text |
| Collection Ads | Hero (1:1 or 1.91:1) + 4 product tiles from catalog; opens Instant Experience; mobile-only |
| Lead Ads | Native in-app form, no landing page; intro card + ≤3-5 questions + privacy URL + thank-you |
| Messenger / Click-to-Messenger Ads | Feed creative + "Send Message" CTA → opens Messenger thread with welcome template (≤3 quick-reply chips) |
| Click-to-WhatsApp Ads | Feed/Reels/Stories creative + "Send WhatsApp Message" CTA → opens WA chat with pre-filled message (≤160 char, editable) |
| Advantage+ Shopping campaigns | Up to 150 creatives per campaign; catalog feed must include 1:1 + 4:5 (+ 9:16 for Reels) |

### Feed — Slots and Limits

| Slot | Preview Threshold | Hard Cap | Notes |
|------|-------------------|----------|-------|
| Primary text | ~125 chars before "See more" | 63,206 (effectively unlimited) | First 125 chars decide click-through |
| Headline | 27 chars before truncation | 40 chars recommended | Below image on Feed; smaller on IG |
| Description | 27 chars before truncation | 30 chars recommended | News-Feed-only on FB |
| URL | n/a | n/a | Destination URL |
| CTA button | Enum | n/a | See CTA section below |

### Stories / Reels — Slots and Limits

| Slot | Notes |
|------|-------|
| Primary text | Optional, smaller display, treat 60 chars as visible budget |
| Headline | Not always shown on Stories — Reels show it but small |
| Visual | 9:16 vertical, full screen, sound-on but assume sound-off readability |
| CTA button | Enum, anchored to bottom of screen |
| Sticker text | Manual overlay on the asset itself, not a Meta-managed field |

### Visual Ratios by Placement

| Placement | Recommended Ratio | Notes |
|-----------|-------------------|-------|
| Facebook Feed | 1:1 (1080×1080) or 4:5 (1080×1350) | 4:5 takes more mobile screen |
| Instagram Feed | 1:1 or 4:5 | Same — 4:5 outperforms 1:1 on mobile |
| Stories | 9:16 (1080×1920) | Full screen, safe zone matters |
| Reels | 9:16 (1080×1920) | Same as Stories |
| Right Column | 1.91:1 (1200×628) | Desktop only, tiny — use brand visuals |
| Audience Network | 1:1 or 1.91:1 | Varies by publisher |
| Marketplace | 1:1 | Same as Feed |
| Video minimum | 1 second | Practical min: 6–15s for short, 15–30s for full |
| Video max | 241 minutes (Feed) | Practical max: 60s for performance ads |
| Reels video max | 90 seconds | Sweet spot: 15–30s |
| Stories video max | 60 seconds (auto-split into 15s cards) | Each card is its own segment |
| File size — image | 30 MB | JPG or PNG |
| File size — video | 4 GB | MP4, MOV, GIF |

### Safe Zones (Stories / Reels)

- Top ~14% (≈270px on 1920px asset) reserved for username/handle overlay — never put critical copy there
- Bottom ~20-35% (≈380-670px depending on CTA + caption stack) reserved for CTA button + interaction icons + caption — never put critical copy there
- Effective safe zone: middle band of the 1920px height
- Logo + key copy belongs in the middle band

### Advantage+ Creative (Default-On Since Feb 2026)

Default ON for Sales, Leads, and App Promotion objectives. The system auto-applies these enhancements unless toggled off per ad:

1. Image enhancement (recolor / crop)
2. 3D parallax effect
3. Music overlay
4. Image expansion (generative fill)
5. Alt headlines generation
6. Primary text variants generation
7. Image animation (animate statics)
8. Text variations generation

Brand-safety opt-outs (toggle per ad, persist across future campaigns since Mar 2026):
- Disable "Image enhancement" + "3D effect" for brand-driven creative
- Disable "Music" for accounts with sonic identity
- Disable "Image animation" for product photography
- Disable "Text variations" + "Image expansion" for regulated verticals

### CTA Button Enum (Pick One — 2026 Full Enum)

Meta only allows CTAs from this enum (selection depends on campaign objective). Cannot use custom CTA text.

Action / commerce:
- Apply Now
- Book Now
- Buy Tickets
- Download
- Get Access
- Get Directions
- Get Offer
- Get Quote
- Get Showtimes
- Install Now
- Order Now
- Request Time
- Shop Now
- Sign Up
- Subscribe
- Use App

Info / engagement:
- Contact Us
- Donate Now
- Learn More
- Listen Now
- Play Game
- Read More
- See Menu
- View Menu
- Watch More
- Watch Now

Messaging-objective only:
- Call Now
- Send Message (opens Messenger)
- Send WhatsApp Message (opens WhatsApp thread)

Pick the CTA that matches the actual landing-page action. "Learn More" is the universal default but converts worse than a verb that names the action.

### Hook Rules (Where Reads Actually Happen)

Meta is brutal about scroll-speed. The first 3 elements decide everything:

1. The image / video first frame — must stop the thumb
2. First 3 words of primary text — must reward the stop
3. The next line before "See more" — must promise something worth the click

So:
- Primary text first sentence must hook in ≤125 chars
- Do not lead with a brand name or "we are excited to announce" — pure scroll-past
- Video first frame must be the hook, not a logo intro
- Caption every line of video — 85%+ of Meta video plays on mute

### Policy Constraints (Common Rejections)

- Personal attributes: "Are you depressed?" / "Diabetics, listen up" — Meta's Personal Attributes policy bans calling out the viewer's condition
- Before/after imagery: banned for weight loss, cosmetic, financial outcomes — even if real
- Sensational language: "Shocking", "You won't believe" — manual review trigger
- Misleading scarcity: "Last day!" "Only 3 left!" without evidence — disapproval
- Profanity: even mild ("damn") — disapproval
- Restricted categories: weight loss, gambling, dating, financial products, healthcare — require certification
- Body parts isolated from context: cropped tight on stomach/legs — disapproval risk
- Text-on-image rule: was strict, now relaxed — but heavy text overlays still suppress delivery (lower reach, higher CPM)

### Output Format

```markdown
# Meta Ads — [Product] [Campaign Name]

## Placements
[Facebook Feed / Instagram Feed / Stories / Reels / Audience Network]

## Final URL
[Landing page URL]

## Primary Text
> [Copy — first sentence ≤125 chars must hook]
> [Rest of copy if any]

Preview slice (first 125 chars): "[show what users see before See more]"

## Headline (≤27 char recommended, ≤40 hard)
> [Headline] — [chars]

## Description (≤27 char recommended)
> [Description] — [chars]

## CTA Button (enum only)
[Selected CTA from enum] — [why this one matches the landing action]

## Visual Spec
- Ratio: [1:1 / 4:5 / 9:16]
- Shot: [concrete scenario, not stock]
- Text overlay: "[copy on the image/video]"
- First frame (video): [what's visible at 0s]
- Caption track: [yes — list per-scene captions if video]

## Variant Set
| # | Angle | Primary Text Opener | Headline | CTA | Visual |
|---|-------|---------------------|----------|-----|--------|
| 1 | [angle] | [≤125 char] | [≤27] | [enum] | [ratio + shot] |
| 2 | ... | ... | ... | ... | ... |

## Pre-Submit Checklist
- [ ] Primary text hook within first 125 chars
- [ ] First 3 words of primary text are not brand-name throat-clearing
- [ ] CTA button from enum, matches landing action
- [ ] Video first frame is the hook
- [ ] All video text captioned (85% mute viewing)
- [ ] Safe zones respected for Stories/Reels
- [ ] No personal-attribute language ("you, the [condition]")
- [ ] No before/after for restricted verticals
- [ ] No misleading scarcity
- [ ] Visual ratio matches placement
```

## When NOT to Use This Skill

- Audience setup, lookalike creation, retargeting rules → out of scope
- Pixel events, Conversions API setup → out of scope
- Campaign objective selection, Advantage+ settings → out of scope
