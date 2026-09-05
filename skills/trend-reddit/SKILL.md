---
name: trend-reddit
title: "Reddit Trend Harvester Playbook"
description: "Harvest Reddit conversations and community-specific opportunities with cited posts, current rule checks, and explicit coverage limits. Activate when researching Reddit trends, scanning subreddits, or preparing a Reddit evidence brief; return observed patterns and qualified angles for downstream drafting."
license: Apache-2.0
compatibility: "Requires Octoweb browser and network access; some Reddit surfaces require an authenticated session."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(reddit)
  - session(trend) content(subreddit)
  - match(\breddit\s+(trend|trends|harvest|brief|post)\b)
  - match(\b(harvest|scan|analyze)\s+reddit\b)
  - match(\br/[a-zA-Z0-9_]+\b)
---

## Overview

Return a source-backed brief for each target subreddit. Harvest the questions and evidence that matter to the supplied audience, verify community permission for proposed angles, and distinguish observations from editorial hypotheses. Drafting and publishing are downstream steps.

## Mental model

Separate the sampled surface, community permission, and buyer intent. Downvotes reduce visibility; moderators enforce community rules alongside sitewide defenses (official, Reddit Safety, 2026-07). Don't infer current Hot or Best formulas, fixed ranking weights, or comment-entry cutoffs from archived code or displayed scores.

The Home-feed X experiment hides an item and signals less similar content for a limited global subset (official, Reddit Changelog, 2026-08). Record Home as a personalized sample; don't combine it with community-sort observations as if they share a population (directional).

## Harvest procedure

### Establish scope and access

Record the audience and buying situation, target language/geography, research period, product category, supplied proof, and requested campaign stage. Discover communities from actual buyer-language queries before assuming that large builder communities contain buyers (directional).

If available, use Reddit Pro Trends for keyword conversations and community discovery. Its coverage is public SFW English content; private, banned, quarantined, NSFW, deleted, and messaging content are excluded (official, Reddit Pro Trends, 2026-05). Inspect original posts behind theme summaries. State the coverage limits in the brief.

Use modern `www.reddit.com` pages. Old Reddit requires login during the announced transition; new public API requests are being restricted gradually (official, Reddit Infrastructure, 2026-08). Use authorized authentication when available. Before automated collection, establish that the collection method and intended use are authorized. Don't treat a working login or publicly rendered page as evidence of scraping permission. If permission is unknown, use supplied records or an authorized research surface and report the coverage gap (directional). If blocked, record the blocked URL and missing evidence; don't bypass the gate or call the community inactive.

### Inspect surfaces

Use the following existing URL forms as navigation probes, not guarantees of current availability or sort behavior (directional). Substitute the actual subreddit name and URL-encode search terms; these are URL templates rather than draft placeholders. Verify the rendered sort and date filter after navigation, and retain the actual final URL.

| Purpose | Navigation probe | Capture |
|---|---|---|
| Current community sample | `https://www.reddit.com/r/{sub}/hot/` | Visible posts and the sort actually selected |
| Additional discovery sample | `https://www.reddit.com/r/{sub}/rising/` | Use only if the requested surface renders; don't assume it proves acceleration |
| Recent highly scored sample | `https://www.reddit.com/r/{sub}/top/?t=day` | Selected time filter and observed content |
| Broader comparison sample | `https://www.reddit.com/r/{sub}/top/?t=week` | Recurring subjects and counterexamples |
| Submission/saturation sample | `https://www.reddit.com/r/{sub}/new/` | Repeated angles, unanswered questions, and quiet posts |
| Community permission | `https://www.reddit.com/r/{sub}/about/rules/` | Full rules, linked wiki/sidebar, pinned threads |
| Topic discovery | `https://www.reddit.com/search/?q={encoded-topic}&t=week` | Actual query, time filter, and returned communities |
| Broad comparison only | `https://www.reddit.com/r/all/top/?t=day` | Label separately from niche demand |

