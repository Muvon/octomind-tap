---
name: marketing-backlink-prospecting
title: "Backlink Prospecting & Qualification — Find Safe Free Places"
description: "Operational funnel for finding and qualifying SAFE free places to place backlinks. Encodes the prospect categories (reclamation, resource pages, broken links, journalist requests, communities, aggregators, niche directories), the per-target qualification rubric (topical fit, real traffic, outbound profile, page context, anchor naturalness, reachability), Google's link-spam guardrails (penalty triggers, rel attribution rules), and the 2026 AI-search citation overlay (Reddit/community as Perplexity/ChatGPT citation sources). Use AFTER niche/audience are clear and BEFORE any outreach. Pairs with marketing-tool-discovery — that one earns links via tools you build; this one places links on properties that already exist."
license: Apache-2.0
compatibility: "Stack-agnostic. Pairs with marketing:seo (off-page strategy), marketing-tool-discovery (passive earning via tools), and content:article / content:blog (the actual outreach copy). Requires websearch and webfetch for prospect discovery and qualification."
domains: marketing content launch
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
---

# Backlink Prospecting & Qualification

## Overview

Most "free backlink" attempts fail in one of two ways: they spray submissions across generic directories and forums (which earn nothing and risk penalties), or they over-rely on a single tactic (only HARO, only guest posts) and stall. This skill is the funnel that prevents both. It organizes free-link opportunities by category and risk profile, encodes a per-target qualification rubric so prospects get manually filtered before any outreach, and bakes in Google's actual link-spam guardrails (March 2026 update — devaluation in minutes, not months) so the work doesn't trigger algorithmic demotion or manual actions.

It pairs with `marketing-tool-discovery` — that skill decides what tool to *build* to earn passive links; this skill decides where to *place* links on properties that already accept them. Use this AFTER the site's niche and audience are clear and BEFORE any outreach email is written. The deliverable is a prioritized prospect list with per-category outreach approach, ready to hand off to `content:article` for the actual copy.

---

## Instructions

### Core Rules

- **Topical relevance is the dominant signal.** Post-2026, DR/DA alone is an obsolete primary filter. A DR-30 site that has lived in your exact vertical for 5 years outranks a DR-80 generalist link farm in real value. Always check vertical history before scoring authority.
- **Manual qualification, every prospect.** No batch submission, no automated discovery-to-outreach pipelines. Every link target gets eyeballed against the rubric. Tools that mass-submit to directories are the fastest path to manual action.
- **The intent test.** Ask: would this link exist if SEO didn't exist? If no → it's a violation in waiting. Google's policy treats intent as the dividing line between natural and unnatural.
- **Topical fit beats authority.** A 1 on topical fit is an automatic strike regardless of any other score. Off-topic links from high-DR sites trigger Google's reasonable-surfer discount AND mixed-niche cluster signals.
- **Toxic neighborhood is permanent.** Once a site links to spam (casino/pharma/foreign-language farms), it's contaminated. Do not pursue a link there even if the page itself looks clean. Penalty contagion is real.
- **Velocity matters.** A natural site earns links at a roughly steady rate. Spiking 50 links in a week from a campaign is fine ONCE, on a newsworthy basis. Sustained spike-velocity is the #1 SpamBrain trigger.
- **Anchor diversity is natural.** Branded ("Acme"), URL-only ("acme.com"), and natural-phrase anchors should dominate. Exact-match keyword anchors should be the minority. Outreach you control = always use branded.
- **Community links count, even when nofollow.** Reddit, Stack Exchange, LinkedIn group posts are usually `rel="ugc"` or `nofollow` — but they drive AI-search citations (Reddit = ~40% of LLM citations across major models, 46.7% on Perplexity), brand search volume (which now outranks backlinks as an LLM citation predictor), and direct traffic. Treat them as visibility, not just SEO.
- **Output a hand-off brief, not a verdict.** The deliverable names downstream agents (`content:article` for the email, `marketing:seo` for the strategy review) and what they need.

### The Funnel

#### Stage 1 — Profile the Site

Force concrete answers before generating any prospect list. If unclear, stop and ask.

