---
name: video-editing
title: "Short-Form Video Editing: Footage to Platform-Ready Shorts"
description: "Short-form video editing pipeline for marketing and creator footage, built on code-driven tools: transcript-first story selection, auto-editor silence cuts and jump cuts, horizontal-to-vertical 9:16 reframes, punch-ins, b-roll cutaways, SFX, audio ducking under the voice, loudness normalization, word-timed captions, and platform encodes, plus podcast and webinar clip selection and hook-swap variants of winning ads. Use when editing footage someone shot, clipping a podcast or webinar, or re-cutting an existing ad."
license: Apache-2.0
compatibility: "Requires: ffmpeg (libass build for captions and text), auto-editor, python3; Node.js for Remotion motion graphics. macOS/Linux."
capabilities: shell video-editing captions
domains: video
rules:
  - session(editor)
  - session(clips)
  - session(adcraft)
  - session(ugc)
  - content(footage)
  - content(podcast)
  - content(webinar)
  - content(clips)
  - match(\b(edit|cut|trim|clip|re-?cut)\b.*\b(footage|recording|talking[- ]head|podcast|webinar|stream|vlog|raw (video|clip))\b)
  - match(\b(jump cuts?|punch[- ]ins?|b-?roll|silence (removal|cut)|dead air)\b)
  - match(\bhook (swap|variants?)\b)
  - semantic(edit my raw footage into a short)
  - semantic(turn this podcast episode into short clips)
  - semantic(cut the silences and add zooms and b-roll)
  - semantic(make new hook variants of my winning ad)
---

## Overview

Most marketing video work starts from footage that already exists: a creator's talking head, a founder recording, a podcast episode, a product demo, or last month's winning ad. This skill is the edit pipeline for that footage. It uses tested tools in a fixed order so the result looks edited rather than assembled: auto-editor for cuts, vetted ffmpeg recipes for reframes, punch-ins, cutaways and the audio mix, and the `video-captions` script for captions. Every command lives in `references/ffmpeg-recipes.md` (absolute path listed under Skill Resources); read it before the first edit step.

## Mental model

An edit is a chain of files, each the output of one decision: transcript → edit decision list → cut → reframe → visual rhythm → audio mix → loudness → captions → encode. Every step writes into `./video-out/<slug>/` (`raw/`, `work/`, `broll/`, `sfx/`, `music/`, `captions/`, `cuts/`, `meta/`), so any step can be redone without redoing the rest.

Native beats polished on short-form feeds: TikTok's own guidance asks for content that is not overly polished, and practitioners report that more distinct variants beat more polish on one. Spend effort on the story (hook, payoff, pacing), captions, and variants, not on effects.

Don't write custom frame-by-frame pipelines (moviepy, PIL, OpenCV loops). Every step below has a tested command; compose those.

## Rules

### Footage → short

1. Ingest: copy sources into `raw/`, probe resolution, frame rate, rotation, duration, and loudness.
2. Transcribe the raw audio with word timestamps (`video-captions` sources table). Read it and write `edit.md`: the hook line, the payoff, the ranges to keep, the flubs, repeats and filler to cut, each with a reason.
3. Clean the voice if it was recorded on a phone or in a room (voice cleanup recipe).
4. Cut: `auto-editor raw/clip.mp4 --margin 0.15s --cut A,B --cut C,D -c:v libx264 -crf 16 -o work/cut.mp4` — silence removal plus one `--cut` per flub range from `edit.md` (`3.2sec,3.6sec`). Keep 0.1–0.2 s of air so speech still breathes.
5. Reframe to the target aspect: face-centred crop for talking heads, blurred fill for screens and wide shots.
6. Visual rhythm: a visual change every 2–3 s. Hard 110–120% punch-ins on emphasis words (times from the transcript), b-roll cutaways of 1–3 s showing the product in use, text cards for numbers and lists. The speaker's face carries the hook.
7. Audio: SFX on cutaway entries only (one whoosh or pop, not every cut). Music bed ducked under the voice, or none for UGC-style; licensed or generated music only.
8. Loudness: two-pass to -14 LUFS integrated, -1 dBTP.
9. Captions and hook box: `video-captions` pipeline on the mixed file.
10. Encode with the `video-spec-sheet` preset; export cut-downs; pull a cover frame.
11. QA: watch the whole cut once, then check frames at the hook, every cutaway, and the CTA.

### Edit conventions

Defaults, with the strength of their evidence. Let the account's own retention and hook-rate data overrule them.

