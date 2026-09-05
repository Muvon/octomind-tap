---
name: social-hackernews
title: "Hacker News Publishing Playbook"
description: "Prepare source-grounded Hacker News submission briefs, human-authorship handoffs, and launch response plans. Activate for Show HN, Ask HN, Tell HN, Launch HN, linked articles, or HN comments; choose the right format, preserve author voice, and connect useful discussion to product evaluation."
license: Apache-2.0
compatibility: "Requires web access to Hacker News and linked source material."
domains: content
rules:
  - content(hackernews)
  - match(\bhacker\s+news\b)
  - match(\bshow\s+HN\b)
  - match(\bask\s+HN\b)
  - match(\blaunch\s+HN\b)
  - match(\btell\s+HN\b)
  - match(\bpost\s+(on|to|for)\s+HN\b)
  - match(\by\s*combinator\b)
  - match(\bycombinator\b)
---

## Overview

Prepare an HN publishing brief that makes the author's actual work understandable and worth examining. Use supplied proof and the author's documented voice before platform register; apply platform policy as the publication gate. Keep generic voice guidance in `content-voice`.

HN prohibits generated or AI-edited text in its comments guidelines, and moderator guidance explicitly applies hand-writing to Show HN text (official, HN Guidelines and Show HN Tips, rechecked 2026-09-05). Deliver factual notes and editorial diagnostics for the human to write from independently. Identify a missing fact, unclear referent, or unsupported conclusion without supplying replacement sentences. Don't offer humanization as permission to paste generated prose, or claim an exemption for generated titles.

## Mental model

Treat HN as an opportunity for informed evaluation. Don't forecast placement from points, comment counts, or a historical ranking formula. Distinguish visible attention from qualified interest and paid adoption (directional).

HN describes ranking as points divided by a power of age, with flags, anti-abuse software, overheated-discussion demotion, account or site weighting, and moderator action also affecting placement. The FAQ says higher submitter karma doesn't make posts rank higher (official, HN FAQ, 2026-09). Don't convert these mechanisms into invented constants or a comment-to-point target.

Silence is common: a Show HN corpus had median outcomes of 2 points and 0 comments (measured, Jonno, n=41,301 submissions, 2026-07). Plan around useful feedback and verified evaluation attempts, not a promised front-page result. Open reference/post-types.md when setting success expectations, handling moderation, or preparing Launch HN logistics.

## Format and source rules

| Goal | Format and decision |
|---|---|
| Share an engineering article, including your own blog | Regular link; preserve its original title, with the permitted corrections below (official, HN Guidelines, 2026-09). |
| Let strangers examine something you personally built | Show HN; require non-trivial, tryable work and maker availability. Blog posts, landing pages, waitlists, fundraisers, newsletters, and lists don't qualify (official, Show HN Guidelines, 2026-09). |
| Learn from others' experience | Ask HN; leave the URL field blank (official, HN FAQ, 2026-09). Give the problem, prior attempts, constraints, and the experience sought; omit disguised product research pitches (directional). |
| Share a concise factual notice | Tell HN as an editorial choice, with observed scope and evidence; don't infer a platform word limit (directional). Send questions or notices about HN itself to hn@ycombinator.com (official, HN Guidelines, 2026-09). |
| Recruit | Reply in the current Who Is Hiring? thread, following its instructions; don't submit a standalone job ad (official, HN FAQ, 2026-09). |
| Launch a YC startup through the curated program | Launch HN after approval and an agreed day; use the official instructions in the reference (official, Launch HN Instructions, 2026-09). |

### Titles and links

For linked articles, start from the source headline. Remove the site name and gratuitous number phrases; retain meaningful quantities. Change misleading or linkbait wording accurately, without editorializing. Append [video] or [pdf] for those formats. Don't strip a product name that is the subject merely because it resembles the domain (official, HN Guidelines, 2026-09).

For Show HN or a text submission, have the human author state the artifact or actual question plainly. Prefer a name plus capability or a documented build story (directional). Use the Show HN prefix for eligible work (official, Show HN Guidelines, 2026-09). For Launch HN, keep the complete title within 80 characters (official, Launch HN Instructions, 2026-09). For other submission types, check the current submission form before stating a numeric limit; the Launch HN citation alone does not establish their cap. Don't import an unsupported shorter target.

