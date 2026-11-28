---
name: video-publishing
title: "Video Publishing: TikTok, Instagram, YouTube Uploads"
description: "Publish finished video cuts to TikTok, Instagram and YouTube: spec validation, compliance checks, per-platform metadata, scheduling, publish report."
license: Apache-2.0
compatibility: "Requires: ffprobe; an Upload-Post profile for TikTok and YouTube, an Instagram Graph API token and a public HTTPS media bucket. macOS/Linux."
capabilities: publish-tiktok publish-instagram publish-youtube
domains: producer
rules:
  - match((?i)\b(publish|upload|post|schedule|distribute|ship|put|go)\b.{0,80}\b(to|on)\s+(tiktok|instagram|youtube|reels|shorts|ig|meta)\b)
  - match((?i)\b(publish|upload|post|schedule|distribute)\b.{0,30}\b(this|the|my|these|them|finished|final|approved|new)\b.{0,30}\b(video|cuts?|reels?|shorts?|clips?|ad|explainer)\b)
  - match((?i)\b(pre-upload|publish(ing)? (report|plan)|go(es)? live|went live|are live|poll\w*\b.{0,30}\b(status|upload\w*)|upload\w*\b.{0,30}\b(flagged|rejected|removed))\b)
  - match((?i)\b(per-platform|platform-compliant|each platform'?s?)\b.{0,50}\b(metadata|captions?|limits?|hashtags?|descriptions?|titles?)\b)
  - match((?i)\b(check|validate|audit|meets?)\b.{0,70}\b(requirements?|limits?|specs?|rules|policy|disclosures?)\b.{0,50}\b(tiktok|reels?|shorts|youtube|instagram|platforms?)\b)
  - semantic(upload this finished video to TikTok and YouTube with the right captions, 0.76)
  - semantic(check this video meets platform specs and write per-platform metadata, 0.73)
---

## Overview

This skill ships a finished asset bundle (the cuts, metadata and publish checklist from a produced ad, UGC ad, explainer, edit or clip set, with thumbnails where relevant) to the requested platforms: TikTok, Instagram (Reels, feed, Stories) and YouTube (Shorts, long-form). It validates specs, checks compliance, adapts the metadata file to each platform's constraints, uploads, polls status, and writes a report. It does not generate or edit media, write creative copy from scratch, or fix failed cuts; a wrong-aspect upload, a banned hashtag or a re-used flagged audio track wastes the whole creative pipeline, so check before posting.

## Rules

### Approval

Upload only after the user has approved the platforms, the adapted metadata and the compliance results. An autonomous, non-interactive brief that names the platforms and authorizes publishing uses the defaults, uploads, and lists assumptions in the report.

### Phase 1 — Intake and spec validation

1. Confirm the bundle has the cuts to ship (`tiktok.mp4`, `reels.mp4`, `shorts.mp4`, `feed-4x5.mp4`, `youtube-16x9.mp4`, `stories-15s.mp4`, whichever are required) plus `meta/publish-checklist.md` (AI-generated assets, music source, paid relationships) and, for YouTube long-form, a thumbnail in `./video-out/<slug>/thumbs/`. Recall the Upload-Post profile, cross-post defaults, preferred posting times, compliance flags and past rejections from memory.
2. For each cut, validate against `video-spec-sheet`, reading real values with `ffprobe -v error -show_entries stream=codec_name,width,height,pix_fmt:format=duration -of json <cut>`: aspect ratio matches the platform, duration is within the platform cap, H.264 yuv420p with AAC audio, resolution at or above the minimum.
3. If any cut fails validation, stop; don't auto-fix. Report the failure and send the user back to the producer of the cut.
4. A missing required cut for a target platform: stop and list the missing file. A missing YouTube thumbnail: ask for one (see `video-thumbnails`) before a long-form upload.

### Phase 2 — Compliance check

For each platform, run these checks before upload (2026 rules, which change often; `content-disclosure` holds the paid-partnership and AI-label rules, `video-spec-sheet` the music rules and metadata limits):

| Platform | Check |
|---|---|
| All | AI label and paid-partnership disclosure per `content-disclosure`, for every platform in the run. No medical or financial guarantees or unsubstantiated claims. No engagement-bait CTAs or captions ("like/follow to…"); TikTok keeps them out of For You. |
| TikTok | Business accounts may only use Commercial Music Library or owned/licensed audio. |
| Instagram (Reels / feed) | Licensed or original audio only. No TikTok / YouTube watermarks. Max 5 hashtags. |
| YouTube (Shorts) | 9:16 or 1:1, ≤3 min (classified as a Short automatically; `#shorts` is optional). A Short over 1 min with any active Content ID claim is blocked worldwide, so clear the music first. |
| YouTube (all) | Long-form: custom thumbnail, chapters if ≥4 sections (first at 0:00, at least 3, each ≥10 s), licensed b-roll only. |

If any check fails, surface the specific blocker (claim, hashtag, music) to the user. Don't soften or rewrite copy to get through compliance without explicit approval, and don't strip captions to "make it work".

### Phase 3 — Metadata adaptation

Read `./video-out/<slug>/meta/` if present, otherwise ask. Adapt to each platform's constraints; copy is a creative decision, so truncating to the platform maximum is the only edit you make on your own.

- TikTok: no title; caption within the Content Posting API limit in the `video-spec-sheet` metadata table, front-load the first line (only one or two lines show before "more"); 3–5 niche tags.
- Instagram Reels: no title; caption and hashtag limits from the `video-spec-sheet` metadata table (only the first ~125 characters show before "more"); cover readable in the 3:4 grid crop; audio attribution if remixing.
- Instagram feed: the same, aspect 4:5 (or 1:1).
- YouTube Shorts: title and description within the `video-spec-sheet` metadata table; ≤3 hashtags shown above the title, more than 15 and all are ignored; `#shorts` optional; custom thumbnail (YPP); group related Shorts in a Series.
- YouTube long-form: title (front-load the keyword) and description within the same table; same hashtags; add chapters, end-screen and a custom thumbnail.

Packaging: captions and on-screen keyword text use the literal words viewers search, not clever phrasing. Flag a cut with no keyword text rather than rewriting it. For posting cadence and search or indexing guidance use the `social-tiktok` and `social-instagram` skills; for cross-post copy beyond these three platforms use `social-x`, `social-bluesky` or `social-linkedin`.

Save adapted metadata to `./video-out/<slug>/meta/<platform>-final.md` per platform.

### Phase 4 — Upload

One platform at a time, never in parallel: parallel uploads race in metadata APIs and risk partial failure. Upload only to platforms the brief named. Never re-publish a failed upload silently; surface the error. Never publish publicly when a required AI label or paid-partnership disclosure couldn't be set: hold it private and tell the user. The source bundle in `./video-out/<slug>/cuts/` is read-only.

#### TikTok via `publish-tiktok`

1. `upload_video` with `user` (the Upload-Post profile), `platforms: ["tiktok"]`, `videoPathOrUrl` (absolute path of the cut), the adapted caption as `title`, and `platformOptions` for privacy level, the AI-generated content flag, and the commercial-content toggles the checklist calls for. If an option isn't accepted, publish private and ask the user to set it in the app before going public.
2. Poll `get_status` / `get_job_status` until published or a terminal failure. Manage scheduled posts with `list_scheduled` / `edit_scheduled` / `cancel_scheduled`.

#### Instagram via `publish-instagram`

1. Upload the cut to a public HTTPS URL (the user provides a bucket; don't assume one). If no bucket is configured, stop and ask.
2. `validate_access_token`, then check `get_content_publishing_limit` before posting.
3. For organic hook or concept tests, use Instagram Trial Reels: shown to non-followers first, auto-shared to followers based on the first 72 h. Test distinct concepts, not only hook swaps. If the provider doesn't expose Trial Reels, ask the user to set it in the app.
4. `publish_reel` (or `publish_media` for feed video / `publish_carousel`) with the URL and caption.

#### YouTube via `publish-youtube`

Uploads go through the same Upload-Post profile as TikTok (the channel is connected once in the Upload-Post dashboard).

1. Stage local files that need a URL (thumbnail, `.srt` captions): `create_media_upload` (filename, contentType, contentLength from `stat`, mediaType) → `curl -sS -X PUT -H "Content-Type: <type>" --data-binary @<file> "<upload_url>"` → `complete_media_upload` → use the returned `media_url`.
2. `upload_video` with `user`, `platforms: ["youtube"]`, `videoPathOrUrl` (absolute path), the adapted `title` and `description` (chapters included for long-form), `scheduledDate` + `timezone` when scheduling, and `platformOptions`: `youtubePrivacyStatus`, `youtubeTags`, `youtubeCategoryId`, `youtubeThumbnailUrl`, `youtubePlaylistId`, `youtubeContainsSyntheticMedia` (realistic AI), `youtubeHasPaidProductPlacement` (sponsored), `youtubeSelfDeclaredMadeForKids` (false unless the brief says the video is for kids).
3. Poll `get_status` until the video URL comes back.
4. Ask the user to confirm in YouTube Studio that the thumbnail, captions and disclosure settings applied; until confirmed, report them as requested, not verified. Custom Shorts thumbnails and Test & Compare variants are set in desktop Studio: hand over the variant files (`thumbs/a.jpg`, `b.jpg`, `c.jpg`) with that instruction.

#### Scheduling

Use platform-native scheduling (`upload_video` with `scheduledDate` + `timezone` for TikTok and YouTube, IG `scheduled_publish_time` if the provider exposes it); never simulate scheduling on your side.

### Phase 5 — Report

Save `./video-out/<slug>/publish-report.md`: a table with one row per platform and columns Platform, Status (published / scheduled), URL, Posted at, Notes (e.g. container id, caption truncated to 2200, `publishAt` set), headed by the slug and date. Record platform reject reasons, working caption patterns and posting windows that performed in memory.

### Phase 6 — Retention review (24–72 h after posting)

When the user brings numbers back, run the retention review in the `video-hooks` skill per post, hand the re-cut or re-hook brief to the editing step (`video-editing` or `video-clips`), and record what worked in memory. Never delete and re-upload a flopping Short.

## Examples

### Example 1: failing spec

❌ A 16:9 cut for TikTok gets cropped by the publisher and uploaded.

✅ Stop, report "tiktok.mp4 is 1920×1080; 9:16 required", and return it to the producer.

### Example 2: missing disclosure option

❌ The AI-generated flag isn't accepted by the provider, so the video goes public anyway.

✅ Publish private, tell the user which setting to flip in the app, and report the post as held.

## Checklist

- [ ] Every cut probed with `ffprobe` and matched to its platform spec.
- [ ] Compliance table run for every platform; blockers shown, not softened.
- [ ] Metadata adapted per platform and saved to `meta/<platform>-final.md`.
- [ ] AI label and paid-partnership disclosures set, or the post held private.
- [ ] Uploads run sequentially, only to the named platforms.
- [ ] Status polled to a terminal state; errors surfaced.
- [ ] `publish-report.md` written; Studio-side settings reported as requested until confirmed.

## Composition / References

- `video-spec-sheet` — specs, music rules, metadata limits.
- `content-disclosure` — AI labels and paid-partnership rules.
- `video-hooks` — retention review after posting.
- `video-thumbnails` — YouTube thumbnails and covers.
- `social-tiktok`, `social-instagram`, `social-x`, `social-bluesky`, `social-linkedin` — cadence, indexing and cross-post copy.
