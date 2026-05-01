---
name: video-hooks
title: "Video Hooks — First-1.5s Retention Patterns"
description: "Catalog of proven first-1.5-second hook patterns for short-form video (TikTok, Reels, Shorts). Use whenever drafting an ad or social-video script — the hook is what decides whether the rest of the clip ever gets watched. Encodes pattern types (pattern-interrupt, problem-aware, curiosity-gap, contrarian, on-screen-text, motion-cut, voice-led), the rules for each, and what to NEVER open with."
license: Apache-2.0
compatibility: "Stack-agnostic. Pairs with skills/video-spec-sheet for platform constraints and skills/ad-frameworks for body structure."
domains: video content launch
rules:
  - session(video)
  - session(adcraft)
  - content(hook)
  - content(short-form)
  - content(reels)
  - content(shorts)
  - content(tiktok)
  - match(\bopens?\s+with\b)
  - match(\bfirst\s+\d+\s*(seconds|s)\b)
---

# Video Hooks — First-1.5s Retention Patterns

## Overview

Short-form video lives or dies in the first 1.5 seconds. The hook is the only sentence in the script that matters more than the offer — if it doesn't earn the next breath, the user swipes and the rest of the work is wasted. This skill encodes the small number of hook patterns that *actually* convert on TikTok, Reels, and Shorts in 2025–2026, the rules each pattern follows, and the dead opens to avoid.

Pair with `video-spec-sheet` (platform constraints) and `ad-frameworks` (body structure once the hook lands).

---

## Instructions

### Core Rules

- **The hook is the first 1.5s of video, not the first sentence of the script.** It is *visual + audible + on-screen text* together. Treat all three as the hook.
- **Earn the next second**, not the next minute. Each beat (1.5s, 3s, 5s) needs its own retention reason.
- **Never open with the brand.** Brand goes in the resolution, not the open. Brand-first opens have ~30–40% lower 3s retention.
- **Never open with "Hi guys" / "In this video" / "Today I'll show you".** These are skip triggers — the algorithm has trained users to expect filler after them.
- **Show motion in frame 1.** A still opener loses ~20% of viewers vs. a moving opener (camera shake, zoom, subject motion, or quick cut).
- **Caption visible by frame 5.** ~85% of feed scrolls are sound-off — the hook must read silently.
- **One claim per hook.** Two ideas = no idea.

### Hook Pattern Catalog

| Pattern | When to use | Template |
|---|---|---|
| Pattern-Interrupt | Cold cold audience, low awareness | `[surprising visual] + "Wait — [absurd claim]"` |
| Contrarian | Audience has heard the cliché | `"Stop [common advice]. Here's why it actually [opposite outcome]."` |
| Problem-Aware | Audience already feels the pain | `"If your [tool/process] still [pain point], you're [losing X]."` |
| Curiosity-Gap | Educational / how-to | `"I tested [N] [things] for [duration]. Only [small N] [outcome]."` |
| Stat Punch | B2B / data-driven | `"[Big number] of [audience] [do thing wrong]. Here's the fix."` |
| Identity Bait | Niche audience | `"You're a [specific identity] if [oddly specific behavior]."` |
| Listicle Promise | Information-dense | `"[N] [things] [audience] should [verb] before [year/event]."` |
| Direct Address | Existing followers / retargeting | `"This is for the [specific user] who [specific pain]."` |
| Negative Framing | Performance ads (Meta/TikTok) | `"Don't [common action] until you [see this/read this]."` |
| Confession | UGC / authentic | `"I'm not supposed to say this, but [insider truth]."` |
| Demo-Cold-Open | Product-led | Show the result *first*, no setup, then reverse-engineer the how. |

### Visual Hook Devices (stack on top of script)

