---
name: video-ugc-ads
title: "UGC Avatar Ads: Talking-Head Performance Creative"
description: "Produce avatar talking-head UGC ads for Meta and TikTok: persona, HeyGen render, voice, lipsync, b-roll, 3-5 hook variants, disclosures. Use for UGC ads."
license: Apache-2.0
compatibility: "Requires: ffmpeg, auto-editor; HeyGen, ElevenLabs and optional Sync.so keys; Node.js for the optional Remotion path. macOS/Linux."
capabilities: video-gen voice avatar lipsync music stock composition variety
domains: producer
rules:
  - match((?i)\bugc\s+(ads?|videos?|creatives?|style|content)\b)
  - match((?i)\b(ai\s+)?avatars?\b.{0,40}\b(ads?|videos?|talking[- ]head|spokesperson|presenter)\b)
  - match((?i)\b(heygen|lip-?sync|sync\.so)\b)
  - match((?i)\bcreator[- ]style\b.{0,30}\b(ads?|videos?)\b)
  - semantic(make a talking head ad with an AI presenter that looks like a creator filmed it, 0.74)
  - semantic(write a creator style script for an avatar ad with disclosure, 0.72)
---

## Overview

This skill produces avatar-driven talking-head ads that perform on Meta Ads Manager and TikTok Ads Manager and can scale to thousands of dollars of spend before fatigue. It composes `avatar`, `voice`, `lipsync`, b-roll cutaways and burned captions into one deliverable.

UGC-style means it looks like a creator filmed it on a phone: hand-held framing, single light, casual room. Imperfection beats polish. The style is allowed; deception is not. An AI avatar is a presenter for the brand, never a real customer recounting an experience that didn't happen.

It does not cover polished cinematic ads (`video-ad-production`), long-form explainers, or publishing.

## Rules

### Phase 1 — Persona and script

1. Apply `video-hooks`, `video-spec-sheet` and `ad-frameworks` (HSO for cold audiences, PAS for problem-aware). Recall persona, avatar id, voice id, winning hooks, banned claims and consent on file from memory.
2. Define one persona: name, age range, tone, accent, look. Use the `content-voice` skill when the persona needs a defined tone.
3. Pick the avatar (browse with `get_avatar_groups` / `get_avatars_in_avatar_group`):
   - Photoreal, off-the-shelf: a HeyGen public avatar.
   - Photoreal, brand-specific: a photo avatar the user already created in their HeyGen account from a single photo (founder, employee, paid model release); no creation tool is wired.
   - Stylized, illustrated or non-human: not covered by the wired provider; say so and offer the closest HeyGen avatar.
4. Pick the voice:
   - Avatar lines: a HeyGen voice from `get_voices` (the render needs a HeyGen voice ID).
   - Narration over cutaways: an ElevenLabs voice via `search_voices`.
   - Cloned founder or employee: ElevenLabs `voice_clone` (consent on file).
   - Localized: the ElevenLabs multilingual model.
5. Before writing, name the share trigger (why viewers send it on; Instagram weighs sends over likes for non-follower reach), reveal the product in the first 3–5 s, and decide the ending: a paid ad closes on a held CTA card (`video-editing`, Ending row); an organic cut ends right after the payoff, loop-friendly (`video-hooks`, "Endings and loops"). Script: hook and last line first, 3 hook variants, one body. The avatar speaks as a presenter ("here's what this does"), not a fictional buyer ("I tried this and lost 10 lbs"). First-person results only when voicing a real, documented customer review the user may use, with typical results stated. Strip AI cadence from VO scripts with the `content-humanize` skill. Save to `./video-out/<slug>/script.md`.
6. Storyboard, marking avatar shots (talking head), cutaway shots (product, b-roll, screen-cap) and on-screen text cards.

### Phase 2 — Avatar renders

For each hook variant and body combination, generate avatar video via `avatar` (`generate_avatar_video` with avatar_id, voice_id and script; poll `get_avatar_video_status`) and save to `./video-out/<slug>/avatar/<variant>-body.mp4`. Render the picked variants in parallel. With a photo avatar, confirm it exists in the account (`get_avatars_in_avatar_group`) and that consent is on file before the first render.

### Phase 3 — B-roll cutaways

Cutaways punch up retention; about 30–40% of total runtime should be cutaways, and the avatar stays in frame for most of the runtime.

1. Real product footage first: clips or photos the user supplies of the product in hand and in use. Generated video still gets intricate products and hand interaction wrong, so real footage under an AI presenter beats a fully generated ad.
2. Product shots when no real footage exists: `generate_image` with the user's real product photos as `inputImagePaths` (keeps shape, label, color); images land in `./image-out/`. Set on-screen copy as text overlays, not generated pixels.
3. Lifestyle b-roll: Pexels stock first (free); generate via `video-gen` (image-to-video; limits per provider in `video-spec-sheet`) only when stock can't deliver.
4. Screen-cap: if the product is software, the user records once; you stitch.

Save cutaways to `./video-out/<slug>/cutaways/`.

### Phase 4 — Lipsync polish (optional)

If the avatar's lipsync looks soft (HeyGen sometimes drifts on consonant-heavy lines), run the cut through `lipsync` (Sync.so). Pricing is per second: run it only on the finished, picked variant, never on rejects, and tell the user the cost first.

