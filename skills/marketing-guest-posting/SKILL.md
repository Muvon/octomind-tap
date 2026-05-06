---
name: marketing-guest-posting
title: "Guest Posting — Editorial Pitches & Safe Link Strategy"
description: "Operational skill for landing genuine editorial guest posts that earn high-quality contextual links without triggering the Oct-2025 spam update on guest-post farms. Encodes the 7-stage workflow (author tier-mapping, discovery operators, 11-point site qualification, content-gap topic ideation, 80–150-word pitch architecture, post writing standards by tier, internal-link strategy, anchor distribution, follow-up). Bakes in Google's hard kill-rules (paid networks, repetitive exact-match anchors, duplicate content, AI-content farms), the data-backed anchor distribution (40-50% branded, <10% exact-match, 68% penalty reduction with diversification), and link-placement rules (1-2 contextual body + 1 bio = 387% more referral traffic than bio-only). Use BEFORE writing any pitch. Stays in the marketing lane: produces strategy, target list, topics, pitch brief — does not write the email or post itself."
license: Apache-2.0
compatibility: "Stack-agnostic. Requires websearch and webfetch for discovery and qualification."
domains: marketing
rules:
  - session(seo)
  - content(guest post)
  - content(guest posting)
  - content(guest blog)
  - content(guest blogging)
  - content(write for us)
  - match(\bguest[\s-]?(post|posting|blog|blogging|blogger|author)\w*)
  - match(\bcontribut(or|ing|ion)s?\s+(post|article|writer|guidelines?)\b)
  - match(\bwrite\s+for\s+(us|me|us\?)\b)
  - match(\bbylined?\s+(article|piece|post|content)\b)
  - match(\bniche\s+edits?\b)
  - match(\blink\s+insertions?\b)
  - semantic(how do we land guest posts on industry blogs)
  - semantic(pitch articles to other publications for backlinks)
  - semantic(write for other blogs to get authoritative links)
  - semantic(strategy for getting accepted as a guest author)
  - semantic(find blogs that accept contributor articles)
---

# Guest Posting

## Overview

Guest posting still works in 2026 — but the rules changed sharply. The October 2025 Google spam update added "AI-generated guest post farms" as a distinct violation category, targeting large-scale operations that publish thin machine content to embed paid backlinks. Volume is now actively penalized. Repetitive exact-match anchors across posts trigger manual review. "Niche edits" sold as guest-post alternatives carry the same penalty as paid guest posts. The tactic survives only when each post is editorially earned, topically aligned, written to publication standard, and linked back with diverse natural anchors.

This skill encodes the 7-stage workflow for doing exactly that: map your authority to publication tiers, discover qualified targets, qualify each one against an 11-point rubric, pitch a specific content gap (not "a guest post"), write to the host's standard, link strategically without over-optimizing, and follow up to build a multi-post relationship. Use BEFORE writing any pitch email. The deliverable is a strategy + brief; orchestration of downstream copywriting belongs to the agent layer, not this skill.

---

## Instructions

### Core Rules

