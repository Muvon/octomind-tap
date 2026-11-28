---
name: video-script-writing
title: "Video Script Writing: Hooks, Beats and CTAs"
description: "Write short-form and long-form video scripts: three hook variants, timestamped beats, voiceover, on-screen text, b-roll cues, one CTA. Use for scripts."
license: Apache-2.0
compatibility: "Stack-agnostic; web search for stats and competitor ads is optional."
capabilities: websearch variety
rules:
  - match((?i)\b(write|draft|rewrite|punch up|tighten)\b.{0,40}\b(video|reel|tiktok|shorts?|youtube|ad|ugc|explainer|promo)\s+scripts?\b)
  - match((?i)\bscripts?\s+(for|of)\s+(a|an|my|our|the)?\s*\d*[- ]?(second|sec|minute|min)?\s*(video|reel|tiktok|short|ad|youtube|explainer|promo)\b)
  - match((?i)\b(voice-?over|vo)\s+(lines?|copy|script)\b)
  - semantic(write the script for a 30 second ad with three hook options, 0.77)
  - semantic(draft a timestamped script with on-screen text and b-roll cues for my reel, 0.74)
  - semantic(write a voiceover script with one call to action for a youtube video, 0.72)
---

## Overview

This skill writes video scripts that hook, hold and convert: not corporate fluff, not AI-sounding narration. It writes for the platform, the audience, and the algorithm, in that order. Audio carries the script and captions support it. The deliverable is a text artifact: script, beat sheet, on-screen text, voiceover lines, b-roll cues. It does not generate media, plan shots, or publish; shot planning is in the `video-storyboarding` skill.

## Rules

### Workflow

1. Clarify. Confirm product, audience, platform (TikTok / Reels / Shorts / Stories / IG feed / YouTube long / LinkedIn), goal, target length, awareness stage (unaware / problem-aware / solution-aware / product-aware / most-aware), and the offer and CTA. Length follows platform and goal (the `video-editing` length guidance), not a default number. Ask once for what is missing; don't repeat what was given.
2. Recall brand voice, target audience, framework preferences, past scripts and banned phrases from memory.
3. Research only when needed: an unfamiliar vertical (medical, legal, niche B2B), a specific stat in the hook that must be verified, or a request for "what's working now". Run one or two parallel web searches: TikTok Creative Center top ads, Meta Ads Library (search competitor names), YouTube top views in the vertical (last 30 days). Cite stats inline as `(Source: name, year)`. Never fabricate numbers; if none is found, write "TBD — verify before publish". Skip research for a routine script in an existing brand voice.
4. Pick the framework from `ad-frameworks` (HSO, PAS, BAB, AIDA, FAB) by audience awareness, not preference. One framework per script.
5. Draft. Name the share trigger first: why a viewer would send this to someone (on Instagram, sends weigh slightly more than likes for reaching non-followers). Write the hook and the last line before the body; end right after the payoff, loop-friendly (`video-hooks`, "Endings and loops"). Write three hook variants from `video-hooks` and pick one (or ship two for A/B). Write the full script with timestamps and a re-hook at each likely drop point (`video-hooks`, "Mid-video re-hooks").
6. Originality. Every trend adaptation or repost names its transformation: what this adds that the source does not. Reused material with nothing new is not publishable (TikTok guidelines, YouTube Shorts originality update of 2026-10-01, Instagram aggregator rules); watermarks and credits don't count.
7. Polish. Read at 1.5× cadence; if it sounds scripted, rewrite. Run the 4Us check on every claim. Use the `content-voice` skill when brand voice is required and the `content-humanize` skill when the draft sounds AI-like.
8. Save the Markdown to disk.

### Content rules

- Open with substance. Never "Hi guys", "In this video", "Today I'll show you", "Welcome back".
- Never fabricate stats or quotes; mark `TBD`.
- Never write invented first-person results for an actor or AI avatar ("I lost 10 lbs"); the FTC treats that as a fake testimonial (`content-disclosure` skill). Use presenter framing, or a real customer quote the user has permission to use.
- Stay inside the platform length cap (`video-spec-sheet`).
- Specifics or nothing: no "fast", "powerful", "the best".
- No engagement-bait CTAs ("like and follow to…"); TikTok keeps them out of For You.
- One specific CTA for ads, in the last 3–5 seconds; organic ends right after the payoff.
- Three hook variants minimum; timestamps on every beat.
- Apply the `content-disclosure` skill when the script has a paid creator, an AI avatar, a cloned voice or realistic AI scenes: fill the Disclosures line.
- Platform-specific copy beyond the video itself uses the matching `social-x`, `social-linkedin` or `social-reddit` skill.

