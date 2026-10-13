---
name: seo-backlink-prospecting
title: "Backlink Prospecting & Qualification: Find Safe Free Places"
description: "Operational funnel for finding and qualifying SAFE free places to place backlinks. Encodes the prospect categories (reclamation, resource pages, broken links, journalist requests, communities, aggregators, niche directories), the per-target qualification rubric (topical fit, real traffic, outbound profile, page context, anchor naturalness, reachability), Google's link-spam guardrails (penalty triggers, rel attribution rules), and the 2026 AI-search citation overlay (Reddit/community as Perplexity/ChatGPT citation sources). Use AFTER niche/audience are clear and BEFORE any outreach. Stays in the SEO lane: produces a prospect brief; outreach copy and on-page wrappers are downstream concerns owned elsewhere."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires websearch and webfetch for prospect discovery and qualification."
domains: seo
rules:
  - session(seo)
  - content(backlink)
  - content(backlinks)
  - content(linkbuilding)
  - match(\blink[\s-]?building\b)
  - match(\bfind\s+(places\s+to\s+)?backlink\w*)
  - match(\bwhere\s+to\s+(get|build|place)\s+backlinks?\b)
  - match(\blink\s+prospect(ing|s)?\b)
  - match(\boutreach\s+(target|list|pros)\w*)
  - match(\bguest\s+post(ing|s)?\b)
  - match(\bbroken\s+link\s+build\w*)
  - match(\bunlinked\s+(brand\s+)?mentions?\b)
  - match(\bresource\s+page\s+links?\b)
  - match(\b(haro|qwoted|featured\.com|journorequest)\b)
  - match(\bdigital\s+pr\b)
  - content(HARO)
  - semantic(where can we get backlinks safely for our website)
  - semantic(find places to publish links pointing to our site)
  - semantic(safe free link building opportunities)
  - semantic(list of websites to get backlinks from in our niche)
  - semantic(how to do outreach for backlinks without getting penalized)
---

## Overview

Free-backlink attempts fail by spraying generic directories and forums (no value, penalty risk) or by leaning on one tactic (only HARO, only guest posts) until it stalls. This funnel groups opportunities by category and risk, qualifies every target manually before outreach, and bakes in Google's link-spam policy to avoid algorithmic devaluation and manual actions.

Use it AFTER niche and audience are clear and BEFORE any outreach email. Deliverable: a prioritized prospect list with an outreach approach per category; outreach copy, on-page wrappers and tracking belong to the orchestrating agent.

## Instructions

### Core Rules

- Topical fit beats authority. DR/DA is an obsolete primary filter: a DR-30 site with 5 years in your exact vertical beats a DR-80 generalist link farm, so check vertical history first. A 1 on topical fit is an automatic strike; off-topic high-DR links draw Google's reasonable-surfer discount and mixed-niche cluster signals. Third-party readings of the March 2026 (Mar 27–Apr 8) and May 2026 core updates saw aggregation-model sites lose (Google gave no specifics): discount "list of Y for Z" pages with no primary value.
- Manual qualification, every prospect. No batch submission or automated discovery-to-outreach pipelines; mass-submit directory tools are the fastest path to a manual action.
- Intent test: would this link exist if SEO didn't? If not, it's a violation in waiting; Google's policy treats intent as the natural/unnatural line.
- Toxic neighborhood is permanent. A site linking to spam (casino/pharma/foreign-language farms) is contaminated even if your page looks clean; penalty contagion is real.
- Velocity matters. Natural sites earn links at a steady rate. A 50-link week is fine once, on a newsworthy basis; a sustained, unexplained spike is a classic link-scheme footprint.
- Anchor diversity. Branded ("Acme"), URL-only ("acme.com") and natural-phrase anchors dominate; exact-match stays a minority. Outreach you control always uses branded.
- Community links count even when nofollow. Reddit, Stack Exchange and LinkedIn group posts are usually `rel="ugc"` or `nofollow`, but forum threads hold many SERP slots and AI-answer citations, and branded web mentions correlate with AI Overview visibility more than backlinks do (Ahrefs, 2025; correlation, not cause). Treat them as visibility, not just SEO.
- Output a prospect brief, not a verdict.

### The Funnel

#### Stage 1 — Profile the Site

Get concrete answers first; if unclear, stop and ask.

