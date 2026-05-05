---
name: marketing-tool-discovery
title: "Free-Tool Discovery for Backlinks & Traffic"
description: "Validation funnel for deciding WHICH free tool to build for backlinks, embeds, and AI-search citation. Encodes the data-moat-first methodology: niche-fit gate, data inventory, 5-candidate scoring across niche/moat/SEO/feasibility/monetization, alignment checklist, and hand-off brief that names the downstream build agent. Use BEFORE any tool-build work to avoid building commodity tools that earn nothing. Skip if the user has already validated the concept and just wants to build."
license: Apache-2.0
compatibility: "Stack-agnostic. Pairs with marketing:seo (off-page strategy) and the developer:* agents (build hand-off). Requires websearch and webfetch for competitor and SERP scans."
domains: marketing content launch
rules:
  - session(seo)
  - content(backlink)
  - content(backlinks)
  - content(free tool)
  - content(free tools)
  - match(\bbuild\s+a\s+(free\s+)?tool\b)
  - match(\btool\s+for\s+(seo|backlinks|traffic|leads)\b)
  - match(\b(seo|backlink)\s+tool\s+ide(a|as)\b)
  - match(\blink[\s-]?bait\b)
  - match(\bembed\s+(widget|tool|calculator)\b)
  - match(\blink\s+magnet\b)
  - semantic(what free tool should we build to drive backlinks)
  - semantic(linkable asset idea to attract organic links)
  - semantic(interactive calculator or widget to earn traffic)
  - semantic(build something free that other sites will embed or link to)
---

# Free-Tool Discovery for Backlinks & Traffic

## Overview

Most free tools built for SEO fail because they're picked by gut, not by a gate. They duplicate something Lorem-Ipsum-generic, run on commodity data, drift outside the site's niche, or have no monetization path — so even when they get traffic, they don't earn links and don't move revenue. This skill encodes the discovery funnel that prevents that: a niche-fit + data-moat gate that kills 80% of bad ideas before any build effort, a 5-candidate scoring rubric that ranks survivors, and a hand-off format that names the downstream build agent so nothing falls between roles.

Use this skill BEFORE any tool-build work. Skip it if the user has already validated their concept and just wants to ship.

---

## Instructions

### Core Rules

- **The data moat decides everything.** A tool without proprietary or hard-to-replicate data is a commodity. Commodity tools earn no durable links — competitors clone them in a day. If no moat, kill the idea even if everything else looks good.
- **Niche fit is non-negotiable.** A "useful" tool that doesn't serve the site's existing audience earns off-topic links that Google discounts. Cosmetics site → skin-tone matcher YES, SEO checker NO.
- **80/20 the planning.** 80% of the value of this skill is in idea selection (niche fit + data moat). Building is downstream. Do not let users skip the gate to "just start building."
- **Five candidates, not one.** Single-idea brainstorms anchor to whatever came first. Always generate five and rank — even if four are obvious dead ends, the comparison clarifies why the survivor wins.
- **Output a hand-off, not a verdict.** The skill's deliverable is a brief that names the downstream build agent (`developer:typescript`, `developer:svelte`, etc.) and what they need from the data source. A "good idea" with no hand-off is not done.
- **Compound over spike.** Prefer tools that keep earning links for years (calculators on durable data, embed widgets) over tools tied to a news cycle.

### The Funnel

#### Stage 1 — Gatekeeping Questions (kill or proceed)

Before anything else, force two answers from the user. If either is "no" or "unclear," stop and ask. Do not proceed to candidate generation.

1. **Niche question:** "What is the site's niche, in one sentence? Who exactly visits today?"
2. **Data question:** "What data do you already own or can ingest cheaply? List concretely."

Examples of valid data sources:
- Product or service specifications (catalogs, SKUs, configurations)
- Blog post / article databases (your content corpus)
- Public APIs you can hit affordably (price feeds, weather, gov data, sports stats)
- Proprietary metrics (your own benchmarks, performance data, conversion stats)
- Customer datasets (anonymized usage data, survey results)
- Community-generated content (reviews, ratings, comments — with rights)

If the user can't name concrete data, kill the engagement: "Without a data source you own or can ingest cheaply, every tool you build will be commodity. Come back when you have at least one of these." Do not soften this.

#### Stage 2 — Generate 5 Candidates

