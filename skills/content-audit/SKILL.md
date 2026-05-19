---
name: content-audit
title: "Content Audit Rubric & Scoring Harness"
description: "Read-only audit harness for content quality. Detects the content type (X post / X thread / LinkedIn / Threads / Bluesky / Mastodon / Hacker News / Reddit post, or blog / article), routes to the matching social-* skill plus the cross-cutting voice/humanize/grounding/geo checks, scores per-axis 0–10 + overall 0–100, emits a canonical findings report with severity tiers, evidence, and suggested rewrites. For X surfaces also emits a Phoenix-style verdict (Pass / Borderline / Likely-Suppressed / Kill-Switch-Risk). Single source of truth for the diagnostic shape — used by content:audit (read-only) and content:editor (diagnose-then-edit)."
license: Apache-2.0
compatibility: "Composes with content-domain skills only: social-*, content-voice, content-humanize, content-grounding, content-geo. Read-only — never mutates source files. Requires filesystem-read for file inputs."
domains: content
rules:
  - content(audit)
  - content(score)
  - content(review)
  - content(diagnose)
  - session(audit)
  - match(\b(audit|score|review|diagnose|grade|critique)\s+(this|my|the|a)\s+(post|thread|tweet|article|blog|draft|copy)\b)
  - match(\b(how\s+(good|strong|viral)\s+is\s+this)\b)
  - match(\b(will\s+this\s+(work|rank|perform|land))\b)
  - match(\b(check|inspect)\s+.{0,40}before\s+(posting|publishing|shipping)\b)
  - semantic(audit this post before I publish)
  - semantic(score this draft against the algorithm)
  - semantic(tell me what will fail in this content)
---

## Overview

The shared rubric for scoring any piece of content the system writes for. The audit agent uses it to produce read-only reports. The editor agent uses it to produce the diagnosis that drives its rewrites. Same rubric, same vocabulary, same report shape — the only difference is what happens after the report is rendered.

The harness does three things: detect what kind of content this is, route to the platform-specific knowledge skill, and grade the content with a structured per-axis score plus a prioritized findings list. It never writes to the source file.

## Mental model

An audit is intent-versus-execution: what does this content type need to win, what does this draft actually deliver, where is the gap, and how cheap is each fix.

Three constraints keep the harness useful instead of confusing:

- Platform skills own the rules; the harness owns the grading. `social-x` knows what good X looks like; this skill knows how to count, weight, and report what it finds. Never restate platform rules here — read them from the activated skill.
- One canonical report shape across every content type. Same headers, same severity tiers, same axis vocabulary. Only the weights on each axis change per content type. Skim-able regardless of input.
- Read-only — the auditor renders the report and stops. Suggested rewrites are proposals inside the report, never disk writes. To apply, hand off to `content:editor`.

## Instructions

### Content-type detection

Read the input. Match against these signatures. If signal is ambiguous, ask the user once before scoring.

| Signature | Type | Routed skills |
|---|---|---|
| ≤ 280 chars, no thread markers, single block | X post | `social-x` + cross-cutting |
| 2+ blocks separated by blank lines or "—" / "Post N" markers, each ≤ 280 chars | X thread | `social-x` + cross-cutting |
| ≤ 3000 chars, conversational, no formal sections | LinkedIn post | `social-linkedin` + cross-cutting |
| Similar to X but with different platform context cue | Threads / Bluesky / Mastodon / Reddit / HN | matching `social-<platform>` + cross-cutting |
| 600–1200 words, opinionated, conversational | Blog post (content quality) | cross-cutting + `content-geo` |
| 1500–3000+ words, sections, citations, formal voice | Article (content quality) | cross-cutting + `content-geo` |

Cross-cutting skills always loaded: `content-voice`, `content-humanize`, `content-grounding`.

Don't guess between blog and article — confirm if borderline. Don't guess platform if no cue — ask which one.

This audit covers content quality — voice, hook, dwell, slop, structure, specificity, grounding, safety, topic fit, and answer-first structure for long-form. The rubric stays focused on what makes the writing itself work.

### Inputs the audit accepts

Required: the content (file path or pasted text).

Optional context that sharpens the score — ask for any that are missing if the user wants a thorough audit, otherwise note as "Unscored axis":
- Target platform / format (if not auto-detectable)
- Account / brand niche
- Account stage (new account, established, large)
- Target audience
- Primary keyword (for SEO content)
- Anchor accounts (for X / LinkedIn)
- Brand voice notes (pull from memory before asking)
- Intended posting time / cadence (for social)

### Score axes

Every audit returns the same axis set. Weight per axis varies by content type — see the weight table below. Score each 0–10 (10 = nothing to fix, 0 = blocking issue). Missing context = "Unscored — needs {context}".

| Axis | What it measures |
|---|---|
| Hook | First sentence / first 280 chars / title — does it earn the next read? |
| Dwell risk | Visual density, paragraph length, scroll-friction. Low score = predicted scroll-past. |
| Slop risk | AI-template shape, recycled hook, motivational fluff, synonym rotation. |
| Voice | Match to documented brand voice; first-person specificity; contractions; rhythm variation. |
| Specificity | Real numbers, named tools, named people, dated events vs. abstractions. |
| Structure | Format-appropriate sectioning, one-idea-per-unit, transitions, conclusion landing. |
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

- Critical — blocks reach or ships a fabrication. Fix before publishing. (Kill-switch flag, fabricated stat, anonymous byline on YMYL, intent mismatch, information-gain-zero, missing hook.)
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

No suggested rewrites for structural findings (those are scoping decisions for the editor agent). No suggested rewrites for findings the auditor flagged as "needs verification" — preservation is the default.

### Escalation rule

If a check cannot be completed, do not infer. Flag as "Unverified" with a precise reason:

- Missing input context (no niche given, no target keyword) → list as "Unscored axis — needs {context}; ask the user before re-scoring."
- Named entity the model has no training-data confidence on → "Unverified entity — would need {websearch / user source} before scoring grounding."
- Live signal needed (current SERP, current AIO presence) → "Unverified — needs live SERP fetch."
- Source content too short to evaluate an axis → "Unscored — not enough signal."

Never grade an axis from a guess. Unverified beats wrong.

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
| Dwell risk | 4/10 | 15 | 6.0 |
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
- Run `content:editor` to apply the {N} critical and {N} moderate fixes.
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

Overall: 62/100 — Borderline
Phoenix verdict: Borderline — Dwell-risk axis at 4 is the choke point

| Axis | Score | Weight | Weighted |
|---|---|---|---|
| Hook | 8/10 | 20 | 16.0 |
| Dwell risk | 4/10 | 15 | 6.0 |
| Slop risk | 7/10 | 15 | 10.5 |
| Voice | 7/10 | 10 | 7.0 |
| Specificity | 6/10 | 10 | 6.0 |
| Structure | 5/10 | 5 | 2.5 |
| Grounding | 9/10 | 10 | 9.0 |
| Safety + brand-safety | 10/10 | 10 | 10.0 |
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
- `social-x`, `social-linkedin`, `social-threads`, `social-bluesky`, `social-mastodon`, `social-hackernews`, `social-reddit` — platform rulebooks
- `content-voice` — voice / AI-pattern check
- `content-humanize` — 8-dimension humanization diagnostic (when Slop-risk score is low)
- `content-grounding` — fact-grounding triage for the Grounding axis
- `content-geo` — answer-first / extractable structure for the Answer-first / GEO axis

Used by agents:
- `content:audit` — read-only orchestrator, produces report only
- `content:editor` — uses the diagnosis to drive surgical edits