1. **Niche** — one sentence. Sub-niche if applicable.
2. **Audience** — who visits today? What do they search for?
3. **Existing link profile** — rough count, top referring domains, any past penalty history. (Run `site:[domain]` and check Search Console if accessible.)
4. **Brand mentions** — does the brand get mentioned online already? (Search `"[brand]" -site:[domain]` to surface.)
5. **Linkable assets** — what does the site already publish that's link-worthy? (Original data, tools, comprehensive guides, calculators.) If nothing yet → flag that prospecting will be uphill until at least one asset exists; recommend the `marketing-tool-discovery` skill in parallel.

#### Stage 2 — Generate Prospect Lists by Category (parallel)

PARALLEL-FIRST: fire all category searches simultaneously in ONE block. Don't serialize discovery.

Categories, ordered by risk-adjusted ROI:

##### A. Reclamation (highest ROI, lowest risk)

The site is *already mentioned*; the only step is asking for the link. Conversion rate sits at 30–60% — far higher than any cold tactic.

- **Unlinked brand mentions** — `"[brand]" -site:[your-domain.com]`. Filter for posts that mention the brand in body copy without linking. Highest priority: Tier-1 publications (Forbes, Times, Fortune) — these rarely accept cold outreach for guest posts but will reclaim a link they meant to add.
- **Broken backlinks pointing to your site** — pages that linked to a URL on your site that's now 404. Either restore the URL or 301 it; no outreach needed.
- **Image attribution reclamation** — `Google Images` reverse-search your branded images / charts / screenshots. Sites using them without credit usually add a link when asked.

##### B. Discovery-based (moderate effort, low risk)

You find the page; the page exists to host links to good content.

- **Resource pages** — search operators:
  - `[topic] intitle:resources inurl:resources`
  - `[topic] "useful resources"`
  - `[topic] "recommended links" OR "useful links"`
  - `[topic] "best [tools/blogs/guides]" 2026`
- **Broken link building** — find resource pages and roundups in your niche, check outbound links for 404s (use a free broken-link checker on the page), pitch your URL as the replacement.
- **Niche aggregators / submission sites** — Hacker News (for tech), Product Hunt (for products), Indie Hackers, Designer News, Lobsters, niche subreddits. Submission usually nofollow but drives traffic + brand mentions.
- **Industry-specific directories** — directories curated by humans for one vertical (e.g. SaaS directories, lawyer directories per jurisdiction, dev-tool catalogs). NOT generic web directories.
- **Best-of lists ("listicles")** — `[topic] "best [thing]" 2026 OR 2025`. Email the author with a fit case for inclusion.

##### C. Earned via outreach (high effort, highest authority)

You're contributing original value; the link is the byproduct.

- **Journalist requests / digital PR** (HARO replacements, post Dec-2024 shutdown):
  - **Source of Sources (SOS)** — Peter Shankman (original HARO creator) — honor system, off-topic pitch = ban. Free.
  - **Featured.com** — relaunched HARO brand, free daily newsletter. More selective than original HARO.
  - **Qwoted** — expertise-profile matching, journalists post queries.
  - **#JournoRequest** and **#PRRequest** on X — direct, no platform.
  - Best results: work 2–3 platforms simultaneously.
- **Guest posts** — operators:
  - `[topic] intitle:"write for us"`
  - `[topic] "submit a guest post"`
  - `[topic] "contributor guidelines"`
  - **Strict filter:** never pay; never accept a flat fee structure; only pursue when the site shows editorial review (named editor, rejection rate, masthead). Paid-without-rel-sponsored = penalty.
- **Podcast / interview pages** — `[topic] inurl:interview OR inurl:podcast`. Pitch yourself as a guest; episode pages link to your site.
- **Original research → outreach** — if the site has produced unique data (survey, benchmark, study), pitch the research to journalists in the niche. Single research report: 22+ links is realistic.

##### D. Community (high effort, AI-citation value, mostly nofollow)

Links here are usually `rel="ugc"` or nofollow — but they're now load-bearing for LLM citation visibility.

- **Reddit** (highest LLM-citation weight) — find on-topic subreddits via `site:reddit.com [topic] [pain point]`. Engage genuinely; link only when it adds value AND the subreddit allows. Most subreddits ban self-promotion; respect the rules or get banned.
- **Stack Exchange** (technical) — answer questions in your area; link as supporting reference.
- **LinkedIn groups, niche forums, Discord/Slack communities** — long-form engagement, not link-drop hit-and-run. Build a 3-month presence before any link.
- **Niche Q&A sites** — Quora, vertical Q&A platforms.

##### E. Profile / listing (low effort, modest value, legitimate when niche-fit)