Brainstorm exactly five candidate tools that:
- Use one or more of the user's named data sources
- Solve a problem the user's existing audience actually has
- Could plausibly be embedded, shared, or cited

Write each as one sentence: `[Tool name] — [what it does] — [data it uses]`.

Example for a GPU benchmark site:
1. **GPU Compatibility Matrix** — checks if a GPU fits a given motherboard/case/PSU — uses spec database
2. **FPS Estimator** — predicts FPS for game × GPU × resolution — uses benchmark database
3. **Upgrade ROI Calculator** — shows cost-per-FPS gained for an upgrade — uses spec + benchmark + price data
4. **Power Draw Estimator** — calculates total system wattage needed — uses spec database
5. **GPU Generation Timeline** — visualizes performance gains across generations — uses benchmark database

#### Stage 3 — Score Each Candidate Across 5 Dimensions

Score 1–5 (1 = bad, 5 = excellent) on each dimension. Total a candidate by summing — but a single 1 in `data_moat` or `niche_fit` is a kill regardless of total.

| Dimension | What 5 looks like | What 1 looks like |
|---|---|---|
| **Niche fit** | The site's exact audience uses this monthly | The audience would never search for this |
| **Data moat** | Built on proprietary data competitors can't easily replicate | Built on data anyone can scrape in a day |
| **SEO signals** | Sticky (3–5 min dwell), produces shareable outputs, AI-citable answers, natural embed hook | Static result, nothing to embed, no citation hook |
| **Feasibility** | Mostly client-side, ships in days | Months of backend, infrastructure-heavy |
| **Monetization path** | Clear path to email capture / affiliate / paid upgrade / sponsorship | No revenue connection at all |

A score of 1 on niche_fit OR data_moat → strike the candidate. No exceptions.

#### Stage 4 — Alignment Checklist (final gate on the top candidate)

Before recommending the highest-scoring candidate, run it through:

- [ ] **Audience match** — does this solve a problem the site's existing visitors face?
- [ ] **Brand fit** — would the site's customers expect them to build this? (Yes = free credibility. No = build credibility before launching.)
- [ ] **Competitive moat** — would a competitor need the user's specific data/position to replicate, or could they build it in a week?
- [ ] **Longevity** — will this tool still be relevant in 2 years, or is it a trend rider?

A "no" on any of these is not an automatic kill — but every "no" must be acknowledged in the hand-off brief with mitigation.

#### Stage 5 — Hand-Off Brief

Output a single brief in the format below. This is the deliverable.

```markdown
# Free Tool Brief: [Tool Name]

## Niche Fit
[One paragraph. Who the tool serves and why this matches the site's existing audience.]

## Data Moat
[One paragraph. The proprietary/exclusive data this runs on. Why competitors can't replicate cheaply.]

## SEO Signals
- Expected dwell time: [estimate, with reasoning]
- Embed opportunity: [yes/no — which publishers would embed and why]
- AI citation potential: [yes/no — does it produce extractable, citable answers? FAQ/structured-output formats?]
- Backlink hook: [the natural reason a journalist or blogger would link]
- Shareability: [does it produce a result users want to share? screenshot? badge?]

## Feasibility
- Mostly client-side? [yes/no]
- Data ingestion needs: [one-time / periodic / live]
- External APIs needed: [list, with cost notes]
- Estimated build effort: [days/weeks]

## Monetization Path
[How the tool feeds the funnel — email capture, affiliate clicks, paid upsell, sponsorship slots, lead gen.]

## Alignment Notes
- Audience match: [✅/⚠️ + note]
- Brand fit: [✅/⚠️ + note]
- Competitive moat: [✅/⚠️ + note]
- Longevity: [✅/⚠️ + note]

## Build Hand-Off
- **Build agent:** `developer:[language]` (e.g. developer:typescript, developer:svelte)
- **Stack hint:** [Svelte / Next / static HTML / Astro — based on feasibility]
- **Data source:** [exact source the build agent needs access to]
- **On-page wrapper:** route to `content:seo` for the page copy + meta + schema
- **Launch content:** route to `content:article` for the launch post / press hook
- **Tracking:** [what events to instrument — embed loads, completions, email captures]
```

### Decision Guide — common cases

