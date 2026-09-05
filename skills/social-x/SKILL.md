---
name: social-x
title: "X (Twitter) Publishing Playbook"
description: "Write and revise X posts, replies, threads, profiles, and launch proof in the author's documented voice. Activate for X or Twitter publishing copy, product announcements, demos, customer outcomes, and post-publication reply plans. Choose formats and conversion paths using dated evidence without inventing experience or promising reach."
license: Apache-2.0
compatibility: "Text editing; network access for source checks and a signed-in X session for account-specific format validation."
domains: content
rules:
  - content(tweet)
  - content(tweets)
  - content(twitter)
  - match(\b(twitter|x)\s+thread\b)
  - match(\btweetstorm\b)
  - match(\bpost\s+(on|to|for)\s+(x|twitter))
  - match(\b(x|twitter)\s+(post|reply|bio|launch|article|space)\b)
  - match(\bviral\s+(tweet|thread|post)\b)
  - match(\bwrite.{0,40}for\s+(x|twitter)\b)
---

## Overview

Write X copy that a particular person can stand behind and a relevant reader can use. Apply supplied facts and proof first, the author's documented voice next, and platform structure afterward. Use `content-voice` for generic editing; this skill supplies X decisions. Publishing is a downstream step.

Open `reference/mechanics.md` when checking ranking, labels, subscription claims, format availability, or a suspected penalty. Open `reference/launch.md` when planning launch execution, choosing benchmark tests, or reporting outcomes. Open `reference/examples.md` when drafting a thread, long post, bio, or casual-chain reply.

## Mental model

For You combines followed-account candidates from Thunder with Phoenix retrieval and SimClusters for out-of-network discovery. Ranking orders candidates; visibility filtering separately returns allow, interstitial, or drop. The documented candidate path filters out-of-network replies and reposts and posts older than 48 hours (official, X algorithm README, 2026-08). Don't extend this cutoff to every X surface.

Use originals for a discovery attempt and replies to address an existing conversation (directional). A conditional new-author lift exists for originals; it excludes replies and reposts (official, X cold-start, 2026-08). It promises neither impressions nor customers.

Published weights multiply predicted actions, not observed engagement counts. Repeated-author scoring operates within a feed request; it supplies no daily posting quota (official, X parameters, 2026-08). Bookmarks can indicate reader utility when available, but this evidence establishes no current bookmark weight. Don't solicit saves or describe them as either a proven boost or a proven non-signal.

## Format and anatomy decisions

Choose the shortest form that preserves the claim and its conditions (directional). Start with the useful observation or visible result. Keep the post about a single idea; add enough context to interpret it. End when the information ends, or state the chosen action. A twist and a quotable moral aren't required.

| Situation | Choose | Boundary or decision |
|---|---|---|
| Compact observation | Short single | Stop when complete; no engagement sweet spot is established |
| Claim needs a qualification | Fuller single | Ordinary composer limit: 280 characters (official, X posting help, 2026-09); check the composer with the final URL |
| Explanation must be read continuously | Longer post | Up to 25,000 characters for Premium subscribers (official, X Premium, 2026-09); use only the space needed |
| Distinct steps each have useful evidence | Thread | Break at a change of claim or artifact; each entry must make sense on its own; apply the selected composer's limit to each entry |
| Another post supplies necessary context | Reply | Address its actual claim; read the chain before drafting |
| Your audience needs the context too | Quote | Add analysis or a substantiated counter-case; represent the original fairly |
| Reusable formatted explanation | Article candidate | Check account access and formatting in the live editor before assigning it; this evidence doesn't establish its tier or cap |

Craft decisions in this table are directional; the labeled limits are platform constraints. Don't split a complete thought merely to make a thread. Don't promise a thread or long-post ranking multiplier.

| Evidence to show | Media choice (directional) |
|---|---|
| Language carries the whole point | Text alone |
| A visible state or comparison matters | Legible screenshot or image; include source context and alt text |
| Sequence or interaction matters | Native demo video; caption speech and show the relevant action early |
| A reaction fits the author's established register | Context-appropriate GIF; avoid using it to answer a serious objection |
| Sustained explanation needs motion | Longer video; verify upload support before preparing the asset |

X's current app help permits up to 4 total media items, including mixed photos, GIFs, and video; verify the target client's accepted combination and preview its layout (official, X posting help, reviewed 2026-09-05). Don't brief a multi-image layout as a swipe carousel. Video duration/file-size caps still need tier/client verification. A vertical cut is a presentation choice, not a promised video-tab boost (directional).

