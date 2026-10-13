---
name: content-locale-humanize-de
title: "German Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in German (de) target text; auto-loads alongside content-locale-humanize when the target language is German."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
domains: content
rules:
  - content(german)
  - match(\bde-(DE|AT|CH)\b)
  - match(\bGerman\b)
  - match(\bDeutsch\b)
  - semantic(check if this German translation sounds native)
  - semantic(eliminate translationese from this German text)
---

## Overview

Calibration anchors and current norms for German (de-DE, de-AT, de-CH), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: blog convergence only, not corpus research; treat as a weaker prior than Spanish or French.

- Power adjectives: nahtlos, ganzheitlich, innovativ, zunehmend, zweifellos, zweifelsohne, letztendlich, hochwertig, effizient, skalierbar, unzählig, nuanciert.
- Connector pileup: ferner, folglich, darüber hinaus, insbesondere, dennoch, daher, zudem, hingegen, infolgedessen.
- Opener tic: "Ein weiterer wichtiger Aspekt …" on consecutive paragraphs. Stock closers: "Insgesamt", "Zusammenfassend ist festzuhalten".
- Rhythm: sentences clustering at 15–25 words throughout.

### Translationese from English

- "in 2026" instead of "2026" or "im Jahr 2026".
- Split compounds ("Marketing Strategie") instead of "Marketingstrategie" or "Marketing-Strategie"; genitive apostrophes ("Peter's").
- Title Case headings; German capitalizes nouns only.
- Passive and "von" chains mirroring English; possessive pronouns where German uses the article.
- False friends: "realisieren" for bemerken, "eventuell" for schließlich, "Sinn machen" (now common, but "Sinn ergeben" reads better in formal text).

### Current norms

- Register: choose du or Sie from the brand guide (consumer tech often du; B2B, finance, and public sector usually Sie), never mix, and capitalize Sie/Ihr.
- Gender-inclusive language: the Rat für deutsche Rechtschreibung's rules in force since 1 July 2024 treat word-internal characters (Genderstern, Doppelpunkt, Unterstrich) as outside core orthography, and several Länder bar them in schools and administration (Bavaria and Hesse from 2024, Saxony from August 2025). Follow the client guide. Without one, use neutral forms (Studierende, Team, Fachleute) or paired forms consistently; don't add or strip gender characters on your own.
- Regional: de-CH uses ss for ß and «…» quotes; de-AT vocabulary (Jänner, heuer) where the audience is Austrian.

## References

Reviewed 2026-10-12. AI tells: walterwrites.ai, the-decoder.de, eology.de. Norms: [Rat für deutsche Rechtschreibung](https://www.rechtschreibrat.com/), Duden.
