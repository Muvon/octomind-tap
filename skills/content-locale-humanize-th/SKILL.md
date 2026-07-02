---
name: content-locale-humanize-th
title: "Thai Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Thai (th) target text — auto-loads alongside content-locale-humanize when the target language is Thai."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(thai)
  - match(\bth-TH\b)
  - match(\bThai\b)
  - match(ภาษาไทย)
  - semantic(check if this Thai translation sounds native)
  - semantic(eliminate translationese from this Thai text)
---

## Overview

Sourced calibration anchors for Thai, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: weakest of any language in this set. A targeted search turned up Thai-specific AI-detection tooling but no independently-documented word-level or phrase-level AI tells — don't invent a plausible-sounding list to fill the gap.

Lean entirely on the structural checks in `content-locale-humanize` for Thai: source-syntax interference (Thai has no articles, no verb tense inflection, and a different clause-topicalization pattern than English — literal English sentence structure carried into Thai is unusually visible), sentence-rhythm clustering, connector-pileup, and paragraph-opener templating. Thai's lack of spaces between words and different clause-boundary conventions also make burstiness/rhythm judgments harder to make by eye — read for natural clause-break rhythm rather than word-count.

If a genuine Thai-specific AI-tell word list becomes available, add it here — this file exists as the attachment point.

## References

No solid per-language sourcing found as of this writing; see Overview.