If a probe redirects or isn't available, navigate from the community page using the visible controls. Mark unavailable surfaces explicitly; don't relabel a fallback as Rising or claim chronological order without checking. Inspect selected posts and their reply chains rather than stopping at cards. Scroll incrementally if content hasn't rendered (directional).

Direct rules JSON was verified for r/rust and r/mcp; it isn't a guaranteed logged-out interface (official, Community Rules, checked 2026-09). Use `https://www.reddit.com/r/{sub}/about/rules.json` only when accessible. If it fails, use current rendered rules; if those also fail, mark clearance unknown.

Where Reddit's limited US shopping experiment surfaces product summaries or source discussions, follow through to the original contribution. Pricing and buy links depend on a participating business catalog (official, Reddit Shopping, 2026-02; expansion checked 2026-09). Don't invent a universal Reddit Answers or shopping harvest endpoint.

### Check rules before recommending

Record rule URLs, access date, and the exact clause relevant to the proposed angle. Check permitted formats, title restrictions, required flair, promotional placement, AI policy, repost permission, and any stated eligibility.

Promotion isn't inherently spam; communities decide their own promotional restrictions (official, Reddit Spam Guidance, 2026-03). Don't apply a universal promotional quota or infer approval from another post remaining visible.

Poster Eligibility can check account age, total/subreddit karma, verified email, and approved-contributor status while hiding thresholds. Post Check flags likely rule violations with an LLM but doesn't itself block submission (official, Reddit Eligibility, 2026-08). Report the actual message; don't guess eligibility from a public karma count.

AI-generated or modified content must follow community rules and carry a tag or other disclosure; presenting generated content as human-generated is prohibited (official, Reddit Manipulated Content, 2026-05). Record stricter local rules as publication constraints.

| Verified rule example | Scope to preserve |
|---|---|
| r/rust | Prohibits slop regardless of origin and allows discretionary removal of apparently AI-generated submissions (official, r/rust Rules, checked 2026-09) |
| r/mcp | Allows disclosed self-promotion with Showcase for your work; fake unaffiliated promotion and AI-generated promotional slop can result in bans (official, r/mcp Rules, checked 2026-09) |

Re-check both examples at research time. Build every other culture/permission row from current evidence; don't maintain subscriber-count stereotypes or assume flair conventions from memory.

### Collect and interpret evidence

For every cited contribution, record the permalink, verbatim title or relevant short excerpt, community, observed format/flair, publication time, collection time, selected sort, displayed score, comment count, and upvote ratio if shown. Record author participation, relevant reply excerpts, disclosed affiliation, and visible moderation notices. Mark unavailable metrics unknown (directional).

Use Reddit Pro Performance where authorized for post views, upvote ratio, comments, shares, and available comment/account metrics. Hourly post views cover the first 48 hours and remain available for 45 days; export only fields actually supported by CSV (official, Reddit Pro Performance, 2026-04).

Capture awards as context, not a stable demand benchmark: Reddit announced expanded free-award availability (official, Reddit Changelog, 2026-08).

| Observation | Interpretation rule (directional) |
|---|---|
| Displayed score and comment count | Describe the snapshot; don't call score raw upvotes |
| Score or comments divided by age | Lifetime average only; don't present it as current velocity |
| Repeated observations | Report change over the observed interval with collection times |
| Many comments | Read them to distinguish evaluation, argument, and unrelated attention |
| Repeated angle in New | Compare actual replies and unresolved gaps before calling saturation |
| Removed/deleted marker | Preserve the visible state; cause stays unknown without an explicit notice |
| Apparently successful launch | Separate engagement from reported activation or purchase |

For a requested campaign stage, collect evidence for downstream drafting; these are harvest judgments (directional):

