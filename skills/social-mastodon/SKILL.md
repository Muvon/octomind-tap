---
name: social-mastodon
title: "Mastodon Publishing Playbook"
description: "Write and revise Mastodon posts, replies, launches, and proof updates in the author's documented voice. Activate for Mastodon or Fediverse publishing briefs; check the actual server before applying Mastodon mechanics elsewhere. Covers discovery, visibility, accessible publishing, disclosure, and qualified follow-up."
license: Apache-2.0
compatibility: "Browser or HTTP access for current server rules, composer limits, and source verification."
domains: content
rules:
  - content(mastodon)
  - content(fediverse)
  - content(activitypub)
  - content(toot)
  - match(\bpost\s+(on|to|for)\s+mastodon\b)
  - match(\bthe\s+fediverse\b)
---

## Overview

Write something the named author can defend and the intended reader can use. Apply supplied facts and proof first, the author's documented voice next, then platform guidance. Don't assume every Fediverse service has Mastodon's controls. Prepare copy and a publishing handoff; posting, scheduling, and outreach require a request for those actions.

## Mental model

| Surface or action | Writing consequence |
|---|---|
| Home | Includes followed accounts and followed hashtags; don't promise every tagged post universal delivery (official, Timelines, 2026-05). |
| Public/Live feeds | Local filtering and access restrictions exist; check the connected server before planning discovery there (official, Timelines, 2026-05). |
| Explore/Trends | Uses a periodically recalculated internal score: status interactions, tag usage, and link sharing. Don't reduce it to boosts or call the platform algorithm-free (official, Trends, 2026-05). |
| Search | Full-text availability depends on server setup; direct lookup and library search also exist. Don't call untagged posts invisible or assert a current indexing default (official, Network, 2025-11). |
| Favourite / boost | A favourite notifies the author without resharing; a boost reshares. Neither counts as a customer outcome (official, Network, 2025-11). |
| Quotes | New posts default to Anyone; authors can restrict quoting to followers or Just me, change permissions, and revoke quotes. Check the source post's permission (official, Quote posts, 2025-11). |

Use the UI terms “post,” “server,” and the displayed visibility labels. Treat software previews as announcements: Messages separation and changes to followed-hashtag navigation were previewed for Mastodon 5.0, not established as shipped behavior (official, Foundation preview, 2026-08).

Open [reference/mechanics.md](reference/mechanics.md) when preparing an account, attachments, a poll, scheduled publishing, edits, or an integration. Record the connected server's limits before declaring a package ready; don't substitute a named server roster or an assumed default.

## Rules and format decisions

### Choose the audience deliberately

| Intent | Choice |
|---|---|
| Public announcement or discoverable explanation | Select Public and inspect the resulting audience in the composer (directional). |
| Public side conversation without public-feed discovery | Select Quiet public, formerly Unlisted: excluded from public feeds, Explore, and search, but visible on the profile and eligible for Home (official, Posting, 2026-07). |
| Update intended for followers | Inspect the Followers audience and account settings before publishing (directional). |
| Requested personal follow-up | Inspect Specific people/private-mention recipients; confirm the actual control label. Keep confidential customer material in an approved support channel (directional). |

Replies have an additional Home rule: the follower normally needs to follow both participants. Quiet public isn't a promise to deliver a reply to every follower (official, Posting, 2026-07).

### Fit the explanation to the space

Use qualitative length bands relative to the verified server cap; these are editorial choices, not performance optima (directional).

| Material | Format and length band |
|---|---|
| Complete observation or announcement | Compact standalone post; leave room for the useful link and disclosure. |
| Necessary detail that won't fit | Substantive root with understandable self-reply installments, each below the cap. Add numbering only if it helps readers follow the sequence; omit empty thread-promotion intros. |
| Methodology or durable documentation | Brief finding plus a blog/documentation link; keep evidence and conditions at the destination. |
| Visual evidence | Short caption plus the artifact; use multi-image only when the sequence adds information. |
| A decision readers can inform | Compact poll prompt with neutral, distinct options; verify option limits, duration, selection mode, and attachment compatibility. Don't call respondents representative buyers. |

