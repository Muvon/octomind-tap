---
name: video-editing
title: "Footage Editing: Captioned Shorts and Ad Variants"
description: "Edit existing footage into captioned shorts: silence cuts, reframes, b-roll, ad variants, single edits like trims and joins. Use for cutting raw video."
license: Apache-2.0
compatibility: "Requires: ffmpeg (libass build for captions and text), auto-editor, python3, whisper-ctranslate2; Node.js for Remotion motion graphics. macOS/Linux."
capabilities: video-editing thumbnails voice music stock
rules:
  - match((?i)\b(edit|cut|trim|re-?cut|re-?frame|reframe)\b.{0,50}\b(footage|recording|talking[- ]head|vlog|raw (video|clip)|founder video|ugc delivery|podcast|webinar|keynote|interview|livestream|stream|vod)\b)
  - match((?i)\b(jump cuts?|punch[- ]ins?|silence (removal|cut)|dead air|b-?roll (inserts?|footage))\b)
  - match((?i)\bhook swaps?\b|\b(re-?cut|variants?|versions?)\b.{0,40}\b(winning|best[- ]performing|top[- ]performing)\s+(ad|video|creative)\b)
  - match((?i)\b(vertical|9:16)\s+clips?\b|\bclips?\.md\b|\b(standalone|quotable|self-contained)\s+(moments?|segments?|answers?)\b|\b(render|reframe|batch-render|pull|mine)\b.{0,40}\b(clips?|shorts|moments)\b)
  - match((?i)\b(trim|join|concat\w*|re-?encode|append)\b.{0,40}\b(video|clip|mp4|mov|file)\b)
  - semantic(edit my raw footage into a captioned short, 0.76)
  - semantic(cut the silences and add zooms and b-roll)
  - semantic(trim and join these video files and reframe them to vertical, 0.71)
---

## Overview

Most marketing video work starts from footage that already exists: a creator's talking head, a founder recording, a product demo, a UGC delivery, a clip someone generated, or last month's winning ad. This skill is the edit pipeline for that footage. It turns it into captioned, platform-ready shorts (a 9:16 master plus feed cut-downs), re-cuts a winner into new variants, or applies one requested edit to a finished file. It uses tested tools in a fixed order so the result looks edited rather than assembled: auto-editor for cuts, vetted ffmpeg recipes for reframes, punch-ins, cutaways and the audio mix, and the `video-captions` script for captions. Every command lives in `references/ffmpeg-recipes.md` (absolute path listed under Skill Resources); read it before the first edit step.

It does not cover generating new footage or avatar ads, long-form explainers, or publishing. Picking highlight clips out of long recordings is in the `video-clips` skill.

## Mental model

An edit is a chain of files, each the output of one decision: transcript → edit decision list → cut → reframe → visual rhythm → audio mix → loudness → captions → encode. Every step writes into `./video-out/<slug>/`, so any step can be redone without redoing the rest.

Native beats polished on short-form feeds: TikTok's own guidance asks for content that is not overly polished, and practitioners report that more distinct variants beat more polish on one. Spend effort on the story (hook, payoff, pacing), captions, and variants, not on effects.

Don't write custom frame-by-frame pipelines (moviepy, PIL, OpenCV loops). Every step below has a tested command; compose those.

## Rules

### Single-edit mode

The request names one operation on an existing file (burn these exact text lines, trim, join, append an end card, extract a frame, re-encode to a platform spec): do only that operation, skip the story steps and the approval wait.

1. Probe the input: resolution, frame rate, duration, audio streams.
2. Apply the matching recipe; burned-in text uses the given lines verbatim, inside the platform safe zone from `video-spec-sheet`.
3. QA: extract frames where the edit shows (each text line, each join, the last frame), open and look at them; probe the output and confirm duration, resolution and audio survived.
4. Write to the exact output path requested; return that path with the probe result and the QA frame paths.

