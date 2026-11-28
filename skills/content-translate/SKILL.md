---
name: content-translate
title: "Content Translation & Localization"
description: "Translate documents, code comments, UI strings and structured content, keeping formatting and terms consistent. Use for localizing large files."
license: Apache-2.0
compatibility: "Requires file read, file edit and shell tools. Works with any LLM model. Supports markdown, code, TOML, YAML, JSON, and plain text."
domains: writer
rules:
  - content(translate)
  - content(translation)
  - content(localize)
  - content(localization)
  - match(translat(?:e|ion|ing|ed))
  - match(localiz(?:e|ation|ing|ed))
  - semantic(translate this document into Spanish and keep the formatting, 0.72)
  - semantic(localize the interface strings in this file for another language, 0.72)
  - semantic(translate the comments in my code but keep the terms consistent, 0.72)
  - semantic(convert this content to German without changing the structure, 0.72)
---

## Overview

Translate and localize documents, code comments, UI strings, and structured content while preserving meaning, formatting, placeholders, and terminology. Use for anything from one string to a multi-file documentation set. For a native-fluency audit of the result, load the content-locale-humanize skill.

## Mental model

A translation is a contract: same meaning and function, target-native form. Accuracy and completeness come first, then terminology, then fluency, style, and locale conventions; these are the MQM error dimensions reviewers will score. Professional practice (ISO 17100) separates translation from an independent revision. An LLM draft is machine output: it still needs that revision step (ISO 18587 post-editing), however fluent it reads.

## Rules

### Brief before translating

| Factor | Decide |
|---|---|
| Locale | Full BCP 47 tag, not just language: es-ES vs es-419, pt-BR vs pt-PT, fr-FR vs fr-CA, zh-Hans-CN vs zh-Hant-TW |
| Domain and audience | Technical, legal, medical, marketing, academic, UI; expert or general |
| Register | tu/vous, du/Sie, tú/usted, keigo level, Korean speech level; hold it constant |
| Assets | Existing glossary, translation memory, style guide, shipped localized UI |
| Do-not-translate | Brand and product names, code identifiers, commands, legal entity names |

Ask when the locale variant, register, or domain is unknown and would change the output. Don't guess between es-ES and es-419.

### Modes

Detect the mode first. If it is unclear, ask in one sentence.

- Translate (default): source content plus a target language.
- Validate: the source and an existing translation to check or grade. Report mistranslations, register drift, dropped or added meaning, terminology inconsistency, and broken placeholders. Don't rewrite unless asked.
- Native audit: does a translation sound native, or does it read like AI or machine translation? Detect the domain and score native fluency, translationese, and AI-slop with the `content-locale-humanize` skill, which reasons natively in the target language, not with the English list in `content-voice`. Report only, unless asked to fix.
- Adjust: an existing translation plus a directional ask (register shift, terminology swap, length trim, locale-variant change, tone). Return the revised version and a delta note.

After a native-audit report, "fix these" means Adjust with the findings as the ask.

### Intake and delivery

