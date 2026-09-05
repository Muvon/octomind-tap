---
name: trend-youtube
title: "YouTube Trend Harvester Playbook"
description: "Harvest YouTube topic demand, channel-relative outliers, buyer questions, and reusable format ideas. Activate for YouTube trend scans, competitor or launch monitoring, and evidence-backed content briefs. Separate observed public data from private analytics and turn findings into original angles with explicit limitations."
license: Apache-2.0
compatibility: "Requires browser and network access. Account-specific Studio research requires an authorized signed-in session."
capabilities: browser memory-read memory-write
domains: browser
rules:
  - session(trend) content(youtube)
  - match(\byoutube\s+(trend|trends|trending|harvest|brief)\b)
  - match(\b(harvest|scan|analyze)\s+youtube\b)
  - match(\byoutube\s+(competitor|launch)\s+(research|monitoring|scan)\b)
  - session(trend) match(\boutlier\s+(video|videos|hunting)\b)
---

## Overview

Build a reproducible evidence brief for a specific audience, topic and campaign stage. Collect current URLs and observable facts, compare similar uploads, and identify what could be adapted with the user's own proof. Publishing and scriptwriting are downstream steps.

Don't turn a public breakout into a claim about retention, conversion, or algorithm causation. Separate observation, calculation and interpretation in every recommendation.

## Mental model

Treat channel-relative performance as a useful comparison, not a transferable guarantee. Compare similar formats at comparable ages and record the channel's size and context. A launch, news event or paid campaign can confound the apparent format advantage (directional).

Use separate Shorts and long-form baselines. Metricool found format, channel-size and frequency associations that differed across cohorts (measured, Metricool Shorts, n=799,718 videos, 2026-08). Don't infer that Shorts subscribers convert at a known rate or that adopting Shorts causes long-form decline.

Public views count playback starts; they don't establish qualified demand (official, YouTube performance FAQ, 2026-09). Qualified Shorts views exclude loops and require engaged views on public Shorts (official, YouTube qualified metrics, 2026-08). Keep public counts separate from private engagement and eligibility metrics.

## Harvest procedure

### Establish scope and access

Record the audience's job, language, geography, campaign stage, competitor set and research question. Read relevant prior observations when available. Use the user's authorized browser session for private surfaces; otherwise continue with public data and mark private metrics unavailable.

The evidence set does not establish current Charts category coverage, the legacy Trending-page status, Studio research-tab names, Hype eligibility, or the Google Trends query parameter. Discover these in the current interface rather than treating remembered URLs or menu paths as confirmed platform facts.

### Discover surfaces and capture working URLs

| Candidate surface | Navigation procedure | Capture or fallback |
|---|---|---|
| Public YouTube search | Open `https://www.youtube.com/`, enter the literal buyer task, inspect available filters | Copy the resulting URL and visible filter settings; don't construct or reuse an opaque filter token without checking it |
| Anchor and competitor channels | Follow the channel link from a verified result; open the relevant upload-format view | Copy the resolved channel and video URLs, displayed views and upload dates |
| Category charts, if present | Follow current YouTube navigation to the category surface relevant to the brief | Record its exact title, scope, country and resolved URL; don't assume a music endpoint covers podcasts or trailers |
| Google Trends | Open `https://trends.google.com/`; select YouTube Search if offered | Record the selected search property, region, time range and generated URL; omit corroboration if the YouTube property cannot be verified |
| Studio research, if accessible | Inspect the authorized account's current research and audience surfaces | Copy exact tab and card labels; inspect any searches or gaps shown. Don't assume Inspiration contains research cards |
| Shorts discovery, if offered | Inspect the current player and any visible trend or audio entry point | Capture the exact path and locale. Don't prescribe a pause-to-Trends route across app and web |
| Hype or experimental outlier tools, if offered | Inspect visible eligibility information and the account's available controls | Record the displayed definition and restrictions; omit absent features without guessing a subscriber threshold |
| Third-party outlier service, if authorized | Use available results with their disclosed methodology | Preserve source and denominator; independently inspect candidate videos |

These are conditional navigation procedures, not assurances of availability. An unavailable surface is a coverage limitation, not evidence of absent demand. Close only research tabs you opened.

### Record observations

