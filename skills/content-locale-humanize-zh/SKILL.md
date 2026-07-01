---
name: content-locale-humanize-zh
title: "Chinese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Chinese (zh) target text — auto-loads alongside content-locale-humanize when the target language is Chinese."
license: Apache-2.0
compatibility: "Extends content-locale-humanize's AI-Slop & Translationese dimension. Load both together — this file has no rubric of its own."
domains: content
rules:
  - content(chinese)
  - match(\bzh-(Hans|Hant|CN|TW)\b)
  - match(\bChinese\b)
  - match(中文)
  - semantic(check if this Chinese translation sounds native)
  - semantic(eliminate translationese from this Chinese text)
---

## Overview

Sourced calibration anchors for Chinese, feeding `content-locale-humanize`'s AI-Slop & Translationese dimension. This is a calibration aid, not the checklist — reason natively beyond it (see the core skill's "why structure, not word lists" section).

## Instructions

Sourcing confidence: the best quantitative backing of any non-English language checked. A university news-lab corpus study measured roughly 4x higher parallel-sentence-structure rates in AI-generated Chinese text versus human-written text.

Calque tell: "不是…而是…" (a direct calque of the English "not X but Y" hedge-flip construction).

Triad-listing tell: "首先…其次…最后" (first…second…finally), used as a rhythm crutch rather than because the content has exactly three parts.

Watch for English-syntax interference in translated technical content: relative clauses and passive constructions that mirror English sentence structure instead of Chinese topic-comment structure.

## References

Renmin University 新闻坊 (RUC Journalism Studio) news-lab corpus study.
