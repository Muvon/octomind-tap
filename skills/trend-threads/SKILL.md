---
name: trend-threads
title: "Threads Trend Harvester Playbook"
description: "Harvest current Meta Threads conversations into a source-backed brief with post URLs, visible metrics, audience questions, and reusable structures. Activate for Threads trend scans or campaign research; distinguish observed conversation from inferred reach and buying intent."
license: Apache-2.0
compatibility: "Octoweb browser access and network. Authorized signed-in access where a surface requires it."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(threads)
  - match(\bthreads\s+(trend|trends|harvest|brief|research)\b)
  - match(\b(harvest|scan|analyze)\s+threads\b)
---

## Overview

Harvest Meta Threads conversations for a defined audience and purpose. “Threads” in a platform research request means Meta's app; interpret multi-post threads using their named destination.

Return evidence and transferable structures. Drafting or publishing posts is a downstream step. Preserve source wording when quoting; don't turn observed copy into unsupported writing or algorithm rules.

## Mental model

Threads Insights includes views, interactions, follower detail, discovery sources, and trends (official, Meta Personalization, 2025-07). Use public views when visible and owner Insights only with authorized access. Missing metrics mean unavailable, not zero.

Author replies correlated with higher engagement in an observational study (measured, Buffer Replies, n=128,000-plus Threads posts, 2026-02). Record who participates and what they say; author participation doesn't prove automatic distribution or buying interest. Avoid fixed signal weights, virality thresholds, expiry cutoffs, and self-reply resurfacing claims.

## Rules and harvest procedure

### Define the sample

Take the target audience, geography and language, buyer situation, desired research outcome, and time window from the brief. If absent, state the scope you select before collecting. Keep the resulting sample bounded by that purpose (directional).

Record whether access is signed in and whether a surface is personalized. Treat For You, Following, custom feeds, and other feed names as interface observations when present; don't assume their current defaults, ordering, or audience share.

### Navigate surfaces