- **Industry awards** — submit for "best of" lists in your vertical.
- **Speaker pages** — every conference you speak at has a speaker page that links out.
- **GitHub README cross-references** — for technical/dev sites, getting referenced from a popular repo's README compounds.
- **Wikipedia citations** — high bar; only pursue if you have a genuinely citable original source. Don't add the link yourself; let an editor decide.
- **About / partnership pages** — vendor partner directories, customer testimonial pages on tools you use.

##### F. Forbidden (kill on sight, no exceptions)

- Generic web directories (DMOZ-clones, "submit URL" sites)
- Foreign-language link farms (regardless of how cheap)
- Comment spam (any optimized-anchor comment)
- Forum signature link farms with optimized anchors
- "Write for us" pages that accept any topic for a flat fee without `rel="sponsored"`
- PBNs of any tier (including AI-content PBNs — March 2026 update specifically targets these)
- Paid-link networks disguised as guest-post networks
- Reciprocal-link schemes ("we link, you link" en masse)
- Auto-generated content sites
- Casino / pharma / porn / sketchy-finance neighborhoods (unless that *is* your niche)

#### Stage 3 — Qualify Each Prospect (Rubric)

For every prospect, walk this checklist top-to-bottom. STRIKE on the first failure — do not re-score. This is a kill-rule, not a scoring system.

| # | Check | How to verify | Strike condition |
|---|-------|---------------|------------------|
| 1 | **Topical fit** | Read 5 recent articles from the site | Mixed-niche, off-topic, abandoned vertical |
| 2 | **Real traffic** | Similarweb / Ahrefs traffic estimate; manually check engagement (comments, shares) | Bot traffic / no organic / no engagement signals |
| 3 | **Editorial signals** | Author bios with real names; dates; comments; depth | Auto-generated content, plagiarism, no human editor |
| 4 | **Outbound link profile** | Sample 5 outbound links from recent articles | Links to spam neighborhoods, foreign farms, casino |
| 5 | **Indexed and ranking** | `site:[domain]`; check if it ranks for its target keywords | Not indexed; ranks for nothing; deindexation flags |
| 6 | **Page context** | Visit the actual page where your link would land | Buried among 100+ outbound links; pure link page; 30–70 outbound is the sweet spot |
| 7 | **Anchor / rel naturalness** | What anchor will appear? View source or anchor in their template. | Forced exact-match anchor in editorial; rel-stripped paid link |
| 8 | **Reachability** | Find named editor / contact email | Ghost editor, no contact, generic info@ only |
| 9 | **Cost transparency** | Read "write for us" / contact / ad pages | Paid placement passing ranking signal without `rel="sponsored"` |
| 10 | **Penalty history** | Search `"[domain]" + penalty OR deindexed` | Site has documented manual action history |
| 11 | **Velocity contribution** | Where does this link sit in the campaign's overall pace? | Adding this link spikes velocity past natural range |

A prospect that survives all 11 → eligible for outreach. Anything else → skip.

#### Stage 4 — Rank Survivors

Sort by composite score:
- **Topical fit weight:** 3× (most important)
- **Real traffic weight:** 2×
- **Authority signals (DR / DA / TF):** 1× (tie-breaker, not a primary filter)
- **Reachability:** 1× (multiplier — unreachable = score 0)

Top 20% → priority outreach this month. Middle 60% → systematic follow-up over the quarter. Bottom 20% → skip; opportunity cost too high.

#### Stage 5 — Hand-Off Brief

Output one brief in this format. The brief is the deliverable — the emails come from `content:article`.

