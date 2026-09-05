---
name: social-medium
title: "Medium Publishing Playbook"
description: "Draft and revise Medium stories in the author's documented voice, with sourced proof and a deliberate business purpose. Covers publication submissions, native launches, canonical syndication, disclosure, reader access, and measurement. Activate for writing for Medium, publishing on Medium, a Medium draft or piece, or revising a Medium publishing plan."
license: Apache-2.0
compatibility: "Requires a text editor; network access and a Medium account for publishing and story statistics."
domains: content
rules:
  - match(\bmedium\.com\b)
  - match(\bmedium\s+(article|post|story|publication|draft|piece|newsletter)\b)
  - match(\b(post|write|writing|publish|publishing|draft)\s+(on|to|for)\s+medium\b)
  - match(\bmedium\s+partner\s+program\b)
  - match(\bboost\s+nomination\b)
---

## Overview

Write a useful story whose judgments belong to the named author. Start with supplied facts and proof, then the author's documented voice; use Medium register as the fallback. Apply `content-voice` for general editing, with the platform decisions below.

## Mechanics and mental model

| Distribution | Meaning |
|---|---|
| Network | Reaches followers of the writer or publication. (official, Distribution Guidelines, 2026-06) |
| General | Matches reader interests and related follows, including beyond the author's followers. (official, Distribution Guidelines, 2026-06) |
| Boost | Human curators select stories for higher-priority distribution; no structural checklist guarantees selection. (official, Distribution Guidelines, 2026-06) |

Publication-editor Boost nominations closed on May 31, 2026; internal review continues and publications remain a discovery source. Don't pitch nomination access. (official, Nomination update, 2026-05)

Publication acceptance and authentic recommendations matter: Medium attributes most average-feed stories to human actions. (official, Curation era, 2026-07) Publication stories receive more presentations, views and reads in Medium's aggregate data, especially for smaller followings; this isn't an individual guarantee. (measured, Reader tips, n=Medium platform data with sample undisclosed, 2026-03)

Open [reference/mechanics.md](reference/mechanics.md) when advising on earnings, interpreting performance evidence, preparing newsletter or technical assets, or checking a publication's submission controls.

## Rules and format decisions

Record the author's actual position and supporting source for each factual assertion before drafting. Don't invent experience, quotations, dates, or outcomes. Mark missing specifics with bracketed placeholders in example drafts; a draft with unresolved placeholders isn't publishable. Prefer omitting an unsupported claim when it adds nothing.

### Destination and access

| Situation | Choose |
|---|---|
| Small following; relevant publication accepts submissions | Submit a tailored draft; use audience fit and editorial quality. No follower threshold applies. (official, Worth it, 2026-02) |
| Established relevant following; no editorial dependency | Consider solo publication for control; compare your own outcomes. (directional) |
| No publication access, poor topic fit, or incompatible deadline | Publish a complete solo story and build a proof portfolio; pursue editorial relationships separately. (directional) |
| Existing article on an owned domain | Use Import for syndication. It backdates publication and sets the original URL as canonical; inspect both before publishing. (official, Import, 2026-09) |
| New argument or materially different reader problem | Write a native story; cite earlier work where relevant and avoid duplicate Medium versions. (directional) |
| Discovery or buyer evaluation is the goal | Prefer free access; keep the article useful without visiting the destination. (directional) |
| Eligible original work; member earnings are the goal | Consider a paywall; don't imply it creates a superior audience. Open the earnings reference first. (directional) |
| Paywalled story needs unrestricted sharing | Use an author/editor Friend Link. Member reads can still earn; nonmember reads through that link don't. (official, Friend Links, 2026-09) |

### AI disclosure and authorship

| Actual contribution | Action |
|---|---|
| Human-authored material | Preserve its evidence and voice; don't add fictional disclosure or experience. |
| AI-generated text, including incorporated assistance | Describe the actual assistance clearly near the opening. For generated text, place disclosure within the first two paragraphs. (official, AI policy, 2026-09) |
| AI-generated writing, even disclosed | Keep it off the paywall. It cannot receive General or Boost distribution. (official, AI policy, 2026-09; official, Distribution Guidelines, 2026-06) |
| Undisclosed generated or assisted text | Resolve disclosure before publication; undisclosed text is restricted to Network. Paywall violations can remove paywall access or revoke enrollment. (official, AI policy, 2026-09) |
| Author wants an original essay instead | Have the author develop the argument from their records and write it; reassess the finished contribution honestly. Surface rewording doesn't establish human authorship. (directional) |
| Synthetic illustration or narration proposed | Document its origin; caption synthetic assets plainly and check current applicable controls before publishing. Don't invent a disclosure toggle or treat media as evidence of an event. (directional) |

