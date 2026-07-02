---
name: content-locale-humanize-de
title: "German Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in German (de) target text — auto-loads alongside content-locale-humanize when the target language is German."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(german)
  - match(\bde-(DE|AT|CH)\b)
  - match(\bGerman\b)
  - match(\bDeutsch\b)
  - semantic(check if this German translation sounds native)
  - semantic(eliminate translationese from this German text)
---

## Overview

Sourced calibration anchors for German, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: blog-convergence only, not corpus research — treat as a weaker prior than Spanish or French.

Power adjectives: nahtlos, ganzheitlich, innovativ, zunehmend, zweifellos, zweifelsohne, letztendlich, hochwertig, effizient, skalierbar, unzählig, nuanciert.

Connectors: ferner, folglich, darüber hinaus, insbesondere, dennoch, daher, zudem, hingegen, infolgedessen.

Opener tic: "Ein weiterer wichtiger Aspekt…" starting consecutive paragraphs.

Stock closers: "Insgesamt", "Zusammenfassend ist festzuhalten".

Rhythm: sentences clustering 15–25 words throughout.

## References

walterwrites.ai, the-decoder.de, eology.de.
