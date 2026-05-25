---
name: ad-linkedin
title: "LinkedIn Ads Production Spec"
description: "What to produce for a LinkedIn ad — Sponsored Content (single image, video, carousel, document), Message Ads, and Text Ads. Encodes the exact slots (intro text, headline, description), character limits, asset ratios, the CTA enum per format, and the professional-context rules that decide whether B2B audiences engage or scroll past. Use whenever the task is producing LinkedIn ad copy or asset briefs. Strictly platform-specific — does not cover audience filters, matched audiences, or LinkedIn Insight Tag setup."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to LinkedIn Ads."
domains: launch
rules:
  - content(linkedin ads)
  - content(linkedin ad)
  - match(\blinkedin\s+ads?\b)
  - match(\bsponsored\s+content\b)
  - match(\bsponsored\s+(post|update)\b)
  - match(\bmessage\s+ads?\b)
  - match(\binmail\s+ads?\b)
  - match(\blinkedin\s+text\s+ads?\b)
  - semantic(write a linkedin ad)
  - semantic(sponsored content linkedin)
  - semantic(linkedin carousel ad)
---

## Overview

This skill defines exactly what to produce for a LinkedIn ad. It is platform-spec only: the slots LinkedIn exposes, the limits per format, asset ratios, and the CTA enum. It does not cover audience filters, account targeting, or Insight Tag setup.

LinkedIn ads play to a different audience norm than Meta or TikTok: the viewer is logged into a professional identity, expects substance over flash, and treats fluff as a credibility hit. Insight-led, stat-led, or named-customer copy outperforms pitch-led copy on most formats.

## Instructions

### Ad Formats Covered

| Format | What You Produce |
|--------|------------------|
| Sponsored Content — Single Image | Intro text, image, headline, description, CTA |
| Sponsored Content — Video | Intro text, video, headline, CTA |
| Sponsored Content — Carousel | Intro text + 2–10 cards (each with image + headline) + CTA |
| Sponsored Content — Document | Intro text, document (PDF/PPT/DOC) preview + headline + CTA |
| Sponsored Content — Event | Intro text + LinkedIn Event card |
| Message Ads (formerly Sponsored InMail) | Subject line, sender selection, message body, CTA, optional banner |
| Conversation Ads | Subject line, message body, branching CTA buttons (up to 5) |
| Text Ads | Headline, description, small image, destination |
| Dynamic Ads | Headline, description, template-driven (Follower / Spotlight / Content) |
| Lead Gen Form | Form name, intro, form fields, privacy URL, thank-you message |

### Sponsored Content — Single Image / Video / Carousel Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Intro text | 150 chars before "see more" truncation; 600 char hard cap | First 150 chars decide engagement |
| Headline | 70 chars hard cap | Below image — always visible |
| Description | 70 chars hard cap | Renders on LinkedIn Audience Network only — NOT in main feed |
| Destination URL | URL | Landing page |
| CTA button | Enum | See CTA section |
| Image | 1200×627 (1.91:1) recommended; 1:1 (1200×1200) and 1:1.91 vertical (628×1200) also accepted | Max 5MB |
| Video | 16:9, 1:1, or 9:16 (vertical fully supported) | 3s min, 30 min max — sweet spot 15–30s; max 200MB |
| Carousel cards | 2–10 cards | Each card: 1080×1080 (1:1) + 45 char headline |
| Document | PDF, DOC, DOCX, PPT, PPTX | Up to 300 pages OR 1M words, max 100MB. Design ≤10 pages — feed previews only 3–10 pages before see-more truncation |

### Message Ads / Conversation Ads — Slots

| Slot | Message Ads | Conversation Ads | Notes |
|------|-------------|------------------|-------|
| Subject line | 60 chars | 60 chars | Inbox preview — must earn the open |
| Message body | 1,500 chars | 8,000 chars | Conversational tone, NOT a press release |
| Custom footer (legal/T&Cs) | 2,500 chars | 20,000 chars | Optional disclosure block |
| CTA button | Up to 3 buttons | Up to 5 branching buttons per node (typical tree depth 2-4) | 25 chars per button |
| Banner image | 300×250 (desktop only) | Same | Optional — if absent, another advertiser's banner may display in your slot |
| Sender | Must be a personal LinkedIn account | Same | Must be a 1st-degree connection of the campaign manager who explicitly approves; cannot be company page |

⚠️ EU TARGETING BLOCK (CRITICAL): Sponsored Messaging (both Message Ads and Conversation Ads) cannot target EU members since Jan 2022. Mixed EU + non-EU campaigns deliver only to non-EU.

### Text Ads — Slots

| Slot | Limit | Notes |
|------|-------|-------|
| Headline | 25 chars | Hard cap |
| Description | 75 chars | Hard cap |
| Image | 100×100 | Tiny — logo or face only |

### Visual Ratios by Format

| Format | Ratio | Pixel Dimensions |
|--------|-------|------------------|
| Sponsored single image — landscape | 1.91:1 | 1200×627 |
| Sponsored single image — square | 1:1 | 1200×1200 |
| Sponsored video — landscape | 16:9 | 1920×1080 |
| Sponsored video — square | 1:1 | 1080×1080 |
| Sponsored video — vertical | 9:16 | 1080×1920 |
| Carousel card | 1:1 | 1080×1080 |
| Message banner | 300×250 | Right rail on desktop |
| Document | A4 / 16:9 | Per slide / page |

