---
name: social-reddit
title: "Reddit Publishing Playbook"
description: "Draft and revise Reddit posts, comments, AMAs, and product launches in the author's documented voice. Use when preparing content for a subreddit: check community rules, choose a native format, ground claims in supplied proof, disclose affiliations and AI use, and plan useful replies and outcome measurement."
license: Apache-2.0
compatibility: "Requires network access to current Reddit rules and post pages; some research requires an authenticated session."
domains: content
rules:
  - content(reddit)
  - content(subreddit)
  - content(upvote)
  - content(upvotes)
  - content(karma)
  - match(\br/[a-zA-Z0-9_]+)
  - match(\bpost\s+(on|to|for)\s+(reddit|r/))
  - match(\bask\s?me\s?anything\b|\bAMA\b)
---

## Overview

Write a useful contribution for a particular community in a particular person's voice. Apply supplied facts and proof first, the author's documented voice next, and platform register as the fallback; community rules remain a publication gate. Use `content-voice` for general editing and this skill for Reddit decisions.

## Mental model

Separate visibility from permission and qualified interest. Downvotes reduce visibility; moderators enforce community rules alongside sitewide defenses (official, Reddit Safety, 2026-07). Don't use archived Hot or Best formulas, fixed ranking weights, or comment-entry cutoffs to predict distribution.

The Home-feed X experiment hides an item and signals less similar content for a limited global subset (official, Reddit Changelog, 2026-08). Keep each angle relevant; don't treat a personalized Home sample as a community-wide leaderboard (directional).

Treat editorial advice marked (directional) as craft judgment, never a detection bypass or performance promise.

## Community and format decisions

Read the target's current rules, sidebar, pinned threads, and recent comparable posts before drafting. Record rule URLs and access date, allowed format/flair, promotional placement, eligibility, AI restrictions, audience register, and recurring objections. If rules are inaccessible, mark clearance unknown and withhold the publication recommendation.

Use modern community pages and their rules links. Direct community rules JSON was verified for r/rust and r/mcp; it isn't a guaranteed logged-out interface (official, Community Rules, checked 2026-09). Old Reddit requires login during the announced transition; new public API requests are being restricted gradually (official, Reddit Infrastructure, 2026-08).

Promotion isn't inherently spam. Some communities prohibit it; others set their own promotional share guideline (official, Reddit Spam Guidance, 2026-03). Resolve local requirements instead of counting toward a universal quota.

Build a roster by angle, with permission verified separately for every actual subreddit (directional):

| Audience situation | Candidate venue | Contribution and clearance question |
|---|---|---|
| Practitioner evaluating a workflow | Relevant specialist community | Reproducible artifact; check source and promotion rules |
| Buyer comparing alternatives | Existing question in the buyer's niche | Answer the stated constraints; disclose your stake |
| Maker showing a finished object | Relevant showcase community or designated thread | Show the object and a real limitation; check media/flair |
| Local customer planning a job | Relevant city or trade community | Explain local scope; check commercial-post placement |
| Existing users needing support | Product's owned community | Answer unresolved problems and publish useful documentation |

Choose qualitative length bands from the surrounding posts, not a platform-wide word target (directional):

| Community/task | Format | Post length band and anatomy | Comment length band |
|---|---|---|---|
| Expertise or technical discussion | Text; link if the source is the subject | Developed explanation with evidence and conditions | Developed answer if needed to evaluate evidence |
| Showcase or craft | Image/gallery or demo video where enabled | Compact caption explaining the artifact | Brief observation or compact process answer |
| Help or buying question | Text or existing question thread | Compact account of attempts and unresolved constraints | Compact answer; expand for a necessary procedure |
| Experience or local service story | Text with permissioned evidence | Developed account of the decision and consequences | Compact response to the particular experience |
| Casual chat | Text or enabled media reply | Brief observation | Brief conversational reply |
| Existing relevant submission | Repost, formerly crosspost | Short destination-specific context | Match the destination's discussion depth |

