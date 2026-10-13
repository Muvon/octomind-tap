---
name: content-locale-humanize-ja
title: "Japanese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Japanese (ja) target text; auto-loads alongside content-locale-humanize when the target language is Japanese."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
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

Calibration anchors and current norms for Japanese (ja-JP), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: anecdotal blog discourse, not quantitative research.

- Katakana loanwords where a native term exists: インサイト, アウトプット, スケーラビリティ.
- Hedge endings such as「〜ではないでしょうか」; SEO-blog closers such as「いかがでしたか」.
- Uniformly formal, emotionally flat register; the same phrase repeated within a passage instead of natural rephrasing.

### Translationese (翻訳調)

- Pronouns Japanese would drop: 彼, 彼女, それ, あなた.
- 「〜することができる」for every "can", 「〜によって」passives, 「〜を持っている」for "have".
- Long noun-modifying chains copied from English relative clauses; 「〜しましょう」for every "let's".

### Current norms

- Style: です・ます for most product, marketing, and help content; だ・である for reference or academic text. Never mix them in body text.
- Keigo: avoid double honorifics (おっしゃられる, ご覧になられる) and reflexive 「させていただく」; machine output tends to over-polish.
- Notation: full-width 、。 (the 2022 公用文作成の考え方 made 、 the default even in horizontal official text); half-width alphanumerics; follow the house rule for long-vowel katakana (コンピューター vs コンピュータ) and for spacing between Japanese and Latin text (the JTF translation style guide uses none). Hold each choice throughout.

## References

Reviewed 2026-10-12. AI tells: note.com and Zenn blog discourse; ai-souken.com. Norms: 文化審議会「公用文作成の考え方」(建議, 2022), JTF日本語標準スタイルガイド.