1. Niche — one sentence, plus sub-niche.
2. Audience — who visits and what they search for.
3. Existing link profile — rough count, top referring domains, past penalties (`site:[domain]`, Search Console if accessible).
4. Brand mentions — `"[brand]" -site:[domain]`.
5. Linkable assets — original data, tools, comprehensive guides, calculators. If none, flag that prospecting is uphill until one exists and recommend `seo-tool-discovery` in parallel.

#### Stage 2 — Generate Prospect Lists by Category (parallel)

PARALLEL-FIRST: fire all category searches in ONE block. Ordered by risk-adjusted ROI:

##### A. Reclamation (highest ROI, lowest risk)

Already mentioned; you only ask for the link. Converts at 30–60%, far above any cold tactic.

- Unlinked brand mentions — `"[brand]" -site:[your-domain.com]`, body-copy mentions without a link. Top priority: Tier-1 publications (Forbes, Times, Fortune), which rarely accept cold guest posts but will reclaim a link they meant to add.
- Broken backlinks to your site — pages linking to your now-404 URLs. Restore or 301; no outreach needed.
- Image attribution — Google Images reverse-search your branded images, charts, screenshots; uncredited users usually add a link when asked.

##### B. Discovery-based (moderate effort, low risk)

Pages that exist to host links to good content.

- Resource pages — `[topic] intitle:resources inurl:resources`, `[topic] "useful resources"`, `[topic] "recommended links" OR "useful links"`, `[topic] "best [tools/blogs/guides]" 2026`.
- Broken link building — find 404 outbound links on niche resource pages and roundups (free broken-link checker), pitch your URL as replacement.
- Niche aggregators — Hacker News (tech), Product Hunt (products), Indie Hackers, Designer News, Lobsters, niche subreddits; usually nofollow but drive traffic and mentions.
- Industry-specific directories — human-curated, one vertical (SaaS directories, lawyer directories per jurisdiction, dev-tool catalogs). NOT generic web directories.
- Best-of listicles — `[topic] "best [thing]" 2026 OR 2025`; email the author a fit case.

##### C. Earned via outreach (high effort, highest authority)

Original value first; the link is the byproduct.

- Journalist requests / digital PR (HARO replacements after the Dec-2024 shutdown); best results come from working 2–3 at once:
  - Source of Sources (SOS) — free, by Peter Shankman (original HARO creator); honor system, off-topic pitch = ban.
  - Featured.com — relaunched HARO brand, free daily newsletter, more selective than the original.
  - Qwoted — expertise-profile matching; journalists post queries.
  - #JournoRequest and #PRRequest on X — direct, no platform.
- Guest posts — `[topic] intitle:"write for us"`, `[topic] "submit a guest post"`, `[topic] "contributor guidelines"`. Never pay, never accept a flat-fee structure; pursue only sites with editorial review (named editor, rejection rate, masthead). Paid without `rel="sponsored"` = penalty.
- Podcast / interview pages — `[topic] inurl:interview OR inurl:podcast`; pitch yourself as a guest, episode pages link out.
- Original research — pitch unique data (survey, benchmark, study) to niche journalists; 22+ links from one report is realistic.

##### D. Community (high effort, AI-citation value, mostly nofollow)

Usually `rel="ugc"`/nofollow, but load-bearing for LLM citation visibility.

- Reddit (highest LLM-citation weight) — `site:reddit.com [topic] [pain point]`. Engage genuinely; link only when it adds value AND the subreddit allows. Most ban self-promotion; break rules, get banned.
- Stack Exchange (technical) — answer in your area, link as supporting reference.
- LinkedIn groups, niche forums, Discord/Slack — long-form engagement, no hit-and-run drops; 3 months of presence before any link.
- Niche Q&A — Quora, vertical Q&A platforms.

##### E. Profile / listing (low effort, modest value, legitimate when niche-fit)

- Industry awards — "best of" lists in your vertical.
- Speaker pages — every conference you speak at links out.
- GitHub README cross-references — for dev sites, a popular repo's README mention compounds.
- Wikipedia citations — only with a genuinely citable original source; never add the link yourself, let an editor decide.
- About / partnership pages — vendor partner directories, testimonial pages on tools you use.

##### F. Forbidden (kill on sight, no exceptions)

