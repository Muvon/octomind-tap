---
name: social-bluesky
title: "Bluesky Publishing Playbook"
description: "Write and revise Bluesky posts, replies, threads, launches, and proof posts in the author's own voice. Activate for Bluesky drafting, format selection, community participation, or a publishing package with sourced claims and an explicit next step."
license: Apache-2.0
compatibility: "Bluesky app or browser access for composer checks; network access for source and destination verification."
domains: content
rules:
  - content(bluesky)
  - content(bsky)
  - match(\bbsky\.app\b)
  - match(\bat\s+protocol\b)
  - match(\bpost\s+(on|to|for)\s+bluesky\b)
  - match(\bstarter\s+pack\b)
---

## Overview

Write something the intended reader can use, in language the actual author would choose. Apply this precedence: supplied facts and proof, then documented author voice, then platform constraints. Use platform register only as a fallback; publication is a downstream step.

## Mental model

| Surface | Supported behavior | Writing decision |
|---|---|---|
| Following | Reverse chronological (directional, Buffer timing, 2026-08) | Test when your audience is online; chronology doesn't make timing irrelevant. |
| Discover | Default algorithmic feed with broad reach; strangers' Discover respects the recommendation opt-out (official, Visibility declaration, 2026-09) | Check the account's intended visibility; don't invent ranking weights. |
| Custom feeds | Topic- and list-based feeds needn't honor that opt-out (official, Visibility declaration, 2026-09) | Inspect the specific feed's description and returned posts before claiming fit. |

Keep post text within 300 grapheme clusters (official, Post lexicon, 2026-09). Validate the final composer text after inserting mention handles, links, and emoji; don't estimate a URL discount or count bytes.

Attach up to 10 photos; the carousel appears from 5 photos (official, Photos release, 2026-06). Video allows up to 10 minutes and 300 MB (official, Video release, 2026-08). These are ceilings, not targets. Check the actual combination of quote, image, GIF, video, and link preview in the composer; the supplied evidence doesn't establish a universal embed-exclusivity rule.

Automatic thread numbering was introduced as a beta option; its feature gate was subsequently removed (official, Thread numbering, 2026-08; App releases, 2026-09). Inspect the thread composer and preview; don't assume numbering is enabled or type duplicate markers. Make every installment understandable alone (directional).

Open reference/platform-mechanics.md when preparing media, a thread, community seeding, account controls, or a launch involving chats. It separates verified features from controls requiring a current UI check.

## Format and anatomy rules

Start on the useful detail. Keep a single idea per post, provide enough context to understand it, and stop when it is complete (directional).

| Reader's need | Choose | Execution (directional) |
|---|---|---|
| Understand a complete observation | Plain text | State the observation and its consequence without a suspense opener. |
| Inspect a source or try something | Link card | Explain what the destination contains. Preview its title and image; check destination and OG metadata. |
| See evidence or a physical detail | Image or photo sequence | Attach the crop that proves the claim; use further frames only for necessary context. |
| See motion or a workflow | Native video; GIF if a silent loop suffices | Show the relevant action promptly. Preserve conditions and visible limitations. |
| Follow a connected explanation | Thread | Give the root useful substance; make follow-ups self-contained. Put extensive documentation at a linked destination. |
| Resolve the original author's point | Reply | Read the chain; answer the actual question without restating the post. |
| Add context for your own readers | Quote post | Add a specific contribution that stands alone. Use a plain repost when you have nothing to add. |

Write alt descriptions for visible meaning and relevant screenshot text; don't use the field as an overflow post, hidden joke, or keyword list. Bluesky documents search matches in image alt text, so it is public searchable content, not a private metadata field (official, Search Tips, 2024-05; writing advice is directional). Prepare captions for speech and an asset brief identifying source and crop. Preview accessibility fields and captions; don't assert an unsupported alt-text cap.

Use only relevant hashtags supported by the topic or a verified feed criterion. Preserve readable capitalization; don't impose lowercase or a numeric tag quota (directional).

## Launch and proof posts

Collect the audience and buying situation, promise, source-backed proof, desired action, destination, campaign stage, and disclosure obligations. Stages include teaser, launch day, proof, objection, and recap. Record the author's role and actual experience. Choose no CTA deliberately when the post's job is explanation (directional).

