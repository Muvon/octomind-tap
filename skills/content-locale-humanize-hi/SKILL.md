---
name: content-locale-humanize-hi
title: "Hindi Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Hindi (hi) target text — auto-loads alongside content-locale-humanize when the target language is Hindi."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(hindi)
  - match(\bhi-IN\b)
  - match(\bHindi\b)
  - match(हिन्दी|हिंदी)
  - semantic(check if this Hindi translation sounds native)
  - semantic(eliminate translationese from this Hindi text)
---

## Overview

Sourced calibration anchors for Hindi, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: moderate — one specific, well-reasoned, distinctive finding rather than a broad convergent word list.

Over-Sanskritization: AI-generated Hindi systematically reaches for formal Sanskrit-derived (tatsama) vocabulary even in casual or practical contexts, where a native speaker would naturally use colloquial or Urdu-derived (tadbhava) words instead. Formal register applied to an everyday topic is itself a tell — check whether the vocabulary register matches the domain, not just whether individual words are "correct."

Missing Hinglish: authentic contemporary Hindi — especially digital, informal, or conversational registers — code-switches with English words, phrases, and sometimes full clauses as a completely natural feature. AI-generated Hindi tends to avoid this entirely, producing an artificially "pure" Hindi that reads as stiffer and more formal than how the target audience actually writes or speaks. Flag content that never code-switches when the domain/register would call for it (casual blog, social, UI copy) as a likely AI/translationese signal.

## References

gptcleanuptools.com (Hindi AI Detector product page, self-reported linguistic rationale — treat as a plausible starting hypothesis, not corpus-verified).