### Footage → short

1. Ingest: locate the footage (paths given, or `./video-out/<slug>/raw/`), copy sources into `raw/`, probe resolution, frame rate, rotation, duration and loudness. Ask only for what is missing: platform(s), goal, organic or paid, CTA, brand font and colors, a reference edit to match. Defaults: 9:16 master, `pop` captions. If the footage is unusable (clipped audio, wrong orientation, too short for the brief), say what is wrong and the fix before editing.
2. Transcribe the raw audio with word timestamps (`whisper-ctranslate2 ... --word_timestamps True --output_format json`; see the `video-captions` sources table). Read it and write `./video-out/<slug>/edit.md`: the hook line for the first 1.5–3 s, the payoff, the last line (written with the hook: end right after the payoff, loop-friendly, see `video-hooks` "Endings and loops"), mid-video re-hook points at likely drop-off moments (`video-hooks` "Mid-video re-hooks"), keep ranges, cuts (flubs, repeats, filler, dead context) with timestamps and reasons, emphasis words for punch-ins, cutaway slots and what each shows, and the on-screen hook text. For a trend adaptation or repost, add the transformation: what the cut adds that the source does not.
3. Show `edit.md` and wait for approval before cutting. An autonomous, non-interactive brief skips the wait, uses the defaults, and lists assumptions in `edit.md`.
4. Clean the voice if it was recorded on a phone or in a room (voice cleanup recipe; `isolate_audio` only for heavy noise, on the final selects).
5. Cut: `auto-editor raw/clip.mp4 --margin 0.15s --cut A,B --cut C,D -c:v libx264 -crf 16 -o work/cut.mp4` — silence removal plus one `--cut` per flub range from `edit.md` (`3.2sec,3.6sec`). Keep 0.1–0.2 s of air so speech still breathes.
6. Reframe to the target aspect: face-centred crop for talking heads, blurred fill for screens and wide shots.
7. Visual rhythm: a visual change every 2–3 s. Hard 110–120% punch-ins on emphasis words (times from the transcript), b-roll cutaways of 1–3 s showing the product in use (the user's b-roll first, then Pexels via `searchVideos` / `downloadVideo`, otherwise list the gap), text cards for numbers and lists. The speaker's face carries the hook.
8. Audio: SFX on cutaway entries only (one whoosh or pop, not every cut; `text_to_sound_effects` when no library exists). Music bed ducked under the voice (`compose_music`), or none for UGC-style; licensed or generated music only.
9. Loudness: two-pass to -14 LUFS integrated, -1 dBTP.
10. Captions and hook box: run the `video-captions` pipeline on the mixed file, only after the cut and the mix are final. Presets: `pop` default, `box` for a native lo-fi look, `clean` for 16:9. Add the `--hook` text, burn, write the SRT sidecar.
11. Encode with the `video-spec-sheet` preset; export 4:5 and 1:1 cut-downs re-captioned at their size; render the cover with `video-thumbnail render <hook frame> --format reels --layout top --text "<hook text>"` (a 16:9 cut also gets a `--format youtube` thumbnail; full Test & Compare sets are in the `video-thumbnails` skill).
12. QA: watch the whole cut once, then open frames at the hook, every cutaway, the CTA, and the cover preview; check loudness and the caption script's safe-zone warnings. If an image can't be read, list the frame files for the user and say what is unverified.

### Edit conventions

Defaults, with the strength of their evidence. Let the account's own retention and hook-rate data overrule them.

| Convention | Default | Evidence |
|---|---|---|
| Hook | Spoken hook and on-screen hook text in the first 1–3 s; product or brand visible by 3 s | TikTok creative guidance |
| Captions | Always, word-timed, inside the safe zone; audio leads, captions support | Platform guidance (most views sound-on; captions serve the rest and search) |
| On-screen text pace | 5–10 words per second at most | TikTok creative guidance |
| Ending | Ads: CTA on a held frame or card, not a fade. Organic: end right after the payoff, last frame flows back into the hook | TikTok-cited recall data; practitioner |
| Length | By platform and goal (next section); ad length follows the platform's ad spec and the creative test | Measured, per platform |
| Visual change | Every 2–3 s | Practitioner |
| Punch-ins | 110–120%, hard cut on an emphasis word | Practitioner |
| B-roll | 20–40% of runtime, 1–3 s each, product in use | Practitioner and vendor |
| SFX | Only on cutaway entries and reveals | Practitioner |
| Music | Ducked under voice; about -18 dB or off for UGC | Practitioner |
| Look | Native, lo-fi framing beats studio gloss on TikTok | TikTok creative guidance |

### Length by platform and goal

Descriptive data, not targets; let the account's own retention overrule it, and let the story set the length.

- TikTok organic: videos over 60 s got 43.2% more reach (Buffer, 1.1M videos, 2025-03, measured). US TikTok Creator Rewards needs videos of at least 1 min (official terms, 2026-07-20).
- YouTube Shorts: 11–20 s had the highest median views (quso.ai, 508k posts in the full dataset; Shorts subset size unstated, 2026-06, measured).
- Instagram Reels: videos up to 3 min can reach non-followers (reported platform guidance, Instagram Help via Socialinsider, 2026-07).
- Paid ads: length follows the platform's ad spec and the creative test; put the hook and proposition in the first 3 s.
- Don't pad to hit a length, and don't cut a payoff to fit one.

### Iterating a winning ad

- Hook swaps: same body, new first 1.5–3 s (new spoken line, new opening shot, or new hook text). Ship 3–5 clearly different hooks, not wording tweaks, plus distinct concepts (different angle, format, or opening scene): Jon Loomer's Meta Andromeda guidance says ad variations should differ significantly, not subtly, so concept variety is what widens the test (directional).
- Re-cuts: length variants from the same selects, chosen by platform and goal; tighter pacing; a different CTA.
- Resizes: 9:16 master, then 4:5 and 1:1 for feeds, re-captioned at each size.
- Claims and the offer stay exactly as approved.
- Name every file `YYYYMMDD_concept_angle_hookID_format_len_vN` (e.g. `20261024_founder_pain_h3_9x16_30s_v1.mp4`) and list each variant in `meta/variants.md` with what changed.

### Retention review of a flop

After about 24–72 h, run the retention review in the `video-hooks` skill, then re-cut or re-hook the drop-off spot as a new variant and record what worked in memory. Never delete and re-upload a flopping Short.

### Integrity

- Cuts tighten what the speaker said; they never splice words into a claim, testimonial or result the speaker did not make.
- Creator footage used in paid ads needs the creator's usage rights; paid partnerships carry the platform's partnership label.
- Brand content uses licensed, owned or generated music, never trending sounds.
- Reused material needs a transformation (TikTok guidelines, YouTube Shorts originality update of 2026-10-01, Instagram aggregator rules); watermarks and credits don't count.

### Tool choice

| Need | Use |
|---|---|
| Silence cuts, filler and flub ranges | auto-editor |
| Reframes, punch-ins, cutaways, text cards, audio mix, loudness, encodes | ffmpeg recipes in `references/ffmpeg-recipes.md` |
| Captions and hook box | `video-captions` script |
| Kinetic type, animated graphics, smooth camera moves, many templated variants | Remotion (`npx create-video@4.0.538 --yes --blank`, `npx remotion render`) |
| Hand-off to a human editor | `auto-editor raw.mp4 --export premiere` (or `resolve`, `final-cut-pro`) plus `edit.md` |
| Translated subtitles, per-language burn-ins, dubbed voice-over of a finished cut | `video-localization` skill |

Keep generation loss low: intermediates at `-crf 16 -preset veryfast`, one final encode at the platform preset, and never re-encode a file that is only being remuxed (`-c copy`).

## Examples

### Example 1: silence cutting

❌ A Python loop that detects quiet frames with numpy and writes kept frames through moviepy. Slow, drops audio sync, and loses quality on every pass.

✅ `auto-editor raw/clip.mp4 --margin 0.15s -c:v libx264 -crf 16 -o work/cut.mp4`, then `--export v1` if the kept ranges are needed for planning.

### Example 2: captions before the cut

❌ Transcribe and caption the raw recording, then cut silences: every caption after the first cut drifts.

✅ Transcribe the raw file only to plan cuts; caption the final mixed file.

### Example 3: a splice that invents a claim

❌ Joining "we cut costs" from minute 2 with "by 80%" from minute 9 into one sentence.

✅ Keep the speaker's sentences whole; cut between sentences, never inside a claim.

## Output format

`./video-out/<slug>/`: `edit.md`, `raw/`, `work/` (intermediates), `broll/`, `sfx/`, `music/`, `captions/` (`vo.json`, `captions.ass`, `captions.srt`), `cuts/` (`master-9x16.mp4`, `feed-4x5.mp4`, `feed-1x1.mp4`, variants), `thumbs/` (`cover-reels.jpg`, previews), `meta/` (`variants.md`, `publish-checklist.md` with music source and any disclosure).

## Checklist

- [ ] `edit.md` written before cutting: hook, payoff, keep ranges, cuts with reasons.
- [ ] Cuts made with auto-editor and recipes; no custom frame-processing code.
- [ ] Hook spoken and shown in the first 3 s; product or subject visible early.
- [ ] Visual change about every 2–3 s; cutaways show the product in use.
- [ ] Voice clear over music; loudness about -14 LUFS, true peak ≤ -1 dBTP.
- [ ] Word-timed captions on the final mix, inside the safe zone.
- [ ] Platform encode per `video-spec-sheet`; cut-downs re-captioned; cover frame saved.
- [ ] Variants named by the convention and listed in `meta/variants.md`.
- [ ] Length chosen for the platform and goal; organic ends right after the payoff and loops into the hook.
- [ ] Variants include distinct concepts, not only hook swaps.
- [ ] After posting: retention drop-off second found and re-cut or re-hook done (`video-hooks`).

## Composition / References

- `video-captions` — word timings, caption presets, burn.
- `video-spec-sheet` — safe zones, encode presets, disclosure and music rules.
- `video-hooks` — hook patterns for hook swaps, endings, re-hooks, retention review.
- `video-thumbnails` — covers and thumbnails.
- `video-localization` — translated subtitles and dubs.
- `video-clips` — selecting standalone clips from long recordings.
- `references/ffmpeg-recipes.md` — tested commands for every step above.
- [auto-editor options](https://auto-editor.com/ref/options)
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)
- [ffmpeg filters](https://ffmpeg.org/ffmpeg-filters.html)
- [Buffer: longer TikToks get more views](https://buffer.com/resources/longer-tiktoks-get-more-views-data) — 1.1M videos, over 60 s +43.2% reach (measured, 2025-03).
- [quso.ai video retention benchmarks](https://quso.ai/research/video-retention-benchmarks) — 508k posts in the full dataset (Shorts subset size unstated), Shorts 11–20 s highest median views (measured, 2026-06).
- [TikTok Creator Rewards program terms (US)](https://www.tiktok.com/legal/page/global/creator-rewards-program-us/en) — US eligibility needs videos of at least 1 min (official, 2026-07-20).
- [Instagram Reels length (Instagram Help via Socialinsider)](https://www.socialinsider.io/blog/instagram-reels-length/) — non-follower reach for videos up to 3 min (reported, 2026-07).
- [Jon Loomer: Meta Andromeda creative diversification](https://www.jonloomer.com/meta-andromeda-creative-diversification/) — variations should differ significantly, not subtly (directional, 2025-10-20).
