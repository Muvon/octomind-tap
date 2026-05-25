---
name: ad-youtube
title: "YouTube Ads Production Spec"
description: "What to produce for a YouTube ad — Skippable In-Stream (TrueView), Non-Skippable, Bumper, In-Feed (Discovery), Masthead, and YouTube Shorts. Encodes the exact slots (headline, description, companion banner, CTA), duration limits, asset ratios (16:9, 9:16, 1:1), the first-5-seconds hook rule that decides whether anyone watches past skip, and the policy constraints. Use whenever the task is producing YouTube ad copy or video briefs. Strictly platform-specific — does not cover audience targeting, conversion linkage, or Google Ads campaign setup."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to YouTube Ads."
domains: launch
rules:
  - content(youtube ads)
  - content(youtube ad)
  - match(\byoutube\s+ads?\b)
  - match(\btrueview\b)
  - match(\bin.stream\s+ads?\b)
  - match(\bbumper\s+ads?\b)
  - match(\bshorts\s+ads?\b)
  - match(\byoutube\s+(shorts|masthead)\s+ads?\b)
  - semantic(write a youtube ad)
  - semantic(youtube preroll script)
  - semantic(produce a youtube bumper ad)
---

## Overview

This skill defines exactly what to produce for a YouTube ad. It is platform-spec only: the formats YouTube offers, duration constraints, the slots the ad serves into (headline, description, companion banner, CTA), and asset ratios per surface.

YouTube ads are bought through Google Ads but follow their own creative rules. Most decisions live in the first 5 seconds — that's the skip-decision window for skippable formats and the entire ad for Bumpers.

## Instructions

### Ad Formats Covered

> 2024-2026 naming/sunset updates: "TrueView In-Stream" → Skippable In-Stream Ads (TrueView branding fully deprecated). "Discovery Ads" → In-Feed Video Ads. Video Action Campaigns (VAC) sunset — new VACs blocked from March 2025, all remaining VACs auto-upgraded to Demand Gen in Q2 2025. Demand Gen is now the primary action/conversion video buying type.

| Format | Duration | Skippable | Where It Shows |
|--------|----------|-----------|----------------|
| Skippable In-Stream Ads | ≥12s, no max (sweet spot 15–60s) | After 5s | Pre/mid/post-roll on watch pages |
| Non-Skippable In-Stream | 6–15s standard globally; 15-20s in select markets/reservation buys | No | Pre/mid/post-roll |
| Bumper Ads | ≤6s | No | Pre/mid/post-roll |
| In-Feed Video Ads (formerly Discovery) | Any | n/a (click-to-watch) | YouTube search results, watch-next sidebar, homepage |
| Masthead | Up to 30s autoplay muted | n/a | YouTube homepage hero — reservation-only buy |
| Shorts Ad | ≤60s plays in feed (uploadable up to 3 min, only first 60s plays), 9:16 | Skippable via swipe at any moment | Shorts feed (vertical) |
| Demand Gen Ads (YouTube placements) | Multi-format mix | n/a | YouTube In-Stream + In-Feed + Shorts + Discover + Gmail. Replaces VAC. |
| Video Reach Campaigns (VRC) | Mixed Bumper + Skippable + In-Feed | mixed | Automated reach mix |
| Video View Campaigns (VVC) | View-optimized | mixed | Skippable In-Stream + In-Feed + Shorts at lower CPV |
| Connected TV (CTV) / YouTube on TV screens | Standard 16:9 | n/a | TV screens — no CTA overlay, no companion banner; use QR code or "search [brand]" fallback |
| YouTube Select | Premium reservation | mixed | Top 5% inventory, brand-safe lineups |
| Pause Ads (rolling out CTV 2025-2026) | Static | n/a | Shown when viewer pauses on TV; 16:9 1920×1080 + CTA overlay |
| Outstream (off-YouTube) | Up to 60s | n/a | Google Video Partners network |

### Skippable In-Stream — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Video | ≥12s; sweet spot 15–60s | Hook in first 5s before skip |
| Headline | 15 chars | Shown alongside ad |
| Description | 2 lines × 35 chars | Optional |
| Companion banner | 300×60 (auto-generated or custom) | Desktop only |
| CTA overlay | 10 chars | Optional clickable overlay during video |
| Final URL | URL | Landing page |

