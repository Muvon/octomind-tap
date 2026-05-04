---
name: content-humanize
title: "Content Humanization"
description: "Science of AI text detection, 8-dimension humanization diagnostic, and 7-pass rewrite technique for transforming AI-generated content into genuinely human writing."
license: Apache-2.0
compatibility: "Octomind content agents."
domains: content
rules:
  - content(humanize)
  - content(ai-generated)
  - match(\bhumanize\b)
  - match(\bmake\s+(this|it|my)\s+(text|content|writing|copy)?\s*(sound|feel|read)\s+(more\s+)?human\b)
  - match(\bsounds?\s+(too\s+)?(like\s+)?ai\b)
  - match(\bai[-\s]?detection\b)
  - match(\bdetect(ed|ion)\s+as\s+ai\b)
  - match(\bai[-\s]generated\s+(text|content|writing|copy)\b)
---

# Content Humanization

## Overview

AI-generated text has measurable signatures that readers and search engines detect. This skill encodes the science behind those signals, a scoring diagnostic across 8 dimensions, and a 7-pass rewrite technique for eliminating them. The goal isn't evasion — it's quality. Human-written articles get 5.44x more traffic and hold reader attention 41% longer.

---

## Instructions

### Why AI Text Is Detectable

| Signal | AI pattern | Human pattern |
|---|---|---|
| Perplexity | ~21 (predictable word choices) | ~36 (unexpected, domain-specific vocabulary) |
| Burstiness | Uniform sentence lengths (15–25 words) | Dramatic variation — fragments to 40-word sentences |
| Vocabulary | 50+ dead words/phrases at 5–10× frequency | Natural, specific, domain-appropriate |
| Contractions | Absent or sparse | Constant — "don't", "it's", "won't" |
| Grammar | Perfect throughout | Natural breaks — "And", "But", fragments, asides |
| Voice | Detached, encyclopedic | First-person, opinionated, emotionally varied |
| Structure | Parallel sections, equal lengths, formulaic | Deliberately unequal, unpredictable |
| Transitions | "Furthermore", "Moreover", "Additionally" | Absent, or "But.", "So.", "The catch?" |

Google's March 2026 update amplified "Experience" — content demonstrating genuine first-hand experience outranks comprehensive but impersonal content. 96% of AI Overview citations come from sources with strong E-E-A-T signals.

---

### 8-Dimension Diagnostic

Score each dimension 1–10 (10 = fully human). Sum = X/80.

**Risk levels**: Pass (65+) / Borderline (45–64) / Flagged (30–44) / Critical (<30)

#### 1. Perplexity (Word-Level Unpredictability)
- Flag every statistically obvious word choice
- Count AI vocabulary hits (dead words, transitions, phrases)
- Check for domain-specific or unexpected vocabulary
- Score: high unique/surprising vocabulary = high, generic/predictable = low

#### 2. Burstiness (Sentence-Level Variation)
- Measure sentence length range (shortest vs longest)
- Flag 3+ consecutive sentences within ±5 words of each other
- Check for fragments (<5 words for emphasis)
- Check for long momentum sentences (>30 words)
- Check paragraph length variation across the piece
- Score: dramatic variation with intentional rhythm = high, uniform = low

#### 3. Vocabulary Hygiene
Count every instance of dead vocabulary (see content-voice skill for full lists). Scoring: 0 hits = 10, 1–3 = 7, 4–8 = 4, 9+ = 1.

Also flag formal overreach: "utilize" (use), "facilitate" (help), "demonstrate" (show), "commence" (start), "culminate" (end), "subsequent" (next), "prior to" (before), "in order to" (to), "serves as" (is).

#### 4. Contraction Density
- Count uncontracted forms: "do not", "it is", "will not", "can not", "they are", "we have", "does not", "is not", "was not", "would not", "should not", "could not"
- Target: <2 uncontracted forms per 500 words (unless deliberate emphasis)
- Score: natural contractions throughout = 10, formal throughout = 1

#### 5. Grammatical Humanity
- Sentences starting with "And", "But", "So", "Or" — present? (humans do this constantly)
- Sentence fragments for emphasis — present?
- Parenthetical asides — present?
- Trailing participles: sentences ending with "...highlighting", "...ensuring that", "...contributing to", "...underscoring", "...reflecting" — count each
- "Not just X, but also Y" constructions — count
- Semicolons connecting simple phrases — count (AI overuses these)
- Perfect grammar throughout with zero breaks = AI signal
- Score: natural grammar breaks present = high, perfect throughout = low

#### 6. Voice & Personality
- First-person markers: "I've found", "In my experience", "What I've seen", "We tested" — present?
- Opinions: "I'd argue", "Honestly", "This is overrated", "This matters more than people think" — present?
- Emotional variance: enthusiasm, skepticism, frustration, curiosity, humor — any present?
- Conversational asides: parenthetical thoughts, self-corrections, rhetorical questions?
- Vulnerability or uncertainty: "I'm not sure about this", "The data is mixed", "We got this wrong"?
- Specific references: named tools, people, events, publications, dates?
- Score: rich personality throughout = 10, detached encyclopedic = 1