| Convention | Default | Evidence |
|---|---|---|
| Hook | Spoken hook and on-screen hook text in the first 1–3 s; product or brand visible by 3 s | TikTok creative guidance |
| Captions | Always, word-timed | Platform guidance (muted viewing) |
| On-screen text pace | 5–10 words per second at most | TikTok creative guidance |
| Ending | CTA on a held frame or card, not a fade | TikTok-cited recall data |
| Length | 15–35 s for ads and organic shorts | Practitioner |
| Visual change | Every 2–3 s | Practitioner |
| Punch-ins | 110–120%, hard cut on an emphasis word | Practitioner |
| B-roll | 20–40% of runtime, 1–3 s each, product in use | Practitioner and vendor |
| Music | Ducked under voice; about -18 dB or off for UGC | Practitioner |
| Look | Native, lo-fi framing beats studio gloss on TikTok | TikTok creative guidance |

### Long-form → clips

1. Transcribe the full episode with word timestamps (`--model medium` or larger for multi-speaker audio).
2. Find 20–40 s candidates that stand alone: they open on a strong self-contained line and hold the payoff to the end. Never end before the punchline; never open on context the viewer lacks.
3. Score each candidate 1–5 on hook strength, standalone clarity, payoff, and quotability. Write `clips.md`: rank, start–end, first line, payoff line, score, suggested on-screen hook.
4. Cut each pick with a little padding, reframe (track the active speaker per segment), caption with a `--hook` line, and render as `cuts/clip-NN-9x16.mp4`.
5. Ship the full ranked set; the user's tests pick winners. Automated virality scores are not evidence.

### Iterating a winning ad

- Hook swaps: same body, new first 1.5–3 s (new spoken line, new opening shot, or new hook text). Ship 3–5 clearly different hooks, not wording tweaks.
- Re-cuts: 15 / 30 / 45 s lengths from the same selects; tighter pacing; a different CTA.
- Resizes: 9:16 master, then 4:5 and 1:1 for feeds, re-captioned at each size.
- Name every file `YYYYMMDD_concept_angle_hookID_format_len_vN` (e.g. `20261024_founder_pain_h3_9x16_30s_v1.mp4`) and list each variant in `meta/variants.md` with what changed.

### Tool choice

| Need | Use |
|---|---|
| Silence cuts, filler and flub ranges | auto-editor |
| Reframes, punch-ins, cutaways, text cards, audio mix, loudness, encodes | ffmpeg recipes in `references/ffmpeg-recipes.md` |
| Captions and hook box | `video-captions` script |
| Kinetic type, animated graphics, smooth camera moves, many templated variants | Remotion (`npx create-video@4.0.538 --yes --blank`, `npx remotion render`) |
| Hand-off to a human editor | `auto-editor raw.mp4 --export premiere` (or `resolve`, `final-cut-pro`) |

Keep generation loss low: intermediates at `-crf 16 -preset veryfast`, one final encode at the platform preset, and never re-encode a file that is only being remuxed (`-c copy`).

## Examples

### Example 1: silence cutting

❌ A Python loop that detects quiet frames with numpy and writes kept frames through moviepy. Slow, drops audio sync, and loses quality on every pass.

✅ `auto-editor raw/clip.mp4 --margin 0.15s -c:v libx264 -crf 16 -o work/cut.mp4`, then `--export v1` if the kept ranges are needed for planning.

### Example 2: captions before the cut

❌ Transcribe and caption the raw recording, then cut silences: every caption after the first cut drifts.

✅ Transcribe the raw file only to plan cuts; caption the final mixed file.

### Example 3: podcast clip ends early

❌ A 30 s clip that stops on "and the reason that worked was" because the 30 s mark fell there.

✅ Extend to the end of the payoff sentence (42 s) or pick a tighter opening line; length follows the story.

## Checklist

- [ ] `edit.md` (or `clips.md`) written before cutting: hook, payoff, keep ranges, cuts with reasons.
- [ ] Cuts made with auto-editor and recipes; no custom frame-processing code.
- [ ] Hook spoken and shown in the first 3 s; product or subject visible early.
- [ ] Visual change about every 2–3 s; cutaways show the product in use.
- [ ] Voice clear over music; loudness about -14 LUFS, true peak ≤ -1 dBTP.
- [ ] Word-timed captions on the final mix, inside the safe zone.
- [ ] Platform encode per `video-spec-sheet`; cut-downs re-captioned; cover frame saved.
- [ ] Variants named by the convention and listed in `meta/variants.md`.

## Composition / References

- `video-captions` — word timings, caption presets, burn.
- `video-spec-sheet` — safe zones, encode presets, disclosure and music rules.
- `video-hooks` — hook patterns for hook swaps and clip openers.
- `references/ffmpeg-recipes.md` — tested commands for every step above.
- [auto-editor options](https://auto-editor.com/ref/options)
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)
- [ffmpeg filters](https://ffmpeg.org/ffmpeg-filters.html)
