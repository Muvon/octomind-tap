---
name: video-ad-production
title: "Short-Form Ad Production: Brief to Platform Render"
description: "Produce a cinematic short-form video ad end to end: script, frames, generated clips, voiceover, music, captions, platform-spec render. Use for ad builds."
license: Apache-2.0
compatibility: "Requires: ffmpeg, auto-editor; provider keys for image and video generation, voice and music; Node.js for the optional Remotion path. macOS/Linux."
capabilities: websearch video-gen voice music composition variety
domains: producer
rules:
  - match((?i)\b(make|produce|create|build|generate|ship|render|develop|need|want)\b.{0,50}\b(\d+[- ]?(second|sec)s?|stories|reels?|tiktok|shorts?|cinematic|product-led|product|video|short-form|promo|vertical)\s+ad\b)
  - match((?i)\b(image[- ]to[- ]video|generated (video |image )?(clips?|shots?)|ai[- ]generated (video|clips?|ad)|slick generated|cheap (draft )?(variants?|drafts?))\b)
  - match((?i)\b(stitch\w*|re-?stitch\w*|upscal\w+)\b.{0,60}\b(shots?|clips?|ad|render|cut)\b)
  - match((?i)\b(fix|repair|regenerate)\b.{0,50}\b(shot|clip|logo|label|cap)\b.{0,80}\b(ad|render|upscal\w+|stitch\w*|final cut)\b)
  - match((?i)\bscript\b.{0,40}\b(final|stitched|platform-spec)\s+render\b|\bstoryboard through\b)
  - semantic(produce a finished 30 second video ad from this brief, 0.76)
  - semantic(build a cinematic product ad from frames to final render, 0.76)
---

## Overview

This skill produces a complete, ready-to-upload cinematic or product-led short-form ad for TikTok, Reels, Shorts, feed and Stories: script, storyboard, generated frames and clips, voiceover, music bed, captions, and a final stitched render at platform spec. It is pragmatic about cost. The wired video-gen tool renders image-to-video clips at roughly 720p, so generate cheap variants, let the user pick winners, and spend extra only on winners: upscale for final resolution, targeted video edit for fixes. Tool names, models and limits per provider are in the `video-spec-sheet` provider table.

It does not cover avatar or UGC-style performance ads (`video-ugc-ads`), long-form explainers (`video-explainers`), or publishing.

## Rules

### Phase 1 — Plan (no generation yet)

1. Intake: product, audience, platform(s), length, awareness stage, offer and CTA, brand voice, banned phrases. Ask for what is missing. Recall brand voice, audience, past ad outcomes, winning hooks, banned phrases from memory.
2. Apply `video-hooks`, `video-spec-sheet` and `ad-frameworks`.
3. Write the script (HSO / PAS / BAB / AIDA per awareness stage) with 3 hook variants and timestamps (`video-script-writing`). Name the share trigger (why a viewer would send this to someone; on Instagram, sends weigh slightly more than likes for reaching non-followers). Reveal the product in the first 3–5 s. Save to `./video-out/<slug>/script.md`.
4. Decompose into beats; save the storyboard to `./video-out/<slug>/storyboard.md` and the asset checklist (`video-storyboarding`).
5. Research only for a new brand or unfamiliar vertical (top-ads teardown via TikTok Creative Center and Meta Ads Library), a hook that needs a verified stat, or a banned-topic check (medical, financial, regulated). One parallel block; ads ship fast, so don't over-research.

### Phase 2 — Frames (parallel)

For each beat, generate one reference frame at the target aspect with `generate_image` (`aspectRatio` 9:16 / 1:1 / 16:9, `fileName` beat-NN.png), all beats in one tool block. Images land in `./image-out/`; move them to `./video-out/<slug>/frames/`. For the product itself, pass the user's real product photos as `inputImagePaths` so the frame keeps its true shape, label and color. Keep ad copy, prices and logos out of generated pixels; set them later as text overlays or captions. Open every frame and look at it before animating: a warped product, stray text, or a frame that misses its beat gets regenerated now, while it is cheap.

### Phase 3 — Clip variants (parallel, cheap-first)

For each beat that needs motion (most of them), generate two clip variants with the video-gen image-to-video tool from `frames/beat-NN.png`, at the ratio matching the cut (the provider table lists the accepted ratio values; 9:16 for vertical):

- Variant A: the storyboard's motion prompt.
- Variant B: an alternative camera move or seed.

Poll the provider's task-status tool until done. Stop after this phase and show the variant grid (a Markdown table linking each clip). Wait for the user to mark winners ("B for beat 02, A for beat 03"); don't auto-pick.

### Phase 4 — Finish winners

For each user-picked winner:

- Upscale with the video-gen upscale tool so the final 1080p encode never upscales 720p source.
- If a winner has one fixable flaw (hand, logo, background), fix it with the video-gen targeted edit tool instead of regenerating.
- Save to `./video-out/<slug>/clips/beat-NN-final.mp4`.

### Phase 5 — Voiceover, music, sound design

- Voiceover via `voice` (ElevenLabs default). One file per beat (`vo/beat-NN.mp3`); splitting per beat makes timing trivial. One voice across all beats unless the script calls for two.
- Music via `music` (ElevenLabs Music, `compose_music`). Generate a track matching the storyboard's music brief (genre, BPM, energy curve, length).
- Sound design: SFX from a local library (`assets/sfx/`) or generate via `text_to_sound_effects`. Whooshes on cuts, a riser at the offer, impact on stat reveals.