Submit the original source (official, HN Guidelines, 2026-09). Prefer a canonical destination without tracking clutter or shorteners; use the specific repository file when that file is the story (directional). A paywall with a workaround is allowed; don't automatically substitute an archive for the original source (official, HN FAQ, 2026-09). Search Algolia for the URL, title, and related prior submissions before choosing an angle (directional).

### Body and rendering

Use short prose paragraphs separated by blank lines. HN's comment renderer supports indented code and asterisk-delimited italics; it doesn't render Markdown headings, bold, bullets, or backtick code as Markdown (official, HN Formatting, 2026-09). Keep command lines indented and links as plain URLs. This skill's tables and checklists are planning tools, not pasteable HN formatting.

For Show HN, assemble notes on the maker's real backstory and differentiation, with a clear description and relevant technical detail. Context can go in submission text or, if it doesn't appear there, a first comment; either placement is acceptable (official, Show HN Tips, 2026-09). Inspect the submitted item before adding context again. Don't require a timed first comment or duplicate the pitch.

## Launch and proof posts

Collect the audience and buying situation, promise, available proof with source locations, desired action, destination URL, campaign stage, and disclosure obligations. Stage choices include teaser, launch day, proof, objection, and recap. Record “no CTA” when deliberate. If evidence is missing, return a missing-input list and stop the publishable package; don't manufacture an experience.

Use these qualitative length bands as craft guidance, not platform limits (directional):

| Shape | HN anatomy | Length band |
|---|---|---|
| Launch-day announcement | Eligible Show HN: artifact, real origin, differentiator, try path, limits, commercial terms | Compact opening context; enough prose to evaluate |
| Demo or artifact | Runnable work with an inspectable example; hardware can use a detailed article or video (official, Show HN Guidelines, 2026-09) | Brief orientation beside the artifact |
| Customer outcome or proof | Regular article: baseline and changed result, conditions, source, confounders, unresolved cost | Full explanation at source; minimal HN context |
| Founder decision or build update | Regular technical retrospective; reserve another Show HN for substantial change | Short rationale in-thread; long analysis at source |
| Objection answer | Reply to the actual concern with evidence and a bounded limitation | Direct paragraph; expand for necessary detail |
| Recap or lessons | Resolve questions in the existing thread; submit a separate article only if it independently teaches something | Compact thread update or substantive article |

Apply a strip test to proof articles: with the product name and sales invitation removed, the reader should still learn something useful (directional). Don't require an outcome number when the evidence is qualitative.

Put the artifact or article in the submission URL field. Put relevant evaluation instructions in human-authored context; don't hide the destination in a reply to chase reach (directional). Explain pricing and any required onboarding before readers try the product, as Launch HN advises; apply the same readiness standard to commercial Show HN (official, Launch HN Instructions, 2026-09; directional for the extension).

Disclose the author's affiliation and any sponsorship next to relevant claims. Describe synthetic demo material as synthetic; don't present it as customer evidence (directional). The verified HN text rule supplies no AI-disclosure workaround or media-label scheme (official, HN Guidelines, 2026-09).

Prefer the maker's personal account and add a contact email to the profile for moderator contact or repost invitations (official, Show HN Tips, 2026-09). Make public contact in the about field an intentional privacy choice (directional). Don't invent an account-age or karma prerequisite.

Seed product evaluation through genuine participation. Don't ask friends, employees, customers, or outside communities to submit, vote, or comment on the HN thread; don't arrange booster comments or pose as unaffiliated users (official, HN Guidelines and Show HN Tips, 2026-09). Keep ordinary product sharing separate from HN participation requests. For Launch HN, don't coordinate with press or other launch events (official, Launch HN Instructions, 2026-09).

## Voice on this platform

Read the actual thread before preparing a reply brief. Note the technical depth, unresolved question, and emotional register. Preserve the author's vocabulary and natural contractions. Use precise, restrained prose as the fallback; allow warmth when it belongs to the author. Introduce no typos, fake corrections, lowercase camouflage, or dropped words (directional; Aborn).

Use an affiliation opener when relevant and skip generic flattery (directional). Answer the substantive claim without addressing the commenter by username or cross-examining them (official, Launch HN Instructions and HN Guidelines, 2026-09). Keep real uncertainty and explain the scope of disagreement.

In editorial feedback, point to the actual problem: an unsupported contrast, redundant emphasis, ambiguous claim, or ending that repeats the answer. Don't prescribe sentence-length variation, remove every dash or three-item list, or treat polish as evidence of machine authorship. A real question can belong in a comment when it seeks missing information; avoid questions used to cross-examine or manufacture engagement (directional; HN Guidelines).

