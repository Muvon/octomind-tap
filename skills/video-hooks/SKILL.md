---
name: video-hooks
title: "Video Hooks: TikTok, Reels, Shorts Retention Guide"
description: "Evidence-graded video hooks playbook for TikTok, Reels, and Shorts: an 11-pattern opening hook catalog (pattern-interrupt, contrarian, curiosity-gap, stat punch, identity bait), visual hook devices, banned opens, sound-on audio hooks, endings and loops built for rewatch, mid-video re-hooks, share triggers, organic hook testing (Instagram Trial Reels, distinct concepts), and an originality and engagement-bait guard. Includes post-publish retention review: TikTok finish and skip rates, Instagram Skip Rate and retention chart, YouTube viewed-vs-swiped, and what to re-cut. Use when drafting an ad or social-video script, or when a posted clip loses viewers early."
license: Apache-2.0
compatibility: "Stack-agnostic."
domains: video
rules:
  - session(video)
  - session(adcraft)
  - content(short-form video)
  - content(reels)
  - content(shorts)
  - content(tiktok)
  - content(video hook)
  - content(video ad)
  - match(\bvideo\s+hook\b)
  - match(\b(first|opening)\s+\d+\s*(seconds|s)\s+of\s+(the\s+)?(video|clip|reel|short|ad)\b)
  - match(\bopens?\s+with\b.*\b(video|clip|reel|short|ad|shot|frame)\b)
  - match((?i)\b(go(ing|es)?|went)\s+viral\b)
  - match((?i)\b(retention|skip)\s+(rate|graph|chart|curve|drop)\b)
  - match((?i)\b(trial\s+reels?|swiped\s+away|viewed\s+vs\.?\s+swiped)\b)
  - semantic(make the opening of this video stronger)
  - semantic(the first few seconds of my reel are too weak)
  - semantic(write a hook for this short-form video)
  - semantic(how do I get viewers to keep watching past the first second)
  - semantic(my retention drops in the first 3 seconds, what should the opener be)
  - semantic(how do I make this tiktok go viral)
  - semantic(viewers drop off in the middle of my short, how do I fix it)
  - semantic(how should this reel end so people rewatch it)
  - semantic(my short flopped, read the retention chart and tell me what to re-cut)
  - semantic(test different hooks for this reel before posting to followers)
---

## Overview

Short-form video lives or dies in the first 1.5–3 seconds. The hook is the only sentence in the script that matters more than the offer — if it doesn't earn the next breath, the user swipes and the rest of the work is wasted. This skill encodes the hook patterns that convert on TikTok, Reels, and Shorts in 2026, the rules each pattern follows, and the dead opens to avoid. Platform research behind these rules is correlational: treat them as strong priors and let the account's own hook-rate data overrule them.

## Instructions

### Core Rules

- The hook is the first 1.5s of video, not the first sentence of the script. It is visual + audible + on-screen text together. Treat all three as the hook.
- Earn the next second, not the next minute. Each beat (1.5s, 3s, 5s) needs its own retention reason.
- Don't open on a logo card or with the brand name as the first word. Do get the product or brand on screen naturally inside the first 3–5 seconds — in use, in hand, in the result shot. Google's ABCD research ties early product/brand presence and tightly framed opening shots to higher recall, and TikTok's creative guidance reports that most of its highest-CTR auction ads surface the key message or product within 3 seconds.
- Never open with "Hi guys" / "In this video" / "Today I'll show you". Viewers have learned that filler follows.
- Show motion in frame 1 and change the frame early: subject motion, push-in, or a cut. Google's ABCD guidance recommends more than two distinct frames in the first five seconds.
- Design for sound on. Over 75% of Reels views are sound-on (Meta, 2024-11), so audio is the primary hook channel: the spoken line and sound design must carry the hook alone. Keep burned-in captions and a hook text that reads silently by frame 5 for the sound-off minority. In Meta/Toluna's correlational analysis of 100 ads, an audio plus visual hook made a direct-response ad 1.5× likelier to land in the top 20% for purchase intent; speech plus music was 2.0× for brand ads (top 20% brand interest) and 2.1× for direct-response purchase intent (measured). The source gives no time window; ppc.land's write-up recommends landing both hook channels in the first 1–2 s (reported; directional).
- One claim per hook. Two ideas = no idea.
- Name why someone would send it. Instagram's top ranking signals are watch time, likes per reach, and sends per reach; Mosseri said sends are slightly more important than likes for unconnected (non-follower) reach (reported; no weights published, directional). Every script states its send reason: who would forward it and why ("send this to the friend who...").
- No engagement bait, no unchanged reposts. TikTok keeps content that pushes viewers to inflate likes or follows, and reused content with nothing new, out of For You. YouTube's Shorts originality update (reported, 2026-10-01) and Instagram's originality rules point the same way: a border, watermark, subtitles, speed change, or credit does not make a repost original. Every adaptation of existing footage names its transformation: new hook, new structure, new commentary, or new footage.

