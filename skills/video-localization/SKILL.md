---
name: video-localization
title: "Video Localization: Subtitle Translation and Dubbing"
description: "Localize a finished video: subtitle limits per language, re-timing, per-language burn-in, dubbed voice-over. Use for translated captions or dubs."
license: Apache-2.0
compatibility: "Requires: ffmpeg with libass for burn-in; a voice tool for dubbing. macOS/Linux."
capabilities: shell captions voice
domains: video
rules:
  - content(translate captions)
  - content(translated captions)
  - content(dubbing)
  - content(dubbed)
  - content(localize)
  - content(localise)
  - content(localization)
  - match((?i)\b(translate|translated)\s+(the\s+)?(subtitles?|captions?|srt)\b)
  - match((?i)\b(dub|dubbing|voice-?over)\b.{0,20}\b(in|into)\s+\w+\b)
  - match((?i)\b(make|create)\s+an?\s+\w+\s+version\s+of\s+(this|the|my)\s+video\b)
  - semantic(make this video available in Spanish and German)
  - semantic(translate the captions of my short into other languages)
---

## Overview

A finished short in one language becomes a set of per-language versions: translated subtitles that fit reading-speed limits, a burned-in cut per language, and optionally a dubbed voice track. The text translation itself belongs to the content domain's translation agent; this skill covers what the translation must fit into (line length, characters per second, cue timing) and what happens to the video afterwards.

## Mental model

A subtitle is a timed container with two hard limits: how many characters fit on a line and how many characters a viewer can read per second. A translation that is correct but too long fails the second limit, so the cure is a shorter translation or more time, never smaller type. Dubbing has the same problem in audio: the translated line must be speakable inside the original line's slot.

## Rules

### Limits per language

Netflix's Timed Text Style Guides are the public reference for subtitle limits. Use them as the default for any platform that does not publish its own. Values checked on 2026-11-15; re-check a language's guide before a client delivery.

| Language | Characters per line | Lines | Reading speed, adult programs | Source |
|---|---|---|---|---|
| English | 42 | 2 | 20 characters per second (17 for children's) | [English guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide) |
| Korean | 42 | 2 | 17 characters per second (13 for children's) | [Korean guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/216014517-Korean-Timed-Text-Style-Guide) |
| Japanese | 13 full-width horizontal, 11 vertical; half-width characters count half | 2 | 4 characters per second | [Japanese guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215767517-Japanese-Timed-Text-Style-Guide) |
| Any other language | Open that language's guide on Netflix Partner Help before translating; do not carry over the English numbers | 2 | Same | [Timed Text Style Guide index](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines) |

Timing for every language: a cue lasts at least 5/6 of a second (20 frames at 24 fps) and at most 7 seconds (same source). Where a line must break, prefer a bottom-heavy pyramid, break after punctuation and before conjunctions and prepositions, and keep names, articles with their nouns, and verbs with their auxiliaries together (English guide).

### Pipeline

1. Start from the source-language word timings and SRT of the locked cut (`video-captions`). Don't re-transcribe after the picture changes.
2. Hand the SRT text to the content domain's translation agent with the limits row for the target language. Ask for fit, not just meaning: the translation may condense, and it keeps brand names, numbers and the call to action intact.
3. Re-time. For each translated cue compute characters divided by cue duration and compare it with the table.
   - Over the limit and the neighbouring cue has slack: extend the cue into the slack, up to 7 seconds.
   - Still over: merge or split cues on sentence boundaries, then re-check the 5/6 second minimum.
   - Still over: send the line back for a shorter translation. Don't shrink the font or speed up the cue.
4. Save one SRT per language as `captions/<lang>.srt` under the video's output folder. Upload these as sidecar subtitle tracks wherever the platform accepts them.
5. Burn-in per language, only for platforms that take no sidecar (TikTok, Reels). Render with the `video-captions` command from the translated timings, one cut per language, with the `clean` preset: the bold presets are untested with non-Latin scripts. Use a font that covers the script (Noto Sans CJK for Chinese, Japanese, Korean; Noto Sans Arabic for Arabic), pass it with `--fontsdir` and `--font`, and render one frame before the full burn. Check three frames: text inside the safe zone from `video-spec-sheet`, no missing-glyph boxes, no overlap with the speaker's face.
6. Right-to-left scripts (Arabic, Hebrew): check one frame for line order and punctuation placement before the batch.

### Dubbing through the voice tool

Use the voice capability's `text_to_speech` with a voice that supports the target language; `search_voices` lists candidates. Use `voice_clone` to carry the speaker's own voice across languages only with that speaker's consent, recorded in the publish checklist.

1. Translate the script by speech segment, with the original segment's duration as the budget.
2. Synthesize each segment and measure its duration with `ffprobe`.
3. Over budget by up to 10 percent: speed the segment up with ffmpeg `atempo` (house default; beyond 10 percent speech sounds rushed). Over by more: send the line back for a shorter translation.
4. Under budget: pad with silence. Don't slow the voice.
5. Mix: dubbed voice on the dialogue track, the original music and effects bed kept, voice at the same loudness as the original (about -14 LUFS integrated for the finished file).
6. Run the lip-sync question explicitly: a dub on a talking-head shot will not match lip movement. Say so to the user and offer a lip-sync pass only if the `lipsync` capability is available.
7. A dub of a real person's voice, or an AI voice presented as a real person, falls under `content-disclosure`. Record the AI-voice line in the publish checklist.

On YouTube, a dubbed track is uploaded as an audio-only file of about the video's length under Languages in YouTube Studio, for channels with Advanced features access ([YouTube Help](https://support.google.com/youtube/answer/13338784), checked 2026-11-15). Other platforms need one finished video per language.

### Per-language deliverables

| Item | Path under the video's output folder |
|---|---|
| Subtitle file | `captions/<lang>.srt` |
| Burned cut | `cuts/<lang>/master-9x16.mp4` |
| Dubbed audio | `audio/<lang>-dub.wav` |
| Notes | `meta/localization.md`: target languages, limits row used, cues re-timed or shortened, voice and consent |

## Examples

### Example 1: Spanish subtitles for a 30 second short

Source SRT at 18 characters per second. Spanish runs about as long or longer. Translate, compute characters per second per cue, extend two cues into slack, send one 3-second cue back for a shorter line, deliver `captions/es.srt` and a `clean` burn.

### Example 2: Japanese cut

Horizontal lines hold 13 full-width characters, so a 2-second cue holds at most 8 characters at 4 characters per second. Condense hard; don't carry the English sentence over.

## Checklist

- [ ] Limits row opened for each target language; none copied from English.
- [ ] Every cue within the characters-per-second limit, 5/6 second minimum, 7 second maximum.
- [ ] One SRT per language saved; burned cuts only where the platform needs them.
- [ ] Font covers the script; three frames checked per burned cut.
- [ ] Dub segments within budget; voice-clone consent and AI-voice disclosure recorded.
- [ ] `meta/localization.md` written.

## References

- [Netflix English Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/217350977-English-Timed-Text-Style-Guide)
- [Netflix Korean Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/216014517-Korean-Timed-Text-Style-Guide)
- [Netflix Japanese Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215767517-Japanese-Timed-Text-Style-Guide)
- [Netflix subtitle timing guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)
- [YouTube Help: multi-language audio tracks](https://support.google.com/youtube/answer/13338784)
- `video-captions` skill: word timings and burn-in
- `video-spec-sheet` skill: safe zones
- `content-disclosure` skill: AI voice and dub disclosure
