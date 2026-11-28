---
name: video-explainers
title: "Explainer Videos: SaaS Demos and Hero Videos"
description: "Produce 60-180s explainer, SaaS demo and landing-page hero videos with Remotion motion graphics, voiceover, screen-capture briefs and captions."
license: Apache-2.0
compatibility: "Requires: Node.js, ffmpeg; ElevenLabs key for voice and music; Remotion (free for individuals and companies of up to 3 people, licence needed beyond). macOS/Linux."
capabilities: video-gen voice music composition
domains: producer
rules:
  - match((?i)\bexplainer\s+(videos?|films?|animations?)\b|\bexplainers?\b.{0,40}\b(voiceover|captions?|diagrams?|animated)\b)
  - match((?i)\b(make|create|produce|build|put together|turn|deliver)\b.{0,60}\b(explainer|walkthrough|recap video|hero (explainer|video)|pre-?roll)\b)
  - match((?i)\b(saas|product|app|software)\s+(demo|walkthrough|hero)\s+videos?\b|\b(landing[- ]page\s+)?hero\s+videos?\b|\bremotion\b)
  - match((?i)\banimated\s+(callouts?|diagrams?|flow|architecture)|\bmotion graphics\b|\bscreen recordings?\b.{0,40}\b(walkthrough|narrat\w+|video)\b|\brecap video\b)
  - semantic(make a 90 second explainer video for our product with voiceover and screen recordings, 0.78)
  - semantic(produce a youtube pre-roll that explains what our software does, 0.73)
  - semantic(create a saas demo hero video with motion graphics and narration, 0.72)
---

## Overview

This skill builds 60–180 s explainer videos for SaaS demos, landing-page hero videos, YouTube pre-roll and conference recap videos. The core is Remotion-based motion graphics plus voiceover, screen-capture cutaways and captions, in 16:9 with 9:16 cut-downs on request.

Explainers are clarity-led, not hype-led. The job is to make a complex product feel inevitable in two minutes. Pacing is medium (2–4 s per beat), the story arc is AIDA, and visuals are diagrams and screen capture, not cinematic generation. It does not cover short-form cinematic ads (`video-ad-production`), UGC-style avatar ads, or publishing.

## Mental model

```
brief
  → narrative arc (AIDA: hook, problem, solution, demo, CTA)
  → screen-capture script (what the user has to record)
  → motion-graphics storyboard (Remotion compositions)
  → voiceover (ElevenLabs, single voice, conversational pace ~2.5 wps)
  → music bed (ElevenLabs Music, low-energy, ducks under VO)
  → Remotion composition of motion graphics and screen captures
  → captions burned in
  → multi-aspect cut (16:9 master, 9:16 cut-down for Shorts)
```

## Rules

### Phase 1 — Narrative arc

1. Apply `video-hooks`, `video-spec-sheet` and `ad-frameworks`. Recall brand voice, positioning, primary CTA, winning explainers, banned claims and the preferred narrator voice from memory. Use `content-voice` for brand voice on the VO script.
2. Default framework: AIDA, with a FAB-loaded Desire beat for product-aware audiences.
3. Standard beat plan (90–120 s):
   - 0–8 s: hook and problem statement (AIDA: A + I)
   - 8–25 s: stakes — why the problem matters, who it hurts
   - 25–60 s: solution — what the product does, with one demo path
   - 60–95 s: proof — one customer, one stat, one screenshot
   - 95–115 s: differentiator — why this, not alternatives
   - 115 s–end: CTA — try free, book a demo, sign up
4. Save the beat sheet to `./video-out/<slug>/beats.md` and wait for approval. Then save the VO script to `./video-out/<slug>/script.md` (timestamped, 2.5 wps target); the `content-humanize` skill strips AI cadence from it before render.

### Phase 2 — Screen-capture brief

For software explainers the user records the screen; a real product UI can't be generated. Produce a precise brief and save it to `./video-out/<slug>/screen-capture-brief.md`:

```markdown
# Screen Capture Brief — <product>

## Recording 1 — Dashboard intro · used 8–14s
- Resolution: 1920×1080 (or 2560×1440 if Retina)
- Duration: 6–10s
- What to record: Open dashboard. Hover over the X chart. Click into the Y view.
- Cursor: visible; use a cursor highlighter if available.
- Window: full-app, no other tabs visible.

## Recording 2 — …
```

Wait for the user to drop recordings into `./video-out/<slug>/screen-cap/raw/` before continuing. Never skip this step for a software product.

### Phase 3 — Motion-graphics storyboard

For the moments not covered by screen capture (hook, problem framing, transitions, stat reveals, end card):

1. Each beat is one Remotion composition.
2. Visual style: clean, type-led, single accent color, simple iconography. Avoid the stock-footage explainer look unless the brief asks for it.
3. Generate reference frames via `image-gen` for non-typographic beats (b-roll, icons, illustrations). Save to `./video-out/<slug>/frames/`.
4. Use `video-gen` only for transition visuals: abstract motion, not literal scenes. Cinematic generation undersells an explainer, and fake software UI is never acceptable: use real screen capture or none.

### Phase 4 — Voiceover