### Hook Pattern Catalog

| Pattern | When to use | Template |
|---|---|---|
| Pattern-Interrupt | Cold cold audience, low awareness | `[surprising visual] + "Wait — [absurd claim]"` |
| Contrarian | Audience has heard the cliché | `"Stop [common advice]. Here's why it actually [opposite outcome]."` |
| Problem-Aware | Audience already feels the pain | `"If your [tool/process] still [pain point], you're [losing X]."` |
| Curiosity-Gap | Educational / how-to | `"I tested [N] [things] for [duration]. Only [small N] [outcome]."` |
| Stat Punch | B2B / data-driven | `"[Big number] of [audience] [do thing wrong]. Here's the fix."` |
| Identity Bait | Niche audience | `"You're a [specific identity] if [oddly specific behavior]."` |
| Listicle Promise | Information-dense | `"[N] [things] [audience] should [verb] before [year/event]."` |
| Direct Address | Existing followers / retargeting | `"This is for the [specific user] who [specific pain]."` |
| Negative Framing | Performance ads (Meta/TikTok) | `"Don't [common action] until you [see this/read this]."` |
| Confession | UGC / authentic | `"I'm not supposed to say this, but [insider truth]."` |
| Demo-Cold-Open | Product-led | Show the result first, no setup, then reverse-engineer the how. |

### Visual Hook Devices (stack on top of script)

- Hard cut at 0:00.5 — first frame is mid-action, not establishing.
- On-screen text larger than usual: readable at thumbnail size and inside the platform safe zone.
- Pattern-interrupt object — something visually unexpected in frame 1 (a banana, a hand, a face mid-expression).
- Speed ramp — slow-mo for 0.3s then snap to real-time.
- Camera move — zoom-in or push-in at 0.0–0.5s; static cameras lose attention.
- Caption animation — words appearing in time with speech keep the eye moving; test against flat text on the account's own data.

### Workflow

1. Read the brief — product, audience, awareness level (cold / warm / retargeting).
2. Pick 3 patterns from the catalog that fit the audience and awareness level.
3. Write 3 hook variants — one per pattern. Each ≤ 12 words on screen, ≤ 8 words spoken.
4. For each variant, specify: visual (frame 1 description), on-screen text, voiceover line, motion device, and the last line or frame that flows back into the hook.
5. Score each on: pattern-interrupt strength (1–5), claim specificity (1–5), caption readability sound-off (1–5).
6. Pick the top scorer — but ship at least 2 variants, and make some of them distinct concepts, not only hook swaps (see Organic hook testing). Judge live variants by hook rate (3-second views ÷ impressions) and hold rate (15-second or ThruPlay views ÷ 3-second views), not by likes.
7. Any number in a hook needs a source before publish; claims also need substantiation under ad policies.
8. Write the hook and the last line first, then the body between them; mark a re-hook at each beat boundary where the viewer's question has just been answered.
9. State the send reason, and the named transformation if the clip adapts existing material.

### Decision Guide

| Scenario | Hook pattern |
|---|---|
| Cold audience, fully unaware of the problem | Pattern-Interrupt or Confession |
| Audience knows the problem but not the solution | Problem-Aware or Stat Punch |
| Audience knows the solution category, comparing | Contrarian or Demo-Cold-Open |
| Audience is already a fan / past visitor | Direct Address or Identity Bait |
| Performance ad on TikTok / Meta | Negative Framing or Pattern-Interrupt |
| Educational / informational content | Curiosity-Gap or Listicle Promise |

### Endings and loops

