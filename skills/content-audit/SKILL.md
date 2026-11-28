---
name: content-audit
title: "Content Audit Rubric & Scoring Harness"
description: "Read-only content audit: detects content type, scores each axis 0-10, reports findings with evidence and rewrites. Use to diagnose a draft or post."
license: Apache-2.0
compatibility: "Read-only. Requires filesystem read access for file inputs; live SERP or source checks need network access."
domains: writer
rules:
  - match((?i)\b(audit|scored?\s+audit|score|grade)\s+(this|my|the|our|an?|attached|these|each)\b.{0,60}\b(post|thread|tweet|article|blog|bios?|caption|comments?|replies|reply|title|draft|copy|submission)\b)
  - match((?i)\b(rubric|per-axis|axis\s+scores?|prioritized\s+findings|critical/moderate/minor|overall\s+score|platform\s+fit)\b)
  - match((?i)\b(how\s+(good|strong|viral)\s+is\s+this|will\s+this\s+(work|rank|perform|land)|honest\s+audit|audit\s+with\s+scores|score\s+it|flag\s+any\s+problems)\b|\b(check|inspect)\s+.{0,40}before\s+(posting|publishing|shipping)\b)
  - match((?i)\b(edit|fix|tighten|polish|rewrite|surgical)\w*\b.{0,80}\b(draft|post|article|newsletter|copy|essay|hook|intro|piece)\b)
  - match((?i)\bhumani[sz]e\b|\bAI-sounding\b|\bChatGPT-written\b|\bsurgical\s+edit\b)
  - semantic(audit this post before I publish, 0.72)
  - semantic(score this draft against the algorithm, 0.72)
  - semantic(tell me what will fail in this content, 0.72)
  - semantic(score this blog post and show what to rewrite, 0.72)
  - semantic(review my draft and tell me what is weak and why, 0.72)
---

## Overview

The shared rubric for scoring any content the system writes. A read-only audit renders reports from it; an edit session uses the same diagnosis to drive rewrites. The harness detects the content type, routes to the platform skill, and grades with per-axis scores plus a prioritized findings list. It never writes to the source file.

## Mental model

An audit is intent-versus-execution: what does this content type need to win, what does this draft actually deliver, where is the gap, and how cheap is each fix.

Three constraints keep the harness useful instead of confusing:

- Platform skills own the rules; the harness owns the grading. `social-x` knows what good X looks like; this skill knows how to count, weight, and report what it finds. Never restate platform rules here — read them from the activated skill.
- One canonical report shape across every content type. Same headers, same severity tiers, same axis vocabulary. Only the weights on each axis change per content type. Skim-able regardless of input.
- Read-only — the audit renders the report and stops. Suggested rewrites are proposals inside the report, never disk writes. To apply them, run an edit session with the report as input.

## Instructions

### Content-type detection

Read the input. Match against these signatures. If signal is ambiguous, ask the user once before scoring.

| Signature | Type | Routed skills |
|---|---|---|
| ≤ 280 chars, no thread markers, single block | X post | `social-x` + cross-cutting |
| 2+ blocks separated by blank lines or "—" / "Post N" markers, each ≤ 280 chars | X thread | `social-x` + cross-cutting |
| ≤ 3000 chars, conversational, no formal sections | LinkedIn post | `social-linkedin` + cross-cutting |
| Similar to X but with different platform context cue | Threads / Bluesky / Mastodon / Reddit / HN / Facebook | matching `social-<platform>` + cross-cutting |
| Image or video caption, hook line, or script for a short vertical video, named or cued as Instagram, TikTok or YouTube | Instagram / TikTok / YouTube copy | `social-instagram`, `social-tiktok` or `social-youtube` + cross-cutting; scored with the X post/thread weights |
| Long-form post named or cued as dev.to or Medium | dev.to / Medium article | `social-devto` or `social-medium` + cross-cutting + `content-geo` + `content-formats`; scored with the Article weights (Blog weights under 1500 words) |
| 600–1500 words, opinionated, conversational | Blog post (content quality) | cross-cutting + `content-geo` + `content-formats` |
| 1500–3000+ words, sections, citations, formal voice | Article (content quality) | cross-cutting + `content-geo` + `content-formats` |

