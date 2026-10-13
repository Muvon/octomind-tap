---
name: content-locale-humanize
title: "Locale-Native Humanization & Translationese Elimination"
description: "MQM-informed, structural-pattern diagnostic for making translated/localized content read as if a native speaker wrote it from scratch, in any target language. Detects translationese and AI-slop by pattern (interference, frequency outliers, rhythm, templating), not by a per-language word list."
license: Apache-2.0
compatibility: "Language-agnostic; works on any target locale. Network access helps for exact-phrase usage checks."
domains: content
rules:
  - content(localize)
  - content(native-fluency)
  - content(translationese)
  - match(\btranslationese\b)
  - match(\bnative[-\s]?(sound|fluen|speak|written)\b)
  - match(\bdoes\s+this\s+(sound|read)\s+native\b)
  - match(\bsounds?\s+(too\s+)?(like\s+)?(a\s+)?(translat(ed|ion)|machine[-\s]?translat)\b)
  - semantic(check if this translation sounds like a native speaker wrote it)
  - semantic(eliminate translationese and AI slop from this localized text)
  - semantic(score this translation for native fluency in the target language)
---

## Overview

A translation can be accurate and still read as translated: stiff syntax, over-explicit connectors, a few statistically overused words, uniform rhythm, English conventions leaking through. Native readers feel it as "not written by someone who thinks in this language," and it costs the same trust an English AI-slop draft does. Use this skill to audit and fix translated or AI-generated text in any target language.

Per-language word lists go stale and don't generalize, so this skill encodes structural patterns backed by translation-quality research (MQM, translation universals). Per-language calibration skills add sourced examples and current orthography norms; they are aids, not the boundary.

## Mental model

Corpus research on translated text identifies four universals that hold across language pairs (Baker; Volansky, Ordan and Wintner 2015 report high classification accuracy from these features alone):

- Simplification: shorter sentences, plainer words, lower lexical density, avoided subordination compared with native writing in the same register.
- Explicitation: spelling out what a native writer leaves implicit; connectors linking ideas that need no link.
- Interference (shining-through): source syntax, word order, idiom, or conventions bleeding into the target. Function-word and structure distributions alone identify translated text in corpus studies. Weight it heaviest.
- Normalization: a distinctive voice flattened into safe, generic phrasing.

AI-generated text in other languages shows the same meta-pattern seen in English: a handful of frequency-outlier "power words," connectors opening most paragraphs, sentences clustered in one length band, and English AI clichés calqued into the target (French "plonger dans," Spanish "sumergirse en," both doing the job of "delve into"). Multilingual models export English habits through translation. Check for the pattern; word lists only calibrate.

Sourcing for per-language tells is uneven: say so in the report when it is thin, and never present a blog-sourced word list as corpus evidence.

## Rules

### Calibrate to the domain first

