---
name: content-distribute
title: "Content Distribution: Publish and Report"
description: "Publish approved content to YouTube, Instagram, TikTok, and X with platform-native metadata, then report results against baselines. Use after approval."
license: Apache-2.0
compatibility: "Needs the connected publishing tools for YouTube, Instagram, TikTok, and X, and the user's approval of the content and the publish plan."
capabilities: publish-youtube publish-instagram publish-tiktok publish-x stock image-gen variety
domains: writer
rules:
  - match((?i)\b(publish|schedule|upload|package|packaging)\b.{0,80}\b(youtube|instagram|tiktok|reels?|shorts|twitter|x)\b)
  - match((?i)\b(approved|finished|signed[- ]off|final)\b.{0,60}\b(video|clip|clips|content|reel|short|footage|cut)\b)
  - match((?i)\b(thumbnail|content\s+calendar|platform[- ]fit|aspect\s+ratio)\b)
  - match((?i)\b(readout|how\s+did)\b.{0,80}\b(posts?|videos?|release|reels?|published|uploads?)\b|\bcompared\s+(with|to)\s+(normal|baseline|usual)\b|\bversus\s+.{0,20}baseline\b)
  - match((?i)\b(performance|results)\s+(readout|report)\b)
  - semantic(publish this approved video to YouTube and TikTok, 0.72)
  - semantic(how did last week's posts perform, 0.72)
  - semantic(schedule and publish my approved posts across social platforms, 0.72)
  - semantic(write metadata and titles for uploading this video to every platform, 0.72)
  - semantic(compare this month's post results against our usual numbers, 0.72)
---

## Overview

Take finished, approved content and run the publishing loop: platform-fit checks, per-platform metadata and packaging, scheduled publication, and a performance readout that feeds the next round. The outcome is content live on the chosen platforms with verified status, and a readout against the account's own baseline. This skill operates after the creative work is done; it does not write posts or captions from scratch, produce or edit video or image assets, manage community replies, or run paid promotion.

## Rules

### Workflow

1. Intake. Identify the assets, the target platforms, and the approval state. Unapproved content stops here.
2. Fit check. Verify each target's constraints (duration, aspect ratio, file format) and flag anything the platform will reject or crop badly. Name the exact constraint violated and the smallest fix; don't publish a known-bad upload.
3. Package per platform with platform-native metadata, aspect ratio, and pacing, never one blob cross-posted, using the conventions below.
4. Confirm. Present the publish plan (asset, platform, metadata, time) and wait for the explicit go.
5. Publish through the platform tools. Verify each publish call's response and report the live status per platform.
6. Read out. On request or on a later pass, pull performance (views, engagement), compare it with the account's baseline from memory, and state one concrete takeaway per post.
7. Memorize the publish history (what, where, when) and durable performance patterns (formats and hooks that outperform for this account).

### Platform conventions

- YouTube (Help Center): put the one or two main keywords in both title and description. Titles cap at 100 characters, so keep the promise in the first 60 or so that survive truncation. Write a unique description per video with the hook and link before "Show more". Tags are a minor signal. Thumbnail and title make one promise the video keeps.
- Instagram: Reels over stills for reach. The caption's first line is the hook; the rest folds. Captions are capped at 5 hashtags (rolling out since December 2025); hashtags help search, not reach (Mosseri). Originality matters: accounts primarily posting unoriginal content lose recommendations, and non-Meta watermarks are flagged at upload, so re-render instead.
- TikTok API publishing (official developer rules): the publish flow must show the creator's nickname, let the creator pick privacy status with no pre-selected default, set interaction settings, and display the Music Usage Confirmation. Commercial-content and AI-label settings follow the `content-disclosure` skill. Unaudited API clients can only post SELF_ONLY to private accounts; never claim such a post went public.
- X (Twitter): standard accounts are capped at 280 characters per post. A thread is a reply chain: post the first tweet, then create each following segment as a reply to the previous one's returned id, verifying each segment landed before posting the next.
- Short-form on all platforms: vertical 9:16, a hook in the first 1 to 3 seconds, text overlays burned in because most mobile viewing is sound-off.
- Scheduling: consistency beats timing tricks; publish when the account's audience is active per the memory baseline.
- At most one clear call to action per post.

### Reporting and safety

- Performance readouts compare with the account's own baseline, not absolute numbers. A takeaway names what to repeat or drop, not vanity metrics.
- Report failed publish calls with the platform's error verbatim. Never silently retry into duplicates: check the status before any retry. Record per-platform post IDs and permalinks against the source asset so performance stays attributable.
- Disclosure: paid-partnership and AI-content labels are separate checks. Run both through the `content-disclosure` skill before the publish plan and flag any open item in the plan.
- Flag platform-policy risks (music rights, disclosure requirements) before publishing, not after.
- Don't fabricate performance numbers. Report only what the tools return and say when metrics are unavailable.
- Never publish without an explicit go on the presented plan. Never publish unapproved or draft content. Never re-run a publish call without checking whether the first one landed.
- Asked to write the post itself: produce only placeholder metadata; the copy comes from the social writing skill (`content-social`).

### Interaction

- "Publish this to <platforms>": fit check, packaging, publish plan, wait for the go.
- "Go" or an approval: execute, verify per platform, report live links and status.
- "How did last week's posts do?": performance readout against baseline with takeaways.

## Output format

- Publish plan as a table: asset, platform, title or caption (first line), scheduled time, status. Metadata drafts per platform in fenced blocks.
- Performance readout: per post, platform, key metrics against baseline, and one takeaway line.

## Checklist

- [ ] The content is approved and the plan carries the user's explicit go.
- [ ] Every target passed the fit check; metadata is platform-native.
- [ ] Paid-partnership and AI-content disclosure checks are done.
- [ ] Each publish response was verified; post IDs and permalinks recorded.
- [ ] Readouts use the account's baseline and only returned numbers.

## Composition / References

- `content-disclosure` (paid-partnership and AI labels), `content-social` (the copy that gets published), `video-hooks` (what to repeat from a retention review).
