---
name: design-ux-review
title: "UX Review: Heuristic Audit and Microcopy"
description: "Review a page or flow against Nielsen's heuristics with WCAG 2.2 AA spot checks, rate findings by severity, and rewrite failing microcopy in place."
license: Apache-2.0
compatibility: "A browser for live URLs and image viewing for screenshots; works from a described flow when neither is available."
capabilities: browser image-view
domains: designer
rules:
  - match((?i)\b(heuristics?|Nielsen)\b.{0,40}\b(rate|severity|findings|issues?|problems?)\b|\b(usability|UX)\s+(review|critique|pass|issues?|problems?)\b|\bheuristic\s+evaluation\b.{0,40}\b(flow|page|findings)\b)
  - match((?i)\b(review|critique|evaluate|look\s+at)\b.{0,40}\b(screenshots?|checkout|onboarding|landing\s+page|signup|form|navigation|information\s+architecture|help\s+center)\b)
  - match((?i)\b(microcopy|ux\s+writing|error\s+(messages?|handling)|validation\s+messages?|empty\s+states?|button\s+(labels?|text|copy))\b|\b(clearer|better)\s+(labels?|button\s+text)\b|\brewrite\b.{0,40}\b(error|validation|confirmation|messages?|labels?|button)\b)
  - match((?i)\b(friction|confusing)\b|\binformation\s+architecture\b)
  - semantic(which of these two designs is better for the user's task, 0.72)
  - semantic(review this checkout flow for usability problems and rate severity, 0.72)
  - semantic(rewrite the confusing error messages and button labels on this page, 0.72)
  - semantic(critique this screen against usability heuristics, 0.72)
---

## Overview

A UX review evaluates an interface, as a live page, a screenshot, or a described flow, against established usability heuristics and WCAG accessibility criteria. It rates each finding by severity, proposes the smallest fix, and rewrites the interface words that fail users. The critique is evidence-based and kind to the team but honest about the user's experience: it cites the heuristic, shows where it breaks, and never pads findings.

Use it for heuristic evaluations with severity ratings, WCAG 2.2 AA spot checks, UX writing (labels, calls to action, errors, empty states, onboarding), form and flow critique, information-architecture review, and design decisions that need usability evidence. A spot check is not a full accessibility audit, and the review does not cover logos, naming, marketing page copy, SEO structure, or frontend implementation.

## Mental model

Critique without a task is decoration. A checkout for stressed commuters and a dashboard for daily power users fail differently, so every review starts from who uses the interface, for what task, on what device. Hesitation in an expert reviewer is a stop sign for a real user. Severity is impact times frequency times persistence on the primary path, so ten cosmetic notes never outrank one task blocker.

## Rules

Method:

1. Establish context: who uses this, for what task, on what device. Ask for the top user task if it is not given.
2. Walk the flow. With a URL, open it in the browser, attempt the primary task as a first-time user would, and screenshot the checkpoints. Note where you hesitated.
3. Evaluate against the heuristics and the WCAG spot-check list below. Every finding states what, where (screenshot or element), which principle, severity 0 to 4, and the smallest fix.
4. Rewrite the words. For microcopy findings, give the replacement text in place, not advice about text.
5. Prioritize by severity times frequency on the primary task path.
6. Deliver the report. Save it to a file when substantial. Record the product's context and past findings for follow-up reviews.

Severity scale (Nielsen):

| Score | Meaning |
|---|---|
| 0 | Not a problem |
| 1 | Cosmetic |
| 2 | Minor: annoys, doesn't block |
| 3 | Major: delays or derails the task; fix soon |
| 4 | Catastrophic: blocks the task or loses data; fix before ship |

The 10 heuristics, applied and not recited: visibility of status (loading, saving, progress); match to the real world (user words, not the org chart); user control (undo, escape, back); consistency (internal first, platform second); error prevention (constraints beat validation beats error messages); recognition over recall (show options, don't demand memory); flexibility (shortcuts for experts); minimalist design (every element competes with the task); good error recovery; help where the need is (inline, not manuals).

AI features add their own checks (Microsoft HAX guidelines; Google PAIR): say what the AI can and can't do, label generated content, show sources or confidence where a wrong answer costs something, make output editable and undoable, and keep a non-AI path for critical tasks.

WCAG 2.2 AA spot checks:

- Text contrast at least 4.5:1 (3:1 for large text and UI components); WCAG 2.x ratios, not APCA.
- Targets at least 24 by 24 CSS px (2.5.8); 44 by 44 is comfortable.
- Keyboard: every action reachable, focus visible and not hidden behind sticky headers or banners (2.4.11), no traps.
- Images have meaningful alt text; form inputs have real labels (a placeholder is not a label); no meaning carried by colour alone; visible label matches the accessible name.
- Drag actions have a single-pointer alternative (2.5.7); help sits in the same relative place across pages (3.2.6); users aren't made to re-enter what they already gave (3.3.7); login works without memory or puzzle tests, so allow paste, password managers, and passkeys (3.3.8).
- Flag, cite the criterion number, and note that this is a spot check, not certification. Verify criterion details by web search when unsure; cite, don't recall.

Forms, where conversion dies: one column; labels above fields; ask only what you will use, because every field costs completion; inline validation on blur, not on submit; error text says what happened and how to fix it, next to the field; never clear the form on error; autofill, correct input types (email, tel), and autocomplete attributes on; never block paste.

Microcopy craft:

- Buttons say what happens ("Save changes", not "Submit" or "OK"). Sentence case everywhere.
- Error anatomy: what happened, then why (if useful), then what to do now. Never blame the user, never show bare codes.
- Empty states are onboarding: what belongs here and the one action to start.
- Confirmation dialogs name the consequence ("Delete 3 files?" with "Delete" and "Keep", never "Are you sure?" with "Yes" and "No").
- Numbers and specifics beat adverbs ("saves in about 2 s", not "blazing fast").

Critique discipline: cite the principle, not taste. "Violates recognition over recall (heuristic 6)" beats "feels clunky". Separate observation from interpretation. Acknowledge what works, since it also tells the team what to keep. When two patterns are defensible, say so and give the deciding question instead of faking certainty.

## Examples

- A URL arrives: walk the primary task in the browser, then produce the full report.
- A screenshot arrives: open the image, evaluate what is visible, and state what can't be assessed statically (states, keyboard, latency).
- "Write the error message, empty state, or onboarding copy": ask context questions only if the action is ambiguous, then give the copy in two variants, strict and friendly.
- "Which design is better?": judge both against the task and the heuristics, pick one, and name the deciding factor.
- A non-interactive brief: infer the primary task from the page's own call to action, state it as an assumption, and proceed.

## Output format

One paragraph of verdict (can a first-time user complete the primary task?), then a findings table with the columns number, location, finding, heuristic or WCAG reference, severity, and smallest fix. Then microcopy rewrites as before and after pairs, then a top-3 "fix this week" list. Save as `ux-review-<product>.md` when asked or when findings exceed about 10. Reference screenshots by checkpoint name.

## Checklist

- [ ] The primary user task is stated
- [ ] Every finding has a location, a principle, a severity from 0 to 4, and a smallest fix
- [ ] Findings are ordered by severity on the primary path and not padded
- [ ] Every microcopy finding carries replacement text
- [ ] Accessibility notes name the standard checked and say they are spot checks
- [ ] The report states what the evidence could not show

## Composition / References

- The `design-accessibility-audit` skill takes over when a full standards audit, conformance verdict, or statement is needed.
- The `design-user-research` skill covers evidence from interviews, feedback, and usability tests.
- Sources: Nielsen Norman Group heuristics and severity scale, WCAG 2.2, Microsoft HAX guidelines, Google PAIR.
