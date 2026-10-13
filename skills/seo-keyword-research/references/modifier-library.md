# Long-Tail Modifier Library

Full modifier set for Stage 3 expansion. Apply each pattern to every seed term; expect 5–15 winnable long-tails per seed after Stage 4 qualification.

## Question modifiers (highest GEO value — earn AI citations)

```
how to [seed]
how does [seed] work
what is [seed]
what is [seed] used for
why [seed] matters
why [seed] is [adjective]
when to use [seed]
where to find [seed]
which [seed] is best for [audience]
who needs [seed]
is [seed] worth it
do I need [seed]
can I [verb] with [seed]
should I [verb] [seed]
```

These map directly to AI Overview / ChatGPT / Perplexity citation patterns. Pair with answer-first content structure (handled in another domain).

## Intent modifiers (commercial / transactional)

```
best [seed] for [audience]
best [seed] [year]
top [seed] for [use case]
[seed] for [audience size or segment]
free [seed]
free [seed] no signup
cheap / affordable [seed]
[seed] under $[price]
[seed] alternative to [incumbent]
[seed] vs [alternative]
[seed] without [obstacle]
[seed] that [specific capability]
[seed] for beginners / for experts
[seed] reviews [year]
[seed] pricing
[seed] discount / coupon
buy [seed]
get [seed]
hire [seed]
```

Caveat for "best [seed] [year]" patterns: third-party review sections on Forbes / Fortune / CNN-style publishers still crowd some of these SERPs despite Google's site reputation policy (whose manual actions no longer apply to EEA searchers since Aug 30, 2026). Score realism low unless the user has DR ≥ 50 or a niche-brand-page play.

## Constraint modifiers (sharpen specificity → reduce competition)

```
[seed] for solo / for two-person / for small team / for remote teams
[seed] for [industry vertical]
[seed] for [geo / region / country]
[seed] in [year]
[seed] with [specific feature]
[seed] without [common annoyance]
[seed] step by step
[seed] checklist
[seed] template
[seed] examples
[seed] case study
[seed] beginner guide
[seed] advanced guide
```

This is the highest-yield bucket for low-DR sites — every constraint removes competitor pages that wrote for the broader query.

## Outcome modifiers (high commercial intent)

```
how to [seed] in [time bound]
how to [seed] without [obstacle]
[seed] tutorial for [audience]
[seed] guide [year]
[seed] case study
[seed] roi / cost / pricing
[seed] mistakes to avoid
[seed] best practices [year]
[seed] checklist [year]
fastest way to [seed]
cheapest way to [seed]
[seed] in 5 minutes / 10 minutes / one day
```

## Comparison modifiers (mid-funnel, GEO-friendly)

```
[seed] vs [alternative 1]
[seed] vs [alternative 2]
[A] vs [B] vs [C]
difference between [A] and [B]
[seed] alternative
top alternatives to [seed]
is [seed] better than [alternative]
when to use [A] vs [B]
[A] or [B] for [use case]
```

Comparison queries score high for AI-citation potential when written as side-by-side tables with extractable rows.

## Problem-trigger modifiers (TOFU, audience research)

```
why is my [thing] [problem]
[symptom] in [tool/service]
fix [problem] in [context]
stop [bad outcome]
prevent [problem]
[problem] when using [tool]
[error message phrase]
how to fix [error]
```

Mine these from support forums, Reddit threads, GitHub issues, and Discord/Slack help channels. They signal active pain — high conversion if your product solves them.

## Audience-specific modifiers

```
[seed] for [job title]
[seed] for [company stage] (startup, series-A, enterprise)
[seed] for [team size]
[seed] for [region]
[seed] for [industry]
[seed] for non-[expert]
[seed] without [prerequisite knowledge]
```

Layer with constraint modifiers for compound specificity (e.g. "self-hosted CRM for solo financial advisors GDPR-compliant" — likely zero-volume, but the cluster exists).

## Modifier wheel (mental model — for ad-hoc expansion)

For any seed, the question wheel runs across 6 axes:

```
WHO    × [seed] × the searcher / target audience
WHAT   × [seed] × variants / kinds / examples / specs
WHERE  × [seed] × geo / context / channel
WHEN   × [seed] × timing / season / lifecycle stage
WHY    × [seed] × motivation / problem-trigger
HOW    × [seed] × method / step-count / time-bound

× LIKE / VS / WITH / WITHOUT / FOR / AGAINST [other entity]
```

Cross-multiply axes for 36+ candidate phrasings per seed. Filter at Stage 4.

## SERP-mined patterns (free, parallel)

- Google autocomplete — type seed + each letter a–z; capture suggestions per letter (incognito).
- Google "People Also Ask" — search the seed, expand 2–3 PAA branches; each branch reveals 3–5 related questions.
- Google "Related searches" — bottom-of-SERP carousel.
- Google Trends — "Related queries (rising)" tab for momentum signals.
- Reddit / forum mining — `site:reddit.com [seed]` — actual user phrasing; pull thread titles + top comment phrasings.
- Quora / Stack Exchange / niche forums — same approach for verticals where Reddit isn't dominant.
- AlsoAsked — visualizes PAA tree (free tier, limited queries).
- AnswerThePublic — visualizes question/preposition/comparison wheel (free tier, limited queries).
- Lowfruits — keyword tool specifically built for low-competition discovery; identifies SERPs dominated by weak/forum content.
- Glimpse / Exploding Topics — surfaces trending and emerging keywords before tools assign volume.

Run all SERP-mined sources in parallel for each seed; dedupe at Stage 4.

## Tools — free vs paid

| Tool | Tier | Use for |
|---|---|---|
| Google Search (incognito) + autocomplete | Free | Seed expansion, SERP review |
| Google Trends | Free | Volume sanity, trend direction, "Related queries (rising)" momentum |
| Google Search Console | Free | Existing query mining, page-2 quick wins, impression data |
| Bing Webmaster Tools | Free | Keyword data, IndexNow, sitemap submission — Bing's index also feeds Copilot and, historically, ChatGPT search |
| Ahrefs Free Backlink Checker | Free | DR estimate for site + competitors |
| AlsoAsked / AnswerThePublic free | Free (limited) | PAA / question-modifier expansion |
| Reddit / forums | Free | Real user phrasing, zero-volume validation, AI-citation pre-mining |
| Lowfruits | Freemium | Purpose-built low-competition keyword discovery — flags SERPs dominated by weak/forum content |
| Glimpse / Exploding Topics | Freemium | Emerging keywords pre-volume; momentum signal before tools assign KD |
| SparkToro | Freemium | Audience research — what your buyers actually read/listen-to/follow (informs seed phrasing) |
| Ahrefs / SE Ranking / Serpstat / SEMrush | Paid | Full keyword databases, KD scores, competitor ranking lists, SERP overview |
| Surfer SEO / NeuronWriter / Frase | Paid | TF-IDF / NLP entity coverage — which entities the top 10 cover that you're missing (Stage 5) |
| Profound / Otterly / AthenaHQ / Peec | Paid | AI search visibility tracking — share of citation across ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude; the measurement layer for the brief's GEO claims |