### Phase 5 — Voice and audio bed

1. Pre-render voiceover in `voice` (ElevenLabs) per beat, for any non-avatar narration over cutaways.
2. Generate or pick a low-key bed via `music` (ElevenLabs Music). UGC ads typically run muted music or none; don't fight the voice.
3. Sound design stays minimal. UGC reads as authentic when it sounds like a phone-recorded clip.

### Phase 6 — Stitch and variant scaling

1. Compose avatar, cutaways and audio bed with the cutaway, ducking and loudness commands from the `video-editing` recipe reference (ffmpeg via the shell). Don't improvise filter graphs or frame-processing code.
2. Use Remotion (`npx create-video@4.0.538 --yes --blank`, `npx remotion render`) when generating 10 or more templated variants from the same hook and body skeleton.
3. Ship 3–5 hook variants of one body: same avatar, different first 1.5 s. Hook swaps iterate one creative; ad fatigue also needs distinct concepts.

### Phase 7 — Captions

Burn captions on every final cut as support: audio is primary (over 75% of Reels views are sound-on, per Meta), so voice and mix carry the ad. Use the `video-captions` pipeline: word timestamps of the final mix, proofread against `script.md`, `pop` preset, hook text from the script. Keep the caption block below the avatar's chin (the preset default) and inside the safe zone, never over the face.

### Phase 8 — Bundle for ad platforms

```
./video-out/<slug>/
  ads/        variant-A-9x16.mp4, variant-B-9x16.mp4, variant-C-9x16.mp4,
              variant-A-1x1.mp4 (FB feed), variant-A-4x5.mp4 (IG feed)
  meta/       primary-text.md (per variant; front-load ~125 chars, verify per placement)
              headlines.md (≤27 chars for Facebook feed)
              disclosures.md (AI-generated content disclaimer on, any paid-creator disclosure, claims substantiation)
              landing-utms.md (UTM-tagged URLs per variant)
  ads-library-checklist.md
```

### UGC performance rules

- First 1.5 s is the avatar speaking the hook, not a logo or stock cutaway.
- One creator across all variants in a campaign; mixing creators reads as branded.
- No music duck on the avatar's voice. Music sits at -18 dB or off.
- Captions inside the safe zone: Meta Reels keeps the top 14%, bottom 35% and 6% sides clear (see `video-spec-sheet`).
- Length: 15–30 s is the usual starting range for paid UGC; let the account's hook and hold rates decide. Both platforms accept far longer ads.
- Test hook variants in Meta Ads Manager, one ad set per hook.

### Compliance (2026, verify live)

- Fake-review and testimonial rules, AI-generated testimonials included: see the `content-disclosure` skill. The Endorsement Guides treat virtual influencers as endorsers.
- AI avatars and synthetic voices, paid or branded posts, EU audiences and New York ads with a synthetic performer: follow the `content-disclosure` skill. Disclose stock AI avatars rather than argue the edge; note each disclosure in `meta/disclosures.md`.
- A real person's likeness or voice (photo avatar, `voice_clone`) needs their written consent on file.
- No copy that violates Meta or TikTok ads policies (medical claims, financial guarantees, before/after with health products).
- No engagement-bait CTAs ("like and follow to…"); TikTok keeps them out of For You.
- Don't ship a variant without the AI-generated content disclosure noted in `meta/disclosures.md`.

### Interaction

- New brand: ask whether the avatar is photoreal off-the-shelf, a founder photo avatar, or a paid model release. Consent matters.
- Three variants picked: confirm body length and CTA, then render in parallel.
- "Many variants": offer the Remotion-template route.
- Confirm paid Meta or TikTok ad-library compliance versus an organic post.
- An autonomous, non-interactive brief doesn't ask: use a public HeyGen avatar and the defaults above, and list assumptions in the bundle. The consent confirmation for a real person's likeness stays mandatory.

## Examples

### Example 1: avatar voice

❌ "I used this serum for 30 days and my skin cleared up." spoken by a stock avatar as a customer.

✅ "Here's what this serum does and what the clinical study measured." Presenter framing, typical results stated.

### Example 2: lipsync spend

❌ Run Sync.so over all five rendered variants.

✅ Run it on the one picked variant whose lipsync looks soft.

## Checklist

- [ ] One persona, one avatar and voice across every variant.
- [ ] Consent on file before any real person's photo or voice is used.
- [ ] Avatar speaks the hook in the first 1.5 s; cutaways 30–40% of runtime.
- [ ] No fictional-customer testimonial; claims substantiated.
- [ ] Captions burned inside the safe zone, not over the face.
- [ ] `meta/disclosures.md` filled for every variant.
- [ ] Everything saved under `./video-out/<slug>/`.

## Composition / References

- `video-hooks`, `ad-frameworks` — hooks and framework choice.
- `video-editing` — stitch, cutaway, ducking and loudness recipes.
- `video-captions` — captions on every final cut.
- `video-spec-sheet` — safe zones, provider limits, encodes.
- `content-disclosure` — testimonial, AI and paid-partnership rules.
- `content-voice`, `content-humanize` — persona tone; stripping AI cadence.
