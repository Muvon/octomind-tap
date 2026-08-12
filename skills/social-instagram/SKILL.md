---
name: social-instagram
title: "Instagram Publishing Playbook"
description: "Ground-truth 2026 playbook for organic Instagram. Covers the three official ranking signals (watch time, likes per reach, sends per reach — all ratios), the format-by-objective split the benchmark studies actually show (Reels for non-follower reach, carousels for engagement and 9x saves, single images economically dead), the measured 8.5-second Reels watch-time budget, the carousel second-chance mechanic, Trial Reels as the platform's cleanest A/B test, the April 2026 originality/aggregator demotion, hashtag reality (−31.7% views correlation; context only), and Meta's AI-label mechanics. Activate when drafting anything destined for Instagram."
license: Apache-2.0
compatibility: "Octomind content agents. Platform-specific to Instagram (Reels, carousels, Stories, captions)."
domains: content
rules:
  - match(\binstagram\b)
  - match(\binsta\s+(post|reel|reels|caption|story|carousel)\b)
  - match(\big\s+(post|reel|reels|caption|story|carousel)\b)
  - match(\bpost\s+(on|to|for)\s+instagram\b)
---

## Overview

Instagram in 2026 is a watch-time platform wearing a photo app's clothes. Every surface (Feed, Stories, Explore, Reels) runs its own ranking algorithm, but three signals dominate creator reach per Mosseri's own statements: watch time, likes per reach, and sends per reach. All three are ratios — reach without engagement actively hurts, and raw counts flatter you while the algorithm divides.

The market context is brutal and measured: publishing volume grew ~24% year over year while engagement grew ~19% (Metricool, n=24.4M posts), so median engagement rate fell to 0.30% (Rival IQ 2026) and only 21% of sub-10K accounts grew at all. Winning here means picking the right format for the objective and engineering for the specific ratios the ranker predicts — not posting more.

Pair with `content-voice`. Templated, mass-produced content now collides with the April 2026 originality policy regardless of who or what wrote it.

## Instructions

### The Format Decision — different denominators, different winners

The eternal "Reels vs carousels" argument is two study designs talking past each other. Engagement-rate studies divide by followers (Socialinsider, Rival IQ, Buffer) — carousels win. Reach studies count views from non-followers (Metricool, Buffer) — Reels win. Both are right. Choose by objective:

| Objective | Format | Measured basis |
|---|---|---|
| Reach new audience | Reels | Reels far outrank carousels on non-follower reach; >4x interactions of single images (Metricool 2026, n=24.4M) |
| Deepen existing audience, saves | Carousel | 9x more saves than single images; highest per-follower ER every year measured (0.50–0.55%) |
| Quick presence between bigger posts | Story | Relationship surface — reaches people who already follow closely; not discovery |
| Almost never | Single image | Interactions −25%, engagement −46% YoY (Metricool); reach −22% |

Carousels are also Instagram's comparative advantage as a platform: 4.7x more views and 5.8x more interactions than the same carousels get on TikTok (Metricool).

### Reels Craft — budget 8.5 seconds

Average Reels watch time measured across 24M posts is 8.5 seconds (Metricool 2026 — doubled YoY). That, not a target duration, is the design constraint; no single "ideal length" survives scrutiny across studies.

- Hook lands in the first 1–2 seconds — visually, not after a logo card. Most viewers are gone before second 9 no matter the runtime.
- Loops beat length: total seconds watched counts replays, so a 15-second Reel watched three times outranks a 60-second Reel abandoned once. Engineer the last frame to flow into the first.
- Silent-watchable with burned-in captions — but not a text card: Instagram's own Recommendation Guidelines demote muted Reels AND majority-text Reels. The target is video that works muted without being a slideshow of sentences.
- Production hygiene is a ranking gate, not polish: no low resolution, no borders, no other platform's watermark (TikTok logo = suppressed from Explore/recommendations since 2021). Your own logo is officially fine — Mosseri said so directly (Oct 2024).
- Captions are a confirmed Reels ranking factor: front-load the niche keywords people would search; Instagram search matches captions, bios, on-screen text.

### Design for Sends

