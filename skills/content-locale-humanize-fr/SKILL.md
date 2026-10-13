---
name: content-locale-humanize-fr
title: "French Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in French (fr) target text; auto-loads alongside content-locale-humanize when the target language is French."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
domains: content
rules:
  - content(french)
  - match(\bfr-(FR|CA|BE|CH)\b)
  - match(\bFrench\b)
  - match(\bfrançais\b)
  - semantic(check if this French translation sounds native)
  - semantic(eliminate translationese from this French text)
---

## Overview

Calibration anchors and current norms for French (fr-FR, fr-CA, fr-BE, fr-CH), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: solid; convergent, independently reported sources.

- Connector pileup: de plus, en outre, par ailleurs, donc, cependant, ainsi, nearly every paragraph.
- Calqued English metaphors: plonger dans, naviguer, s'embarquer.
- Power words: crucial, essentiel, vital. Stock: en constante évolution, tapisserie, nuance, en conclusion.
- Construction: "non seulement… mais aussi…" on repeat.

### Translationese from English

- Anglicisms: "faire du sens" (avoir du sens), "adresser un problème" (traiter), "supporter" for prendre en charge, "être en charge de" (être chargé de), "définitivement" for certainement, "opportunité" for occasion.
- Passive chains and possessives where French uses the article; Title Case headings; "2ème" for 2e.

### Current norms

- Typography (France): no-break space before : and narrow no-break space before ; ! ? and inside « ». Quebec (OQLF): no space before ; ! ?, space before :. Accented capitals (É, À) are standard.
- Register: vous for most brand and B2B copy; tu only when the brand guide uses it. Hold one.
- Inclusive writing: the 21 November 2017 circular excludes the point médian from official texts, and the Académie française opposes it. Follow the client guide; otherwise prefer doublets ("les candidates et les candidats") and epicene nouns.
- fr-CA vocabulary follows OQLF (courriel, clavardage) where the audience is Québécois.

## References

Reviewed 2026-10-12. AI tells: alexiacontenuillimite.substack.com, startups-nation.fr, gpthuman.ai. Norms: [OQLF Vitrine linguistique](https://vitrinelinguistique.oqlf.gouv.qc.ca/), Académie française, Lexique des règles typographiques en usage à l'Imprimerie nationale.
