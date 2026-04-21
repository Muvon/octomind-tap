---
name: content-translate
title: "Content Translation & Localization"
description: "Translate and localize documents, code comments, UI strings, and structured content while preserving formatting, adapting to domain-specific terminology, and maintaining consistency across large files via batching."
license: Apache-2.0
compatibility: "Requires text_editor, view, shell tools. Works with any LLM model. Supports markdown, code, TOML, YAML, JSON, and plain text."
domains: developer writer translator
rules:
  - content(translate)
  - content(translation)
  - content(localize)
  - content(localization)
  - match(translat(?:e|ion|ing|ed))
  - match(localiz(?:e|ation|ing|ed))
---

# Content Translation & Localization

## Overview

Translate documents, code comments, UI strings, and structured content between languages while preserving original formatting, adapting terminology to the target domain, and maintaining consistency across large files. This skill handles everything from single paragraphs to multi-file projects by splitting work into coherent batches, tracking terminology across segments, and validating output quality.

Use this skill when:
- Translating documentation, READMEs, or technical guides
- Localizing UI strings, error messages, or API docs
- Translating code comments or inline documentation
- Working with large files that exceed context-window limits
- Adapting content for a specific domain (medical, legal, technical, marketing)

## Instructions

### 1. Pre-Translation Analysis

Before translating any content, analyze the source to determine:

| Factor | What to Identify | How to Record |
|--------|-----------------|---------------|
| **Source language** | Detect from content or ask user | Note in translation log |
| **Target language** | User-specified or inferred from context | Note in translation log |
| **Domain** | technical, legal, medical, marketing, academic, casual | Determine from vocabulary and context |
| **Tone** | formal, informal, instructional, persuasive, neutral | Match in target language |
| **Audience** | developers, end-users, experts, general public | Adjust complexity accordingly |
| **Format constraints** | markdown, code blocks, frontmatter, tables, HTML | Preserve exactly |
| **Key terminology** | Domain-specific words that must translate consistently | Build a glossary BEFORE translating |

**Rule**: If the user does not specify source/target language or domain, ASK before proceeding. Do not guess languages or domains.

### 2. Terminology Glossary (Mandatory for Multi-File or Domain Work)

For any translation involving domain-specific language or multiple batches:

1. **Extract key terms** from the source before translating
2. **Research equivalents** in the target language for the identified domain
3. **Record decisions** in a glossary format:
   ```
   TERM (source) → TRANSLATION (target) [domain: X, notes: Y]
   ```
4. **Reference the glossary** in every subsequent batch
5. **Update the glossary** if new terms appear mid-translation

**Rule**: Never translate the same domain term differently across batches. Consistency trumps literal accuracy.

### 3. Batching Strategy for Large Files

When a file exceeds safe context-window limits (typically >2000 words or >15000 characters):

1. **Split at natural boundaries**:
   - Markdown: split at `##` or `###` headers
   - Code: split at function/class boundaries
   - UI strings: split by screen or feature group
   - Narrative: split at paragraph or scene breaks

2. **Never split inside**:
   - Code blocks (```...```)
   - Tables (breaks alignment)
   - Frontmatter blocks (---...---)
   - Numbered lists with cross-references
   - Sentences (split at period + newline, not mid-sentence)

3. **Batch size guidelines**:
   | Content Type | Max Words/Batch | Max Characters/Batch |
   |-------------|----------------|---------------------|
   | Plain text / Markdown | 1500 | 10000 |
   | Technical docs with code | 1000 | 7000 |
   | UI strings / JSON | 500 | 4000 |
   | Legal / Medical | 800 | 6000 |

4. **Overlap strategy**: Include the last 1-2 sentences of the previous batch at the start of the next batch to maintain flow and context. Remove duplicates in final assembly.

5. **Track batch state**:
   ```
   Batch X/Y | Section: "Heading Name" | Words: N | Status: translated
   ```

### 4. Translation Workflow

Follow this exact sequence for every translation task:

**Step 1 — Analyze**: Identify language pair, domain, tone, audience, format.
**Step 2 — Glossary**: Extract and define key terminology (skip for trivial <200 word translations).
**Step 3 — Batch**: Split large content into coherent segments.
**Step 4 — Translate**: Process each batch with full context.
**Step 5 — Assemble**: Combine batches, remove overlaps, verify continuity.
**Step 6 — Validate**: Run quality checks (see Section 6).
**Step 7 — Deliver**: Present final translation with glossary if applicable.

### 5. Format Preservation Rules

Preserve all non-textual elements exactly. Translate ONLY human-readable text.

| Element | Rule |
|---------|------|
| **Markdown syntax** | Keep `#`, `##`, `**`, `*`, `` ` ``, `[](url)`, `![]()` unchanged |
| **Code blocks** | Do NOT translate code inside ```. Translate ONLY comments (`//`, `#`, `/* */`) |
| **Inline code** | Keep `` `variable_name` `` unchanged. Translate surrounding text only |
| **Frontmatter (YAML/TOML)** | Keep keys unchanged. Translate string values only |
| **HTML tags** | Keep `<tag attr="value">`. Translate text nodes only |
| **URLs** | Never translate URLs. Keep `https://...` as-is |
| **Variables / Placeholders** | Keep `{name}`, `%s`, `{{var}}`, `$VAR` unchanged |
| **Tables** | Translate cell contents. Preserve `|` and `-` alignment structure |
| **Numbered lists** | Keep numbers. Translate text. Preserve indentation |
| **Emoji** | Preserve emoji. Do not translate to text equivalents unless requested |