### Phase 6 — Stitch and mix

Pick by user preference; default to the lighter ffmpeg path.

- ffmpeg (default): concat the clips, overlay VO, duck the music under the VO with `sidechaincompress`, add SFX, two-pass loudness to -14 LUFS. Take every command from the `video-editing` skill's recipe reference; don't improvise filter graphs or frame-processing code.
- Remotion (`composition`): scaffold with `npx create-video@4.0.538 --yes --blank ./video-out/<slug>/remotion-project`, write one React composition per beat (clips, VO, music, kinetic type), check frames with `npx remotion still`, render with `npx remotion render`. Use it when the brief asks for animated type, motion graphics, or many parallel variants from one template.

### Phase 7 — Captions

Run the `video-captions` pipeline on the stitched, mixed cut: word timestamps of the final audio, proofread against `script.md`, the `pop` preset with the hook text from the script, burned in. On the Remotion path, render captions inside the composition from the `video-captions --remotion` JSON instead.

### Phase 8 — Multi-platform delivery

If the brief covers multiple platforms, render the master once at the largest aspect (typically 9:16 1080×1920) and downconvert per `video-spec-sheet`:

- TikTok, Reels: the 9:16 master (captions already sit inside the Reels safe zone).
- Shorts: the 9:16 master; ≤3 min auto-classifies as a Short. Keep ≤60 s if any music could draw a Content ID claim.
- Stories: first 15 s of the master.
- IG feed (1:1 1080×1080 / 4:5 1080×1350): re-edit, drop b-roll, keep hook and offer; re-caption at this size.
- YouTube long-form trailer (16:9 1920×1080): padded with extra b-roll.

### Phase 9 — Bundle

Final asset tree under `./video-out/<slug>/`: `brief.md`, `script.md`, `storyboard.md`, `asset-checklist.md`, `frames/beat-NN.png`, `clips/beat-NN-final.mp4`, `vo/beat-NN.mp3`, `music/track.mp3`, `sfx/`, `captions/` (`vo.json`, `captions.ass`, `captions.srt`), `cuts/` (`master-9x16.mp4`, `tiktok.mp4`, `reels.mp4`, `shorts.mp4`, `stories-15s.mp4`, `feed-4x5.mp4`, `youtube-16x9.mp4`), and `meta/` (`titles.md`, `descriptions.md` with hashtags, `publish-checklist.md`).

`publish-checklist.md` records, per cut: which beats are AI-generated (frames, clips, voice, music), the disclosure each platform needs (`content-disclosure` skill), the music source and licence, and any claim that needs substantiation. The finished `cuts/` folder is ready for publishing or for the user.

### Cost discipline

- Phase 3 variants only on the provider's cheapest image-to-video model; upscale and edit only user-picked winners; never upscale or edit every variant.
- One voiceover pass per beat; don't regenerate VO unless the script changes.
- Music is one track for the whole ad, not one per beat.
- Transcribe the final VO mix once for captions; don't re-run captions on every draft cut.
- Reference frames are cheap; clip generation is the bill, so be deliberate about clip count.

### Compliance

- Realistic AI footage, cloned voices, AI people and paid partnerships are disclosed at upload per the `content-disclosure` skill. The ffmpeg encode strips C2PA credentials, so platforms will not detect AI content for you. Note each disclosure in `publish-checklist.md`.
- Music for ads comes from the generated track (paid ElevenLabs plan), TikTok's Commercial Music Library, or a licence the user holds, never trending sounds.
- Health, finance and before/after claims need substantiation the user supplies.

### Approval gates

- Show script and storyboard; wait for an explicit "ship it" before any generation call, since generation costs money.
- Wait for the user's variant picks (Phase 3) and for stitch approval after Phase 4 previews.
- A "go fast" request, or an autonomous, non-interactive brief, skips the gates: use the provider's cheapest image-to-video model for all clips, ffmpeg for the stitch, 9:16 only, and list the assumptions in `brief.md`.
- After the bundle, offer variants on a cheaper provider, an alternative framework, more cuts (1:1, 16:9), and a publish handoff.

## Examples

### Example 1: cost

❌ Upscale all 24 variant clips, then ask which ones the user likes.

✅ Show the 24 cheap variants, upscale the 12 the user picked.

### Example 2: text in frames

❌ Prompt the image model for "50% OFF" on the product box.

✅ Generate the box without copy and set the offer as a text overlay or caption.

## Checklist

- [ ] No generation call before script and storyboard approval (unless "go fast" or autonomous).
- [ ] Every reference frame opened and checked before animating.
- [ ] Winners picked by the user, not by the agent; one aspect ratio in the cut.
- [ ] Captions from the `video-captions` command, not frame-by-frame code.
- [ ] Platform-spec encode per `video-spec-sheet` for every cut.
- [ ] AI-disclosure and music-licence lines filled in `publish-checklist.md` for every cut.
- [ ] Everything saved under `./video-out/<slug>/`.

## Composition / References

- `video-hooks`, `ad-frameworks` — script and hook choice.
- `video-script-writing`, `video-storyboarding` — Phase 1 artifacts.
- `video-editing` — stitch, ducking and loudness recipes.
- `video-captions` — captions on the final cut.
- `video-spec-sheet` — provider table, encodes, music rules.
- `content-disclosure` — AI labels and paid-partnership rules.
- `content-voice`, `content-humanize` — brand-voice projects; drafts that sound AI.
