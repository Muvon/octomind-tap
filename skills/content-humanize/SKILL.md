---
name: content-humanize
title: "Content Humanization"
description: "Review and revise stiff or formulaic writing with an evidence-based eight-dimension editorial diagnostic and seven-pass edit. Preserve facts, author voice, and platform authorship rules; no detector-evasion promises."
license: Apache-2.0
compatibility: "A draft and its intended audience/platform; source records and author samples when available."
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
  - semantic(make this writing sound more human and less robotic)
  - semantic(this draft reads like AI wrote it)
  - semantic(eliminate AI signature from this text)
  - semantic(rewrite so it does not read as AI generated)
  - semantic(my content keeps getting flagged as AI written)
---

## Overview

Use when a draft feels generic, inflated, repetitive, or unlike its intended author. Diagnose concrete reading problems and revise only what helps. Keep the eight-dimension diagnostic and seven-pass workflow below as editorial tools; they do not measure human authorship.

## Mental model

The goal is trustworthy, readable work, not text that fools a classifier. Facts and permitted authorship come before fluency. Use [content-voice](../content-voice/SKILL.md) for everyday writing choices and [content-grounding](../content-grounding/SKILL.md) for verification.

## Evidence and scope

- Research checked 2026-09-05. Detector findings depend on language, genre, model, sample, and evaluation setup. A 2026 Czech-language study found no systematic non-native bias in its tested detectors, unlike claims derived from earlier English studies. Neither result gives a universal social-post detector or a safe punctuation formula.
- Don't label a draft “80% human,” invent perplexity/burstiness thresholds, or claim that grammar, contractions, em dashes, or sentence variation prove authorship. Don't promise detector avoidance.
- Google's guidance emphasizes accuracy, quality, relevance, and value. E-E-A-T is not a single ranking factor, and quality-rater scores do not directly set rankings. Don't attach unsourced traffic multipliers, attention percentages, or search-update claims to this editing process.
- Check the destination's actual authorship policy before rewriting publishable prose. Some communities restrict AI-generated or AI-edited posts/comments; a stylistic rewrite or disclosure does not automatically make them eligible. Where necessary, provide factual research notes and leave prohibited public prose to the human author.
- Keep the requested scope. Editing voice does not authorize changing the speaker's opinion, results, product claims, affiliation, or source. If a claim is uncertain, verify or flag that specific claim while progressing on independent edits.

## Eight-dimension diagnostic

For each dimension, record “clear,” “needs revision,” or “evidence missing,” with a short excerpt and a reason. Prioritize factual/authorship problems over stylistic preferences. Do not sum these statuses into a detection or publication score.

| Dimension | Check |
|---|---|
| Source fidelity | Does every change preserve numbers, qualifiers, chronology, technical terms, and attribution? |
| Speaker and experience | Does the actual author own each first-person claim, decision, quote, or emotional reaction? |
| Substance | Can the reader identify the point, evidence, and useful consequence without generic filler? |
| Precision | Are claims concrete and bounded? Are necessary uncertainty and limitations retained? |
| Register | Does the wording suit the author, audience, topic, and language without invented slang or forced informality? |
| Rhythm | Do sentence and paragraph boundaries follow the argument, without choppiness or artificial variation? |
| Format and context | Does the piece fit its medium and conversation, with accessible text and enough standalone context? |
| Ending and action | Does it stop cleanly or offer a relevant next step, without empty morals, bait, or false urgency? |

A word or construction alone is not a defect. Explain its effect in this passage. A clear formal statement can pass; a casual unsupported testimonial cannot.

## Seven-pass rewrite

1. Preserve the factual contract. Mark claims and source gaps; lock quotations, measurements, disclaimers, and conditions that cannot change without evidence.
2. Find the point. Move the answer, observation, or supported claim forward. Remove repetitive setup, inflated significance, and material unrelated to the reader's task.
3. Make language precise. Replace vague modifiers with supplied facts, use direct verbs, and keep consistent terminology. Don't add numbers, anecdotes, or causal claims to make the prose vivid.
4. Restore the author's register. Follow real samples where available; otherwise use restrained plain language. Keep necessary formality and technical vocabulary. First person and contractions are options, not quotas.
5. Repair flow. Read aloud where useful; split overloaded sentences, join choppy ones, and trim empty transitions. Keep punctuation, comparisons, headings, or lists when they clarify meaning.
6. Adapt the medium. Rework spoken text for delivery, replies for their actual parent, and posts for the destination's format and audience. Review alt text, captions, link context, and disclosures separately.
7. Compare against the source. Check for invented experience, stronger certainty, omitted limitations, changed dates, or inaccurate CTA destinations. Resolve substantive findings before polishing again; don't keep rewriting solely to improve a self-assigned score.

For a short post, these are quick checks, not seven mandatory full rewrites. Stop when the identified problems are resolved. If evidence or intent remains missing, report it instead of manufacturing a smoother answer.

## Examples

Illustrative source: the team changed a retry setting after one failed import. It has not measured a general success rate.

Before:
> We learned the hard way that reliability isn't about tools. It's about mindset. One simple change fixed everything.

After:
> After an import failed, we changed the retry setting. We haven't measured whether that change improves the overall success rate.

The revision preserves the actual action and uncertainty without manufacturing a transformation.

Illustrative formal notice:
> Do not share the recovery code.

Keep it. Forcing a contraction, aside, or fragment would not improve this instruction.

## Checklist

When a diagnostic is requested, report the affected dimensions, excerpts, fixes, and unresolved evidence. Keep this review separate from public copy. Use another audit's editorial rubric only when requested; label its scores as judgments, not detector probabilities.

- [ ] Source facts, qualifiers, and disclosures survive the revision.
- [ ] No invented experience, mistakes, emotions, or persona signals were added.
- [ ] Each change fixes a stated reading problem rather than chasing a quota.
- [ ] The destination permits the proposed level of writing assistance.
- [ ] Before/after examples preserve meaning; unresolved facts are identified.
- [ ] Final prose and internal review notes are clearly separated.

## References

- [Al Ali et al., EACL 2026](https://aclanthology.org/2026.eacl-srw.20/) — language-specific detector evaluation; do not generalize its Czech findings to every language or platform.
- [Google AI-content guidance](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) and [people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content).
- [GOV.UK clear-language guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/writing-guidelines/clear-language/) — an example of professional plain language.
