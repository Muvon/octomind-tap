---
name: content-locale-humanize-it
title: "Italian Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Italian (it) target text — auto-loads alongside content-locale-humanize when the target language is Italian."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(italian)
  - match(\bit-(IT|CH)\b)
  - match(\bItalian\b)
  - match(italiano)
  - semantic(check if this Italian translation sounds native)
  - semantic(eliminate translationese from this Italian text)
---

## Overview

Sourced calibration anchors for Italian, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: solid — convergent across multiple independent Italian-language sources.

Power adjectives: dinamico, efficiente, innovativo, stimolante, cruciale, fondamentale.

Connector pileup: inoltre, tuttavia, nonostante, quindi, perciò, dunque, di conseguenza.

Stock phrases: "È interessante notare che" (opens elaborations), "Un aspetto cruciale" (opens central paragraphs), "Vale la pena menzionare" (flags minor details as significant), "In conclusione" / "per concludere" (closes almost every response).

Overrepresented nouns/verbs: optare, efficienza, agevolare, massimizzare, istituzione, integrazione, ottimizzazione, "soluzione efficace", "scenario in evoluzione".

## References

navigaweb.net, fastweb.it, compilatio.net, marcoilardi.it.