Don't invent personal history, customer quotes, measurements, timelines, or shipped results. Obtain missing evidence before treating a draft as publishable; omit a claim if the author can't substantiate it.

Length bands below describe editorial density, not performance optima. Every installment remains within the text ceiling above.

| Shape | Anatomy (directional) | Length band (directional) |
|---|---|---|
| Launch day | Name the released thing and who can use it; show a concrete function, limitation, and next step. Remove the product name as a strip-test: the remaining detail should still teach or show something. | Compact standalone announcement; link for detail |
| Demo or artifact | State the task; attach the real output or recording and its operating conditions. | Short framing beside media |
| Customer outcome | Give the before and after with source, permission, measurement window, and what remained unresolved. | Near-budget proof post; contextual follow-up if needed |
| Founder decision | State the choice, evidence behind it, and cost or unfinished work. | Standalone observation |
| Objection answer | Name the specific concern; show the supported answer and applicability boundary. | Direct reply or standalone explanation |
| Recap or lessons | Report what changed after feedback and what still needs work; link the usable artifact. | Short connected thread if the evidence needs it |

Bluesky says it doesn't punish links and encourages off-platform clicks (official, Bluesky outlook, 2026-01). Put the destination in the root when it serves the reader; use a reply for supplementary detail and a profile link as a stable fallback (directional). Don't hide every launch link in replies to evade an invented penalty. Community-built Offprint, Leaflet, and pckt.blog are long-form options supported by Bluesky's publishing partnership (official, Summer of Standard.site, 2026-06).

Keep consistent `utm_source`, `utm_medium`, and `utm_campaign`; use `utm_content` to distinguish placements (official, Google URL builder, 2026-09). Verify that the destination matches the promise. Separate attributed visits and activation from public interactions (directional).

Disclose affiliation and sponsorship plainly: undisclosed commercial content, disruptive repetition, and artificial social-signal manipulation are prohibited (official, Community Guidelines, 2025-09). Don't organize engagement pods or scripted employee replies. For voluntary employee shares, use the person's real involvement and disclose the relationship (directional).

For community seeding, inspect relevant feeds and starter packs, respect their inclusion choices, and answer existing needs. Pack reference-list opt-out UI exists (official, App releases, 2026-09). Don't promise placement, demand reposts, or bypass an opt-out. Use chats only for invited follow-through (directional).

Illustrative launch calendar: offsets are planning examples, not measured best intervals. Skip a slot without new evidence; arrange reply coverage during the first hours after each post (directional).

| Offset (illustrative) | Post or preparation | Reply plan and measurement (directional) |
|---|---|---|
| T−7 | Gather relevant questions; prepare a useful artifact or teaser | Record vocabulary and actual evaluation needs. |
| T−3 | Show a demo or founder decision | Answer feasibility questions; log requested use cases. |
| T0 | Publish the announcement and working destination | Staff replies; record qualified questions, substantive quotes, and destination actions separately. |
| T+1 | Answer the most consequential objection | Follow up in its original context; note whether the concern was resolved. |
| T+3 | Publish permissioned proof if available | Clarify conditions; record relevant trial or support conversations. |
| T+7 | Share a bounded recap | Report outcomes and unresolved issues; compare posts at similar ages. |

Choose a founder handle for lived decisions and a brand handle for product availability or support, according to the real speaker; no verified Bluesky founder-versus-brand uplift is supplied (directional). Brands needn't imitate an engineer or adopt forced banter.

## Voice on this platform

Keep content-voice as the generic baseline. For Bluesky, read the surrounding conversation for subject depth, formality, and humor before replying. Match its context without impersonating participants. Art commentary may be playful; a service update should be practical; technical claims need precision. Don't impose a platform-wide political identity or engineering register (directional).

Preserve the author's contractions, fragments, and punctuation. Introduce no typos, fake edits, dropped articles, or lowercase camouflage. Retain an effective em dash, but revise repeated dash pivots or dash-heavy short posts; don't impose a quota or remove useful punctuation merely to look human (directional, Aborn and Cox).

