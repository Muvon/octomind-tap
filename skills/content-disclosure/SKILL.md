---
name: content-disclosure
title: "Content Disclosure: Paid Partnership and AI Labels"
description: "Paid-partnership and AI-content disclosure rules per platform and jurisdiction: FTC, YouTube, TikTok, Meta, EU AI Act, New York. Use before publishing."
license: Apache-2.0
compatibility: "Stack-agnostic."
domains: content video
rules:
  - content(disclosure)
  - content(disclose)
  - content(sponsored)
  - content(paid partnership)
  - content(altered content)
  - content(ai label)
  - content(ai-generated)
  - match((?i)\b(FTC|endorsement guides?)\b)
  - match((?i)\bAI Act\b)
  - match((?i)\bsynthetic (content|performer|media)\b)
  - match((?i)\b(label|tag|mark)\w*\s+(this|my|the)?\s*(video|post|ad|content)\s+as\s+(ai|sponsored|an ad)\b)
  - content(brand deal)
  - content(influencer)
  - content(affiliate)
  - semantic(do I need to disclose that this video is AI generated)
  - semantic(how do I label a sponsored post)
---

## Overview

Two kinds of disclosure apply to published content. A paid-partnership disclosure tells the audience that a brand paid, gave something of value, or has another connection to the speaker. An AI-content disclosure tells the audience that realistic video, audio or images were generated or altered by AI. Each platform and each jurisdiction sets its own trigger, its own place to put the label, and its own penalty. This skill holds one table per kind, so every agent that publishes reads the same rows. Rows were checked on the primary source on 2026-11-15 except where a row says a page could not be read; rows that move often carry their source date. If the agent has a web tool, open the linked page before a paid launch and prefer what the page says over this table.

## Mental model

Ask three questions in order, for each placement of the piece.

1. Is there a material connection (payment, free product, employment, family tie)? If yes, the FTC rule and the platform's partnership tool both apply.
2. Is any person, voice, place or event in the piece realistic and AI-generated or AI-altered? If yes, the platform AI label applies, and the law of the audience's country may apply on top.
3. Is it an ad or an organic post? Ad systems (TikTok Ads Manager, Meta ads) have their own mandatory disclaimers, separate from the organic toggles.

A platform toggle does not replace the legal duty: the FTC says a platform's disclosure tool may help but should not be assumed sufficient on its own.

## Rules

### Paid partnership