Put the destination in the root when readers need it. Remove unnecessary tracking only when the brief permits; preserve functional, signed, and required attribution parameters and test the destination (directional). Mastodon counts HTTP(S) links as 23 characters in its documented composer, so shortening a URL doesn't save space (official, Posting, reviewed 2026-09-05). Open Graph supplies preview cards (official, PreviewCard, 2026-06). Equal observed link/text medians don't establish a universal absence of link penalties (measured, Buffer, n=Mastodon subsample undisclosed, 2026-03).

### Hashtags and content warnings

Choose tags by distribution need, not follower-count thresholds. Verify recent relevant posts on the target server's tag surface; an inaccessible or empty sample doesn't prove a tag is dead everywhere. Capitalize words in multi-word tags for readability (directional).

| Account situation | Tag decision (directional) |
|---|---|
| New or small audience seeking topic discovery | Use a small set of live, directly relevant topic tags. |
| Established audience, useful topic contribution | Keep tags that connect the contribution to an active conversation. |
| Personal exchange or no relevant active tag | Omit tags; don't fill a quota. |

| Server/community context | CW decision (directional) |
|---|---|
| Explicit local content rules | Follow the actual rule, regardless of server category. |
| Community asking for spoiler, politics, food, or other topic warnings | Use a short descriptive label for matching material. |
| Sensitive reply chain | Preserve a relevant warning when the reply continues that material. |
| Routine product or technical update | Don't add a warning solely to manipulate discovery; follow local promotion rules. |

Describe the material plainly in the warning. Don't infer policy from an “art,” “technical,” or “general” server label (directional).

### Account and disclosure choices

| Publishing identity | Use it for (directional) |
|---|---|
| Personal/founder account | Decisions the person owns and questions they can answer from experience. |
| Project account | Release information and support with a named reply owner; don't fabricate a founder persona. |
| Account on an owned server | An organization prepared to own operations and moderation; complete the setup checks in the mechanics reference. |

| AI or commercial situation | Required decision |
|---|---|
| Generative-AI content on mastodon.social or mastodon.online | Disclose it; primarily or exclusively AI-generated accounts are prohibited. A CW isn't a substitute for disclosure (official, Community Standards, 2026-02). |
| Independent server | Read its current commercial and AI-content rules; the operated-server terms don't govern it (official, Server terms, 2026-07). |
| Assistance whose policy classification is unclear | Establish what was generated and check the applicable wording before publication; don't invent an editing exemption (directional). |
| Sponsored, gifted, employee, or founder post | State the relevant relationship and apply the brief's disclosure obligations. Identify synthetic media as such where required; never present it as product evidence (directional). |

Editing for voice doesn't erase disclosure obligations. Don't claim an automatic AI label, missing-alt-text block list, or repeated-post defederation mechanism.

## Launch and proof posts

For campaign work, record audience, buying situation, promise, sourced proof, desired action/destination, disclosures, and stage. Use writing samples when available; record the author's role and reply availability. Missing samples do not block a restrained factual draft. No CTA is valid. If essential evidence is absent, narrow or withhold that claim; don't invent a customer result (directional).

Use these post shapes with the format bands above (directional):

| Shape | Anatomy and length band |
|---|---|
| Launch day | Compact: concrete new capability, intended user, constraint, usable destination. Strip the product name mentally: the post should still explain something useful. |
| Demo/artifact | Short caption: task shown, observable behavior, boundary; attach accessible proof and link to try or inspect it. |
| Customer outcome | Near-cap if needed: prior state, intervention, bounded outcome with conditions and permission; link the method. |
| Founder decision/build update | Compact: actual decision, reason grounded in evidence, cost or unresolved trade-off. |
| Objection answer | Compact: the real concern, direct answer, supporting artifact; state who shouldn't use the product. |
| Recap/lessons | Brief finding plus durable link; distinguish adoption evidence from unresolved feedback. |

Seed through useful participation in relevant conversations. Mention collaborators only when directly involved; let employees contribute their own experience with affiliation visible. Don't organize reciprocal boosts, copied praise, unsolicited pitch mentions, or fake customer conversations (directional).

