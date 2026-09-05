---
name: trend-mastodon
title: "Mastodon Trend Harvester Playbook"
description: "Harvest Mastodon posts and topic conversations into a sourced, server-scoped brief. Activate for Mastodon or Fediverse trend scans and harvesting requests. Verify accessible surfaces, preserve sampling limits, and distinguish observed participation from inferred spread or writing recommendations."
license: Apache-2.0
compatibility: "Octoweb browser access and network access. A signed-in session may be needed for restricted server surfaces."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(mastodon)
  - session(trend) content(fediverse)
  - match(\b(mastodon|fediverse|fedi)\s+(trend|trends|harvest|brief|post|toot)\b)
  - match(\b(harvest|scan|analyze)\s+(mastodon|fediverse)\b)
---

## Overview

Return a reproducible brief of what relevant people are discussing, the evidence they share, and questions a downstream writer could address. Preserve the actual author's words and source URLs; publishing is a downstream step. Scope findings to the observed servers and retrieval period.

## Mental model

Home includes followed accounts and followed hashtags; public timelines support local filtering and may restrict access (official, Timelines, 2026-05). Explore/Trends uses a periodically recalculated internal score: status interactions, tag usage, and link sharing. Don't describe it as algorithm-free or boost-only (official, Trends, 2026-05).

Full-text search depends on server setup. Direct lookup and library search also exist; don't infer that untagged posts are invisible or assert an indexing default (official, Network, 2025-11). A favourite notifies the author without resharing; a boost reshares (official, Network, 2025-11). Neither a ratio nor appearance on different servers proves the path a post travelled.

Quiet public is excluded from public feeds, Explore, and search while remaining profile-visible and eligible for Home; reply delivery normally requires following both participants (official, Posting, 2026-07). A harvest of discoverable public material isn't representative of every conversation.

## Harvest procedure

### Establish scope

Identify the home server, topic, audience, language, intended buying situation, and observation period from the brief. Record software and accessible surfaces before applying Mastodon paths to a Fediverse host. Select other servers from actual relevant participants and topic activity, not an undated category roster (directional).

Read the posting server's current rules when the brief requests downstream opportunities. Independent servers have their own policies; the operated-server terms apply only to mastodon.social and mastodon.online (official, Server terms, 2026-07). Record commercial and AI-content restrictions by URL and scope; don't infer them from a server's niche.

### Resolve surfaces and harvest

Resolve API paths below against the verified server origin. For browser work, follow the links actually exposed by that server and record the resulting URL. Don't hard-code legacy web routes or treat the root landing page as a trends page (directional).

| Surface | Verified entry or discovery procedure | Record |
|---|---|---|
| Trending posts | `/api/v1/trends/statuses` (official, Trends, 2026-05). | Ranked candidates and retrieval time. |
| Trending tags / links | `/api/v1/trends/tags` and `/api/v1/trends/links` (official, Trends, 2026-05). | Relevant topics and primary-source links; retain surface type. |
| Local public timeline | `/api/v1/timelines/public?local=true` (official, Timelines, 2026-05). | Accessible local material; access restrictions if present. |
| Public timeline | `/api/v1/timelines/public` (official, Timelines, 2026-05). | The queried server's results, without calling them a global census. |
| Topic timeline | Append the URL-encoded tag to `/api/v1/timelines/tag/` (official, Timelines, 2026-05). | Recent relevant posts and observed URL. |
| Profiles and conversations | Follow actual author and conversation links returned by the interface (directional). | Original post, reply context, profile, and relevant proof. |
| Collections | Inspect exposed Featured links; Collections have shareable URLs and manual discovery (official, Release, 2026-06). | Curator and relevant opt-in participants; no inferred endorsement. |

A configurable institutional landing page can emphasize server description and recent local-profile updates rather than Trending (official, Release, 2026-06). Keep it as a separate culture surface.

Public and hashtag timeline pagination has a documented default of 20 and maximum of 40 results (official, Timelines, 2026-05). Follow the current documented pagination controls, record the requested and returned counts, and continue until the chosen time cutoff or research budget. Don't assume a snapshot completes a feed. For other surfaces, inspect their own pagination rather than transferring those limits (directional).

When access fails, record the response and authentication state; use an authorized session or another accessible surface. Don't bypass restrictions. An empty page can reflect visibility or access, so report “no relevant posts observed in this sample,” not “dead tag” (directional).

### Preserve evidence

For each selected post, capture the following fields. Use “not observed” for missing values; don't replace them with inferred counts (directional).

