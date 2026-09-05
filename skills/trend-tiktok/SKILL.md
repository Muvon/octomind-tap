---
name: trend-tiktok
title: "TikTok Trend Harvester Playbook"
description: "Harvest TikTok trend evidence into a source-linked brief with audience fit, observed momentum, original angles, and commercial-use constraints. Activate for TikTok trend scans, Creative Center research, and browser-based campaign discovery; separate observed posts from ad examples and generated suggestions."
license: Apache-2.0
compatibility: "Requires browser and network access; authenticated TikTok business or publishing account access when a surface requires it."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(tiktok)
  - match(\btiktok\s+(trend|trends|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+tiktok\b)
  - session(trend) match(\bcreative\s+center\b)
---

## Overview

Collect inspectable TikTok evidence for a specific audience and buying situation. Return source-linked candidates with momentum, limitations and an original contribution; drafting and publishing are downstream work. Reuse prior observations only when their timestamp and filters are known.

## Mental model

Separate observed posts, commercial examples and generated suggestions. A popular post is evidence of attention; it does not establish retention, conversions or the cause of its distribution.

TikTok's historical explainer says follower count and prior hits are not direct recommendation factors (official, TikTok recommendation explainer, 2020-06). That does not make views divided by followers a pure algorithm score. Account history and outside exposure remain possible explanations; don't infer current launch-pool rules from that old explainer.

Use chart changes and new relevant executions to assess momentum. A post-level reach window does not establish a trend's expiration date. Classify sound-dependent versus reusable-format candidates to decide what needs rechecking before production (directional).

## Harvest procedure

### Establish the scope

Record target country, language, niche, buyer situation, account type, and whether the brief is organic, commercial or paid. Clarify what decision the harvest must support: topic selection, an opening, a demo format, a creator shortlist, or an objection-answer post.

Read prior observations for matching filters when available. Don't write to persistent memory unless that workflow is authorized; return reusable observations in the brief otherwise.

### Navigate from verified entry points

| Surface | Entry and use |
|---|---|
| TikTok One Creative Suite | Start at `https://ads.tiktok.com/creative/creativeCenter` and open the current Trends surface. Trends and Symphony Creative Studio are exposed here (official, Creative Suite, undated; verified 2026-09). |
| Trend charts | Follow live navigation for available topics, hashtags or music; record the actual URL, displayed filter labels and selected values. Don't assume every surface supports country, industry and period filters. |
| TikTok in-product discovery | Navigate search and open relevant results, then follow their tag, sound or profile links. Save the resolved URLs. Avoid constructed route templates or assuming logged-out access. |
| Keyword-related surfaces | Use a keyword tool only if present and its metric definition is visible. Record whether it describes paid creative, organic queries or something else; don't substitute ad keyword performance for organic search demand. |
| Content Suite | If authorized access is available, inspect existing brand-relevant UGC using AI Search, Projects and Creators (official, Content Suite announcement, 2026-06). Keep permission status separate from discoverability. |
| Symphony Creative Studio | Symphony Agent can generate briefs and ads from campaign prompts and trend/top-ad insights (official, Product Preview, 2026-07). Treat output as suggestions to verify against actual posts, never as observed examples. |

Use the current root navigation when an old URL fails, redirects, or shows a different page. Record the final destination and access state. If navigation or labels have changed, describe the surface actually observed; don't claim a specific redirect history without observing it. If access is blocked, mark that coverage unavailable and continue with accessible evidence. Don't invent missing chart values.

Render the page before extracting it. Record session market and login state without collecting credentials. Close only the research tabs you opened when finished.

The Commercial Music Library is described as supplying paid-ad-cleared tracks and an approved-for-business-use filter in the ad playbook (official, SMB Playbook, undated; verified 2026-09). Record the current rights/filter wording and selected track's permissions. Popularity is not commercial clearance. Do not assume the legacy label still appears on every chart.

### Capture source records

For each candidate, record:

- Observation timestamp, resolved URL, handle, publication date or displayed age, and language/market context.
- Visible views and engagement counts, follower count when visible, duration and format. Mark unavailable data explicitly rather than estimating it.
- Exact hook transcription, first-frame description, overlay wording, caption, sound attribution and the visible disclosure state.
- Account's comparable recent posts; whether the candidate is a paid example, creator post, or ambiguous. Mark outside promotion unknown when unobservable.
- Relevant comment excerpts with enough context to explain the buyer's question; omit unnecessary personal information.
- Source surface, filters and metric definitions, including whether counts are rounded or collected at different times.

Label harvested numbers inline as (measured, live TikTok observation, n=observed sample scope, observation month); insert the actual scope and date. Keep exact timestamps in the record. Use (official, source name, publication or verification month) for documented mechanisms and (directional) for editorial interpretations without numerical claims.

### Compare and cluster

Cluster by the shared creative device and viewer problem, not merely a repeated tag. Classify sounds, formats/memes, challenges, effects or topics as editorial categories; these are not a claim about the current UI tab names (directional).

| Dimension | Inspect | Don't infer |
|---|---|---|
| Momentum | Comparable chart snapshots and new relevant executions | A universal lifecycle from the age of a top post |
| Relative attention | Views/follower context and the account's normal range | Causal recommendation strength or genuine engagement |
| Discussion quality | Comments with use cases, objections or specific requests | Buyer intent from comment count alone |
| Relevance | Fit to the supplied audience and proof the author can show | Product demand from global popularity |
| Original contribution | A niche-specific demonstration, evidence or substantive response | Permission to copy an execution |
| Production readiness | Available footage, rights and usable sound | That a trend ranking grants a commercial license |

Compute views/follower or comments/views only when visible counts and denominators are usable; disclose rounding and observation time. Compare similar account contexts and post ages. Never use length multiplied by views as a completion proxy; public views do not reveal completion.

Use ordinal decisions: recommend, watch, or reject. Recommend when relevant evidence and a feasible original execution support the brief; watch when momentum or rights remain uncertain; reject when fit or source quality fails. Avoid fabricated score thresholds (directional).

### Assess freshness without a deadline myth

Compare observed chart direction with recent independent executions. Explain disagreements instead of forcing a verdict. A falling chart with fresh niche-specific examples may still support a useful post; a high rank without recent evidence may need another observation (directional).

Call a candidate crowded when the sampled executions repeat the same device without a useful new angle. Report that as a sample-bound judgment. Don't convert it into a platform saturation penalty, use a fixed age cutoff, or claim the feed reserves a fixed number of same-sound slots (directional).

### Apply originality and commercial gates

Name the author's proposed original layer and any missing asset permission. Reused material without creative edits can be For You-ineligible (official, Integrity and Authenticity, 2025-08). Re-verify the current regional rule when a recommendation depends on it.

Capture disclosures and possible rights issues as observations, not enforcement verdicts. Distinguish public visibility from eligibility to republish, advertise or monetize. Don't fill the harvest with duplicated penalty lists or infer an AI-label reach effect from high or low views.

For campaign seeding, prioritize relevant existing creator contributions over a scripted wave of identical comments (directional). Fake engagement and repetitive irrelevant posting are covered by TikTok's authenticity rules (official, Integrity and Authenticity, 2025-08).

### Return a usable brief

Include the audience/job, coverage and access gaps, candidate clusters, source records, observed momentum, proposed original angle, hook bank derived from visible structures, commercial constraints and the next recheck condition. Keep exact quotes separate from adapted hooks, and mark a proposed hook as unpublished craft (directional).

For launch research, identify real objections, demonstrable use cases, relevant creators, and which source asset could support each recommendation. Don't invent customer outcomes or convert campaign case studies into forecast returns. Give the writer the evidence and its limitations; don't draft an entire launch calendar during a harvest.

## Examples

### A rising sound with incomplete clearance

Illustrative brief, not live observations (directional):

- Scope: [market], [buyer situation], observed [timestamp].
- Evidence: [sound URL]; chart moved from [earlier rank] to [current rank] using [matching filters]. Recent niche examples: [post URLs].
- Interpretation: sound-dependent candidate; recent executions address the supplied audience, but the commercial-use status isn't verified.
- Decision: watch pending clearance. Proposed original layer: demonstrate the author's actual packing problem in the sound's pause; use owned speech if music permission remains unresolved.

This separates chart evidence from rights and leaves missing observations explicit. It does not turn rank movement into a deadline.

### High views without retention evidence

Illustrative brief, not live observations (directional):

Source: [post URL], with [displayed views] at [timestamp]. Duration: [displayed duration]. Comparable posts: [URLs and visible counts]. Comments include [verbatim relevant excerpt].

Conclusion: relative attention is observable; completion and sales are unknown. Recommend inspecting the opening and the visible demonstration. Do not call the duration/view combination a retention win.

## Checklist

- [ ] Market, audience, buyer situation and commercial scope are explicit.
- [ ] Live entry points and resolved URLs are recorded; missing or renamed surfaces and access gaps are disclosed.
- [ ] Chart comparisons use matching filters and known observation times.
- [ ] Every quoted hook and number traces to a source record; absent data remains unknown.
- [ ] Organic posts, paid examples and generated suggestions are distinguished.
- [ ] Relative metrics have usable denominators; no completion proxy, fixed trend expiry or invented scoring threshold appears.
- [ ] Each recommendation names its original contribution, evidence, rights status and recheck condition.
- [ ] The brief contains relevant objections and usable hook structures without invented author experience.
- [ ] Commercial music and regional policy checks are identified where needed; no popularity-to-permission inference remains.
- [ ] Reusable observations are returned or stored only as authorized; research tabs are closed.

## References

- [TikTok One Creative Suite](https://ads.tiktok.com/creative/creativeCenter), undated, verified 2026-09.
- [SMB Playbook](https://ads.tiktok.com/business/library/Global_SMB_Creative_Playbook.pdf), undated, verified 2026-09.
- [Content Suite announcement](https://ads.tiktok.com/business/en/blog/content-suite-creator-ugc-library?redirected=1), 2026-06-22; [Product Preview](https://ads.tiktok.com/business/en/blog/tiktok-product-preview), 2026-07-28.
- [TikTok recommendation explainer](https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you?lang=en), 2020-06-18; [Integrity and Authenticity](https://www.tiktok.com/community-guidelines/en/integrity-authenticity), 2025-08-14.

Re-validate when: URLs redirect or navigation/filter labels change; login or regional access changes; music permissions change; recommendation or authenticity guidance changes.
Validated: 2026-09