**Rule**: If you are unsure whether something should be translated, keep it unchanged and add a translator note `[TN: ...]`.

### 6. Domain Adaptation

Adapt translation style based on detected domain:

| Domain | Approach |
|--------|----------|
| **Technical / Developer** | Use established technical terminology in target language. Keep English loanwords if they are standard (e.g., "debug", "commit", "pull request" in many languages). Prefer official documentation translations. |
| **Legal** | Use precise legal terminology. When exact equivalents don't exist, use accepted transliterations or add explanatory notes. Never paraphrase. |
| **Medical** | Use internationally recognized medical terms (ICD, anatomical). When translating for patients vs. professionals, adjust complexity. |
| **Marketing** | Prioritize emotional impact and cultural resonance over literal accuracy. Adapt idioms, metaphors, and cultural references. |
| **Academic** | Maintain formal register. Use discipline-standard terminology. Preserve citation formats. |
| **Casual / UI** | Use concise, natural phrasing. Respect character limits if specified. Ensure buttons/labels feel native. |

### 7. Quality Validation Checklist

Before delivering any translation, verify:

- [ ] **Completeness**: Every sentence from the source is present in the target
- [ ] **Consistency**: Key terms are translated the same way throughout
- [ ] **Accuracy**: No meaning is added, removed, or distorted
- [ ] **Fluency**: Target text reads naturally to a native speaker
- [ ] **Format**: All markdown, code, frontmatter, and structure is preserved
- [ ] **Variables**: All placeholders, URLs, and code identifiers are intact
- [ ] **Numbers/Dates**: Formatted correctly for target locale (if applicable)
- [ ] **Gender/Formality**: Correctly matches target language conventions

**Rule**: If any check fails, flag the issue and re-translate the affected section. Do not deliver partial or unverified translations.

### 8. Handling Ambiguity

When the source is ambiguous:
1. Choose the most likely meaning based on domain and context
2. Add a translator note: `[TN: ambiguous source; translated as "X" meaning Y]`
3. If the ambiguity significantly affects meaning, ASK the user for clarification instead of guessing

### 9. Post-Translation Consistency Review

For multi-batch translations, perform a final pass:
1. Read the assembled translation start-to-finish
2. Check for tone shifts between batches
3. Verify that pronouns and references resolve correctly across batch boundaries
4. Ensure the glossary was applied uniformly
5. Confirm formatting is intact across the entire document

## Examples

### Example 1: Simple Markdown Document

**Source**:
```markdown
# Getting Started

Install the package via npm:

```bash
npm install my-package
```

Then import it in your code:

```javascript
import { init } from 'my-package';
init({ apiKey: 'your-key' });
```
```

**Target (Spanish, technical domain)**:
```markdown
# Primeros pasos

Instala el paquete mediante npm:

```bash
npm install my-package
```

Luego impórtalo en tu código:

```javascript
import { init } from 'my-package';
init({ apiKey: 'your-key' });
```
```

**Notes**: Code blocks preserved. Comments would be translated if present. `npm install` command kept as-is (standard CLI).

---

### Example 2: Large File Batching

**Source**: 5000-word technical guide with 12 sections.

**Workflow**:
```
Analysis: EN → DE, domain: technical/software, tone: formal instructional
Glossary: 23 terms extracted (API, webhook, endpoint, payload, etc.)

Batch 1/4: Sections 1-3 (Introduction, Setup, Configuration) — 1200 words
Batch 2/4: Sections 4-6 (Authentication, Requests, Responses) — 1150 words
Batch 3/4: Sections 7-9 (Error Handling, Rate Limits, Webhooks) — 1300 words
Batch 4/4: Sections 10-12 (SDKs, Examples, Changelog) — 1350 words

Overlap: Last sentence of Batch 1 included at start of Batch 2 for context.
Assembly: Combined, overlaps removed, TOC regenerated.
Validation: All 23 glossary terms consistent. All code blocks intact.
```

---

### Example 3: Domain-Specific UI Strings

**Source** (medical app, English):
```json
{
  "symptom_checker_title": "Check Your Symptoms",
  "disclaimer": "This tool does not provide medical advice. Consult a doctor for diagnosis.",
  "button_start": "Start Assessment"
}
```

**Target** (German, medical domain):
```json
{
  "symptom_checker_title": "Symptome überprüfen",
  "disclaimer": "Dieses Tool ersetzt keine medizinische Beratung. Konsultieren Sie einen Arzt für eine Diagnose.",
  "button_start": "Untersuchung starten"
}
```

**Glossary entry**: `assessment` → `Untersuchung` [domain: medical, notes: NOT "Bewertung" — medical context requires clinical term]

---

### Example 4: Frontmatter Preservation

**Source**:
```markdown
---
title: "Deployment Guide"
description: "How to deploy to production"
author: "DevOps Team"
---

# Deployment Guide
```

**Target** (French):
```markdown
---
title: "Guide de déploiement"
description: "Comment déployer en production"
author: "DevOps Team"
---

# Guide de déploiement
```

**Notes**: Keys (`title`, `description`, `author`) preserved. Values translated except `author` (proper noun).

## References

- For right-to-left (RTL) languages: ensure bidirectional text markers are preserved if present in source
- For CJK languages: be aware that word boundaries differ; segment by meaning, not spaces