- **Pitch a content gap, not "a guest post."** Editors get 50+ generic guest-post pitches per week and delete them in seconds. The pitches that get accepted name a specific topic the publication should already have covered and offer to fill it. The phrase "I'd love to contribute a guest post" is the kiss of death.
- **Match your authority to the publication tier.** Pitching tier-1 with no portfolio is a waste — they want named expertise and prior tier-1 placements. Start where you are; build up. The tier-mapping step (Stage 1) is non-negotiable.
- **Anchor diversification is data-backed, not a vibe.** 40-50% branded, 20-30% partial-match, 15-25% semantic/long-tail, 5-10% generic, <10% exact-match. Diversification reduces manual-action risk by 68%. Track distribution across all guest posts placed.
- **2–4 posts/month is the cadence ceiling.** More than that triggers velocity-pattern detection. Quality beats quantity now in a way that wasn't true 3 years ago.
- **Body links beat bio links.** 1-2 contextual body links + 1 author bio link is the safe default. Body placement generates up to 387% more referral traffic than bio-only. The link must genuinely help the reader at that exact point — if it doesn't, drop it.
- **Never pay for a guest post placement that passes ranking signal.** Paid + no `rel="sponsored"` = penalty. "Vetted networks" charging $200-500 per placement are usually disguised PBNs. Real editorial requires real outreach.
- **Each post must be unique.** Duplicate content across publications is its own violation category. Re-pitching the same topic to multiple sites = OK only if each post is independently written.
- **One pitch, one topic-set.** Don't blast the same 3-topic pitch to 50 sites. Each pitch is researched per-publication, references their actual content, fills a specific gap they have.
- **AI-written drafts are detectable and devalued.** The Oct 2025 update specifically targets thin AI content farms. Use AI for outlining/research support if needed, but ship human-written prose at publication standard.
- **Output a brief, not a finished email.** This skill produces the strategy, target list, topics, and pitch architecture. The actual email and post writing happen elsewhere — stay in the marketing lane.

---

### The 7-Stage Workflow

#### Stage 1 — Tier-Mapping (where YOU can realistically pitch)

Before discovering any target, force the user to honestly map their authority. Pitching above your tier is the #1 cause of pitch failure.

**Author Authority Inventory:**
1. **Prior published work** — list it. URLs, publication, date.
2. **Named expertise** — credentials, role, years in the field, specific niche depth.
3. **Original assets** — proprietary data, original research, named tools, signature frameworks.
4. **Social proof** — speaking engagements, podcast appearances, citations, follower count if relevant.
5. **Domain you'd link from** — the brand/site doing the pitching. Its DR, niche relevance, recognizable name.

**Tier Mapping:**

| Tier | Examples | Author Requirement | Realistic Acceptance |
|---|---|---|---|
| **T1 — Top-tier** | TechCrunch, Forbes, Inc., HBR, Fast Company, Wired, Search Engine Journal, Smashing Magazine | Senior named expert, prior tier-1 placements, specific original data or contrarian framing | <5% even with strong portfolio |
| **T2 — Industry authority** | Top 5–20 publications in a vertical (Ahrefs blog, Moz, GitHub blog, Cloudflare blog, etc.) | Demonstrable expertise, 3+ tier-2/3 placements, original case study or technical depth | 10–20% with strong portfolio |
| **T3 — Niche publication** | Specialized blogs DR 30–60, active editor, 5k–50k organic monthly | Some demonstrable expertise, 1+ prior placement OR exceptional pitch | 30–50% |
| **T4 — Emerging blog** | DR 10–30, smaller audience but on-topic, owner-edited | Genuine domain knowledge | 60–80% |

**The honest rule:** if the user has zero prior placements, START at T4, ladder up. Trying to land a tier-1 pitch with no portfolio wastes 4 weeks and generates a pile of unanswered emails.

**Output of Stage 1:** a written tier mandate. Example: "Author has 2 T3 placements + proprietary benchmark data. Realistic mandate: T2 (stretch) and T3 (core), no T1 attempts this quarter."

#### Stage 2 — Discovery (operators + competitor reverse-engineering)

PARALLEL-FIRST: fire all discovery searches in ONE block.

**Operator library** (substitute `[topic]` with the niche term):

```
[topic] intitle:"write for us"
[topic] intitle:"write for me"
[topic] intitle:"contribute to"
[topic] intitle:"contributor guidelines"
[topic] inurl:/guest-post/
[topic] inurl:write-for-us
[topic] inurl:contribute
[topic] "submit a guest post"
[topic] "submit an article"
[topic] "now accepting guest posts"
[topic] "guest writer wanted"
[topic] "become a contributor"
[topic] ("write for us" OR "guest post" OR "contribute" OR "submit")
```

