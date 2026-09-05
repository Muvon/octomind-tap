---
name: social-linkedin
title: "LinkedIn Publishing Playbook"
description: "Write and revise LinkedIn posts, launch copy, comments, and supporting profile or long-form copy in the author's documented voice. Activate for LinkedIn drafting, with evidence-led format selection, customer-proof handling, and a complete publishing package."
license: Apache-2.0
compatibility: "Browser and network access for source checks and LinkedIn previews."
domains: content
rules:
  - content(linkedin)
  - match(\blinkedin\s+(post|comment|article|newsletter|launch|profile)\b)
  - match(\bpost\s+(on|to|for)\s+linkedin\b)
  - match(\bprofessional\s+post\b)
  - match(\bcareer\s+post\b)
---

## Overview

Write LinkedIn content that expresses the author's actual judgment and helps a specific reader act. Apply supplied facts and proof first, then documented author voice, then platform conventions. Use `content-voice` for generic editing. Prepare copy and a publishing handoff; posting, scheduling, and outreach require a request for those actions.

## Mental model

LinkedIn uses profile information and interaction history in retrieval and ranking; it publishes no universal comment multiplier or single dominant signal (official, LinkedIn Feed Engineering, 2026-03). Write for a reader's professional problem, rather than an imagined scoring formula (directional).

Keep evidence labels with advice. Official labels identify documented features or policy; measured labels identify observational cohorts, not causal promises. Directional labels identify craft judgment. Keep sample scope and limitations when quoting a benchmark. Never combine vendor engagement rates into a universal target.

Open `reference/mechanics.md` when selecting formats from benchmarks, checking feature availability, or explaining ranking and disclosure. Open `reference/launch.md` when preparing customer proof, a joint launch, paid-support copy, or attribution handoff.

## Format and anatomy rules

Standard posts allow 3,000 characters; Articles are a separate long-form feature (official, LinkedIn Post Help, 2026-08). Count the finished post including its link and disclosure. Use the shortest complete explanation (directional). AuthoredUp observed strong engagement medians at 1,301–2,500 characters (measured, AuthoredUp Length, n=372,126 personal-profile posts, 2026-08); Flypost found no measurable text-only length effect in its matched subset (measured, Flypost, n=121 paired creators, 2026-07).

Put the concrete subject and stake in the opening. Follow with the evidence and its conditions; end with an appropriate next action or stop. Use paragraph breaks where the thought changes, without a staircase of isolated sentences (directional). Preview the actual mobile opening; treat published mobile/desktop fold estimates as approximate interface observations, not a guaranteed character budget (directional; AuthoredUp Length, 2026-08). Don't place a fictional fold marker after a fixed line.

| Reader need / available asset | Format and execution |
|---|---|
| Understand a decision or lived experience | Text post: show the supplied decision or experience and what informed it; retain relevant costs or unresolved questions when supported (directional). |
| Follow a procedure or inspect a mini-report | Native PDF document: make the cover promise specific, give each slide a substantive job, and finish with the usable takeaway. Choose slide count from the material (directional). |
| Inspect physical evidence or compare states | Image or multi-image post: label context and comparison conditions; make each image legible on a phone. Test portrait framing without cropping proof (directional). |
| See behavior or hear an explanation | Native captioned video: start with the task/result, show the operation, retain failure boundaries. Let necessary demonstration determine duration (directional). |
| Evaluate a launch | Announcement with a demonstration or artifact. Apply the strip-test below (directional). |
| Read a durable argument | Article: give it a specific title, sourced sections, and a feed introduction that delivers a useful finding (directional). |
| Return to a recurring subject | Newsletter brief: define the recurring reader promise and issue scope; confirm account availability before packaging it. Don't promise notification delivery or growth (directional). |
| Participate in a demonstration or discussion | Live: schedule an Event before broadcasting (official, LinkedIn Live Help, 2026-06). For audio-only requests, confirm the current event options before promising standalone Audio Events (directional). |
| Help decide between real alternatives | Poll: use meaningful options and explain who the answer applies to. Treat votes as self-selected input (directional). |
| Discuss someone else's work | Repost with commentary: name the original contribution, add a supported implication or disagreement, and credit the source. Avoid an empty reshare (directional). |