When preparing a disagreement brief, identify the strongest plausible reading of the other person's claim, then the evidence or condition that changes the conclusion. Don't speculate about the commenter's motives or whether they read the source. Distinguish a defect report from a personal preference and make the technical consequence clear (official, HN Guidelines, 2026-09; briefing method: directional).

Retain the costs and remaining failures in a build story; don't turn it into a miracle-fix parable (directional; extrapolation from StoryScope fiction research). Use source records to identify the author's actual decision and stakes (directional; Lees). Check provenance instead of treating an AI-detector score as proof; manuscript research doesn't validate detection of HN comments (directional; Editing Study).

## Cadence and engagement

Choose a time when the maker can answer and fix problems. Treat weekday overlap with the intended audience as a timing experiment; no universal best-hour recommendation is established here (directional). Open reference/post-types.md for the measured response curve.

The following T-7 to T+7 schedule is an illustrative planning calendar, not a tested optimum or daily posting quota (directional):

| Stage | Work and post shape | Reply plan and measurement |
|---|---|---|
| T-7 through T-1 | Read prior threads; prepare artifact and source notes. Keep teasers off Show HN. | Test anonymous access, mobile and themes; check instrumentation. |
| T0 | Human-authored Show HN, eligible link, or agreed Launch HN. | Maker present during the first hours; record evaluation questions and reproducible bugs. |
| T+1 | Answer objections in the existing thread; repair broken evaluation paths. | Return with verified fixes; distinguish trial intent from general applause. |
| T+2 | Reduce monitoring as activity falls; keep unresolved replies owned. | Preserve objections and limits in docs; inspect conversion friction. |
| T+3 through T+7 | Close the loop in-thread; develop a useful proof article if justified. | Report what changed and what remains unanswered; don't manufacture another launch. |

Record native points and comments as attention context. Tag substantive evaluation questions, implementation reports, and commercial questions separately as qualified-interest indicators (directional). Follow destination visits through demo attempts, completion, signup, activation, and purchase; a founder case reported demo completion without purchases (measured, DDL to Data, n=single founder launch report, 2026-01). Don't infer revenue from rank.

Keep campaign attribution consistent internally. For links that use campaign parameters, Google defines source, medium, campaign, and content fields (official, Google Analytics URL Builder, 2026-09). Prefer the clean original HN submission URL; preserve available referrer and conversion data without disguising duplicates (directional).

On criticism, identify the valid concern, answer with supplied evidence, and admit unknowns. Return with a fix only after verification. Don't claim a fix earned karma. Flag abuse or contact moderators instead of feeding it (official, HN Guidelines, 2026-09).

## What gets suppressed

HN disallows primary use for promotion and solicitation of votes, comments, or submissions; penalties or bans can affect submissions, accounts, and sites (official, HN Guidelines and HN FAQ, 2026-09). Remove fabricated detection inputs and permanent-ban predictions. Don't treat a rank drop as proof of flags, a domain penalty, or a voting ring.

| After posting | Action |
|---|---|
| Quiet but available | Wait, check the artifact, and collect evidence; silence doesn't diagnose product-market fit (directional). |
| Suspected mistaken removal | Inspect the item and email hn@ycombinator.com with its URL and the specific concern; don't send a boost demand (directional). |
| Second-chance pool or repost invitation | Follow moderator instructions if contacted; don't promise selection or model a recovery deadline (directional). |
| Considering a repost | A small number is acceptable if the story hasn't had significant attention in the last year or so; otherwise duplicates are buried. Don't delete and repost (official, HN FAQ, 2026-09). |
| Substantially different release | Link the earlier Show HN and explain the changes; moderator guidance suggests only once or twice yearly (official, Show HN Tips, 2026-09). |

Deletion exists; don't tell users HN has no delete. Use available controls appropriately and contact moderators for privacy concerns. Don't promise a fixed edit/delete window or deletion after replies from inconclusive evidence (official, HN FAQ, 2026-09).

## Examples

These are illustrative editorial exercises, not real launch results or pasteable posts. Bracketed specifics must be filled from supplied evidence before the human writes independently. Open reference/examples.md when preparing a source-note handoff or reviewing title derivation and objections.

### Developer tool: Show HN

Title brief: required Show HN prefix; artifact is a dependency-change inspector; human chooses the final wording (illustrative).