- Required, ask once, and don't proceed without them: the target language with locale variant (`es-MX` not `es`, `pt-BR` not `pt`, `zh-Hans` or `zh-Hant`, `en-US` or `en-GB`, `de-DE`, `de-AT` or `de-CH`, `fr-FR` or `fr-CA`) and the register (formal, informal, or neutral; it drives the T-V choice, honorifics, and contractions). Ask with one message: `I need: (1) target language with locale variant, (2) register. Optional: purpose (marketing, docs, legal, UI, prose), output destination. Source: <detected language>; confirm if wrong.`
- Source language: auto-detect and confirm only when ambiguous (Norwegian Bokmål or Nynorsk, Serbian Cyrillic or Latin).
- Optional: purpose (it sets how aggressively to localize), glossary, output destination. A glossary that is referenced but not provided: ask for the file or the entries. In parallel, recall the translation glossary, brand voice, locale conventions, and prior choices from memory.
- With every input present, start immediately.
- Stop and ask only when a load-bearing sentence is genuinely ambiguous, the target demands a gender or honorific the source leaves open and the reader is unknown, a tagline needs transcreation rather than translation, or numbers look like they should be converted (for example USD prices for an EU audience).
- In an autonomous, non-interactive run, don't ask: infer the register from the source, take the most probable reading of each ambiguity, and flag each such choice in the notes. The target language stays required.
- Output goes exactly where the user said. A named file path: write there, and overwrite only when invited. "In place" or "replace" on a source file: overwrite the source. Several locales into one file or structured format: use the shape described. No destination: answer inline and never invent a filename. File input without a destination: answer inline and offer to write it to a path.
- After delivering, memorize durable terminology choices, per-locale brand-voice rules, T-V decisions, and recurring untranslatables (importance 0.7 to 0.9).
- Source already in the target language: say so and don't translate. The request is generation, not translation ("translate this idea into Spanish marketing copy"): say in one line that it is a writing task and treat it as one.
- Several target locales: one independent block per locale, each with its own notes and no cross-references.

### Translation practice

- Translate meaning, voice, and intent, not words. Ask how a native speaker would say it, never what the dictionary word is. Equivalent effect beats equivalent form: if a pun, idiom, or rhetorical device cannot survive, recreate the effect in a form natural to the target.
- When the literal and the natural rendering diverge, choose natural and flag it if load-bearing. When two natural options carry different connotations, take the one closer to the source and note the other.
- Never resolve source ambiguity silently: ask, or translate the more probable reading and flag it in the notes. When the target demands a gender the source leaves neutral, ask, or use the most inclusive target form and flag it.
- Untranslatable: keep the source word italicized with a short gloss on first occurrence, or paraphrase. Never invent a fake target word.
- Police false friends, calques, source-syntax bleed, and mixed register (one register unless the source deliberately shifts). In technical and legal text, preserve and gloss rather than substitute a local equivalent. Transcreate marketing text only when the user permits.
- Use web search only for a proper noun's accepted transliteration, a brand's official localized name, or the usual rendering of a culture-bound reference or emerging technical term: two or three targeted queries per item. Unverified: preserve the source and add a note. Never fabricate a localized brand name.
- Raw machine translation handed over for fixing is full post-editing (ISO 18587) unless the user says it is for internal gisting.
- The translator is invisible: add no meaning, examples, qualifiers, or hedges absent from the source, and drop no meaning, nuance, hedges, or tone present in it. Don't edit or improve the source; translate what is there.
- Convert currency, units, or dates only with permission, and warn when text expansion threatens the layout.
- Self-review before delivery: back-translate two or three critical sentences and fix drift; check one rendering per concept, one register and T-V form, and placeholder, code-block, and link counts against the source; rewrite anything that reads like source syntax or a dictionary lookup.
- Deliver translation notes whenever a non-trivial choice was made. Keep them a thin addendum; the translation is the artifact.

### Terminology

- Build or load a glossary before translating: `source term → target term [domain, notes, rejected alternatives]`. Reuse it in every section and extend it when new terms appear.
- UI labels in docs must match the shipped localized UI exactly. If the product isn't localized, keep the source label and add a translation only if the style guide asks for it.
- Verify uncertain terms against target-language vendor documentation and terminology portals, or an exact-phrase search on native sites. Keep established English loanwords where the target domain uses them ("commit," "pull request" in most developer registers).
- One source term, one target term per sense. If the source uses one word for two concepts, split it rather than forcing consistency.

### Context and segmentation

- Give the model the brief, glossary, and enough surrounding document to resolve references. Current long-context models can hold a whole document; segment by output budget, not by an old context ceiling.
- Split only at structural boundaries: headings, functions, string groups, scenes. Never split inside code blocks, tables, frontmatter, lists with cross-references, or sentences.
- Pass the previous translated section as context instead of overlapping source text and deduplicating later.
- Track state per section (`Section X/Y | heading | status`). After assembly, read start to finish for tone drift, cross-references, anchors, and glossary use.

