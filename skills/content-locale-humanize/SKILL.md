---
name: content-locale-humanize
title: "Locale-Native Humanization & Translationese Elimination"
description: "MQM-informed, structural-pattern diagnostic for making translated/localized content read as if a native speaker wrote it from scratch, in any target language — detects translationese and AI-slop by pattern (interference, frequency outliers, rhythm, templating), not by a per-language word list."
license: Apache-2.0
compatibility: "Composes with content-translate. Used by content:translate in NATIVE-AUDIT mode. Language-agnostic — the dimensions apply to any target locale."
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

A translation can be accurate and still read as translated — stiff syntax, over-explicit connectors, a handful of statistically overused words, uniform sentence rhythm. Readers feel it as "not written by someone who thinks in this language," and it costs the same trust an English AI-slop draft costs an English reader.

Per-language dead-word lists don't generalize and go stale fast — the English list in `content-voice` already had to be refreshed once the first-wave words (delve, tapestry) faded. This skill encodes the STRUCTURAL patterns that stay evergreen across any language, backed by translation-quality research (MQM, Mona Baker's translation universals), with a few sourced example words per major language as calibration aids — not a boundary.

## Instructions

### Why structure, not word lists

Corpus research on translationese identifies four measurable universals, independent of language pair (Baker's translation universals, corroborated across studies at ~77–100% classification accuracy):

- Simplification — shorter sentences, plainer words, lower lexical density, avoided subordination, compared to what a native writer in that register would produce.
- Explicitation — spelling out what a native writer leaves implicit; retained optional connective words a native writer would drop; over-connecting ideas that don't need a connector.
- Interference (also called "shining-through") — source-language syntax, word order, or idiom bleeding into the target. The single strongest, most reliably detectable signal — function-word and sentence-structure distributions alone identify translated text at 86–93% accuracy in corpus studies, beating human judges. Weight it heaviest.
- Normalization — flattening a distinctive voice into safe, generic, canonical phrasing; leveled register.

Separately, real per-language research into AI-generated text (2024–2026) turns up the exact same meta-pattern in every language checked: a handful of frequency-outlier "power words," logical connectors opening nearly every paragraph, sentences clustering in one length band, and — strikingly — the SAME cliché metaphors showing up translated literally (French "plonger dans," Spanish "sumergirse en" — both doing the job of English "delve into"). Multilingual models are exporting English AI-habits through translation. Check for the pattern; the word list below is a calibration aid, not the checklist.

Sourcing confidence varies sharply by language — say so in the report when it's thin. Spanish and French have solid, convergent, independently-reported sourcing. German sourcing is SEO-blog convergence, not corpus research — treat it as a weaker prior. Japanese sourcing is anecdotal blog discourse. Chinese has the best quantitative backing of any non-English language (a university news-lab study measured ~4x higher parallel-sentence-structure rates in AI text). Arabic is the weakest — most published lists are direct translations of the English canon, not independent findings. Don't present any of this table as harder evidence than it is.

### Domain calibration — do this before scoring

Native-fluency expectations shift by content domain; the same signal reads differently depending on what's being translated. Detect the domain first — technical, legal, medical, marketing, academic, casual/UI, journalistic, literary (the same categories `content-translate` Phase 2 already detects) — then calibrate every dimension below to it:

- Technical/developer: English loanwords for established terms ("commit," "webhook," "endpoint," "pull request") are NATIVE in most languages' tech register — never flag them as anglicism/interference. Short, direct sentences are the domain norm, not a simplification tell. Flag missing or incorrect standard terminology instead.
- Legal: heavier subordination and formality ARE the native register here — don't apply the general rhythm-clustering penalty. Precision beats natural flow; a stiff-sounding legal sentence can still be exactly correct.
- Medical: internationally recognized terms (ICD codes, anatomical Latin) are expected verbatim. Register shifts hard between patient-facing (plain) and professional (technical) content — check the audience match, not just fluency.
- Marketing: highest tolerance — and expectation — for transcreation. Idiom, rhythm, and cultural reference should be reshaped aggressively for impact, not preserved literally. Judge against "would this land with a native reader," not sentence-by-sentence naturalness.
- Academic: formal register is native; don't flag formality as stiffness. Discipline-standard terminology and citation format matter more than rhythm variation.
- Casual/UI: shortest, plainest phrasing wins. Button/label brevity is domain-native, not oversimplification.

When domain is ambiguous, detect it from vocabulary and structure before scoring — never apply one universal register expectation across every content type.

### The 6 Dimensions

Score each 0–10 (10 = fully native/faithful). Sum = X/60.

Bands: Pass (48+) / Borderline (34–47) / Flagged (20–33) / Critical (<20)

Dual gate, mirroring MQM's actual scoring mechanic (themqm.org: Neutral=0/Minor=1/Major=5/Critical=25 penalty weights, quality = 1 − penalty÷word-count): a single Critical finding fails the audit regardless of the numeric band. A fluent-but-wrong translation is not a pass. Don't let a high AI-Slop or Native-Fluency score paper over a Critical Accuracy finding.

#### 1. Accuracy & Completeness
- Every claim, instruction, and nuance from the source present in the target — nothing added, nothing dropped.
- Mistranslation, omission, addition, untranslated fragments, broken placeholders — each an instant Critical finding.
- Spot-check 2–3 load-bearing sentences via mental back-translation. If meaning drifts, it's a finding.

#### 2. Native Fluency & Naturalness (the core "does this sound native" check)
- Interference: does sentence structure, clause order, or nesting mirror the SOURCE language's grammar instead of the target's? This is the highest-value check in the whole rubric.
- Calques: idioms or fixed expressions rendered word-for-word instead of the target's real equivalent.
- Collocation naturalness: correct dictionary words that don't actually pair that way in native usage.
- Simplification: suspiciously plain/short sentences and avoided subordination versus what this register normally produces.
- Explicitation: information spelled out that a native writer would leave implicit; connectors linking ideas that don't need linking.
- Rhythm clustering: 3+ consecutive sentences in the same length band — judged against the TARGET language's own natural range, not English norms (German tolerates much longer sentences than Japanese; don't import one language's burstiness rule into another).
- Read-aloud test: would a native speaker actually say this to a colleague, or does it read like a translated pamphlet?

#### 3. Register & Formality Consistency
- T-V form / honorific level / keigo tier chosen once, held constant start to finish — no mid-document drift.
- Formality matches the stated purpose and audience.
- Politeness padding that oversoftens a direct source statement — a known MT/AI tell in several languages.

#### 4. Terminology & Consistency
- Domain terms, brand names, glossary entries rendered identically every time — no synonym rotation across one document.
- Anglicism check: an English loanword used where the target has a standard native term (lexical interference) — flag it, unless the loanword IS the domain standard (e.g. "commit" in developer docs).

#### 5. Locale Convention Fidelity
- Dates, numbers, currency, units, punctuation, and quotation marks match target-locale convention (see `content-translate` Phase 3 for the full cheat sheet).

#### 6. AI-Slop & Translationese Calibration
- Frequency-outlier words: the same EVALUATIVE word — an adjective, adverb, or verb an AI reaches for to add emphasis ("crucial," "seamlessly," "leverages") — repeated 3+ times across the piece is a tell regardless of language. This check targets stylistic choice, never identity: a word that NAMES something (a product, brand, protocol, command, field, person) is referential, not evaluative, and must repeat exactly as many times as the content needs it to — that's dimension 4's job, and dimension 4 always wins the conflict. Before flagging a repeated word, ask "does varying or shortening this change what's being pointed at?" — if yes, it's a name, leave it alone; if no, it's a style choice, count it.
- Connector pileup: logical connectors ("furthermore"-class words in the target language) opening more than roughly 1 in 4 paragraphs.
- Templated structure: the same paragraph-opener pattern repeating section after section.
- Cross-lingual cliché transfer: an English AI-cliché calqued into the target (see examples below).

### Calibration anchors — per-language, auto-loaded

Sourced per-language calibration lives in dedicated skills, not inline here — `content-locale-humanize-es`, `-fr`, `-de`, `-ja`, `-zh`, `-ar`, `-pt`, `-it`, `-ko`, `-hi`, `-th` — each auto-loads by its own rule match when the target language comes up, so a Spanish job never pulls in Chinese or Korean anchors it doesn't need. Add a new language by dropping in a new `content-locale-humanize-<code>` skill; never grow this file with per-language content.

No matching per-language skill exists yet for this target: run the same structural checks anyway — connector density, power-word frequency, sentence-rhythm clustering, paragraph-opener templating, cross-lingual cliché transfer, source-syntax interference. Reason as a native speaker of that specific language; don't wait on a word list to exist.

### Phrase verification — check real usage when unsure

Intuition is fallible in a target language; real usage is the arbiter. When you can't tell whether a collocation or turn of phrase sounds native, run an exact quoted-phrase web search and let the result decide.

The technique:
1. Search the phrase in double quotes (exact-phrase match), in the target language — e.g. `"чувствительные данные"`, `"权限边界"`.
2. Scope to where native speakers of this domain actually write, when you can: add a site filter for a native-language platform the audience uses (a popular native tech blog/forum for developer content, a native news site for journalism, etc.). Also try the unscoped search.
3. Read the verdict: real hits on genuinely native-written pages mean people say it — keep it. Zero / "no results" means they don't — rephrase, then run the SAME check on your replacement before accepting it. Don't swap one unverified phrase for another.

Verify BOTH directions: a phrase already in the draft that sounds off, AND any phrase you're rewriting INTO the draft. A confident-sounding replacement that nobody actually uses is the same defect as the original.

Build a running list as you go — phrases you verified as natural (safe to reuse) and phrases you verified as not-used (avoid). It saves repeat lookups and makes the report auditable.

Reserve this for genuinely uncertain phrases — a handful per document; constructions you already know are native don't need lookups. And never claim support from usage or documentation you didn't actually check — a fabricated authority claim ("natives say this" / "the docs use this term" when you never searched or opened them) is worse than admitted uncertainty, because it shuts down the review that would have caught the error.

### Fix-Pass Technique

Apply in order. Preserve every fact and instruction — rewrite the phrasing, not the content.

Pass 1 — Interference sweep: hunt source-syntax bleed and calques first (highest-value signal). Rewrite with native grammar and idiom, not word-substitution.

Pass 2 — Frequency-outlier sweep: count repeated power words and connectors; cut or vary within the range a native writer would actually use.

Pass 3 — Rhythm pass: rebuild sentence-length variation to the TARGET language's own natural norms.

Pass 4 — Register lock: verify T-V/honorific/politeness level held constant start to finish.

Pass 5 — Locale-convention pass: dates, numbers, currency, units, punctuation, quotation marks.

Pass 6 — Native-ear final read: read the whole piece as a skeptical native editor. Any sentence a real native speaker wouldn't say out loud gets rewritten.

### Diagnostic Report Format

```
## 🌐 NATIVE-FLUENCY DIAGNOSTIC: [locale] — [filename or "Draft"]
**Word count**: X words (target) vs Y words (source)
**Overall score**: X/60
**Band**: Pass (48+) / Borderline (34–47) / Flagged (20–33) / Critical (<20)

| Dimension                        | Score | Key Findings |
|-----------------------------------|-------|--------------|
| Accuracy & Completeness           | X/10  | [summary]    |
| Native Fluency & Naturalness      | X/10  | [summary]    |
| Register & Formality Consistency  | X/10  | [summary]    |
| Terminology & Consistency         | X/10  | [summary]    |
| Locale Convention Fidelity        | X/10  | [summary]    |
| AI-Slop & Translationese          | X/10  | [summary]    |

### Findings (severity-ordered)
[CRITICAL/MODERATE/MINOR] {one-line issue} — source: "..." → target: "..." — fix direction

### What's working
- {strength}
```

### Evaluator caution

LLM self-evaluation research shows evaluators miss a large share of errors and carry self-preference bias toward output from their own model family. Reference-free quality estimation is a documented poor hallucination detector — fluent-but-wrong can outscore disfluent-but-faithful, which is exactly why the Accuracy dimension's back-translation spot-check is mandatory, not optional. Treat a Pass band as strong evidence, not a guarantee — for high-stakes or YMYL content, run the audit with a different model than the one that produced the translation.

More rounds is not more quality. Research on iterative LLM self-refinement (TEaR; Self-Refine; CorrectBench) consistently finds that score-then-fix loops peak around the first correction pass and can decline by the third-to-fifth round — the estimator's judgment quality is the bottleneck, not the number of iterations. Keep loop caps low (2 rounds, not open-ended), and if a second round still fails, escalate to a cross-model check or a human rather than looping further.

## Examples

### Interference (highest-value catch)

Source (German, verb-final subordinate clause): "...weil das System jede Anfrage validiert, bevor es sie verarbeitet."

❌ Translationese English: "...because the system, before it processes it, validates every request." (clause order bled from German)

✅ Native: "...because the system validates every request before processing it."

### Cross-lingual cliché transfer

❌ French: "Dans cet article, nous allons plonger dans les subtilités de..." (calqued English AI-cliché "delve into")

✅ Native: "Cet article détaille..." / "Voyons comment..." — whatever a French writer would actually open with.

### Frequency-outlier power word

❌ Spanish, same document: "...una función crucial..." / "...un papel crucial..." / "...un paso crucial..." (three uses of "crucial")

✅ Native: vary with the specific word each context calls for — "fundamental," "decisivo," "central" — or cut the modifier where the sentence doesn't need it.

## References

MQM framework: Lommel/Uszkoreit/Burchardt 2013; themqm.org; WMT operational set (Freitag et al., arXiv:2104.14478); LLM-as-MQM-judge (GEMBA-MQM, arXiv:2310.13988; xCOMET, arXiv:2310.10482). Translation universals: Baker; Olohan & Baker 2000; Laviosa 1998; Volansky/Ordan/Wintner 2015; Baroni & Bernardini 2006; Koppel & Ordan 2011; Teich 2003 (interference/shining-through). Per-language AI-tell research: adslzone.net, genbeta.com, pageon.ai (Spanish); startups-nation.fr, gpthuman.ai (French); walterwrites.ai, the-decoder.de, eology.de (German); note.com/Zenn blog discourse (Japanese); Renmin University 新闻坊 news-lab study (Chinese); Al Jazeera (Arabic). LLM-as-judge blind spots and self-preference bias: arXiv:2406.13439, arXiv:2512.16272, arXiv:2306.05685, arXiv:2410.21819. Reference-free QE as weak hallucination detector: arXiv:2208.05309. Iteration-count findings: TEaR (arXiv:2402.16379), Self-Refine (arXiv:2303.17651), CorrectBench (arXiv:2510.16062), M-MAD (arXiv:2412.20127).