For each candidate, save its resolved URL, channel, title, thumbnail description, publication date, observation timestamp, displayed views, format, language, duration and relevant audience context. Quote only the passage needed to establish the finding; inspect the video or transcript before claiming that its packaging promise is delivered.

Record representative buyer questions and objections from comments with their source URLs. Distinguish commenters' assertions from verified product facts. For competitor launches, record the shown feature, actual availability statement, CTA destination, commercial relationship if stated, and unresolved objections. Don't infer sales from praise or a busy thread (directional).

If private analytics are authorized, copy the metric name and date range exactly. “How many chose to view” means viewed versus swiped away (official, YouTube Shorts analytics, 2026-09). The Shorts player update uses hearts and the feedback controls “Not Interested” and “Don't recommend this channel” (official, YouTube Shorts experience, 2026-06). Don't relabel unavailable feedback as dislikes or invent a healthy swipe-away band.

### Compare and classify

Compute the baseline as the median of a declared set of comparable uploads. Record every baseline video and its observation age. Candidate views divided by that median gives the outlier multiple; if the denominator is missing or zero, report the multiple as unavailable. Avoid universal multiple cutoffs (directional).

Prefer comparable time-since-upload windows. If only current totals exist, state the age mismatch. Exclude dissimilar formats and label selection rules before comparing. Public counts do not reveal traffic source, paid support, private retention or unique buyers; treat these as unknown unless source evidence supplies them.

For historical comparisons, record the metric definition at each observation. Separate observations across a verified definition change; if comparable counts cannot be established, report the multiple as unavailable rather than pooling them (directional).

| Finding | Decision |
|---|---|
| Repeated packaging or structure across independent relevant channels | Propose a test using original proof; replication strengthens the hypothesis but doesn't establish transfer |
| Durable task query with current supporting examples | Propose a buyer-intent tutorial and show the demand evidence |
| News or controversy spike | Report the timing dependency; recommend only if the brief can act while it remains relevant |
| Isolated breakout or weak baseline | Mark tentative; collect corroboration before calling it repeatable |
| High views with irrelevant audience or uncheckable promise | Exclude from recommendations and state the reason |

These classification decisions are craft judgments (directional). Rank candidates by evidence quality and audience fit, with production feasibility as a gate. Don't assign precise scores that imply validated thresholds.

### Return an actionable brief

Each recommendation includes source observations, the explicit baseline calculation, corroboration or its absence, audience fit, and the original transformation. Describe the structural pattern as a hypothesis. Name the user's proof needed to execute it and a bounded outcome to evaluate (directional).

For a launch brief, separate the announcement opportunity from proof and objection-answer opportunities. Suggest a next-step destination only when verified. Include substantive buyer questions even when the source upload is not a view outlier (directional).

Use this compact launch-evidence handoff within the harvest, selecting relevant rows (directional):

| Opportunity | Capture and original proof needed |
|---|---|
| Launch walkthrough | Source URL, shown availability and limitations; user's working walkthrough and verified destination |
| Demo or artifact | Demonstrated steps and result; user's reproducible footage and prerequisites |
| Bounded customer proof | Source claim, baseline, conditions and exclusions; user's customer records and reuse permissions |
| Founder or build-in-public update | Speaker, stated role and actual decision; user's firsthand evidence, keeping founder testimony distinct from brand claims |
| Objection answer | Question and comment URL, existing answer and remaining uncertainty; user's relevant test and limitations |
| Handoff checks | Campaign audience, promise, stage and desired action; verified CTA route or unavailable; stated affiliations, permission gaps and observed enforcement evidence, without inferring suppression from low views |
| Community opportunity | Conversation URL, host rules and unanswered question; whether a launch link could directly help where promotion is permitted. Hand off the observation without posting |
| Follow-up, illustrative | Before launch: capture questions; at launch: inspect walkthrough and destinations; afterward: revisit objections at recorded comparable ages. Adjust checks to the research window |

Preserve sourced quotations and the speaker's register. Refer publishing execution to [social-youtube](../social-youtube/SKILL.md#launch-and-proof-posts).

Save permitted observations with timestamps for later comparison. Return observed facts and source URLs before interpretation, then limitations and the next useful research check. Don't reproduce a publishing-policy or dead-pattern checklist here.