### Format preservation

| Element | Rule |
|---|---|
| Markdown | Keep syntax; translate text, link text, and alt text |
| Code blocks | Translate comments and user-facing strings only, never code |
| Inline code, variables, placeholders | Keep `{name}`, `%s`, `{{var}}`, `$VAR` byte-for-byte; reorder around them as grammar needs |
| Frontmatter | Keep keys; translate string values that are human-facing |
| HTML | Keep tags and attributes; translate text nodes and `alt`/`title` |
| URLs | Keep, unless a localized page exists; then point to it |
| Heading anchors | Translated headings change `#slugs`; update in-page links and TOC |

If unsure whether something is translatable, keep it and add `[TN: ...]`.

### Software strings

- Translate whole messages; never concatenate fragments, which breaks word order and agreement.
- Use ICU MessageFormat or the platform's plural API with CLDR plural categories (Arabic has six forms, Russian and Polish four, Japanese and Chinese one). Don't hand-code an English "s".
- Check gender, case, and article agreement around placeholders; ask for translator comments when a placeholder's content is unknown.
- Respect length limits. Labels under 10 characters can double or triple in European languages; text over 70 characters runs about 30% longer (W3C, citing IBM). Typical whole-text expansion: German +20–30%, Spanish and French +15–25%, Russian +15%; CJK usually runs shorter in characters. Flag truncation risks instead of abbreviating unclearly.
- RTL: isolate embedded LTR runs (`<bdi>`, `dir="auto"`, or Unicode FSI/PDI), keep numbers and code readable, and let layout mirror.

### Locale conventions

Follow Unicode CLDR data for the exact locale; this table covers the common traps.

| Locale | Quotes | Number | Date | Watch |
|---|---|---|---|---|
| de-DE | „…“ (de-CH «…») | 1.234,56 (CH 1’234.56) | 12.10.2026 | de-CH uses ss, not ß |
| fr-FR | « … » | 1 234,56 | 12/10/2026 | narrow no-break space before ; ! ? and no-break space before : |
| fr-CA | « … » | 1 234,56 | 2026-10-12 | OQLF: no space before ; ! ?, space before : |
| es-ES | «…» (RAE first choice), then “…” | 1234,56; 12 345,6 | 12/10/2026 | opening ¿ ¡ required |
| es-MX | “…” | 1,234.56 | 12/10/2026 | ustedes, no vosotros, across es-419 |
| it-IT | «…» or “…” | 1.234,56 | 12/10/2026 | perché (acute), è (grave) |
| pt-BR / pt-PT | “…” / «…» | decimal comma | 12/10/2026 | vocabulary and pronouns differ; never mix |
| ja-JP | 「…」『…』 | 1,234.56; 万 for large | 2026年10月12日 | full-width 、。; no spaces between words |
| zh-Hans-CN | “…”, 《》 for titles | 1,234.56; 万/亿 | 2026年10月12日 | full-width ，。、；：？！; …… and —— |
| zh-Hant-TW | 「…」『…』 | same | same | regional terms: 軟體, 網路, 資訊, 影片 (CN 软件, 网络, 信息, 视频) |
| ko-KR | “…” | 1,234.56 | 2026. 10. 12. | word spacing (띄어쓰기) per National Institute of Korean Language |
| ar | «…» or “…” | Western or Arabic-Indic digits per market | RTL | ، ؛ ؟ punctuation |
| hi-IN | “…” | 12,34,567.89 (lakh/crore) | 12/10/2026 | । ends sentences |
| th-TH | “…” | 1,234.56 | Buddhist Era (CE + 543) in formal contexts | no spaces between words; a space marks a clause or sentence break |

