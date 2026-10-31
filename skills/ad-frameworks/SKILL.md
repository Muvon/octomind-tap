---
name: ad-frameworks
title: "Ad Frameworks: AIDA, PAS, BAB, 4Us"
description: "Compact playbook of ad copy frameworks (AIDA, PAS, problem-agitation-solution, before-after-bridge, 4Us, FAB) and when to apply each, including a decision guide that matches framework to audience awareness level (Schwartz). Use when structuring the body of an ad: script, body copy, landing-page sections, or any persuasive piece."
license: Apache-2.0
compatibility: "Stack-agnostic."
domains: video
rules:
  - content(advertisement)
  - content(copywriting)
  - match(\bads?\b)
  - match(\bad\s+(copy|creative|script|frame|funnel|account)\b)
  - match(\b(facebook|meta|tiktok|google|youtube|reddit|x|twitter|linkedin)\s+ads?\b)
  - match(\bpaid\s+(social|search|media)\b)
  - match(\bAIDA\b)
  - match(\bPAS\b)
  - match(\bproblem.agitation.solution\b)
  - match(\bbefore.after.bridge\b)
  - session(adcraft)
  - session(ugc)
  - semantic(write a punchier ad for our product)
  - semantic(structure this ad copy better)
  - semantic(make this ad creative more compelling)
  - semantic(which ad framework should we use for this audience)
  - semantic(rewrite this landing page hero in a proven copy formula)
  - semantic(my ad is not converting, what is wrong with the structure)
---

## Overview