"Sends per reach" is one of the biggest ranking signals by Mosseri's explicit statement — of everyone who saw it, how many DM'd it to a friend. It's a ratio, and he warns "don't force it" (send-bait is engagement bait). The craft translation: make content with a specific identifiable recipient in mind — the "this is so you" post for a defined kind of person, the reference material useful enough to forward, the in-joke for a niche. If you can't name who would send it to whom, it won't be sent.

### Carousels — two hooks per post

Official mechanic (Mosseri): if someone sees your carousel and doesn't swipe, Instagram often gives it a second chance later, opening on slide 2. No other format gets two independent hook attempts.

- Slide 1 and slide 2 must each work as a cold open — slide 2 written as a continuation wastes the second chance.
- Save-bait is the carousel's job: frameworks, checklists, step-by-steps, before/afters — brands at 100K–1M followers average ~98 saves per carousel vs 43 per image (Socialinsider).
- Swipe-through is dwell; end with a slide worth screenshotting.

### Trial Reels — the platform's built-in A/B test

Trial Reels (official, Dec 2024) publish to non-followers only: off your grid, invisible to followers, evaluated within ~72 hours, one tap (or automatic threshold) to promote to everyone. It is the cleanest legitimate way to test hooks against the recommendation system without spending follower goodwill. Use it to race two hook variants of the same content; promote the winner. Commonly reported as requiring 1,000+ followers (unofficial).

### Collabs

Collab posts with up to 5 co-authors measured at 4.78x impressions and 4.39x interactions vs solo posts (Emplifi). The value comes from audience disjointness — a collab with an account whose followers are your followers adds nothing. Pick partners whose audience you want and don't have.

### Hashtags and SEO — context, not reach

- Mosseri, repeatedly and verbatim: hashtags are "not a way to get more reach"; they help search and categorization "on the margins." Following hashtags was removed entirely in Dec 2024.
- Measured correlation is negative: posts with hashtags averaged 31.7% fewer views and 33.9% fewer interactions (Metricool; correlational — heavy hashtag use proxies for spammy accounts, but it kills the "more tags = more reach" theory).
- Use 3–5 that literally describe the content, for search. Spend the effort on caption keywords instead — captions rank; tag walls don't.
- One clear niche outranks keyword-stuffed everything-accounts in Instagram search (directional but consistent).

### Stories — the relationship surface

Stories rank on closeness (interaction history, likely friends-and-family connection) — they deepen existing followers and are not a discovery tool. The measured shape: ~24% of viewers exit on frame 1, strong Stories keep 60–80% to the last frame. Craft: front-load the point on frame 1, use interactive stickers (polls/questions/sliders engage ~12–18% of viewers and replies grew +88% YoY), keep sequences short. Link stickers convert at 1–5% typically.

### Comments — genuine questions, not bait

Questions in captions measured +36.7% comments; explicit comment-CTAs +203% (Metricool). But Meta demotes accounts that repeatedly post engagement bait ("tag 3 friends", "comment YES") at the account level — with explicit carve-outs for genuine questions and advice requests. Ask real questions you want answered; skip the vote-farming formats.

### The Originality Line (April 2026 — the big one)

Accounts that repeatedly repost content they didn't create lose recommendation eligibility app-wide — extended in April 2026 from Reels to photos and carousels too. Meta's stated bar for "original": wholly created, or materially edited third-party content (added humor, commentary, voiceover, a take). Watermark-slaps and speed changes explicitly don't qualify. Followers still see demoted content; non-followers never will. Trend participation therefore must carry your original framing — riding a trending format without adding anything is precisely what this policy targets.

### AI Content — what's actually true

- Meta labels AI content "AI info" (renamed from "Made with AI" July 2024), triggered by C2PA metadata or self-disclosure. AI-modified (not generated) content gets the label tucked in the post menu.
- Meta has never stated a ranking penalty for the label itself; the only stated demotion in that policy is for fact-checker-rated misinformation. Claims of "80% reach loss for AI labels" trace to SEO blogs, not Meta — ignore them.
- The real algorithmic risk for AI-assisted content is the originality policy above: templated, mass-produced material is what loses recommendations, however it was made. The audience discount on obviously-AI content is real even where the algorithm is neutral.
- Ads are different: AI-generated visuals/text/audio in sponsored content require explicit disclosure, and Meta auto-flags.

