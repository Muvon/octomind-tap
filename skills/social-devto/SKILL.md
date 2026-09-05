---
name: social-devto
title: "DEV Community (dev.to) Publishing Playbook"
description: "Write and revise DEV articles, discussions, comments, and launch or proof material in the author's documented voice. Activate for dev.to drafts, publishing packages, series, challenge entries, or company cross-posts; apply current disclosure and promotion rules before preparing copy for publication."
license: Apache-2.0
compatibility: "Markdown editor; network access for DEV policy, editor, and tag checks."
domains: content
rules:
  - match(\bdev\.to\b)
  - match(\bDEV\s+Community\b)
  - match(\bforem\b)
  - match(\bpost\s+(on|to|for)\s+dev\.to\b)
  - match(\bdevto\b)
---

## Overview

Write something a developer can use or answer, in the voice of the person accountable for it. Apply supplied facts and proof first, the author's documented voice next, and platform register as the fallback; respect publication policy throughout. Use `content-voice` for generic editing and the rules here for DEV structure and publishing decisions.

## Mechanics and evidence

- Treat discovery as personalized: follows and reactions interact with semantic similarity, quality, and time decay. Don't promise reach from a tag recipe (official, DEV Feed, 2026-05).
- Use the current reaction vocabulary: Love, Unicorn, Wow, Well Done, and Hot Take (official, DEV Engagement, 2026-09). Don't assign bookmarks a strongest-signal weight or treat reactions as purchase intent.
- Recognize Community Gems as curator endorsements that affect author trust and discovery, including a Curated feed; weighting is evolving (official, DEV Gems, 2026-09). Earn recognition through useful work; don't solicit reciprocal awards (directional).
- Treat public feed-code inspections as models, not production measurements. Comments, follows, language, and age affected the inspected variant; no universal comment multiplier or visibility window follows from it (measured, Loibner, n=single checked-in variant, 2026-07).

Open [reference/publishing-evidence.md](reference/publishing-evidence.md) when checking editor fields, planning an AMA or challenge, choosing a timing experiment, or citing performance. It contains the evidence limits and source register; don't turn its account case studies into targets.

## Format and publishing decisions

Choose by the reader's job. These shapes and qualitative length bands are editorial guidance, not platform post-type guarantees (directional).

| Job | Shape and length band | Required substance |
|---|---|---|
| Reproduce a technique | Article; full walkthrough to reference-length | Working example, setup conditions, explanation, failure boundary |
| Compare real experience | `discuss`; brief context to short argument | State the unresolved decision and your partial answer; ask an answerable question |
| Evaluate a built artifact | `showdev`; compact demonstration to full walkthrough | Show the artifact and how to try it; disclose ownership and limitations |
| Follow a continuing investigation | Series; self-contained article per installment | Recurring problem, new evidence in each entry, useful stopping point |
| Ask about a person's expertise | AMA; brief invitation | Verifiable remit, excluded topics, actual reply availability |
| Enter a challenge | Announcement's required template; sufficient detail for judging | Prompt fit, eligible build, reproducible submission evidence |

Series navigation appears after the second entry (official, DEV Writing, 2026-09). Don't split an explanation merely to multiply posts. A listicle earns its format when entries help readers choose or express the author's specific humor; remove interchangeable filler (directional).

Front-load the technical situation or defensible claim in the title. Open on the problem itself; avoid rhetorical-question openers. A discussion's question belongs after enough context to make it answerable (directional).

### Tags and editor package

Use at most four relevant tags (official, DEV Editor, 2026-09). Treat the following allocation as a selection method, not a distribution formula (directional).

| Candidate | Keep when | Drop or replace when |
|---|---|---|
| Broad topic, such as `programming` or `webdev` | Its current tag description fits the article | Another tag describes the intended reader more precisely |
| Format, such as `discuss` or `showdev` | The draft actually invites discussion or demonstrates a project | The article is a tutorial or opinion without that job |
| Niche, such as `rust`, `postgres`, or `accessibility` | The implementation materially uses that topic | It appears only in passing |
| Language-community tag | Current guidance and recent posts fit the language | You are guessing its purpose or copying another language's tag recipe |

Check each candidate's live page, description, and recent posts. Record visible follower counts with capture dates; mark unavailable counts unknown. Among equally relevant tags, compare current audience size; don't maintain a supposedly permanent biggest-tag list (directional).

Prepare an editor checklist for `title`, `published`, `tags`, `cover_image`, `canonical_url`, `series`, and `description`; inspect the current editor before mapping the package to front matter. Keep publication disabled during review, quote YAML strings when needed, and preview the rendered article. The reference separates verified features from unverified field constraints (directional).

