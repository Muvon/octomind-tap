---
name: content-locale-humanize-ko
title: "Korean Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Korean (ko) target text — auto-loads alongside content-locale-humanize when the target language is Korean."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(korean)
  - match(\bko-KR\b)
  - match(\bKorean\b)
  - match(한국어)
  - semantic(check if this Korean translation sounds native)
  - semantic(eliminate translationese from this Korean text)
---

## Overview

Sourced calibration anchors for Korean, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: moderate, but with one structurally important, well-reasoned finding below.

Korean makes up roughly 1% of typical LLM training corpora versus roughly 60% English — meaning Korean output starts from a shakier native-fluency baseline than most other languages checked here. Weight interference and awkward-register findings a little more heavily for Korean; the model has comparatively less native Korean signal to draw on, so translationese bleeds through more easily.

Connector pileup: 그리고 (and), 하지만 (but), 그래서 (so) — mechanically chaining sentences instead of letting the logic connect on its own, a substitute for genuine narrative flow.

Overused descriptive-adverb endings: -게, -이, -히 — these tell rather than show; native Korean writing favors more concrete verbs over adverb-modified generic ones.

Frequency-outlier word: 중요한 (important) and its English cognate "significant" — both measured as disproportionately overused versus native baselines.

## References

rebrandb.com, zdnet.co.kr, curious-500.com.
