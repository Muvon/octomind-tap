---
name: content-locale-humanize-ja
title: "Japanese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Japanese (ja) target text — auto-loads alongside content-locale-humanize when the target language is Japanese."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(japanese)
  - match(\bja-JP\b)
  - match(\bJapanese\b)
  - match(日本語)
  - semantic(check if this Japanese translation sounds native)
  - semantic(eliminate translationese from this Japanese text)
---

## Overview

Sourced calibration anchors for Japanese, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: anecdotal blog discourse, not quantitative research.

Katakana-loanword overuse where a native term exists — インサイト (insight), アウトプット (output), スケーラビリティ (scalability).

Hedge endings like「〜ではないでしょうか」.

Overly formal/neutral register reading emotionally flat.

Same phrase repeated within one passage instead of natural rephrasing.

## References

note.com and Zenn blog discourse; ai-souken.com.