### Cadence

- Consistency compounds: consistent posters measured ~5x engagement per post vs occasional posters (Buffer, n=100K+ accounts). Brands average ~8 Reels/month and rising.
- Don't dump posts back-to-back — Buffer observed Instagram suppressing some of a burst. Space them.
- Metrics that matter post-2025: views, reach, sends (impressions and plays no longer exist as metrics). Judge Reels by watch-time-completed and sends-per-reach, not likes.

### What Dies on Instagram

- Single images as a strategy — measured freefall across every study.
- Reposted TikToks with the watermark — suppressed from Explore/recs since 2021.
- Aggregator/repost accounts — zero recommendations since April 2026.
- Hashtag walls — negative measured correlation, no follow-a-hashtag pathway left.
- Engagement bait — account-level demotion for repeat offenders.
- Text-card "Reels" (majority-text) and muted video — named in the Recommendation Guidelines.
- Send-bait ("share this with someone who…" as a formula) — the signal is genuine sends; Mosseri's "don't force it" was aimed at exactly this.

## Pre-publish Checklist

- [ ] Format matches objective: Reels for reach, carousel for depth/saves, Story for existing audience
- [ ] Hook in first 1–2 seconds (Reel) or slides 1 AND 2 (carousel second-chance)
- [ ] Watch-time budget respected: would a viewer still be there at second 9?
- [ ] Works muted, has burned-in captions, isn't a text card
- [ ] No low-res, borders, or other-platform watermarks; own logo OK
- [ ] Caption front-loads searchable keywords; 3–5 descriptive hashtags max
- [ ] The send test passes: you can name who would DM this to whom
- [ ] Original take present — survives the "materially edited?" bar if trend-derived
- [ ] Genuine question over engagement-bait formula, if soliciting comments
- [ ] High-stakes hook variants → Trial Reel first, promote the winner
- [ ] Judged after publish on views/reach/sends, not likes

## Examples

### Example 1: The send test applied

Draft caption: "10 productivity tips every founder needs 🚀 #productivity #founder #hustle #entrepreneur #startup #grind"

Fails: generic listicle (no identifiable recipient), hashtag wall, AI-cliché energy. Rewrite as a carousel: slide 1 "Your calendar isn't full. It's leaking." — slide 2 cold-open "The 3 leaks nobody audits:" — specific, screenshot-worthy final slide. Caption: "Audited 40 founder calendars this quarter. Same three leaks every time. Which one is yours?" Two hooks, save-bait structure, genuine question, zero tag wall — and it's the post an operator forwards to their co-founder.

### Example 2: Trend participation that survives the originality bar

A trending audio is peaking in your niche. Lazy version: lip-sync the meme format verbatim — recommendation-ineligible territory for repeat offenders since April 2026. Surviving version: same audio, but the on-screen text and voiceover carry your niche's specific version of the joke plus one insight only your account would know. Material edit, original commentary — eligible, and differentiated in a saturated trend.

## References

- Instagram Ranking Explained (Mosseri, official): https://about.instagram.com/blog/announcements/instagram-ranking-explained
- Meta Recommendation Guidelines + Transparency Center (engagement bait, originality): https://transparency.meta.com
- Meta AI-labeling policy: https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/
- Measured figures: Socialinsider 2026 (n=35M posts), Metricool 2026 (n=24.4M posts / 375K accounts), Rival IQ 2026 benchmark, Buffer format/timing studies (n=4M posts), Emplifi collab study (2024). ER figures are per-follower unless stated; reach figures are view-based — the denominators differ by study and that difference drives the format guidance above.
- Numbers dated 2025–2026; platform policy shifts fast — re-validate the originality-policy scope, Trial Reels eligibility, and caption-links rollout (Meta Verified test, March 2026) before advising on them as current.
- Companion skills: `content-voice` (kill the AI markers), `trend-instagram` (octoweb domain) for harvesting what's currently working.
