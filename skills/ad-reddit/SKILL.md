---
name: ad-reddit
title: "Reddit Ads Production Spec"
description: "What to produce for a Reddit ad — Promoted Posts (image, video, link, text), Free-form Ads (the rich-content 2024+ flagship), Carousel Ads, Conversation Placement Ads, Promoted User Posts (boost an existing organic), Product Catalog Ads, and AMA Ads. Encodes the exact slots, char limits, asset ratios, CTA enum, AND the Reddit-specific creative rules — native voice, per-subreddit variants, real-artifact imagery, comment engagement plan — that decide whether the ad performs or gets downvoted into oblivion. Use whenever the task is producing Reddit ad copy or assets. Strictly platform-specific — does not cover subreddit targeting strategy or Reddit Pixel setup."
license: Apache-2.0
compatibility: "Octomind launch agents. Platform-specific to Reddit Ads."
domains: launch
rules:
  - content(reddit ads)
  - content(reddit ad)
  - content(promoted post reddit)
  - match(\breddit\s+ads?\b)
  - match(\bsubreddit\s+ads?\b)
  - match(\bfree.form\s+ad\b)
  - match(\bpromoted\s+user\s+post\b)
  - match(\bconversation\s+placement\b)
  - semantic(write a reddit ad)
  - semantic(produce a reddit free-form ad)
  - semantic(reddit promoted post copy)
---

## Overview

This skill defines exactly what to produce for a Reddit ad. It is platform-spec only: the slots Reddit exposes per format, the asset specs, the CTA enum, AND — critically — the native-voice and subreddit-fit rules that decide whether the ad performs or gets reported/downvoted.

Reddit is the platform where polished ad creative DIES. The audience is hostile to obvious advertising. The ads that work look like organic Reddit posts: first-person voice, real screenshots, plain headlines, honest reasoning, founder/maker accounts, comments enabled and actively answered.

## Instructions

### Ad Formats Covered