### Non-Skippable In-Stream — Slots

Same as Skippable, but:
- Duration: 15s or 20s only (region-dependent)
- No skip — full watch is forced
- Higher CPM, sharper diminishing returns past second 10
- Region-restricted: not available in all markets

### Bumper Ad — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Video | ≤6s | Hard cap; one beat, one message |
| Companion banner | 300×60 | Optional |
| Headline | 15 chars | Optional |
| Description | 2 lines × 35 chars | Optional |

### In-Feed (Discovery) Ad — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Thumbnail | Custom upload, 1280×720 | Hero of the click |
| Headline | 100 chars | Shown next to thumbnail |
| Description line 1 | 35 chars | First visible line |
| Description line 2 | 35 chars | Second visible line |
| Video | Any duration | The video the click plays |

### Masthead — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Video | Up to 30s | Autoplay muted on homepage |
| Headline | 25 chars | Below video |
| Description | 35 chars × 2 lines | Below headline |
| CTA button | 10 chars | Optional |
| Companion video panel | 1280×720 still | Right side of hero |

### Shorts Ad — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Video | 9:16, ≤60s | Sweet spot 15–30s |
| Caption / overlay | Manual on video | No native caption field |
| CTA button | Enum | Shown at bottom |
| Landing URL | URL | |

### Video Asset Specs

| Asset | Spec | Notes |
|-------|------|-------|
| In-Stream / Bumper / Masthead | 16:9 (1920×1080) | Standard widescreen |
| Vertical (also accepted for In-Stream) | 9:16 (1080×1920) | Improves Shorts placement |
| Square (also accepted) | 1:1 (1080×1080) | Mobile-friendly fallback |
| Shorts | 9:16 (1080×1920) | Mandatory |
| Hosted on | YouTube | Must be uploaded to YouTube first |
| Visibility | Public or Unlisted | Private videos cannot run as ads |
| Audio | Required | Sound-on by default for In-Stream |

### CTA Button Enum (when CTA button is available)

YouTube CTA text is pulled from the same Google Ads enum as Display/PMax. Common values:
- Sign Up
- Shop Now
- Learn More
- Get Quote
- Install Now
- Subscribe
- Watch Now
- Apply Now
- Book Now
- Contact Us
- Download

CTA text in YouTube ads is limited to 10 chars on the in-video overlay button — use punchy verbs.

### The First-5-Seconds Rule (Skippable In-Stream)

The skip button appears at second 5. Everything before that decides:
1. Whether the view counts as paid (5s view = paid impression for TrueView)
2. Whether the user clicks the skip
3. Whether they remember the brand at all

Production rules:
- Brand reveal by second 1 (logo, name, or product visible)
- Hook line in seconds 0–3 — name the audience or the problem
- Pay-off promise by second 4 — what they'll see if they don't skip
- Value beat by second 7 — give them something even if they skip
- Reserve full pitch for seconds 10–30
- End with CTA at seconds 25–30 even for longer ads

### Bumper Ad — One Beat Only

6 seconds is one idea. Not two. Not a beginning-middle-end. One.

- Open with the visual punchline
- One spoken line max
- Brand reveal must be visible by second 2
- End on the product/logo + a single-verb CTA on screen

### In-Feed (Discovery) Thumbnail Rules

The thumbnail does the work, not the title. The viewer chooses to click — there's no forced impression.

- Thumbnail should not look like a typical ad
- High contrast, expressive face or sharp product shot
- Avoid text-on-thumbnail unless ≤4 words
- Match the thumbnail to the YouTube watch context — looks like a video they'd choose

### Policy Constraints (Common Rejections + 2024-2026 Updates)

