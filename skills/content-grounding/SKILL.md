---
name: content-grounding
title: "Fact Grounding & Anti-Hallucination"
description: "Confidence triage, mandatory research triggers, source verification, and clarification escalation for content writing and editing. Prevents fabricated facts about unfamiliar tools, products, people, versions, prices, or recent events. Applies before any specific claim is written."
license: Apache-2.0
compatibility: "Octomind content agents. Requires websearch and the webfetch capability for live source verification."
capabilities: websearch webfetch
domains: content
rules:
  - content(article)
  - content(blog)
  - content(editor)
  - content(seo)
  - content(grounding)
  - content(research)
  - match(\b(write|draft|edit|review)\s+(an?|the|this|my)\s*(article|blog|post|piece|copy|review|guide|tutorial)\b)
  - match(\b(verify|fact[-\s]?check|ground[-\s]?truth|source|cite|citation)\b)
  - match(\b(hallucinat\w*|fabricat\w*|made[-\s]?up|invented)\b)
  - match(\b(unfamiliar|niche|obscure|new|unknown)\s+(tool|product|library|framework|api|sdk|service|platform)\b)
  - match(\b(don'?t|do\s+not|never)\s+(make\s+up|invent|guess|assume|fabricate)\b)
  - semantic(write accurately about a tool you might not know)
  - semantic(do not invent facts about this product)
  - semantic(verify the specifics before writing)
  - semantic(ask if you are not sure instead of guessing)
  - semantic(this is a niche tool you may not have training data on)
  - semantic(make sure every fact in the article is real)
---

## Overview

Most content hallucinations are preventable. They happen when a writer asserts a specific — a function name, a version number, a price, a feature, a quote, a statistic — that it cannot ground in training data or verified research, and fills the gap with something plausible-sounding. This skill encodes the protocol every content agent applies before writing any specific claim: triage confidence, research what isn't certain, escalate to the user when research fails, and never paper over uncertainty with a confident-sounding fabrication.

A draft about a tool the model has never seen is the highest-risk scenario. The default must be "verify or ask" — never "guess and ship."

## Instructions

### Confidence triage (before writing any specific claim)

Every claim falls into one of five buckets. The bucket dictates the action:

| Bucket | Example | Action |
|---|---|---|
| Common knowledge | "JavaScript runs in browsers" | Write — no source needed |
| Familiar specific | A widely-documented tool's main use case | Write; verify if you'd hesitate to say it aloud |
| Unfamiliar entity | A tool, product, library, person, paper the agent doesn't recognize | Stop. Research before writing anything specific. |
| Time-sensitive | Current version, current price, "latest", anything from the last 18 months | Stop. Search the web — training data is stale. |
| Speculative | Opinion, prediction, synthesis | Write, mark as opinion ("I'd argue", "Evidence suggests") |

If a claim doesn't fit cleanly into "common knowledge" or "familiar specific," it needs research or escalation. Default to caution. The cost of one extra search is trivial; the cost of one fabricated fact in a published article is reputation damage that compounds.

### Research triggers (live verification required)

These claims require live verification — training data alone isn't enough:

- Named tool, library, framework, SDK, service, or product not immediately recognized
- Any version number, release date, or "latest" claim
- Pricing, plans, free-tier limits, billing terms, seat counts
- API endpoints, function signatures, type signatures, CLI flags, configuration keys, environment variable names
- Statistics, percentages, study results, survey numbers, market sizes
- Quotes attributed to a specific person
- People — name, title, current role, affiliation, credentials
- Events, launches, acquisitions, funding rounds in the last 18 months
- URLs, GitHub repos, documentation paths, social handles
- Anything the user provides as the subject of the piece rather than as general background

If a trigger fires and you proceed without research, that is a protocol violation — flag yourself and stop.

### Research protocol (when triggered)

1. Specific queries first. `"[product name] documentation"`, `site:github.com [tool]`, `[product] pricing 2026`, `[person name] [role/company]`. Vague queries surface SEO sludge.
2. Prefer primary sources. Official docs, the GitHub README, the vendor's pricing page, a press release on the company domain, the person's own bio, the peer-reviewed paper PDF. Treat blog summaries and listicles as secondary — they often repeat each other's mistakes.
3. Cross-reference at least two independent sources for any specific number, date, feature, or quote. One source can be wrong; two agreeing primary sources is the floor.
4. If sources conflict, search deeper for the primary source or surface the conflict to the user. Don't pick a side silently.
5. For genuinely new or niche subjects, fetch the user-provided URL or the official site directly via the `webfetch` capability. Don't paraphrase what you can fetch verbatim — quote or excerpt the source.
6. Parallel-first. Fire the discovery queries in one block — official docs query, GitHub query, recent news query, pricing/release query — then read what came back.
7. Re-consult sources as you write. When drafting long-form, re-fetch the primary source whenever a section needs a specific fact, instead of relying on what you remember from the first read. Grounded writing means every claim resolves to a source the agent re-read, not to the model's training memory.

### Escalation: when research fails

After 2–3 targeted searches without authoritative info, STOP. Do not proceed to write the specific claim. Escalate with a precise, one-question-at-a-time ask — not a vague "tell me more":

Good escalations (specific, actionable):
- "I can't find official documentation for [tool X]. Can you share the docs URL or a primer page?"
- "Sources differ on [Y]: the vendor site says A, a third-party review says B. Which is canonical?"
- "Your draft says [product Z] supports [feature]. I can't confirm it in the current docs — can you point me to the release note, or should I drop the claim?"
- "I don't have ground truth on [person/event]. Can you provide a source, or should I omit the reference?"

Bad escalations (vague, scope-creeping):
- "Tell me more about this." — useless without specificity
- "Anything else I should know?" — invites scope creep, not a fix

Rules of escalation:
- One blocking question at a time; chain follow-ups, don't bundle a dozen.
- Always offer the user a fork: "I can (a) wait for your source, (b) drop the claim, (c) mark it `[needs verification]`." That makes the response one-tap.
- Never substitute escalation for laziness — exhaust the research protocol first.

### Output rules — every factual claim

1. Inline source or attribution for every specific claim. Either a hyperlink to the primary source, or `(Source: [Name], [Year])`.
2. Opinion markers for synthesis or judgment — "I'd argue", "In my experience", "Evidence suggests", "The consensus seems to be". Never present opinion as fact.
3. Verified vs. unverified. If you can't source it and can't drop it, mark it inline `[needs verification]` and surface it in the grounding report at the end.
4. Confident voice ONLY for verified facts. Hedging belongs on opinions, not on data points. "Acme released version 4.2 in March 2026" or you don't write the sentence.

### Anti-fabrication absolutes — never invent

Zero-exception. If you don't know the exact value, find it or rewrite around it. Do not guess, do not interpolate from "similar products", do not extrapolate "what it probably looks like":

- Function signatures, parameter names, type signatures, return types
- API endpoints, request/response shapes, status codes, headers
- CLI flags, subcommands, environment variable names, config keys, file paths
- Version numbers, release dates, deprecation timelines
- Pricing tiers, free-tier limits, billing units, seat caps
- URLs, email addresses, GitHub repo paths, package names
- Person names, job titles, company affiliations, credentials
- Direct quotes attributed to a named person
- Statistics, percentages, study sample sizes, study citations, dataset sizes
- Product features, supported platforms, integration lists, language support
- Command outputs, error messages, log lines

If you find yourself "rounding to a plausible-sounding answer" — STOP. That's a hallucination forming. Search or escalate.

### Editing existing drafts (content:editor focus)

When given a draft about an entity you don't have ground truth on, the protocol changes shape. You are no longer the author of the claim; you are the editor of someone else's. Default to preservation:

1. Inventory named entities before editing. List every tool, product, person, library, version, statistic, URL, command, and quoted block the draft references.
2. Triage each entity against the five buckets. Anything unfamiliar → mark for verification.
3. Preserve original specifics. Never "improve" or "clean up" a function signature, a CLI flag, a version number, a quote, a stat, or a URL you didn't verify. The original is the user's ground truth; your assumption is not.
4. Search the unfamiliar entities before any rewrite touches them. Two parallel queries per entity is the floor — official docs and a corroborating source.
5. If verification fails after research, ask the user for the canonical reference (docs URL, product page, original interview transcript). Don't rewrite the claim into something you find plausible.
6. Voice edits are still safe. When the factual content is unverifiable, you can still fix rhythm, dead vocabulary, hooks, transitions — anything that doesn't change what the draft claims. Surface the untouched factual claims in the grounding report.

A bad edit that "corrects" a real fact into a plausible-sounding fabrication is worse than no edit at all.

### User-provided drafts about niche or unfamiliar topics

When the user provides a draft and the subject is outside common knowledge:

1. Acknowledge it explicitly up front. "This is about [X] — let me verify the specifics before editing." Don't pretend confidence you don't have.
2. Ask up front for: official docs URL, vendor/product page, any source materials the user already has, the canonical reference for any quote or stat.
3. If the user can't or won't provide sources, run the research protocol. If that also fails, edit ONLY voice/structure/rhythm — flag every factual claim as unverified rather than touch it.
4. Never silently rewrite an unfamiliar specific into a different specific. That is the highest-cost failure mode in editing.

### Confidence reporting in the output

When delivering work that involved any research or any unresolved gap, surface it explicitly. The user must see exactly which claims rest on what:

```
## 🔍 Grounding Report
- Verified via primary source: [claim — link]
- Verified via cross-reference: [claim — sources A, B]
- Verified via user-provided source: [claim — source]
- Unresolved (flagged `[needs verification]` in draft): [list]
- Skipped (couldn't verify — rewrote around or dropped): [list]
- Open questions for you: [list]
```

This is non-negotiable for any piece involving named tools, recent events, specific numbers, or technical specifics. No grounding report = no ship-ready output.

### Anti-patterns to refuse

- The "sounds plausible" fill — writing what a similar product probably does when you can't confirm the specific one
- The silent rewrite — changing a specific term in someone else's draft to one you find cleaner without verifying either
- The vague hedge — using "many users", "various tools", "in some cases" to mask the fact that you don't have a number
- The fake citation — `(Source: Industry Report, 2025)` with no actual report behind it
- The bundled escalation — asking the user eight questions at once instead of researching seven and escalating one
- The skip-and-ship — proceeding to draft anyway because "the user will catch it" — they won't, and that's why they hired you

## Examples

### Confidence triage in action

User: "Write a blog post about Octomind's new agent SDK."

❌ Wrong: Start writing about features, pricing, and use cases based on what "agent SDKs typically have."

✅ Right:
1. Triage: "Octomind agent SDK" — unfamiliar entity, post-training-cutoff possible.
2. Research in parallel: `"Octomind agent SDK" documentation`, `site:octomind.dev sdk`, `Octomind SDK release notes`, `Octomind agent SDK github`.
3. If results sparse → escalate: "I can't find docs for the Octomind agent SDK. Three options: (a) share the docs URL, (b) paste a primer / changelog, (c) name a launch post I can fetch. I don't want to fabricate features."

### Anti-fabrication in editing

Draft says: "The `octomind init --workspace` command creates a new project."

❌ Wrong: Edit to "The `octomind new --project` command initializes a project" because the rewrite "sounds cleaner."

✅ Right: Preserve the original command exactly. If asked to verify, search `octomind CLI init command` or webfetch the docs. If unverifiable, ask: "Can you confirm the exact init command? I see `octomind init --workspace` in your draft and don't want to change it to something that doesn't exist."

### Escalation phrasing — specific, forked, one-tap

❌ "I need more info about this product."

✅ "I'm writing the integrations section. Your draft mentions Slack and Jira. I can confirm Slack via the docs but can't find Jira anywhere on the vendor site or GitHub. Three options: (a) you confirm Jira is supported with a source, (b) I drop Jira from the list, (c) I mark it `[needs verification]` and you check before publish. Which?"

### When research succeeds — clean grounding

User: "Mention that Acme raised their Series B last year."

✅ Right:
1. Triage: time-sensitive, named entity, specific event.
2. Research: `Acme Series B 2025`, `site:acme.com news Series B`, `Acme Series B announcement`.
3. Find: TechCrunch article + Acme press release agreeing on date and amount.
4. Write: "Acme raised a $42M Series B in October 2025, led by Sequoia ([TechCrunch](url), [press release](url))."
5. Grounding report notes: verified via cross-reference (primary + secondary).