DEV supports Markdown and documented Liquid embeds including GitHub, CodePen, and Twitter (official, DEV Editor, 2026-09). Add language hints to article code fences. Preview every embed; provide a useful text link if rendering fails. Choose a real screenshot when it explains the work, with descriptive alt text and a caption identifying its context. Inspect the actual cover crop; don't promise a click lift (directional).

Cross-post complete useful work with `canonical_url` pointing to the original; DEV supports canonical attribution and RSS imports (official, DEV Writing, 2026-09). Repair relative links and missing assets. Don't describe canonical attribution as guaranteed SEO protection (directional).

## Launch and proof posts

Collect the audience and buying situation, promise, available proof with source, desired action, destination, campaign stage, and disclosure obligations. Include the author's notes and voice samples. Select teaser, launch day, proof, objection, or recap; deliberately choosing no CTA is valid. If source material is missing, return the specific evidence request instead of manufacturing experience (directional).

Apply the policy gate before drafting promotional copy: the currently linked guidelines prohibit AI-assisted or generated articles that promote a business, program, or course (official, DEV AI Guidelines, 2024-04). AI-written launch copy from this workflow isn't cleared for DEV publication. Provide an evidence brief for independent human authorship or nonpromotional education; removing a CTA or selecting a label doesn't erase promotional purpose. Recheck for a superseding policy before publication.

For policy-eligible work, choose the following anatomy and qualitative length band (directional):

| Shape | Anatomy | Length band |
|---|---|---|
| Launch day | Developer problem → artifact in use → design choice → limitation → relevant destination | Compact announcement to walkthrough |
| Demo or artifact | Input → observable output → reproduction instructions → unsupported case | Short demonstration to full tutorial |
| Customer proof | Before/after under comparable conditions → source and permission → confounders → who can reuse it | Focused case study |
| Founder decision | Actual disputed choice → evidence considered → cost accepted → next unresolved test | Short update to technical essay |
| Objection answer | Reader's objection → direct answer → reproducible evidence → remaining limit | Brief answer to worked comparison |
| Recap | Original promise → observed outcome → unresolved issue → useful next artifact | Compact review to reference article |

Use the strip-test: removing the product name and CTA should leave something worth learning. DEV recommends complete educational articles and warns against over-promotion (official, DEV Organization Guide, 2026-09). Bring niche expertise through a familiar developer problem; open the reference for the bounded case evidence behind that choice.

Choose an individual byline for personal work. For company work, credit the real contributor within the Organization, complete their profile, and use canonical attribution for company-blog reposts; DEV recommends human profiles and supports Organization sidebar CTAs (official, DEV Organization Guide, 2026-09). State actual role and subject expertise in the bio; avoid a generic founder pitch (directional).

Put the necessary demo or source link beside the evidence and the conversion CTA in the Organization sidebar or a brief outro. Avoid repeating the same self-link; allow additional owned links only when each supports a distinct claim. Don't hide the destination in a comment to chase an assumed reach benefit. State affiliation beside product claims and sponsorship near the opening; confirm any required placement label in the publishing workflow (directional).

For destination attribution, use consistent `utm_source`, `utm_medium`, and `utm_campaign`; distinguish article and sidebar links with `utm_content` (official, Google URL Builder, 2026-09). Keep attribution separate from claims that DEV caused a sale (directional).

DEV recommends relevant commenting and following, plus Welcome and discussion participation (official, DEV Organization Guide, 2026-09). Participate where you can contribute without pitching. Have collaborators disclose their relationship and add independent substance; exclude vote rings, scripted applause, disguised employees, and unsolicited link drops. These are community-integrity guardrails, not a claimed DEV penalty formula (directional).

Use this illustrative launch-week plan only when the policy gate passes. T offsets are planning labels, not measured optimal days (directional).

| Illustrative offset | Work and reply plan | Observe |
|---|---|---|
| T-7 to T-1 (illustrative plan; directional) | Join relevant discussions; prepare proof and preview; skip empty teasers | Recurring developer questions and useful profile context |
| T0 (illustrative plan; directional) | Publish the native demo; author covers the first hours for setup failures and substantive questions | Views, qualified technical comments, missing instructions |
| T+1 to T+3 (illustrative plan; directional) | Correct the post; answer the strongest objection if new evidence warrants it | Reproduction reports, product-fit questions, source-tagged visits |
| T+4 to T+7 (illustrative plan; directional) | Publish a technical follow-up or bounded recap; continue replies on the original | Returning commenters, follows, Gems, downstream activation |

