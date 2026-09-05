---
name: trend-bluesky
title: "Bluesky Trend Harvester Playbook"
description: "Harvest Bluesky conversations, formats, and launch evidence into a sourced brief. Activate when scanning Bluesky trends or researching post angles, custom feeds, and relevant community responses; record observed surfaces and account baselines without inventing amplification paths."
license: Apache-2.0
compatibility: "Octoweb browser access and network access. Use the available Bluesky session; record signed-in state and unavailable surfaces."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(bluesky)
  - match(\bbluesky\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+bluesky\b)
  - match(\bbsky\.app\b)
---

## Overview

Return an auditable brief about the requested Bluesky community. Separate what you observed from an explanation of why it happened. Harvest evidence and reusable editorial observations; writing and publishing are downstream steps.

## Mental model

Discover is a default algorithmic feed with broad reach. It respects an account's recommendation opt-out for strangers; topic- and list-based feeds needn't honor that declaration (official, Visibility declaration, 2026-09). Don't describe Discover as opt-in or assign it unverified reply or graph weights.

Following is reverse chronological (measured, Buffer timing, n=over three million posts, 2026-08). Timing can affect what an online audience encounters; chronology doesn't guarantee a reply's delivery or make old posts equally visible.

Followers can hide a followed account's reposts in feeds (official, Repost controls, 2026-08). Don't equate repost count with audience delivery, or presume quotes outperform plain reposts. Use the sampled community, not an assumed technical or political platform identity, as your scope (directional).

## Harvest rules

### Establish the collection scope

Record the user's topic, intended audience, language, geography, and time range. Record collection time and timezone, signed-in state, query filters, and stopping criterion. Choose a bounded sample that includes ordinary posts and relevant smaller accounts as well as popular examples (directional).

Do not publish, follow accounts, join chats, or contact curators as part of harvesting. Preserve private chat boundaries; public trend collection doesn't authorize use of private messages.

### Resolve surfaces through the current app

