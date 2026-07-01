---
name: content-locale-humanize-fr
title: "French Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in French (fr) target text — auto-loads alongside content-locale-humanize when the target language is French."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(french)
  - match(\bfr-(FR|CA|BE|CH)\b)
  - match(\bFrench\b)
  - match(\bfrançais\b)
  - semantic(check if this French translation sounds native)
  - semantic(eliminate translationese from this French text)
---

## Overview

Sourced calibration anchors for French, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: solid. French has the most convergent, independently-reported sourcing of any language checked so far.

Connector pileup: de plus, en outre, par ailleurs, donc, cependant, ainsi — nearly every paragraph.

Cliché metaphors (English AI-isms calqued): plonger dans, naviguer, s'embarquer.

Power words: crucial, essentiel, vital.

Stock: en constante évolution, tapisserie, nuance, en conclusion.

Construction: "non seulement… mais aussi…".

## References

alexiacontenuillimite.substack.com, startups-nation.fr, gpthuman.ai.