Collections provide a consent-aware ecosystem resource: only discoverable opted-in profiles can be included, additions notify members, members can leave, and the cap is 25 profiles with no follow-all. Collections have shareable URLs under Featured and currently rely on manual discovery. Share a useful collection's link without making inclusion conditional on promotion (official, Release, 2026-06).

The launch-week table is an illustrative schedule, with T marking launch day. Its dates are example planning slots, not measured timing advice. Skip a slot when there is no new evidence (directional).

| Phase | Post shape | Reply plan and observation |
|---|---|---|
| T-7 (illustrative) | Decision or useful problem explanation | Discuss real constraints; record audience language. |
| T-2 (illustrative) | Demo or permission-based preview | Answer access questions; check whether readers can evaluate it. |
| T (illustrative) | Native announcement with root link | Assign first-hours coverage; record qualified questions and blockers. |
| T+1 (illustrative) | Objection answer | Return with evidence; separate team replies from independent responses. |
| T+3 (illustrative) | Supported proof, if available | Ask permission to use reported outcomes; document exclusions. |
| T+7 (illustrative) | Recap linking the durable artifact | Revisit unanswered questions; record reported adoption and unresolved limitations. |

Track qualified replies and independent participant/server diversity alongside observed boosts, favourites, and quotes. Connect volunteered trial or adoption reports to source records; keep website conversion data separate. Don't infer sales from applause (directional). Open [reference/evidence.md](reference/evidence.md) when choosing experiments, interpreting performance, or adapting a launch that links to another community.

## Voice on this platform

Use `content-voice` for generic editing. Preserve recognizable phrasing from the author's samples and the decisions in their notes. Keep technical names exact and explain limitations without ritual hedging. Read the target conversation for depth and formality; don't impose a FOSS persona on another community or insert slang, deliberate errors, fake edits, or lowercase camouflage (directional).

Replies should address the actual point; use a short list when it makes instructions easier to follow. Threads need enough context in each installment; numbering is an editorial choice, not a bot signal. Media descriptions should convey the supplied artifact, including relevant chart labels or screenshot text, without invented interpretation or overflow sales copy (directional). Descriptions are optional in Mastodon but recommended; include them in the publishing package (official, Posting, 2026-07).

Remove filler, repetitive suspense, unsupported novelty claims, and endings that demand engagement. Keep real contrasts, meaningful lists, ordinary questions, and useful summaries. Preserve the author's punctuation without contraction, sentence-length, or dash quotas. Don't erase genuine tradeoffs to make a tidy story. These are editing heuristics, not authorship tests (directional; Aborn, Cox, Gichigi). The evidence reference explains their limits.

## Cadence and engagement

Choose audience-local times when the author can answer, then compare similarly scoped posts at matched observation ages. Buffer publishes no Mastodon timing window; don't import universal ET hours or fixed federation-delay rules (measured, Buffer, n=Mastodon subsample undisclosed, 2026-03).

Add self-replies for necessary information, not manufactured activity. Preserve useful questions for follow-up proof posts; verify a relevant participant's actual contribution before attributing a spread path (directional). Observational reply studies support investigating conversation and network context, not quotas or causal reach promises; see the evidence reference.

## What gets suppressed

Keep visibility settings, server enforcement, and reader preference separate. Quiet public limits discovery by design (official, Posting, 2026-07). Commercial and AI rules require a server-specific policy check (official, Server terms, 2026-07). Don't turn low engagement, missing descriptions, link presence, or unfamiliar tone into an invented ranking penalty.

Adapt imported posts by checking handles and destination paths; remove empty hype. Make a boost request only when sharing serves a concrete reader need, without pressure. Neither a blanket boost-request taboo nor automatic cross-post suspension is established here (directional).

## Examples

These are illustrative drafts, not reports of real launches. Bracketed facts and links must be supplied and checked before publication; no example is publishable unchanged. All proposed tags require the live-tag check.

### Developer tool announcement

> [Tool] now shows the file that supplied each setting. I built it for debugging inherited configuration. The screenshot uses [documented fixture]; it doesn't cover environment overrides yet. Release notes and a runnable example: [link]. #DevTools

Asset brief: capture the actual setting and its source. Alt text: “[Setting] has value [value], read from [file]; environment overrides aren't shown.”

Why it works: the launch shape names behavior a developer can inspect.
The provenance rule keeps both the fixture and limitation explicit.