Headings: English Title Case is an error in most target languages; use sentence case (German capitalizes nouns only). Converting Simplified to Traditional script is not localization for Taiwan or Hong Kong.

en-US: 1,000.50, 05/23/2026 (ISO 2026-05-23 when the source enforces it). Russian, Polish, Czech, Slovak: «…» or „…“ by country.

### Domain adaptation

| Domain | Approach |
|---|---|
| Technical | Target-market standard terms; keep standard loanwords; mirror vendor docs in the target language |
| Legal | Preserve legal effect; use the target jurisdiction's terms; flag concepts with no equivalent instead of paraphrasing them away |
| Medical | Recognized terminology; plain language for patients, technical for professionals; never soften warnings or dosages |
| Marketing | Transcreate from the brief: adapt idiom, rhythm, and cultural reference, but keep claims, prices, and disclaimers exact |
| Academic | Formal register, discipline terminology, citation format unchanged |
| UI | Shortest natural phrasing; consistent verbs for the same action; respect limits |

Gender-inclusive forms follow the client's style guide. Academies and several governments restrict typographic forms (asterisks, colons, the French point médian, the Italian schwa); the per-language locale skills carry the current norms. Without a guide, prefer neutral rewording or paired forms. Spanish: doublets ("todos y todas") or neutral rewording in formal text; the RAE rejects "todes", "tod@s", and "todxs", though some activist or youth audiences expect them.

### Risk inventory

| Risk | Handling |
|---|---|
| Idioms and calques | Target equivalent or paraphrase, never literal ("raining cats and dogs") |
| Culture-bound references | Localize for marketing and literary; preserve and gloss for technical and legal |
| Untranslatables (saudade, hygge, schadenfreude, mono no aware) | Source word italicized with a short gloss on first use, or paraphrase |
| False friends | actually ≠ actualmente; sympathique ≠ sympathetic; embarazada ≠ embarrassed; library ≠ librería (bookshop); Gift means poison in German |
| Wordplay, puns, alliteration, rhyme | Recreate the effect, not the form |
| Honorifics | Japanese -san/-sama, Korean -ssi/-nim, Indian -ji |
| Gendered references | Follow the target's requirements; ask when the source is silent and the reader unknown |
| Names, brands, products, code identifiers | Usually verbatim; verify official localized names |
| Numbers, dates, currencies, units, addresses, phones, quotes | Locale-format; convert currency or units only on explicit ask |
| Source-syntax bleed | English passives read unnatural in Romance and Slavic targets; literal nominalization-heavy German reads bureaucratic in English |
| Marketing under-localization | A transliterated tagline usually dies; transcreate with the requester's permission |

### Ambiguity

Choose the reading the domain and context support and note it: `[TN: ambiguous source; translated as "X" meaning Y]`. Ask when the choice changes meaning materially.

### Quality review

- Revise against the source, segment by segment: omissions, additions, numbers, negation, units, names, glossary terms. Reading only the target misses fluent errors.
- Run mechanical checks: placeholder and tag parity, numbers, URLs, glossary hits, length limits. For shipped content, log findings with MQM-style categories and severities.
- LLM self-review misses errors and favors its own output. For high-stakes content, review with a different model or a qualified human. Metrics (COMET, MetricX) and LLM judges (GEMBA-style) are screening tools, not sign-off; back-translation catches only gross drift.
- Fixing raw machine translation is full post-editing (ISO 18587:2017, under revision): human-translation quality, every check applies. Light post-editing (comprehensible, not publishable) only for internal gisting at the requester's word; state which level was delivered.
- Grade an existing translation analytically (ISO 5060:2024, MQM): tag each error by type (accuracy, fluency, terminology, style, locale convention, markup/placeholder) and severity (critical / major / minor); counts drive the verdict, not impression.

### Report shapes

Adjustment delta note:

```
✏️ Adjustments (<what the user asked for>)

- <change category> — was: "<short snippet>" → now: "<short snippet>" — <reason>
- <change category> — applied throughout: <e.g. T-V form switched tú → usted>
- Preserved: <what was kept intact>
```