**Competitor reverse-engineering** (the highest-yield discovery method):
- Take a competitor URL → free Ahrefs Backlink Checker → top 100 referring domains
- Filter referring page URL or anchor text for "guest", "contributor", "by [author name]"
- Each hit is a publication that already publishes content in your niche AND accepts outside contributions

**Topic-research / content-gap tools:**
- For each candidate publication, identify topics in your niche they haven't covered (use site search + keyword gap analysis if available)
- This becomes raw material for Stage 4 (topic ideation)

**Niche-specific operator variants:**

| Niche | Add-on operator |
|---|---|
| SaaS / dev tools | `intitle:"engineering blog" + "guest"` |
| E-commerce | `intitle:"contributor" + "ecommerce"` |
| Finance | `intitle:"contributor" + "finance"` (caution: YMYL — higher editorial bar) |
| Marketing/SEO | `intitle:"write for us" + "marketing"` |
| Local services | `[city] [niche] intitle:"contribute"` |

**Pitfall:** "Write for us" pages openly advertised attract paid networks. The highest-quality publications often DON'T have "write for us" pages — discovery there requires competitor reverse-engineering and direct editor relationships, not operator searches.

#### Stage 3 — Qualify Each Target (the 11-point rubric)

Walk top-to-bottom, kill on first failure. This is a kill-rule list, not a score.

| # | Check | How to verify | Strike condition |
|---|-------|---------------|------------------|
| 1 | **Topical fit** | Read 5–10 recent posts | Mixed-niche, off-topic, abandoned vertical |
| 2 | **Real organic traffic** | Similarweb / Ahrefs traffic estimate; check engagement | Bot traffic, no organic, no real readers |
| 3 | **Editorial signals** | Named editors, masthead, rejection rate, response times | Anonymous, no editor, accepts everything |
| 4 | **Indexed and ranking** | `site:[domain]`; check 5 sample posts in SERPs | Not indexed; deindexation history |
| 5 | **Outbound link profile** | Sample 5 outbound links from recent guest posts | Links to spam, casino, foreign farms, PBN tells |
| 6 | **Author diversity** | Sample 10 posts → are authors varied real people? | Same 2–3 authors across "different sites"; PBN tell |
| 7 | **Template uniformity across sites** | Check if multiple "different" sites share template, hosting IP, footer | Network footprint = PBN |
| 8 | **Past-author destinations** | Click on past guest authors' bio links → where do they go? | All link to same handful of domains = paid network |
| 9 | **Cost transparency** | Read "write for us" + contact + ad pages carefully | Paid placement passing ranking signal without `rel="sponsored"` |
| 10 | **Penalty history** | Search `"[domain]" + (penalty OR deindexed OR algorithm)` | Documented manual action / traffic cliff post-update |
| 11 | **Authority match** | Is this tier achievable for the user's portfolio? | Pitching 3+ tiers above realistic mandate |

A prospect that survives all 11 → eligible for pitch. Anything else → skip.

**Network-graph check (for advanced users with paid tools):** if Ahrefs/Semrush show backlinks from this domain "negatively impact" linked sites, that's a hard strike — the site is a known toxic linker.

#### Stage 4 — Topic Ideation (per qualified target)

This is the stage that separates 6% pitch reply rates from 18%. Generic topic offers fail. Specific content-gap offers convert.

**Per-target ideation process:**

1. **Inventory the publication's recent content** — last 30 posts. Group by sub-topic.
2. **Identify the gaps** — what sub-topics in their declared niche are missing or under-covered? What perspectives haven't they shown?
3. **Match to the user's unique assets** — proprietary data, lived experience, technical specialty, contrarian framing.
4. **Generate 3–5 topic candidates** that:
   - Fit the publication's editorial niche exactly
   - Don't duplicate something they ran in the last 6 months
   - Bring something only the user can bring (data, case study, technical depth)
   - Match a known search-intent pattern in the niche (keyword research, if needed, is handled outside this skill)