## Voice on this platform

Use proofread, approachable technical prose as the fallback register. Preserve the author's normal contractions and terminology. First-person claims require their records or testimony. Keep reproducible code exact; never inject typos, fake edits, lowercase camouflage, or dropped articles (directional).

Keep comments short and in prose, consistent with `content-voice`; use inline code when needed and link longer reproductions. Don't default to code blocks or mini-article headings in replies. Answer the specific claim, explain the relevant constraint, and leave room for correction (directional).

Apply the generic voice rules without duplicating a vocabulary blacklist. For DEV tutorials, remove empty Introduction/Conclusion scaffolding, automatic step ladders, equally sized sections, emoji headings, and obligatory “Happy coding” or follow-me endings. Keep prerequisites and numbered procedures when execution actually depends on them (directional).

Scan for repeated contrast pivots, padded triads, staccato stacks, empty dramatic openers, repetitive emphasis words, tidy moral closers, and dense em-dashes. These are editing heuristics from Aborn, Cox, and Gichigi, not authorship tests (directional). Use a dash only when it fits the author's register and helps the sentence; don't add punctuation to satisfy a quota. Strip miracle-fix stories that omit costs, “nobody talks about” framing, rhetorical-question hooks, hashtag stacks, and engagement-bait closers (directional). Keep documented disagreement and unresolved limitations.

## Cadence and engagement

Publish when the intended language community can read and the author can reply. Compare slots in that audience's timezone; don't inherit a US morning default. Use a fluent reviewer for localized examples and idiom (directional).

Single-account observations support testing morning slots, continuing series, and sustainable scheduling, with no universal optimum (measured, Jackson, n=30 posts, 2026-02). The reference preserves scope and separates correlations from recommendations. Open it before setting a length or timing benchmark.

Review results weekly and refresh comparison samples monthly (directional). Record views and substantive comments, distinguish implementation reports from praise, and track relevant follows. Organizations expose views, reactions, and comments; don't assume native CTA analytics (official, DEV Organizations, 2026-09). Observe Gems as quality recognition, not a quota (directional).

Use your own comparable posts' median and spread at matching post ages, separated by format and language. Preserve the sample and collection method. Don't use Top outliers as a minimum success target or claim uncollected reading-list totals (directional).

## What gets suppressed

DEV uses algorithmic detection and Gemini-assisted moderation with promotion, automated-generation patterns, quality, and author context among its inputs (official, DEV Moderation, 2026-01). A polished builder story doesn't exempt spam.

Choose the disclosure matching actual creation: Hand Written (No AI), AI-Assisted (Some AI), or Fully Autonomous. Rough drafting, generated code examples, major copyedits, and translation count as assistance; the announcement offers tier selection without saying every editor save requires it. Synthetic firsthand claims and deceptive low-effort undisclosed generation can lead to suspension (official, DEV AI Disclosure, 2026-08).

The AI Content in Feed setting exists; filtering controls, exact distribution effects, and enforcement are evolving (official, DEV AI Disclosure, 2026-08). Don't promise that disclosure is reach-neutral or conceal assistance to evade preferences. Document generated-media provenance; don't invent a separate DEV media-label rule (directional).

Backlink-building as an article's main purpose can lead to suspension. The guidelines name personal-blog and Organization/company-blog exceptions; these don't override the AI-promotion restriction (official, DEV AI Guidelines, 2024-04).

## Examples

These are illustrative drafting fragments, not reported outcomes or publication-ready promotions. Fill every bracket from supplied evidence and confirm the policy gate before publishing. The tags are candidates to verify (directional).

### Developer tool: demonstration

> Title: Tracing unused imports without deleting dynamic dependencies
>
> I maintain [tool]. Its report marks static imports that it can't trace to an entry point. In [fixture], [observed output] made the candidates easier to inspect, but dynamic imports still needed manual review. The annotated terminal capture shows where that review starts. You can reproduce it with [fixture link]; [unsupported resolver] remains outside the test coverage.

Why it works: the demo anatomy makes the result inspectable without a sales preamble.  
The provenance rule leaves outcome and coverage unclaimed until sourced.

### B2B SaaS: customer proof

