---
name: trend-hackernews
title: "Hacker News Trend Harvester Playbook"
description: "Harvest Hacker News discussions and inspectable artifacts into a dated, source-linked brief. Activate when researching HN trends, prior submissions, launch examples, or audience objections. Separate observed attention from ranking hypotheses and product demand."
license: Apache-2.0
compatibility: "Requires browser access to Hacker News and Algolia. Inspect removed items with a logged-in profile configured for showdead."
capabilities: octoweb memory-read memory-write
domains: browser
rules:
  - session(trend) content(hackernews)
  - session(trend) content(hn)
  - match(\b(hacker\s*news|hn)\s+(trend|trends|harvest|brief|post|submit)\b)
  - match(\b(harvest|scan|analyze)\s+(hacker\s*news|hn)\b)
  - match(\bshow\s*hn\b)
  - match(\bask\s*hn\b)
---

## Overview

Harvest HN evidence for a specific topic, audience, and decision. Return a dated brief with inspectable sources and limits on what the observations establish. Publishing and human-authored responses are downstream work; don't produce pasteable posts or contact commenters.

## Mental model

Separate attention from usefulness. Compare public points and comments within a declared sample, then read the conversation to find evaluation problems and unanswered questions. Don't infer ranking weights from correlations, profile karma, domain names, or a popular commenter (directional).

HN describes ranking as points divided by a power of age, with flags, anti-abuse software, overheated-discussion demotion, account or site weighting, and moderator action also affecting placement. The FAQ says higher submitter karma doesn't make posts rank higher (official, HN FAQ, 2026-09). Don't convert these mechanisms into invented constants or a comment-to-point target.

Quiet submissions belong in the sample: the median Show HN received 2 points and 0 comments in a recent corpus (measured, Jonno, n=41,301 submissions, 2026-07). A front-page-only collection can't estimate typical outcomes. Comment volume isn't evidence that replies boost rank; don't label a rank drop a penalty without direct evidence.

## Harvest procedure

### Define the scope

Record the research question, relevant audience, candidate topic terms, and intended product-evaluation decision. Define time bounds and comparison formats before selecting examples. Use the same bounds when comparing angles; keep evergreen exemplars separate from the current sample (directional).

### Open the relevant surfaces

All HN paths below use https://news.ycombinator.com. Follow the live navigation and record the resolved URL. The directory names and descriptions come from HN's list directory and FAQ (official, HN Lists and HN FAQ, 2026-09).

| Surface | URL | Use and limit |
|---|---|---|
| Front page | https://news.ycombinator.com/news | Record current placement; follow More for later pages without assuming they're all decaying. |
| New submissions | https://news.ycombinator.com/newest | Include overlooked work; don't infer an age cutoff from inclusion. |
| New Show HN | https://news.ycombinator.com/shownew | Sample new artifacts before selection into the main Show feed. |
| Show HN | https://news.ycombinator.com/show | Selected Show HNs; don't treat as the full population. |
| New Ask HN | https://news.ycombinator.com/asknew | Sample new text submissions and genuine questions. |
| Ask HN | https://news.ycombinator.com/ask | Questions and other text submissions; inspect the actual format. |
| Best | https://news.ycombinator.com/best | Highest-voted recent links, not a calendar-day leaderboard. |
| Launches | https://news.ycombinator.com/launches | YC launches; separate this curated program from ordinary Show HN. |
| Highlights | https://news.ycombinator.com/highlights | Selected comments from across years; use for depth and register, not current trend frequency. |
| Second-chance pool | https://news.ycombinator.com/pool | Record pool inclusion when visible; don't infer the original submission's trajectory. |
| Repost invitations | https://news.ycombinator.com/invited | Overlooked links invited to repost; don't treat an invitation as a self-serve entitlement. |
| Hiring threads | https://news.ycombinator.com/whoishiring | Locate the relevant recurring thread and read its own instructions. |
| Algolia | https://hn.algolia.com/ | Search topic terms and prior URLs; set filters in the live interface. |