- Disturbing content, gore, jump scares — disapproval
- Misleading thumbnails (clickbait that doesn't reflect the video) — disapproval
- Repeating content (same ad uploaded multiple times) — disapproval
- Inappropriate content for ads — even if monetisable as organic, ads have stricter rules
- Embedded ads / sponsorships inside the video — must be disclosed
- Restricted categories: alcohol, gambling, dating, healthcare, financial — region certification
- Trademark / music licensing — Content ID matches block ads
- Made for Kids (MFK) — personalised ads DISABLED; CTA overlays DISABLED; no remarketing; no companion banner clickable
- Mandatory AI/synthetic content disclosure (effective March 2024, enforced 2025+) — if video uses realistic AI-generated faces/voices/events, disclose at upload via Creator Studio. Failure = disapproval. Does NOT apply to: clearly animated, obvious VFX, AI used only for scripts/captions/ideation, beauty filters.
- Inauthentic content (2025) — ads using cloned voices of real people without consent are disapproved
- Shorts has no 5s skip — viewer can swipe at any moment. Hook must be at frame 1, not second 1.

### Output Format

```markdown
# YouTube Ads — [Product] [Campaign Name]

## Format
[Skippable In-Stream / Non-Skippable / Bumper / In-Feed Discovery / Masthead / Shorts]

## Landing URL
[URL]

## Video Spec
- Duration: [Xs — match format]
- Ratio: [16:9 / 9:16 / 1:1]
- Resolution: 1920×1080 (16:9) or 1080×1920 (9:16)
- Audio: required, sound-on assumed for In-Stream
- Captions: SRT recommended for accessibility + watch-time

## Scene Plan — Skippable In-Stream Example (30s)
| Time | Beat | Visual | Spoken / VO | On-Screen Text |
|------|------|--------|-------------|----------------|
| 0:00–0:01 | Brand reveal + hook | [shot] | "[hook line]" | "[overlay]" |
| 0:01–0:05 | Pay-off promise | [shot] | "[promise]" | "[overlay]" |
| 0:05–0:10 | Value beat | [shot] | "[VO]" | "[overlay]" |
| 0:10–0:22 | Demo / proof | [shot] | "[VO]" | "[overlay]" |
| 0:22–0:30 | CTA | [shot] | "[CTA spoken]" | "[CTA on screen]" |

## Bumper Example (6s)
| Time | Visual | VO | On-Screen |
|------|--------|----|-----------|
| 0:00–0:02 | [visual punchline + brand] | "[one line]" | "[2 words]" |
| 0:02–0:04 | [product/logo] | [silence or single beat] | "[product name]" |
| 0:04–0:06 | [end frame + CTA] | "[CTA verb]" | "[CTA copy]" |

## Companion Text
- Headline (≤15 char In-Stream / ≤25 Masthead / ≤100 In-Feed): "[copy]"
- Description (2 × 35 char): "[line 1]" / "[line 2]"
- Companion banner: 300×60 — [brief]
- CTA button text (≤10 char on overlay): "[copy]"

## In-Feed Discovery (if used)
- Custom thumbnail: 1280×720 — [brief, what's the visual hook]
- Headline (≤100 char): "[copy]"
- Description line 1 (≤35): "[copy]"
- Description line 2 (≤35): "[copy]"

## Variant Set
| # | Angle | Format | First 5s Hook | CTA |
|---|-------|--------|---------------|-----|
| 1 | [angle] | Skippable / Bumper | "[hook]" | [enum + ≤10 char overlay] |
| 2 | ... | ... | ... | ... |

## Pre-Submit Checklist
- [ ] Video uploaded to YouTube (public or unlisted)
- [ ] Format duration respected (Bumper ≤6s, Non-Skip 15/20, Skippable ≥12s)
- [ ] Hook within first 3s, brand reveal by second 1 (Skippable)
- [ ] Pay-off promise before second 5 (skip-decision moment)
- [ ] Captions / SRT for accessibility
- [ ] Companion text within char limits
- [ ] CTA overlay ≤10 char
- [ ] In-Feed thumbnail does not look like an ad
- [ ] No trademark / music licensing issues (run Content ID check)
- [ ] No restricted vertical issues
- [ ] Sound-on intentional — audio adds value, not noise
```

## When NOT to Use This Skill

- Audience targeting (in-market, affinity, custom) → out of scope
- Conversion linkage, Google Ads campaign objective → out of scope
