---
name: social-tiktok
title: "TikTok Publishing Playbook"
description: "Ground-truth 2026 playbook for organic TikTok. Covers the official ranking reality (follower count is not a direct factor — verbatim; completion of longer videos = strong indicator; For You drives 72.7% of views), the saturation math (volume +72%, views −31% YoY), the official 3–6 second hook window, lo-fi beating polished (+33% consideration, TikTok/Lumen), the measured comment asymmetry (questions +26%, asking for likes −60%), video-over-carousel evidence, TikTok SEO and the search-value RPM factor, the September 2025 unoriginality enforcement, Creator Rewards floors, and the honest AI-content picture (labeled, not throttled). Activate when drafting anything destined for TikTok."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to TikTok (videos, carousels, captions, sounds)."
domains: content
rules:
  - match(\btiktok\b)
  - match(\btik\s?tok\b)
  - match(\bpost\s+(on|to|for)\s+tiktok\b)
  - match(\bfor\s+you\s+(page|feed)\b)
---

## Overview

TikTok distribution is interest-matching, not audience-owning: the For You feed drives 72.7% of video views (Metricool 2026, n=2.31M posts) and TikTok states verbatim that "neither follower count nor whether the account has had previous high-performing videos are direct factors in the recommendation system." Every video re-earns its reach from zero against the viewer's interest clusters.

The 2026 market context is saturation, and it's measured: published video volume grew 72% year over year while views fell 31% and reach fell 29% (Metricool). Follower growth rates dropped by a third across all tiers (Socialinsider, n=2M videos). "Post more" is not supported by current data — post better-matched, better-hooked content is. And speed matters structurally: 96% of a post's total reach and ~98% of its interactions arrive within the first 10 days (Metricool).

Pair with `content-voice`. Low-effort output dies here on quality grounds — the For You eligibility rules catch it regardless of who or what made it.

## Instructions

### How ranking actually works (official, not folklore)

- Three official signal categories: user interactions (likes, shares, comments, watch behavior), video information (captions, sounds, hashtags), device/account settings (weakest tier).
- The only official weighting statement is qualitative: a strong indicator like "whether a user finishes watching a longer video from beginning to end" outweighs weak indicators like shared geography. Every numeric weight table circulating online is practitioner guesswork — completion and watch-through are the strongest bets, per TikTok's own example.
- A qualified view = a unique For You view of at least 5 seconds (Creator Academy). Repeat views don't count toward it.
- New uploads are tested on a small pool and expand with performance (directional but consistent); the "tested on your followers first" claim contradicts the official follower-count statement — treat it as false. The numeric "200-view jail" thresholds are creator shorthand, not policy.
- The feed deliberately diversifies: it "generally won't show two videos in a row made with the same sound or by the same creator" — you compete against your own recent posts less than folklore claims, and trends rotate by design.

### The Hook — 3 to 6 seconds, officially

TikTok's own creative guidance (Creative Playbook, Marketing Science studies): "the first 3–6 seconds are critical" and "regardless of format, the first six seconds are vital for impact." The endorsed structure is Hook → Unique Selling Points → Call-to-action (template timing: hook 1–4s, USPs ~20s, CTA 1–4s). From ads data, labeled as such: 63% of the highest click-through videos hook within the first three seconds.

- Open on the payoff, the conflict, or the claim — never on a logo, an intro, or "hey guys."
- The circulating retention statistics ("60% past 3s = 4x reach" etc.) are fabricated stat-farm content with no methodology. Design for the official 3–6s window and measure your own retention curve.

### Lo-fi beats polished — TikTok measured it

TikTok Marketing Science (Lumen study): lo-fi creative sees 33% stronger consideration than polished ads. Supporting official studies: 75% of users respond positively to TikTok-first creative (Ipsos 2022); ads featuring creators drove +24% brand favorability (Hotspex 2021); 43% of heavy users say good TikTok advertising blends in with content. These studies date 2020–2023 but remain TikTok's current public creative position.