Apply practitioner heuristics as editorial judgment, never authorship detection: remove filler, empty suspense, unsupported novelty claims, and endings that merely solicit engagement. Keep useful contrasts, lists, questions, and summaries; don't replace the author's style with punctuation, contraction, or sentence-length quotas (directional, Aborn, Cox, Gichigi). Retain real tradeoffs and uncertainty. An ordinary sincere acknowledgment can be a complete reply; it needs no invented anecdote or forced follow-up question (directional).

Carry supplied facts into cross-posts, then rebuild the Bluesky framing and CTA for the actual reader. Don't anchor adaptation on another network's character limit (directional).

## Cadence and engagement

### Measured signals

Video had median 5 interactions, images 4, and links and text 3 each (measured, Buffer engagement, n=Buffer-published Bluesky subset, 2026-03). Sprout found 45% of surveyed Bluesky users most likely to engage with text-based brand posts (measured, Sprout platform survey, n=Bluesky survey subset, 2026-03). These measure different populations and outcomes; test relevant media without replacing useful text with decorative assets (directional).

Author replies correlated with 5% higher Bluesky engagement in a within-account comparison; causality wasn't established (measured, Buffer engagement, n=nearly two million cross-platform posts, 2026-03). Reserve time to answer meaningful replies. Ask questions only when the answers will be useful (directional).

Test audience-local Saturday 5 p.m., Saturday 6 p.m., or Sunday 9 a.m.; weekday evenings around 6–9 p.m. were stronger than late mornings in the study (measured, Buffer timing, n=over three million posts, 2026-08). Follow your audience's baseline and availability, without a universal daily cap or expiry window (directional).

Open reference/measured-signals.md when selecting formats, comparing results, or planning timing. It contains sample limits, survey findings, and starter-pack/custom-feed evidence. Re-measure against dated post samples instead of reviving universal repost ratios.

## What gets suppressed

Bluesky reports detecting and downranking toxic or spammy posts (official, Bluesky outlook, 2026-01). Use a fresh, useful follow-up instead of repeating the announcement. Don't interpret weak engagement as proof of bots or punishment (directional).

Automated media labels and hide/warn/show controls are documented for sensitive content (official, Transparency report, 2026-01). Inspect the current post self-label picker for an applicable content warning. Writing "AI image" is a plain disclosure; don't present it as a picker selection or promise it prevents labeling. Disclose synthetic media when relevant to understanding its provenance (directional). The verified evidence establishes neither a universal AI self-label nor punctuation-based hiding.

Before launch, decide the intended reply audience and quote participation. Inspect current threadgate, hide-reply, quote-disable, and quote-detach controls where available; verify scope rather than assuming these settings make a post private. Keep an accessible support route if participation is restricted (directional).

## Examples

These are illustrative briefs and drafts, not reports of real releases. Product behavior is stipulated only for teaching. Replace bracketed fields with supplied evidence before publishing; unfilled examples aren't publishable.

### Developer tool: artifact launch

Illustrative brief: the author built a config comparison tool; it doesn't inspect environment variables. Avoid the unsupported rewrite "The fastest config debugger."

> I built [tool] to show which config value wins when files overlap. The screenshot traces [setting] back to its source. Environment variables aren't covered yet. Try it on a sample config: [link]

Why it works: the launch rule puts a demonstrable function ahead of the pitch.
The limitation bounds the claim; the screenshot must come from the supplied build.

### B2B SaaS: customer proof

Illustrative brief: a customer approved a timed export comparison; manual review continued.

> With [customer]'s permission: their export took [before] before [change] and [after] afterward, on the same [dataset], measured over [measurement window]. They still review exceptions by hand. The comparison and its limits: [link]

Why it works: the proof rule keeps comparison conditions beside the outcome.
Every measurement needs a source; the unresolved manual step prevents a miracle-fix story.

### Creator: print announcement

Illustrative brief: a printmaker photographed a finished print; no digital edition exists.

> The print of [title] is ready. I've included a close-up of the paper because the texture disappears in the flat scan. This is a physical print; there's no download edition. Sizes and shipping details: [link]

Why it works: the image rule gives the photograph a specific job.
The creator's practical register and format limitation serve an actual purchase decision.

### Local service: answer an expressed need

Illustrative brief: someone asked whether a repair shop accepts walk-ins; the shop requires bookings.