Cross-cutting skills always loaded: `content-voice`, `content-humanize`, `content-grounding`.

Don't guess between blog and article — confirm if borderline. Don't guess platform if no cue — ask which one. The axis-weight table below has four columns; a surface scored with another type's weights says so in the report header. Phoenix-style verdicts stay X-only.

This audit covers the writing itself: hook, dwell, slop, voice, specificity, structure, grounding, safety, topic fit, and answer-first structure for long-form.

### Inputs the audit accepts

Required: the content (file path or pasted text).

Optional context that sharpens the score (ask for missing items on a thorough audit, otherwise mark the axis "Unscored"): target platform, niche, account stage, audience, primary keyword, anchor accounts, brand voice notes (check memory first), posting time.

### Score axes

Every audit returns the same axis set. Weight per axis varies by content type — see the weight table below. Score each 0–10 (10 = nothing to fix, 0 = blocking issue). Missing context = "Unscored — needs {context}".

| Axis | What it measures |
|---|---|
| Hook | First sentence / first 280 chars / title — does it earn the next read? |
| Dwell risk | Visual density, paragraph length, scroll-friction. Low score = predicted scroll-past. |
| Slop risk | AI-template shape, recycled hook, motivational fluff, synonym rotation. An editorial judgment: never cite an AI-detector percentage as evidence (detectors are unreliable on edited text). |
| Voice | Match to documented brand voice; first-person claims owned by the speaker; register and rhythm that fit the venue (no contraction or sentence-length quotas). |
| Specificity | Real numbers, named tools, named people, dated events vs. abstractions. |
| Structure | Format fits the query's intent (`content-formats` table) with that format's must-haves; one idea per unit; transitions; conclusion landing. |
| Grounding | Fabrication risk on named entities, stats, quotes, versions, URLs. |
| Safety + brand-safety | PTOS category risk (X-specific); ad-adjacency risk (MediumRisk verdict). |
| Topic fit | Niche/embedding fit and audience-cluster match for the content's intended surface. |
| Answer-first / GEO | Each section leads with the answer in 1–2 sentences; extractable passages; sourced from `content-geo`. Blog and article only. |

### Axis weights by content type

Normalise the per-axis 0–10 scores using these weights to get the 0–100 overall.

| Axis | X post/thread | LinkedIn | Blog | Article |
|---|---|---|---|---|
| Hook | 20 | 18 | 14 | 12 |
| Dwell risk | 18 | 14 | 10 | 8 |
| Slop risk | 15 | 14 | 12 | 10 |
| Voice | 10 | 10 | 14 | 12 |
| Specificity | 10 | 10 | 14 | 14 |
| Structure | 5 | 10 | 14 | 14 |
| Grounding | 10 | 10 | 12 | 14 |
| Safety + brand-safety | 7 | 6 | 4 | 4 |
| Topic fit | 5 | 8 | 4 | 4 |
| Answer-first / GEO | — | — | 2 | 8 |

Weights sum to 100. Any axis flagged "Unscored" is dropped and the remainder re-normalised; report the dropped weight as "{N} pts unscored" so the reader sees coverage.

### Phoenix-style verdict (X surfaces only)

After scoring, map the X audit to one of four verdicts. This is the harness's predicted reach posture — not a real Phoenix prediction, but a structured projection based on the algorithm mechanisms encoded in `social-x`.

| Verdict | Trigger |
|---|---|
| Pass | Overall ≥ 75 AND no axis < 5 AND no PTOS / MediumRisk flag |
| Borderline | Overall 55–74, or one axis < 5 with no kill-switch flag |
| Likely-Suppressed | Overall < 55, or Dwell-risk ≤ 3, or Slop-risk ≤ 3, or MediumRisk brand-safety flag |
| Kill-Switch-Risk | Any PTOS category positive, or muted-keyword certainty, or Safety axis ≤ 2 |