5. **Pre-write the value proposition** — for each topic, one sentence on why their audience needs this.

**Topic angles that work:**

| Angle | Description | Example |
|---|---|---|
| **Original data** | Survey, benchmark, internal metrics from your operation | "We analyzed 40,000 deploy logs — here's what slow CI actually costs" |
| **Specific case study** | One company, one problem, the numbered process and outcome | "How we reduced page-weight 73% on a 10M-page site (the 4 changes that mattered)" |
| **Technical contrarian** | Disagree with conventional wisdom, with evidence | "Why we stopped using [popular tool] after 3 years — and what we ship instead" |
| **Underserved sub-topic** | A niche the publication's audience cares about but coverage is thin | "Building accessible forms in Svelte 5 — runes-era patterns" |
| **Process post** | Step-by-step on something readers struggle with | "Setting up multi-region failover on Cloudflare Workers, end to end" |
| **Tool/framework deep-dive** | Honest evaluation of something their audience uses | "30-day report from migrating from Postgres to Neon" |

**Topic angles that fail:**
- Generic listicles ("10 ways to improve your SEO")
- Broad topics already covered ("What is content marketing?")
- Topics that promote your product (editors smell this in 5 seconds)
- "Trends in [niche] for 2026" pieces (every publication has 5 of these)
- Anything resembling a pitch deck

**Output of Stage 4:** for each qualified target, 3–5 specific topic offers, each one sentence + a value prop.

#### Stage 5 — Pitch Architecture (the 80–150-word email)

Pitch performance data:
- Personalized pitch = **18% reply** vs **6% generic** (3× difference)
- Length: **80–150 words**, no longer
- Subject line: **specific, references their content**, not generic
- Body structure (in order): personalization hook → credibility line → 3 topic offers → soft CTA

**Architecture:**

```
SUBJECT: [Specific reference to a recent post + 4–6 word topic suggestion]
   GOOD: "Loved your CI piece — pitch on monorepo trade-offs?"
   BAD: "Guest post pitch for [publication]"
   BAD: "Quick question"

OPENING (1–2 lines) — Personalization hook tied to a SPECIFIC article they published.
   Reference the title or a specific point. Not "love your blog" — "your piece on X
   made me rethink Y."

CREDIBILITY (1 line) — One sentence on who you are, why you can write on this.
   Name 1–2 prior placements (with link), or your specific expertise/data.

TOPIC OFFER (the meat — 3–5 lines) — 3 specific topic ideas, each one sentence,
   each addressing a content gap on their site. Title + value prop.

CTA (1 line) — Soft. "Happy to send a draft outline if any of these fit."
   NEVER "let me know what you think" or "if interested, please reply."

SIGN-OFF — Name. One link. Done.
```

**Length math:** subject ~10 words; opening ~25 words; credibility ~25 words; topic offers ~50 words; CTA ~10 words; signature ~5 words = ~125 words. Stay in this range.

**Pitch template (brief — not a finished email):**

```
Subject: [Reference to specific post they wrote] — [topic suggestion in 4-6 words]

Hi [Editor first name],

Your [post title or specific point] last [time-frame] got me thinking about [related angle]. Specifically, the part where you mentioned [specific quote/idea] — I think there's a follow-up that would resonate with [audience descriptor].

I'm [credibility — role + 1 prior tier-comparable placement OR specific original asset]. A few topics I could write that I think would fit:

  • [Topic 1 title] — [one-sentence value prop tied to their audience]
  • [Topic 2 title] — [one-sentence value prop]
  • [Topic 3 title] — [one-sentence value prop]

Happy to send a detailed outline if any of these fit your editorial calendar.

— [Name]
[One link, branded]
```

**Pre-pitch relationship-building (multiplier):**