Metricool observed stronger results for some document and multi-image formats than for video in its cohort (measured, Metricool, n=673,658 posts, 2026-04); AuthoredUp observed stronger document than video results in its personal-profile cohort (measured, AuthoredUp Formats, n=3M+ personal-profile posts, 2026-09). Include documents and multi-image posts among relevant format tests; do not infer a universal video advantage from these cohorts (directional). Don't discard polls: Socialinsider reports 4.50% engagement for its Q2 table, but its collection dates conflict with that table's period (measured, Socialinsider, n=1.3M business posts, 2026-03; see reference caveat).

Package image descriptions and alt text wherever supported. LinkedIn may supply automatic alt text, with no assignment alert on mobile; review each image's description rather than assuming missing warnings mean it is ready (official, LinkedIn Alt Text Help, reviewed 2026-09-05). For documents, include accessible text and a text summary if the uploader lacks per-slide descriptions. Supply corrected captions, an asset brief, and source permissions (directional).

## Launch and proof posts

For launch or proof planning, record the audience, buying situation, promise, available proof, desired action/destination, campaign stage, disclosures, and reply owner. Use author voice samples when available; their absence does not block a restrained, fact-bounded draft or routine edit. No CTA is valid. If essential proof is missing, narrow or withhold that claim while continuing supported work.

Use problem framing before announcement and follow with deeper evaluation material. This follows LinkedIn's ramp, launch, and nurture guidance (official, LinkedIn Launch Guide, 2026-05). Bundle minor changes when they don't justify a distinct buyer story (directional; Oakley, 2026-03).

Use the observed AuthoredUp depth band above as an optional starting range for developed feed posts, without padding. Use shorter captions when the asset supplies the explanation; use an Article when the argument exceeds the post constraint. These shape choices are craft judgment (directional).

| Shape | Anatomy | Length band |
|---|---|---|
| Launch day | Buyer task → available change → visible proof → eligibility/limitation → action | Short caption with proof asset; developed feed post otherwise |
| Demo or artifact | Show task → demonstrate operation → state test conditions → offer access | Short caption; explanation in asset |
| Customer outcome | Prior state → intervention → observed outcome with timeframe/denominator → confounders → source | Developed feed post |
| Founder decision / build update | Actual choice and evidence; include a rejected alternative, cost, or next test only when supported and relevant | Short or developed feed post |
| Objection answer | Specific buyer concern → evidence → cases where concern still applies → next step | Developed feed post |
| Recap / lessons | Expected outcome → observed result → attribution limits → changed plan | Developed feed post; Article for detailed analysis |

For announcement and proof posts, remove the product name temporarily: the remaining post should still show something useful. If it doesn't, add the artifact or explain the decision. A factual availability notice may remain short when availability itself serves the audience; don't invent a lesson (directional).

Use a root-post link when the reader needs immediate access. If testing a first-comment link, prepare a descriptive resource sentence and publish it immediately with the post; state where it is and check visibility. This is publishing discipline, with no proven ranking protection (directional). Link effects differed by account type: profile link posts had fewer impressions, Page link posts more (measured, Metricool, n=673,658 posts, 2026-04). Test qualified visits, not reach alone.

Disclose material relationships and obtain consent for customer/partner attribution and reuse (directional). Content shared for money, free products/services, or other value requires LinkedIn's Brand Partnership label; its toggle works only on Public posts and resets Off for each new post. Don't bypass it through audience settings (official, Brand Partnership Help, reviewed 2026-09-05). LinkedIn recommends disclosing heavy AI reliance when non-obvious; this isn't a blanket AI-assistance labeling mandate (official, AI Help, reviewed 2026-09-05). Preserve C2PA Content Credentials; a missing provenance icon doesn't establish human origin (official, Credentials Help, reviewed 2026-09).

Use genuine Collaborative Posts for joint work; members and Pages can invite up to five collaborators (official, LinkedIn Collaborative Posts, 2026-07). Give voluntary employee contributors their own experience angle. Don't organize reciprocal engagement rings, copy-paste praise, automated replies, or concealed endorsements (directional application of LinkedIn Authenticity, 2026-06). Open the launch reference for destination-specific voting rules and paid permissions.

