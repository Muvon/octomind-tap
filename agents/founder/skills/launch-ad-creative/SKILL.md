---
name: launch-ad-creative
title: "Ad Creative: Angles, Copy Variants and Visual Briefs"
description: "Produce paid ad creative: 4-6 distinct angles, slot-fitted copy, visual scenarios and a test plan per platform. Use when writing ads for a product."
license: Apache-2.0
compatibility: "Needs web search for competitor ad research. Any OS."
capabilities: variety
rules:
  - match((?i)\bad\s+(copy|creatives?|angles?|variants?|headlines?|briefs?)\b)
  - match((?i)\b(write|draft|produce|create|brainstorm)\b.{0,40}\b(ads|ad\s+copy|ad\s+creative|ad\s+variants)\b)
  - match((?i)\bvisual\s+(scenarios?|briefs?)\b.{0,30}\bads?\b)
  - match((?i)\b(rsa|sponsored\s+(content|post)|reels|tiktok|meta|linkedin|google|youtube)\b.{0,60}\b(headlines?|hooks?|angles?|scenarios?|variants?|creative|ad\s+copy|primary\s+text)\b)
  - match((?i)\b(a/?b|variant)\b.{0,30}\b(headlines?|primary\s+text|variants?)\b|\bvideo\s+(ad\s+)?scenarios?\b|\bshot[- ]by[- ]shot\b|\bhook\s+(lines?|ideas?)\b)
  - match((?i)\b(problem|curiosity|contrarian|identity|benefit|social\s+proof)\b.{0,40}\bangles?\b)
  - semantic(write ad copy and creative angles for our product)
  - semantic(give me several different angles for ads with headlines and primary text)
  - semantic(write video ad scenarios shot by shot for tiktok and reels)
  - semantic(plan an A/B test of ad variants for each platform)
---

## Overview

Produce complete ad creative packages for indie founders and small teams: platform-correct copy variants, visual scenarios and a creative brief. A product gets 4-6 distinct angles, each tested against the audience the platform delivers, and every line fits its slot exactly. This skill produces the assets a campaign needs; it does not set bids, budgets, targeting or conversion tracking. Each platform has its own slot rules, character limits, asset specs and CTA enum: read them from the matching `ad-<platform>` skill and apply them exactly. Never invent limits from memory.

## Mental model

Think in angles, not features. Delivery systems (Meta Advantage+/Andromeda, Google PMax and AI Max) find the audience through the creative, so variants must differ in angle, persona, format or hook. Near-duplicate wording adds nothing for the system to route.

## Rules

### Process

Fire independent search queries in parallel.

1. Understand the offer: product, audience, primary benefit, current positioning.
2. Confirm platforms: each has its own slot rules and asset specs.
3. Research the space: how competitors run ads in this category on these platforms.
4. Generate 4-6 distinct creative angles before writing any copy.
5. Produce per-platform assets: copy variants and visual scenarios that respect each platform's spec.
6. Validate: every slot under its limit, every visual ratio correct, message match to the landing page.

Research searches:

- "[competitor] ads" plus the public ad libraries: Meta Ad Library, Google Ads Transparency Center, LinkedIn Ad Library, TikTok Creative Center (Top Ads). They render client-side; if search can't read them, ask the user to paste what is running.
- "[product category] ad creative examples"
- "[audience] pain points reddit" and "[audience] objections [product type]"
- "[product category] landing page", for message-match alignment

Memory: before starting, remember(["ad creative", "brand identity", "positioning", "target audience", "competitors", "landing page copy"]). After completing, memorize() winning angles, platform mix, audience insights and control variants.

### Creative angles (pick 4-6 per campaign)

| Angle | Hook pattern | When it works |
|-------|--------------|---------------|
| Problem | "Tired of X?" / "Why does X always Y?" | Audience knows the pain |
| Benefit | "Get X in Y minutes" | Outcome is concrete and quantifiable |
| Curiosity | "The X most [audience] miss" / "What if X..." | Cold audience, top-funnel |
| Social Proof | "X founders switched to Y because..." | Credibility-driven category |
| Contrarian | "Stop doing X. Do Y instead." | Crowded space, need to stand out |
| Identity | "For founders who [trait]" | Audience self-selects on identity |
| Mechanism | "How [novel approach] beats [old way]" | Technical or informed audience |
| Urgency | "[Limited offer / launch / deadline]" | Real scarcity only; fake kills trust |

### Visual scenario rules (all platforms)

- Describe the shot, not the brand. "Founder at desk, late night, half-finished coffee" beats "professional office scene".
- Specify motion for video: what changes between second 0 and second 6.
- Call out the text overlay copy explicitly; visual and overlay copy together carry the ad.
- Specify the aspect ratio per platform every time.
- For static, describe the image and where the text and CTA sit in the frame.
- A video ad needs hook timing: the first 3 seconds decide everything.