If pitching T1/T2 (where acceptance rates are <20%), do this BEFORE the pitch over 2–4 weeks:
- Share their content 2–3× on social with your own thoughtful comment
- Leave 1–2 substantive comments on their recent posts (not "great article!")
- Send one appreciation email — no pitch, just thank them for a specific piece
- Reference all of this implicitly in the eventual pitch

This is what moves T1/T2 acceptance rates from 5% to 20%+.

#### Stage 6 — The Post Itself (writing standards by tier)

The post lives or dies based on whether it meets the publication's standard. Match the tier:

**Tier-1 standard:**
- "As good or better than what you post on your own blog"
- 2,500–4,000 words; longer is fine if substantive
- Actionable system, not summary — step-by-step process the reader can apply
- Custom screenshots, charts, original data
- Search-intent match — readers should find it via target queries
- Original quotes (not just citations) where possible
- Internal linking to host site's own relevant content (3–5 internal links to THEIR posts) — this is a signal of editorial care

**Tier-2 standard:**
- 1,500–2,500 words
- Case study or process post format works well
- Visuals required but can be lighter
- Internal linking to host site (2–3 links to their posts)

**Tier-3 standard:**
- 1,000–1,500 words
- Substantive but doesn't need T1 production polish
- 1–2 internal links to host site

**Tier-4 standard:**
- 800–1,200 words
- Solid contribution, simpler structure

**Universal rules across all tiers:**
- Original — never duplicate published-elsewhere content
- Human-written — AI-content farms are now a tagged violation category
- Match the publication's voice (read 5 of their posts before writing)
- Lead with the value, not the setup
- No promotional content for your own product/service in the body

**Output of Stage 6:** an outline + post-writing brief (target word count, format, voice notes, internal-link list). Actual prose generation is out of scope for this skill.

#### Stage 7 — Link Strategy (placement + anchors)

This is where the penalty risk is highest. Get it right.

**Link placement (where the links go):**

| Link Type | Count | Placement | Notes |
|---|---|---|---|
| **Body link** (preferred) | 1–2 | Inside the article body, contextually relevant | 387% more referral traffic than bio-only; always preferred |
| **Author bio link** | 1 | In the bio at top or bottom | Standard; safe; usually nofollow |
| **In-content related-link** | 0–1 | Linking to host's other content | Signals editorial care; not your link, but boosts pitch acceptance |

**Body link rules:**
- The link must genuinely help the reader at that exact point in the post
- Place near (within 1–2 paragraphs of) a topic the linked page covers
- Don't force a link if the post doesn't naturally call for one — better to have only the bio link than a forced body link

**Anchor text distribution (DATA-BACKED, track across all posts):**

| Anchor Type | Target Mix | Examples |
|---|---|---|
| **Branded** | 40–50% | "Acme", "Acme Tools", "Acme's documentation" |
| **Partial-match** | 20–30% | "Acme's CI/CD platform", "see Acme's monorepo guide" |
| **Semantic / long-tail** | 15–25% | "this benchmark on deploy time", "the team's analysis of cold-start latency" |
| **Generic** | 5–10% | "here", "this article", "see this case study", URL-only |
| **Exact-match keyword** | <10% | "monorepo CI tool", "best CI/CD platform" — used SPARINGLY |

**Why this matters:** diversification reduces manual-action risk by **68%**. Sites that use exact-match on every guest post get flagged within months. Track anchor distribution across your last 20 placements; if exact-match exceeds 10%, stop using them entirely until ratio rebalances.

**Author bio rules:**
- ONE link only
- Anchor: branded or URL — never exact-match keyword
- 1–2 sentence bio — don't write a sales pitch
- Link to homepage or a specific resource (a blog post, tool, or about page) — not to a sales page

**Forbidden in any guest post:**
- Self-promotional CTAs ("buy our X", "sign up for our Y")
- Stuffed exact-match anchors
- Affiliate links unless explicitly approved by host (and then with `rel="sponsored"`)
- Linking to the same destination URL across multiple posts (sitewide pattern)