#### 7. Structural Unpredictability
- Section lengths: all roughly equal? (AI) or deliberately varied? (human)
- Paragraph openers: all topic sentences? Or varied (question, example, continuation)?
- Conclusion: recap of main points? (AI) Or forward-looking/question/callback? (human)
- Opening: broad definitional? (AI) Or specific scene/claim/stat with commentary? (human)
- Subheadings: generic labels ("Benefits", "Challenges")? Or personality ("Why This Actually Matters")?
- Synonym rotation: same concept called different names each paragraph? (AI tell)
- Score: unpredictable, varied structure = high, formulaic = low

#### 8. Transition Quality
- Count formulaic transitions: "Furthermore", "Moreover", "Additionally", "Moving on", "As we discussed", "It's worth noting"
- Check for conversational alternatives: "But here's the thing", "So.", "The catch?", "And yet."
- Check for zero-transition jumps (just starting the next idea — humans do this often)
- Score: organic or absent transitions = high, formulaic = low

---

### Diagnostic Report Format

```
## 🧬 HUMANIZATION DIAGNOSTIC: [filename or "Draft"]
**Word count**: X words
**Overall humanization score**: X/80
**Risk level**: Pass (65+) / Borderline (45–64) / Flagged (30–44) / Critical (<30)

| Dimension          | Score | Key Findings              |
|--------------------|-------|--------------------------|
| Perplexity         | X/10  | [summary]                |
| Burstiness         | X/10  | [summary]                |
| Vocabulary         | X/10  | [X dead words found]     |
| Contractions       | X/10  | [X uncontracted forms]   |
| Grammar humanity   | X/10  | [summary]                |
| Voice & personality| X/10  | [summary]                |
| Structure          | X/10  | [summary]                |
| Transitions        | X/10  | [X formulaic found]      |

### Worst Offenders (fix these first)
1. [Most impactful issue — specific location — fix]
2. [Second — specific location — fix]
3. [Third — specific location — fix]

### Dead Word Inventory
[List every flagged word/phrase with location]
```

---

### 7-Pass Rewrite Technique

Apply section by section, in order. Preserve every fact, citation, and data point — rewrite the voice, not the content.

**Pass 1: Vocabulary** — Replace every dead word, dead transition, dead phrase, and formal overreach. Use the simplest natural word. Don't replace with another AI-sounding synonym — use what a human expert in this field would actually say.

**Pass 2: Contractions** — Convert every uncontracted form unless it's deliberate emphasis. "Do not touch this" (emphasis) is fine. "It does not appear to be the case" → "It doesn't look like it."

**Pass 3: Rhythm** — Rebuild sentence lengths for burstiness. Find runs of 3+ similar-length sentences: break one into a fragment, merge two into a long flowing one. After any sentence >25 words, follow with one <8 words. Insert a one-sentence paragraph between dense ones.

**Pass 4: Transitions** — Kill every formulaic transition. Replace with nothing (just start the next idea), or: "But.", "So here's the thing.", "The catch?", "And yet —", "Which brings up something interesting."

**Pass 5: Grammar humanity** — Start 2–3 sentences per section with "And" or "But". Add 1–2 parenthetical asides per major section. Use at least one fragment per section. Remove all trailing participle phrases — rewrite as separate sentences. Remove all "not just X, but also Y" constructions. Remove semicolons connecting simple phrases.

**Pass 6: Voice injection** — At least one first-person observation per major section (if content type allows). At least one opinion or position taken. At least one moment of specificity: a named tool, person, date, or publication. At least one emotional beat: enthusiasm, skepticism, surprise, frustration.

**Pass 7: Structure** — Make section lengths deliberately unequal. Vary paragraph openers (question, example, continuation — not always topic sentence). If the conclusion recaps, rewrite to end with a question, prediction, or callback. If subheadings are generic, inject personality. Kill synonym rotation — pick the best word and stick with it.

---

## Examples

**AI writes:**
> "Digital marketing has evolved significantly over the past decade. Companies now utilize multiple channels to reach their audiences. Social media platforms offer unique opportunities for engagement. Content marketing remains a powerful strategy for building trust."

**Human writes:**
> "Digital marketing looks nothing like it did ten years ago. Nothing. The channels alone — social, search, email, video, podcasts, influencer partnerships — would've seemed absurd in 2014. And here's what nobody tells you: most companies are still figuring it out, throwing budget at whatever platform had a good case study last quarter."

**What changed:** Specific over abstract. Fragments for punch. Contractions throughout. First-person energy. Unexpected vocabulary. Dramatic rhythm shifts. No dead words.