| Jurisdiction or platform | Rule | Where to set it | Source (checked 2026-11-15) |
|---|---|---|---|
| United States, FTC | Disclose any financial, employment, personal or family relationship with a brand, and anything of value received to mention a product. The disclosure sits with the endorsement itself, is hard to miss, uses plain words such as "ad", "advertisement" or "sponsored", and is not left on a profile page or behind a "more" click. In video, put it in the video, not only the description; said and shown works best. Repeat it periodically in live streams. Unclear terms such as "sp", "collab" or "thanks" alone do not count. | In the piece itself, plus the platform tool | [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers), page dated November 2019 |
| United States, FTC fake reviews rule | Bans fake or false testimonials, including AI-generated ones that misrepresent the author as someone who does not exist, and insider reviews that hide a material connection. The agency may seek civil penalties against knowing violators. | Script and casting stage | [FTC press release, 2024-08-14](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials) |
| YouTube | Creators who include branded content, sponsorships or endorsements select the paid promotion option in the video details; the label shows at the start of the video. In the upload flow the option reads "Yes, my video includes branded content". | YouTube Studio, video details | [YouTube Help: paid product placements](https://support.google.com/youtube/answer/154235) |
| TikTok | Content Posting API, direct post: `brand_content_toggle` (boolean, required) is set to true when the video is a paid partnership promoting a third-party business; `brand_organic_toggle` (boolean) is set to true when the video promotes the creator's own business. In the app the choices read "Your brand" (shown as Promotional content) and "Branded content" (shown as Paid partnership); branded content cannot be posted privately. Posts from an unaudited API client are restricted to private viewing. Still disclose in the video per the FTC row. | Post settings, or the two toggles in the API | [Content Posting API reference](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post); [Content sharing guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines), checked 2026-11-15 |
| Instagram | Instagram has its own branded-content toggle or partnership label. The toggle name and consequences were not confirmed on a platform page in this pass: open the current help-center article before the upload, and still disclose in the video per the FTC row. | Post settings | Look up live |

### AI-generated and altered content

| Jurisdiction or platform | Rule | Where to set it | Source (checked 2026-11-15) |
|---|---|---|---|
| YouTube | Disclose AI-generated or altered content that looks realistic: a real person made to say or do something they did not, altered footage of a real event or place, a realistic scene that did not occur, or AI music that is the main focus. Not needed for clearly unrealistic content, aesthetic edits (filters, captions, audio repair), gameplay footage from video games (the page lists minor edits and says the list is not exhaustive), cloning your own voice for voiceover, or AI help with scripts, titles and thumbnails. YouTube may add the label itself for its own AI tools and for C2PA metadata. Repeated non-disclosure can lead to labelling, removal or suspension from the Partner Program. Disclosure alone does not limit audience or monetization. | YouTube Studio upload, "AI use" under Attributes | [YouTube Help: altered or synthetic content](https://support.google.com/youtube/answer/14328491) |
| TikTok, organic | Creators must label AI-generated or significantly edited content that shows realistic-looking scenes or people. Unlabelled content may be removed, restricted or labelled by TikTok. The policy was released 2026-08-25 and took effect 2026-09-24. Via the Content Posting API, the optional boolean `is_aigc` adds a "Creator labeled as AI-generated" tag in the video description. | In-app label, or `is_aigc` in the API | [TikTok Community Guidelines: integrity and authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity); [Content Posting API reference](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post) |
| TikTok, ads | Ads Manager lists "AI-generated, synthetic, or manipulated media" as a mandatory disclaimer category, covering media fully made by AI and genuine material substantially altered by AI. The page states no penalty. | Ads Manager disclaimer | [TikTok Ads help: ad disclaimers](https://ads.tiktok.com/help/article/about-ad-disclaimers-in-tiktok-ads-manager) |
| Meta (Instagram, Facebook, Threads), organic | Meta applies the "AI info" label when it detects industry-standard AI indicators or when the poster discloses; Meta says its labelling method is still evolving and may miss some AI-edited content. Meta's Community Standards on manipulated media may require its disclosure tool for photorealistic video or realistic-sounding audio and may penalize non-disclosure; that text was not readable in this pass, so read it before posting. The Instagram Content Publishing API takes an optional `is_ai_generated` parameter, not available for carousel children. | Meta disclosure tool, or `is_ai_generated` in the API | [Meta: labeling AI content](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/); [Instagram Graph API: IG User media](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media) |
| Meta, ads | Ads made or significantly edited with Meta's generative tools or third-party tools get an "AI info" label in the "About this ad" menu. Meta's ads post (updated 2026-06-01) says it also detects ads made with third-party AI tools through industry-standard signals and applies the same label; check the page for the current rollout. | Ad setup | [Meta newsroom: expanding GenAI transparency for ads products](https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/), updated 2026-06-01 |
| European Union, AI Act Article 50 | 50(4), deepfakes: deployers disclose that image, audio or video they generate or manipulate is a deepfake; for evidently artistic, creative, satirical or fictional work, the disclosure may be limited so it does not spoil the work. 50(4), text: AI-generated text published to inform the public on matters of public interest is disclosed as AI-generated, unless the content has undergone human review or editorial control and a natural or legal person holds editorial responsibility for its publication. Record the reviewer and the accountable editor for each such piece. Applies from 2026-08-02. 50(2): providers of generative systems mark outputs in a machine-readable way; systems placed on the market before 2026-08-02 have until 2026-12-02 to comply (Regulation (EU) 2026/1744, published in the Official Journal 2026-07-24, in force 2026-07-27; the EUR-Lex page did not load in this pass, so read the Official Journal text for these dates). 50(5): the information is clear, given no later than the first exposure, and accessible. | In the piece, at first exposure | [Article 50 text](https://artificialintelligenceact.eu/article/50/); [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) |
| New York, GBL § 396-b | An ad that includes a synthetic performer (an AI-generated person not recognizable as a real individual, such as an AI avatar presenter) must conspicuously disclose it when the advertiser has actual knowledge. Civil penalty $1,000 for a first violation, $5,000 for each later one. Audio-only ads and AI used solely to translate a human performer are exempt. Ads and promotional materials for expressive works (films, television, streaming content, documentaries, video games and similar audiovisual works) are also exempt, if the synthetic performer's use in the ad is consistent with its use in the work. The act takes effect 180 days after it became law; it was signed on 2025-12-11 (chapter 617), which gives 2026-06-09 by computation (the statute page does not state the date). | In the ad itself | [NY Senate: GBL 396-b](https://www.nysenate.gov/legislation/laws/GBS/396-B), revised 2026-06-12 |

### Other states

Other U.S. states have AI-content and provenance laws, and California's AI Transparency Act amendments have reported start dates in 2026 and 2027. The statute dates were not confirmed on a primary source in this pass. For an audience in a state not listed above, look up the current statute before publishing; do not rely on this table for it.

### Handling in a deliverable

- Every piece carries a disclosure line in its publish checklist: paid relationship (yes or no, how disclosed), AI content (which beats: frames, clips, voice, music, avatar), platform setting applied per placement.
- Re-encoding with ffmpeg strips C2PA Content Credentials, so a platform will not auto-label the file. Set the label by hand.
- Hold a post private when a required label or partnership setting could not be set, and say why.

## Examples

### Example 1: sponsored short with an AI voice-over

A creator posts a TikTok for a brand and uses a cloned voice of a real person who did not record the lines. Checklist: say "ad" aloud and show it on screen in the first seconds (FTC); turn on TikTok's branded-content toggle; turn on the AI-generated label because the voice is realistic and the person did not say it; for EU viewers, the deepfake disclosure applies from 2026-08-02.

### Example 2: animated mascot ad

A clearly cartoon mascot explains a product. No AI label is needed on YouTube (clearly unrealistic content); the ad still carries the paid-promotion disclosure.

## Checklist

- [ ] Material connection decided for each placement; disclosure said and shown in the piece, not only in the caption.
- [ ] Realistic AI people, voices, places or events listed in the publish checklist.
- [ ] Platform AI label or API field set per placement; ads use the ad-system disclaimer.
- [ ] EU audience: Article 50(4) deepfake disclosure at first exposure.
- [ ] EU public-interest text: label it as AI-generated, or record the reviewer and the accountable editor.
- [ ] New York ad with an AI presenter: conspicuous synthetic-performer disclosure.
- [ ] Rows checked against the live page for a paid launch.

## References

- [FTC Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers)
- [FTC final rule on fake reviews and testimonials](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials)
- [YouTube Help: paid product placements](https://support.google.com/youtube/answer/154235)
- [YouTube Help: altered or synthetic content](https://support.google.com/youtube/answer/14328491)
- [TikTok Community Guidelines: integrity and authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity)
- [TikTok Ads help: ad disclaimers](https://ads.tiktok.com/help/article/about-ad-disclaimers-in-tiktok-ads-manager)
- [Meta: labeling AI content](https://transparency.meta.com/governance/tracking-impact/labeling-ai-content/)
- [EU AI Act Article 50](https://artificialintelligenceact.eu/article/50/)
- [Regulation (EU) 2026/1744 (Digital Omnibus on AI)](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng)
- [New York GBL 396-b](https://www.nysenate.gov/legislation/laws/GBS/396-B)
