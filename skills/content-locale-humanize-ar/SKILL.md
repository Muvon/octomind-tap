---
name: content-locale-humanize-ar
title: "Arabic Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Arabic (ar) target text; auto-loads alongside content-locale-humanize when the target language is Arabic."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Arabic (Modern Standard Arabic unless the brief names a dialect), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: the weakest of the set. Most published Arabic AI-word lists translate the English canon rather than report independent findings; treat any item as a hypothesis.

- Stock phrases: "في الختام" (in conclusion), "لا شك أن" (there's no doubt that).
- Lean harder on the structural checks (interference, connector density, rhythm clustering) than on vocabulary matching.

### Translationese from English

- "يتم + مصدر" passives ("يتم تحديث البيانات") where a native writer uses the internal passive or active voice ("تُحدَّث البيانات").
- "من قِبَل" as a calque of the English agent "by"; dummy "قام بـ" + noun; "حيث" as an all-purpose connector.
- English word order and stacked pronouns; Latin punctuation (, ; ?) instead of ، ؛ ؟.

### Current norms

- Register: MSA for written product, documentation, and formal copy; Gulf, Egyptian, or Levantine dialect only when the brief targets that market and channel.
- Digits: Western (0–9) or Arabic-Indic (٠–٩) per market and house style; hold one choice. RTL layout with isolated LTR runs for code, URLs, and Latin brand names.

## References

Reviewed 2026-10-12. AI tells: one Al Jazeera piece naming a handful of phrases; otherwise translated-from-English lists. Norms: Unicode CLDR locale data; Arabic translation-criticism literature on English interference.