Private replies and bios: `reference/examples.md` (directional).

Reposts preserve the original username, community, and score in the preview; destinations must allow reposting (official, Reddit Reposting, 2026-07). No permission follows from the original post's success.

Title decisions (directional):

| Subject | Lead with | Remove |
|---|---|---|
| Result | Supported outcome and the condition that bounds it | Unsupported magnitude or causal certainty |
| Artifact | What readers can inspect | Brand slogan and empty launch excitement |
| Question | Exact unresolved problem | Vague help request or a rhetorical opener that obscures the question |
| Decision | Concrete choice and cost | Forced contrast or tidy life lesson |

Check the actual composer and local title rules. Front-load useful information; don't impose an unsupported character cap. Name the product when relevant and permitted, and identify ownership early in promotional content.

## Launch and proof posts

For campaign work, record audience, buying situation, promise, sourced proof, desired action/destination, stage, disclosures, and author role. Use voice samples when available; missing samples alone don't block a restrained factual draft. Omitting a CTA is a valid deliberate choice. Narrow unsupported claims or mark essential gaps in a nonpublishable working draft; don't invent evidence to fill the brief.

Post shapes and qualitative length bands are craft choices (directional):

| Shape | Native anatomy | Length band |
|---|---|---|
| Launch day | Ownership, buying problem, inspectable result, limitation, permitted action | Compact announcement with supporting context |
| Demo/artifact | Visible task, actual input/output, operating conditions, access path | Brief caption; extend only to explain proof |
| Customer outcome | Permissioned result bounded by the proof checklist in `reference/examples.md` | Developed evidence account |
| Founder decision | Decision, rejected option, actual cost, current uncertainty | Compact operator account |
| Objection answer | Fair statement of objection, evidence relevant to it, unsuitable cases | Brief answer or developed technical explanation |
| Recap | What changed, what failed, unresolved question, source-specific outcomes | Developed retrospective without repeated launch copy |

Apply the strip-test: after removing the product mention, the post should still teach or show something useful. A permitted announcement can identify its product openly; don't disguise a sales pitch as an unrelated question. Keep proof legible, preserve meaningful precision, redact private information, and obtain permission for customer quotes or screenshots (directional).

### Links, identity, and seeding

Put a relevant destination in the root post where permitted. Use the designated promotional thread when required. In comments, link when it directly answers the question and local rules permit; don't hide a prohibited pitch in a reply or profile detour. Prefer a direct inspectable destination (directional). Repetitive promotion and unsolicited mass outreach violate spam policy (official, Reddit Spam, 2026-05).

Disclose ownership, employment, sponsorship, gifted products, or affiliate benefit beside the recommendation as applicable (directional). AI-generated or modified content must follow community rules and carry a tag or other disclosure; presenting generated content as human-generated is prohibited (official, Reddit Manipulated Content, 2026-05). Human review doesn't create an exemption. For automation, verify applicable permissions and requirements, disclose automation, and never conceal it through voice edits (directional).

Use a disclosed founder account for personal decisions and an identifiable brand account for official support (directional). Eligible Reddit Pro organizations can seek verification; individual verification remains an alpha test, and verification doesn't override community rules (official, Reddit Verified Profiles, 2026-07).

Participate where you have relevant contributions. Don't manufacture independent praise, coordinate votes, buy accounts, or seed repetitive employee comments; Reddit's defenses address spam and inauthentic voting (official, Reddit Safety, 2026-07). Employees should disclose their roles and contribute only relevant expertise (directional). Product Hunt's sharing guide recommends existing community participation and prohibits upvote requests or rewards for its launches (official, Product Hunt Sharing, checked 2026-09).

For an owned subreddit, seed useful original discussion and mix in relevant reposts. Contact destination moderators before substantial outbound reposting; don't increase it when it brings no member-growth response (official, Reddit Community Seeding, 2026-05).

### Launch-week rhythm

