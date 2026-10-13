---
name: content-locale-humanize-hi
title: "Hindi Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Hindi (hi) target text; auto-loads alongside content-locale-humanize when the target language is Hindi."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Hindi (hi-IN), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: moderate; one specific, well-reasoned finding rather than a convergent word list.

- Over-Sanskritization: AI-generated Hindi reaches for formal tatsama vocabulary in casual or practical contexts where native speakers use everyday or Urdu-origin words. Check that vocabulary register matches the domain, not just that words are correct.
- Missing Hinglish: contemporary digital, informal, and conversational Hindi code-switches with English words and phrases naturally. Text that never code-switches in a casual blog, social post, or UI string likely reads as AI or translationese.

### Translationese from English

- "द्वारा" agent passives ("यह फ़ाइल उपयोगकर्ता द्वारा बनाई गई") where Hindi uses the active ("उपयोगकर्ता ने यह फ़ाइल बनाई"); "किया जाता है" everywhere.
- English clause order kept intact instead of Hindi verb-final structure.

### Current norms

- । (purna viram) ends sentences; lakh/crore grouping (12,34,567); follow house style on nukta (फ़, ज़) and on Devanagari vs Roman script for English terms, and hold it.
- Spelling follows the Central Hindi Directorate's standard orthography (मानक हिंदी वर्तनी).

## References

Reviewed 2026-10-12. AI tells: gptcleanuptools.com (Hindi AI Detector product page, self-reported rationale; a plausible hypothesis, not corpus-verified). Norms: Central Hindi Directorate (केंद्रीय हिंदी निदेशालय).
