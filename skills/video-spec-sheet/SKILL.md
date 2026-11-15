---
name: video-spec-sheet
title: "Video Spec Sheet: Platform Specs and Safe Zones"
description: "Platform video output specs: aspect ratio, length, codec, bitrate, safe zones, ffmpeg presets for TikTok, Reels, Shorts, YouTube. Use to check an export."
license: Apache-2.0
compatibility: "Stack-agnostic."
domains: video content
rules:
  - session(video)
  - session(adcraft)
  - content(reels)
  - content(shorts)
  - content(tiktok)
  - content(instagram stories)
  - content(aspect ratio)
  - match(\bsafe\s+zone\b)
  - match(\b(video\s+)?codec\b)
  - match(\b(video\s+)?bitrate\b)
  - match(\bplatform\s+specs?\b)
  - match(\b(9:16|16:9|1:1|4:5)\b)
  - semantic(what dimensions should I export this video at)
  - semantic(safe export settings for TikTok or Reels)
  - semantic(what are the platform specs for short-form video)
  - semantic(which codec and bitrate should I use for vertical video)
  - semantic(why does my video get cropped on Instagram)
---

## Overview

Each social platform has its own combination of aspect ratio, max duration, codec, bitrate, frame rate, and caption / UI safe zones. Getting any of these wrong on the export means the platform will either reject, re-encode (quality drop), or crop your creative. This skill encodes the 2026 specs as a single table the agent extracts from per brief. Caps and safe zones move several times a year: treat every number marked 2026 as a starting point and confirm it against the platform's live spec page before a paid launch.

## Instructions

### Core Rules