Start at [Bluesky](https://bsky.app/) and navigate through the visible UI. Copy the actual share URL after selecting a feed or search filter. The verified source set doesn't establish canonical Discover or hashtag routes; don't substitute a guessed path or generator identifier.

| Surface to inspect | Navigation and record (directional) | Sampling limit |
|---|---|---|
| Trending topics or Explore, if present | Check current search/home navigation; open a relevant topic and retain its resulting URL | Record region, language, and absence if unavailable; don't assume a default feed roster. |
| Discover | Select the named feed in the current session and copy its URL | Treat the sample as session-conditioned, not a platform census. |
| Following | Select Following explicitly | Record whether the follow graph provides relevant material; home alone doesn't identify the selected feed. |
| Topic and hashtag search | Enter the query, including the hash for a tag; use available filters and share the result URL | Record sort choice exactly as displayed; don't call an unfiltered result a recent sample. |
| Custom feeds | Inspect current feed discovery navigation, then the feed's description and actual results | Record feed URL, owner, stated criteria, and whether each cited post was observed there. |
| Relevant profiles and packs | Open from observed posts or feed descriptions; copy profile and pack URLs | Record topical relevance and observed repost behavior; don't assert a fixed pack-size range. |

Search supports shareable filters for keywords, people, date range, and language (official, Search rollout, 2026-07). The app completed its search migration in the subsequent release (official, Search migration, 2026-07). These announcements don't establish an API endpoint or sort-mode contract: adapt browser collection to the current UI.

Record missing or inaccessible surfaces as unavailable. Don't invent logged-out access guarantees, quarterly feed renames, or results from a guessed public API route. Inspect enough of each surface to satisfy the declared sampling scope; use independent browser tabs only when the browser supports them safely (directional).

### Capture each candidate

Save the canonical post URL and full displayed handle, source surface, collection time, publication time, and post age. Record visible likes, replies, reposts, and quotes separately, plus follower count if available. Mark unavailable metrics unavailable; don't manufacture impressions or infer that a missing view count is universally unavailable (directional).

Capture the actual opening text, format, media's evidentiary role, link destination, affiliation disclosure, and relevant reply context. Record visible restrictions or labels as observations; don't reverse-engineer a suppression rule from them (directional).

For a thread, inspect the root and relevant follow-ups. Note whether installments carry enough context independently; automatic numbering exists, and its feature gate was removed in the later release (official, Thread numbering, 2026-08; App releases, 2026-09). Don't count displayed numbering as author-written hook text without checking.

If format constraints matter to a recommendation, use the verified limits: 300 grapheme clusters for post text (official, Post lexicon, 2026-09); up to 10 photos, with a carousel from 5 (official, Photos release, 2026-06); video up to 10 minutes and 300 MB (official, Video release, 2026-08). Don't score a longer asset as better or assert a universal embed-exclusivity rule.

### Compare without invented thresholds

Use account-relative comparisons among posts of similar age, subject, and format. Report raw counts and explain the comparison set. Reposts divided by likes is a descriptive ratio; if likes are zero, mark it undefined. Never use a universal strong/breakout threshold or a follower-band multiplier (directional).

| Dimension | Evidence to return (directional) |
|---|---|
| Audience fit | Replies showing the requested community's use cases or questions; don't infer profession from a like. |
| Distribution | Observed reposts, quotes, and actual appearances on named surfaces, with collection times |
| Conversation | Substantive answers, author follow-through, and unresolved objections |
| Proof | Inspectable artifact or source, its conditions, and what it doesn't establish |
| Saturation | Repeated claims within the declared sample and the missing detail an original contribution could address |

Distinguish discovery location from diffusion. Finding a post in Discover and a custom feed doesn't establish movement between them. A prominent account's repost doesn't establish its contribution to subsequent counts. Overlapping feeds aren't independent audiences (directional).

Bluesky says it doesn't punish links; it also reports downranking toxic or spammy posts (official, Bluesky outlook, 2026-01). Don't reject root links or label low engagement a promotion penalty. Spam, disruptive repetition, and artificial social-signal manipulation are prohibited (official, Community Guidelines, 2025-09).

## Launch and proof posts

When the brief concerns a launch, harvest the announcement, demo, proof, objection answers, and recap where available. Record what each post offers before the click, the actual next step, the author's relationship to the product, and evidence of qualified interest. A reply asking about compatibility or availability is more interpretable than an unexplained like count for that specific buying question (directional).

Record relevant starter packs without treating them as guaranteed placement. Reference-list opt-out UI exists (official, App releases, 2026-09). Preserve exclusion choices and describe curator or participant accounts as observed sources, not an outreach target list.

In the brief, separate native interactions from destination visits or conversions. Only report private analytics if supplied with scope and authorization. Don't attribute a sale to a post from timing alone or generalize founder-versus-brand performance from another platform (directional).

## Measured signals

Use these dated comparisons to design the sample, not as pass/fail scores.

| Result | Scope and use |
|---|---|
| Video median 5 interactions, images 4, links and text 3 each (measured, Buffer engagement, n=Buffer-published Bluesky subset, 2026-03) | Historical Buffer-user observations; inspect whether media carries proof instead of assuming automatic image lift. |
| Author replies associated with 5% higher engagement (measured, Buffer engagement, n=nearly two million cross-platform posts, 2026-03) | Within-account comparison; no causal or Discover-ranking conclusion. |
| Test audience-local Saturday 5 p.m., Saturday 6 p.m., or Sunday 9 a.m.; weekday evenings around 6–9 p.m. were stronger than late mornings (measured, Buffer timing, n=over three million posts, 2026-08) | Compare with the actual community's activity; no universal expiry interval or daily thread cap. |
| Substantial short-term repost increase associated with pack inclusion (measured, Starter-pack study abstract, n=over 50,000 packs, 2026-08) | No supported matched-control multiplier or current pack-size limit in the reviewed abstract. |
| 9.04% of eligible test posts reached a monitored feed's Top 50 within 24 hours (measured, Custom-feed study abstract, n=5,000 monitored feeds, 2026-08) | A defined monitored-panel outcome, not the chance of reaching any Bluesky feed. Record actual appearances. |

The prior unlabeled ratios and hot-feed anecdotes aren't benchmarks. Any new measurement needs post URLs, query and feed identifiers, capture times, raw counts, and a declared comparison rule. Re-derive when surfaces or the audience change (directional).

## Examples

### A bounded distribution observation

Illustrative counts and placeholders below teach the reporting shape; they aren't observed posts.

> Source: [post URL], by [full handle], found in [feed URL] at [capture time]. Observed counts: 120 likes and 18 reposts (illustrative). Repost/like ratio: 0.15 (illustrative calculation). Replies and quotes weren't captured. The author's recent comparable-post baseline isn't available.
>
> The screenshot shows [specific artifact]. A reply asks about [use case]. The post also appeared in [other feed URL], but collection doesn't establish which surface distributed it first. Keep it as a relevant artifact example; distribution strength remains unclassified.

Why it works: raw counts remain separate from causal attribution.
The report states missing evidence instead of inventing a breakout label.

### High likes with little decision evidence

Illustrative comparison, not a real brand judgment:

> [Post URL] has more visible likes than the other sampled posts. Its replies don't explain an evaluation need, and the destination offers no inspectable proof. Keep it in the dataset; rank it below [evidence-bearing post URL] for this launch brief's goal of finding useful product explanations.

Why it works: the ranking follows the brief's stated evidence goal.
It makes no bot, employee-engagement, or platform-penalty accusation.

## Checklist

- [ ] Collection scope, timezone, session state, and inaccessible surfaces are recorded.
- [ ] Trending/Explore availability was checked; Discover, filtered searches, and relevant custom feeds use observed URLs.
- [ ] Each cited post has a full handle, canonical URL, capture time, age, and raw metrics or explicit missing values.
- [ ] Discovery surface is separated from inferred diffusion; no attribution percentages or universal ratio thresholds appear.
- [ ] Comparisons state the account baseline and sample limits; counts aren't treated as conversions.
- [ ] Format, source proof, disclosures, and meaningful reply context are captured.
- [ ] Launch evidence and unresolved buyer questions are distinguished from popular but unrelated material.
- [ ] Feed criteria and actual inclusion are separated; pack opt-outs are respected.
- [ ] Any recommended angle is tied to observed evidence, without copied post text presented as original writing.
- [ ] Only tabs opened for this task are closed; no account interactions or messages were sent.

## References

- [Visibility declaration](https://bsky.network/blog/content-visibility-declaration/), 2026-09-01.
- [Repost controls](https://bsky.app/profile/bsky.app/post/3msqpuobiwk2t), 2026-08-10.
- [Search rollout](https://bsky.app/profile/bsky.app/post/3mqafridzgk2e), 2026-07-09; [Search migration](https://github.com/bluesky-social/social-app/releases/tag/1.128.0), 2026-07-16.
- [Thread numbering](https://bsky.app/profile/bsky.app/post/3msqpusnigc2t), 2026-08-10; [App releases](https://github.com/bluesky-social/social-app/releases), 2026-09-03.
- [Post lexicon](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/post.json), undated; reviewed 2026-09.
- [Photos release](https://bsky.app/profile/bsky.app/post/3mnslrkd6ok2g), 2026-06-08; [Video release](https://bsky.app/profile/bsky.app/post/3mtwf7gxkwc2r), 2026-08-25.
- [Bluesky outlook](https://bsky.social/about/blog/01-28-2026-bluesky-2026-predictions), 2026-01-28; [Community Guidelines](https://bsky.social/about/support/community-guidelines), 2025-09-19.
- [Buffer engagement](https://buffer.com/resources/state-of-social-media-engagement-2026/), 2026-03-05; [Buffer timing](https://buffer.com/resources/best-time-to-post-on-bluesky/), 2026-08-05.
- [Starter-pack study abstract](https://arxiv.org/abs/2608.17489), 2026-08-18; [Custom-feed study abstract](https://arxiv.org/abs/2608.13874), 2026-08-14.

Re-validate when: navigation or feed names change; ranking code changes; search migrations occur; policy updates or new vendor reports appear.

Validated: 2026-09
