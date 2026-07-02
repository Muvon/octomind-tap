---
name: content-locale-humanize-pt
title: "Portuguese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Portuguese (pt) target text — auto-loads alongside content-locale-humanize when the target language is Portuguese."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(portuguese)
  - match(\bpt-(BR|PT)\b)
  - match(\bPortuguese\b)
  - match(português)
  - semantic(check if this Portuguese translation sounds native)
  - semantic(eliminate translationese from this Portuguese text)
---

## Overview

Sourced calibration anchors for Portuguese, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: moderate — listicle-level convergence (multiple independent sites), not corpus research.

Overused words: crucial, jornada (calque of English AI-cliché "journey" as a metaphor, not literal travel).

Watch for the same connector-pileup and stock-opener patterns documented for Spanish and French — Portuguese AI output leans on the same "além disso"-class transitions. Distinguish pt-BR from pt-PT register and vocabulary; don't apply European Portuguese conventions to a Brazilian-audience piece or vice versa.

## References

humanizartextos.com, gowinston.ai.