#### Stage 8 — Follow-up & Relationship

The pitch isn't a one-shot. Build the relationship:

| Action | Timing | Purpose |
|---|---|---|
| First follow-up | 7 days after pitch (no reply) | Polite bump, re-state one topic, ask if a different angle would fit |
| Second follow-up | 14 days after pitch (no reply after first follow-up) | One sentence; do not pitch a third time |
| Thank-you note | After post is published | One paragraph, no ask, mention a specific reader response if any |
| Share + amplify | Day of and week after publication | Post on social; tag the publication and editor; comment-engage |
| Re-pitch trigger | 90 days after publication | Pitch a follow-up topic referencing the prior post's reception |

**Goal:** convert a one-off placement into a 3–4 post relationship over 12 months. This is more valuable than 4 different one-off placements at the same tier, because each subsequent post:
- Has a higher acceptance rate (relationship now exists)
- Compounds your association with the publication
- Builds a credible portfolio for tier-up moves

---

### Decision Guide — Edge Cases

| Situation | Action |
|---|---|
| Site lists "guest post fee: $200" with no `rel="sponsored"` mention | **Strike** — paid placement passing ranking signal = penalty |
| "Vetted network" agency offers 10 placements/month for $2k | **Strike** — at scale this is functionally a guest-post farm; Oct 2025 update target |
| Niche-edit / link-insertion service offers placement on existing article for $300 | **Strike** — same penalty class as paid guest posts |
| Site clearly editorial but their "write for us" page hasn't been updated in 2 years | **Email the editor directly anyway** — the page is outdated, not the policy |
| Editor responds: "We charge $150 per published post, fully edited" | **Skip unless `rel="sponsored"` is explicitly applied** — clarify; if dofollow paid, walk away |
| User wants to use one ghostwriter for 10 posts under different bylines | **Refuse** — same-author footprint across "different" voices = PBN-detection trigger |
| User wants to syndicate the same post to 5 sites | **Refuse** — duplicate content is its own violation; rewrite per publication |
| Pitch reply: "We need it within 48 hours and 3,500 words" | **Decline if not realistic** — rushed posts read as rushed; better to pass than ship sub-standard |
| User has zero portfolio; asks to pitch tier-1 | **Refuse and ladder** — start tier-3/4, build 3–5 placements, then ladder up |
| Same topic accepted by two publications independently | **Write two original versions** — different angles, different examples, different conclusions; never publish the same draft twice |
| Pitch accepted but editor wants you to remove the body link | **Negotiate once, accept gracefully** — bio-link-only is still a valid placement at lower value |
| Pitch accepted but editor wants exact-match anchor on the body link | **Push back** — request branded or partial-match; if they insist on exact, walk away (manual-action risk on you, not them) |
| Tier-1 has been engaged for 3 months, no acceptance | **Stop. Drop tier.** — at T2 your portfolio grows; you can re-pitch T1 in 6 months from a stronger position |

---

### Google's Position on Guest Posting (the actual rules)

Google has been consistent: editorial guest posts on relevant authoritative sites are **endorsed**. Manipulative ones are **violations**. The line:

**ALLOWED:**
- Editorial guest contributions on topically aligned sites
- Posts written for genuine readership, not just for the link
- Properly attributed sponsored content with `rel="sponsored"`
- Niche-relevant outreach that builds real relationships

