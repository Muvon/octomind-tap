---
name: video-clips
title: "Podcast Clips and Webinar Shorts from Long Recordings"
description: "Turn a podcast, webinar, stream or talk into ranked standalone vertical clips with reframes, captions and hooks. Use when picking podcast clips."
license: Apache-2.0
compatibility: "Requires: ffmpeg (libass build), auto-editor, python3, whisper-ctranslate2. macOS/Linux."
capabilities: video-editing thumbnails
rules:
  - match((?i)\b(podcast|webinar|livestream|stream|interview|talk|episode|recording|keynote)\b.{0,60}\b(clips?|shorts|highlights?|moments)\b)
  - match((?i)\b(clips?|shorts|highlights?|moments)\b.{0,40}\b(from|out of|of)\b.{0,40}\b(podcast|webinar|livestream|stream|interview|episode|recording|keynote)\b)
  - match((?i)\b(find|pick|extract|select)\b.{0,30}\b(best|top|standalone|viral)\s+(moments|clips|highlights)\b)
  - semantic(turn this podcast episode into short clips, 0.77)
  - semantic(find the best moments in this webinar recording and make vertical shorts, 0.77)
  - semantic(pick ranked standalone clips with captions and hooks from a long recording, 0.74)
---

## Overview

This skill turns a podcast episode, webinar, livestream, interview or conference talk into a ranked set of standalone vertical clips, each reframed, captioned and opened with a hook. Selection comes from the transcript, not from waveform peaks or a virality score: a clip earns its place when its first line stands alone and its payoff lands before it ends. Editing follows tested tools (auto-editor, the ffmpeg recipes in the `video-editing` skill, the `video-captions` script), never hand-written frame-processing code.

It does not cover editing a single short from raw footage end to end (`video-editing`), generating footage, or publishing.

## Rules

### Intake

1. Locate the recording and probe it: resolution, layout (one speaker, two side by side, camera-switched, screen share), duration, loudness.
2. Ask only for what is missing: how many clips, target platforms and goal, audience and topic focus, names to spell right, topics to avoid. Defaults: 10 clips, 9:16, length by platform and goal.
3. Recall earlier preferences from memory: show name and hosts, caption style, clip length preferences, topics to avoid, clips that performed.

### Transcript

Extract audio and transcribe once with word timestamps (`whisper-ctranslate2 ... --model medium --word_timestamps True --output_format json`; use `medium` or larger for multi-speaker audio; pass host and guest names with `--initial_prompt`). Save to `./video-out/<slug>/captions/full.json` and a readable `transcript.md` with a timestamp every sentence.

### Selection

1. Read the whole transcript. List 2–3× more candidates than requested.
2. A candidate opens on a self-contained line (a claim, a surprising number, a question, a contrarian take) and ends right after its payoff sentence, loop-friendly where the cut allows (`video-hooks`, "Endings and loops"). Write the hook and the last line first. Never end on a setup; never open on context the viewer lacks ("as I said earlier").
3. Score each 1–5 on hook strength, standalone clarity, payoff, and quotability; drop anything under 12/20.
4. Write `clips.md`: rank, start–end, length, first line, payoff line, re-hook points at likely drop-offs (`video-hooks`, "Mid-video re-hooks"), transformation (what the clip adds: reframe, hook, edit, captions), score with one-line reasoning, suggested on-screen hook (≤8 words), suggested title.
5. Show `clips.md` and wait for the user's picks ("1, 3, 4, 7"). An autonomous, non-interactive brief renders the top-ranked clips up to the requested count and lists assumptions in `clips.md`.

### Render each pick

Follow the `video-editing` skill and its recipe reference per clip:

1. Cut with 0.2–0.4 s padding at both ends; tighten internal silences with auto-editor (`--margin 0.15s`).
2. Reframe by layout: face-centred crop for one speaker (tracking the active speaker per segment), stacked halves for two side-by-side speakers, blurred fill for screen share. When the layout changes mid-recording (camera switches, screen-share segments), reframe per segment and note it in `clips.md`.
3. Land each re-hook point from `clips.md` with a punch-in, cutaway, or caption emphasis.
4. Two-pass loudness to -14 LUFS.
5. Run the `video-captions` pipeline on the cut clip: re-transcribe it, proofread names, render in `pop` (captions at `--y 0.5` on stacked layouts) with the `--hook` text, burn.
6. Render clips one by one and report progress; save as `cuts/clip-NN-9x16.mp4`.

### Deliver

Encode per `video-spec-sheet`. Render one cover per clip with `video-thumbnail render <frame> --format shorts --layout top --text "<hook text>"` from the hook frame (pull it with `video-thumbnail frames` or `ffmpeg -ss`; text stays inside the 3:4 grid crop, checked at feed size, see `video-thumbnails`). Write `meta/clips-manifest.md`: file, source timestamps, hook text, title, suggested caption copy, any disclosure. QA frames at the hook and the payoff of every clip, and each cover, by opening the images; if an image can't be read, list the frame files for the user and say placement is unverified.

### Retention review (after posting)

After about 24–72 h, run the retention review in the `video-hooks` skill per clip, then re-cut or re-hook the drop-off spot as a new clip and record what worked in memory. Never delete and re-upload a flopping Short.

### Selection and rights rules

| Rule | Why |
|---|---|
| Length follows the story, platform and goal: see the `video-editing` length guidance (monetized TikTok ≥60 s; Shorts often short; Reels ≤3 min for non-follower reach) | A clip cut before its punchline fails regardless of length |
| One idea per clip | Two ideas halve the payoff |
| Hook text names the tension, not the topic ("He turned down $2M" beats "Funding talk") | Text is read before the first word lands |
| Ship the full ranked set; the user's tests pick winners | Automated virality scores are not evidence |
| Guests and hosts keep their meaning; no splicing across sentences into new claims | Clips quote real people |
| Clips from someone else's show need the owner's permission | Repurposing rights belong to the recording's owner |
| Every clip names its transformation; reused footage with nothing new is held back (TikTok guidelines, YouTube Shorts originality update of 2026-10-01, Instagram aggregator rules). Watermarks and credits don't count | Reposts without new value lose reach |

## Examples

### Example 1: clip ends early

❌ A 30 s clip that stops on "and the reason that worked was" because the 30 s mark fell there.

✅ Extend to the end of the payoff sentence (42 s) or pick a tighter opening line; length follows the story.

### Example 2: hook text

❌ "Funding talk".

✅ "He turned down $2M" — the tension, in eight words or fewer.

## Output format

`./video-out/<slug>/`: `transcript.md`, `clips.md`, `captions/` (`full.json`, per-clip `clip-NN.json`, `.ass`, `.srt`), `work/`, `cuts/clip-NN-9x16.mp4`, `meta/` (`clip-NN-cover.jpg`, `clips-manifest.md`).

## Checklist

- [ ] Transcribed once with word timestamps; selection made from the transcript.
- [ ] `clips.md` written and the user's picks received before rendering.
- [ ] Each clip opens on a standalone line and ends after its payoff.
- [ ] Each clip names its transformation; rights are clear.
- [ ] Each cut clip re-transcribed for captions; names proofread.
- [ ] Loudness about -14 LUFS; encode per `video-spec-sheet`.
- [ ] One cover per clip; manifest written; QA frames opened.
- [ ] Everything saved under `./video-out/<slug>/`.

## Composition / References

- `video-editing` — cut, reframe, audio and loudness recipes.
- `video-captions` — per-clip captions and hook box.
- `video-hooks` — opening lines, endings, re-hooks, retention review.
- `video-spec-sheet` — encodes and safe zones.
- `video-thumbnails` — clip covers.
