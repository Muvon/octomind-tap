---
name: content-locale-humanize-it
title: "Italian Native-Fluency Calibration"
description: "Per-language calibration anchors for detecting AI-slop and translationese in Italian (it) target text; auto-loads alongside content-locale-humanize when the target language is Italian."
license: Apache-2.0
compatibility: "Calibration data only; no tools required. Network access helps for usage checks."
domains: content
rules:
  - content(italian)
  - match(\bit-(IT|CH)\b)
  - match(\bItalian\b)
  - match(italiano)
  - semantic(check if this Italian translation sounds native)
  - semantic(eliminate translationese from this Italian text)
---

## Overview

Calibration anchors and current norms for Italian (it-IT, it-CH), feeding content-locale-humanize's dimensions. A calibration aid, not the checklist; reason natively beyond it.

## Rules

### AI tells

Sourcing confidence: solid; convergent across independent Italian-language sources.

- Power adjectives: dinamico, efficiente, innovativo, stimolante, cruciale, fondamentale.
- Connector pileup: inoltre, tuttavia, nonostante, quindi, perciò, dunque, di conseguenza.
- Stock phrases: "È interessante notare che", "Un aspetto cruciale", "Vale la pena menzionare", "In conclusione" / "per concludere" closing almost every piece.
- Overrepresented: optare, efficienza, agevolare, massimizzare, integrazione, ottimizzazione, "soluzione efficace", "scenario in evoluzione".

### Translationese from English

- False friends: "in accordo a" (secondo), "realizzare" for rendersi conto, "eventualmente" meaning finally, "processare" for elaborare, "supportare" for essere compatibile con.
- Passive and possessive pileups; Title Case headings.

### Current norms

- Accents and apostrophes: perché, poiché (acute), è (grave); "un po'", "qual è" without apostrophe.
- Register: tu for most consumer tech, Lei (capitalized) for formal and institutional copy; hold one.
- Inclusive language: the Accademia della Crusca (2023 opinion for the Corte di Cassazione) advises against the asterisk and schwa, endorses feminine job titles (la ministra, l'avvocata), and accepts the unmarked masculine plural; a March 2025 Education Ministry circular excluded both signs from school communications. Follow the client guide.

## References

Reviewed 2026-10-12. AI tells: navigaweb.net, fastweb.it, compilatio.net, marcoilardi.it. Norms: [Accademia della Crusca](https://accademiadellacrusca.it/).