| Stage/evidence | Capture for the brief |
|---|---|
| Before launch | Current buyer questions, rule clause for the proposed angle, and missing proof |
| Launch/demo | Inspectable artifact, operating conditions, disclosed affiliation, and substantive evaluation questions |
| Customer proof/recap | Permissioned source, metric definition and unit, actual sample and rate denominator, measurement window, comparable baseline for change claims, confounders, and unresolved objections; keep qualitative evidence qualitative |

AutoModerator supports configured domain, keyword, pattern, and affiliate-link checks (official, Reddit AutoModerator, 2026-08). Rules Hub uses LLMs to interpret rule intent under moderator control and remains in rollout (official, Reddit Infrastructure, 2026-08). Don't identify a hidden classifier or infer a phrase penalty from a removal.

### Build the opportunity brief

Use a per-community decision table. Assign qualitative priorities as analyst judgment; don't calculate universal virality scores (directional).

| Field | Required output |
|---|---|
| Audience/angle | Buyer situation and proposed contribution |
| Permission | Allowed, prohibited, or unknown; rule clause and URL |
| Observed register | Current evidence for length/depth and format, with example links |
| Proof gap | Unanswered question the supplied artifact could address |
| Fit | Direct, adjacent, or weak, with reasoning |
| Saturation | Repetition and counterexamples in the sampled period |
| Follow-up | Likely substantive questions and expertise needed to answer |
| Evidence limits | Missing surfaces, access restrictions, and selection bias |

If reporting a format mix or any new count, attach an inline measured label naming the current harvest, its actual sample size, and collection month. Include the sample definition and collection period. Without comparable evidence, use a qualitative hypothesis marked (directional).

Choose timing from recent target-community observations and author availability; no universal ET window or weekend exclusion is supported here (directional). Include timezones and quiet posts when studying timing. A winners-only sample can't establish the effect of publishing time (directional).

Reposts, formerly crossposts, preserve the original username, community, and score; destinations must permit reposting (official, Reddit Reposting, 2026-07). For substantial outbound community promotion, Reddit recommends contacting moderators and avoiding escalation when reposting doesn't bring member growth (official, Reddit Community Seeding, 2026-05). Recommend no fixed small-to-large order or safe daily volume.

Don't seed activity while harvesting. Repetitive mass promotion, unsolicited mass outreach, rapid old-content reposting for karma, and continuously promotional bots violate spam policy (official, Reddit Spam, 2026-05). Close research tabs when the brief is complete.

## Examples

### Permission remains unknown

Illustrative brief excerpt:

> The demo appears relevant to the workflow questions in [post URLs]. The rules page is blocked in the available session, so publication clearance is unknown. The unresolved question is [specific constraint]; obtain the current rules before recommending this venue.

Why it works: relevance and permission are separate findings.
The placeholders require actual evidence before the brief can be delivered.

### Removal without a stated cause

Illustrative brief excerpt:

> [Post URL] displays a removal notice, but no reason is visible. [Comment URL] objects to the absence of test conditions. Treat that criticism as a proof gap; the moderation cause remains unknown.

Why it works: it preserves the visible evidence without diagnosing a filter.
The proposed proof requirement comes from the conversation, not guessed ranking mechanics.

### Consumer repair: proof does not generalize

Illustrative opportunity brief with unfilled evidence placeholders; no real community clearance or result is asserted:

> Permission: [current rule clause, URL, access date] governs repair demonstrations and affiliation disclosure. Observed question: [short excerpt and permalink] asks whether [repair method] holds under [use condition]. Source/sample limits: [sample definition, selected surface, collection period, source URLs]; these conversations don't establish repair durability. Supplied proof gap: [permissioned repair photos] show appearance but leave [load or wear condition] untested. Qualified angle: a scoped explanation of what the photos demonstrate and what remains untested, conditional on the cited rule permitting it (directional).

Why it works: the handoff uses a relevant artifact without treating visible repair as proof of durability.

### Local service: buying interest does not authorize outreach