Illustrative planning offsets, not measured timing optima; skip slots that lack new evidence or local permission. T denotes launch day.

| Offset (illustrative schedule) | Work or post shape | Reply plan | Qualified-interest evidence |
|---|---|---|---|
| T-7 to T-3 | Research buyer questions; prepare demo and permission requests | Resolve scope with moderators when needed | Relevant unanswered questions; community clearance |
| T-2 to T-1 | Rehearse the promise; optional permitted teaser with useful artifact | Assign technical and product/support owners | Specific evaluation requests |
| T | Publish approved launch or demo | Cover the first hours; answer substantive questions and log objections | Relevant replies, requests to try, stated buying constraints |
| T+1 to T+3 | Correct the original; answer objections in context | Follow actual conversations; don't mass-message commenters | Continued evaluation; obstacles resolved or still open |
| T+4 to T+7 | Publish new proof or recap only if warranted | Return with evidence to unresolved questions | Repeat participation; attributed activation where available |

Use Reddit Pro post views, upvote ratio, comments and shares, plus available comment views/replies and account reach/followers. Hourly post views cover the first 48 hours and remain available for 45 days (official, Reddit Pro Performance, 2026-04). Export supported fields; don't assume every visible metric is in CSV. Awards are contextual: Reddit announced expanded free-award availability, so award changes alone don't establish stronger demand (official, Reddit Changelog, 2026-08).

Keep Reddit-native engagement separate from destination visits, activation, retention, and revenue. Record attribution uncertainty (directional). Open `reference/examples.md` when building a launch measurement package, evaluating commerce or paid follow-through, or adapting proof to a new niche.

### AMAs

Arrange moderator pre-approval and the accepted proof method before announcing an AMA. Prepare a proof photo or official identity link when requested; share only necessary identity information. Agree on topic boundaries, flair, start/end time with timezone, and answer ownership. State who is answering and disclose commercial interests (directional).

Answer substantive questions throughout the announced window, including difficult ones; acknowledge unknowns and return with verified answers. Mark the session closed and state any real follow-up commitment. Video comments are available where moderators enable them in eligible public SFW communities and don't autoplay; pair any video answer with useful text (official, Reddit Video Comments, 2026-06; text accompaniment: directional). Check enabled media and upload constraints in the composer; don't invent duration limits.

## Voice on this platform

Keep the author's natural conversational register. Use surrounding comments to calibrate depth and formality, without adopting hostile behavior or slang the author doesn't use. Don't add typos, fake edits, dropped articles, or lowercase camouflage. Open `reference/imperfections.md` when calibrating register, local idiom, or a sensitive reply; it contains register decisions rather than error injection.

Read the parent comment as well as the submission before answering. Identify which person's question, constraint, or evidence the reply addresses; don't attribute a reply's claim to the original poster. If the author lacks firsthand experience, attribute the source instead of inventing an anecdote. Preserve the difference between observed, reported, and inferred results, and qualify the affected claim rather than hedging every sentence (directional).

Default to prose in comments, but keep lists, headings, and copyable code when they make the answer easier to use. A factual list may contain as many items as needed; remove padding rather than a particular count. Don't force a detailed troubleshooting answer into a casual one-liner (directional).

Match the composer: Reddit's Rich Text and Markdown editors are distinct, and their output is not generic GitHub Markdown. Preview quotes, code, links, and line breaks instead of pasting raw markup into the wrong mode. Accompany a screenshot with the relevant error text or explanation; preserve exact code/error strings while editing the surrounding prose (official, Reddit Formatting Guide, 2026-08; text-equivalent practice: directional).

Open `reference/ai-tells.md` during the editorial pass for the scoped pattern checklist and evidence limits. Its purpose is better communication. No punctuation choice or prose cleanup proves authorship or promises avoidance of accusations.

## Cadence and engagement

Choose timing from recent target-community observations and author availability; no universal ET window or weekend exclusion is supported here (directional).