> Title: The webhook retries our billing test missed
>
> I work on [service]. With [customer's permission], we compared [before] and [after] on [same workload] over [window]. [Source record] shows the change, including the retries excluded from the headline result. We haven't repeated the comparison under [unmeasured condition], so this result only supports [bounded conclusion]. The reproduction notes are at [source link].

Why it works: the proof anatomy keeps conditions and exclusions beside the result.  
The link rule gives the reader evidence before any conversion request.

### Creator product: series

> Series: Offline notes in a reading app
>
> Opening entry: Choosing what survives a lost connection. I chose [documented approach] because [constraint from notes]. The fixture at [link] reproduces [bounded behavior]; it doesn't cover concurrent edits.
>
> Follow-up entry: Conflicting edits after reconnect. The fixture now shows [new evidence]. I kept [documented merge rule] because [author's reason], accepting [known cost]. The original decision is at [entry link]; concurrent edits remain unresolved.

Why it works: each installment has its own reader job and new evidence.  
The voice rule preserves the author's decision without inventing a transformation.

### Local service: discussion and reply

> Title: Keeping a repair shop's booking page usable by keyboard
>
> I maintain [shop's booking page]. During [documented check], focus moved to [observed location] after a slot became unavailable. [Proposed approach] gives the user a route back, but we haven't checked [assistive setup]. If you've handled this state, where did you put focus, and what did your user test reveal?

> Reply: Your example returns focus to the date field after the slot disappears. I'd check what the page announces at that point; focus alone doesn't show whether the changed availability is clear. I haven't tested your implementation.

Why it works: the discussion question follows a concrete technical situation.  
The reply stays in prose and distinguishes an inspection suggestion from a test result.

## Checklist

- [ ] Hook names the situation; draft develops a focused idea and the chosen format's reader job.
- [ ] Every personal claim and specific has supplied provenance; unresolved example brackets block publication.
- [ ] Author voice matches; AI-tell pass covers body and ending, with no manufactured mistakes.
- [ ] Policy gate passed; AI tier is accurate; affiliation, sponsorship, and media provenance reviewed.
- [ ] Personal versus Organization byline chosen; contributor profile and CTA destination checked.
- [ ] Tags exist and fit; audience-count check dated or marked unavailable; official tag limit respected.
- [ ] Editor fields validated; draft preview checked; canonical, series, code, and embeds render correctly.
- [ ] Cover asset brief, crop review, alt text, and explanatory captions prepared where needed.
- [ ] Self-links justify their placement; CTA or deliberate no-CTA choice and tracking path are explicit.
- [ ] Challenge or AMA requirements checked in the reference when applicable.
- [ ] Author owns follow-up replies; measurement plan includes qualified interest and a comparable baseline.

## References

- [DEV Editor](https://dev.to/p/editor_guide), undated; verified 2026-09.
- [DEV Writing](https://dev.to/help/writing-editing-scheduling) and [DEV Engagement](https://dev.to/help/reacting-commenting-engaging), undated; verified 2026-09.
- [DEV Feed](https://dev.to/devteam/how-were-using-gemini-embeddings-to-build-a-smarter-community-driven-feed-on-dev-1b9f), 2026-05-22.
- [DEV Gems](https://dev.to/devteam/introducing-community-gems-celebrating-human-curation-and-the-best-of-our-community-58c8), 2026-09-02.
- [DEV Organization Guide](https://dev.to/help/organizations/maximizing-your-dev-organization) and [DEV Organizations](https://dev.to/organizations), undated; verified 2026-09.
- [DEV AI Guidelines](https://dev.to/guidelines-for-ai-assisted-articles-on-dev/), 2024-04-08; verified 2026-09.
- [DEV AI Disclosure](https://dev.to/devteam/introducing-ai-disclosure-on-dev-tools-for-nuance-clarity-and-better-feeds-34mk), 2026-08-26.
- [DEV Moderation](https://dev.to/devteam/fighting-spam-at-scale-how-we-use-gemini-to-protect-the-dev-community-277j), 2026-01-22.
- [Google URL Builder](https://support.google.com/analytics/answer/10917952?hl=en), undated; verified 2026-09.
- [Jackson: account experiment](https://dev.to/leejackson/i-built-a-content-calendar-that-runs-itself-heres-what-30-days-of-data-taught-me-2oac), 2026-02-16; [Loibner: feed-model inspection](https://dev.to/davidloibner/six-articles-200-views-so-i-read-the-feeds-source-code-4ek8), 2026-07-29.
- [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/), 2026-07-10; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), revised 2026-06; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how), 2026-02-18: practitioner editing heuristics.
- [Evidence register and additional formats](reference/publishing-evidence.md): dated Jackson, Loibner, and other case sources; Aborn, Cox, and Gichigi editing references.

Re-validate when: editor or feed features rename; AI or challenge policy updates; feed-model commits land; new account measurements or vendor reports are used.

Validated: 2026-09