Strong ads aren't written from scratch — they're written into a framework that has been pressure-tested across millions of dollars of spend. The framework's job is to make the structure invisible: the viewer feels a story, the writer follows a checklist. This skill gives you the small set of frameworks that actually convert in 2026 short-form video and direct-response copy, plus a rule for which one to pick based on the audience's awareness level (Schwartz's five stages).

## Instructions

### Core Rules

- Pick the framework before writing the script. Trying to pick mid-draft means the writer reverts to default narration.
- Every framework needs an explicit CTA. In Meta/Toluna's analysis of 100 short-form ads (correlational), direct-response ads with a CTA were 1.9× likelier to land in the top 20% for purchase intent (measured). Implicit "the offer is the rest of the video" leaves that on the table.
- Put the product and the proposition on screen early, then show them again. In the same correlational analysis, brand plus message in the first 5 s scored 1.7× for brand ads, and showing the product more than once scored 2.7× for direct-response ads (top 20% for purchase intent). Adding context that supports the main message, such as USPs or features ("Tell your story"), scored 5.3× for direct-response ads (measured; top 20% for purchase intent). TikTok's guidance: put the proposition in the first 3 s (official). Never hold the product reveal for the last third.
- Match framework to audience awareness, not your preference. A cold audience can't follow PAS — they don't yet feel the problem.
- One framework per piece. Mixing AIDA + PAS halfway through makes the piece muddled.
- Specifics, not adjectives. "47% faster" beats "much faster". Numbers, names, time spans.
- Every claim needs proof you could show a regulator. Testimonials and before/after beats must reflect typical results or say what's typical, and paid creators or UGC scripts need a clear disclosure (US FTC Endorsement Guides; FTC reviews rule since Oct 2024 bans fake or bought testimonials). Meta and TikTok also restrict before/after imagery in health, weight-loss, and cosmetic ads.

### Framework Catalog

#### AIDA — Attention, Interest, Desire, Action

Old, durable, works for awareness-stage audiences.

| Beat | Job | Time in 30s ad |
|---|---|---|
| Attention | Hook (see `video-hooks`) | 0–2s |
| Interest | Reveal what's coming, plant curiosity | 2–8s |
| Desire | Show the outcome / transformation | 8–22s |
| Action | Single, specific CTA | 22–30s |

When to use: brand-awareness ads, product launches to a wide audience, top-of-funnel.
Avoid for: retargeting, performance ads with sophisticated audiences.

#### PAS — Problem, Agitation, Solution

The workhorse of direct-response. Works when the audience already has the pain.

| Beat | Job | Time in 30s ad |
|---|---|---|
| Problem + proposition | Name the pain, mirror the frustration, and put the product or proposition on screen | 0–5s |
| Agitation | Twist the knife — show what happens if it's not solved, with the product still on screen | 5–16s |
| Solution | Demo the product already introduced, prove it, show it again in use | 16–26s |
| CTA | One specific action | 26–30s |

When to use: Performance ads, problem-aware to most-aware audiences, B2B.
Avoid for: broad awareness — cold audience tunes out the problem.

#### BAB — Before, After, Bridge

Transformation-driven. Strong for D2C, fitness, finance, productivity.

| Beat | Job |
|---|---|
| Before | Show life with the problem (specific, sensory) |
| After | Show life without it (specific, sensory) |
| Bridge | The product / system that gets you there |

When to use: transformation products, weight-loss / finance / fitness / productivity, lifestyle.
Avoid for: pure information products (no transformation arc).

#### 4Us — Useful, Urgent, Unique, Ultra-specific

A copy-checking heuristic, not a structure. Apply to every claim in the piece.

| U | Question |
|---|---|
| Useful | Does this help the viewer? |
| Urgent | Why must they act now? |
| Unique | Why this product, not the 10 others? |
| Ultra-specific | Specifics over generics? |

A line that doesn't pass at least 2 of 4 should be rewritten.

#### FAB — Features, Advantages, Benefits

Translation engine. Use to convert a feature list into copy.

| Layer | Question | Example |
|---|---|---|
| Feature | What it has | "M3 Pro chip with 12-core CPU" |
| Advantage | What it does | "Compiles 2x faster than M2" |
| Benefit | What it means for the user | "Ship code while the demo is still loading" |

Rule: the script lives at the Benefit layer. F and A are research notes.

#### Hook → Story → Offer (HSO)

The dominant short-form social structure.

| Beat | Job |
|---|---|
| Hook | First 1.5s (see `video-hooks`) |
| Story | One specific narrative — first-person, real or composite. ~70% of total runtime. Product visible from the first 3–5 s and shown again in use. |
| Offer | Offer details + CTA, ~20% of runtime. The product is already on screen; this beat names the deal. |

When to use: TikTok / Reels / Shorts UGC and creator-style ads. Default for short-form.
Avoid for: B2B explainer, anything where a story would feel forced.

### Audience Awareness — pick framework by stage (Schwartz)

| Awareness | Framework | Reason |
|---|---|---|
| Unaware (no problem felt) | HSO with curiosity hook | Cold audience won't sit through PAS |
| Problem-aware | PAS or BAB | They feel the pain, agitate it |
| Solution-aware | BAB or AIDA | They know solutions exist, differentiate |
| Product-aware | FAB-driven AIDA, with comparison | They know your category, why YOU |
| Most-aware (your fans) | Direct offer — skip framework, lead with deal | Don't sell to people who already bought |

### Workflow

1. Identify audience awareness stage from the brief (or ask — don't guess).
2. Pick the framework from the table above.
3. Pre-write the offer before the body — ensures the body builds toward something specific.
4. Draft each beat, time-boxed to the ad length.
5. Run every claim through the 4Us check.
6. Read aloud at 1.5x speed. If it sounds AI / scripted at speed, rewrite for natural cadence.
7. Show the script with timestamps, not just lines. Time is the unit, not paragraphs.
8. Check the product and proposition are on screen in the first 3–5 s and shown more than once, and that a CTA is present.

### Decision Guide

| Situation | Framework |
|---|---|
| TikTok / Reels organic UGC | HSO |
| TikTok / Reels paid ad, problem-aware audience | PAS |
| Meta paid ad, transformation product | BAB |
| YouTube pre-roll (5–15s) | HSO with hard cut at 3s + visible skip-friendly first beat |
| YouTube pre-roll (un-skippable, 15s) | PAS or AIDA, CTA in last 3s |
| Long-form explainer (60–180s) | AIDA with FAB-loaded D-beat |
| Landing page hero | Hook + 4Us-checked one-liner + CTA |
| Cold email | PAS, 75 words max |
| Retargeting / cart-abandon | Direct offer, no framework, lead with deal |

## Examples

### Example 1: PAS for a B2B SaaS TikTok ad (30s)

Product: An on-call alerting tool. Audience: backend engineers, problem-aware (their team uses PagerDuty + duct tape).

```
0–3  P  Hook: "Your on-call rotation is broken. [Product] fixes the noise."
       (visual: phone going off at 3am, hand smacking the snooze, the product's alert card on screen)

3–8  P  "67% of pages last quarter were noise — the kind that wakes you up
       for a flapping check that auto-resolves before you log in."
       (visual: fast-cut alerts spamming a dashboard)

8–18 A  "Every false page costs $8 of engineer time and the next real one
       hits a tired brain. The third Tuesday in a row, you stop trusting
       the alerts entirely. That's when the real outage gets missed."
       (visual: someone dismissing alerts on a phone, then a prod outage)

18–26 S "Quietly groups duplicate alerts, runs a 30-second auto-heal, and
       only pages a human if the system is still on fire after that."
       (visual: dashboard going from red waterfall to one calm card)

26–30 CTA "10 days free. Set it up in 4 minutes. Link in bio."
       (visual: founder deadpan to camera)
```

### Example 2: HSO for a D2C creator UGC Reel (20s)

Product: A teeth-whitening pen. Audience: cold, scrolling.

```
0–1.5  Hook: "I tested 11 whitening pens for my wedding. Only one didn't
              wreck my enamel."
              (visual: line-up of pens, hand pushing 10 off-screen, the winner stays in frame)

1.5–14 Story: "I'm 4 weeks out, panicking, and Sephora is full of strips
              that bleed at the gums. This one [show product] — bamboo
              applicator, no peroxide, results in 6 days. My dentist
              actually said 'whatever you're doing, keep doing it.'"
              (visual: morning routine, before/after, dentist text screenshot)

14–20  Offer: "20% off through the link, free returns if it doesn't work
              for you in 14 days."
              (visual: product on bathroom counter, hand pulling phone toward camera)
```

### Example 3: AIDA for a YouTube pre-roll (15s, un-skippable)

```
0–2  A  "Stop scrolling for 12 seconds. This will pay for itself."
2–6  I  "Most freelancers under-invoice by 23% and don't know it."
6–11 D  "We pulled the data from 4,000 freelance invoices. The fix is one
        rule. [show result]"
11–15 A "Free calculator at link. 60 seconds, no signup."
```

## Checklist

- [ ] Framework picked from the audience awareness stage before drafting; one framework per piece.
- [ ] Product and proposition on screen in the first 3–5 s, shown more than once, with USPs or features supporting the main message.
- [ ] Explicit single CTA; no claim without proof; every line through the 4Us.

## References

- Eugene Schwartz, Breakthrough Advertising (1966) — the awareness-level model.
- David Ogilvy, Ogilvy on Advertising — the canonical book on long-form direct-response.
- [Meta Ads Library](https://www.facebook.com/ads/library/) — to study current top-spending ads.
- [TikTok Top Ads](https://ads.tiktok.com/business/creativecenter/topads) — by vertical and region.
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices) — proposition in the first 3 s (official, 2025-06).
- [Meta: Reels creative strategies](https://www.facebook.com/business/news/reels-creative-strategies) — Meta x Toluna analysis of 100 short-form video ads, correlational: CTA 1.9× (direct-response), brand plus message in first 5 s 1.7× (brand ads), product shown more than once 2.7× (direct-response, top 20% purchase intent), "Tell your story" (USPs or features supporting the main message) 5.3× (direct-response) (official, measured, 2025-12-02).
- [ppc.land write-up of the Meta/Toluna study](https://ppc.land/meta-and-toluna-study-finds-emojis-lift-reels-purchase-intent-2-5x/) — secondary coverage (reported, 2026-05-18).