```markdown
# Backlink Prospecting Brief: [Site / Campaign Name]

## Site Profile
- Niche: [...]
- Audience: [...]
- Existing link profile: [rough DR / referring domains / past penalty notes]
- Brand mentions found: [count + Tier-1 examples]
- Linkable assets identified: [list — flag if thin]

## Prospect Pool by Category

### A. Reclamation (priority — fastest wins)
| Source | Page | Mention/Link Status | Outreach Approach | Tier |
|---|---|---|---|---|
| ... | ... | unlinked mention | direct ask | T1 |

### B. Discovery-based
| Source | Page Type | Topical Fit | Traffic | Outreach Angle | Score |
|---|---|---|---|---|---|

### C. Earned (digital PR / guest posts / podcasts)
| Platform / Publication | Hook | Pitch Angle | Approach | Status |
|---|---|---|---|---|

### D. Community (visibility / AI-citation)
| Platform | Strategy | Cadence | Notes |
|---|---|---|---|
| Reddit r/[sub] | answer-first engagement, no link drops | 3×/week | nofollow but high LLM-citation value |

### E. Listings / profiles
| Directory / List | Submission Process | Cost | Verdict |
|---|---|---|---|

### F. Toxic — explicitly excluded
[List with reason for the strike, so the call is auditable.]

## Outreach Approach Per Category

| Category | Approach | Tone | Hand-off |
|---|---|---|---|
| Resource page | "I noticed your resources page on X. I built [thing] that adds [unique angle]. No worries if it's not a fit." | Brief, value-first | content:article writes the email |
| Broken link | "Your post links to [URL] which is 404. [My replacement] covers the same scope." | Helpful, factual | content:article writes the email |
| Unlinked mention | "Thanks for mentioning [brand]. Could the next edit add a link to [URL]?" | Gracious, low-friction | content:article writes the email |
| HARO/Qwoted/SOS | 75–100 words, lead with credentials, direct expertise, no pitch slap | Editorial, expert-positioned | the agent writes pitches in real time |
| Forum / Reddit | Genuine answer; link only if it adds value | Peer, not promotional | the strategist participates personally |
| Guest post | Pitch a topic the site hasn't covered + your unique data | Editorial, contributor-positioned | content:article + content:blog |

## Velocity Plan
- Target pace: [X new links / month based on baseline]
- Monthly budget by category: [reclamation N, discovery N, earned N, community ongoing]
- Red flags to watch: spike weeks, anchor concentration, sudden DR drop on referring domains

## Hand-Offs
- Outreach copy → `content:article` (with the per-category template above)
- Page-level on-page setup for landing pages → `content:seo`
- Link-worthy asset gap (if profile thin) → `marketing-tool-discovery` skill
- Tracking instrumentation → developer:[stack]
```

### Decision Guide — Edge Cases

| Situation | Action |
|---|---|
| Prospect has DR 80 but recent posts are unrelated | **Strike** — topical drift / cross-niche farm |
| "Write for us" accepts any topic, fee $50, no `rel="sponsored"` | **Strike** — paid editorial without disclosure = penalty risk |
| On-topic forum thread, 4 days old, active | **Engage** — answer first, link only if it adds value |
| Site looks legit, no organic traffic per Similarweb | **Investigate** — could be brand-new (OK) or dead (skip). Check whois date + Wayback. |
| Resource page with 200+ outbound links | **Skip** — link will be buried |
| Reciprocal request: "we'll add you if you add us" | **Case-by-case** — once between two niche-relevant sites is OK; mass exchange = no |
| Site has documented manual penalty history | **Strike** — penalty contagion |
| Aggregator wants `rel="dofollow"` link in exchange for fee | **Strike** — paid editorial without `rel="sponsored"` |
| Reddit subreddit bans self-promotion | **Engage without linking** — visibility-only contribution; link in profile only |
| Tier-1 publication mentions brand without link | **High priority** — these rarely accept cold outreach for anything else |
| Unsure if site is a PBN | **Default skip** — uncertainty alone is a strike. Footer disclosures, identical templates, single hosting IP, identical author across "different" sites = PBN tells. |
| User wants to do mass directory submission | **Refuse and explain** — March 2026 update specifically targets this pattern |
| AI-search visibility is the priority, not rank | **Pivot** — weight community (Reddit, Stack Exchange) and brand-mention reclamation higher than traditional backlinks |

### Google's Link-Spam Policy — the hard lines

These are direct from Google's spam policy. Treat as kill-rules, not guidelines.

- **"Exchanging money for links, or posts that contain links"** — without `rel="sponsored"` is a violation
- **"Exchanging goods or services for links"** — same as above
- **"Using automated programs or services to create links"** — auto-submission = violation
- **"Requiring a link as part of a Terms of Service, contract, or similar arrangement"** — forced linking = violation
- **"Advertorials or native advertising where payment is received for articles that include links that pass ranking credit"** — paid editorial without rel = violation
- **"Low-quality directory or bookmark site links"** — generic directories = violation
- **"Forum comments with optimized links in the post or signature"** — keyword-anchor signature spam = violation
- **"Excessive reciprocal link exchanges without genuine partnership value"** — link swap networks = violation