Ask and Show have a small points threshold before inclusion in their main feeds; their new feeds cover incoming submissions (official, HN FAQ, 2026-09). Don't assign a numeric threshold.

For Algolia, open the base search URL, enter the topic, choose the requested date range and sort in the interface, then copy the URL the interface produces. Verify the visible filter state and returned timestamps. Don't hand-assemble remembered last24h or pastWeek parameter values. Record exact window bounds, sort choice, returned count, and whether pagination was exhausted; if the interface fails, report the missing coverage. This is a reproducibility procedure, not a claim about undocumented query parameters (directional).

Repeat for the product URL and distinctive title phrases to find previous submissions. Separate retries, materially changed releases, and articles that merely mention the same technology (directional).

### Read before classifying

For each candidate, record the verbatim title, item URL, destination, submitter handle, submission timestamp, collection timestamp, points, comments, observed feed placement, and literal visible status. Mark unavailable values unknown. Follow the source link and read relevant reply branches before describing the claim or audience response (directional).

Record author context as submission text or first comment, whichever is present. Show HN moderator guidance accepts either placement if submission text doesn't appear; it sets no mandatory first-comment deadline (official, Show HN Tips, 2026-09).

Inspect whether strangers can try the work. Show HN excludes landing pages, signup-only pages, newsletters, and ordinary blog posts, and asks makers to be available (official, Show HN Guidelines, 2026-09). Record pricing visibility and evaluation barriers as product-readiness observations, not automated penalty causes (directional).

Read for reusable evidence: the question a prospective user asks, an implementation report, a specific objection, or a limitation the maker acknowledges. Record the source comment and distinguish the author's claim from independent corroboration. Don't copy another person's first-person experience into a writing brief as the user's experience (directional).

### Compare without inventing causality

| Evidence available | Permitted inference |
|---|---|
| A single timestamped snapshot | Report visible counts and age; don't call lifetime average points an early velocity curve. |
| Repeated snapshots | Calculate change in visible points divided by elapsed time; label the interval and missing observations. This arithmetic isn't a model of HN ranking. |
| Similar subject across sampled threads | Compare questions and proof; describe repetition within the searched scope rather than declaring universal saturation. |
| A rank drop | Report the observed movement. Leave the cause unknown. |
| A flagged or dead label | Record the literal state; don't invent a flag count, account diagnosis, or detection input. |
| Self-reported signups or purchases | Attribute them to the author with the stated window; don't infer paid adoption from comments or stars. |

The table is an analysis procedure (directional). Label every measurement with its source name, actual reviewed scope, and collection month; the specimen below shows the format. Label interpretive recommendations “(directional)” and omit precise numerical prescriptions without evidence.

For removed items, check the item page and profile showdead setting; dead content is hidden by default (official, HN FAQ, 2026-09). Don't claim that logging in alone reveals every removed post. Missing pages and inaccessible sources are coverage gaps, not negative findings.

## Launch evidence and handoff

Keep approved Launch HN separate: it is a curated, one-time YC program with an agreed day and front-page placement (official, Launch HN Instructions, 2026-09). Copy observed batch codes verbatim without generating a current-code list or a scheduling rule.

For Show HN, report the audience problem, artifact, available proof, desired action, and destination. Include commercial terms, affiliation, and remaining limits as observations. Suggest a missing-proof question when needed. Don't transform the harvest into a launch copy template (directional).

Use founder availability as the scheduling input. Treat weekday audience overlap as an experiment rather than asserting a universal best hour (directional). Response coverage can extend beyond the opening burst: the median cumulative curve reached 50% of comments at 7.2 hours and 90% at 26 hours (measured, Jonno, n=2,066 Show HNs with at least 10 comments, 2026-07). These are discussion-subset observations, not survival gates or optimal posting times.

Don't recommend community voting, booster comments, or asking friends to participate. HN prohibits soliciting votes, comments, or submissions (official, HN Guidelines and Show HN Guidelines, 2026-09). Note a useful contributor's public evidence only when it bears on the research question; don't turn handles into an outreach or influence list.

