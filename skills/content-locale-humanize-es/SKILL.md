---
name: content-locale-humanize-es
title: "Spanish Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Spanish (es) target text; auto-loads alongside content-locale-humanize when the target language is Spanish."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
domains: content
rules:
  - content(spanish)
  - match(\bes-(ES|MX|AR|419)\b)
  - match(\bSpanish\b)
  - match(\bespañol\b)
  - semantic(check if this Spanish translation sounds native)
  - semantic(eliminate translationese from this Spanish text)
---

## Overview

Calibration anchors and current norms for Spanish (es-ES and es-419 variants), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: solid; convergent, independently reported sources.

- Overused words: crucial, explorar/exploraremos, desafíos, cautivar, considerar, enfrentar, adoptar; the calque "sumergirse en".
- Connector pileup: además, sin embargo, por lo tanto, aunque, por otro lado.
- Stock openers: "Es importante tener en cuenta…", "Vale la pena señalar que…", "En conclusión…".
- Filler: muy, bastante, realmente, simplemente.

### Translationese from English

- Passive "ser + participio" where Spanish uses the pasiva refleja or active voice ("Los datos son procesados" → "Los datos se procesan").
- Gerundio de posterioridad ("Se cayó, rompiéndose la pierna"); "en base a" (prefer "con base en", "según").
- False friends: "aplicar a un puesto" (solicitar), "eventualmente" meaning finally, "remover" for quitar, "soportar" for ser compatible con.
- Possessives with body parts and belongings; capitalized months and weekdays; Title Case headings.

### Current norms

- Variant: vosotros only in es-ES; ustedes across es-419; voseo only when the brief targets Rioplatense audiences. Pick tú or usted once.
- RAE: "solo" and demonstratives take no accent; since 2023 an accent is allowed where the writer judges there is real ambiguity. Opening ¿ ¡ are required. RAE prefers «…», then “…”.
- Inclusive language: the RAE defends the generic masculine and rejects @, x, and -e endings ("todes"); Argentina barred inclusive forms in national public administration in 2024. Follow the client guide; otherwise use natural collective nouns (el personal, la ciudadanía) or paired forms sparingly.
- Check doubtful usage with FundéuRAE and the Diccionario panhispánico de dudas.

## References

Reviewed 2026-10-12. AI tells: adslzone.net, genbeta.com, pageon.ai. Norms: [RAE](https://www.rae.es/), [FundéuRAE](https://www.fundeu.es/).
