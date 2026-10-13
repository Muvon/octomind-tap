---
name: content-locale-humanize-th
title: "Thai Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Thai (th) target text; auto-loads alongside content-locale-humanize when the target language is Thai."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Thai (th-TH), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: the weakest in this set. Searches found Thai AI-detection tools but no independently documented word- or phrase-level AI tells. Don't invent a plausible list to fill the gap; if a sourced list appears, add it here.

### Translationese from English

Lean on the structural checks, which are unusually visible in Thai:

- English sentence structure carried over: Thai has no articles or tense inflection and topicalizes differently.
- ถูก-passives copied from English; native Thai reserves ถูก mostly for adverse events and otherwise prefers active or topic-first sentences.
- Pronouns Thai would drop (คุณ, เขา, มัน) and stacked การ/ความ nominalizations mirroring English abstract nouns.
- Rhythm is hard to judge by eye without word spaces; read for natural clause breaks rather than word counts.

### Current norms

- No spaces between words; a space marks a clause or sentence break, full stops are not used in running text, and English-style comma density reads as translated.
- Polite particles (ครับ/ค่ะ) are gendered: in UI and documentation either avoid them or follow the brand voice, consistently.
- Spelling and transliteration follow the Royal Society of Thailand; formal and government contexts use Buddhist Era years (CE + 543).

## References

Reviewed 2026-10-12. No solid per-language AI-tell sourcing found. Norms: Royal Society of Thailand (ราชบัณฑิตยสภา) dictionary and transcription rules.