- Generic web directories (DMOZ clones, "submit URL" sites)
- Foreign-language link farms, however cheap
- Comment spam (any optimized-anchor comment)
- Forum signature link farms with optimized anchors
- "Write for us" pages taking any topic for a flat fee without `rel="sponsored"`
- PBNs of any tier (AI-content PBNs are also scaled content abuse)
- Paid-link networks disguised as guest-post networks
- Reciprocal-link schemes ("we link, you link" en masse)
- Auto-generated content sites
- Casino / pharma / porn / sketchy-finance neighborhoods (unless that is your niche)

#### Stage 3 — Qualify Each Prospect (Rubric)

Check in order (verify, then strike condition); STRIKE on the first failure. A kill-rule, not a score.

1. Topical fit — read 5 recent articles. Strike: mixed-niche, off-topic, abandoned vertical.
2. Real traffic — Similarweb / Ahrefs estimate plus manual engagement check (comments, shares). Strike: bot traffic, no organic, no engagement.
3. Editorial signals — real-name author bios, dates, comments, depth. Strike: auto-generated, plagiarized, no human editor.
4. Outbound link profile — sample 5 outbound links from recent articles. Strike: spam neighborhoods, foreign farms, casino.
5. Indexed and ranking — `site:[domain]`, ranks for its target keywords? Strike: not indexed, ranks for nothing, deindexation flags.
6. Page context — visit the page where your link would land. Strike: buried among 100+ outbound links or a pure link page; 30–70 outbound is the sweet spot.
7. Anchor / rel naturalness — view source or their anchor template. Strike: forced exact-match anchor in editorial; rel-stripped paid link.
8. Reachability — find a named editor / contact email. Strike: ghost editor, no contact, generic info@ only.
9. Cost transparency — read "write for us" / contact / ad pages. Strike: paid placement passing ranking signal without `rel="sponsored"`.
10. Penalty history — search `"[domain]" + penalty OR deindexed`. Strike: documented manual action.
11. Velocity contribution — its place in the campaign's pace. Strike: pushes velocity past natural range.

Survives all 11: eligible for outreach. Anything else: skip.

#### Stage 4 — Rank Survivors

Composite score: topical fit 3×, real traffic 2×, authority signals (DR / DA / TF) 1× as tie-breaker only, reachability 1× as a multiplier (unreachable = 0).

Top 20%: priority outreach this month. Middle 60%: systematic follow-up over the quarter. Bottom 20%: skip, opportunity cost too high.

#### Stage 5 — Prospect Brief

The brief is the deliverable:

```markdown
# Backlink Prospecting Brief: [Site / Campaign Name]

## Site Profile
- Niche: [...]
- Audience: [...]
- Existing link profile: [rough DR / referring domains / past penalty notes]
- Brand mentions found: [count + Tier-1 examples]
- Linkable assets identified: [list — flag if thin]

## Prospect Pool by Category (one table per category)
- A. Reclamation (priority, fastest wins): Source, Page, Mention/Link Status (e.g. unlinked mention), Outreach Approach (direct ask), Tier (T1...)
- B. Discovery-based: Source, Page Type, Topical Fit, Traffic, Outreach Angle, Score
- C. Earned (digital PR / guest posts / podcasts): Platform / Publication, Hook, Pitch Angle, Approach, Status
- D. Community (visibility / AI-citation): Platform, Strategy, Cadence, Notes (e.g. Reddit r/[sub]: answer-first engagement, no link drops, 3×/week, nofollow but high LLM-citation value)
- E. Listings / profiles: Directory / List, Submission Process, Cost, Verdict
- F. Toxic, explicitly excluded: each with its strike reason, so the call is auditable

## Outreach Approach Per Category
- Resource page (brief, value-first): "I noticed your resources page on X. I built [thing] that adds [unique angle]. No worries if it's not a fit."
- Broken link (helpful, factual): "Your post links to [URL] which is 404. [My replacement] covers the same scope."
- Unlinked mention (gracious, low-friction): "Thanks for mentioning [brand]. Could the next edit add a link to [URL]?"
- HARO/Qwoted/SOS (editorial, expert-positioned): 75–100 words, lead with credentials, direct expertise, no pitch slap
- Forum / Reddit (peer, not promotional): genuine answer; link only if it adds value
- Guest post (editorial, contributor-positioned): a topic the site hasn't covered + your unique data

## Velocity Plan
- Target pace: [X new links / month based on baseline]
- Monthly budget by category: [reclamation N, discovery N, earned N, community ongoing]
- Red flags: spike weeks, anchor concentration, sudden DR drop on referring domains

## Open Items (for the orchestrating agent)
- Outreach copy per template above
- On-page wrapper / landing page setup
- Link-worthy asset build (if profile thin)
- Tracking instrumentation
```