| Field group | Contents |
|---|---|
| Identity | Canonical post URL, full federated handle, source server, profile URL. |
| Sampling | Retrieval timestamp and timezone, publication time, queried server, exact surface URL, pagination boundary. |
| Content | Faithful excerpt, topic, format, language, tags, CW, visibility when observable, source/artifact link. |
| Interactions | Displayed boosts, favourites, replies, and quotes; specify observation time and interface. |
| Conversation | Relevant external replies, author self-replies, questions, objections, participants' servers, and actual contribution. |
| Accessibility | Presence and usefulness of media descriptions; distinguish missing metadata from inaccessible inspection. |
| Spread | Each observed server appearance; evidence for any specific boost event. Keep causal path unknown unless documented. |

Deduplicate the same post across surfaces by its canonical URL. Report appearances separately from unique posts. Keep raw excerpts distinct from paraphrases; label interpretation as inference (directional).

Attach sample scope to quantitative summaries using the form “measured, named capture, n=observed sample size, capture month.” Preserve the underlying URLs and calculations. Never label a sample “measured” without a reproducible capture.

### Assess relevance without fake virality thresholds

Compare similar topics and formats at comparable post ages. Prefer evidence relevant to the intended audience over raw popularity. Use qualitative assessments of niche fit and qualified interest; explain each with a cited excerpt or reply (directional).

| Observation | Permitted interpretation |
|---|---|
| Same canonical post on different servers | Cross-server appearance observed; route and causal contributor remain unknown. |
| Relevant people discuss implementation or buying constraints | Candidate qualified-interest evidence; don't infer a purchase. |
| Author adds installments | Explanatory depth; keep separate from independent participation. |
| Numerous reactions with sparse discussion | Visible reaction pattern; no conversion or accessibility-penalty inference. |
| Unavailable view count | Leave it unobserved; don't invent impressions or a reach denominator. |
| A tagged topic repeats | Inspect whether the evidence or audience question is new before calling it saturated. |

A crisis-discourse study associated external replies with wider and more diverse cascades; mention and URL predictors also produced overestimation errors (measured, Discussion study, n=54,333 seed posts, 2026-05). It supports inspecting conversations, not reverse-engineering a sales formula.

Buffer's Mastodon image/video medians exceeded link/text medians modestly; its Mastodon subsample is undisclosed and it offers no Mastodon timing window (measured, Buffer, n=Mastodon subsample undisclosed, 2026-03). Don't prescribe fixed boost ratios, follower cutoffs, ET posting windows, or a federation maturation period.

### Return opportunities only when requested

Separate harvested evidence from optional writing hypotheses. For each hypothesis, identify the unmet question, usable proof, relevant live tags if any, and a limitation. Choose tags by topical need, not account-size quotas. Use the audience's observed timezone and account history for timing experiments; label recommendations directional (directional).

For requested campaign research, capture these inputs for a downstream [Mastodon posting handoff](../social-mastodon/SKILL.md); leave unavailable inputs unresolved (directional).

| Input | Harvest record |
|---|---|
| Campaign stage and opportunity | Supplied stage; requested launch, demo, proof, founder account, or objection angle; source question and faithful excerpt separate from the writing hypothesis. |
| Proof and destination | Artifact URL, what it demonstrates, its limits, and the supplied destination; distinguish observed evidence from an unverified claim in the brief. |
| Relationship and policy | Speaker's supplied affiliation; posting server's promotion and disclosure rules with URL, retrieval date, and scope; unresolved permission checks. |
| Timing and replies | Launch-period observations with timestamps and comparable post ages; audience timezone if observed; supplied reply owner or an unresolved assignment. No inferred posting schedule. |

Record actual CW practice alongside local policy; don't declare politics, promotion, or ordinary technical content universally CW-required or exempt. Media descriptions are optional but recommended in Mastodon; absence doesn't establish automatic blocking (official, Posting, 2026-07).

When quotes matter, record the source post's permissions. Anyone is the documented default, with followers or Just me restrictions and revocation controls (official, Quote posts, 2025-11). Don't infer that most authors disable quotes.

Identify relevant ecosystem curators through their public contributions. Collections require discoverability opt-in, notify additions, allow self-removal, and have a cap of 25 with no follow-all (official, Release, 2026-06). A curator list is research output, not authorization to contact people or coordinate boosts.

## Examples

### Cross-server appearance without a causal story

Illustrative reporting pattern, not an observed campaign:

> The canonical post appears on the queried home-server Trends surface and a relevant topic surface elsewhere. The accessible thread contains a question about deployment constraints. No boost event connecting those appearances was captured. Treat the question as an objection to investigate; the route remains unknown.

In an actual brief, attach the canonical URL, surface URLs, timestamps, and the quoted question. Don't promote co-occurrence into a federation-breakout claim.

