---
name: video-captions
title: "Add Captions to Video: Word-Timed TikTok-Style Subtitles"
description: "Add captions to video that look edited, not hand-made: a word-timed video caption generator pipeline with word-level timestamps from local faster-whisper, TikTok/Reels caption presets (pop, karaoke, word, box, clean) with an active-word highlight, rendered to ASS and burned in with ffmpeg and libass, plus SRT sidecars and Remotion caption JSON. Use whenever a video needs auto captions, burned-in subtitles, a word-by-word highlight, or an on-screen hook line."
license: Apache-2.0
compatibility: "Requires: python3, an ffmpeg built with libass (macOS: Homebrew ffmpeg-full), and a word-timestamp source such as whisper-ctranslate2. macOS/Linux."
capabilities: shell captions
domains: video
rules:
  - session(adcraft)
  - session(ugc)
  - session(explainer)
  - session(editor)
  - session(clips)
  - content(footage)
  - content(clips)
  - content(podcast)
  - content(tiktok)
  - content(reels)
  - content(shorts)
  - content(captions)
  - content(subtitles)
  - match(\b(burn(ed)?[- ]in|word[- ]by[- ]word|karaoke)\s+(captions?|subtitles?|text)\b)
  - semantic(add animated captions to this video)
  - semantic(the subtitles look ugly, make them look like TikTok captions)
  - semantic(highlight each word as it is spoken)
---

## Overview

Captions carry the message for the muted viewer and decide whether a short looks edited or amateur. This skill is the one caption pipeline for the video domain: real word timings, a vetted renderer with platform-tuned presets, and a libass burn. It replaces hand-written frame-by-frame text drawing (PIL, moviepy, OpenCV) and plain `force_style` SRT burns, which produce the flat, mistimed captions viewers read as low effort.

## Mental model

Three inputs make a caption good, and the pipeline fixes each one at the source:

- Timing comes from per-word timestamps of the final audio, never from even spacing or sentence-level SRT.
- Look comes from a preset designed for the format: page size, case, outline, active-word highlight, position.
- Rendering goes through libass (the ASS subtitle renderer inside ffmpeg), which shapes text properly and animates per word at full frame rate.

The renderer is the `video-captions` command, installed on PATH with the `captions` capability (the same file is the bundled `scripts/captions.py`, listed under Skill Resources). It turns any word-timing JSON into a styled `.ass` file and can burn it. It needs only python3 and finds an ffmpeg with libass on its own, including Homebrew's keg-only `ffmpeg-full`. `video-captions --help` lists every option.

## Rules

### Pipeline

1. Caption last. Lock the cut and the audio mix first; caption timings must match the final file.
2. Extract the speech: `ffmpeg -i cut.mp4 -vn -ar 16000 -ac 1 captions/vo.wav`.
3. Get word timings (table below). Save the JSON under `./video-out/<slug>/captions/`.
4. Proofread the words against the script or brief. Fix single-word misspellings with `--replace Wrong=Right` (repeatable); fix multi-word errors by editing the `word`/`text` fields in the JSON and keeping the timings.
5. Fetch the font once (Fonts below).
6. Render and burn:

```bash
video-captions captions/vo.json --video cut.mp4 -o captions/captions.ass \
  --preset pop --fontsdir fonts --srt captions/captions.srt --burn cuts/master-9x16.mp4
```

7. Extract three frames at word-dense moments (`ffmpeg -ss 2.4 -i out.mp4 -frames:v 1 check-2.4.png`) and look at them: face clear, text inside the safe zone, highlight on the spoken word. Adjust `--y`, `--max-words`, or the preset and re-render. If your tools can't display images, rely on the script's font and safe-zone warnings, and tell the user which frame files to check and that placement is unverified.

Without `--burn` the script prints the exact burn command with the right ffmpeg binary; use that when the burn joins a larger filter chain (`-vf "scale=...,ass=captions.ass:fontsdir=fonts"`).

### Word-timing sources

| Situation | Source | How |
|---|---|---|
| Default, any audio | Local faster-whisper (`captions` capability, default provider) | `whisper-ctranslate2 captions/vo.wav --model small --language en --word_timestamps True --output_format json --output_dir captions` |
| Noisy creator footage, accents, non-English | Same CLI, bigger model | `--model large-v3-turbo` (or `medium`) |
| Brand names and jargon | Same CLI, biased | `--initial_prompt "Octomind, HeyGen, Reels"`, then `--replace` for leftovers |
| OpenAI key, `captions:whisper` provider | `transcribe_audio` | `model="whisper-1"`, `response_format="verbose_json"`, `timestamp_granularities=["word"]`; write the returned JSON to a file |
| JSON already exported from AssemblyAI, Deepgram, ElevenLabs Scribe or TTS with-timestamps, whisper.cpp `-ojf`, WhisperX | That file | Pass it straight to the script; it detects the shape and units |

The AssemblyAI MCP tools return transcript text only, so they can't time captions. An `.srt` input works but the script interpolates word timing inside each cue and warns; use it only when no audio is available.

### Presets