### CTA Button Enum (Current 2026)

Sponsored Content CTAs (campaign-objective driven):

- Apply
- Download
- Get quote (renamed from "View Quote")
- Learn more
- Sign up
- Subscribe
- Register
- Join
- Attend
- Request demo
- Visit website
- View jobs
- Try now
- Order now
- Contact us

CTAs cannot be custom — pick from the enum. Match the verb to the landing action.

### Thought Leader Ads (Launched 2023, mature 2026)

Promote a personal LinkedIn post from any member (employee or external) with their explicit permission.

- No editable headline / intro / description / CTA / URL in Campaign Manager — the post itself IS the creative
- Author edits the post organically; advertiser sponsors as-is
- Author must publish the post BEFORE it can be promoted; cannot retroactively change content
- Author approval is required per campaign in Campaign Manager
- Objectives supported: Brand Awareness, Engagement, Video Views, Website Visits
- Highest CTR format in B2B per 2026 benchmarks (metadata.io, Dreamdata)
- Best fit: CEO/founder personal POV posts, contrarian operator takes, customer-success narratives

### Connected TV (CTV) Ads (Launched 2024, expanded 2026)

Programmatic CTV buying via The Trade Desk, Amazon DSP, or direct via LinkedIn CTV Select (Paramount/NBCUniversal).

- Spec: 15s or 30s creative, 1920×1080 16:9, MP4/MOV, ≤200MB
- No clickable URL or CTA in-stream — audience-buy mechanic, not direct response
- Use for high-value account-based awareness only; pair with retargeting Sponsored Content for response

### Copy Rules — What Wins on LinkedIn

- Lead with a stat, a named customer, or a contrarian insight. "Most B2B founders…" works; "We're excited to announce…" doesn't.
- First-person founder voice outperforms third-person corporate voice for early-stage products.
- Specificity matters more than on consumer platforms — "We cut deploy time from 22 to 4 minutes at [named customer]" beats "Faster deploys."
- Avoid hashtag spam in intro text — 1–3 max, and only if they're real LinkedIn topics.
- Document ads outperform single-image for thought-leadership content (whitepaper, framework, checklist).
- Carousel cards: each card must stand alone. Most viewers swipe 2–3 cards, not all 10.
- Video: caption everything. LinkedIn autoplay is silent, captions decide watch time.

### Subject Line Rules (Message Ads)

- ≤40 chars performs best in the inbox preview
- Personalisation (first name) lifts open rate ~10–15%
- Curiosity > pitch — "Quick question about [their company]'s onboarding" beats "Demo invite"
- Skip ALL CAPS and emojis — both flag as marketing-bait on a professional surface

### Policy Constraints (Common Rejections)

- Misleading employment claims: "Make $X working from home" — auto-disapproval
- Personal attribute targeting in copy: "You, a CTO at a Series B…" — Personal Attributes policy
- Get-rich-quick / crypto / dating — restricted categories
- Trademark in copy without authorisation — disapproval
- Misleading product claims — manual review
- Body parts isolated — disapproval risk
- Bait-and-switch landing pages — account suspension risk

### Output Format

```markdown
# LinkedIn Ads — [Product] [Campaign Name]

## Format
[Sponsored Content / Message Ad / Conversation Ad / Text Ad / Document Ad / Carousel]

## Destination URL
[Landing page URL]

## Intro Text (≤150 char preview, ≤600 hard)
> [Copy — first 150 chars must hook]

Preview slice (first 150 chars): "[show what's visible before see more]"

## Headline (≤70 char)
> [Headline] — [chars]

## Description (≤100 char, if format supports)
> [Description] — [chars]

## CTA Button (from enum)
[Selected CTA]

## Visual Spec
- Format: [Single image / Video / Carousel / Document]
- Ratio: [1.91:1 / 1:1 / 16:9 / 9:16]
- Shot: [concrete scenario]
- Text overlay: "[copy]"
- Video captions: [yes — silent autoplay is the default]

## Carousel Cards (if format = carousel)
| Card | Headline (≤45 char) | Visual Brief |
|------|---------------------|--------------|
| 1 | [headline] | [shot] |
| 2 | ... | ... |

## Message Ad Specific (if format = message)
- Sender (real person): [name + role]
- Subject (≤60 char, ≤40 preferred): "[subject]"
- Body (≤1500 char): "[message]"
- CTA buttons (up to 3, 25 char each): "[CTA 1]" / "[CTA 2]" / "[CTA 3]"

## Variant Set
| # | Angle | Intro Hook | Headline | CTA |
|---|-------|------------|----------|-----|
| 1 | [angle] | [≤150 char] | [≤70] | [enum] |
| 2 | ... | ... | ... | ... |

## Pre-Submit Checklist
- [ ] Intro text hook within first 150 chars
- [ ] Lead is stat / named customer / contrarian insight (not "we're excited")
- [ ] Headline ≤70 chars
- [ ] CTA from enum matches landing action
- [ ] Video captioned for silent autoplay
- [ ] Carousel cards stand alone (don't depend on swipe-to-N)
- [ ] No personal-attribute language ("you, a [role]")
- [ ] No misleading income/employment claims
- [ ] Visual ratio matches format
```

## When NOT to Use This Skill

- Account-Based Marketing list building → out of scope
- Insight Tag pixel setup → out of scope
- Matched audience upload → out of scope
- Sales Navigator outreach → that's organic, not paid
