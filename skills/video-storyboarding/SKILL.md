---
name: video-storyboarding
title: "Shot List and Storyboard: Beat-by-Beat Video Planning"
description: "Plan a beat-by-beat video storyboard and shot list: framing, motion, transitions, music brief, asset checklist, reference frames. Use after a script."
license: Apache-2.0
compatibility: "Stack-agnostic; reference frames need an image generation tool."
domains: producer
rules:
  - match((?i)\b(plan|planning|draft|create|build|produce|make|deliver|need|write)\b[^.]{0,30}\bstory-?boards?\b|\bstory-?boards?\s+(for|with|of)\b)
  - match((?i)\b(shot[- ]by[- ]shot|shot\s+list|beat\s+sheet|beat[- ]by[- ]beat|asset checklist|reference frames?)\b)
  - match((?i)\b(plan|break down|lay out)\b.{0,30}\b(the\s+)?shots?\b)
  - semantic(plan every shot of this ad with framing, motion and transitions, 0.77)
  - semantic(turn this script into a storyboard with reference frames)
  - semantic(build a shot list and music brief before we generate visuals, 0.71)
---

## Overview

This skill turns a brief or a finished script into a frame-accurate storyboard: shot list, framing, motion, on-screen text positions, audio bed, transitions, and an asset checklist, with optional generated reference frames per beat. It produces plans and reference frames, never finished video. It does not write the script (`video-script-writing`), generate clips, voice or music, stitch, or publish.

## Rules

### Workflow

1. Intake. Read the script at `./video-out/<slug>/script.md` if one exists. If not, ask for the brief (product, audience, platform, length, framework, hooks), or ask the user to provide or generate the script first. Recall brand voice and tone notes from memory.
2. Apply `video-hooks` to the first beat, `video-spec-sheet` for aspect, fps, safe zones and caption positions, and `ad-frameworks` so pacing matches the framework (an HSO body is longer than a PAS body). Tone notes from the `content-voice` skill carry into voiceover direction.
3. Decompose the script into discrete beats. One beat = one camera setup or one cut; if you write "and then…" inside a beat, it's two beats. Typical short-form: 8–18 beats per 30 s; long-form: about 15–30 beats per minute. Self-correct: fewer than 8 beats in 30 s means stretch one or two; more than 18 means collapse adjacent ones.
4. Design each beat: framing (close / medium / wide), motion (static, zoom-in, push-in, whip-pan, handheld, dolly), subject, on-screen text and position, transition into the next beat, audio cue. Present the beat list and wait for sign-off before generating frames.
5. Music and sound design: brief the soundtrack (genre / BPM / mood / where it ducks) and the SFX layer (whooshes on cuts, risers on the offer, impacts on stat reveals).
6. Asset checklist: enumerate every asset that must exist before render: stock clips (Pexels), AI-generated frames, AI-generated clips, voiceover lines, music track, captions.
7. Reference frames (optional, on request or when the product or aesthetic is unfamiliar): after approval, generate one image per beat in parallel, all calls in one tool block.
8. Save `./video-out/<slug>/storyboard.md` and `./video-out/<slug>/asset-checklist.md`. An autonomous, non-interactive brief skips the sign-off wait, generates frames only if the brief asked for them, and lists assumptions in `storyboard.md`.

### Reference frames

1. Match the storyboard's aspect ratio in every call via the tool's `aspect_ratio` parameter (`9:16`, `1:1`, `16:9`, `4:5`). Frames that will become generated clips use the clip's ratio, since image-to-video animates the frame as given.
2. One image per beat, `output_format: png` (the tool defaults to webp). Filename `frames/beat-NN.png`. Files land in `./image-out/`; list those paths in the storyboard. Pass earlier frames as `inputImagePaths` with `maintainCharacterConsistency` when a character recurs.
3. Prompt template (plain language; no Midjourney-style `--flags`):
   ```
   <subject>, <framing>, <motion suggestion as static composition>,
   <lighting>, <style — photorealistic / 3D / illustrated / etc.>
   ```
4. Save the prompt and seed beside each frame in `asset-checklist.md` so the prompt can be re-run for variants.

### Guards

- Don't generate frames before the beat list is approved.
- Don't mix aspect ratios across beats; pick one and hold it.
- Don't place critical text in a platform's UI bands (outside the safe zone; see `video-spec-sheet`).
- The asset checklist is the source of truth: no asset is "remembered" outside it.
- Flag anything AI-generated in each beat's generation source, for the disclosure step at publish.
- Save outputs to `./video-out/<slug>/` only.

## Output format

Save to `./video-out/<slug>/storyboard.md`:

```markdown
# Storyboard — <product>, <platform>, <length>

**Aspect:** <9:16 | 1:1 | 16:9 | 4:5> · **fps:** <30 | 60> · **Length:** <Xs> · **Beats:** <N>

## Beats

### Beat 01 — <name> · 0:00–0:01.5 · Hook
- Framing: <close-up | medium | wide | extreme close>
- Subject: <person | product | text | screen | b-roll>
- Camera: <static | zoom-in 0→100 | push-in | whip-pan | handheld>
- On-screen text: `<text>` — position: <upper-third center | center | etc.>
- Voiceover: "<line>"
- Transition out: <hard cut | whip-pan | match-cut | dip-to-white>
- Audio cue: <SFX, music swell, drop>
- Reference frame: `frames/beat-01.png` (or "tbd")
- Generation source: <stock | flux | recraft-svg | video-gen-i2v | live-action>

### Beat 02 — …

### Beat NN — CTA · X:XX–end

## Music brief

- Genre: <e.g. minimal techno | lo-fi hip-hop | cinematic riser>
- BPM: <range>
- Energy curve: <flat | rises into offer | drops at hook then rises>
- Mix: ducks -8 dB under VO, full at silent beats and at the offer
- Track sources, in order of preference: ElevenLabs Music (`compose_music`) → curated stock library

## Sound design layer

| t | SFX | Reason |
|---|---|---|
| 0:00 | whoosh + sub-impact | hook reveal |
| 0:03 | riser | building toward problem |
| 0:18 | drop + texture | solution reveal |
| 0:28 | UI click | CTA emphasis |

## Asset checklist

| ID | Beat | Type | Source | Status |
|---|---|---|---|---|
| F01 | 01 | still | flux | TODO |
| C02 | 02 | clip | video-gen-i2v from F01 | TODO |
| V01 | 01–14 | voiceover | elevenlabs | TODO |
| M01 | full | music | elevenlabs-music | TODO |
| S01 | 01,03,18,28 | sfx | local lib / freesound | TODO |
```

Save the asset checklist as a standalone file too: `./video-out/<slug>/asset-checklist.md` (same table, expanded with prompts and seeds for each generated asset).

## Checklist

- [ ] Script read, or the brief confirmed.
- [ ] One beat per camera setup; beat count in range for the length.
- [ ] One aspect ratio across all beats; text inside the safe zone.
- [ ] Beat list approved before any frame generation.
- [ ] Music brief, sound design layer and asset checklist complete; AI-generated sources flagged.
- [ ] `storyboard.md` and `asset-checklist.md` saved.

## Composition / References

- `video-script-writing` — the script a storyboard starts from.
- `video-hooks` — hook beats.
- `video-spec-sheet` — aspect, fps, safe zones, caption positions.
- `ad-frameworks` — pacing by framework.
- `content-voice` — tone notes for voiceover direction.
