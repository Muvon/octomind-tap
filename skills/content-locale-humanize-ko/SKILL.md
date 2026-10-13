---
name: content-locale-humanize-ko
title: "Korean Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Korean (ko) target text; auto-loads alongside content-locale-humanize when the target language is Korean."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Korean (ko-KR), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: moderate.

- Korean is a small share of typical LLM training data compared with English, so interference bleeds through more easily; weight interference and register findings slightly higher.
- Connector pileup: 그리고, 하지만, 그래서 chaining sentences mechanically instead of letting the logic connect.
- Adverb-modified generic verbs (-게, -이, -히) where a concrete verb would carry the meaning.
- 중요한 / 중요하다 measured as disproportionately overused against native baselines.

### Translationese (번역투)

- "~에 의해" passives, "~을/를 가지다" for "have", "~에 있어서", "~하는 것이 필요하다", and "~를 통해" everywhere.
- Pronouns 그/그녀 and plural -들 where Korean leaves them implicit; stacked -적 adjectives.

### Current norms

- Speech level: 합니다체 for formal documents and notices, 해요체 for most consumer apps and UI; pick one and hold it.
- Word spacing (띄어쓰기) and loanword spelling (외래어 표기법: 콘텐츠, 메시지) follow the National Institute of Korean Language; spacing errors read as machine output immediately.

## References

Reviewed 2026-10-12. AI tells: rebrandb.com, zdnet.co.kr, curious-500.com. Norms: [국립국어원](https://www.korean.go.kr/).