Prefer a founder or expert for personal decisions and discussion; keep the Page useful for verified product facts, shareable proof, and buyer evaluation (directional). Similar impressions per post, but higher profile engagement, were observed in Metricool's sample; a universal Page reach discount isn't supported (measured, Metricool, n=673,658 posts, 2026-04).

Illustrative launch-week schedule, not a measured timing prescription; offsets below are planning examples. Choose posts only when new substance exists.

| Illustrative day | Shape | Reply plan during first hours | Measure |
|---|---|---|---|
| T−7 (illustrative) | Buyer problem or founder decision | Author handles context questions | Relevant objections and reader roles |
| T−3 (illustrative) | Artifact preview | Expert answers feasibility questions | Requests to inspect or try |
| T0 (illustrative) | Launch demonstration | Staff product answers; check promised link immediately | Qualified comments and outbound clicks |
| T+2 (illustrative) | Proof or objection answer | Return to unresolved questions | Evaluation requests and consenting DM conversations |
| T+7 (illustrative) | Bounded recap | Answer late replies; acknowledge missing evidence | Qualified visits and attributed next actions |

Review native clicks and media consumption where exposed alongside public reactions; public counts omit useful activity (measured, Metricool Press, n=673,658 posts, 2026-04). Keep inquiries separate from verified signups or opportunities. Supply consistent campaign tags and distinguish creative/link placement with `utm_content` (official, Google URL Builder, 2026-09 review, undated). Attribution implementation and publishing are downstream steps.

## Voice on this platform

Read supplied LinkedIn samples for formality and how the author explains a decision. Preserve that register; fall back to direct professional prose. Keep natural contractions and fragments without adding errors. Don't inject dropped articles, lowercase camouflage, fake edits, or typos to simulate humanity (directional; Aborn, 2026-07).

| Surface | Register choice |
|---|---|
| Feed post | State the actual subject before institutional excitement. Retain the author's specific judgment and bounded uncertainty (directional). |
| Professional comment | Read the thread; address its claim with evidence or a useful clarification. Don't invent a matching workplace anecdote (directional). |
| Personal announcement reply | A sincere acknowledgment is enough. Don't turn another person's news into a pitch or forced question (directional). |
| Document / Article | Use structure for navigation; proofread labels and preserve technical precision (directional). |
| Profile headline / About | Name the work and whom it helps. Support credentials with evidence; make the next step clear. Avoid an invented founder persona (directional). |
| Connection note / DM / InMail | Refer to an observed buyer problem or actual conversation. Explain relevance and ask permission before sending a resource; don't treat a reaction as purchase intent (directional; Venetz, 2026-07). |

Review voice and substance, not supposed proof of authorship. Remove filler, repetitive suspense, unsupported “nobody talks about” claims, and generic conclusions. Keep meaningful contrasts, useful lists, ordinary questions, and summaries when they serve the professional reader; don't turn an editing heuristic into a word or punctuation ban (directional; Aborn, 2026-07; Cox, 2026-06; Gichigi, 2026-02). Preserve necessary uncertainty and actual tradeoffs (directional inference from StoryScope, 2026-08).

Retain useful punctuation in the author's register; avoid dense em-dashes without imposing an artificial quota (directional; Cox, 2026-06). Add no errors. Use genuine records for personal stakes; request missing detail or remove the claim (directional; Lees, 2026-08). Open the mechanics reference for localization and detector limitations.

## Cadence and engagement

Choose sustainable frequency around available proof and reply capacity. Don't impose a daily maximum: Buffer's LinkedIn frequency analysis found gains at higher cadence (measured, Buffer Timing, n=2M posts, 2026-07). This doesn't justify repeated launch copy.

Test audience-local afternoons/evenings against account history: Buffer found a 3–8 PM window, with Wednesday 4 PM and Friday 3–4 PM strongest (measured, Buffer Timing, n=4.8M+ posts, 2026-07). For global audiences, rotate tests across named audience timezones and compare like-for-like posts. Don't schedule solely from the author's timezone (directional).

Assign an author or informed reply owner, cover the first hours, revisit later questions, and plan handoff beyond office hours (directional). Replying correlated with about 30% higher engagement (measured, Buffer Replies, n=72,000 LinkedIn posts, 2025-12). Half of impressions arrived within 48 hours in another cohort; that isn't a feed expiry or reply deadline (measured, Metricool, n=673,658 posts, 2026-04).

