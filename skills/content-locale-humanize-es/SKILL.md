---
name: content-locale-humanize-es
title: "Spanish Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Spanish (es) target text — auto-loads alongside content-locale-humanize when the target language is Spanish."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(spanish)
  - match(\bes-(ES|MX|AR|419)\b)
  - match(\bSpanish\b)
  - match(\bespañol\b)
  - semantic(check if this Spanish translation sounds native)
  - semantic(eliminate translationese from this Spanish text)
---

## Overview

Sourced calibration anchors for Spanish, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: solid. Spanish has the most convergent, independently-reported sourcing of any language checked so far.

Overused words: crucial, explorar/exploraremos, desafíos, cautivar, considerar, enfrentar, adoptar.

Connector pileup: además, sin embargo, por lo tanto, aunque, por otro lado.

Stock openers: "Es importante tener en cuenta…", "Vale la pena señalar que…", "En conclusión…".

Filler: muy, bastante, realmente, simplemente.

## References

adslzone.net, genbeta.com, pageon.ai.