## Brief output

Return the scope and coverage limits before the candidate table. For each useful example, include the source and collection time, factual observation, possible lesson, and counterevidence. Keep title text verbatim; for linked articles, flag unexplained differences from the source headline rather than generating alternatives (official, HN Guidelines, 2026-09).

Group substantive objections by evaluation problem, with links to the supporting comments. Separate native attention counts from destination conversion evidence. End with what the author needs to supply and which sources remain inaccessible (directional).

HN prohibits generated or AI-edited text in comments, and moderator guidance extends the hand-writing requirement to Show HN text (official, HN Guidelines and Show HN Tips, 2026-09). Deliver research notes; don't propose disguising AI authorship.

## Examples

### Illustrative artifact record

This is a schema specimen, not a real result. Brackets must be replaced with observed evidence in a delivered brief.

```text
Title: [verbatim title]
Item and destination: [item URL] / [artifact URL]
Collected: [timestamp]; submitted: [timestamp]
Surface and status: [observed feed] / [literal label or no visible label]
Points and comments: [observed values]
Evidence label: (measured, [harvest name], n=[reviewed scope], [collection month])
Evaluation: [what a stranger could inspect]
Author context placement: [submission text or first comment]
Qualified-interest evidence: [comment URL and accurate paraphrase]
Limitation: [unanswered evaluation concern]
Interpretation: [bounded editorial inference] (directional)
Ranking cause: unknown
```

### Illustrative moderation comparison

Rejected reasoning: infer that a SaaS domain or submitter karma caused a flagged state.

Accepted record: preserve [item URL], [collection timestamp], and [visible label]. Note whether an explicit moderator explanation exists. With no explanation, record the cause as unknown. Keep product-readiness criticism separate from platform enforcement.

### Illustrative repeated angle

Search [topic terms] over [declared date bounds]. Link the reviewed threads and identify the repeated implementation claim. If the user's material supplies [new evidence or a different constraint], explain how it differs. Otherwise report that the searched examples leave the proposed contribution unclear; don't apply a fixed saturation count.

## Checklist

- [ ] Scope, queries, date bounds, resolved URLs, collection time, and incomplete coverage are recorded.
- [ ] New and overlooked submissions balance selected winners; Launch HN and historical comments remain separate.
- [ ] Each example has a source link, literal status, observed counts, and an evidence label.
- [ ] Velocity uses repeated snapshots; no hidden upvote ratio, domain bonus, or karma weight is inferred.
- [ ] Qualified interest comes from substantive thread evidence; conversion is source-attributed separately.
- [ ] Author context placement, pricing, trial access, affiliation, and limitations are observed rather than invented.
- [ ] Shared title, timing, feed, repost, and human-authorship facts follow the cited official sources.
- [ ] No booster-comment plan, pasted prose, or invented personal experience enters the handoff.
- [ ] All research tabs opened for this task are closed when no longer needed.

## References

Official pages are undated unless stated; labels use the validation month.

- [HN Guidelines](https://news.ycombinator.com/newsguidelines.html), [HN FAQ](https://news.ycombinator.com/newsfaq.html), [HN Lists](https://news.ycombinator.com/lists): checked 2026-09.
- [Show HN Guidelines](https://news.ycombinator.com/showhn.html), [Show HN Tips](https://news.ycombinator.com/item?id=22336638), [Launch HN Instructions](https://news.ycombinator.com/yli.html): checked 2026-09.
- [Algolia search](https://hn.algolia.com/): use the current interface; coverage recorded per harvest, 2026-09.
- [Jonno study](https://jonno.nz/posts/your-show-hn-dies-in-7-hours/): 2026-07; distinguish the full corpus from the discussion subset.

Re-validate when:
- Feed names or Algolia filter behavior change.
- HN policy, moderation guidance, or submission text placement changes.
- New reproducible outcome or response-timing studies appear.

Validated: 2026-09