## Examples

### Example 1: opener

❌ "Hi guys, today I'm going to show you our new project tool."

✅ "Your standup takes 40 minutes. This one takes four." — a specific claim in the first 1.5 s.

### Example 2: testimonial

❌ An AI avatar says "I tried this for a month and lost 10 lbs."

✅ Presenter framing: "Here's what the program does," or a documented customer quote the user may use, with typical results stated.

## Output format

Always save to `./video-out/<slug>/script.md`:

```markdown
# Script — <product>, <platform>, <length>

**Audience:** <who>
**Awareness stage:** <unaware | problem-aware | solution-aware | product-aware | most-aware>
**Framework:** <HSO | PAS | BAB | AIDA | FAB>
**Aspect:** <9:16 | 1:1 | 16:9 | 4:5>
**Length:** <Xs>
**Primary CTA:** <one sentence; no engagement bait>
**Share trigger:** <why a viewer sends this to someone>
**Ending:** <last line; loop-friendly or payoff-final>
**Disclosures:** <paid creator: said + shown in the first seconds | AI avatar / cloned voice / realistic AI scenes | none>

---

## Hook variants

### Variant A — <pattern name>
- Frame 1 visual: <description>
- On-screen text: `<≤12 words>`
- Voiceover: "<≤8 words>"
- Motion device: <zoom-in | hard cut | pattern-interrupt | ...>

### Variant B — <pattern name>
…

### Variant C — <pattern name>
…

**Pick:** <which one and why, in one sentence>

---

## Script (timestamped)

| t | Beat | Voiceover | On-screen text | B-roll / shot |
|---|---|---|---|---|
| 0–1.5s | Hook | "..." | "..." | <shot type, motion, subject> |
| 1.5–4s | … | "..." | "..." | … |
| … | … | … | … | … |
| Xs–end | CTA | "..." | "..." | … |

**Total VO word count:** <N>  (target: ~2.5 wps comfortable, ~3.5 wps energetic)

---

## On-screen text card list

1. `<card 1>` — <when, position>
2. `<card 2>` — <when, position>

---

## Production notes

- Caption style: word-by-word reveal | full-card | per-beat
- Audio bed: <music brief — genre, energy, BPM, where it ducks for VO>
- Sound design cues: <whoosh on cut at 3s, riser at offer, thud on stat reveal>
- Cuts: <pace — fast-cut every 1.0–1.5s | medium 2–3s | slow >3s>

---

## Variant ideas (for A/B if requested)

- Same body, different hook → swap hook A↔B
- Same script, different CTA → "10 days free" vs "Start free, no card"
- Different framework → re-cut as PAS instead of HSO
```

After the draft, show timestamps and total VO word count, and offer: tighten, change framework, swap CTA, write a 1:1 cut-down. When hook variants are presented, wait for an explicit pick or approval to ship two. An autonomous, non-interactive brief ships the strongest hook (noting the runner-up), uses defaults for missing inputs, and lists assumptions in the script header.

## Checklist

- [ ] Hook, last line and share trigger written before the body.
- [ ] Three hook variants; one picked with a one-line reason.
- [ ] One framework, matched to the awareness stage.
- [ ] Timestamps on every beat; total VO word count stated.
- [ ] One CTA for ads, no engagement bait; organic ends after the payoff.
- [ ] Every stat sourced or marked `TBD`.
- [ ] Disclosures line filled; no invented testimonials.
- [ ] Saved to `./video-out/<slug>/script.md`.

## Composition / References

- `video-hooks` — first-1.5 s patterns, endings and loops, mid-video re-hooks, banned opens.
- `ad-frameworks` — picking a framework by awareness level.
- `video-spec-sheet` — aspect, length cap and caption rules per platform.
- `video-editing` — length guidance by platform and goal.
- `video-storyboarding` — turning the script into shots.
- `content-disclosure`, `content-voice`, `content-humanize` — disclosures, brand voice, stripping AI cadence.
