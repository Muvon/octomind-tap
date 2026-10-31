---
name: video-spec-sheet
title: "Video Spec Sheet: Platform Specs and Safe Zones"
description: "Canonical reference for platform-by-platform video output specs: aspect ratio, length cap, codec, bitrate, frame rate, color, caption style and safe-zone bands. Per-platform spec table covers TikTok, Reels, Shorts, IG/FB feed, Stories, Snapchat, YouTube long-form, X, LinkedIn, and Pinterest, plus safe-zone reserves, caption rules, and copy-paste ffmpeg presets. Use when picking output settings, validating an export, or spec-checking before publishing."
license: Apache-2.0
compatibility: "Stack-agnostic."
domains: video
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
- AI-generated clips usually come out at 720p (Runway Gen-4 Turbo renders 1280×720 / 720×1280). Upscale picked shots before the final 1080p encode; never let the platform upscale.
- Re-encoding with ffmpeg drops any C2PA Content Credentials the generator embedded, so platform auto-labelling of AI content will not fire. Disclose manually at upload (see Disclosure and Rights).

### Platform Spec Table (2026 — verify live)

| Platform | Aspect | Resolution | Length cap | Frame rate | Codec | Bitrate | Audio |
|---|---|---|---|---|---|---|---|
| TikTok organic | 9:16 | 1080×1920 | 10 min recorded in-app, 60 min uploaded | 30 / 60 | H.264 | 8–10 Mbps | AAC 128k+ 48kHz |
| TikTok in-feed ad (non-Spark) | 9:16 (16:9, 1:1 accepted) | 1080×1920 (min 540×960) | 10 min, 500 MB | 30 | H.264 | ≥516 kbps (aim 8 Mbps) | AAC 128k+ 48kHz |
| Instagram Reels | 9:16 | 1080×1920 (Meta ads guide recommends 1440×2560) | Organic up to 20 min since late 2025, but Reels over 3 min aren't recommended to non-followers (reported, Instagram Help via Socialinsider, 2026-07); Reels ads up to 15 min, 4 GB | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| YouTube Shorts | 9:16 or 1:1 | 1080×1920 | 3 min; any square/vertical upload ≤3 min is classified as a Short automatically | 30 / 60 | H.264 | 8–12 Mbps | AAC 384k 48kHz |
| Facebook video | 9:16 or 4:5 | 1080×1920 / 1080×1350 | All Facebook video uploads publish as Reels since 2025; feed ads 1s–241 min, 4 GB | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| IG / FB Stories | 9:16 | 1080×1920 | 60s per card | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| Snapchat | 9:16 | 1080×1920 | 60s (verify Spotlight cap) | 30 | H.264 | 5–8 Mbps | AAC 128k+ 48kHz |
| YouTube long-form | 16:9 | 1920×1080 / 3840×2160 | 12 hr or 256 GB | 30 / 60 | H.264 (or H.265 source) | 8 / 12 Mbps (1080p30/60), 35–45 Mbps (4K30) | AAC 384k 48kHz |
| X | 16:9 or 1:1 | 1280×720+ | 2 min 20 s standard; longer on Premium | 30 / 60 | H.264 | 5–25 Mbps | AAC 128k 48kHz |
| LinkedIn feed | 1:1, 4:5, 16:9, 9:16 | 1080×1080 / 1920×1080 / 1080×1920 | 15 min desktop upload, 10 min mobile | 30 | H.264 | 8–10 Mbps | AAC 128k 48kHz |
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

| Item | Rule |
|---|---|
| YouTube | Turn on "altered or synthetic content" in Studio when realistic AI makes a real person say/do something, alters a real event or place, or shows a realistic scene that never happened. Not needed for clearly unrealistic/animated content or AI used only for scripts, captions, production help. |
| TikTok organic | Use the AI-generated content label (API field `is_aigc`) for realistic AI content; unlabelled realistic AI content can be removed. Paid partnerships and own-brand promotion need the commercial content toggles. |
| TikTok ads | Ads Manager's AI-generated content disclaimer is mandatory for AI-generated or AI-significantly-altered images, video or audio; undisclosed ads are rejected or restricted. |
| Meta | Meta auto-applies "AI info" when it detects C2PA/IPTC signals or its own gen-AI tools; political and social-issue ads must self-disclose photorealistic AI. |
| EU | AI Act Art. 50(4): deepfake content shown to EU audiences must be disclosed as AI-generated or manipulated from 2 Aug 2026. |
| New York | GBL § 396-b (in force 9 Jun 2026): ads that include a synthetic performer (an AI-generated person not recognizable as a real individual, e.g. an AI avatar presenter) must conspicuously disclose it when the advertiser knows. $1,000 first violation, $5,000 each after. Audio-only ads and AI used solely to translate a human performer are not covered. |
| Music | YouTube Shorts over 1 min with any active Content ID claim are blocked worldwide. Business TikTok accounts and all ads use the Commercial Music Library or owned/licensed music; trending sounds are not cleared for brand use. AI music (e.g. ElevenLabs) is commercially usable only on a paid plan per its terms. |

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

## Checklist

- [ ] Aspect and resolution match the platform row; no platform-side upscaling.
- [ ] Length is under the 2026 cap and the cap was checked live for paid launches.
- [ ] Captions, faces and CTA sit outside every UI band of every placement the cut will run in.
- [ ] H.264 yuv420p, AAC 48 kHz stereo, `+faststart`, about -14 LUFS / -1 dBTP.
- [ ] AI-disclosure and music-rights rows resolved for each platform.

## References

- [TikTok in-feed ad specs](https://ads.tiktok.com/help/article/video-ads-specifications)
- [TikTok ad disclaimers (AI-generated content)](https://ads.tiktok.com/help/article/about-ad-disclaimers-in-tiktok-ads-manager)
- [Instagram Reels ad specs and safe zones](https://www.facebook.com/business/ads-guide/update/video/instagram-reels)
- [YouTube Shorts up to 3 minutes](https://support.google.com/youtube/answer/15424877)
- [YouTube recommended upload encoding settings](https://support.google.com/youtube/answer/1722171)
- [YouTube altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491)
- [Meta Ads Guide](https://www.facebook.com/business/ads-guide)
- [New York synthetic performer ad disclosure, GBL § 396-b (Cooley summary)](https://www.cooley.com/news/insight/2026/2026-01-29-new-york-enacts-synthetic-performer-disclosure-law-for-advertisements-including-those-using-generative-ai)
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices)
- [Instagram Reels length (Instagram Help via Socialinsider)](https://www.socialinsider.io/blog/instagram-reels-length/), 2026-07, reported.
- [Meta Reels ads, sound-on share](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads), 2024-11-07, official.
- [Instagram five-hashtag cap (Business Today)](https://www.businesstoday.in/technology/news/story/no-more-hashtag-stuffing-instagram-limits-hashtag-usage-to-just-5-per-reel-and-post-507444-2025-12-19), 2025-12-19, reported.
- [Instagram Graph API: IG User media](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media), official — caption maximum 2,200 characters.
- [TikTok for Business: Kantar report on sound](https://ads.tiktok.com/business/en-US/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok), 2021-06, official — 88% of TikTok users say sound is essential (self-reported).