- Native, handheld, person-on-camera beats studio polish. Feature real people — creators, employees, customers.
- Talking-head with on-screen text is the workhorse format; the creator-favorability data is the evidence for faces over faceless.
- Production floor, not ceiling (official specs): 9:16 vertical, minimum 720p, sound always on — but ~30% watch muted (Creator Academy via Hootsuite), so burned-in captions and text overlay carry the message regardless.

### Comments — the measured asymmetry

The single most actionable measured finding (Metricool 2026): a question in the post earns +26% comments and asking for comments +14% engagement — while asking for likes cuts interactions by 60%. Buffer's 52M-post study adds that replying to comments was "the strongest signal in the entire dataset."

- End with a genuine question the niche wants to argue about.
- Never ask for likes/follows — measured self-harm and engagement-bait policy territory ("artificially increase engagement" = For You ineligibility).
- Reply to early comments personally; reply-videos (answering a comment with a new video) are a sound mechanic for series content — no reliable uplift percentage exists, so treat them as a content source, not a multiplier.

### Format and length

- Video beats carousels, measured twice: median ER 3.39% vs 1.92% (Buffer, n=45M posts), 5x views and 6x interactions (Metricool). TikTok's own 2024 claim that photo posts out-engage video is outdated marketing. Carousels remain a niche play for reference/save content, not reach.
- Length: officially "video lengths from 15 sec to 3 min — any length within this range can find success," with the first 6 seconds vital. TikTok has been distributing longer (1–3 min+) content more where completion holds (directional); 60% of users interact most with sub-60s video (Sprout 2026). Rule: as long as the content stays dense, as short as it can be — completion of what you publish is the strong indicator.
- Sounds: use the Commercial Music Library for business-cleared tracks. The 0%-volume trending-sound trick fails — audio analysis reads the actual sound.

### TikTok SEO — search is an earnings factor

Captions, sounds, and hashtags are official ranking inputs; "search value" is one of TikTok's four official RPM factors (with originality, play duration, engagement) — TikTok literally pays more for searchable content. 49% of US consumers have used TikTok as a search engine (Adobe 2025), though Gen-Z preference for it over Google is small and falling (8%→4%, 2024→2026) — optimize for discovery, don't bet the strategy on search alone.

- Say the keywords out loud in the video (spoken audio is indexed — directional but consistent), put the primary keyword at the front of the caption, keep auto-captions on.
- Hashtags are back, measured: posts with ≥1 hashtag get ~5% more views and >9% more interactions; hashtag-driven traffic +114% YoY (Metricool). Use 1–5 specific, descriptive ones — not 30, not zero.

### Monetization floors (know them before advising creators)

Creator Rewards requires: 10,000+ authentic followers, 100,000+ authentic views in 30 days, videos at least 1 minute long, original content with 1,000+ For You views — duets, stitches, photo posts, and sponsored content are ineligible. RPM = originality × play duration × engagement × search value. This is why serious creators structure ideas as 1-minute+ originals.

### What Dies on TikTok

- Watermarked re-uploads — the For You eligibility standards exclude "content with someone else's visible watermark or superimposed logo," including other editing apps' logos. Cross-posting Reels with the watermark kills distribution.
- Unoriginal content generally — enforcement escalated 15 September 2025: repeated imports/copies without "new, creative edits" now affect both earnings and visibility.
- Delete-and-repost of a flopped video — duplicate detection can flag the re-upload as unoriginal, making it For-You-ineligible; worse than the original stall.
- Extremely short clips, GIF-only videos, QR codes — named in the eligibility standards.
- Engagement bait — policy ineligibility, and the measured −60% for like-begging.
- Polished ad-feel content — not penalized, just outcompeted (the lo-fi +33% is the inverse framing).
- "Shadowban" is not the mechanism — TikTok's term is "ineligible for the For You feed"; diagnose against the eligibility standards, not superstition.

### AI content — labeled, not throttled