1. A single voice for the whole explainer, ElevenLabs default, conversational and mid-energy.
2. Generate per beat (`vo/beat-NN.mp3`) so timing can be tightened.
3. Cadence about 2.5 words per second for technical content, about 3 for marketing-led explainers.
4. Pause discipline: at least 0.5 s between beats; longer before the offer.

### Phase 5 — Music bed

- A low-energy instrumental from `music` (ElevenLabs Music, `compose_music`).
- Ducks -8 to -10 dB under VO; full at silent transitions and the offer.
- One track for the whole explainer; switching tracks mid-piece kills coherence.

### Phase 6 — Composition (Remotion-led)

Remotion, not ffmpeg, is the default composer for explainers: they re-render often (data updates, copy edits, localization), and a React composition makes a copy change a one-line diff, not a re-edit. Remotion is free for individuals and companies of up to 3 people; larger companies need a Remotion Company License, so confirm before rendering client work.

1. Scaffold with the official CLI: `npx create-video@4.0.538 --yes --blank ./video-out/<slug>/remotion-project`, then `npm i` inside it.
2. Write one React composition per beat in `src/` and register them in `src/Root.tsx`: motion-graphics beats, screen-cap recordings (`<OffthreadVideo>` from `public/`), voiceover and music (`<Audio>`), captions.
3. Check key frames with `npx remotion still <CompositionId> out/check-NN.png --frame=<n>` and open and look at them before a full render.
4. Render the master: `npx remotion render <CompositionId> ../cuts/explainer-16x9.mp4 --codec=h264 --crf=18`.

### Phase 7 — Captions

1. Run the `video-captions` pipeline on the final VO mix: word timestamps, proofread against `script.md`.
2. 16:9 master: `clean` preset in the lower third (standard YouTube position). 9:16 cut-downs: `pop` preset at the preset default.
3. Burn the `.ass` onto the rendered master with `video-captions --burn`, or render captions inside Remotion from the `video-captions --remotion` JSON (`createTikTokStyleCaptions` from `@remotion/captions`). Ship the `.srt` sidecar for YouTube and LinkedIn uploads.

### Phase 8 — Multi-aspect delivery

Default 16:9 master (1920×1080). On request, also:

- 9:16 cut-down (60 s) for Shorts: re-edit, keep hook, solution and CTA, drop proof and differentiator.
- 1:1 cut-down (30 s) for LinkedIn and IG feed: hook, solution and CTA only.
- Hero video for a landing page: 16:9, muted, `playsinline`, poster frame, 20–40 s, captioned, compressed hard (aim under about 5 MB) so it doesn't sink the page's LCP.

### Explainer performance rules

- Pacing: 2–4 s per beat. Faster reads as an ad; slower reads as documentation.
- Cut every time the VO finishes a sentence; visual change reinforces information change.
- Show, don't summarize. If the VO says "the dashboard updates live", the screen capture shows it updating live.
- One stat per minute; two stats in a minute and both are forgotten.
- No music for the first 2 seconds, then fade in. A cold open with VO and visual reads as serious; a cold open with music reads as an ad.
- End on a still card with the CTA, not on a fade.
- A cloned voice of a real person or a realistic AI scene needs the disclosures in the `content-disclosure` skill; note it in the bundle. Generic narration TTS and diagrams don't.

### Interaction

- Brief received: confirm length target (60 / 90 / 120 / 180 s), primary aspect, awareness stage and screen-capture availability.
- Beat sheet drafted: wait for explicit approval before the full VO script.
- Screen-capture brief drafted: hand off and wait for recordings.
- Render complete: show the master cut; offer 9:16, 1:1 and muted-hero variants.
- "Iterate": treat as a copy or data update and re-render via Remotion with minimal diffs.
- An autonomous, non-interactive brief skips the beat-sheet approval wait, defaults to 90 s 16:9, and lists assumptions in `beats.md`; it still stops for screen-capture recordings that can't be produced.

## Output format

```
./video-out/<slug>/
  beats.md
  script.md
  screen-capture-brief.md
  screen-cap/
    raw/         (user-provided)
    edited/      (trims)
  frames/
  vo/
  music/
  captions/      (vo.json, captions.ass, captions.srt)
  remotion-project/
  cuts/
    explainer-16x9.mp4
    explainer-9x16-60s.mp4
    explainer-1x1-30s.mp4
    hero-muted-16x9.mp4
```

## Checklist

- [ ] AIDA beat sheet approved before the VO script.
- [ ] Screen-capture brief delivered; recordings received for software products.
- [ ] No fake software UI; no cinematic AI video standing in for a demo.
- [ ] One narrator voice, one music track, music fades in after 2 s.
- [ ] Captions burned for sound-off viewing, `.srt` sidecar shipped.
- [ ] Key frames checked with `remotion still` before the full render.
- [ ] Master and requested cut-downs saved under `./video-out/<slug>/cuts/`.

## Composition / References

- `video-hooks`, `ad-frameworks` — opening beat and AIDA structure.
- `video-spec-sheet` — 16:9, 9:16 and 1:1 specs.
- `video-captions` — captions for every cut-down.
- `content-voice`, `content-humanize` — brand voice; stripping AI cadence.
- `content-disclosure` — AI voice and scene disclosures.
