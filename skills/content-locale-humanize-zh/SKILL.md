---
name: content-locale-humanize-zh
title: "Chinese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Chinese (zh) target text; auto-loads alongside content-locale-humanize when the target language is Chinese."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Chinese (zh-Hans and zh-Hant variants), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: the best quantitative backing of any non-English language here; a Renmin University news-lab corpus study measured roughly 4x higher parallel-sentence-structure rates in AI-generated Chinese than in human writing. Phrase-level tells below are practitioner discourse.

- Overused contrast pivots "不是…而是…" and "不仅…更…". Both are native constructions; the tell is frequency, mirroring English "not X, but Y".
- "首先…其次…最后" as a rhythm crutch when the content doesn't have exactly three steps.
- Stock frames: "在当今…的时代", "值得注意的是", "总而言之"; parallel four-character slogans stacked for effect.

### Translationese (翻译腔)

- 被-passives where Chinese uses active or topic-comment structure.
- Long 的 chains copied from English relative clauses; dummy verbs ("进行讨论" for "讨论", "作出决定").
- Overused 当…的时候, 一个, and pronouns (他, 她, 它, 我们) that Chinese would drop.

### Current norms

- Variant is more than script. zh-Hans (mainland, Singapore) vs zh-Hant (Taiwan, Hong Kong) differ in vocabulary (软件/軟體, 视频/影片, 网络/網路, 信息/資訊) and quotes (“” vs 「」); automatic script conversion is not localization.
- Punctuation: full-width ，。、；：？！ per GB/T 15834-2011; 《》 for titles; …… and —— as two-character marks. Spacing between Chinese and Latin text or digits follows the house style (common in tech docs, not required by the national standard); hold it throughout.

## References

Reviewed 2026-10-12. AI tells: Renmin University 新闻坊 (RUC Journalism Studio) news-lab study; Chinese practitioner guides. Norms: GB/T 15834-2011 标点符号用法.