Private writing beats:
- Identify the dependency report and link its runnable example.
- Explain the author's documented reason for inspecting changes before merge.
- State supported manifests, the unsupported case, and the actual evaluation path from source notes.

Why it works: artifact-first format gives readers something to examine.
The limitation prevents an unsupported security or completeness promise.

### B2B SaaS: proof article

Source headline: “Reconciling invoice imports with duplicate supplier records” (illustrative). Preserve it for the link submission.

Private writing beats:
- Attribute the case to [customer, with permission] and [source record].
- Compare [baseline] with [result] over [measurement window], explaining the same-workload comparison.
- Include [remaining manual work] and the author's vendor affiliation.

Why it works: proof includes conditions and provenance before a commercial claim.
Missing evidence blocks publication; it doesn't invite an invented success story.

### Consumer product: maker demonstration

Title brief: required Show HN prefix; artifact is a knitting-chart editor; distinctive capability is printable row guides (illustrative).

Private writing beats:
- Link the sample chart that strangers can edit and print.
- Explain [author's documented knitting workflow] and [supported notation].
- Describe [unsupported notation] and distinguish free evaluation from paid features.

Why it works: the demonstration has a clear evaluation path.
Pricing and the unsupported notation bound the promise.

### Local service: technical retrospective

Source headline: “Repairing the appointment queue at a bicycle workshop” (illustrative).

Private writing beats:
- Use [workshop records] to explain the scheduling constraint and [decision].
- Report [observed result] alongside [unresolved seasonal constraint].
- Disclose the workshop relationship; omit a booking CTA if the article stands on its own.

Why it works: a service business can share inspectable operational knowledge.
The unresolved constraint keeps the outcome honest and the article useful beyond promotion.

## Checklist

- [ ] Human writes final wording independently; no generated or AI-edited HN text is queued for publication.
- [ ] Hook or first line identifies the actual subject; the package develops a coherent idea.
- [ ] Format fits the goal; link title follows source handling, and any numeric title cap is verified for that submission type.
- [ ] Rendering uses native prose, indented code where needed, and plain URLs.
- [ ] Algolia search checked prior submissions; the repost decision follows the table.
- [ ] Show HN is usable by strangers; pricing and evaluation barriers are explicit.
- [ ] Link and CTA path are intentional, including a deliberate no-CTA choice.
- [ ] Every specific has supplied provenance or is marked only in an illustrative example; missing evidence blocks publication.
- [ ] Affiliation, sponsorship, and synthetic evidence are disclosed as applicable; no unsupported labeling claim remains.
- [ ] Evidence, author voice, and thread context reviewed; useful structure preserved without invented experience or errors.
- [ ] Profile contact choice, maker availability, and follow-up reply ownership are settled; no coordinated participation is planned.
- [ ] Package contains title/source record, destination, private context notes, and reply plan; any linked demo has an asset brief with captions or alternative text where needed.

## References

Official pages are undated unless stated; evidence labels use the validation month.

- [HN Guidelines](https://news.ycombinator.com/newsguidelines.html), [HN FAQ](https://news.ycombinator.com/newsfaq.html), [HN Formatting](https://news.ycombinator.com/formatdoc): checked 2026-09.
- [Show HN Guidelines](https://news.ycombinator.com/showhn.html), [Show HN Tips](https://news.ycombinator.com/item?id=22336638), [Launch HN Instructions](https://news.ycombinator.com/yli.html): checked 2026-09.
- [Algolia search](https://hn.algolia.com/): checked 2026-09.
- [Jonno study](https://jonno.nz/posts/your-show-hn-dies-in-7-hours/): 2026-07; [DDL to Data](https://ddltodata.com/blog/hacker-news-launch-lessons): 2026-01.
- [Google Analytics URL Builder](https://support.google.com/analytics/answer/10917952?hl=en): checked 2026-09.
- [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/): 2026-07; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai): 2026-06; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how): 2026-02.
- [StoryScope](https://arxiv.org/abs/2604.03136), [Lees](https://www.housingwire.com/articles/taste-guts-receipts-ai-writing/), [Editing Study](https://arxiv.org/abs/2608.26710): 2026-08; broader-domain evidence, not HN performance tests.

Re-validate when:
- Guidelines, AI-text policy, submission forms, or rendering change.
- Feed names, moderation guidance, or Launch HN logistics change.
- New reproducible studies replace the response and outcome samples.

Validated: 2026-09