### Decision Guide — Edge Cases

- "Write for us" or aggregator charging a fee (e.g. $50) for a followed link without `rel="sponsored"`: strike, undisclosed paid editorial.
- On-topic forum thread, 4 days old, active: engage; answer first, link only if it adds value.
- Looks legit, no organic traffic per Similarweb: brand-new is OK, dead is a skip; check whois date + Wayback.
- "We'll add you if you add us": once between two niche-relevant sites is OK; mass exchange is not.
- Subreddit bans self-promotion: engage without linking; link in profile only.
- Unsure if a site is a PBN: skip; uncertainty alone is a strike. Tells: footer disclosures, identical templates, single hosting IP, same author across "different" sites.
- User wants mass directory submission: refuse and explain; "low-quality directory or bookmark site links" is named in Google's link spam policy.

### Google's Link-Spam Policy — the hard lines

Quoted from Google's spam policies (updated 2026); kill-rules.

- "Exchanging money for links, or posts that contain links" and "Exchanging goods or services for links"
- "Sending someone a product in exchange for them writing about it and including a link"
- "Excessive link exchanges ('Link to me and I'll link to you') or partner pages exclusively for the sake of cross-linking"
- "Using automated programs or services to create links to your site"
- "Requiring a link as part of a Terms of Service, contract, or similar arrangement" without letting the content owner qualify it
- "Advertorials or native advertising where payment is received for articles that include links that pass ranking credit, or links with optimized anchor text in articles, guest posts, or press releases distributed on other sites"
- "Low-quality directory or bookmark site links"; keyword-rich widget links; widely distributed footer/template links
- "Forum comments with optimized links in the post or signature"
- Manufactured "brand mentions" — Google's May 2026 AI optimization guide says seeking inauthentic mentions isn't helpful and its AI features depend on its spam systems. Engineer real mentions (genuine engagement, real expert presence, real product/data placements), not synthetic campaigns.

Allowed:
- Paid links with `rel="sponsored"` or `rel="nofollow"` — "It's not a violation of our policies to have such links as long as they are qualified."
- User-generated content links with `rel="ugc"` (forums, comments)
- Genuine editorial endorsement
- Disclosed, properly attributed sponsorships / advertising

### AI-Search Citation Overlay (2026)

- Google: AI Overviews and AI Mode use Search's ranking and spam systems; no special markup or llms.txt needed (AI optimization guide, May 2026). Organic quality and authority still decide eligibility.
- Forums and Reddit rank among the most-cited domains in several 2025–2026 studies, but shares vary widely by study, engine and month — cite a dated source or no number.
- ChatGPT search uses third-party search providers (historically Bing) plus OpenAI's own crawler: allow `OAI-SearchBot` in robots.txt and submit sitemaps to Bing Webmaster Tools.
- Clicks shrink on AI-answer queries: Pew (2025) saw traditional-result clicks fall from 15% to 8% of visits with an AI summary; Seer (2025) measured ~61% lower organic CTR on AIO queries.

Implication: for AI-search visibility, weight community engagement and brand-mention reclamation higher (nofollow/ugc mentions still drive citation share); for pure organic rank, editorial backlinks dominate; for omnichannel, both.

### Tools — what's free and what isn't

Free: Google Search Console (existing backlinks, manual actions, indexing); Google Search with operators (discovery); Wayback Machine (site longevity / topical history); Bing Webmaster Tools (backlink data, sometimes links Ahrefs misses); `site:` + manual review (outbound link audit); Source of Sources and Featured.com newsletter (journalist requests); Reddit / Stack Exchange (community prospecting).

Limited free / freemium: Ahrefs Free Backlink Checker (top 100 backlinks of any domain); Moz Link Explorer (DA / spam score samples); Ubersuggest (DR estimates); Qwoted (journalist requests); Hunter.io / Apollo (editor email discovery).