> I run [shop]. We can assess that seam, but please book before bringing the jacket in. A photo of the lining will help us check whether we can reach the damage. Booking details: [link]

Why it works: the reply rule answers the existing question and makes affiliation clear.
The shop offers an assessment without promising a repair outcome.

### Quote: add a useful boundary

Illustrative brief: a museum posts its collection online; the supplied rights page limits commercial use. Quote the announcement with this added context:

> The [museum] collection is useful for studying [subject]. Check the rights notice on the individual image before putting it on merchandise; the collection's online availability doesn't establish permission for that use. Rights page: [link]

Why it works: the quote rule adds a concrete distinction for the author's readers.
The rights claim needs the supplied policy; don't generalize it to other collections.

### Thread: preserve context in each installment

Illustrative brief: a potter documented a glaze comparison and has no food-safety result. Publish the following as connected posts, previewing any automatic numbering.

> I kept [glaze] for the outside of [piece]. The photo shows how it pooled around the handle in [firing conditions]. I haven't established whether this glaze is suitable for food contact.

> For anyone comparing [glaze] with their own samples: this test used [clay body] and [firing conditions]. The darker patch is beside the handle. The flat test tile didn't show that pooling.

Why it works: the thread rule gives each installment its own subject and conditions.
The limited test supports an observation about appearance, with no safety promise.

## Checklist

- [ ] First line carries useful substance; the post has a single idea and matches the author's documented voice.
- [ ] Every specific has supplied provenance; no unfilled example fields or invented experience remain.
- [ ] Final composer text meets the grapheme limit above, including inserted handles and links; every thread post stands alone and numbering isn't duplicated.
- [ ] Photo count and video limits above pass; embed combinations and the rendered link card are checked.
- [ ] CTA or deliberate no-CTA is clear; destination works and attribution parameters are consistent.
- [ ] Alt text, captions, asset brief, and follow-up reply plan accompany relevant formats.
- [ ] Voice and substance review preserves useful structure without manufacturing errors or imposing style quotas.
- [ ] Affiliation, sponsorship, media disclosure, and applicable picker warnings are checked.
- [ ] Launch stage and proof match; reply/quote controls and recommendation visibility reflect the account owner's intent.

## References

- [Search Tips: alt text is searchable](https://bsky.social/about/blog/05-31-2024-search), 2024-05-31; reviewed 2026-09-05.

- [Post lexicon](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/post.json), undated; reviewed 2026-09.
- [Visibility declaration](https://bsky.network/blog/content-visibility-declaration/), 2026-09-01.
- [Photos release](https://bsky.app/profile/bsky.app/post/3mnslrkd6ok2g), 2026-06-08; [Video release](https://bsky.app/profile/bsky.app/post/3mtwf7gxkwc2r), 2026-08-25.
- [Thread numbering](https://bsky.app/profile/bsky.app/post/3msqpusnigc2t), 2026-08-10; [App releases](https://github.com/bluesky-social/social-app/releases), 2026-09-03.
- [Bluesky outlook](https://bsky.social/about/blog/01-28-2026-bluesky-2026-predictions), 2026-01-28; [Community Guidelines](https://bsky.social/about/support/community-guidelines), 2025-09-19.
- [Transparency report](https://bsky.social/about/blog/01-29-2026-transparency-report-2025), 2026-01-29.
- [Summer of Standard.site](https://bsky.social/about/blog/06-22-2026-summer-of-standard-site), 2026-06-22.
- [Google URL builder](https://support.google.com/analytics/answer/10917952?hl=en), undated; reviewed 2026-09.
- [Buffer engagement](https://buffer.com/resources/state-of-social-media-engagement-2026/), 2026-03-05; [Buffer timing](https://buffer.com/resources/best-time-to-post-on-bluesky/), 2026-08-05.
- [Sprout platform survey](https://sproutsocial.com/insights/?p=193529), 2026-03-16.
- [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/), 2026-07-10; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), 2026-06; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how), 2026-02-18. Editing heuristics (directional).
- Deep source notes: [platform mechanics](reference/platform-mechanics.md), [measured signals](reference/measured-signals.md), reviewed 2026-09.

Re-validate when: composer limits or controls change; feed names or ranking code change; labeling policies change; new vendor reports appear.

Validated: 2026-09