For non-X content, omit the verdict and use the overall score band only: Strong (≥ 80) / Ship-ready (65–79) / Needs work (45–64) / Rewrite (< 45).

### Severity matrix

Each finding gets a severity tier.

- Critical — blocks reach or ships a fabrication. Fix before publishing. (Kill-switch flag, fabricated stat, first-person experience with no author source, anonymous byline on YMYL, intent mismatch, information-gain-zero, missing hook.)
- Moderate — degrades performance noticeably. Fix when possible. (Slop-shape hook, dwell-risk wall of text, weak title/meta, missing answer-first block, voice drift.)
- Minor — polish. Optional. (One filler phrase, single data-free section, single passive sentence in an active piece.)

When the severity is ambiguous, default UP — flag as Critical and let the user decide to defer. Never silently downgrade safety findings.

### Finding format

Every finding follows this shape so reports are diff-able and tools can parse them.

```
[SEVERITY] [AXIS] {one-line title}
  Where: {file:line OR section name OR "hook" / "post 2" / "conclusion"}
  Evidence: "{verbatim quote from the content, ≤ 25 words}"
  Why it matters: {one sentence tying to a specific algorithm or quality mechanism}
  Fix direction: {one sentence — what to change, not how to write it}
  Suggested rewrite: {optional — only when the fix is local and short; otherwise omit}
```

No suggested rewrites for structural findings (those are scoping decisions for the edit session). No suggested rewrites for findings the auditor flagged as "needs verification" — preservation is the default.

### Escalation rule

If a check cannot be completed, do not infer. Flag as "Unverified" with a precise reason:

- Missing input context (no niche given, no target keyword) → list as "Unscored axis — needs {context}; ask the user before re-scoring."
- Named entity the model has no training-data confidence on → "Unverified entity — would need {websearch / user source} before scoring grounding."
- Live signal needed (current SERP, current AIO presence) → "Unverified — needs live SERP fetch."
- Source content too short to evaluate an axis → "Unscored — not enough signal."

Never grade an axis from a guess. Unverified beats wrong.

### Audit session

- Parse: read the file path or pasted text. Pull the declared platform or format, niche, audience, account stage, primary keyword, anchor accounts, and brand voice notes from the request. In parallel, recall brand voice and past audit findings on similar content from memory. Brand voice is required input to the Voice axis. Persist nothing after scoring: an audit does not write memory.
- Detect, then confirm: state the detected content type at the top of every audit. If the user redirects, re-route the skills and re-score. If the type is borderline, ask one question ("X post or LinkedIn post?", "Blog or article?") and stop.
- Read each platform skill and cross-cutting skill before scoring against it. Don't recall platform rules from training, and don't invent rubric items, axis weights, or verdict mappings.
- Emit a finding for every axis below 8/10 and every issue the rubric flags.
- Never downgrade a safety, grounding, or kill-switch finding to make a verdict look better.
- Don't invent benchmarks, quote algorithm weights that are not in an activated skill, or predict views, click-through, or ranking. The verdict is a structured projection from the rubric, not a prediction.
- When the user pushes back on a finding, re-read the relevant skill rule and restate it verbatim. If the rule does not back the finding, withdraw it. If it does, hold the line and explain.
- Missing context that would lift the score: render the report with the affected axes Unscored, list the missing context, and offer to re-audit when the user provides it.
- "Just score it, don't ask", or an autonomous, non-interactive brief: audit with what is available and state the assumed content type at the top. Unscored axes stay Unscored.
- "Score only, no findings": render the score block and verdict only.
- A whole folder of drafts: audit one piece at a time.
- Save only when the user asks. The slug is the first six lowercase-kebab words of the content's hook or title. After saving, give the path and the handoff line.

### Output report template

Save as in-conversation rendering by default. If user says "save it," write to `content-audit-{slug}-{YYYY-MM-DD}.md` in CWD. Never mutate the source file.

