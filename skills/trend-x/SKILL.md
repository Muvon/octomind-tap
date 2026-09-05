---
name: trend-x
title: "X (Twitter) Trend Harvester Playbook"
description: "Harvest X conversations into a sourced topic brief. Activate when asked to scan Twitter or X trends, buyer pains, launch reactions, or post formats. Validate live surfaces, compare relevant accounts with explicit metric limits, and distinguish observed patterns from ranking hypotheses."
license: Apache-2.0
compatibility: "Browser and network access. Use an authorized signed-in X session where required; search availability must be checked in the current session."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(x)
  - session(trend) content(twitter)
  - session(trend) match(\btweet)
  - match(\b(x|twitter)\s+(trend|trends|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+(x|twitter)\b)
---

## Overview

Harvest source posts and conversations into a brief that supports a writing or go-to-market decision. Capture the topic, audience, observation window, and buying situation before browsing. Return source evidence and uncertainty; publishing and copywriting are downstream work.

## Mechanics and mental model

For You combines followed-account candidates from Thunder with Phoenix retrieval and SimClusters for out-of-network discovery. Ranking orders candidates; visibility filtering separately returns allow, interstitial, or drop. The documented candidate path filters out-of-network replies and reposts and posts older than 48 hours (official, X algorithm README, 2026-08). Don't extend this cutoff to every X surface.

Treat For You as a personalized sample. Record the session context and compare it with topic searches and relevant account histories (directional). Replies can expose buyer language in a conversation; don't describe them as a guaranteed For You discovery mechanism.

A conditional new-author lift exists for originals; it excludes replies and reposts (official, X cold-start, 2026-08). Eligibility includes at most 1,000 followers and fewer than 1,000 impressions alongside further checks (official, X cold-start, 2026-08). Don't attach a universal boost multiplier to small accounts.

Published weights multiply predicted actions, not observed engagement counts. Repeated-author scoring operates within a feed request; it supplies no daily posting quota (official, X parameters, 2026-08). Public engagement ratios don't reveal predicted non-dwell, private shares, or a post's score. Bookmarks can indicate reader utility when available, but this evidence establishes no current bookmark weight. Don't describe them as either a proven boost or a proven non-signal.

## Harvest procedure and surface decisions

### Establish access and scope

Use the campaign's topic vocabulary and buying problem. Include exact problem phrases alongside product and competitor names. Preserve the audience's language without assuming every complaint signals purchase intent (directional).

The supplied verified evidence doesn't certify search operators, deep-link tab URLs, logged-out search access, or Explore labels. Treat the following as navigation procedures, not confirmed endpoint contracts. Start from `https://x.com` and inspect the live UI; don't fabricate a working URL or bypass an access gate.

| Needed evidence | Navigation procedure | Validation before use |
|---|---|---|
| Current topic discussion | Open Search through the visible interface; enter the topic; select the newest-results tab if offered | Record the actual URL and visible tab label; inspect timestamps |
| Ranked topic sample | Select the available ranked-results tab | Record that ranking can bias the sample; don't call it the full population |
| Explore or trending topics | Open Explore from navigation, then the visible trends surface | Record locale and personalization settings when visible; don't call it global |
| Account comparison | Open a relevant author's profile from a source post or supplied link | Confirm the account and inspect posts within the chosen window |
| Curated niche listening | Open an authorized List through the visible Lists interface or a supplied link | Record list selection and membership bias |
| Event discussion | Search the event name and inspect a relevant hashtag if present | Check event dates and relevance; a tag alone doesn't prove participation |
| Buyer pain and objections | Search exact problem language; inspect roots and full reply chains | Distinguish firsthand reports, product pitches, and copied claims |
| Format-specific material | Use available media filters and inspect the source posts | Record actual format, account access, and truncation |
| Reach diagnosis | Try `https://x.com/i/under_the_hood` in the authorized account | This aggregate-label tool is a pilot, not guaranteed access (official, X README, 2026-08) |

Copy URLs produced by working navigation into the brief. Don't hard-code the old Explore trending path, `f=top`, or `f=live` as verified contracts. If experimenting with `min_faves`, `min_retweets`, `min_replies`, `since`, `until`, `lang`, or `filter` operators, mark them unverified until visible results demonstrate the intended behavior. An engagement filter doesn't create a date boundary. Don't claim a last-day sample without checking timestamps.

Record login walls, unavailable filters, and empty results distinctly. When search is unavailable, use accessible supplied post links and account pages and declare the reduced coverage. Don't report a blocked search as absence of discussion. If an AI-generated summary appears, use it only as a lead and inspect the underlying posts.

Use independent tabs for independent reads only when the browser supports them. Keep interaction within each tab sequential; don't race navigation calls against a shared tab. Close only tabs created for this harvest.

### Capture evidence before scoring

For each candidate, retain its exact URL, handle, observed publication time, capture time, and visible text. Record the root and relevant reply context. Note the format and any truncation. Inspect attached evidence rather than relying on its caption (directional).

Record views and public interactions only when visible. Preserve unavailable fields as unavailable, not zero. Record visible account size; record subscription status only when established. Buffer's Premium comparison makes tier a confounder, not a reason to guess it from a badge (measured, Buffer, n=18.8M X posts, 2026-03).

Capture displayed disclosure or restriction labels separately. Retain source context for factual claims and any visible corrections or Community Notes. A missing label doesn't verify a claim. Don't infer a reach consequence from a label's name without supporting evidence.

### Compare and cluster

Use matched observation windows and comparable account histories. Include ordinary posts as well as apparent breakouts so the sample doesn't consist only of winners (directional).

| Question | Evidence to collect | Limit |
|---|---|---|
| Is this relevant to the buyer? | Specific problem, role, use case, or evaluation question | Likes alone don't establish qualified interest |
| Is it unusual for this author? | Comparable recent posts at similar ages and formats | Follower count isn't an exposure denominator |
| Is it repeated independently? | Distinct authors expressing the same problem with source URLs | Reposts, copied text, and coordinated promotion aren't independent reports |
| Is the angle saturated? | Repeated claims across the actual sampled window | Say “common in this sample”; don't claim platform-wide exhaustion |
| Does the artifact add proof? | Inspectable screenshot, demonstration, source data, or method | Caption claims aren't validation |
| Is there momentum? | Repeated captures with timestamps and visible count changes | A single final count cannot reveal early velocity |

If reporting a public interaction-to-view ratio, name its numerator and denominator and use only visible fields. Don't call it a platform engagement rate or assign a universal breakout threshold. Never infer that low engagement proves scroll-past penalties. Use available own-account analytics to assess profile activity or qualified inquiries; don't estimate competitors' private conversions (directional).

Rank recommendations by relevance and evidence quality, then describe observed attention. Keep private shares and saves separate from public interaction comparisons. Avoid synthetic ranking-weight formulas and action-value hierarchies.

Extract a post's underlying move in plain language: a demonstrated task, a bounded outcome, a specific objection answered, or a decision with a cost. Preserve short source excerpts only where necessary and attribute them. Don't reproduce a viral hook bank or a copied dead-pattern list. The writing brief should describe what the next post can contribute, not supply a persona to imitate (directional).

## Launch and proof posts

For a launch harvest, obtain audience and buying situation, promise, proof source, intended action, destination, campaign stage, and disclosure obligations. No CTA can be deliberate. Don't fill absent campaign facts with imagined customer outcomes.

Search for the exact problem language and inspect what prospective users ask before recommending an announcement angle. The MailTest founder's reported change toward problem searches is anecdotal guidance, not a tested B2B conversion method (directional), citing MailTest founder account, 2026-04.

Return a source-backed candidate for each useful launch shape: announcement, demo, customer outcome, founder decision, objection answer, or recap. Name the available artifact, missing proof, and fit limitation. Don't force a candidate where the harvest contains no evidence. Community and creator seeding recommendations must concern relevant, distinct participation. X prohibits bulk unsolicited promotion, repeated link drops, and coordinated metric inflation (official, X Authenticity, 2025-04).

Keep founder, brand, and creator observations separate. Agency case reports are possible approaches to test, not conversion forecasts (directional), citing Clickstrike, undated. If a harvested post is compensated, gifted, affiliate, or ambassador promotion, the Paid Partnership requirement applies (official, X Paid Partnerships, 2026-09). Don't infer independent customer enthusiasm from disclosed paid endorsements.

## Voice observations on this platform

Describe register without judging human authorship. Record whether the source is formal, conversational, technical, or playful; note reply length and how the author handles uncertainty. Preserve examples of actual word choice with attribution. Don't recommend typo injection or copy an account's distinctive identity (directional).

Keep observed style separate from performance claims. A repeated hook may be common in the sample without being an algorithmic trigger. Leave generic AI-tell editing to downstream writing; harvesting establishes provenance and context.

## Cadence and engagement interpretation

Test weekday mid-mornings, then use account evidence and event timing. Buffer's baseline is 9–11 a.m., with Tuesday and Wednesday leading slots (measured, Buffer timing, n=8.7M X posts, 2026-03). Record the audience timezone; don't impose an evening window or infer a best time from a single successful post.

Buffer associates frequency with growth, with reduced per-post reach at higher frequency; these observations don't establish an X daily quota (measured, Buffer, n=4.8M channel-weeks; separate 15.7M-post reach analysis, 2026-03). Record cadence rather than penalizing accounts for posting bursts by assumption.

Text narrowly led images in Buffer's X format sample; video wasn't the engagement leader (measured, Buffer, n=X subset of 52M+ cross-platform posts, 2026-03). GIFs led raw interactions in Emplifi's different sample (measured, Emplifi, n=16,879 X profiles, reviewed 2026-09). Keep these metrics separate; recommend format tests instead of declaring mandatory media.

Code format observations conservatively: ordinary text is capped at 280 characters, Premium longer posts at 25,000, and the verified attachment plan is up to 4 photos, a GIF, or a video (official, X posting help and Premium, 2026-09). Don't call a multi-image post a swipe carousel. Article access, video tier caps, and other optional-surface details remain unverified until checked in the account. Log them as observed formats without inventing entitlements.

Link-post visibility was lower in political-discussion datasets (measured, NDSS, n=over 40M posts, 2026-02). Record root, reply, and profile link placement as separate observations. The evidence doesn't prove that moving a link to a reply fixes reach. A recommendation must retain the intended conversion path.

## What gets suppressed: diagnostic limits

X prohibits deceptive manipulated media and spam and can restrict reach for violations (official, X Authenticity, 2025-04). EU “Made with AI” indicators and restricted-reach labels are separate (official, X Media Literacy, 2026-07). Don't call an AI label a universal penalty or describe `MediumRisk` as proven organic reach loss.

Don't assign suppression to a `slop_score`, punctuation pattern, topic pivot, or small follower count. Public counters don't expose internal classifier results. Distinguish observed notices from hypotheses, and report inaccessible Under the Hood information as unavailable.

## Examples

### Evidence-qualified format observation

Fictional teaching record; all quantities are illustrative placeholders.

```text
Source: [post URL], [handle]
Published: [observed timestamp]; captured: [timestamp]
Format: ordinary text with a product screenshot
Views: [visible count]; replies: [visible count]; reposts: unavailable
Subscription: unknown
Observation: replies ask whether the export preserves field names.
Artifact: screenshot shows the export dialog; downloaded output wasn't inspected.
Recommended angle: show an actual export and its known limits.
Confidence: buyer-language evidence; no demonstrated conversion result.
```

Why it works: the capture procedure distinguishes visible evidence from an untested product claim.
The recommendation requests a useful artifact without inventing a growth mechanism.

### Saturation without a false threshold

Fictional teaching record.

```text
Claim cluster: automatic invoice approval
Evidence: [source URLs] from independent authors in [observed window]
Repeated claim: manual review can be eliminated
Counter-evidence: [source URL] describes disputed invoices needing review
Coverage limit: signed-in topic search; private discussions weren't available
Recommendation: explain the boundary for disputed invoices using supplied proof
```

Why it works: the cluster rule requires independent source evidence and explicit coverage.
The brief identifies a defensible contribution instead of declaring an entire topic dead.

## Checklist

- [ ] The audience, topic, and observation window are explicit.
- [ ] Each cited post has its exact URL and observed timestamps.
- [ ] Surface URLs and visible tab labels were captured from working navigation.
- [ ] Access failures and personalization limits are stated.
- [ ] Every quoted claim was checked in its original context.
- [ ] Missing metrics remain unavailable rather than zero.
- [ ] Any ratio names its visible numerator and denominator.
- [ ] Tier and account-history differences remain visible in comparisons.
- [ ] Momentum claims have repeated observations.
- [ ] Trend claims cite independent posts.
- [ ] Saturation claims are bounded to the sample.
- [ ] Recommended launch angles identify their proof and fit limitations.
- [ ] Style observations don't assert authorship or classifier results.
- [ ] Labels, policy actions, and ranking hypotheses remain distinct.
- [ ] Format and timing advice uses dated evidence or is marked directional.
- [ ] The brief contains no invented metrics or customer stories.
- [ ] Only harvest-created tabs are closed.

## References

- [X algorithm README](https://github.com/xai-org/x-algorithm/blob/main/README.md), [cold-start](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/author_cold_start.rs), August 13, 2026; [parameters](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs), August 12, 2026. Dated evidence snapshot with September corrections; mutable source URLs don't pin live deployment.
- [X posting help](https://help.x.com/en/using-x/how-to-post), [Premium](https://help.x.com/en/using-x/x-premium), [Paid Partnerships](https://help.x.com/en/rules-and-policies/paid-partnerships-policy), undated, reviewed September 2026.
- [Authenticity](https://help.x.com/en/rules-and-policies/authenticity), April 2025; [Media Literacy](https://help.x.com/en/rules-and-policies/media-literacy-plan), July 2026.
- [Buffer engagement](https://buffer.com/resources/state-of-social-media-engagement-2026/), March 5, 2026; [Buffer timing](https://buffer.com/resources/best-time-to-post-on-twitter-x/), March 13, 2026.
- [Emplifi benchmark PDF](https://go.emplifi.io/rs/284-ENW-442/images/Emplifi-Social-Media-Benchmarks-Report.pdf), undated, reviewed September 2026; [NDSS link study](https://www.ndss-symposium.org/wp-content/uploads/2026-s718-paper.pdf), February 2026.
- [MailTest founder account](https://www.indiehackers.com/post/i-launched-on-product-hunt-today-with-0-followers-0-network-and-0-users-heres-what-i-learned-in-12-hours-1c89889702?commentId=-Oql0RP2NQlQXltRvwH7), April 20, 2026; [Clickstrike cases](https://clickstrike.com/launch-playbook/), undated agency self-reports.

Re-validate when:
- Search operators, feed names, access gates, or format controls change.
- Policy updates, algorithm commits, or runtime defaults change.
- New vendor reports replace the benchmark samples.

Validated: 2026-09
