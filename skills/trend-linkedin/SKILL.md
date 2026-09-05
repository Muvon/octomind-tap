---
name: trend-linkedin
title: "LinkedIn Trend Harvester Playbook"
description: "Harvest LinkedIn posts and conversations into a sourced brief for a specific audience. Activate for LinkedIn trend scans or research briefs; capture current surfaces, buyer questions, format patterns, and evidence limitations without inventing ranking weights."
license: Apache-2.0
compatibility: "Octoweb browser access and network. Signed-in LinkedIn session for personalized feed and search."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(linkedin)
  - match(\blinkedin\s+(trend|trends|harvest|brief|research)\b)
  - match(\b(harvest|scan|analyze)\s+linkedin\b)
---

## Overview

Collect evidence of what relevant LinkedIn audiences are discussing and how posts deliver useful substance. Return source-linked observations and bounded opportunities; drafting and publishing are downstream steps. Preserve the distinction between a public observation, a study result, and a craft inference.

## Mental model

LinkedIn uses profile information and interaction history in retrieval and ranking; it publishes no universal comment multiplier or single dominant signal (official, LinkedIn Feed Engineering, 2026-03). Public engagement cannot reveal dwell time, private conversions, or why a ranker distributed a post. Don't infer those from length or paragraph rhythm (directional).

Keep personal profiles separate from Company Pages. Metricool found similar impressions per post, but profile engagement averaged 2.60% versus 1.60% for Pages (measured, Metricool, n=673,658 posts from 63,108 accounts, 2026-04). Account type belongs in every comparison.

## Harvest procedure

### Establish scope and surfaces

Record the audience, professional problem, campaign stage if supplied, language, target geography/timezone, and observation window. Include practical alternatives to the favored product or thesis. Distinguish exact quotes from paraphrases and redact private material (directional).

Start from the signed-in interface and follow controls actually present. The entry URL below is a navigation starting point, not a guaranteed harvest API; record redirects and unavailable controls (directional).

| Surface | Entry and procedure | What to record |
|---|---|---|
| Personalized feed | Open `https://www.linkedin.com/feed/`; confirm the loaded surface before scanning | Signed-in context, visible filters, suggested versus followed sources where labeled |
| Topic search | Use the current search box, select Posts if offered, then inspect available sort/date filters | Query, displayed filter names, resulting URL and timestamp; never assume a date filter was applied |
| Creator or expert activity | Open a discovered profile and follow its visible Activity/Posts controls | Actual activity URL, time span inspected, visible account context |
| Company Page | Follow the current Page's posts, event, or publication controls | Page identity, original versus employee/customer contribution, format |
| Article / Newsletter / Event | Follow a visible source link from a relevant account or post | Actual URL, publication/event date, authorship, availability restrictions |

Don't construct hashtag-feed URLs or hard-coded `sortBy` parameters. If a deep link fails, return to the current UI and record the failure; don't silently substitute a different query. Treat hashtags as searchable text only when the current interface supports the operation (directional).

Scan independent sources where available; scroll until additional items stop changing the evidence or the requested scope is met. Avoid a fixed scroll quota. If login, pagination, or access controls block the sample, return a partial brief with the boundary stated (directional).

### Capture evidence

For each candidate, record the canonical post URL; author/account type; posted time and observation time; visible follower context; format; link placement; and public reaction, comment, and repost counts. Use “not visible” for inaccessible fields. Inspect the actual asset and a relevant slice of replies; label that slice's scope (directional).

Capture the opening exactly within quotation limits and note what was visible before expansion on the observed client. Don't assign a fixed mobile character fold. Record total length only if the full text was accessible; it doesn't prove dwell time (directional).

Inspect buyer substance: the problem being discussed, proof provided, stated conditions, credible objections, and the requested action. Separate author replies from independent participants where visible. A comment asking about integration, applicability, or access can indicate evaluation; it isn't a verified lead (directional).

Record hashtags, relevant mentions, collaboration labels, sponsorship, and visible Content Credentials without inferring hidden status. Credentialed media can display a provenance icon; absent icons don't establish human origin (official, LinkedIn Credentials Help, 2026-09 review, undated).

### Compare and prioritize

| Dimension | Prefer | Preserve limitation |
|---|---|---|
| Audience fit | A clearly relevant buying situation and identifiable professional context | Titles and badges don't validate expertise |
| Evidence quality | Inspectable work, source-linked outcomes, conditions and counterexamples | A claim in a post remains the author's claim |
| Conversation | Independent questions or reasoned disagreement that affect a decision | Raw comment totals may include author replies |
| Relative response | Comparable account type, format, audience size, post age, and visible history | Public counts don't expose impressions or causal lift |
| Reusable pattern | A task, proof structure, or unanswered question that fits the brief | Don't copy the author's lived experience or sentence template |

The rubric is directional. Use “prioritize,” “watch,” or “insufficient evidence,” with a reason. A comment-to-reaction ratio may describe the observed sample, but supplies no breakout threshold or ranking weight. Leave it undefined when reactions are absent. Don't divide by an invented follower count, infer a reach rate from reactions, or label reaction diversity an algorithmic signal.

### Interpret formats and distribution

Documents and multi-image posts are useful testing candidates, while video has no universal advantage (measured, Metricool, n=673,658 posts, 2026-04; AuthoredUp Formats, n=3M+ personal-profile posts, 2026-09). Capture what the asset demonstrates. Don't prescribe slide counts or a video-duration optimum from format alone (directional).

Polls aren't categorically dead: Socialinsider reports 4.50% engagement in its Q2 table, but its methodology dates conflict with that period (measured, Socialinsider, n=1.3M business posts, 2026-03). Keep that caveat with the claim; prioritize the account's observed outcomes over a cross-vendor leaderboard (directional).