- **Hard cut at 0:00.5** — first frame is mid-action, not establishing.
- **On-screen text larger than usual** (font size 80–100pt for 1080×1920).
- **Pattern-interrupt object** — something visually unexpected in frame 1 (a banana, a hand, a face mid-expression).
- **Speed ramp** — slow-mo for 0.3s then snap to real-time.
- **Camera move** — zoom-in or push-in at 0.0–0.5s; static cameras lose attention.
- **Caption animation** — words appearing in time with speech (auto-caption-style); higher retention than burned-flat text.

### Workflow

1. **Read the brief** — product, audience, awareness level (cold / warm / retargeting).
2. **Pick 3 patterns from the catalog** that fit the audience and awareness level.
3. **Write 3 hook variants** — one per pattern. Each ≤ 12 words on screen, ≤ 8 words spoken.
4. **For each variant, specify**: visual (frame 1 description), on-screen text, voiceover line, motion device.
5. **Score each on**: pattern-interrupt strength (1–5), claim specificity (1–5), caption readability sound-off (1–5).
6. **Pick the top scorer** — but ship at least 2 variants for A/B testing.

### Decision Guide

| Scenario | Hook pattern |
|---|---|
| Cold audience, fully unaware of the problem | Pattern-Interrupt or Confession |
| Audience knows the problem but not the solution | Problem-Aware or Stat Punch |
| Audience knows the solution category, comparing | Contrarian or Demo-Cold-Open |
| Audience is already a fan / past visitor | Direct Address or Identity Bait |
| Performance ad on TikTok / Meta | Negative Framing or Pattern-Interrupt |
| Educational / informational content | Curiosity-Gap or Listicle Promise |

---

## Examples

### Example 1: SaaS dev tool, cold TikTok audience

**Brief:** Promote a CLI tool that auto-generates database migrations.
**Audience:** Backend devs, mostly cold.
**Pattern picks:** Pattern-Interrupt, Contrarian, Stat Punch.

**Variant A — Pattern-Interrupt**
- Frame 1: Terminal mid-typing, a migration error fills the screen in red.
- On-screen text: `your migrations are lying to you`
- Voice: `Your migrations are lying to you.`
- Motion: hard zoom-in on the error.

**Variant B — Contrarian**
- Frame 1: Hand crossing out the words "Write SQL by hand" on whiteboard.
- On-screen text: `STOP writing migrations by hand`
- Voice: `Stop writing migrations by hand. There's a better way.`
- Motion: quick whip-pan to the laptop screen.

**Variant C — Stat Punch**
- Frame 1: Big number `73%` filling the screen.
- On-screen text: `73% of prod outages start in a migration`
- Voice: `Seventy-three percent of prod outages start in a migration. Here's how to stop being one of them.`
- Motion: number scales up from 0 to 73 in 0.5s.

**Pick:** B for cold dev audience — Contrarian + clear visual, no claim that needs sourcing.

### Example 2: D2C skincare, retargeting audience

**Brief:** Cart-abandoners who viewed the SKU but didn't buy.
**Pattern picks:** Direct Address, Confession.

**Variant A — Direct Address**
- Frame 1: Mid-shot of a person looking straight to camera, finger pointing.
- On-screen text: `you ← yes, you who left this in your cart`
- Voice: `You — yes, you, who left this in your cart yesterday.`
- Motion: subject leans into camera.

**Variant B — Confession**
- Frame 1: Founder unboxing a return.
- On-screen text: `nobody told me this would happen with [product]`
- Voice: `Nobody told me this would happen the second week of using it.`
- Motion: hand reveals the product mid-frame.

---

## Hooks That Are Banned

These openers measurably tank retention — never use them:

- "Hi everyone / Hi guys / What's up"
- "In this video / Today I'm going to / Let me show you"
- "Welcome back to my channel"
- Logo on screen alone
- Brand name as the first spoken word
- Any sentence that starts with "So..."
- A static product shot with no motion
- Music-only opener with no visual or text claim

---

## References

- [TikTok Creative Center — Hook patterns](https://ads.tiktok.com/business/creativecenter/) — actual top-performing ad teardowns by vertical.
- [Meta Ads Library](https://www.facebook.com/ads/library/) — search competitors and study their first 1.5s.