Write each image's alt text for the visible evidence, including relevant screenshot text; X allows 1,000 characters per image. Put a longer source document's link in the post, not only the description. X's image-description field doesn't cover video: supply captions and a textual explanation of essential visual action (official, X image-description help, reviewed 2026-09-05; video explanation is editorial guidance).

Text narrowly led images in Buffer's X format sample; video wasn't the engagement leader (measured, Buffer, n=X subset of 52M+ cross-platform posts, 2026-03). Media must earn its place.

For optional surfaces, use these as conditional assignments, not availability promises (directional): an Article for a formatted evaluation guide; Spaces for a live discussion with an available host; a poll for an answer that will change a decision; Communities for participation that fits the visible rules; Lists for listening; DMs for relevant follow-up with permission. Check access and current controls first. A poll response isn't representative customer research.

## Launch and proof posts

For campaign planning, record audience, buying situation, promise, sourced proof, desired action/destination, stage, and disclosures. Verify availability and pricing if mentioned. No CTA is valid. Missing optional brief fields or voice samples don't block supported copy; narrow or withhold claims lacking essential evidence, and continue independent edits without inventing specifics.

These shapes and length bands are craft choices (directional). “Single” uses the ordinary limit above; “long” uses the verified longer-post limit. No band predicts performance.

| Shape | Anatomy | Length band |
|---|---|---|
| Launch day | Who can use it now, task it handles, visible proof, access conditions, action | Compact to fuller single; move supporting evidence into follow-ups |
| Demo or artifact | Task, artifact, what to inspect, known constraint | Short single beside media; thread for distinct steps |
| Customer outcome | Prior condition, observed change, source and measurement conditions, limitation, permitted attribution | Fuller single; long post when qualifications need room |
| Founder decision | Decision, evidence considered, actual cost or tradeoff | Fuller single or long post |
| Objection answer | Fair statement of concern, evidence-based answer, remaining limitation | Reply in context; original if broadly useful |
| Recap | What changed after use, unresolved issue, next useful artifact | Single or evidence-led thread |

Use the strip-test on demos and proof: if the product name disappears, the reader should still learn something or see useful work (directional). Don't invent a customer transformation to satisfy the shape. Keep dates, cohort definitions, and exclusions beside outcome claims. Get permission for customer quotes and private screenshots.

| Desired path | Placement decision (directional) |
|---|---|
| Immediate trial, booking, purchase, or source inspection | Put the destination in the root when hiding it would obstruct the action |
| Self-contained explanation with optional detail | Test a link in a clearly identified follow-up reply; compare qualified visits as well as reach |
| Continuing profile discovery | Keep the profile destination and pinned introduction aligned with the promise |
| Header artwork | Treat as visual context; don't rely on a printed URL as the conversion path |
| Long evaluation document | Use an accessible Article or external document; preview the destination and its CTA |

External-link posts showed lower visibility in political-discussion datasets (measured, NDSS, n=over 40M posts across political datasets, 2026-02). That doesn't establish a universal penalty or prove a link-in-reply workaround. Keep a usable destination when conversion is the goal. Use consistent `utm_source`, `utm_medium`, and `utm_campaign`; distinguish placements with `utm_content` (official, Google Analytics, 2026-09).

State the author's affiliation. Enable Paid Partnership for compensated, gifted, affiliate, or ambassador promotions (official, X Paid Partnerships, 2026-09). Record AI-media provenance, including synthetic people or scenes. X describes EU “Made with AI” indicators separately from restricted-reach labels (official, X Media Literacy, 2026-07); this doesn't establish a blanket AI-text disclosure rule or AI-label penalty.

Seed through relevant conversations where participation is welcome (directional). Match collaborators to audience and expertise; brief proof and constraints while preserving their own wording. Keep creator results separate from brand results. Agency launch cases support testing this approach, not forecasting sales (directional), citing Clickstrike, undated. Don't use bulk unsolicited replies/DMs, irrelevant promotions, duplicate link drops, or coordinated metric inflation (official, X Authenticity, 2025-04). Employee participation must be voluntary, truthful, and distinct. For a Product Hunt destination, invite feedback without requesting or rewarding upvotes; don't recruit HN votes or comments through X (official, Product Hunt launch guide and Show HN, 2026-09).

Use founder handles for documented decisions and personal answers; use brand handles for product facts and support continuity (directional). No verified X founder-versus-brand conversion uplift is supplied.

The following T-7 to T+7 schedule is an editorial plan (illustrative), not a measured optimum. T is launch day. Skip slots without new evidence.