Standard posts allow 3,000 characters; Articles are a separate long-form feature (official, LinkedIn Post Help, 2026-08). Never call a long feed post an Article. Record Newsletter or Event formats only when the source identifies them; don't infer current Audio Events availability from old content (directional).

Link-post impressions/interactions differed by account type: profiles −27%/−20%, Pages +51%/+41% (measured, Metricool, n=673,658 posts, 2026-04). This doesn't test whether a first-comment link is safer. Describe link placement without assigning a penalty (directional).

Half of impressions arrived within 48 hours in Metricool's cohort, not a hard feed expiry (measured, Metricool, n=673,658 posts, 2026-04). Replying correlated with about 30% higher engagement (measured, Buffer Replies, n=72,000 LinkedIn posts, 2025-12). Record observed timestamps; don't infer a required reply count or minute cutoff.

If timing is requested, offer audience-timezone tests. Buffer found a 3–8 PM window, with Wednesday 4 PM and Friday 3–4 PM strongest (measured, Buffer Timing, n=4.8M+ posts, 2026-07). Rotate global-audience tests and compare like-for-like material (directional). Don't impose a daily maximum: Buffer's LinkedIn frequency analysis found gains at higher cadence (measured, Buffer Timing, n=2M posts, 2026-07).

Creator Mode's toggle was removed in March 2024 (official, LinkedIn Creator Mode Help, 2024-03). Verified-member filtering exists in feed conversations and comments (official, LinkedIn Authenticity, 2026-06). Record any active filter as sampling bias; assign no Premium, verification, or Top Voice reach multiplier.

## Bias and integrity checks

Relevance-ranked search and a signed-in feed aren't a platform census. Report surfaces and filters, plus inaccessible material. Compare repeated angles across unrelated sources before calling an idea saturated; don't maintain a static dead-take list (directional).

LinkedIn acts on scaled automated comments and restatement-only replies, and reduces wider distribution for apparently AI-generated posts without perspective (official, LinkedIn Authenticity, 2026-06). Flag observable duplication or empty discussion without declaring authorship from style. Exclude suspicious activity from recommendations only with a stated observation and uncertainty (directional).

Don't borrow another platform's engagement definition. Public counts omit useful LinkedIn clicks and media activity (measured, Metricool Press, n=673,658 posts, 2026-04). Request authorized analytics if the brief requires qualified traffic or conversion claims; otherwise mark those outcomes unavailable.

## Examples

### Evidence note without a ranking story

Illustrative schema; every bracketed field requires source capture:

> Source: [post URL], observed [timestamp/timezone]. Author: [name], personal profile. Published: [source time]. Format: native document. Public counts: [reactions], [comments], [reposts].
>
> The opening names an invoice-review problem. The document shows assignment rules; the inspected replies ask about exceptions. The author explains the manual fallback. The source gives no verified conversion result. Prioritize the unresolved exception question for the brief; don't infer dwell time from the document format.

Why it works: the comparison rubric prioritizes buyer relevance and inspectable substance.
The note separates observed conversation from unavailable business outcomes.

### Bounded trend finding

Weak, illustrative: “Carousels are winning; use more of them.”

> In [observed sample], document posts explained approval workflows, while multi-image posts showed completed installations. These serve different reader tasks. [Source URLs] support the distinction. The sample came from [surface and filters], so it doesn't establish a platform-wide format shift.

Why it works: the harvest procedure preserves asset purpose and sample scope.
The brief supplies a writing opportunity without copying a hook or claiming an algorithm preference.

## Checklist

- [ ] State audience, window, language, timezone, surfaces, filters, and access limits.
- [ ] Every cited post has its actual URL, account type, observation time, source date, and visible counts or explicit unavailable fields.
- [ ] Inspect assets and relevant comments; distinguish author claims from verified outcomes.
- [ ] Capture openings as observed; don't assume a fixed fold, date-filter behavior, or hashtag feed.
- [ ] Compare account type, post age, format, and visible baseline before prioritizing.
- [ ] Label study claims with cohort/date; qualify format mix as the observed sample.
- [ ] Keep missing metrics unknown; no hidden dwell, conversion, badge uplift, or breakout-threshold claims.
- [ ] Record disclosure/credential observations without making authorship accusations.
- [ ] Return sourced opportunities and unresolved buyer questions; remove duplicated hook and dead-pattern prescriptions.
- [ ] Close only tabs opened for this task and preserve the user's session.

## References

- [LinkedIn Feed Engineering](https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed), 2026-03-12; [Post Help](https://www.linkedin.com/help/linkedin/answer/a528176), 2026-08.
- [LinkedIn Authenticity](https://news.linkedin.com/2026/keeping-conversations-real-on-linkedin), 2026-06-04; [Creator Mode Help](https://www.linkedin.com/help/linkedin/answer/a5999182), 2024-03; [Credentials Help](https://www.linkedin.com/help/linkedin/answer/a6282984?lang=en), undated, reviewed 2026-09.
- [Metricool](https://metricool.com/linkedin-trends/), 2026-04-16; [Metricool Press](https://metricool.com/press-release-linkedin-study-2026/), 2026-04-14.
- [AuthoredUp Formats](https://authoredup.com/blog/best-performing-content-on-linkedin), 2026-09-02; [Socialinsider](https://www.socialinsider.io/social-media-benchmarks/linkedin), 2026-03-16, period/methodology conflict retained.
- [Buffer Replies](https://buffer.com/resources/linkedin-engagement-data/), 2025-12-04; [Buffer Timing](https://buffer.com/resources/best-time-to-post-on-linkedin/), 2026-07-22.

Re-validate when search/filter URLs or feature names change; feed engineering or disclosure policies update; new vendor reports revise cohorts or findings.
Validated: 2026-09
