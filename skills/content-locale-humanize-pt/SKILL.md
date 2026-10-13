---
name: content-locale-humanize-pt
title: "Portuguese Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Portuguese (pt) target text; auto-loads alongside content-locale-humanize when the target language is Portuguese."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
domains: content
rules:
  - content(portuguese)
  - match(\bpt-(BR|PT)\b)
  - match(\bPortuguese\b)
  - match(português)
  - semantic(check if this Portuguese translation sounds native)
  - semantic(eliminate translationese from this Portuguese text)
---

## Overview

Calibration anchors and current norms for Portuguese (pt-BR, pt-PT), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: moderate; listicle-level convergence across independent sites, not corpus research.

- Overused words: crucial, jornada (calque of the English AI metaphor "journey").
- The same connector and opener patterns as Spanish and French: "além disso", "vale ressaltar", "é importante destacar", "em suma".

### Translationese from English

- pt-BR gerundismo ("vou estar enviando" for "will be sending"; use "vou enviar").
- False friends: "aplicar para uma vaga" (candidatar-se), "realizar" for perceber, "eventualmente" meaning finally, "suportar" for ser compatível com.
- Possessive overuse ("seu/sua" everywhere), "foi feito por" passives, Title Case headings.

### Current norms

- Never mix variants. pt-BR: você, "estou fazendo", celular, tela, usuário, arquivo, “…”. pt-PT: tu or você by register, "estou a fazer", telemóvel, ecrã, utilizador, ficheiro, «…».
- Spelling follows the 1990 Orthographic Agreement, mandatory in Brazil and Portugal; residual differences remain (pt-BR "fato", pt-PT "facto").

## References

Reviewed 2026-10-12. AI tells: humanizartextos.com, gowinston.ai. Norms: Vocabulário Ortográfico da Língua Portuguesa (ABL; Instituto de Lexicologia e Lexicografia da Língua Portuguesa).