### Inaccessible hashtag surface

Illustrative reporting pattern:

> The tag surface requires authentication in the available session. Current activity and follower coverage weren't observed. The accessible profile post links to a useful artifact, but it cannot establish that the tag is active.

Return the access limitation and available source. Don't recommend the tag as verified or replace the missing sample with a guessed tag size.

### Artisan topic capture with a reproducible denominator

Illustrative fictional capture, not a measured platform result. All URLs and timestamps below are unresolved placeholders; this example is unpublishable as evidence.

| Canonical post URL | Exact queried surface URL | Retrieved at, including timezone | Asks about glaze durability? |
|---|---|---|---|
| `https://[maker-server]/@[author-a]/[post-a]` | `[topic-surface-url]` | `[capture-time-a]` | Yes |
| `https://[maker-server]/@[author-a]/[post-a]` | `[other-server-surface-url]` | `[capture-time-b]` | Yes; duplicate appearance |
| `https://[buyer-server]/@[author-b]/[post-b]` | `[topic-surface-url]` | `[capture-time-c]` | No |
| `https://[craft-server]/@[author-c]/[post-c]` | `[topic-surface-url]` | `[capture-time-d]` | Yes |

Fictional arithmetic: deduplicate by canonical URL to obtain 3 unique posts from 4 appearances. The denominator is every unique post in this illustrative capture; the numerator is the 2 posts coded Yes. The sample share is `2 / 3 × 100 ≈ 66.7%`. It describes captured questions, not the share of buyers with that concern.

For a real capture, retain the excerpts supporting each coding decision, full handles, publication times, observation window, and pagination boundaries. Replace every placeholder and label the recomputed result “measured, [capture name], n=[unique posts], [capture month]” only after the underlying capture is reproducible.

### Local repair-service objection handoff

Illustrative research output for a requested launch brief; all source fields are unresolved placeholders and unpublishable until verified.

| Handoff field | Research output |
|---|---|
| Observed question | “[Can you assess a repair from a photo before I visit?]” — preserve the actual excerpt at `[canonical-question-url]`, retrieved `[timestamp and timezone]`. |
| Supplied proof | `[service-intake-page]` describes photo submissions. Check its text before using it as proof; accepting photos alone does not establish diagnosis accuracy, price, or turnaround. |
| Promotion and disclosure checks | Record `[posting-server-rules-url]`, `[retrieval date]`, relevant commercial and disclosure clauses, and the supplied speaker relationship. Permission remains unresolved until checked for this server. |
| Directional opportunity | Investigate a photo-intake explanation answering the observed question, with the verified intake page as destination and its assessment limits retained (directional). |
| Reply handoff | `[supplied reply owner]` and unresolved service questions; return to the requester without publishing or contacting the questioner. |

## Checklist

- [ ] Server, software, scope, observation period, language, and access state recorded.
- [ ] Surface URLs verified; pagination and sample boundaries explicit.
- [ ] Each cited post has a canonical URL and full federated handle; repeated appearances deduplicated.
- [ ] Displayed counts timestamped; unavailable data remains unobserved.
- [ ] Independent participation separated from self-replies; boost routes asserted only with evidence.
- [ ] Media descriptions, CW, and relevant policy recorded without invented penalties.
- [ ] Tag activity verified within stated scope; empty or restricted samples aren't labeled globally dead.
- [ ] Optional recommendations distinguish evidence from directional hypotheses; no fixed virality or timing thresholds.
- [ ] Sources and calculations support every measured summary; no invented proof or customer outcomes.
- [ ] Only research-created browser tabs closed; preserve the user's existing tabs.

## References

- [Timelines](https://docs.joinmastodon.org/methods/timelines/) and [Trends](https://docs.joinmastodon.org/methods/trends/), 2026-05.
- [Network](https://docs.joinmastodon.org/user/network/) and [Quote posts](https://docs.joinmastodon.org/user/quote-posts/), 2025-11.
- [Posting](https://docs.joinmastodon.org/user/posting/), 2026-07.
- [Release](https://blog.joinmastodon.org/2026/06/mastodon-4.6/), 2026-06.
- [Server terms](https://blog.joinmastodon.org/2026/07/announcing-new-terms-of-service-for-our-servers/), 2026-07.
- [Buffer](https://buffer.com/resources/state-of-social-media-engagement-2026/), 2026-03, Mastodon subsample undisclosed.
- [Discussion study](https://ojs.aaai.org/index.php/ICWSM/article/download/42774/50334/46875), 2026-05, crisis-discourse population.

Re-validate when web routes, access policies, pagination, or UI labels change; when discovery features ship; when ranking code or benchmark reports change.
Validated: 2026-09