Paid (full backlink graphs, advanced filters): Ahrefs, Semrush, Majestic; mention, but out of scope for free prospecting.

## Examples

### Example 1: Dev-tools SaaS (CI/CD pipeline)

Profile: CI/CD tool for platform engineers at 50–500-person orgs ("deploy faster", "GitHub Actions alternative", "monorepo CI"); ~80 referring domains, mostly dev blogs and Hacker News; 12 unlinked dev-blog mentions plus 1 in InfoQ (Tier-1); 3 deep technical guides, 1 benchmark report.

Stage 2, one block: resources, "GitHub Actions alternative" best-of, `site:reddit.com r/devops "monorepo CI"`, `"acme-deploy" -site:acmedeploy.com`, write-for-us devops, `intitle:interview "CI/CD"`, Hacker News + Lobsters submission history.

Stage 3 sample:
- InfoQ unlinked mention: passes all 11, free. Priority 1.
- dev-blog-X guest post: low traffic, else passes. Proceed.
- "Best CI tools 2026" listicle on a monetized site: paid outbound placements, exact-match editorial anchor, $300/year. Strike (paid editorial, no `rel="sponsored"`).
- r/devops AMA: on-topic, nofollow, free. Engage (AI-citation play).
- dev-tools-directory.net: generic, auto-content, links to casino, not indexed, $50. Strike (toxic neighborhood + paid + auto-content).

Output: 14 ranked priority prospects, outreach approach per category.

### Example 2: Cosmetics e-commerce (continuing the prior skill's example)

Profile: inclusive shade-range foundation store; women 25–45 searching "foundation for [skin tone]"; 8 unlinked mentions, mostly beauty bloggers; assets: SKU database with hex codes (proprietary moat) and the Tone Matcher tool from the previous skill.

Stage 2 (parallel): "foundation for [skin tone]" best-of lists, inclusive-beauty resource pages, `site:reddit.com r/MakeupAddiction "foundation match"`, unlinked `"acmebeauty"` mentions, beauty/lifestyle journalist requests, beauty directories (Beauty Independent, etc.), inclusive-beauty conference speaker pages.

Notable calls: generic beauty directory taking any submission for $20, strike (low-quality directory); "best foundations" listicle on a site now posting about crypto and supplements, strike (topical drift); DR-25 beauty blogger with high engagement and 6 years in the exact niche, proceed (topical fit + entity strength outweigh DR).

Hand-off: the Tone Matcher launch leads digital PR via SOS/Qwoted on the inclusive-shade angle; r/MakeupAddiction gets 3 months of genuine engagement before any link mention.

### Example 3: Killing the engagement honestly

User: "We have a new site, no content yet, and we want 100 backlinks in 30 days. What's the cheapest way?"

Response (do not soften; the honest answer is the only useful one):
> Stop. This fails for two reasons. 1) No linkable asset: nothing survives qualification, visitors hit a thin site and won't link, and any link that lands decays fast. 2) 100 links in 30 days on a new domain is a textbook link-scheme footprint: best case SpamBrain neutralizes them, worst case a manual action that takes months to recover from.
>
> Two honest paths. Slow (recommended for new domains): publish 3–5 substantial assets first (one a tool, see `seo-tool-discovery`), spend 30 days on reclamation + community presence, earn 5–15 high-fit links in month 1, compound from there. Fast (only if newsworthy): with unique data or a genuine PR hook, run coordinated digital PR via SOS / Qwoted / #JournoRequest; 10–30 quality links in 30 days IS realistic, but it needs a real story, not a request. "100 links" as the goal is the problem; pick a path and run the funnel against it.

## References

- [Google Search Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies) — the authoritative kill-rules
- [Google — Optimizing for generative AI features (May 2026)](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) — inauthentic mentions, fan-out, no llms.txt
- [Backlinko — high quality backlinks](https://backlinko.com/high-quality-backlinks)
- [Ahrefs — turning unlinked mentions into links](https://ahrefs.com/blog/unlinked-mentions/)
- [HARO/Connectively alternatives 2026](https://www.prezly.com/academy/the-best-haro-alternatives)
- [Pew Research — Google users less likely to click links with an AI summary (2025)](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/)
- [Resource page link building — search operators](https://www.clickrank.ai/link-building-search-operators/)