| Format | Purpose | What You Produce |
|--------|---------|------------------|
| Promoted Post — Image | Single static image post | Username, headline, image, CTA, URL |
| Promoted Post — Video | Single video post (in-feed + conversation) | Username, headline, video, thumbnail, CTA, URL |
| Promoted Post — Link | Card with link preview | Username, headline, URL/link card, CTA |
| Promoted Post — Text | Self-text post | Username, headline, body, CTA, URL |
| Free-form Ads (2023+ flagship) | Rich multi-asset native post | Username, headline, body (up to 40k chars, rich text), up to 20 inline images/GIFs/videos, CTA, URL |
| Carousel Ads | Swipeable cards in feed or conversation | 2–6 cards, each: image, headline, caption, URL |
| Conversation Placement Ads | Slot between OP and comments | Headline, thumbnail (400×300 strongly recommended), CTA, URL |
| Promoted User Posts | Boost an existing organic post (Reddit's Spark Ad equivalent) | Inherits original post slots; adds CTA + destination URL; owner permission required |
| Product Ads (Catalog) | Shoppable, dynamic from feed | Catalog product fields, 1:1 image, dynamic price/title |
| AMA Ads | Promoted AMA event | Headline, body, scheduling metadata |
| Premium — Reddit Takeover | 24h dominance Home/Popular/Search | Multi-placement managed |
| Premium — Category Takeover | 24h 100% SOV in a category | Managed creative bundle |
| Premium — First View | First in-feed impression on Home/Popular | Image or video |
| Interactive Ads | Games, polls, countdowns, branded challenges | Managed |
| Max Campaigns | AI-optimized mix across creative variants | Accepts all standard creative inputs |

### Text Field Limits

| Field | Hard Cap | Practical Target | Notes |
|-------|----------|------------------|-------|
| Headline (post title) | 300 chars | ≤80 chars | Mobile feed truncates beyond ~80; ≤60 for conversation placement |
| Body (Free-form, text posts) | 40,000 chars | 300–1,500 chars | Lead with TL;DR if >300 |
| Caption (per carousel card or inline media) | 50 chars | — | Hard cap |
| Username (display) | n/a | — | Brand handle OR persona; never zero-karma throwaway |
| Destination URL | standard | — | First card's URL used for conversation placement carousel |

### Image Asset Specs

| Asset | Ratios | Recommended Dims | Min Width | Max File |
|-------|--------|------------------|-----------|----------|
| Feed image | 1:1 / 4:5 / 1.91:1 / 16:9 | 1080×1080 / 1080×1350 / 1200×628 / 1920×1080 | 1000 px | 20 MB |
| Vertical (full-screen video thumb) | 9:16 | 1080×1920 | 1080 px | 20 MB |
| Conversation placement thumbnail | n/a | 400×300 strongly recommended | — | 20 MB |
| Formats | JPG, PNG, GIF | — | — | GIF max 3 MB |

Best mobile feed performance: 1:1 (1080×1080) or 4:5 (1080×1350). Stock photos die — use real product UI, screenshots, or hand-drawn diagrams.

### Video Asset Specs

| Spec | Value | Notes |
|------|-------|-------|
| Format | MP4, MOV | H.264, AAC |
| File size | ≤1 GB hard, <512 MB recommended | |
| Frame rate | 30 fps | |
| Duration | 5s min, 15 min max | Sweet spot 15–30s; <60s for completion |
| Aspect ratios | 16:9, 1:1, 4:5, 9:16 | 1:1 and 4:5 dominate mobile feed |
| Min resolution | 720p | 1080p recommended |
| Sound | Off by default | Captions / burned-in subtitles mandatory in practice |
| Thumbnail | Required | Image ad specs |

### Free-form Ads — Rich Body

- Up to 20 inline images/GIFs/videos
- Supports headings, bold, italic, line breaks, inline links
- Up to 40k char body; treat anything past ~1,500 as long-form
- TL;DR at top mandatory for anything >300 chars

### Carousel — Spec

- 2–6 cards
- Per-card sizes: 1200×1500 (4:5), 1440×1080 (4:3), 1920×1080 (16:9), 1200×1200 (1:1)
- Headline per card ≤300 chars (≤80 recommended)
- Caption per card ≤50 chars
- Each card has its own destination URL in feed
- Conversation placement carousel: only the FIRST card's URL is used for the whole unit

### CTA Button Enum

Fixed dropdown — no custom copy allowed:

- Apply Now
- Book Now
- Contact Us
- Download
- Get a Quote
- Get Showtimes
- Install Now
- Learn More
- Order Now
- Play Now
- Read More
- See Menu
- Shop Now
- Sign Up
- Subscribe
- View More
- Visit Site
- Watch More
- Watch Now
- No button (omit CTA — often the best choice for Free-form ads in storytelling format)

Pick the CTA matching the actual landing-page action. Mismatched CTA is a top reason for low Reddit CTR.

## Reddit-Specific Creative Rules (Native Voice + Subreddit Fit)

These are not stylistic preferences. They decide whether the ad performs or dies.

1. Native voice beats polished ad copy. Lowercase headlines acceptable, conversational, slightly self-deprecating. Avoid superlatives ("amazing," "revolutionary," "best-in-class"), buzzwords, exclamation points.

2. First-person, believable persona. "I built this" / "we ran into this problem so we…" outperforms corporate "we are excited to announce." Use a founder/maker/employee account where possible; the verified business account is fine for product showcases but worse for storytelling.

3. Subreddit fit > single creative. Same product → different creative per subreddit cluster. A dev tool ad for r/programming uses different references, examples, and tone than the same product in r/sysadmin or r/startups. Produce one creative variant per subreddit or tight cluster as the default.

4. No clickbait, no hype. Reddit's hostile to teaser headlines. Plain, descriptive, specific. Numbers > adjectives.

5. Tell, don't sell. Long-form Free-form posts with honest reasoning ("here's what didn't work, here's what we changed") outperform short polished ads in most B2B / niche DTC verticals.

6. Engage in the comments. Top-performing ads have the brand actively replying in the thread within the first hour, from the same posting account. Comments are ON by default — leave them on unless legal blocks it. Disabling comments is a credibility killer.

7. Real artifacts over stock photos. Screenshots, terminal output, real product UI, hand-drawn diagrams, native Reddit-style memes — all outperform stock or studio photography.

8. TL;DR at top for any body >300 chars. Reddit convention; ignoring it tanks engagement.

9. Disclose when appropriate. "I work at X" or "(I'm the founder)" in the first line builds trust faster than hiding it; the "Promoted" tag already telegraphs ad status.

10. Username matters. Brand handle for product launches; persona for storytelling; NEVER a fresh zero-karma throwaway — it reads as astroturfing and gets reported.

## Policy + Restricted Categories (2025–2026)

Post-IPO (March 2024) Reddit tightened enforcement.

Prohibited entirely: illegal drugs, weapons, ammunition, exploitative content, fraud / get-rich-quick, deceptive claims, deepfakes / manipulated media of real people, hate speech, political ads targeting elections (most regions; case-by-case allowlist).

Restricted (allowed with gating, certification, or geo-limits):

- Gambling & sports betting — license verification, geo-restricted
- Alcohol — geo + age-gated; no under-21 (US) / local age elsewhere
- Cannabis / CBD — extremely limited; CBD-only in some US states with certification; THC generally blocked
- Cryptocurrency & financial products — regulatory disclosures required, no unregistered securities, no "guaranteed returns"
- Healthcare / pharma / supplements — Rx restricted; OTC needs claims substantiation; no before/after weight-loss imagery
- Dating — mainstream only; no hookup/adult
- Adult content — PROHIBITED in ads regardless of NSFW community context
- Political / issue ads — managed via Reddit's political ads policy with disclosure; many jurisdictions blocked

IP / Trademark: enforced via takedown; do not use competitors' marks, do not impersonate other brands or Reddit itself.

2025–2026 enforcement trends:
- Tighter creative review on AI-generated imagery; disclosure encouraged
- Faster takedown of ads with disabled comments + manipulated screenshots
- Heavier scrutiny on crypto, financial coaching, and "AI tool" ads for misleading claims

## Output Format

```markdown
# Reddit Ads — [Product] [Campaign Name]

## Target Subreddits / Clusters
[List — REQUIRED, since one variant per cluster is the rule]

## Destination URL
[URL]

## Per-Subreddit Variants

### Variant 1: r/[subreddit]
- **Account / Persona**: [brand handle OR persona — match to subreddit tone]
- **Format**: [Promoted Image / Video / Free-form / Carousel / Conversation Placement / etc.]
- **Headline** (≤80 char recommended, ≤60 for conversation placement):
  > "[headline]" — [chars]
- **Body** (Free-form only — TL;DR at top if >300 char):
  > TL;DR: [one-line summary]
  >
  > [body]
- **Media spec**:
  - Image: [ratio + shot description, real artifact preferred]
  - OR Video: [ratio + duration + caption track + thumbnail spec]
  - Conversation placement thumbnail: 400×300 — [shot]
- **CTA**: [from enum, or "No button" for storytelling Free-form]
- **Carousel cards** (if format = carousel):
  | Card | Image | Headline | Caption (≤50) | URL |
  |------|-------|----------|---------------|-----|
  | 1 | [shot] | [≤80] | [≤50] | [URL] |
  | ... | ... | ... | ... | ... |
- **Comment Engagement Plan**:
  - Who responds: [name / handle]
  - Within: [first hour ideal]
  - Tone: [match the subreddit]
- **Disclosure** (if applicable): "[I work at X / I'm the founder]" in first line

### Variant 2: r/[subreddit]
[...]

## Pre-Submit Checklist
- [ ] One variant per subreddit cluster (no single-creative blasting)
- [ ] Native voice — no superlatives, no buzzwords, no "we're excited to announce"
- [ ] First-person framing where storytelling fits the subreddit
- [ ] Headline ≤80 char (≤60 for conversation placement)
- [ ] TL;DR at top if body >300 char
- [ ] Real artifact image, not stock photo
- [ ] Captions burned in on all video
- [ ] CTA from enum (or "No button" for storytelling)
- [ ] Username matches post type (brand for showcase, persona for story)
- [ ] Comments left enabled
- [ ] Reply plan in place (within first hour)
- [ ] No restricted-vertical content without certification
- [ ] No competitor trademark / impersonation
- [ ] No AI-generated imagery without disclosure
```

## Realistic 2026 Scenarios

A. B2B dev tool, Free-form, r/programming + r/devops: Account = founder persona (`u/alex_builds`). Format = Free-form. Headline: "we built a CLI for X because Y kept breaking in CI." Body: TL;DR (2 lines), problem context (3–4 short paragraphs), inline terminal screenshot, link to repo, brief "I'm the maker, AMA." CTA: `Learn More` or `No button`. Different variant for r/devops emphasizing Kubernetes pain.

B. Indie SaaS launch, Promoted Post (image), niche subreddits: Account = brand handle. Format = image post, 1:1, screenshot of actual product UI (no stock). Headline: "Launched our [tool] today — replaces [X] for [Y use case]." Body: 2–3 sentences, honest "we built this because…" framing, pricing transparency. CTA: `Sign Up`. Comments enabled; founder responds within the first hour.

C. DTC niche product, Conversation Placement Ads, topical subreddits: Account = brand handle. Format = conversation placement with 400×300 thumbnail. Headline ≤60 char. Thumbnail is a real product photo on a plain background (NOT lifestyle stock). CTA: `Shop Now`. Variant per subreddit cluster (e.g., r/CampingGear vs r/Ultralight — different language and feature emphasis).

D. Mobile app install, Video Ad, sound-off captioned: Format = 9:16 or 4:5 video, 15–20s. First 3s shows a relatable problem; remainder shows the in-app solution. Burned-in captions throughout. Headline plain ("an app for tracking X"). CTA: `Install Now`. Multiple variants per audience cluster.

E. Promoted User Post boosting existing organic traction: A genuine user post (or brand's own organic post) that already has 500+ upvotes and active comments. Boost via Promoted User Post, add `Visit Site` CTA. Do NOT alter the post body. Brand replies in-thread immediately.

## When NOT to Use This Skill

- Subreddit targeting strategy → out of scope (audience-level decision)
- Reddit Pixel events / conversion tracking → out of scope
- Organic Reddit growth tactics → not paid