| Day (illustrative) | Post shape | First-hours reply plan | Measure if available |
|---|---|---|---|
| T-7 to T-4 | Problem observation or useful artifact | Listen for exact buying constraints | Relevant replies and recurring objections |
| T-3 to T-1 | Demo preview and access conditions | Answer fit questions; record blockers | Demo requests and qualified profile interest |
| T | Original announcement plus working proof | Assign a responder; correct misunderstandings | Qualified replies, destination clicks, trial requests |
| T+1 to T+3 | Objection answer or additional demonstration | Return to unresolved questions | Resolved blockers and permission-based DM conversations |
| T+4 to T+7 | Bounded outcome or lessons | Follow up on actual use | Qualified follow-ups and attributed activation |

Keep native observations separate from downstream analytics. Attribute signups only with supporting records; an impression isn't demand. Carry unresolved attribution as unknown.

## Voice on this platform

Use the author's approved posts to establish their register. Read a reply's surrounding chain for technical precision, warmth, and expected length. Match conversational context without borrowing someone else's identity or slang. Prefer prose in replies; avoid a miniature slide deck. Add a specific answer or useful counter-case and omit unrelated self-promotion (directional).

Preserve natural contractions and fragments. Lowercase is appropriate only when documented in the author's voice; don't add errors, fake edits, missing apostrophes, or typo quotas. Use niche slang or a meme only when its meaning and the author's usage are clear. Have a fluent reviewer check uncertain local idiom (directional).

Apply `content-voice` to X's compressed forms: revise filler, repeated suspense, and slogans that replace the actual finding. Retain useful contrasts, lists, summaries, and the author's punctuation when they carry meaning. These practitioner heuristics aren't authorship tests or proven ranker triggers; don't impose sentence-length, contraction, or punctuation quotas (directional), citing Aborn, 2026-07; Cox, 2026-06; Gichigi, 2026-02.

Ask a question when the answer will inform the conversation, not to withhold the post's point or demand engagement. Remove unsupported “nobody talks about” claims and decorative tag stacks; use thread labels or emoji only when they aid navigation or match the author's register. Relevant event/community hashtags are valid; ad rules don't establish an organic hashtag ban (directional). Use supplied proof for personal stakes; never turn research into “I tested” testimony. Detector scores don't certify authorship.

## Cadence and engagement

Publish at a recurring pace the author can sustain and answer substantive responses. Expand output only while useful material and response capacity support it (directional). Buffer associates frequency with growth, with reduced per-post reach at higher frequency; these observations don't establish an X daily quota (measured, Buffer, n=4.8M channel-weeks; separate 15.7M-post reach analysis, 2026-03).

Test weekday mid-mornings, then use account evidence and event timing. Buffer's baseline is 9–11 a.m., with Tuesday and Wednesday leading slots (measured, Buffer timing, n=8.7M X posts, 2026-03). Choose and record the audience timezone. Don't impose an evening window.

| Account situation | Time allocation (directional) |
|---|---|
| Small follower base, little relevant conversation | Protect time for original proof; use replies to learn buyer language |
| Growing relevant following | Keep originals recurring; increase response time as substantive questions grow |
| Established audience or brand support load | Staff replies and escalation; turn repeated objections into sourced originals |

Follower count alone doesn't justify a reply/original ratio. Plan coverage in the first hours and return to unresolved questions afterward. Buffer's reply association is uncertain and non-causal (measured, Buffer, n=nearly 2M cross-platform posts, 2026-03). Don't manufacture self-reply loops. Update the bio and pinned introduction when the offer changes; state the real work and reader benefit (directional).

## What gets suppressed

Separate policy evidence from low engagement. X prohibits deceptive manipulated media and spam and can restrict reach for violations (official, X Authenticity, 2025-04). Review sources and context for factual claims; retain correction material if challenged or exposed to Community Notes scrutiny. Don't assert a Notes-specific ranking effect without evidence.

When available, inspect `https://x.com/i/under_the_hood` for aggregate visibility labels before diagnosing suppression; availability is a pilot (official, X algorithm README, 2026-08). Distinguish provenance labels, policy actions, and ad-adjacency classifications. Neither awkward prose nor `slop_score` proves a reach penalty. Open the mechanics reference for the actual safety categories and source limits.

## Examples

These are fictional teaching briefs and drafts, not reported results. Their premises are illustrative; production copy needs equivalent supplied evidence. Bracketed specifics remain unpublishable until filled and verified.

### Developer tool: artifact post

Illustrative brief: dry technical voice; patch preview works; generated files are excluded.

