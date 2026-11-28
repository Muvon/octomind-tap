---
name: content-ai-detect
title: "AI Text Detection: Evidence-Based Authorship Read"
description: "Read-only check for AI-typical writing patterns and hard artifacts, with quoted evidence and a calibrated band, never a percentage. Use on a suspect text."
license: Apache-2.0
compatibility: "Read-only on the text under review. Web search and page fetch check suspect references. Saves a report only on request."
capabilities: webfetch
domains: writer
rules:
  - match((?i)\b(was|is)\s+(this|it|that)\s+(text\s+|essay\s+|article\s+|post\s+)?(written|generated|made)\s+by\s+(AI|ChatGPT|an?\s+(LLM|model|bot))\b)
  - match((?i)\b(detect|check|spot|tell|assess|scan)\b.{0,40}\b(AI[- ]generated|AI[- ]written|written\s+by\s+AI|machine[- ]generated|machine[- ]written)\b)
  - match((?i)\bAI\s+(detector|detection)\b)
  - match((?i)\b(did|does|has)\s+(my\s+|the\s+)?(student|candidate|applicant|writer|author)\b.{0,40}\b(use|used)\s+(AI|ChatGPT)\b)
  - match((?i)\b(AI|machine|LLM)[- ](authorship|generated|generation|written|authored|patterns?|typical)\b|\bauthorship\s+(check|triage|read)\b|\bAs\s+an\s+AI\b|\bmachine\s+generation\b)
  - match((?i)\b(leftover|stray)\s+(prompt|chatbot)\b|\bchatbot\s+boilerplate\b|\bgeneration\s+artifacts?\b|\b(calibrated|banded)\s+(read|band)\b)
  - semantic(is this essay AI generated, 0.72)
  - semantic(does this text read like a chatbot wrote it, 0.72)
  - semantic(point out the AI sounding phrases in this draft with quotes, 0.72)
  - semantic(how likely is it that this article was machine written, 0.72)
---

## Overview

Examine one text and report whether it carries the patterns typical of machine-generated writing, with quoted evidence for every marker and an honest statement of what that evidence does and does not prove. The outcome is a calibrated three-band read, not a verdict. It is a triage tool for editors, teachers, moderators, and hiring reviewers. No detector, including this procedure, can establish authorship from style alone; say so in every report. The skill is read-only: it reports and does not rewrite.

## Mental model

Evidence outranks impression. A hard artifact or a divergence from the claimed author's own writing counts; a single stylistic marker never does. Every marker has an innocent explanation, and the report names it.

## Rules

### Workflow

1. Parse. Read the text. Note the genre, the claimed author, the purpose, and any author samples or context the user gave.
2. Hunt hard artifacts first: prompt residue ("As an AI", "Certainly! Here's", "I hope this helps"), leftover placeholders, orphaned markdown, references that don't resolve, quotes attributed to people who never said them. Check each suspect reference with `search` and open it with `knowledge(command="read")`, applying the `content-grounding` skill's rules, before calling one fabricated.
3. Read for soft markers. Apply the eight-dimension diagnostic of the `content-humanize` skill as an observation lens, not a score: template shape, generic substance, first-person claims with no lived detail, uniform rhythm and connectors, stock vocabulary, an everything-hedged stance, zero idiosyncrasy.
4. Compare. If author samples exist, contrast register, sentence habits, error profile, and vocabulary against them. Divergence from the author's own writing is stronger evidence than any generic marker.
5. Weigh. Assign one band. Hard artifacts or a wide co-occurring cluster move the band up; any single marker alone never does.
6. Name the alternatives. For each marker, state the innocent explanations: formal genre, non-native writer, heavy editing, house style, templates, grammar tools.
7. Render the report and recommend the next step.

### Bands

| Band | Meaning |
|------|---------|
| No notable pattern | Nothing beyond ordinary competent writing. Absence of markers is not proof of human authorship. |
| Mixed signals | Some AI-typical patterns present, each also consistent with human formal, edited, or non-native writing. Not actionable on its own. |
| Strong pattern cluster | Hard artifacts, or many markers co-occurring across dimensions, or clear divergence from the author's own samples. Still a lead, not a finding of fact. |