```
# Content Audit — {filename or "Pasted draft"}

Detected type: {X post / X thread / blog / article / ...}
Skills consulted: {social-x, content-voice, content-humanize, content-grounding, ...}
Context provided: {list}
Context missing (axes affected): {list, if any}

## Score

Overall: {N}/100 — {verdict band}
{Phoenix verdict line, X only}

| Axis | Score | Weight | Weighted |
|---|---|---|---|
| Hook | 7/10 | 20 | 14.0 |
| Dwell risk | 4/10 | 18 | 7.2 |
| ...

## Critical findings

[CRITICAL] [AXIS] {title}
  Where: ...
  Evidence: "..."
  Why it matters: ...
  Fix direction: ...
  Suggested rewrite: ...

## Moderate findings
...

## Minor findings
...

## What's working

- {strength 1}
- {strength 2}

## Recommended next step

{One of:}
- Ready to publish — minor polish optional.
- Run an edit session to apply the {N} critical and {N} moderate fixes; paste this report or the file path as input.
- Rewrite recommended — structural issues; restart from a new outline.
- Get the missing context first ({list}) then re-audit.
```

## Examples

### Example — X single-post audit (abbreviated)

```
# Content Audit — pasted draft

Detected type: X post (single)
Skills consulted: social-x, content-voice, content-humanize, content-grounding
Context provided: niche=AI coding agents, account stage=mid (8k followers)
Context missing: none

## Score

Overall: 69/100 — Borderline
Phoenix verdict: Borderline — Dwell-risk axis at 4 is the choke point

| Axis | Score | Weight | Weighted |
|---|---|---|---|
| Hook | 8/10 | 20 | 16.0 |
| Dwell risk | 4/10 | 18 | 7.2 |
| Slop risk | 7/10 | 15 | 10.5 |
| Voice | 7/10 | 10 | 7.0 |
| Specificity | 6/10 | 10 | 6.0 |
| Structure | 5/10 | 5 | 2.5 |
| Grounding | 9/10 | 10 | 9.0 |
| Safety + brand-safety | 10/10 | 7 | 7.0 |
| Topic fit | 8/10 | 5 | 4.0 |

## Critical findings

[CRITICAL] [Dwell risk] Wall of text in first paragraph
  Where: post body, opening 3 lines
  Evidence: "Most teams don't realise that the actual problem with agents is not the model itself but rather..."
  Why it matters: First-screen non-dwell is a negative-weighted Phoenix signal; long unbroken text predicts scroll-past.
  Fix direction: Break the opening into 1-sentence-per-line; lead with the contrarian rule, not the setup.

## Moderate findings
...
```

### Example — blog post audit (abbreviated structure)

Same report shape; Answer-first / GEO axis populated; Phoenix verdict line omitted; band verdict from overall score.

## Checklist

Before returning a report:

- [ ] Content type detected explicitly and confirmed (or asked if ambiguous)
- [ ] All applicable platform + cross-cutting skills consulted (named in report header)
- [ ] Every axis has a score or an explicit "Unscored — needs {context}"
- [ ] Overall score uses the weight table for the detected type; un-scored weight re-normalised
- [ ] Phoenix verdict present for X; band verdict for everything else
- [ ] Every finding has severity, axis, where, evidence quote, why-it-matters, fix-direction
- [ ] Suggested rewrites only on local short fixes — not on structural findings
- [ ] Recommended next step routes to the right surface (publish / editor / outline / get-context)
- [ ] Report rendered in conversation; no source file mutated
- [ ] If saved, file path is `content-audit-{slug}-{YYYY-MM-DD}.md` in CWD

## Composition / References

Content-domain skills the harness composes with:
- `social-x`, `social-linkedin`, `social-threads`, `social-bluesky`, `social-mastodon`, `social-hackernews`, `social-reddit`, `social-facebook`, `social-instagram`, `social-tiktok`, `social-youtube`, `social-devto`, `social-medium` — platform rulebooks
- `content-voice` — voice / AI-pattern check
- `content-humanize` — 8-dimension humanization diagnostic (when Slop-risk score is low)
- `content-grounding` — fact-grounding triage for the Grounding axis
- `content-geo` — answer-first / extractable structure for the Answer-first / GEO axis

Used with:
- An edit session takes this report as its diagnosis and applies the fixes.
