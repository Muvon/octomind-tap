---
name: content-locale-humanize-ar
title: "Arabic Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Arabic (ar) target text — auto-loads alongside content-locale-humanize when the target language is Arabic."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(arabic)
  - match(\bar-(SA|EG|AE)\b)
  - match(\bArabic\b)
  - match(العربية)
  - semantic(check if this Arabic translation sounds native)
  - semantic(eliminate translationese from this Arabic text)
---

## Overview

Sourced calibration anchors for Arabic, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: the weakest of any language checked. Most published Arabic AI-word lists are direct translations of the English canon, not independently observed findings — treat any finding here as a starting hypothesis, not a confirmed tell.

Stock phrases: "في الختام" ("in conclusion"), "لا شك أن" ("there's no doubt that").

Beyond this thin list, lean harder on the structural checks in `content-locale-humanize` (interference, connector density, rhythm clustering) than on vocabulary matching — the vocabulary evidence for Arabic specifically is not solid.

## References

One Al Jazeera piece naming a handful of phrases; otherwise mostly translated-from-English lists.