Detect the domain (technical, legal, medical, marketing, academic, casual/UI, journalistic, literary; the same categories as content-translate's domain adaptation) and calibrate every dimension to it:

- Technical: established English loanwords ("commit," "webhook," "endpoint") are native in most tech registers; don't flag them. Short direct sentences are normal. Flag missing or wrong standard terminology instead.
- Legal: heavy subordination and formality are native; skip the rhythm penalty. Precision beats flow.
- Medical: recognized terms verbatim; check patient-facing versus professional register.
- Marketing: highest expectation of transcreation. Judge whether it lands with a native reader, not sentence-level fidelity.
- Academic: formal register is native; terminology and citation format matter more than rhythm.
- Casual/UI: shortest natural phrasing wins; brevity is not simplification.

### Six dimensions

Score each 0–10 (10 = fully native and faithful). Sum to X/60. Bands: Pass (48+), Borderline (34–47), Flagged (20–33), Critical (<20).

Dual gate, borrowed from MQM: MQM weights errors exponentially (default Neutral 0, Minor 1, Major 5, Critical 25), normalizes penalty points per word, and compares against a project pass threshold. Here, any single Critical finding fails the audit regardless of band. A fluent but wrong translation is not a pass.

1. Accuracy and completeness. Every claim, instruction, number, negation, and nuance present; nothing added or dropped. Mistranslation, omission, addition, untranslated fragments, and broken placeholders are Critical. Compare 2–3 load-bearing sentences against the source directly; back-translation catches only gross drift.
2. Native fluency. Interference (clause order and nesting mirroring the source), calques, unnatural collocations, simplification, explicitation, rhythm clustering (3+ consecutive sentences in one length band, judged by the target language's own range: German tolerates longer sentences than Japanese), and the read-aloud test: would a native say this to a colleague?
3. Register and formality. One T-V form, honorific level, or speech level held start to finish; formality fits purpose and audience; no politeness padding that softens a direct source statement.
4. Terminology and consistency. Domain terms, brand names, and glossary entries identical every time. Flag an anglicism where the target has a standard native term, unless the loanword is the domain standard.
5. Locale conventions. Quotes, spacing before punctuation, number and date formats, units, currency, script variant (zh-Hans vs zh-Hant), regional vocabulary, and heading case (English Title Case carried into es/fr/it/pt/de is an interference error). See content-translate's locale conventions table.
6. AI slop and translationese. The same evaluative word (an adjective, adverb, or verb added for emphasis) repeated 3+ times; connectors opening more than about 1 in 4 paragraphs; the same paragraph-opener template section after section; English clichés calqued into the target. A word that names something (product, protocol, command, field, person) must repeat as often as needed; dimension 4 wins that conflict. Ask: does varying it change what is pointed at? If yes, leave it.

### Per-language calibration

Per-language skills (`content-locale-humanize-es`, `-fr`, `-de`, `-ja`, `-zh`, `-ar`, `-pt`, `-it`, `-ko`, `-hi`, `-th`) auto-load when the target language comes up. They add translationese patterns, AI tells, and current orthography norms. Add a language as a new skill; don't grow this file with per-language content. With no matching skill, run the same structural checks and reason as a native speaker of that language.

### Verify phrases against real usage

When unsure whether a collocation is native, run an exact-phrase search in the target language (e.g. `"чувствительные данные"`, `"权限边界"`), scoped where possible to native sites in the domain, plus an unscoped search. Real hits on native-written pages: keep. None: rephrase and check the replacement the same way. Verify both suspicious phrases in the draft and phrases you rewrite into it. Keep a running list of verified-natural and verified-unused phrases. Reserve this for a handful of genuinely uncertain phrases per document, and never claim usage evidence you didn't check.

### Fix passes

Preserve every fact and instruction; rewrite phrasing, not content.

1. Interference: source syntax and calques first, rewritten with native grammar and idiom, not word substitution.
2. Frequency outliers: cut or vary repeated power words and connectors to a native writer's range.
3. Rhythm: rebuild sentence-length variation to the target language's norms.
4. Register lock: one formality level throughout.
5. Locale conventions: punctuation, spacing, numbers, dates, units, heading case, script and regional vocabulary.
6. Native-ear read: any sentence a native wouldn't say aloud gets rewritten.

### Report format

```
NATIVE-FLUENCY DIAGNOSTIC: [locale] — [filename or "Draft"]
Word count: X (target) vs Y (source)
Overall: X/60 — [band]; Critical findings: N

| Dimension | Score | Key findings |
|---|---|---|
| Accuracy & completeness | X/10 | ... |
| Native fluency | X/10 | ... |
| Register & formality | X/10 | ... |
| Terminology & consistency | X/10 | ... |
| Locale conventions | X/10 | ... |
| AI slop & translationese | X/10 | ... |

Findings (severity-ordered)
[CRITICAL/MODERATE/MINOR] issue — source: "..." → target: "..." — fix direction

What's working
- ...
```

### Evaluator caution

LLM judges miss a large share of errors and favour output from their own model family; reference-free quality estimation is a weak hallucination detector, so fluent-but-wrong can outscore faithful-but-stiff. WMT now pairs MQM with ESA (error span annotation) for human evaluation, and automatic metrics (COMET, MetricX, GEMBA-MQM) are far more reliable for ranking systems than for judging an individual segment. Treat a Pass band as evidence, not a guarantee; for high-stakes or YMYL content, audit with a different model than the translator or a qualified human.

More rounds are not more quality. Self-refinement studies (Self-Refine, TEaR, CorrectBench) find gains peak around the first correction pass and can decline by rounds 3–5. Cap at 2 rounds, then escalate to a cross-model check or a human.

## Examples

Interference. Source (German): "...weil das System jede Anfrage validiert, bevor es sie verarbeitet."
❌ "...because the system, before it processes it, validates every request."
✅ "...because the system validates every request before processing it."

Cross-lingual cliché.
❌ French: "Dans cet article, nous allons plonger dans les subtilités de..."
✅ "Cet article détaille..." or "Voyons comment...", whatever a French writer would actually open with.

Frequency outlier.
❌ Spanish: "...una función crucial..." / "...un papel crucial..." / "...un paso crucial..."
✅ Use the word each context calls for ("fundamental," "decisivo," "central") or drop the modifier.

## Checklist

- [ ] Domain detected and dimensions calibrated to it.
- [ ] Source and target compared directly on load-bearing sentences; every Critical finding listed.
- [ ] Interference and calques checked before word-level slop.
- [ ] Register held constant; locale conventions and heading case match the target.
- [ ] Names and terms left identical even when repeated.
- [ ] Uncertain phrases verified by real usage, not intuition; no fabricated usage claims.
- [ ] Sourcing strength for per-language tells stated; at most 2 fix rounds.

## References

Reviewed 2026-10-12.

- MQM: [scoring models](https://themqm.org/error-types-2/the-mqm-scoring-models/); Lommel, Uszkoreit and Burchardt 2013; Freitag et al. 2021 (arXiv:2104.14478); [ISO 5060:2024](https://www.iso.org/standard/80701.html); WMT25 metrics task (ESA and MQM).
- LLM and metric evaluation: GEMBA-MQM (arXiv:2310.13988); xCOMET (arXiv:2310.10482); judge bias (arXiv:2306.05685, arXiv:2406.13439, arXiv:2410.21819); reference-free QE and hallucinations (arXiv:2208.05309).
- Translation universals: Baker 1993; Laviosa 1998; Olohan and Baker 2000; Teich 2003; Baroni and Bernardini 2006; Koppel and Ordan 2011; Volansky, Ordan and Wintner 2015.
- Iteration: Self-Refine (arXiv:2303.17651); TEaR (arXiv:2402.16379); CorrectBench (arXiv:2510.16062); M-MAD (arXiv:2412.20127).