Illustrative opportunity brief with unfilled evidence placeholders; no real request or consent is asserted:

> Permission: [current rule clause, URL, access date] determines whether service recommendations belong in [designated thread]. Observed question: [short excerpt and permalink] asks which [service] fits [location and job constraint]. Source/sample limits: [query, surface, collection period, source URLs]; search selection may omit other buying situations. Supplied proof gap: [documented service scope] lacks [evidence of suitability for this job]. Qualified angle: a sourced scope comparison for downstream drafting if permitted, with suitability unresolved until that evidence is supplied; the public question supplies no private-message consent (directional).

Why it works: buyer relevance, proof sufficiency, and permission remain separate decisions.

## Checklist

- [ ] Collection method and intended use are authorized; unknown permission switches research to supplied records or an authorized surface with a coverage note.
- [ ] Each recommended community has current rule evidence; unknown clearance is explicit.
- [ ] Each observation records source, timestamp, actual surface, and missing values.
- [ ] New counts carry sample labels; inferences and proposed angles are marked directional.
- [ ] Timing, formats, and saturation use community-specific evidence without fixed thresholds.
- [ ] AI disclosure, promotion, eligibility, and repost constraints preserve their actual scope.
- [ ] The brief distinguishes exposure, useful discussion, and reported downstream outcomes.
- [ ] Removed states have no invented causes; access and coverage limits are disclosed.
- [ ] Research tabs are closed; no content was published or seeded.

## References

- [Reddit Safety](https://redditinc.com/news/how-were-keeping-reddit-real-and-safe-in-the-ai-era), 2026-07-06.
- [Reddit Changelog](https://support.reddithelp.com/hc/en-us/articles/52393330268436-Changelog-August-12-2026), 2026-08-12.
- [Reddit Pro Trends](https://support.reddithelp.com/hc/en-us/articles/47619216411284-Reddit-Pro-Feature-Trends), 2026-05-28.
- [Reddit Infrastructure](https://redditinc.com/news/modernizing-reddits-infrastructure-and-moderation-tools), 2026-08-05.
- [Community Rules: r/rust](https://www.reddit.com/r/rust/about/rules.json) and [r/mcp](https://www.reddit.com/r/mcp/about/rules.json), undated, checked 2026-09.
- [Reddit Shopping](https://redditinc.com/news/in-case-you-saw-it-we-are-testing-a-new-shopping-product-experience-in-search), 2026-02-19; page includes a later test expansion, checked 2026-09.
- [Reddit Spam Guidance](https://support.reddithelp.com/hc/en-us/articles/28012014962580-How-do-I-keep-spam-out-of-my-community), 2026-03-28.
- [Reddit Eligibility](https://support.reddithelp.com/hc/en-us/articles/33702751586836-Poster-Eligibility-Guide-Post-Check), 2026-08-10.
- [Reddit Manipulated Content](https://support.reddithelp.com/hc/en-us/articles/41180423371156-Manipulated-Content-and-Misleading-Behavior), 2026-05-19.
- [Reddit Pro Performance](https://support.reddithelp.com/hc/en-us/articles/47618462633364-Reddit-Pro-Feature-Performance), 2026-04-02.
- [Reddit AutoModerator](https://support.reddithelp.com/hc/en-us/articles/15484574206484-Automoderator), 2026-08-28.
- [Reddit Reposting](https://support.reddithelp.com/hc/en-us/articles/4835584113684-What-is-reposting-fka-crossposting), 2026-07-13.
- [Reddit Community Seeding](https://support.reddithelp.com/hc/en-us/articles/15484360497812-Planting-seeds-aka-encouraging-and-maintaining-an-active-community), 2026-05-28.
- [Reddit Spam](https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam), 2026-05-19.

Re-validate when feed names, URL behavior, access policy, community rules, moderation tools, analytics fields, or inspectable performance research change.

Validated: 2026-09