| Preset | Look | Use for |
|---|---|---|
| `pop` (default) | 1–3 words, uppercase, white with black outline, active word yellow and scaled up | TikTok, Reels, Shorts, UGC and talking-head ads |
| `karaoke` | Up to 5 words; spoken words switch to green and stay lit | Fast voiceover, listicles |
| `word` | One large word at a time with a scale-in | High-energy hooks and punchy lines; tiring past about 15 s |
| `box` | TikTok-native white box, black text, active word red | Lo-fi, native creator look |
| `clean` | Sentence case, 1–2 lines on a translucent box | 16:9 explainers, long-form, accessibility cuts |

Override per brand with `--highlight "#RRGGBB"`, `--color`, `--outline-color`, `--case`, `--max-words`, `--size`. Keep one accent color per video and white text on a dark outline for contrast. Keep pages short: TikTok's creative guidance caps on-screen text at 5–10 words per second, and the default pages follow speech word by word.

### Placement

| Frame | Default | Move it when |
|---|---|---|
| 9:16 talking head | Block centered at 58% of height, just under the chin | Face sits low in frame: `--y 0.62`; never over the face |
| 9:16 product or screen demo | 58% | The product or UI fills the middle: `--y 0.30` (upper third) |
| 16:9 | `clean` at 86%, other presets at 80% | Lower-third graphics occupy the bottom |
| Hook line | `--hook "text" --hook-end 3` puts a white box at 20% height | Always pair with the spoken hook in the first 3 s |

Keep the block out of the 9:16 UI bands: Meta Reels reserves the top 14% and bottom 35%, TikTok the right-side action rail and a caption area that grows from the bottom. The script warns when a page reaches into those bands.

### Fonts

The caption font must exist as a file; otherwise libass silently substitutes a plain fallback, the most common cause of ugly burns. Download it once into `./video-out/<slug>/fonts/` and pass `--fontsdir` (the script warns if it can't find the family):

| Family (`--font`) | File |
|---|---|
| Poppins Black (default) | `https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Black.ttf` |
| Montserrat Black | `https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Black.ttf` |
| Anton | `https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf` |
| Archivo Black | `https://github.com/google/fonts/raw/main/ofl/archivoblack/ArchivoBlack-Regular.ttf` |
| Bebas Neue | `https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf` |

All five are SIL Open Font License. A brand font the user supplies works the same way; `--font` takes the font's internal family name. Use `--bold` only for fonts without a heavy cut.

### Sidecars and other renderers

- `--srt file.srt` writes sentence-level cues for platform upload (YouTube, LinkedIn) alongside the burned captions.
- `--remotion file.json` writes Remotion `Caption[]` JSON. For Remotion compositions, feed it to `createTikTokStyleCaptions()` from `@remotion/captions`; in the `create-video --tiktok` template, save it as `public/<video>.json` next to `public/<video>.mp4` instead of running the template's whisper.cpp step. Use the Remotion path when captions need emoji or motion libass can't draw.
- Burned ASS can't render color emoji; keep emoji out of burned captions.
- Non-Latin scripts are untested with the bold presets: render one frame first, use `clean`, and a font that covers the script (Noto Sans CJK, Noto Sans Arabic).

## Examples

### Example 1: SRT force_style burn

❌ `ffmpeg -i ad.mp4 -vf "subtitles=captions.srt:force_style='Fontsize=44,Outline=2'" out.mp4` — one style for the whole file, sentence-length cues, no active-word highlight, and stock Homebrew ffmpeg fails outright (no libass).

✅ `video-captions captions/vo.json --video ad.mp4 -o captions/captions.ass --preset pop --fontsdir fonts --burn cuts/ad-captioned.mp4`

### Example 2: hand-rolled frame rendering

❌ A Python loop that draws text onto every frame with PIL, splitting the script evenly across the clip's duration. Timing drifts from speech, text has no shaping, and the render is slow.

✅ Transcribe the final audio with word timestamps, proofread, render with a preset. No custom drawing code.

### Example 3: captions over the face

❌ `--y 0.40` on a talking-head close-up: the caption block covers the mouth.

✅ Default `--y 0.58`, checked on an extracted frame; `--y 0.62` if the speaker sits low in frame.

## Checklist

- [ ] Captions rendered from word timings of the final cut's audio, not a draft and not interpolated SRT.
- [ ] Words proofread against the script; brand names spelled right.
- [ ] Font file downloaded into `fonts/` and passed with `--fontsdir`; no font warning from the script.
- [ ] Preset matches the format; one accent color.
- [ ] Three extracted frames checked (face clear, block inside the safe zone, highlight on the spoken word), or reported to the user as unchecked.
- [ ] `captions.ass`, `captions.srt`, and `vo.json` saved under `./video-out/<slug>/captions/`.

## Composition / References

- `video-spec-sheet` — platform safe zones, export presets, disclosure rules.
- `video-editing` — where captions sit in the edit pipeline (after the cut and the audio mix, before the final encode).
- `video-hooks` — the hook line passed to `--hook`.
- [ASS override tags (Aegisub)](https://aegisub.org/docs/latest/ass_tags/)
- [ffmpeg `ass` and `subtitles` filters](https://ffmpeg.org/ffmpeg-filters.html#ass)
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)
- [Remotion captions](https://www.remotion.dev/docs/captions/)