### Story anatomy and assets

Write a title that names the subject and earned claim. Let the subtitle add scope or a limitation. Open on a documented event, a concrete finding, or the reader's actual problem. Build sections around evidence and decisions; end when the reader has the promised answer. (directional)

Choose length by purpose: Medium accepts well-crafted short and long stories. Recent evidence is useful for timely analysis, but no universal recency window or argumentative headline is required. (official, Distribution Guidelines, 2026-06)

Use descriptive headings in long guides. Structured stories receive an automatic web table of contents without a writer toggle; don't promise retroactive coverage. (official, Long reads, 2026-07)

Prepare readable code blocks for short excerpts and a linked gist or repository for full examples; preview any embed and provide a text fallback. Give prerequisites and expected output from supplied evidence. Don't claim code was run unless a record proves it. These are packaging choices, not guarantees of editor support. (directional)

Choose a cover that explains the subject. Supply an asset brief stating the image's purpose and source, with crop guidance. Write a factual caption, attribution, and useful alt text; verify rights and mobile readability. Don't manufacture screenshots or customer scenes. (directional)

Use all five topic slots when accurate fits exist; relevance beats broad popularity. Topic pills now appear at the story's top. (official, Reader tips, 2026-03; official, Writer newsletter, 2026-08)

### Publication submission and recovery

Read the live guide for accepted subjects, draft status, rights, AI rules, and submission method. Check length and formatting instructions. Publication controls can require a subtitle, preview image, shared topic, paywall status, or minimum reading time. (official, Submission controls, 2026-07)

Match a relevant story topic to the publication's About-page topics. Topicless or unmatched drafts can receive an off-topic badge; the badge doesn't automatically reject them. (official, Off-topic badge, 2026-06)

Editors may include an optional rejection reason in the status email. (official, Writer newsletter, 2026-08) Use these editorial decisions, not assumed platform reason codes:

| Feedback | Next step |
|---|---|
| Subject or audience mismatch | Find a better-fit publication or publish solo. (directional) |
| Named evidence or craft problem | Fix it; resubmit only under the publication's rules. (directional) |
| Submission requirement missed | Correct the requirement without distorting the story. (directional) |
| No explanation | Recheck the guide; move on without repeated editor mentions or duplicate submissions. (directional) |

## Launch and proof posts

Take a campaign brief before drafting: audience and buying situation; promise; available proof with sources; desired action and destination; campaign stage (teaser / launch day / proof / objection / recap); disclosure obligations. Accept a deliberate no-CTA choice. If proof is missing, draft an explanation or proposal without presenting it as a result.

Use these qualitative length bands as craft guidance; they aren't word-count benchmarks. (directional)

| Shape | Anatomy | Length band |
|---|---|---|
| Launch day | Reader problem → demonstrated change → availability and exclusions → optional next step. Remove the product name: the explanation should still teach something. | Compact to medium essay. (directional) |
| Demo or artifact | Task → prerequisites → reproducible walkthrough → observed output → failure boundary and artifact link. | Medium to long guide. (directional) |
| Customer proof | Baseline → intervention → sourced outcome with denominator and observation window → confounders and permission → evaluation path. | Medium to long case study. (directional) |
| Founder decision / build in public | Decision → evidence considered → cost or unresolved tradeoff → next observation. Link installments as a developing record. | Compact to medium essay. (directional) |
| Objection answer | State the buyer's objection accurately → test or explanation → conditions where it remains valid → optional evaluation link. | Compact to medium explanation. (directional) |
| Recap | Compare intended outcome with observed result → limits of attribution → next decision. | Medium retrospective. (directional) |

Put a relevant first-party link beside the artifact or at the earned ending; keep a profile link as a secondary path. State founder, employee, or commercial affiliation where it affects trust. First-party business and mailing-list links are allowed; traffic-first spam and third-party advertising or sponsorships are prohibited. Disclosure doesn't authorize a prohibited sponsored placement. (official, Medium Rules, 2026-09)

Use consistent `utm_source`, `utm_medium`, and `utm_campaign`; distinguish links with `utm_content`. (official, Google URL builder, 2026-09) Measure destination actions separately from Medium engagement; attributed visits don't prove sales causation. (directional)