### B2B SaaS proof

Illustrative brief: an operations team uses invoice-matching software; customer permission and measurements still need source records.

> [Customer, with permission] used [product] to match invoice exports. In [measurement period], [defined measure] moved from [before] to [after] across [sample]. Their team still reviewed disputed matches. I work on the product; the method and exclusions are here: [link].

Why it works: the proof shape bounds the outcome with its measurement conditions.
Affiliation and the remaining manual work support an informed buying decision.

### Creator artifact

> I've put the sewing pattern for [bag] online. The instructions use [tested fabric]; I haven't checked the fit with heavier canvas. The sample photo shows the inside seam before lining. Pattern and materials notes: [link]. #Sewing

Asset brief: show the documented seam. Alt text: “Inside seam of [bag], showing [visible seam construction] before the lining is attached.”

Why it works: the artifact carries useful information without a sales preamble.
The format rule keeps the caption brief and the limitation near the link.

### Local service

Illustrative brief: a cycle-repair organizer offers puncture repairs at a community session; damaged rims need workshop assessment.

> We're taking bookings for the cycle-repair session at [venue] on [date]. Bring a bike with a puncture; we can patch inner tubes, but damaged rims need the workshop. I run the session. Access details and booking: [link]. #[VerifiedLocalTag]

Why it works: the service post answers the practical booking decision.
The scope boundary prevents an invitation from becoming a repair guarantee.

### Technical reply repair

Over-structured draft to revise: a reply with a benefits heading and an unnecessary caveats section, ending by summarizing the original post without answering its question.

> [Documented setting] controls that behavior. The example in [source] covers [supported case]; it doesn't establish what happens during [unverified condition]. I'd leave that part open until there's a trace.

Why it works: reply register stays in prose and answers the specific concern.
The provenance rule keeps uncertainty attached to the missing evidence.

## Checklist

- [ ] First line carries the useful point; the post develops a focused idea.
- [ ] Every specific is supplied or example-placeholder-marked; no unresolved placeholders in publishable copy.
- [ ] Voice and substance reviewed; useful structure preserved without manufactured errors or style quotas.
- [ ] Server rules checked for commercial content and AI use; required disclosures present.
- [ ] Visibility and quote permissions deliberate; reply recipients checked.
- [ ] Live character, attachment, poll, and alt-text limits checked; post language set correctly.
- [ ] Relevant tags verified live; CW matches material and local rules.
- [ ] Clean link works; CTA or deliberate no-CTA choice matches the brief.
- [ ] Publishing package includes caption, asset brief, alt text, and captions/transcript where needed; poll options reviewed if used.
- [ ] Reply owner and follow-up plan set; scheduling and edits checked when applicable.

## References

- [Timelines](https://docs.joinmastodon.org/methods/timelines/) and [Trends](https://docs.joinmastodon.org/methods/trends/), 2026-05.
- [Network](https://docs.joinmastodon.org/user/network/) and [Quote posts](https://docs.joinmastodon.org/user/quote-posts/), 2025-11.
- [Posting](https://docs.joinmastodon.org/user/posting/), 2026-07; [PreviewCard](https://docs.joinmastodon.org/entities/PreviewCard/), 2026-06.
- [Release](https://blog.joinmastodon.org/2026/06/mastodon-4.6/), 2026-06; [Foundation preview](https://blog.joinmastodon.org/2026/08/5.0-laying-the-foundation/), 2026-08.
- [Community Standards](https://help.joinmastodon.org/article/12-community-standards), 2026-02; [Server terms](https://blog.joinmastodon.org/2026/07/announcing-new-terms-of-service-for-our-servers/), 2026-07.
- [Buffer](https://buffer.com/resources/state-of-social-media-engagement-2026/), 2026-03.
- [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/), 2026-07; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), 2026-06; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how), 2026-02. Practitioner heuristics only.
- [Mechanics reference](reference/mechanics.md) and [Evidence reference](reference/evidence.md), maintained 2026-09; scoped sources and checks for optional formats.

Re-validate when server limits or policies change, discovery features ship, UI labels change, ranking code changes, or new benchmark reports appear.
Validated: 2026-09