Answer the question and add what is missing. Use a specific answerable prompt only when its answers will matter. Don't attach a question to every post (directional). Direct questions correlated with more comments (measured, Metricool, n=673,658 posts, 2026-04). Moderate spam and fraud links while preserving reasoned criticism (directional).

Omit hashtags unless they clarify a topic or campaign; if useful, place them unobtrusively after the copy. Mention people only for a relevant contribution and with consent where appropriate. Promise no discovery boost or hashtag-feed access (directional).

## What gets suppressed

LinkedIn reduces wider distribution of apparently AI-generated content without perspective and acts on scaled automated comments or replies that merely restate a post (official, LinkedIn Authenticity, 2026-06). No cited policy establishes word-specific suppression or fabricated-story detection.

LinkedIn explicitly targets “comment to agree” bait, repetitive low-substance posts, and videos unrelated to their accompanying text (official, Feed Update, 2026-03). A specific question with a useful answer is different from a demand for comments. Add the author's supported perspective; cosmetic rewording of an empty post does not address the published concern (directional).

Treat a “Seems like AI slop” analytics tip as a revision cue, not a takedown or policy decision (official, AI Help, reviewed 2026-09-05). Diagnose weak substance before cosmetic edits. Don't describe legitimate stories, announcements, or promotional links as automatically prohibited (directional).

## Examples

These are fictional teaching scenarios with bounded outcomes, not customer evidence. Bracketed fields are provenance placeholders; affected drafts aren't publishable until filled and verified. Package notes stay outside the post.

### Developer tool: demo caption

> The migration preview flags an index rebuild before you apply the schema change.
>
> I'm showing it against a disposable database in this recording. It catches the rebuild in this example; it doesn't estimate the lock time on your production workload. The runnable example and setup notes are at [demo URL].

Package: native screen recording, corrected captions, readable command output.

Why it works: the demo shape gives the buyer an inspectable task.
It follows the provenance rule and names what the demonstration cannot establish.

### B2B SaaS: customer proof

> The review queue got shorter after [customer] changed how disputed invoices were assigned.
>
> In [source period], the median wait moved from [before] to [after] for [eligible invoices]. They also changed staffing, so we can't isolate our routing feature's contribution. [Approved case-study URL] includes the measurement method and the cases excluded.

Package: approved comparison image, alt text with conditions; disclose the supplier relationship.

Why it works: the customer-outcome shape retains denominator and confounder.
Every missing specific is marked; the copy avoids a miracle-fix claim.

### Consumer product maker: design decision

Illustrative source brief: the maker's test notes report corner wear before the pages were used up; the maker chose a replaceable cover despite extra hinge bulk, documented in a side-view photo.

> I kept the notebook cover replaceable after the pocket test.
>
> The corners wore before the pages were used up. A replaceable cover adds bulk at the hinge, which you can see in the side-view photo. I'm keeping that tradeoff in this version; it won't suit someone who wants the thinnest notebook.

Package: multi-image wear detail and side view, descriptive alt text. No CTA.

Why it works: register matching preserves a maker's direct explanation.
The decision has a visible cost and makes no durability promise beyond the test.

### Local services: availability notice

Weak, illustrative: “Delighted to announce our amazing new service.”

> We're opening evening repair appointments for people who can't leave a bike during work.
>
> The booking page lists jobs we can finish during the appointment. If inspection finds damage that needs parts, we'll agree a return visit before starting that work. Availability and the inspection fee are at [booking URL].

Package: booking link in the root post; staffed replies about eligible repairs.

Why it works: the launch shape makes availability useful without a fabricated lesson.
The service boundary replaces generic excitement and avoids promising every repair immediately.

## Checklist