| Thread situation | Response decision (directional) |
|---|---|
| Relevant unanswered problem | Add the missing answer, even in a quiet or older thread |
| Active conversation with room for expertise | Address a specific point; don't echo the leading reply |
| Your product conflicts with the reader's constraints | Say so and recommend a suitable route if known |
| Someone else's showcase or persistent pile-on | Don't hijack it; disengage if you can't contribute constructively |
| Evidence contradicts your earlier advice | Correct the claim openly and state the changed implication |

Reserve time for useful early replies and later follow-up. Admit ignorance when appropriate; when someone acts on advice, help with the next real obstacle. Don't infer a ranking multiplier from reply activity (directional).

For an AI accusation, choose by substance rather than escalation order (directional):

| Trigger | Response |
|---|---|
| Factual error identified | Correct it and provide the source |
| Genuine authorship or automation question | State the actual assistance used and correct missing disclosure |
| Unsupported insult with no question | Leave it unanswered; don't debate detector scores |
| Rule violation or abusive exchange | Stop; resolve the moderation issue without evasive reposting |

Open `reference/imperfections.md` for worked response choices.

## What gets suppressed

Check eligibility messages: communities can gate on account age, total/subreddit karma, verified email, and approved-contributor status; thresholds are hidden. Post Check uses an LLM to flag likely rule violations but doesn't itself block submission (official, Reddit Eligibility, 2026-08).

AutoModerator can enforce configured domain, keyword, pattern, and affiliate-link checks (official, Reddit AutoModerator, 2026-08). Rules Hub uses LLMs to interpret rule intent under moderator control and remains in rollout (official, Reddit Infrastructure, 2026-08). Follow the meaning of rules; don't claim ubiquitous AI-text classifiers or universal phrase penalties.

Repeated mass posting, rapid old-content reposting for karma, and continuously promotional bots are prohibited (official, Reddit Spam, 2026-05). If a post disappears, inspect its state and moderation messages; record the reason as unknown unless explicitly supplied. Don't diagnose removal from a logged-out view or low score alone (directional).

## Examples

These fictional source briefs and drafts illustrate craft, not real testimonials or publishable claims. The stated outcomes belong only to these examples. For actual work, replace them with the author's evidence and add disclosure appropriate to the production process.

### Developer tool: artifact post

Illustrative brief: a maintainer writes terse debugging notes; a saved trace shows a dry-run reporting error. The fix remains untested on remote storage.

> Title: Our dry-run report skipped filenames containing tabs
>
> I maintain the tool. The files were present in the scan, but our report parser dropped those rows. The attached trace shows the point where they disappeared. The patched report includes them on local storage; remote storage is still untested. Reproducer: [source link].

Why it works: ownership is visible and the artifact supports the claim.
The limitation follows the proof rule without inventing a success story.

### B2B SaaS: objection reply

Illustrative brief: an operations founder uses plain, candid replies; their product pilot still required manual weekend refunds.

> Keep your current refund workflow for now. I work on the product you're considering, and our pilot team still entered weekend refunds by hand. Your unattended-weekend requirement rules us out. The current limitation is documented at [source].

Why it works: it answers the buyer's situation without steering into a pitch.
The source and unsuitable case apply the comment decision table.

### Consumer maker: proof caption

Illustrative brief: a bag maker uses tactile descriptions; ride photos show a repaired seam and persistent strap rubbing.

> Title: The bag held at the seam, but the strap still rubs
>
> This is the bag I sew for my shop. You can see the pale scuff beside the buckle in the close-up. The repaired seam held during the loaded ride; the strap rubbing hasn't improved. I'm leaving that photo in the listing so buyers can see where it wears.

Why it works: the caption connects visible wear to the documented use.
The bounded outcome follows the proof rule; no CTA is needed here.

### Local service: experience post

Illustrative brief: a tailor writes practical job notes; the customer approved a pocket repair while leaving worn lining in place and permitted the photos.