Seed through relevant editorial relationships and willing readers who can recommend the work in their own words. Repost notes allow up to 280 characters and appear in followers' For You feeds. (official, Repost notes, 2026-07) Give context about the audience and useful passage. Don't script employee praise or trade claps. (directional)

Illustrative launch-week offsets below are a planning example, not measured timing advice. Shift them to editorial availability and actual proof; a row can be preparation rather than another published story. (directional)

| Offset (illustrative) | Medium work | Reply commitment and measurement |
|---|---|---|
| T−7 | Prepare problem essay and publication pitch; choose solo fallback. | Owner reviews substantive responses; record recurring buyer problems. |
| T−3 | Finish demo and access checks; coordinate newsletter inclusion if available. | Reserve opening-hours coverage; record baseline audience totals. |
| T0 | Publish the launch explanation and artifact. | Author answers evidence questions during the first hours; record views/reads actually exposed. |
| T+1 to T+3 | Correct errors; answer a substantive objection if evidence warrants it. | Return at the promised check-in; log qualified questions and reported trial attempts. |
| T+7 | Publish a bounded recap if there is enough evidence; update the portfolio. | Review read ratio and audience change alongside attributed destination actions. |

Prefer the accountable founder or practitioner byline for personal decisions; use a company publication for a maintained collection. This is a voice and ownership choice, with no verified founder-versus-brand reach multiplier here. (directional)

## Voice on this platform

Use connected essay prose with informative subheads. Keep technical register precise; let personal essays retain the author's natural contractions or fragments. Don't import a feed-thread rhythm of isolated dramatic lines. Start inside the subject instead of announcing what the article will cover. (directional)

Apply the general AI-tell pass from `content-voice`: remove padded contrast frames and decorative triads; inspect uniform short paragraphs, suspense pivots, and repetitive emphasis. Cut obligatory moral endings. These are practitioner editing heuristics, not authorship tests. (directional) Sources: Aborn, 2026-07; Cox, 2026-06; Gichigi, 2026-02.

For Medium, replace generic section labels with the actual decision; avoid a Key Takeaways box that repeats the ending. Remove rhetorical-question openings, miracle-fix narratives, and claims that nobody discusses the subject. Drop engagement-bait closers and hashtag stacks. Use useful punctuation sparingly; don't add typo quotas, fake edits, or lowercase camouflage. Match the author without introducing errors. (directional)

Medium describes AI detection as unreliable and rejects phrase or punctuation tells as durable evidence. Treat provenance and disclosure as separate checks from prose quality. (official, Write for humans, 2026-08)

## Cadence and engagement

Choose a sustainable cadence and declare a response owner with an actual availability window before publishing. Write concise responses that address the passage and add relevant evidence; don't promise distribution or earnings from comments. (directional)

Build toward a continuing editorial relationship if you have access. Without access, develop a solo series and improve the portfolio from real reader questions. Group related expertise stories in a List and link it from About; Medium documents Lists as browsable portfolios. (official, Self-promotion guide, 2025-11)

Use the 160-character bio for your subject and relevant credentials; add a clear photo and expand About with context and links. (official, Reader tips, 2026-03) Medium reports more followers for completed bios without measuring each profile element separately. (measured, Reader tips, n=Medium platform data with sample undisclosed, 2026-03)

For writer newsletters, prepare an accurate subscription promise. For publication newsletters, pitch the story's relevance to the editor; verify the available sending controls and access path. Don't promise automatic sends or infer per-story subscriber attribution from account totals. (directional)

Open the story Stats view or request its screenshot/export. Record the fields actually shown and their date range. Separate feed presentations from all-source views; calculate feed CTR only from corresponding feed views and presentations. Never divide total views by feed presentations. (directional) Treat read ratio as distinct from completion: a qualifying read requires at least 30 seconds. (official, Earnings, 2026-09)

Compare similar stories using sufficient observations; change a weak title or preview deliberately and log the change. If feed data is unavailable, use views, reads and qualitative responses without inventing CTR. No fixed rewrite deadline or threshold is required. (directional)

## What gets suppressed

Medium prohibits repetitive promotional interactions, engagement brigades, bought or automated engagement, duplicate stories, and lightly modified templates; spam can be removed. (official, Medium Rules, 2026-09) Keep launch value in the story and apply the disclosure table before submission. Don't describe awkward prose as an account penalty or promise a formula for Boost.

## Examples

All scenarios below are illustrative, including their supplied facts. They are not actual customer evidence. Replace bracketed fields from records before publication; don't transfer these experiences to an author.