What's *allowed*:
- Paid links with `rel="sponsored"` or `rel="nofollow"` — Google is explicit: "It's not a violation of our policies to have such links as long as they are qualified."
- User-generated content links with `rel="ugc"` (forums, comments)
- Genuine editorial endorsement
- Sponsorships / advertising disclosed and properly attributed

### AI-Search Citation Overlay (2026)

Traditional backlinks are no longer the dominant predictor of LLM citation. The shift:

- **Reddit** = ~40% of citations across major LLMs, 46.7% on Perplexity. Subreddit presence is a primary GEO/AEO signal.
- **ChatGPT** favors Wikipedia (47.9% of top citations) and encyclopedic content.
- **Google AI Overviews** cite YouTube + multimodal heavily (23.3%).
- **Brand search volume** outweighs traditional backlinks as an LLM citation predictor.
- **Citation volatility** is now measured in *weeks* — a single algorithm tweak can shift citation share 50% in under a month.

**Implication for prospecting:** the deliverable should be reframed as *visibility prospecting*, not pure link acquisition. Weight community engagement (Reddit, Stack Exchange) higher when AI-search visibility is the goal — even though those links are usually nofollow/ugc, they directly drive citation share. For pure organic-rank goals, traditional backlinks still dominate; for omnichannel visibility (search + AI), both lanes matter.

### Tools — what's free and what isn't

| Tool | Free tier scope | Use for |
|---|---|---|
| Google Search Console | Free | Existing backlinks, manual actions, indexing |
| Google Search (with operators) | Free | Prospect discovery |
| Wayback Machine | Free | Confirming a site's longevity / topical history |
| Bing Webmaster Tools | Free | Backlink data, sometimes shows links Ahrefs misses |
| `site:` + manual review | Free | Outbound link profile audit |
| Ahrefs Free Backlink Checker | Free (limited) | Top 100 backlinks of any domain |
| Moz Link Explorer (free) | Free (limited) | DA / spam score samples |
| Ubersuggest free | Free (limited) | DR estimates |
| Source of Sources / SOS | Free | Journalist requests |
| Featured.com | Free newsletter | Journalist requests |
| Qwoted | Freemium | Journalist requests |
| Reddit / Stack Exchange | Free | Community prospecting |
| Hunter.io / Apollo (limited free) | Freemium | Editor email discovery |

Tools that require payment for what matters (full backlink graphs, advanced filters): Ahrefs, Semrush, Majestic. Mention but treat as out-of-scope for "free" prospecting.

---

## Examples

### Example 1: Dev-tools SaaS (CI/CD pipeline)

**Profile:**
- Niche: CI/CD pipeline tool, target audience platform engineers at 50–500-person eng orgs
- Audience: searches for "deploy faster", "GitHub Actions alternative", "monorepo CI"
- Existing link profile: ~80 referring domains, mostly developer blogs and Hacker News submissions
- Brand mentions found: 12 unlinked mentions on dev blogs, 1 in InfoQ (Tier-1)
- Linkable assets: 3 deep technical guides, 1 benchmark report

**Stage 2 prospect generation (parallel):**

Fired in one block:
- `intitle:"resources" CI/CD platform engineering`
- `"GitHub Actions alternative" "best" 2025 OR 2026`
- `site:reddit.com r/devops "monorepo CI"`
- `"acme-deploy" -site:acmedeploy.com` (unlinked mentions)
- `intitle:"write for us" devops OR platform-engineering`
- `intitle:interview "CI/CD" 2025 OR 2026`
- Hacker News + Lobsters submission queue history

**Stage 3 qualification (sample):**

| Prospect | T-fit | Traffic | Editorial | Outbound | Indexed | Page Ctx | Anchor | Reach | Cost | Penalty | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| InfoQ unlinked mention | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | free | clean | **Priority 1** |
| dev-blog-X guest post | ✅ | ⚠️ low | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | free | clean | proceed |
| "Best CI tools 2026" listicle on monetized site | ✅ | ✅ | ✅ | ⚠️ paid placements | ✅ | ✅ | ⚠️ exact-match in editorial | ✅ | $300/year | clean | **Strike** (paid editorial, no `rel="sponsored"`) |
| r/devops AMA opportunity | ✅ | ✅ | n/a | n/a | n/a | n/a | nofollow | self | free | clean | **Engage** (AI-citation play) |
| dev-tools-directory.net | ⚠️ generic | ⚠️ low | ❌ auto-content | ❌ links to casino | ❌ | n/a | n/a | n/a | $50 | flagged | **Strike** (toxic neighborhood + paid + auto-content) |