## Examples

### Workflow opportunity

Illustrative record, not an actual harvest:

Candidate: [video URL], [channel], [observation timestamp], [format].
Baseline: [comparable upload URLs and ages]; median [views].
Calculation: [candidate views] divided by [baseline views] = [multiple].
Corroboration: [independent source URLs], or “unavailable.”
Buyer question: [sourced comment and URL].
Interpretation: a reproducible failure diagnosis may fit the audience (directional).
Transformation: demonstrate the user's documented failure and its limits using original footage; don't inherit the source creator's personal story.

### Timing-dependent result

Illustrative decision: a platform-outage reaction has unusually high public views, but the available examples depend on that outage. Record it as a timing-dependent topic. A reliability tutorial remains only a proposed transformation until supported by current buyer questions and the user's own evidence (directional).

### Consumer comparison: objection without an outlier

Illustrative record, not an actual harvest:

Candidate: [bag-comparison video URL], [channel], [format], [views], [observation timestamp and upload age].
Baseline: [same-channel comparable comparison URLs, views, timestamps and upload ages]; median [views].
Calculation: [candidate views] divided by [baseline median] = [multiple], or unavailable if comparable counts are missing.
Buyer objection: [comment asking whether a rigid lunchbox fits, quotation and URL].
Corroboration: [independent question or demonstration URL and observation], or unavailable.
Interpretation: the fit question may justify research even without an outlier; a comment establishes an objection, not the bag's capacity (directional).
Original proof needed: the user's matched packing demonstrations, documented bag and lunchbox dimensions, and observed exclusions; outcome [unverified].

### Local service: seasonal interest outside the service area

Illustrative record, not an actual harvest:

Candidate: [seasonal pruning video URL], [channel], [format], [views], [observation timestamp and upload age].
Baseline: [comparable local upload URLs, views, timestamps, upload ages and seasonal windows], or unavailable.
Calculation: unavailable until a comparable geographic and seasonal baseline is established; then [candidate views] divided by [baseline median] = [multiple].
Geographic scope: [verified source location and URL], [user's service-area source]; query corroboration [YouTube Search property, selected region, period, URL and observation], or unavailable.
Interpretation: interest outside the verified service area does not establish local buyer demand; a regional query cannot locate every viewer (directional).
Original proof needed: the user's local site assessment, applicable seasonal constraints and available service scope; outcome [unverified].

## Checklist

- [ ] Scope and access recorded; unavailable surfaces listed without fabricated findings.
- [ ] Harvest URLs copied from the current interface; Google Trends property confirmed before citing YouTube demand.
- [ ] Candidate and baseline records include observation timestamps, comparable formats and upload ages.
- [ ] Public observations separated from private metrics; unknown retention and conversion remain unknown.
- [ ] Calculation reproducible; no arbitrary universal outlier or swipe-away cutoff.
- [ ] Recommendation includes corroboration, timing dependency, buyer fit and original transformation.
- [ ] Launch monitoring includes verified CTA paths and unresolved buyer objections when relevant.
- [ ] No copied personal claims; examples and missing fields explicitly marked.
- [ ] Permitted observations saved; research-created tabs closed.

## References

Dates on undated Help pages denote validation month.

- [YouTube performance FAQ](https://support.google.com/youtube/answer/12220281?co=GENIE.Platform%3DDesktop&hl=en), undated; checked 2026-09.
- [Qualified Shorts metrics](https://blog.youtube/news-and-events/youtube-monetization-qualified-watch-hours-shorts-views/), 2026-08-12.
- [YouTube Shorts analytics](https://support.google.com/youtube/answer/12942217?co=YOUTUBE._YTVideoType%3Dshorts&hl=en), undated; checked 2026-09.
- [Shorts player update](https://blog.youtube/news-and-events/youtube-shorts-experience-updates-features/), 2026-06-25.
- [Metricool Shorts study](https://metricool.com/youtube-shorts-algorithm/), 2026-08-05; observational comparisons.

Re-validate when:
- Harvest surfaces, category coverage, URLs, account access or feature names change.
- View definitions, player controls or monetization metrics change.
- New reports revise comparative baselines or methodology.

Validated: 2026-09