### Copy principles (all platforms)

- Match the slot exactly. Never write 60 characters for a 30-character headline, and annotate every line that has a hard limit with its character count.
- One idea per variant. Variants that test two things at once are unusable.
- Concepts, not tweaks: variants differ in angle, persona, format or hook.
- Audience language beats marketing language: pull phrases from how the audience actually talks.
- Specific beats vague: "Saves 4 hours per release" beats "Saves time".
- Literal beats clever in a feed. The ad is skimmed without context, so the control headline states the offer or outcome; wordplay goes in a test variant.
- Comparative and superlative claims ("#1", "faster than X", "cheapest") need proof the landing page shows. The FTC requires a reasonable basis before a claim runs and a comparison must state its basis, and Google and Meta reject improbable or unrealistic outcome claims. Without proof, state the measured fact instead.
- Name the set: "Works with Shopify and WooCommerce", not "works with your store".
- Active verbs in CTAs: "Get the demo" beats "Demo request form". Use only CTAs that exist in the platform's enum.

### Forbidden patterns

- Generic stock-photo briefs ("happy people in office"); they get ignored.
- Copy that doesn't fit the slot.
- The same copy reused across platforms; each platform's audience and norms differ.
- Hype language: "revolutionary", "game-changing", "AI-powered", "-grade" and "-native" compounds without substance.
- Fake scarcity, fake or AI-fabricated testimonials (banned by the FTC's reviews-and-testimonials rule since Oct 2024), misleading benefit claims.
- Visuals that violate platform policy (before/after for restricted verticals, claims of personal attributes). Flag platform policy risks when relevant.

### Ask or assume

- Product given, no platforms: ask which platforms (Google, Meta, LinkedIn, X, TikTok, YouTube, Microsoft Ads (Bing), Reddit). Budget tier matters too: top-of-funnel versus retargeting changes the angle mix.
- Vague request: ask one question, "What platform are we writing for, and is there a landing page already live?"
- Autonomous or non-interactive brief: no questions. Use the platforms and landing page in the brief (default Meta and Google if none named), and list assumptions.

## Output format

```markdown
# Ad Creative: [Product Name]

## Campaign Context
- Product: [What it does, in one line]
- Audience: [Specific persona, not "everyone"]
- Primary benefit: [The one outcome that matters most]
- Landing page: [URL + hero headline for message match]

## Creative Angles (4-6 Selected)
| # | Angle | Hook | Why It Works for This Audience |
|---|-------|------|-------------------------------|
| 1 | [Angle] | [One-line hook] | [Reasoning] |

## [Platform Section: One Per Target Platform]

> Every line below annotated with char count to confirm fit

### Angle 1: [Name]

### Angle 2: [Name]

## Message-Match Check
| Ad Copy Element | Landing Page Element | Match? |
|-----------------|---------------------|--------|
| Primary headline | Landing hero | [Yes / Adjust to: ...] |
| Primary benefit | Hero subheadline | [Yes / Adjust to: ...] |
| CTA verb | Hero CTA | [Yes / Adjust to: ...] |

## Testing Plan
- Control: [Which variant is the safest baseline]
- First test cycle: [2-3 variants to test against control]
- Success metric: [CTR / CPC / CVR, defined before launch]
- Decision rule: [Per the `marketing-experiments` skill: sample size per variant from its table; kill a variant that spends 3x the target cost per conversion with no conversion; scale a variant that beats control by the minimum lift at sample size and is at or under target cost; anything else is no verdict yet]
```

Save deliverables as Markdown in the working directory:

- Full campaign: `ads-[product]-[campaign-name].md`
- Single-platform brief: `ads-[platform]-[product].md`
- Visual scenarios only: `ads-visuals-[product].md`

## Checklist

- [ ] 4-6 distinct angles chosen before any copy was written?
- [ ] Every copy line with a hard limit annotated with its character count and under the limit?
- [ ] Aspect ratio and overlay copy given for every visual scenario?
- [ ] Competitor ad creative checked in the public ad libraries or marked as unavailable?
- [ ] Ad promise matches the landing page headline language?
- [ ] A control, test variants and a success metric defined?
- [ ] Comparative claims backed by proof; no fake scarcity or testimonials; policy risks flagged?
- [ ] No bid, targeting, budget or tracking advice mixed into the creative?

## Composition / References

- `ad-google`, `ad-meta`, `ad-linkedin`, `ad-x`, `ad-tiktok`, `ad-youtube`, `ad-bing` and `ad-reddit` skills hold the per-platform slot rules, limits and CTA enums.
- `ad-frameworks` skill: AIDA, PAS, BAB and 4Us structures for the copy itself.
- `marketing-experiments` skill: sample sizes and stop rules for the testing plan.
- `writing-variety` skill: keeps variants from repeating the same opening.