> Title: Keeping the worn lining during a pocket repair
>
> I run the alterations shop that did this repair. The pocket is usable again. The customer wanted to keep the lining, so the fraying you can see in the photo is still there; replacing it would be a separate job. Photos shared with permission.

Why it works: affiliation and job scope are explicit.
The remaining issue prevents a misleading before/after promise.

## Checklist

For every draft:

- [ ] The reply addresses the right speaker and current context; quotes, paraphrases, and inferences remain distinguishable.
- [ ] Hook/first line states the subject; the contribution has a single main idea.
- [ ] Current rules, eligibility, format, and flair checked; unknown clearance blocks recommendation.
- [ ] Link and CTA path fit the venue; no CTA is recorded when deliberate.
- [ ] Every specific has supplied provenance or a draft-only placeholder; incomplete drafts aren't publishable.
- [ ] Evidence, voice, and substance reviewed; useful structure preserved; no invented experience or mistakes; required affiliation and AI disclosures included.

For posts:

- [ ] Proof and strip-test checked; package includes title/body, caption, asset brief, accessible image description or alt text where supported, and video transcript/captions as needed.
- [ ] Reply owner and availability recorded; follow-up and measurement plan fit the goal.

For comments:

- [ ] Read the reply chain; answer an unresolved point at suitable depth without hijacking it.

## References

Dates identify supplied source updates; “checked” identifies undated sources reviewed for this edition.

- [Reddit Safety](https://redditinc.com/news/how-were-keeping-reddit-real-and-safe-in-the-ai-era), 2026-07-06.
- [Reddit Changelog](https://support.reddithelp.com/hc/en-us/articles/52393330268436-Changelog-August-12-2026), 2026-08-12.
- [Community Rules: r/rust](https://www.reddit.com/r/rust/about/rules.json), [r/mcp](https://www.reddit.com/r/mcp/about/rules.json), checked 2026-09.
- [Reddit Infrastructure](https://redditinc.com/news/modernizing-reddits-infrastructure-and-moderation-tools), 2026-08-05.
- [Reddit Spam Guidance](https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community), 2026-03-28.
- [Reddit Reposting](https://support.reddithelp.com/hc/en-us/articles/4835584113684-What-is-reposting-fka-crossposting), 2026-07-13.
- [Reddit Spam](https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam), 2026-05-19.
- [Reddit Formatting Guide](https://support.reddithelp.com/hc/en-us/articles/360043033952-Formatting-Guide), 2026-08-06; checked 2026-09-05.
- [Reddit Manipulated Content](https://support.reddithelp.com/hc/en-us/articles/41180423371156-Manipulated-Content-and-Misleading-Behavior), 2026-05-19.
- [Reddit Verified Profiles](https://redditinc.com/news/testing-verified-profiles-on-reddit), 2026-07-09.
- [Product Hunt Sharing](https://www.producthunt.com/launch/sharing-your-launch), checked 2026-09.
- [Reddit Community Seeding](https://support.reddithelp.com/hc/en-us/articles/15484360497812-Planting-seeds-aka-encouraging-and-maintaining-an-active-community), 2026-05-28.
- [Reddit Pro Performance](https://support.reddithelp.com/hc/en-us/articles/47618462633364-Reddit-Pro-Feature-Performance), 2026-04-02.
- [Reddit Video Comments](https://redditinc.com/news/a-new-way-to-connect-on-reddit-video-in-comments-is-now-available-for-users), 2026-06-11.
- [Reddit Eligibility](https://support.reddithelp.com/hc/en-us/articles/33702751586836-Poster-Eligibility-Guide-Post-Check), 2026-08-10.
- [Reddit AutoModerator](https://support.reddithelp.com/hc/en-us/articles/15484574206484-Automoderator), 2026-08-28.

Re-validate when community rules or disclosure policy change; when feed, composer, API, moderation, or analytics features change; or when inspectable performance research appears.

Validated: 2026-09