Start at [threads.com](https://www.threads.com/), the current web domain after Meta's migration (official, Meta Web, 2025-04). Navigate through visible controls and copy resolved URLs. The verified migration source doesn't document search parameters, tag routes, profile paths, or a Help Center landing path.

| Surface | Procedure | Evidence and use |
|---|---|---|
| Search | Enter topic language and buyer-problem wording. Use only tabs or date filters visible in the current interface; record their labels and final URL. | Keyword search began rolling out on mobile and web in September 2023 (official, Meta Introduction, 2023-09). Compare discovery results with recent conversations if that control is available (directional). |
| Tagged topics | Open the topic from an actual post or search result; copy the destination. | Meta says tagged-topic posts generally receive more views (official, Meta Personalization, 2025-07). Capture the tag as context without assuming a maximum count or multiplier (directional). |
| Communities Hub | Open the main-menu Hub and select a relevant community. | Communities graduated from beta; Progress and expanded Champion recognition are documented (official, Meta Communities, 2026-06). Use them to find conversations, not certify sales influence (directional). |
| Local Communities | Look for the relevant native-language tags and inspect actual language use. | Initial scope included Japan, Korea, and Taiwan (official, Meta Communities, 2026-06). Preserve local terminology in the brief (directional). |
| Feed selection | Inspect For You, Following, or relevant custom feeds when exposed. Record the selected feed and how it was reached. | Availability and contents are session observations. Sample beyond a personalized feed before claiming a niche trend (directional). |
| Anchor profiles | Open authors from observed posts or search; copy profile and post permalinks. | Include practitioners and potential buyers. Inspect Champions' contributions before assigning relevance (directional). |
| Live Chats | Inspect a current chat or quoted moment only when available and relevant. | Expanded co-hosting and feed quoting were announced as a rollout (official, Meta Communities, 2026-06). Record availability, context, and participation scope (directional). |
| Insights | Use only authorized owner data; record period, source, and metric definition. | Insights documents views and interaction trends over 7–90 days (official, Meta Personalization, 2025-07). Don't assume another author's dashboard is public. |

Open independent surfaces in separate tabs when useful. Scroll until the relevant window is covered or successive loads stop adding distinct material. Use the browser's available controls without assuming a particular scroll-tool name. If a surface is blocked, record that limit and continue through accessible surfaces; don't manufacture access or route behavior.

### Capture each candidate

Retain the post permalink, handle, visible author context, publication time, capture time and timezone, originating surface, and query or topic. Mark missing dates or rounded counts explicitly.

Record text, format, media content, root or reply position, and the observed chain structure. Keep visible likes, views, replies, reposts, and quotes as separately named fields. Where useful, retain an account's comparable posts as a baseline. Don't fabricate follower counts or derive exact metrics from rounded displays.

Read the parent and actual replies. Separate author updates from answers to readers. Note whether commenters provide firsthand accounts, ask product-fit questions, request evidence, or merely react. Record contrary evidence and unanswered objections alongside agreement (directional).

Treat missing alt text, AI labels, or sponsorship information as visibility observations. An absent visible label doesn't establish human authorship, policy compliance, or an undisclosed relationship.

### Assess value without fake precision

Use qualitative assessments; this is an editorial rubric, not a platform ranking model (directional).

| Dimension | Strong evidence | Weak or unavailable evidence |
|---|---|---|
| Distribution | Visible views or owner Insights compared with the same author's similar-age posts | Likes alone, mismatched observation windows, missing baseline |
| Conversation | Relevant questions, distinct contributors, substantive exchanges | Author-only additions, repetitive reactions, unrelated argument |
| Buyer relevance | Fit, adoption, implementation, pricing, or service-availability questions | General applause or broad cultural recognition |
| Reuse value | Clear structure supported by an artifact or documented experience | A result dependent on celebrity, private context, or unverified claims |

Reply-to-like or repost-to-like ratios can describe the sample. State the calculation inputs and leave ratios undefined when the denominator is zero. Don't use universal pass/fail cutoffs or call them primary virality signals.

Retain a small-account example when its structure is relevant; don't discard it solely for modest counts. Separate paid or coordinated activity only when evidence supports that distinction. A busy comment section alone doesn't establish manipulation (directional).

### Describe structures and formats

Name observed structures in plain language: observation, scene, contextual question, evidence-bounded disagreement, demo/artifact, customer outcome, founder decision, objection answer, or recap. Don't rank them as universally winning hooks.

For each useful cluster, describe what the first line does, which supplied detail carries the claim, why the format was needed, and how readers responded. Transfer the structure without copying someone else's experience, voice, or outcome. Don't add a duplicate writing-style blacklist.

Use these qualitative format bands only when the brief requests recommendations (directional):

| Need | Format guidance |
|---|---|
| Observation or contextual question | Brief text: claim plus necessary context. |
| Scene | Brief if the detail stands alone; developed if context is needed. |
| Founder decision or bounded proof | Developed text: add evidence and limitation. |
| Inspectable artifact | Brief or developed caption with an informative image or image sequence. |
| Visible task or transformation | Video with a brief caption, understandable without audio (directional). |
| Necessary depth | Extended text attachment; summarize the point in the root. |
| New information or recurring question | Independently useful self-reply when ready; no prescribed count or delay. |

Standard posts support up to 500 characters and text attachments up to 10,000 characters (official, Meta Text, 2025-09). These are limits, not optimum lengths. No format recommendation should require filling the cap or splitting a coherent sentence.

Media led Buffer's Threads format medians, but format results overlapped (measured, Buffer Engagement, n=2025 Threads subset of Buffer-published posts, 2026-03). Don't translate this into a reach lift, root-link penalty, or instruction to always move links. Record actual link placement and CTA path.

### Timing and interpretation

For general timing hypotheses, weekday 6–11 a.m. local was strongest, with Thursday 9 a.m. the peak in Buffer's sample (measured, Buffer Timing, n=2.5 million posts, 2026-02). Report account evidence and geography before recommending a slot. Don't impose an evening/weekend rule, a fixed judgement window, or delayed self-replies.

Capture repeat observations at comparable post ages when access permits. Distinguish observation timing from a recommendation to publish at that time.

Your Algo introduced private topic preferences with an initial market-limited rollout (official, Meta Communities, 2026-06). Treat feed observations as personalized samples, not a platform census. Meta announced a phase-in of personalized political recommendations (official, Meta Civic, 2025-01); don't describe all political posts as throttled or assert rollout completion.

To assess saturation, compare wording and claims across the sampled niche and time window. Cite examples of repeated framing and any fresh counterexample. Mark saturation unknown when the sample cannot support it; don't keep a static list of supposedly exhausted topics (directional).

### Return the brief

Use the requested output schema. Otherwise return a scope and access note, evidence records, conversation clusters, and implications with their uncertainty. Include source links and capture dates.

For launch research, separate verified buyer objections from inferred demand. Name useful proof formats and any missing source material needed for a future post. Report the observed link or contact path; don't prescribe unsupported messaging, ad, or cross-posting mechanics. Views and conversation describe native response; qualified interest and downstream outcomes require separate evidence.

## Examples

### Artifact with useful replies

Illustrative harvest record; bracketed fields represent observations to fill, not real performance:

> Source: [permalink], [handle], published [time], captured [time and timezone]. Surface: [community and resolved URL]. Views: [visible count or unavailable]. Likes: [count]. Replies: [count]. Reposts: [count]. Quotes: [count].
>
> Structure: demo screenshot with a caption naming the unsupported input. Reader questions concern compatibility. The author answers a limitation in a reply. Buyer relevance: supported by [quoted question and reply permalink]. Distribution: unknown without comparable posts.

This separates source evidence from a performance inference. The future writer needs an equivalent real artifact, not the original author's claim.

### Conversation volume without buying evidence

Illustrative conclusion:

> The post attracted [visible reply count] replies about a design preference. In the inspected replies, no one asked about trial access or product fit. It is useful for audience language; buying intent remains unknown. The sample excludes replies hidden behind [access limitation].

This preserves a useful observation without converting engagement into a sales claim. It doesn't infer a reach penalty from tone or link placement.

## Checklist

- [ ] Scope, timezone, capture window, access limits, and selected surfaces documented.
- [ ] Actual resolved URLs used; no guessed search, feed, profile, tag, or support routes.
- [ ] Post evidence includes timestamps, format, and visible metrics; unavailable fields aren't treated as zero.
- [ ] Owner Insights access is authorized; public visibility isn't assumed to match it.
- [ ] Parent and replies inspected; author activity separated from distinct audience contributions.
- [ ] Distribution, conversation, and buyer relevance assessed separately with comparable baselines where available.
- [ ] No numerical ranking weights, ratio gates, penalties, expiry rules, or resurfacing promises added.
- [ ] Optional recommendations follow verified limits and qualitative bands, with no artificial chain count or delay.
- [ ] Saturation claims cite the current sample; unsupported claims remain unknown.
- [ ] Source experience remains attributed; the brief doesn't fabricate a future author's proof.
- [ ] Research-created tabs closed; pre-existing user tabs preserved.

## References

- [Meta Web](https://about.fb.com/news/2025/04/new-features-threads-web-experience/), 2025-04-24.
- [Meta Introduction](https://about.fb.com/news/2023/07/introducing-threads-new-app-text-sharing/), keyword-search update 2023-09-07.
- [Meta Communities](https://about.fb.com/news/2026/06/meta-launching-new-features-500-million-monthly-threads-users/), 2026-06-16.
- [Meta Personalization](https://about.fb.com/news/2025/03/new-threads-features-more-personalized-experience-you-control/), updated 2025-07-22.
- [Meta Text](https://about.fb.com/news/2025/09/attach-text-threads-posts-share-longer-perspectives/), 2025-09-04.
- [Meta Civic](https://about.fb.com/news/2025/01/meta-more-speech-fewer-mistakes/), 2025-01-07.
- [Buffer Replies](https://buffer.com/resources/threads-comments-engagement/), 2026-02-24.
- [Buffer Engagement](https://buffer.com/resources/state-of-social-media-engagement-2026/), 2026-03-05.
- [Buffer Timing](https://buffer.com/resources/the-best-time-to-post-on-threads/), 2026-02-04.

Re-validate when: domain or navigation changes; metric visibility changes; limits or policies update; Meta publishes ranking details; new vendor reports change the baseline.
Validated: 2026-09