- [ ] Opening names the subject and stake; preview the real mobile fold.
- [ ] Keep a single main idea; choose the format for its evidence and check current constraints.
- [ ] Every specific is supplied or placeholder-marked; verify cited numbers, denominators, dates, and sources. Unfilled drafts aren't publishable.
- [ ] Preserve documented author voice and useful structure; review substance without manufactured mistakes or style quotas.
- [ ] Choose CTA or deliberate no-CTA; verify destination, campaign tags, and first-comment timing if used.
- [ ] Check customer/partner consent, relevant mentions, and restrained hashtags.
- [ ] Review affiliation, the current post's required Brand Partnership toggle, recommended heavy-AI disclosure, and Content Credentials.
- [ ] Supply asset brief, readable assets, alt text/accessibility fallback, corrected captions, and source rights.
- [ ] Assign reply and moderation coverage in audience timezones; include late follow-up and qualified-interest measures.

## References

- [Feed Update](https://news.linkedin.com/2026/ImprovingTheFeed), 2026-03-12; [Alt Text Help](https://www.linkedin.com/help/linkedin/answer/a519856/adding-alternative-text-to-images-for-accessibility?lang=en), reviewed 2026-09-05.
- [Brand Partnership Help](https://www.linkedin.com/help/linkedin/answer/a1627083) and [AI Help](https://www.linkedin.com/help/linkedin/answer/a1481496), reviewed 2026-09-05.

Dates identify publication/update unless marked review. Detailed sources and cohort caveats: [mechanics](reference/mechanics.md) and [launch execution](reference/launch.md).

- [LinkedIn Feed Engineering](https://www.linkedin.com/blog/engineering/feed/engineering-the-next-generation-of-linkedins-feed), 2026-03-12; [Post Help](https://www.linkedin.com/help/linkedin/answer/a528176), 2026-08.
- [LinkedIn Authenticity](https://news.linkedin.com/2026/keeping-conversations-real-on-linkedin), 2026-06-04; [AI Help](https://www.linkedin.com/help/linkedin/answer/a1481496/best-practices-for-content-created-with-the-help-of-ai?lang=en), 2026-08; [Credentials Help](https://www.linkedin.com/help/linkedin/answer/a6282984?lang=en), undated, reviewed 2026-09.
- [LinkedIn Live Help](https://www.linkedin.com/help/linkedin/answer/a7460595), 2026-06-22; [Collaborative Posts](https://news.linkedin.com/2026/introducing-collaborative-posts-now-available-to-members-and-company-pages-on-linkedin), 2026-07-23; [Launch Guide](https://www.linkedin.com/business/marketing/blog/linkedin-ads/how-to-launch-a-product-on-linkedin), 2026-05-26.
- [Metricool](https://metricool.com/linkedin-trends/), 2026-04-16; [Metricool Press](https://metricool.com/press-release-linkedin-study-2026/), 2026-04-14; [Socialinsider](https://www.socialinsider.io/social-media-benchmarks/linkedin), 2026-03-16.
- [AuthoredUp Formats](https://authoredup.com/blog/best-performing-content-on-linkedin), 2026-09-02; [AuthoredUp Length](https://authoredup.com/blog/linkedin-character-limit), 2026-08-11; [Flypost](https://www.flypost.io/learn/linkedin-post-length), 2026-07-24.
- [Buffer Timing](https://buffer.com/resources/best-time-to-post-on-linkedin/), 2026-07-22; [Buffer Replies](https://buffer.com/resources/linkedin-engagement-data/), 2025-12-04.
- [Aborn](https://emilyaborn.com/ai-writing-tells-what-they-cost-you/), 2026-07-10; [Cox](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), 2026-06; [Gichigi](https://tahigichigi.substack.com/p/12-red-flags-of-ai-writing-and-how), 2026-02-18; [Lees](https://www.housingwire.com/articles/taste-guts-receipts-ai-writing/), 2026-08-07; [StoryScope](https://arxiv.org/abs/2604.03136), 2026-08-10 revision.
- [Oakley](https://dreamdata.io/blog/b2b-product-launches-should-be-campaigns-not-single-events), 2026-03-13; [Venetz](https://dreamdata.io/blog/leslie-venetz-why-your-b2b-outbound-is-killing-your-brand), 2026-07-03; [Google URL Builder](https://support.google.com/analytics/answer/10917952?hl=en), undated, reviewed 2026-09.

Re-validate when feature names or composer controls change; disclosure/policy pages update; feed engineering changes; new vendor reports revise cohorts or findings.
Validated: 2026-09