**VIOLATIONS (per Google's spam policy):**
- "Advertorials or native advertising where payment is received for articles that include links that pass ranking credit" (paid guest posts without `rel="sponsored"`)
- "Using automated programs or services to create links" (mass guest-post farms)
- "Excessive reciprocal link exchanges" (you write for me, I write for you, scaled)
- Guest post networks (closed networks publishing for SEO)
- AI-generated guest post farms (Oct 2025 update — distinct violation category)
- Repetitive exact-match anchor patterns across multiple guest posts (algorithmic flag)

The intent test: would this guest post exist if SEO didn't exist? If yes → it's editorial. If no → it's a violation in waiting.

---

### Tools — what's free vs paid

| Tool | Tier | Use for |
|---|---|---|
| Google Search (operators) | Free | Discovery |
| Ahrefs Free Backlink Checker | Free (limited) | Top 100 backlinks of competitor → guest opportunities |
| Wayback Machine | Free | Confirming a site's longevity / topical history |
| Hunter.io free tier | Free (limited) | Editor email discovery |
| Apollo / RocketReach free tier | Free (limited) | Editor LinkedIn / email discovery |
| Featured.com newsletter | Free | Editor calls for sources (HARO replacement) |
| Source of Sources (SOS) | Free | Editor calls for sources |
| Qwoted | Freemium | Journalist matching |
| Similarweb (free tier) | Free | Traffic estimate sanity-check |
| Ahrefs / Semrush full | Paid | Network graph, full backlink profile |

---

## Examples

### Example 1: Tier-3 placement, dev-tools SaaS

**Setup:**
- Author: senior platform engineer, brand: CI/CD SaaS
- Portfolio: 1 prior post on a tier-3 dev blog
- Target: a DR-45 dev-ops focused publication, ~25k organic monthly, named editor

**Stage 1 — Tier mandate:** T3 core (matches portfolio); T2 stretch with an exceptional pitch.

**Stage 2 — Discovery operators (parallel):**
```
"continuous integration" intitle:"write for us"
"devops" intitle:"contribute"
"ci/cd" inurl:/contributors/
site:[competitor.com] "guest post" → reverse-engineer competitor's link sources
```

**Stage 3 — Qualification of target:**
- Topical fit: ✅ (last 30 posts: 60% CI/CD, 30% dev-ops, 10% adjacent)
- Real traffic: ✅ (Similarweb: 22k/mo organic)
- Editorial: ✅ (named editor, masthead, reject rate referenced in their guidelines)
- Indexed/ranking: ✅
- Outbound profile: ✅ (links to GitHub, AWS docs, dev-blog peers)
- Author diversity: ✅ (50+ contributors, all distinct)
- No PBN tells: ✅
- Cost: free editorial; no paid placement signaling
- Verdict: **proceed**

**Stage 4 — Topic ideation (3 candidates):**
- Read last 30 posts. Identified gaps:
1. **"What 18 months of monorepo CI metrics taught us about test parallelization"** — original benchmark data from author's company, fills a gap (publication has covered monorepo strategy but not parallelization specifics)
2. **"Self-hosted runners vs. managed CI: a 6-month cost-and-reliability comparison"** — case study with numbers; publication has discussed runners but not done a head-to-head
3. **"Why we shipped a CI cancellation policy and what we measured after"** — process post; ties to author's company experience

**Stage 5 — Pitch brief:**
```
Subject: Loved the runner-sizing piece — pitch on monorepo CI metrics?

Hi Sarah,

Your post on right-sizing runners last month nailed the cost angle, but the comment thread kept asking about test parallelization specifically — there's a real gap there.

I'm a platform engineer at Acme Deploy. We've been instrumenting our monorepo CI for 18 months across ~3,400 daily runs and have data I haven't seen anywhere else. I wrote a tier-3 piece on runner ergonomics for [other-publication] last quarter (link).

Three angles I could write that fit your editorial scope:

  • What 18 months of monorepo CI metrics taught us about test parallelization — original benchmark data, the 4 metrics that actually matter
  • Self-hosted runners vs. managed CI: a 6-month cost-and-reliability comparison — head-to-head case study with numbers
  • Why we shipped a CI cancellation policy and what we measured after — process post on a non-obvious lever

Happy to send a detailed outline if any of these fit.

— Author Name
acme-deploy.com
```

**Stage 6 — Post writing brief:**
- Tier-3 standard: 1,500 words; case study format; 3 charts from internal data; 2 internal links to host site's prior CI/CD posts
- Outline produced; prose generation handled outside this skill

**Stage 7 — Link strategy:**
- 1 body link: "...we benchmarked this against the [Acme Deploy CI runner pool]..." — partial-match anchor
- 1 author bio link: "Author leads platform engineering at [Acme Deploy]." — branded anchor
- Anchor distribution check: this is post #3 for the brand. Across all 3: 2 branded, 1 partial-match. ✅ within target distribution.

**Stage 8 — Follow-up:** post published; share on Twitter and LinkedIn tagging publication; thank-you email to editor 1 week post-publication; re-pitch in 90 days with the runner comparison topic.

### Example 2: Refusing a tier-1 reach

User: "I have no portfolio but want to pitch a guest post to TechCrunch."

**Response:**
> Stop. TechCrunch's acceptance rate for cold pitches with no prior tier-1 placements is functionally zero. Spending 3 weeks crafting a TechCrunch pitch with no portfolio costs you the 5 tier-3 placements you could land in the same time.
>
> Honest path:
> 1. **Months 1–3:** target tier-4 (DR 10–30 niche blogs, owner-edited). Land 3–4 placements. These are achievable and they're real bylines.
> 2. **Months 3–6:** ladder to tier-3 with the tier-4 portfolio in your credibility line. Land 2–3 here.
> 3. **Months 6–12:** at tier-2 with 5–7 prior placements, acceptance rates jump to 15–20%. Land 2–3 here.
> 4. **Year 2:** at this point a TechCrunch pitch has a chance — you have tier-2 placements, one with original data they'd notice. Now the pitch lands at maybe 5–10% probability instead of 0%.
>
> The path matters more than the destination. Pitching above your tier costs you the tier you could be building.

Do not soften.

### Example 3: Refusing a paid network

User: "I found a service offering 10 guest posts per month on DR 50+ sites for $1,500 total. They handle everything."

**Response:**
> Skip. The math gives away what's actually happening:
>
> - $150 per placement on a "DR 50+" site is below the editorial cost of even outsourced content writing (which is ~$200-400 per post). Real editorial guest posts cost the publisher money to review and edit — they don't pay you to publish, they don't accept $150 placements either.
> - At scale (10/month from one provider), every site in the network is reused across clients. Same author bylines, same anchor patterns, same template-style content. This is the textbook footprint the Oct 2025 update flagged as "AI-generated guest post farms."
> - Even if the links pass initially, devaluation lands within weeks. Worst case: manual action on the receiving domain — your site, not theirs.
>
> The honest math: 10 placements at $150 each from a network = ~$1,500 in spend, ~0 long-term link value, and a manual-action risk on a 6-month recovery curve.
>
> Real editorial costs more in time, but the placements compound. 2 tier-3 editorial guest posts per month, earned through the workflow above, beat 10 paid network posts every quarter.

---

## References

- [Google Search Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies) — link spam definitions
- [Backlinko — The Definitive Guide to Guest Blogging](https://backlinko.com/the-definitive-guide-to-guest-blogging) — Tier framework, qualification, pitch structure
- [Search Engine Journal — Google penalties on guest post articles](https://www.searchenginejournal.com/guest-post-manual-actions/351692/)
- [Search Engine Land — Guest post outreach 2026 process](https://searchengineland.com/guest-post-outreach-proven-scalable-process-473497)
- [Hunter — 15 best-performing guest post email templates](https://hunter.io/templates/seo/guest-post) — pitch performance data
- [Anchor distribution data — 68% penalty reduction](https://staydigitalmarketers.com/2026/01/31/is-guest-posting-safe-seo-risks-penalties/)
- [Editorial links are the new brand mentions for AI search](https://linkbuilder.io/editorial-links/) — 2026 framing