Disclosure example, only if true: “An AI writing tool helped draft the explanation. I checked it against the attached records.” Describe the actual contribution; this wording cannot make generated writing paywall-eligible.

### Developer tool: opening and demo

Illustrative brief: maintainer, reproducible parser failure, workaround still required.

Bad opening: “It's not about parsing. It's about trust. Here's the thing.”

Better title: “Where our parser loses quoted commas”

> The attached fixture puts a comma inside a quoted field. Our parser splits it anyway. I maintain the parser; this walkthrough follows that failure into the tokenizer and shows the workaround we can support today. Multiline fields remain outside this test.

Package: readable fixture and output; link the reproduction beside the explanation.

Why it works: the opening earns its claim through the artifact rule.
Why it works: the limitation prevents a miracle-fix story.

### B2B SaaS: bounded customer proof

Bad: “Our approval tool transformed the customer's entire operation.”

Better title: “The approval queue after the routing change”

> At [customer], median approval time moved from [before] to [after] during [window], across [denominator] requests. The team also changed staffing. I work for [vendor], and the attached case notes can't isolate the software's contribution.

Package: permission and measurement method; end with a relevant evaluation link, not a purchase demand.

Why it works: the proof shape preserves the denominator and attribution limit.
Why it works: placeholders enforce provenance; this draft isn't publishable yet.

### Consumer creator: objection and artifact

Illustrative brief: sewing-pattern designer; prototype permits a seated reach test; durability untested.

Bad: “The perfect pocket for every commuter.”

Better opening:

> I moved the pocket opening toward the side seam so I could reach it while seated. The prototype photo shows the resulting fold. I sell the pattern; this version still needs wear testing before I recommend it for heavy fabric.

Package: credited prototype photo with alt text; offer the pattern's measurement sheet after explaining the test.

Why it works: the objection answer shows the artifact before the CTA.
Why it works: the author owns the commercial relationship and remaining uncertainty.

### Local service: decision and follow-up

Illustrative brief: repair shop owner; intake photos support estimates; hidden damage remains unknown.

Bad: “A simple change fixed our quoting problem forever.”

Better title: “Why we ask for a hinge photo before quoting a repair”

> A close photo lets me see whether the hinge plate has pulled away from the frame. I can then explain the likely repair before the visit. I still can't see concealed rot, so the estimate stays provisional until we inspect the door.

Package: permission-cleared example photo and caption; link booking after the limits. Follow up with actual inspection findings when available.

Why it works: the founder decision explains a buyer-facing constraint.
Why it works: the service claim stays bounded instead of inventing a success statistic.

## Checklist

- [ ] Title and first line deliver a clear subject; subtitle adds scope.
- [ ] Central idea holds; chosen length serves the evidence.
- [ ] Every specific comes from supplied proof; no unresolved example placeholders.
- [ ] Author voice matches; AI-tell pass checks structure and ending without manufactured mistakes.
- [ ] AI contribution reviewed; required disclosure placed; paywall choice complies.
- [ ] Publication guide and live controls checked; rejection/solo path ready.
- [ ] Accurate topics selected within the documented limit.
- [ ] Import date and canonical verified when syndicated; Friend Link tested when used.
- [ ] Affiliation clear; first-party CTA and destination work; promotion stays subordinate.
- [ ] Asset brief, credits, caption and alt text supplied; code and embeds previewed with fallbacks.
- [ ] Newsletter or List package included when relevant; no assumed send automation.
- [ ] Response owner and commitment window recorded; follow-up reply plan ready.
- [ ] Stats source and comparison window specified; no invented CTR or completion claim.

## References

Dates identify source publication/update months; undated help pages use the validation month. Detailed sources and evidence limits: [mechanics reference](reference/mechanics.md#references).

- [Distribution Guidelines](https://help.medium.com/hc/en-us/articles/360006362473-Medium-s-Distribution-Guidelines-How-curators-review-stories-for-Boost-General-and-Network-Distribution), 2026-06-29.
- [AI policy](https://help.medium.com/hc/en-us/articles/22576852947223-Artificial-Intelligence-AI-content-policy), undated, checked 2026-09.
- [Medium Rules](https://help.medium.com/hc/en-us/articles/213477928-Medium-Rules), undated, checked 2026-09.
- [Reader tips](https://medium.com/medium-handbook/four-basic-tips-to-reach-readers-on-medium-3544b5397ff3), 2026-03-04.

Re-validate when: distribution names or submission controls change; AI/paywall policy updates; stats or newsletter interfaces change; new format or performance reports appear.
Validated: 2026-09