- Write the hook and the last line first; the body connects them.
- End right after the payoff: no outro, no "thanks for watching", no fade.
- Design the last frame or line to flow back into the first (a sentence that completes the opening line, a matching frame, the hook's question re-posed) so a rewatch feels natural, not forced. Never pad length to force a loop.
- Why it matters: Shorts count every play and replay as a view since 2025-03-31 (reported), and TikTok lists finished videos among its ranking signals (official).

### Mid-video re-hooks

- Open a loop early ("the third one changes everything") and close it late; each open loop is a reason to stay through the middle.
- Place a pattern interrupt (new angle, location change, punch-in, sound change, text card) at the predicted drop points: right after a payoff lands and the viewer's question is answered.
- After posting, move re-hooks to the actual drop-off seconds on the retention chart (see Retention review after posting).

### Retention review after posting

Read the platform's own data, not likes:

- TikTok: finish and skip data per video.
- Instagram: Skip Rate (share of views skipped in the first 3 s) and the retention chart (reported).
- YouTube Shorts: viewed vs swiped away. One measured study of 5,400 Shorts found under about 60% viewed rarely performed and 70–90% was typical of winners; descriptive, not a target.

Steps: find the drop-off second, name the cause (slow setup, answered question, off-topic beat, audio dip), re-cut or re-hook, record what worked in the variants log. Never delete and re-upload a flopping Short: YouTube's Creator Insider flags it as a spam risk (official).

### Organic hook testing

- Instagram Trial Reels are shown to non-followers first and can auto-share to followers based on first-72-hour performance (official). Use them to test before committing the main feed.
- Test different concepts, not only hook swaps. TikTok asks for visually distinct creatives (official, ads-scoped), and Jon Loomer's Meta Andromeda guidance says ad variations should differ significantly, not subtly (directional).
- Change one concept variable per test (angle, format, opening scene) and log the result against the account's baseline hook rate.

### Myths to Drop

Don't repeat these; none has a traceable source or each is contradicted by official data:

- "TikTok and Reels are watched sound-off": over 75% of Reels views are sound-on (official).
- "Shorter always wins": best length depends on platform and goal; see `video-editing`.
- "63% of successful TikTok ads deliver the message in 3 seconds": untraced. The official guidance is to put the proposition in the first 3 s.
- "Trending audio adds 30–50% reach": untraced.
- "Instagram weights sends 3–5× likes": Instagram publishes no weights.
- "Meta Andromeda uses a 60% similarity score": untraced.
- "Strong hooks hold 80–90% at 3 s": untraced.
- "The platform's official 3-second-hold target is X%": no official 3-second-hold benchmark exists on any platform; use the account's own baseline.

## Examples

### Example 1: SaaS dev tool, cold TikTok audience

Brief: Promote a CLI tool that auto-generates database migrations.
Audience: Backend devs, mostly cold.
Pattern picks: Pattern-Interrupt, Contrarian, Stat Punch.

Variant A — Pattern-Interrupt
- Frame 1: Terminal mid-typing, a migration error fills the screen in red.
- On-screen text: `your migrations are lying to you`
- Voice: `Your migrations are lying to you.`
- Motion: hard zoom-in on the error.

Variant B — Contrarian
- Frame 1: Hand crossing out the words "Write SQL by hand" on whiteboard.
- On-screen text: `STOP writing migrations by hand`
- Voice: `Stop writing migrations by hand. There's a better way.`
- Motion: quick whip-pan to the laptop screen.

Variant C — Stat Punch
- Frame 1: Big number `73%` filling the screen.
- On-screen text: `73% of prod outages start in a migration`
- Voice: `Seventy-three percent of prod outages start in a migration. Here's how to stop being one of them.`
- Motion: number scales up from 0 to 73 in 0.5s.

Pick: B for cold dev audience — Contrarian + clear visual, no claim that needs sourcing. Variant C's 73% is a placeholder and cannot ship without a cited source.

### Example 2: D2C skincare, retargeting audience

Brief: Cart-abandoners who viewed the SKU but didn't buy.
Pattern picks: Direct Address, Confession.

Variant A — Direct Address
- Frame 1: Mid-shot of a person looking straight to camera, finger pointing.
- On-screen text: `you ← yes, you who left this in your cart`
- Voice: `You — yes, you, who left this in your cart yesterday.`
- Motion: subject leans into camera.

Variant B — Confession
- Frame 1: Founder unboxing a return.
- On-screen text: `nobody told me this would happen with [product]`
- Voice: `Nobody told me this would happen the second week of using it.`
- Motion: hand reveals the product mid-frame.

## Hooks That Are Banned

These openers spend the first second on nothing — don't use them:

- "Hi everyone / Hi guys / What's up"
- "In this video / Today I'm going to / Let me show you"
- "Welcome back to my channel"
- Logo on screen alone
- Brand name as the first spoken word
- Any sentence that starts with "So..."
- A static product shot with no motion
- Music-only opener with no visual or text claim

## Checklist

- [ ] Hook is visual + audible + text in the first 1.5 s; works with sound on and reads silently by frame 5.
- [ ] Product or brand on screen by 3–5 s; one claim; every number sourced.
- [ ] Last line or frame written first and flows back into the hook; ends right after the payoff.
- [ ] Re-hook or open-loop beat at each predicted drop point.
- [ ] Send reason named; no engagement bait; transformation named for any adaptation.
- [ ] At least 2 variants, including distinct concepts, not only hook swaps.
- [ ] After posting: drop-off second found, cause named, re-cut or re-hook done, result recorded; no delete and re-upload.

## References

- [TikTok Creative Center](https://ads.tiktok.com/business/creativecenter/) — top-performing ad teardowns by vertical.
- [Meta Ads Library](https://www.facebook.com/ads/library/) — search competitors and study their first 3 seconds.
- [Google ABCDs of effective video ads](https://business.google.com/us/resources/articles/abcds-of-effective-video-ads/) — Attract, Brand, Connect, Direct; correlational creative research.
- [TikTok recommendation system](https://www.tiktok.com/transparency/en/recommendation-system) — finished videos listed as a ranking signal (official, undated page).
- [TechCrunch: YouTube is changing how Shorts views are counted](https://techcrunch.com/2025/03/26/youtube-is-changing-how-youtube-shorts-views-are-counted/) — plays and replays count from 2025-03-31 (reported, 2025-03-26).
- [Social Media Today: Instagram adds retention insights for Reels](https://www.socialmediatoday.com/news/instagram-adds-retention-insights-reels/758464/) — Skip Rate and retention chart (reported, 2025-08-24).
- [Paddy Galloway (@PaddyG96) thread on 5,400 Shorts](https://threadreaderapp.com/thread/1646898356419981315.html), viewed-vs-swiped (measured, 2023-04; descriptive).
- [YouTube Creator Insider](https://www.youtube.com/watch?v=n3jsYK_-aRU) — don't delete and re-upload underperforming Shorts (official, 2023-08-23).
- [Instagram Trial Reels](https://creators.instagram.com/blog/instagram-trial-reels) — non-followers first, auto-share on first-72-hour performance (official, 2024-12-10).
- [TikTok creative best practices](https://ads.tiktok.com/help/article/creative-best-practices) — visually distinct creatives; proposition in the first 3 s (official, 2025-06).
- [Jon Loomer: Meta Andromeda creative diversification](https://www.jonloomer.com/meta-andromeda-creative-diversification/) — variations should differ significantly, not subtly (directional, 2025-10-20).
- [Meta for Developers: Reel ads](https://developers.facebook.com/blog/post/2024/11/07/unlock-the-power-of-reel-ads) — over 75% of Reels views sound-on (official, 2024-11).
- [Meta: Reels creative strategies](https://www.facebook.com/business/news/reels-creative-strategies) — Meta x Toluna correlational analysis of 100 ads: audio plus visual hook 1.5× for direct-response purchase intent; speech plus music 2.0× for brand ads (top 20% brand interest) and 2.1× for direct-response purchase intent (official, measured, 2025-12-02); [ppc.land write-up](https://ppc.land/meta-and-toluna-study-finds-emojis-lift-reels-purchase-intent-2-5x/) (reported, 2026-05-18).
- [Social Media Today: Mosseri on Instagram ranking signals](https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/) — watch time, likes per reach, sends per reach; sends slightly more important than likes for unconnected reach; no weights published (reported, 2025-01).
- [TikTok community guidelines: integrity and authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity) — engagement inflation and unoriginal reused content kept out of For You (official, 2026-08).
- [Social Media Today: YouTube updates Shorts algorithm to favor original content](https://www.socialmediatoday.com/news/youtube-updates-shorts-algorithm-to-put-more-focus-on-original-content/831976/) — aggregator channels likely to see less Shorts distribution (reported, 2026-10-01); [Instagram: rewarding original creators](https://creators.instagram.com/blog/rewarding-original-creators-on-instagram) — a border, watermark, subtitles, or credit does not make a repost original; rolling 30-day assessment (official, 2026-04-30); [TechCrunch on the aggregator crackdown](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/) — speed change (reported, 2026-04-30).