| Situation | Action |
|---|---|
| User has no clear data source | Kill the engagement at Stage 1. No moat = no point. |
| User has data but it's also publicly available | Ask what their version adds (curation, structure, freshness). If nothing, kill. |
| Two candidates tie on score | Pick the one with the stronger embed hook (compounds harder over time). |
| Top candidate fails brand fit only | Acceptable IF the user is willing to build credibility first (1–2 supporting blog posts before tool launch). Note in mitigation. |
| User pushes "let's just start building" before scoring | Hold the line. The whole point of this skill is to refuse premature build. |
| User's niche is too broad to assess | Force a narrowing question: "Which sub-niche is the priority for the next 6 months?" |

---

## Examples

### Example 1: Cosmetics e-commerce site

**Stage 1 inputs:**
- Niche: mid-tier cosmetics e-commerce, focused on inclusive shade ranges for foundations
- Data: SKU database (3,400 products with hex codes + undertone tags), customer purchase history, returns reasons

**Stage 2 candidates:**
1. Skin-Tone-to-Foundation Matcher — uploads selfie or picks tone, returns matching SKUs — uses SKU database
2. Lorem Ipsum for Beauty Copy — generic placeholder text — none
3. Foundation Coverage Comparison — side-by-side coverage levels — uses SKU database
4. Return-Reason Stats Dashboard — public stats on which products are returned and why — uses returns data
5. SEO Keyword Tool for Beauty Brands — generic SEO checker — none

**Stage 3 scores:**
| Candidate | Niche | Moat | SEO | Feas | Monet | Total | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Tone Matcher | 5 | 5 | 5 | 4 | 5 | **24** | ✅ |
| 2. Lorem Ipsum | 1 | 1 | 1 | 5 | 1 | 9 | ❌ kill (niche=1, moat=1) |
| 3. Coverage Compare | 5 | 4 | 4 | 4 | 4 | 21 | possible |
| 4. Returns Dashboard | 4 | 5 | 4 | 3 | 2 | 18 | privacy risk + weak monet |
| 5. SEO Keyword Tool | 1 | 1 | 3 | 3 | 2 | 10 | ❌ kill (niche=1) |

**Stage 4 — Tone Matcher alignment:**
- Audience match ✅ — exact pain point of every shopper
- Brand fit ✅ — site is already known for shade range
- Competitive moat ✅ — matcher accuracy depends on the SKU undertone tags (proprietary)
- Longevity ✅ — foundation matching is a permanent problem

**Stage 5 — Hand-off brief:** (would be written using the template above, naming `developer:svelte` for client-side image processing)

### Example 2: Engineering blog with no data

**Stage 1 inputs:**
- Niche: engineering blog covering distributed systems
- Data: 47 published blog posts, no databases, no APIs, no proprietary metrics

**Action:** Kill at Stage 1.

> "47 blog posts is content, not a tool data source. Building a tool here means building on commodity APIs (GitHub, Stack Overflow) — which means competitors can clone it in a weekend and your moat is zero. Two paths forward:
> 1. Build a data set FIRST. Run benchmarks, scrape your own corpus, run a community survey. Come back when you have something exclusive.
> 2. Skip free tools. Earn links via original research posts and digital PR — that plays to what you do have (writing). Different lever, no tool needed."

Do not soften, do not propose a tool anyway. The honest answer is the only useful one.

### Example 3: User pushes to skip the funnel

User: "I already know I want to build a salary calculator for tech jobs. Just help me design it."

**Response:**
> "Before I hand off to a build agent, two questions — these are the same gates the funnel runs and they're 30 seconds:
> 1. What salary data are you using? (Public scraped Glassdoor data has no moat — Levels.fyi already won that. Proprietary survey, payroll-anonymized, or company-disclosed data is a different game.)
> 2. Who's your existing audience and do they search for salary info? (If you're a dev-tools blog, salary data isn't your niche — links from HR sites won't compound your dev-tools rankings.)
>
> If both pass, I'll write the brief and hand off. If either fails, we change the tool — not skip the questions."

---

## References

- Original article framework: [How to build free tools with Claude Code for backlinks](https://www.madebyagents.com/blog/how-to-build-free-tools-with-claude-code-for-backlinks)
- Eugene Schwartz, *Breakthrough Advertising* — for awareness-stage matching when picking the tool's positioning
- Companion agent: `marketing:seo` — runs this skill as part of off-page strategy
- Companion agent: `content:seo` — receives the hand-off for on-page copy, meta, schema
- Build agents: `developer:typescript`, `developer:svelte`, `developer:python` — receive the build hand-off
