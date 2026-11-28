---
name: seo-strategy-brief
title: "SEO Strategy Brief: Levers, Priorities, Risks"
description: "Builds an evidence-cited SEO and GEO strategy brief: lever choice, P0 to P3 priorities, risks, measurement. Use when asked to plan SEO work, not to audit."
license: Apache-2.0
compatibility: "Requires web search and page fetching. Volume, difficulty and backlink data need a connected keyword-data provider; otherwise mark them as estimates."
rules:
  - match((?i)\b(seo|geo|aeo)\s+(strategy|plan|roadmap|brief)\b)
  - match((?i)(^|objective:\s*)\W*(plan|build|create|draft|write|develop|produce|propose|design)\b.{0,60}\b(keyword|topic\s+cluster|pillar|content\s+(strategy|calendar|plan)|link[- ]?building|outreach|digital\s+pr|guest[- ]post\w*|free[- ]tool|programmatic|refresh\s+plan|page\s+briefs?|source[- ]action|geo\s+(question|experiment)|question\s+set|outreach)\w*)
  - match((?i)\b(research|find|rank)\b.{0,40}\b(long-?tail|question\s+keywords?|keywords?)\b)
  - match((?i)\b(reddit\s+threads?|listicles?)\b.{0,80}\b(prioriti[sz]e|action|cited)\b)
  - match((?i)\bwhich\s+(seo\s+)?(lever|tactic)\b)
  - semantic(build a prioritised SEO roadmap with a measurement plan, 0.75)
  - semantic(plan content clusters and link building for the next six months)
---

## Overview

This skill produces the forward-looking plan: what to build, publish or earn next, ranked, with evidence and risk. The deliverable is a brief saved to disk. It does not audit existing assets diagnostically, and it does not write the content, draft outreach or build the tools: the brief is the deliverable, not the patch. Scope comes before volume: honor a narrow GEO question or audit finding, and reserve quarterly lever selection for an actual strategy request.

## Mental model

Search demand, intent, topical authority, link gravity and AI citation drive the plan. Every recommendation cites a SERP, a competitor, a search-volume signal or a measurable trend, and ladders to a measurable outcome. A tactic list is not a strategy.

## Rules

### Choose the mode

| Request | Mode |
|---|---|
| GEO or AEO, buyer questions, AI visibility | Apply the `geo-visibility-audit` skill in question-discovery or experiment-planning mode. Start from buyer decisions, not keywords; distinguish observed needs from hypothesized prompts; check existing coverage; use its GEO brief shape. Plan from documented findings without inventing causal diagnoses. DR, paid-tool access and analytics are not gates: record missing context and proceed provisionally unless a focused question is necessary. Return a versioned test set or a finding-linked experiment brief, not an automatic keyword calendar. |
| Cited sources, Reddit threads, listicles, getting mentioned | Apply `geo-source-actions` and return per-source action records, not drafts or a mention-count target. |
| Plan or brief a refresh from an existing queue or audit | Apply `seo-content-refresh` in planning mode and return its page briefs. Finding which pages declined and why is diagnostic work. |
| Programmatic or template pages | Apply `seo-programmatic` and return its verdict before any page count. |
| Domain move, replatform, URL restructure | Apply `seo-site-migration` and return the redirect map plan and monitoring window. |
| Business with a storefront or service area | Apply `seo-local`. |
| Anything else | The conventional procedure below. |

Dated Google policy facts come from `seo-google-policy-baseline`; don't quote them from memory.

### Conventional procedure

1. Profile: niche, audience, commercial position, geography, existing content, and DR where conventional SERP qualification needs it. For GEO work, prioritize the buyer decision and desired conversion instead.
2. Discover in one parallel block: web search for SERP competitors, competitor backlink pages, trend signals, People Also Ask style questions and Reddit or community threads; `knowledge(command="read", source="<url>")` for the pages that matter. Google-only SERP features and search volumes stay unverified unless they come from the user, Search Console or a keyword-data tool.
3. Qualify with the relevant rubric: SERP-realism for keywords; topical-fit-and-reachability for links; data-moat-and-niche-fit for free tools; primary-source-versus-intermediary for guest-post targets.
4. Cluster and prioritize: group survivors into clusters or campaigns and bucket them P0 to P3 with the scoring rationale.
5. Write the brief, structured, evidence-cited and saved to disk.

Memory: before any strategy work, `remember` the site niche, audience, existing strategy, competitors, past briefs, DR estimate and commercial position. Afterwards `memorize` the chosen lever, target list and rationale (importance 0.7 to 0.9 for committed decisions).

### Strategy rules

