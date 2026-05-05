---
name: video-spec-sheet
title: "Video Spec Sheet — Platform Specs and Safe Zones"
description: "Canonical reference for platform-by-platform video output specs: aspect ratio, length cap, codec, bitrate, frame rate, color, caption style and safe-zone bands. Use when picking output settings, validating an export, or spec-checking before publishing. Covers TikTok, Reels, Shorts, IG/FB feed, Stories, X, LinkedIn — all four format families: short-form vertical, square/feed, long-form 16:9, story 9:16."
license: Apache-2.0
compatibility: "Stack-agnostic. Used by every video agent for output validation. Pairs with skills/video-hooks for content rules."
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

# Video Spec Sheet — Platform Specs and Safe Zones

## Overview

Each social platform has its own combination of aspect ratio, max duration, codec, bitrate, frame rate, and caption / UI safe zones. Getting any of these wrong on the export means the platform will either reject, re-encode (quality drop), or crop your creative. This skill encodes the current 2026 specs as a single-source-of-truth table the agent can extract from per brief.

---

## Instructions

### Core Rules

- **Always pick the platform spec before generating frames** — generation must match the export aspect ratio (don't generate 16:9 then crop to 9:16 unless intentional).
- **Burn captions on top of the base render**, not as a sidecar — sound-off viewing is the default.
- **Respect the safe zone** — keep all critical text and faces away from where the platform's UI sits (top, bottom, right side for TikTok).
- **Final encode in H.264 / yuv420p**, even if the source is HEVC / 10-bit. Universal compatibility beats marginal quality.
- **Audio: AAC stereo, 128 kbps minimum**, 48 kHz sample rate. Mono audio reads as low-quality on most feeds.
- **Loudness: -14 LUFS integrated** (TikTok / IG / YT now normalize to roughly this — overshooting means platform compression hits you).

### Platform Spec Table

| Platform | Aspect | Resolution | Length cap | Frame rate | Codec | Bitrate | Audio |
|---|---|---|---|---|---|---|---|
| **TikTok feed** | 9:16 | 1080×1920 | 60s (organic), 60min (max) | 30 / 60 | H.264 | 8–10 Mbps | AAC 128k 48kHz |
| **Instagram Reels** | 9:16 | 1080×1920 | 90s (organic), 15min (Reels Long) | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |
| **YouTube Shorts** | 9:16 | 1080×1920 | 60s (cap is enforced) | 30 / 60 | H.264 | 8–12 Mbps | AAC 192k 48kHz |
| **IG / FB feed video** | 1:1 or 4:5 | 1080×1080 / 1080×1350 | 60min (FB), 90s organic on Reels | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |
| **IG / FB Stories** | 9:16 | 1080×1920 | 60s per card | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |
| **Snapchat** | 9:16 | 1080×1920 | 60s | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |
| **YouTube long-form** | 16:9 | 1920×1080 (1080p) / 3840×2160 (4K) | 12hr | 30 / 60 | H.264 (or H.265 source) | 8–12 Mbps (1080p) / 35–45 Mbps (4K) | AAC 192k 48kHz |
| **X / Twitter** | 16:9 or 1:1 | 1280×720+ | 140s organic, 10min Premium | 30 / 60 | H.264 | 5–25 Mbps | AAC 128k 48kHz |
| **LinkedIn feed** | 16:9, 1:1, 9:16 | 1920×1080 / 1080×1080 / 1080×1920 | 10min | 30 | H.264 | 8–10 Mbps | AAC 128k 48kHz |
| **Pinterest Idea Pin** | 9:16 | 1080×1920 | 60s | 30 | H.264 | 5–8 Mbps | AAC 128k 48kHz |

### Safe Zones (don't put critical content here)

| Platform | Top reserve | Bottom reserve | Right reserve | Left reserve |
|---|---|---|---|---|
| TikTok | 130 px | 350 px (caption + buttons) | 200 px (action rail) | 0 px |
| IG Reels | 200 px (header) | 360 px (caption + reel CTA) | 100 px | 0 px |
| YT Shorts | 110 px | 280 px | 180 px | 0 px |
| IG Stories | 250 px (DM bar) | 250 px (Send to / Reactions) | 0 px | 0 px |
| FB Reels | 200 px | 350 px | 120 px | 0 px |
| YT long-form 16:9 | 60 px | 100 px (progress bar) | 0 px | 0 px |

(All measured at 1080×1920 or 1920×1080. Scale with output resolution.)

### Captions / On-Screen Text Rules

- **Center caption block**, never bottom-aligned (bottom is platform UI).
- **For 9:16**: caption block sits roughly in the upper-center third (between Y=600 and Y=1200 of 1080×1920) — avoids both header and CTA bar.
- **Font**: bold sans (Inter Bold, Helvetica Black, SF Pro Display Bold, Montserrat Black). 80–110 pt for headline hooks at 1080×1920.
- **Stroke + drop shadow**: 2 px stroke, 1 px shadow, opacity 0.6 — preserves readability over any background.
- **One sentence per card max**. Two-sentence cards get skipped.
- **Word-by-word reveal in time with VO** outperforms full-sentence flat captions on TikTok / Reels.

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

1. **Identify primary platform** for the brief (TikTok / Reels / Shorts / etc.).
2. **Pick aspect, length cap, fps** from the table.
3. **Mark safe zones** when storyboarding — keep face, hook text, CTA inside the center region.
4. **At export, use the matching ffmpeg preset** above.
5. **If publishing to multiple platforms**, render the master in the *largest* aspect (e.g. 9:16 1080×1920 30fps) and downconvert to others — never upscale.

### Decision Guide

| Brief says | Output |
|---|---|
| "TikTok ad" | 9:16, 1080×1920, 30fps, ≤60s, H.264 8 Mbps |
| "Instagram Reel" | 9:16, 1080×1920, 30fps, ≤90s, H.264 6 Mbps |
| "YouTube Short" | 9:16, 1080×1920, 60fps if motion-heavy else 30, ≤60s, H.264 10 Mbps |
| "Story (any platform)" | 9:16, 1080×1920, 30fps, ≤15s per card |
| "IG feed" | 4:5, 1080×1350, 30fps |
| "FB feed" | 1:1, 1080×1080, 30fps |
| "YouTube long-form" / "explainer" | 16:9, 1920×1080, 30fps (60fps if screen-cap) |
| "Hero video for landing page" | 16:9, 1920×1080, 30fps, mute by default, MP4 + WebM |
| "X / Twitter post" | 16:9 1280×720 if widescreen, else 1:1 1080×1080 |
| "LinkedIn post" | 1:1 1080×1080 (preferred) or 16:9 1920×1080 |
| "Pinterest" | 9:16 1080×1920 |

---

## Examples

### Example 1: TikTok ad export

Source: 4K 16:9 24fps generated at Veo. Target: TikTok ad.

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

---

## References

- [TikTok video specs](https://support.tiktok.com/en/using-tiktok/creating-videos)
- [Instagram Reels specs](https://help.instagram.com/270447560766967)
- [YouTube Shorts specs](https://support.google.com/youtube/answer/12340300)
- [Meta Ads guidelines](https://www.facebook.com/business/ads-guide)