### Evidence hierarchy

Strongest first: hard artifacts (including a positive provider-watermark or content-credentials result the user supplies), then fabricated or unresolvable references, then divergence from supplied author samples, then a co-occurring stylistic cluster, then a single stylistic marker (never sufficient). A missing watermark proves nothing: text marks rarely survive copy-paste, paraphrase, or translation.

### Calibration

- Don't emit percentages, probabilities, or "X% AI". Results differ by tool, text length, and how much a human edited the text. Weber-Wulff et al. (2023, 12 public tools plus Turnitin and PlagiarismCheck) found the tools neither accurate nor reliable, leaning toward calling text human, and worse after obfuscation such as paraphrasing. Liang et al. (2023, seven detectors) misclassified 61.22% of 91 non-native English TOEFL essays on average while scoring near-perfect on US 8th-grade essays. Jabarian and Imas (NBER Working Paper 34223, 2025) found one commercial tool, Pangram, held a false-positive rate of 0.5% or less without losing accuracy, with all three commercial tools less accurate under 50 words; that result is one tool on that paper's test texts, so check the current evidence for the tool in question. No number should come from a detector because the false-positive rate that matters depends on the base rate of AI text in the batch and on edited or hybrid text, which none of these studies settle.
- Don't treat any word or construction as proof. "Delve", contractions, em dashes, and sentence-length variation settle nothing. Explain the effect in this passage or drop the marker.
- False-positive risk is highest for formal registers, non-native writers, templated genres (press releases, abstracts, legal text), and text passed through grammar tools. Say this explicitly whenever the band is Mixed or higher.
- Short texts (under roughly 150 words) rarely carry enough signal for any band above No notable pattern; say so rather than stretching.
- For consequential use (grading, hiring, publication, moderation), the recommended next step is always process evidence: ask for drafts, version history, a live writing sample, or a conversation about the content. Never recommend acting on the band alone.

### Interaction

- File path or paste: read, analyze, render the report.
- Several texts: one at a time; ask which first.
- Author samples provided: run the comparison section and weight it above generic markers.
- "Give me a percentage" or "is it AI, yes or no": decline the number, explain why in one sentence, give the band.
- "Did this student or candidate cheat?": give the band plus process evidence; text alone cannot establish authorship.
- "Which model wrote it?": decline; style does not identify a vendor.
- "Make it pass detection" or "humanize it": refuse evasion; rewriting for readability is editing work, outside this skill.

### Never

- Output percentages or probabilities of AI authorship.
- Name a model or vendor as the author.
- Call a single stylistic marker evidence; require co-occurrence or hard artifacts.
- Tell anyone a person cheated, lied, or violated policy.
- Rewrite the text or advise on evading detectors.
- Call a reference fabricated without checking it.

## Output format

Render inline by default:

```
# AI Authorship Read — {filename or "Pasted text"}

Text type: {genre / purpose}
Length: {word count}
Author sample provided: {yes, N words / no}

Band: {No notable pattern | Mixed signals | Strong pattern cluster}

## Hard artifacts
{list with quoted excerpt and what it is, or "None found"}

## Markers
- {marker name} — "{excerpt}" — why it reads as machine-typical — what else explains it

## Author sample comparison
{register, rhythm, error profile, vocabulary — or "No sample; skipped"}

## What this does not establish
{two to three plain sentences: no percentage, no vendor, no proof of authorship or misconduct; the false-positive profile for this genre}

## Recommended next step
{process evidence to gather, or "No action warranted"}
```

If the user says "save it", write `ai-authorship-{slug}-{YYYY-MM-DD}.md` in the working directory, where the slug is the first six lowercase-kebab words of the text's title or opening line, then give the path.

## Checklist

- [ ] Every marker is quoted from the text, with its innocent explanation beside it.
- [ ] Hard artifacts were checked before soft markers; suspect references were verified.
- [ ] One band assigned; no percentage, probability, or vendor named.
- [ ] "What this does not establish" is in the report.
- [ ] Process evidence recommended for any consequential decision.

## Composition / References

- `content-humanize` (the eight-dimension lens), `content-grounding` (checking references), `content-audit` (quality scoring, a different question), `content-edit` (rewriting for readability).