- Search intent before search volume. Volume on a mismatched-intent keyword is wasted; 100 visits at 8% conversion beat 10,000 at 0.2%.
- SERP-realism: target keywords where the top-10 average DR is within roughly +15 of the user's DR, banded by content-quality gap. A weak or old top 10 pushes the target higher; a definitive top 10 pushes it lower.
- Information gain is the kill rule. If you can't name what the new piece adds that the top 10 doesn't have, the keyword isn't claimable yet.
- Long-tail wins on three compounding axes: SERP-authority profile beats KD, intent specificity converts, and clusters earn topical authority. Google's AI features fan out into related sub-queries, so cover a topic's real sub-questions; a page per fan-out variation is scaled content abuse (Google AI optimization guide, May 2026).
- Topical clusters over single keywords: one pillar plus supporting cluster pages sized to the real sub-topics (Google: "there's no ideal page length"). Internal linking is reciprocal: the pillar links out, each cluster page links back early in the body.
- Cadence follows evidence, not a quota. A daily article target without new information per piece risks Google's scaled content abuse policy; plan the number of pieces the evidence supports.
- Quality over count on links. Ten different niche sites linking once each outweigh one site linking 100 times; unique referring root domains compound, raw inbound count doesn't.
- Niche fit can beat raw DR. Link value follows topical relevance (the reasonable-surfer model), so off-topic links count for little. Rank prospects on topical fit times authority, not authority alone.
- Compound, not spike. Free tools, programmatic pages and embed widgets keep earning links for years. HARO stunts and viral one-offs lose value as the news cycle moves.
- Data moat or no tool. A free tool without proprietary data is a commodity that competitors clone in a day. Every tool concept passes the data-moat gate.
- Primary source over intermediary. Google gave no specifics for the 2026 core updates; third-party analyses saw aggregation-model sites lose. Default to building the canonical resource on the user's own domain over publishing roundups on someone else's.
- Reddit and forums are not a ranking signal (the February 2024 Google-Reddit deal licenses data), but they fill many SERP slots and AI-answer citations. Where the niche has an active subreddit, recommend a 3-month authentic-engagement plan over directory submissions. Choose communities from the citations captured for the engines this buyer uses; Reddit's share differs by engine and shifts within months.
- Authentic mentions only: seeking inauthentic mentions isn't helpful per Google. Earn real mentions and refuse "100 brand mentions per month" pitches.
- AI measurement: Search Console's Generative AI report counts impressions, not clicks, and Web totals include them; verify live dimensions before claiming query-level presence. Use actual answer captures for prompt-level observations; vendor trackers are scoped samples. Separate search performance, AI visibility and attributable activation; study-level CTR changes aren't forecasts for this site.
- Paid links stay a violation: Google's link spam policy names paid links and optimized-anchor links in guest posts and press releases. Refuse any paid placement that passes ranking signal without rel=sponsored.
- Don't chase head terms on a low-DR site: surface realistic long-tails in the same cluster. Surface observed AI Overview presence (or mark it Unverified) and citation-share risk on informational keywords.
- Don't invent named publications, journalists or tool names. Verify with web search or `knowledge`; when verification fails, escalate to the user with a precise forked question.

### Missing inputs

- Missing commercial position: ask only if it blocks the requested brief. Missing DR: record Unknown and request it only for conventional SERP-authority qualification, never as a GEO prerequisite.
- A brief marked AUTONOMOUS or non-interactive: don't ask for DR or commercial position. Estimate them from live signals, label them estimates in the Site Profile, and proceed.
- "Help me with SEO": ask which goal applies: keyword research, content cluster, link campaign, free tool, GEO, programmatic SEO, guest posting or digital PR.

## Output format

For GEO work use the question-register or experiment-brief report and filename from the `geo-visibility-audit` skill; `geo-source-actions` and `seo-content-refresh` define their own reports and filenames. The template below is for conventional strategy. Save it as `seo-strategy-[lever]-[YYYY-MM-DD].md` in the working directory.

```markdown
# SEO Strategy: [Goal — keyword research / cluster plan / link campaign / GEO / free-tool / digital PR / guest-posting / programmatic]
Date: YYYY-MM-DD

## Site Profile
- Niche: [...]
- Audience: [...]
- DR estimate: [...]
- Commercial position: [...]
- Geo / language: [...]

## The Lever (one per quarter)
- [ ] Keyword cluster — [pillar + cluster keywords]
- [ ] Link campaign — [target type, tactic]
- [ ] Free tool — [concept, data moat]
- [ ] Programmatic SEO — [data set, URL pattern]
- [ ] Digital PR — [hook, publication tier]
- [ ] Guest posting — [author tier, target type]
- [ ] GEO / AI-citation — [target pages, buyer questions to test]

## Plan (P0/P1/P2 priorities)
| Priority | Item | Evidence | Effort |
|---|---|---|---|
| P0 | ... | ... | ... |

## Detail (lever-specific)
[Per lever — cluster: pillar + cluster keywords by intent and content type; links: prospects by category, tier, approach; free tool: niche fit, data moat, feasibility, monetization; programmatic: data source, URL pattern, template fields, linking, sitemaps; digital PR: 3 hooks with tier and journalist angle; guest posting: tier, targets, gap topics; GEO: priority pages, prompt-monitoring list]

## Risk Notes
- AIO presence on target keywords: [X of Y observed in dated captures, or Unverified]
- Site Reputation Abuse risk: [present/absent on dominant SERPs; name the region, since manual actions no longer apply to EEA searchers]
- Algorithmic risk flags: [paid-link patterns, manufactured mentions, exact-match anchor over-use, velocity spikes]

## Measurement
- Primary KPI: [...]
- AI-search visibility KPI: [citation share tracking via X tool]
- Cadence: [weekly / monthly / quarterly]

## Open Items (the brief consumer should resolve before execution)
- [...]
```

## Checklist

- [ ] The mode matches the request, and a GEO request used the GEO report shape.
- [ ] Every recommendation cites a SERP, competitor, volume signal or trend, and names its risk.
- [ ] Volume, DR, traffic, KD and competitor numbers are verified or marked as estimates.
- [ ] Keywords pass the SERP-realism and information-gain gates; no head terms on a low-DR site.
- [ ] No link scheme, private blog network or paid placement without rel=sponsored.
- [ ] The plan ladders to a measurable outcome, not a tactic list.
- [ ] The brief is saved under the expected filename and the path is returned.

## Composition / References

- `seo-keyword-research`, `seo-backlink-prospecting`, `seo-guest-posting` and `seo-tool-discovery` hold the procedures for each lever.
- `geo-visibility-audit`, `geo-source-actions`, `seo-content-refresh`, `seo-programmatic`, `seo-site-migration` and `seo-local` cover the special modes in the table above.
- `seo-google-policy-baseline` is the source for dated Google facts.