Translation notes (non-trivial choices only, one bullet each):

```
🗒 Translation notes (<source-lang> → <target-locale>)

- T-V form / Register: <choice> (reason)
- Untranslatable: <source term> rendered as <choice> — alternative: <other>
- Idiom: <source> → <target rendering> (literal would be misleading)
- Culture-bound: <reference> localized (purpose=marketing) / preserved+glossed (purpose=technical)
- Ambiguity flagged: <sentence> — read as <A> over <B> because <reason>
- Length: +/-X% vs source — <warn if a UI string may break layout>
```

Validate report:

```
🔍 Translation review (<source-lang> → <target-locale>) · <verdict>

Verdict: ✅ ship / 🟡 minor fixes / 🔴 needs rework
Overall accuracy: <N>/10 · Naturalness: <N>/10 · Terminology consistency: <N>/10 · Structure integrity: <pass/fail>

Findings (severity-ordered)
- 🔴|🟡|🟢 <one-line issue> — source: "<quote>" → translation: "<quote>" — <why it's wrong / fix direction>

What's working
- <one-line strength>
```

After a validate or native-audit report, offer: `Want me to apply the fixes? Reply with "apply all" / "apply critical" / "apply <#>"`. The native-audit report uses the shape of the `content-locale-humanize` skill.

Confirmation line, only when the output did not go to the conversation:

- `Translation written to <path> (<N> words, <K> placeholders preserved).`
- `Source overwritten with <locale> translation (<N> words, <K> placeholders preserved).`

An adjusted translation goes back in the original's shape, in the conversation unless the user named a file, followed by the delta note above.

## Examples

Markdown, EN → es-ES (technical):

````markdown
## Getting started
Install the package with npm:
```bash
npm install my-package
```
````

````markdown
## Primeros pasos
Instala el paquete con npm:
```bash
npm install my-package
```
````

Heading in sentence case, code untouched, informal tú matching a developer audience in Spain.

Plural string, EN → ru. Wrong (concatenation, one form):

```
"Deleted " + count + " files"  →  "Удалено " + count + " файлов"
```

Right (ICU, CLDR categories):

```
{count, plural, one {Удалён # файл} few {Удалено # файла} many {Удалено # файлов} other {Удалено # файла}}
```

## Checklist

- [ ] Locale tag, domain, audience, and register fixed before translating.
- [ ] Every source sentence present; nothing added, dropped, or softened.
- [ ] Glossary applied uniformly; UI labels match the shipped localized UI.
- [ ] Code, placeholders, tags, URLs, and frontmatter keys byte-identical; anchors updated.
- [ ] Plurals, agreement, and length limits handled for UI strings.
- [ ] Quotes, numbers, dates, spacing, and heading case follow the target locale.
- [ ] Revised against the source, ideally by a different model or a human for high-stakes text.
- [ ] Translator notes and unresolved ambiguities listed for the requester.

## References

Reviewed 2026-10-12.

- ISO 17100 (translation services), ISO 18587 (post-editing; revision in progress), [ISO 5060:2024](https://www.iso.org/standard/80701.html) (evaluating translation output)
- [MQM scoring models](https://themqm.org/error-types-2/the-mqm-scoring-models/)
- [Unicode CLDR](https://cldr.unicode.org/) and [MessageFormat 2.0](https://messageformat.unicode.org/) (stable since CLDR 47, 2025)
- [W3C Internationalization: inline bidi markup](https://www.w3.org/International/articles/inline-bidi-markup/) and [text size in translation](https://www.w3.org/International/articles/article-text-size)
- [OQLF: spacing around punctuation](https://vitrinelinguistique.oqlf.gouv.qc.ca/22039/la-typographie/espacement/espacement-avant-et-apres-les-signes-de-ponctuation-et-les-symboles)