- Always pick the platform spec before generating frames — generation must match the export aspect ratio (don't generate 16:9 then crop to 9:16 unless intentional).
- Burn captions on top of the base render, not as a sidecar. Don't assume Reels are watched sound-off: Meta reports over 75% of Reels views are sound-on (official, Meta for Developers, 2024-11-07). Captions carry the message for the muted viewer and accessibility while the audio carries it for everyone else; in TikTok's Kantar survey 88% of TikTok users said sound is essential (self-reported; official, TikTok for Business blog, 2021-06). Render them from word timings through libass with the `video-captions` skill; stock Homebrew ffmpeg has no libass.
- Respect the safe zone — keep all critical text and faces away from where the platform's UI sits (top, bottom, right side for TikTok).
- Final encode in H.264 / yuv420p, even if the source is HEVC / 10-bit. Universal compatibility beats marginal quality.
- Audio: AAC-LC stereo, 48 kHz, 128 kbps minimum (YouTube recommends 384 kbps stereo for uploads). Mono audio reads as low-quality on most feeds.
- Loudness: master to about -14 LUFS integrated, true peak ≤ -1 dBTP. YouTube normalizes to roughly that level; TikTok and Meta don't publish a target, so -14 is a safe common master.
- AI-generated clips often come out at 720p or 768p class resolution (see the provider table below for each provider's limits). Upscale picked shots before the final 1080p encode; never let the platform upscale.
- Re-encoding with ffmpeg drops any C2PA Content Credentials the generator embedded, so platform auto-labelling of AI content will not fire. Disclose manually at upload (see the `content-disclosure` skill).

### Platform Spec Table (2026 — verify live)

| Platform | Aspect | Resolution | Length cap | Frame rate | Codec | Bitrate | Audio |
|---|---|---|---|---|---|---|---|
| TikTok organic | 9:16 | 1080×1920 | Most accounts post up to 3 min, some up to 5 or 10 min (TikTok developer docs, checked 2026-11-15); look up the current upload limit for TikTok.com and TikTok Studio in TikTok Help | 30 / 60 | H.264 | 8–10 Mbps | AAC 128k+ 48kHz |
| TikTok in-feed ad (non-Spark) | 9:16 (16:9, 1:1 accepted) | 1080×1920 (min 540×960) | 10 min, 500 MB | 30 | H.264 | ≥516 kbps (aim 8 Mbps) | AAC 128k+ 48kHz |
| Instagram Reels | 9:16 | 1080×1920 (Meta ads guide recommends 1440×2560) | Organic up to 20 min, but Reels over 3 min won't be recommended to new audiences (Instagram Help, help.instagram.com/2720958398006062, as of 2026-11); Reels ads up to 15 min, 4 GB | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| YouTube Shorts | 9:16 or 1:1 | 1080×1920 | 3 min; any square/vertical upload ≤3 min is classified as a Short automatically | 30 / 60 | H.264 | 8–12 Mbps | AAC 384k 48kHz |
| Facebook video | 9:16 or 4:5 | 1080×1920 / 1080×1350 | All Facebook video uploads publish as Reels since 2025; feed ads 1s–241 min, 4 GB | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| IG / FB Stories | 9:16 | 1080×1920 | 60s per card | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| Snapchat | 9:16 | 1080×1920 | 60s (verify Spotlight cap) | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| YouTube long-form | 16:9 | 1920×1080 / 3840×2160 | 12 hr or 256 GB | 30 / 60 | H.264 (or H.265 source) | 8 / 12 Mbps (1080p30/60), 35–45 Mbps (4K30) | AAC 384k 48kHz |
| X | 16:9 or 1:1 | 1280×720+ | 2 min 20 s standard; longer on Premium | 30 / 60 | H.264 | 5–25 Mbps | AAC 128k 48kHz |
| LinkedIn feed | 1:1, 4:5, 16:9, 9:16 | 1080×1080 / 1920×1080 / 1080×1920 | Member posts 15 min, 5 GB; Page and Career Page video 10 min, 5 GB (LinkedIn Help, checked 2026-11-15) | 30 | H.264 | 8–10 Mbps | AAC 128k 48kHz |
| Pinterest video Pin | 9:16 or 2:3 | 1080×1920 | 15 min | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |

### Safe Zones (keep critical text, faces and logos out of these UI bands)

| Platform | Top band | Bottom band | Side bands | Source |
|---|---|---|---|---|
| Meta Reels ads (IG + FB) | 14% (~270 px) | 35% (~672 px) | 6% each (~65 px) | Meta Ads Guide |
| Meta Stories | 14% (~270 px) | 20% (~380 px) | 6% each | Meta Ads Guide |
| TikTok | ~130–160 px | ~350–440 px, grows with caption length | right ~140–200 px (action rail) | download TikTok's official safe-zone template |
| YT Shorts | ~110 px | ~280 px | right ~180 px | approximation; preview on device |
| YT long-form 16:9 | ~60 px | ~100 px (progress bar) | 0 px | approximation |

(Pixels at 1080×1920 or 1920×1080; scale with output resolution. Ads that carry a legal disclaimer on Meta need the bottom 40% clear.) Instagram's profile grid crops covers to 3:4, so keep the cover's subject and title inside the centre 1080×1440.

### Captions / On-Screen Text Rules

- Keep the caption block out of every UI band; never bottom-aligned (bottom is platform UI).
- 9:16 talking head: block centered at about 58% of height (Y≈1110 of 1920), just below the chin and above the bottom band. Never over the face.
- 9:16 product or screen demo with the subject mid-frame: upper third (about 30% of height), still below the top band.
- Font: bold sans (Poppins Black, Montserrat Black, Anton, Inter Black). Caption text roughly 80–110 px at 1080×1920, hook text slightly smaller in a box.
- Stroke + drop shadow: about 8% of font size stroke, soft shadow — preserves readability over any background.
- One sentence per card max. Two-sentence cards get skipped.
- Word-by-word reveal in time with VO is the common preset look; test it against flat full-sentence captions on the account's own data (no measured source). Keep on-screen text at or under 5–10 words per second (TikTok creative guidance).
- Instagram captions hold at most 2,200 characters (official, Meta developer docs, Instagram Graph API media reference). Instagram posts allow at most 5 hashtags (reported, Business Today, 2025-12-19; newer than the API reference, which may lag). Put the hook and topic words in the first line, before the "more" truncation.

### Metadata Limits (verify live)

| Platform | Field | Limit | Source (checked 2026-11-15) |
|---|---|---|---|
| YouTube | Title | 100 characters | [YouTube Help](https://support.google.com/youtube/answer/57404) |
| YouTube | Description | 5,000 characters | [YouTube Help](https://support.google.com/youtube/answer/57404) |
| Instagram | Caption | 2,200 characters; at most 5 hashtags (reported, see References) | [Instagram Graph API](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media) |
| TikTok, Content Posting API | Title (caption) | 2,200 UTF-16 characters | [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post) |

The in-app TikTok caption cap and the Instagram visible-before-"more" length were not confirmed on a primary page; write the hook in the first line and keep the first 125 characters self-contained.

### AI Video Generation Providers

The `video-gen` capability wires one provider; which one depends on the user's config. Agents describe the step by what it does (image-to-video clip, upscale, targeted edit) and read the tool names and limits here. Check the wired tool's own schema before sending a request: the server, or the package version for local servers, decides which model ids it accepts.

| Provider | Wired tools | Models and limits (provider docs, checked 2026-11-15) | Native audio |
|---|---|---|---|
| fal (default) | `search_models`, `get_model_schema`, `get_pricing`, `run_model`, `submit_job`, `check_job`, `get_job_result`, `upload_file` | A catalog of hosted models (Kling, Seedance, Wan, LTX, MiniMax, Gemini Omni). Find one with `search_models`, read its limits with `get_model_schema` and its price with `get_pricing` before running it. | Per model; read the schema |
| Runway | tools of Runway's remote server | `gen4_turbo`: 2–10 s, ratios `1280:720`, `720:1280`, `960:960`, `1104:832`, `832:1104`, `1584:672`; `gen4.5`: same ratios, 2–10 s. Upscale (`magnific_video_upscaler_creative`): input up to 30 s, output up to 4k. Editing (`aleph2`): input up to 30 s. | Not stated for Gen-4 Turbo or Gen-4.5 |
| Kling | tools of Kling's remote server | Not confirmed on Kling's own docs in this pass; read the tool schema. | Read the tool schema |
| Gemini | `generate_video_omni`, `extend_video_omni`, `edit_video`, `get_omni_interaction` | `gemini-omni-1.2-flash`: 3–15 s output, 360p, 720p, 1080p or 4K, 24 fps; extension 3–10 s per turn, up to 30 s total. | Yes |
| Replicate | tools of Replicate's remote server | Any video model hosted on Replicate; read the model's input schema for its limits. | Per model |
| MiniMax Hailuo | `generate_video`, `query_video_generation` | `MiniMax-Hailuo-2.3`: 768P at 6 or 10 s, 1080P at 6 s | Not stated |
| Luma | tools of Luma's remote server | `ray-2` and `ray-flash-2`; resolutions 540p to 4k. Luma's older guide notes current docs are in its Agents API docs. | Not stated |

Sources: [fal MCP server](https://fal.ai/docs/model-apis/mcp), [Runway MCP guide](https://docs.dev.runwayml.com/guides/mcp), [Runway API reference](https://docs.dev.runwayml.com/api.md), [Runway models](https://docs.dev.runwayml.com/guides/models/), [Gemini Omni Flash model page](https://aistudio.google.com/docs/models/gemini-omni-flash), [Replicate MCP server](https://replicate.com/docs/reference/mcp), [MiniMax text-to-video reference](https://platform.minimax.io/docs/api-reference/video-generation-t2v), [Luma video generation](https://docs.lumalabs.ai/docs/video-generation).

### Output Presets (ffmpeg) — copy-paste ready

```bash
# 9:16 — TikTok / Reels / Shorts / Stories
-vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30" \
  -c:v libx264 -profile:v high -level 4.0 -crf 21 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -ac 2 \
  -movflags +faststart

# 1:1 — IG / FB feed
-vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30" \
  -c:v libx264 -profile:v high -crf 21 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -ac 2 -movflags +faststart

# 16:9 — YouTube long-form / LinkedIn
-vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps=30" \
  -c:v libx264 -profile:v high -level 4.2 -crf 19 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart
```

### Workflow

1. Identify primary platform for the brief (TikTok / Reels / Shorts / etc.).
2. Pick aspect, length cap, fps from the table.
3. Mark safe zones when storyboarding — keep face, hook text, CTA inside the center region.
4. At export, use the matching ffmpeg preset above.
5. If publishing to multiple platforms, render the master in the largest aspect (e.g. 9:16 1080×1920 30fps) and downconvert to others — never upscale.

### Decision Guide

| Brief says | Output |
|---|---|
| "TikTok ad" | 9:16, 1080×1920, 30fps, H.264 8 Mbps; length is a creative choice (allowed up to 10 min) |
| "Instagram Reel" | 9:16, 1080×1920, 30fps, ≤3 min when the goal is non-follower discovery (up to 20 min is allowed but mostly reaches followers), H.264 6 Mbps |
| "YouTube Short" | 9:16, 1080×1920, 60fps if motion-heavy else 30, ≤3 min; keep ≤60s if it uses any claimable music |
| "Story (any platform)" | 9:16, 1080×1920, 30fps, ≤60s per card |
| "IG feed" | 4:5, 1080×1350, 30fps |
| "FB feed" | 4:5, 1080×1350 (1:1 also fine), 30fps |
| "YouTube long-form" / "explainer" | 16:9, 1920×1080, 30fps (60fps if screen-cap) |
| "Hero video for landing page" | 16:9, 1920×1080, 30fps, muted, poster frame, MP4 (H.264) + WebM/AV1, short loop under ~5 MB |
| "X post" | 16:9 1280×720 if widescreen, else 1:1 1080×1080 |
| "LinkedIn post" | 1:1 1080×1080 or 4:5 1080×1350 |
| "Pinterest" | 9:16 1080×1920 |

### Disclosure and Rights (2026 — verify live)

Paid-partnership and AI-content disclosure rules per platform and jurisdiction are in the `content-disclosure` skill. Music rights stay here:

| Item | Rule |
|---|---|
| Music | YouTube Shorts over 1 min with any active Content ID claim are blocked worldwide. Business TikTok accounts and all ads use the Commercial Music Library or owned/licensed music; trending sounds are not cleared for brand use. AI music (e.g. ElevenLabs) is commercially usable only on a paid plan per its terms. |

## Examples

### Example 1: TikTok ad export

Source: 4K 16:9 24fps generated clip. Target: TikTok ad.

```bash
ffmpeg -i source.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30" \
  -c:v libx264 -profile:v high -level 4.0 -crf 21 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 128k -ar 48000 -ac 2 \
  -movflags +faststart \
  tiktok-ad-9x16.mp4
```

### Example 2: Cross-platform render plan

Brief: One ad, ship to TikTok + IG Reels + IG feed + YT Shorts + YT long-form trailer.

| Cut | Aspect | Resolution | Length |
|---|---|---|---|
| Master | 9:16 | 1080×1920 | 45s |
| TikTok | 9:16 | 1080×1920 | 45s (master) |
| IG Reels | 9:16 | 1080×1920 | 45s (master) |
| YT Shorts | 9:16 | 1080×1920 | 45s (master, captions repositioned higher) |
| IG feed (1:1 cut-down) | 1:1 | 1080×1080 | 30s (re-edited, key beats only) |
| YT long-form trailer | 16:9 | 1920×1080 | 60s (re-edited, b-roll padded) |

## Checklist

- [ ] Aspect and resolution match the platform row; no platform-side upscaling.
- [ ] Length is under the 2026 cap and the cap was checked live for paid launches.
- [ ] Captions, faces and CTA sit outside every UI band of every placement the cut will run in.
- [ ] H.264 yuv420p, AAC 48 kHz stereo, `+faststart`, about -14 LUFS / -1 dBTP.
- [ ] AI-disclosure and music-rights rows resolved for each platform.

## References

- [TikTok in-feed ad specs](https://ads.tiktok.com/help/article/video-ads-specifications)
- [Instagram Reels ad specs and safe zones](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)
- [YouTube Shorts up to 3 minutes](https://support.google.com/youtube/answer/15424877)
- [YouTube recommended upload encoding settings](https://support.google.com/youtube/answer/1722171)
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)
- [Instagram Reels length (Instagram Help via Socialinsider)](https://www.socialinsider.io/blog/instagram-reels-length/), 2026-07, reported.
- [Meta Reels ads, sound-on share](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads), 2024-11-07, official.
- [Instagram five-hashtag cap (Business Today)](https://www.businesstoday.in/technology/news/story/no-more-hashtag-stuffing-instagram-limits-hashtag-usage-to-just-5-per-reel-and-post-507444-2025-12-19), 2025-12-19, reported.
- [Instagram Graph API: IG User media](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media), official — caption maximum 2,200 characters.
- [TikTok for Business: Kantar report on sound](https://ads.tiktok.com/business/en-US/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok), 2021-06, official — 88% of TikTok users say sound is essential (self-reported).