**Output:** 14 priority prospects, ranked, with outreach approach per category. Hand-off to `content:article` for outreach copy.

### Example 2: Cosmetics e-commerce (continuing the prior skill's example)

**Profile:**
- Niche: inclusive shade-range foundation e-commerce
- Audience: women 25–45, primary search "foundation for [skin tone]"
- Brand mentions: 8 unlinked, mostly beauty bloggers
- Linkable assets: SKU database with hex codes (proprietary moat); the Tone Matcher tool (just built per the previous skill)

**Stage 2 prospects (parallel):**

- `"foundation for [skin tone]" "best" 2025 OR 2026`
- `intitle:"resources" inclusive beauty`
- `site:reddit.com r/MakeupAddiction "foundation match"`
- `"acmebeauty" -site:acmebeauty.com`
- HARO: beauty/lifestyle journalist requests
- Beauty-specific directories (Beauty Independent, etc.)
- Speaker pages from inclusive-beauty conferences

**Notable strikes:**
- Generic beauty directory accepting any submission for $20 → strike (low-quality directory pattern)
- "Best foundations" listicle on a site whose recent posts are about crypto and supplements → strike (topical drift)
- Beauty blogger with DR 25 but high engagement, 6-year history in the exact niche → **proceed** (DR low but topical fit + entity strength outweigh)

**Hand-off:** the Tone Matcher tool launch becomes the lead asset for digital PR — pitches go out via SOS/Qwoted naming the inclusive-shade angle. Reddit r/MakeupAddiction sees genuine engagement pre-launch (3 months) before any link mention.

### Example 3: Killing the engagement honestly

User: "We have a new site, no content yet, and we want 100 backlinks in 30 days. What's the cheapest way?"

**Response:**
> Stop. There are two reasons this fails before it starts:
>
> 1. **No linkable asset.** With no published content, there's nothing to link TO that survives qualification. Any prospect who clicks through hits a thin site and won't link. Even if they do, the link decays fast — Google sees the destination is empty.
>
> 2. **100 links in 30 days on a new domain is the textbook SpamBrain trigger.** That velocity is what the March 2026 spam update specifically devalues. Best case: links earn nothing. Worst case: manual action that takes 3–6 months to recover from.
>
> Two honest paths:
>
> - **Slow path (recommended for new domains):** publish 3–5 substantial assets first (one of them a tool, see `marketing-tool-discovery`). Spend 30 days building reclamation + community presence. Earn 5–15 high-fit links in month 1. Compound from there.
> - **Fast path (only if newsworthy):** if you have unique data or a genuine PR hook, do a coordinated digital PR push via SOS / Qwoted / #JournoRequest. 10–30 high-quality links in 30 days IS realistic, but the prerequisite is a real story, not a request.
>
> 100 links in 30 days as the goal itself is the problem. Pick one of the two paths above and the prospecting funnel runs against that goal instead.

Do not soften. The honest answer is the only useful one.

---

## References

- [Google Search Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies) — the authoritative kill-rules
- [Google's Backlink Policy in 2026 — what's now enforced](https://bluetree.digital/google-backlink-policy/)
- [Backlinko — high quality backlinks](https://backlinko.com/high-quality-backlinks)
- [Ahrefs — turning unlinked mentions into links](https://ahrefs.com/blog/unlinked-mentions/)
- [HARO/Connectively alternatives 2026](https://www.prezly.com/academy/the-best-haro-alternatives)
- [AI Platform Citation Source Index 2026 — 5W](https://www.prnewswire.com/news-releases/5w-releases-ai-platform-citation-source-index-2026-the-50-websites-that-now-decide-what-brands-are-visible-inside-chatgpt-claude-perplexity-gemini-and-google-ai-overviews-302759804.html)
- [Reddit's role in AI citations](https://techedgeai.com/ai-platform-citation-source-index-2026-shows-reddits-surge-and-a-new-era-of-volatile-ai-generated-answers/)
- [Resource page link building — search operators](https://www.clickrank.ai/link-building-search-operators/)
- Companion skill: `marketing-tool-discovery` — earning passive links by building free tools
- Companion agent: `marketing:seo` — runs this skill as part of off-page strategy
- Hand-off agents: `content:article` (outreach copy), `content:seo` (on-page wrapper), `developer:*` (tracking)