- TikTok requires labeling of realistic AI content, auto-labels via C2PA Content Credentials, and added an invisible watermark (March 2026) that survives re-uploads. Over 1.3 billion videos labeled to date.
- No measured AI reach penalty exists — every circulating figure claiming one is fabricated. Credible evidence points the other way: AI content achieves enormous reach (a single AI history-POV video hit 4.4M likes, arXiv 2026).
- The real risks: (a) users can dial down AI content via the Manage Topics control (rolling out since Nov 2025) — audience-side opt-out; (b) low-effort AI output gets caught by the unoriginal/low-quality rules on quality grounds; (c) Creator Rewards' originality requirement hits RPM. Disclose realistic AI, make it original, and it competes normally.

### Timing and cadence

- Measured strongest window: 6–9pm audience-local, peak 8pm (Metricool, n=2.31M). Timing tunes the margin; completion decides the outcome.
- Cadence honestly: brand accounts average 2 videos/week (Rival IQ/Quid 2026); growth-tier creator accounts run 8–23 posts/month by size (Socialinsider) — different populations, both measured. Whatever the cadence, the 10-day lifespan means a steady drumbeat beats bursts.

## Pre-publish Checklist

- [ ] Hook lands inside the official 3–6s window; no intro, no logo card
- [ ] Structure: Hook → value/USPs → CTA; dense the whole way (completion is the strong indicator)
- [ ] 9:16, ≥720p, sound on, burned-in captions (30% watch muted)
- [ ] Lo-fi/native register — would this pass as a person's video, not an ad?
- [ ] Keywords spoken aloud + front-loaded in caption; 1–5 specific hashtags
- [ ] Ends with a genuine question; zero like-begging
- [ ] Original: no third-party watermarks, no re-uploads, material edits on any borrowed format
- [ ] 1 minute+ if monetization matters (Creator Rewards floor)
- [ ] Realistic AI content labeled; originality carries it regardless
- [ ] Scheduled toward 6–9pm audience-local when convenient — never at the cost of the idea
- [ ] Plan to reply to early comments; reply-video candidates noted

## Examples

### Example 1: The asymmetry applied

Weak closer: "Like and follow for more AI tips!" — measured −60% interactions territory plus bait policy risk. Strong closer: "That's how we cut our token bill 70%. What's the dumbest thing your agent has done with your money?" — genuine question (+26% comments measured), niche-specific, and the replies seed the next reply-video.

### Example 2: Cross-post done right

Wrong: download the Reel (watermark burned in), upload to TikTok — excluded from For You by the eligibility standards verbatim. Right: export clean from the editor, re-cut the hook for a 3–6s open, swap in a TikTok-native sound from the Commercial Music Library, front-load the spoken keyword, re-caption. Same asset, platform-original execution — eligible and competitive.

## References

- How TikTok recommends videos (official): https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you
- For You feed eligibility standards + integrity policies: https://www.tiktok.com/community-guidelines/en/fyf-standards
- Creator Rewards terms: https://www.tiktok.com/legal/page/global/creator-rewards-program-us/en
- TikTok Global SMB Creative Playbook (hook window, lo-fi studies, production specs): https://ads.tiktok.com/business/library/Global_SMB_Creative_Playbook.pdf
- Measured figures: Metricool 2026 (n=2.31M posts/92K accounts), Socialinsider 2026 (n=2M videos), Buffer 2026 (n=52M posts), Rival IQ/Quid 2026 benchmark, Adobe 2025 search survey. Engagement-rate claims differ by denominator (per-follower vs per-view vs per-post) — attribute the study when citing one.
- Source hygiene: 2026 "TikTok statistics" content is heavily polluted by AI stat farms inventing figures with fake attributions to real firms. Verify anything new against the primaries above before adding it here; re-validate policy items (AIGC controls, originality enforcement) periodically.
- Companion skills: `content-voice` (kill the AI markers), `trend-tiktok` (octoweb domain) for harvesting what's currently rising.