> The patch preview shows which files the rename will touch before you accept it. Generated files are excluded for now. The recording follows the change through review.

Why it works: the artifact rule makes the demo's inspection task clear.
The provenance rule keeps the supported limitation beside the claim.

### B2B SaaS: customer proof

Example brief: approved customer measurement still needs to be supplied.

> [Customer] reduced invoice review time from [before] to [after] during [period]. This covered [cohort]; disputed invoices still needed manual review. Method and approved results: [source URL].

Why it works: the proof shape includes measurement scope and an unresolved condition.
The provenance rule makes the missing evidence visible; this draft cannot ship yet.

### Consumer creator: product availability

Illustrative brief: ceramicist's warm, plain voice; sample photos show darker glaze around the handle; glaze varies. No personal preference has been supplied.

> The blue glaze runs darker around the handle, as the sample photos show. Each fired piece will vary. Available pieces: [shop URL].

Why it works: the description uses supplied visual facts without inventing the maker's preference.
The link rule puts the shopping path beside the product's real limitation.

### Local service: reply in a casual chain

Illustrative brief: bicycle mechanic's conversational voice; someone asks whether a chain noise can be diagnosed from a clip.

Weak draft problem: it offers a confident diagnosis without seeing the bicycle.

> That noise could be the chain rubbing the front derailleur. I can't confirm it from the clip, so a side view while you turn the pedals would help.

Why it works: chain matching keeps the reply conversational and useful.
The evidence rule preserves uncertainty without adding fake mobile typing errors.

## Checklist

- [ ] First line delivers the actual point or visible result.
- [ ] The post develops a single idea.
- [ ] The selected format fits the publishing account's verified constraints.
- [ ] The link and CTA path works, or no CTA is deliberate.
- [ ] Every specific has supplied provenance or is marked as an example placeholder.
- [ ] No unresolved placeholder remains in publishable copy.
- [ ] Customer attribution and private material have permission.
- [ ] Voice and substance review preserves useful structure without style quotas or authorship claims.
- [ ] The author recognizes their voice and approves personal claims.
- [ ] Required partnership disclosure is set.
- [ ] AI-media provenance and applicable labeling have been checked.
- [ ] Factual claims retain their conditions and source context.
- [ ] The package includes final copy and destination.
- [ ] Applicable images have alt text and an asset brief.
- [ ] Applicable video has captions and an asset brief.
- [ ] A follow-up reply plan has an owner.
- [ ] Measurement separates qualified interest from raw engagement.

## References

- X algorithm: [README](https://github.com/xai-org/x-algorithm/blob/main/README.md), [parameters](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/params/param.rs), [cold-start](https://github.com/xai-org/x-algorithm/blob/main/home-mixer/scorers/author_cold_start.rs). Dated evidence snapshot: August 12–13, 2026; details in `reference/mechanics.md`.
- X Help: [posting](https://help.x.com/en/using-x/how-to-post), [Premium](https://help.x.com/en/using-x/x-premium), [Paid Partnerships](https://help.x.com/en/rules-and-policies/paid-partnerships-policy), undated, reviewed September 2026; [Authenticity](https://help.x.com/en/rules-and-policies/authenticity), April 2025; [Media Literacy](https://help.x.com/en/rules-and-policies/media-literacy-plan), July 2026.
- [Image-description controls](https://help.x.com/en/using-x/picture-descriptions) and [writing image descriptions](https://help.x.com/en/using-x/write-image-descriptions), reviewed 2026-09-05.
- Buffer: [engagement report](https://buffer.com/resources/state-of-social-media-engagement-2026/), March 5, 2026; [timing](https://buffer.com/resources/best-time-to-post-on-twitter-x/), March 13, 2026. [NDSS link study](https://www.ndss-symposium.org/wp-content/uploads/2026-s718-paper.pdf), February 2026.
- [Google campaign URLs](https://support.google.com/analytics/answer/10917952?hl=en), [Product Hunt launch sharing](https://www.producthunt.com/launch/sharing-your-launch), [Show HN](https://news.ycombinator.com/showhn.html): undated, reviewed September 2026. [Clickstrike](https://clickstrike.com/launch-playbook/), undated agency self-report.
- Voice heuristics: [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/), July 10, 2026; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), June 2026; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how), February 18, 2026. Scope and further sources in `reference/examples.md`.

Re-validate when:
- Features, tiers, or publishing controls change.
- Policies or algorithm commits change, including runtime defaults.
- New vendor reports replace these samples.

Validated: 2026-09
