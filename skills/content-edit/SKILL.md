---
name: content-edit
title: "Content Editing: Diagnose, Fix, Humanize"
description: "Edit an existing draft: diagnose with the audit rubric, apply surgical fixes that keep the author's voice, and humanize AI-sounding text."
license: Apache-2.0
compatibility: "Needs file read and write, shell for a Git check, and web search to verify facts. Works inside or outside a Git repository."
capabilities: shell
domains: writer
rules:
  - match((?i)\b(edit|fix|polish|tighten|proofread|revise|improve|rewrite)\s+(this|my|the|our)\s+(draft|post|article|blog|copy|piece|essay|thread|newsletter)\b)
  - match((?i)\bhumani[sz]e\s+(this|my|the|it)\b)
  - match((?i)\bmake\s+(it|this)\s+(sound|read)\s+(more\s+)?(human|natural|less\s+like\s+AI)\b)
  - match((?i)\b(sounds?|reads?)\s+(like\s+)?(AI|ChatGPT|a\s+robot)\b)
  - semantic(edit my draft but keep my voice)
  - semantic(apply the audit findings to this article)
---

## Overview

Fix an existing piece without rewriting it: diagnose what is broken, change only what needs changing, and keep the author's voice. Also humanize AI-generated text so it reads like a skilled human wrote it. The outcome is the edited text (saved in place or as a suffixed copy), a plain-prose diff summary, and a list of anything left unverified. This skill does not write from scratch, only scores without editing (that is `content-audit`), or publishes.

The `content-audit` skill owns the diagnosis: rubric, scoring, axes, severity tiers, finding format, report template, and content-type detection. Apply it as written; keep no parallel rubric. This skill is the surgery that follows.

## Mental model

Cut what is dead, strengthen what is weak, leave what works alone. Don't rewrite a good sentence just to show you edited it. Don't add words; only remove or replace. Preservation beats fabrication: an unverifiable specific stays put and gets flagged.

## Rules

### Edit session

1. Read. Load the file from disk or accept pasted content. In parallel, recall brand voice, target audience, style guide, tone preferences, and past edits from memory.
2. Entity inventory. Before diagnosing, list every named entity: tools, products, people, libraries, versions, statistics, URLs, commands, direct quotes. Triage each (familiar, unfamiliar, time-sensitive) and flag anything unfamiliar or time-sensitive for verification before any rewrite touches it.
3. Diagnose. Run the full `content-audit` rubric for the detected content type and produce its canonical report. Detect the content type and confirm it at the top of every session.
4. Present the findings. Confirm the edit scope ("all critical and moderate", "critical only", "a specific section") and any flagged entities (offer to search, or ask for canonical sources).
5. Edit section by section. Voice, structure, and rhythm edits are always safe. Factual edits only on verified entities (training-data confidence, confirmed by research, or a user-provided source).
6. Summarize the diff in plain prose: what changed and why.
7. Save, following the file handling rules below.
8. Memorize only durable style decisions, recurring issues found, and confirmed voice notes. Never memorize the edited text.

### Humanization mode

Triggers: the `content-audit` Slop-risk axis at 5 or below, or the Voice axis at 5 or below; the user says "make it sound human", "humanize this", or "it sounds like AI"; or the humanization diagnostic finds concrete source, register, clarity, or flow problems. Then use the `content-humanize` skill:

1. Scan with its eight-dimension diagnostic.
2. Report evidence-backed findings, affected dimensions, and missing sources, in conversation. This does not replace the audit report shape. Humanization statuses are editorial judgments, not authorship probabilities.
3. Rewrite with its seven-pass technique, section by section.
4. Verify by re-scanning. Confirm the identified problems are resolved and that source meaning, qualifications, and platform authorship rules are preserved. Don't rewrite only to raise a self-assigned score.
5. Save as described below; the suffixed copy is `[filename]-humanized.md`.

Show before and after for changed passages, report the resolved findings and the remaining source gaps, and keep audit scores separate from the humanization diagnostic. During humanization, preserve factual meaning, qualifications, and the author's argument. Within the agreed scope, change ordering, sentence boundaries, and format only to resolve identified reading problems.

### Editing standards

- Voice: the author's voice is sacred. Amplify it, don't replace it: short punchy sentences stay short and punchy, and a specific phrase or rhythm is preserved. Change voice elements only where they actively hurt the piece (per the `content-audit` Voice axis findings). Every edit aligns with the brand voice; if it is undocumented, ask once whether to capture style preferences as you edit.
- Passive voice: review passive constructions when they obscure responsibility or meaning. Use active voice when it clarifies the point; keep passive when the actor is unknown or the process, result, or intended emphasis warrants it.
- House style: apply the user's or the stored house style first. With none, ask once which guide governs (Chicago 18th edition (2024) for books and long-form, the current AP Stylebook (revised yearly) for news and web). Don't mix conventions or impose one silently.
- Specificity: replace every vague claim flagged in the diagnostic with a verified specific (searched or user-sourced), narrow it to what the source supports, or cut it. Call it opinion or hypothesis only when the author actually supplied that position; hedging doesn't replace missing evidence. Never leave a vague claim standing as fact.
- Answer-first (long-form): in article and blog edits, every major section opens with a one- or two-sentence direct answer, so an engine reading only first sentences still gets the key takeaways. Rewrite sections that bury the answer.
- Leave no filler phrases standing.

### Web search in editing

Search only to verify a statistic, version, price, or "latest" claim before keeping it; to check an unfamiliar or post-cutoff named entity (tool, product, person, library); to find a better or more recent data point for a claim the user wants to keep; or to check what actually ranks for the target keyword. Run at most two or three targeted queries per claim.

If searches fail to confirm a claim, stop and ask: "I can't verify [claim]. Options: (a) share a source, (b) drop it, (c) mark `[needs verification]` inline." Tidying up an unverifiable claim is the highest-cost failure mode in editing. Don't fabricate statistics, versions, prices, names, URLs, or quotes to replace vague claims, and don't "improve" any specific (function name, version, command flag, quote, stat, URL, person name) you did not verify.

### File handling

- Input: a file path means read and edit the file; pasted content means work in the session and save to disk only on the user's direction.
- Run `git rev-parse --is-inside-work-tree` once at session start; exit 0 means inside Git.
- Inside Git (the default for projects): edit in place after confirmation. Git is the safety net, so don't drop `*-edited.md` or `*-humanized.md` shadow copies into a tracked tree.
- Outside Git (single-file workflows, /tmp, scratch directories): write `[original-name]-edited.md` (or `-humanized.md`) so the user keeps the original.
- If the user explicitly asks to keep both even inside Git, write the suffixed file.

### Interaction

- File path or pasted content: run the diagnostic, present the report, confirm the scope (for pasted content, also ask for a save path).
- "Just fix the obvious stuff": critical and moderate only, skip minor. "Full edit": everything in the diagnosis. "Only fix the intro": that section only.
- "Score only": render the audit and stop; no edits.
- Revision after an edit: re-diagnose the edited section only.
- The user pastes an existing audit report: skip the diagnostic and go straight to scope confirmation against the supplied findings.
- Autonomous, non-interactive brief, or a self-contained brief (for example an audit report plus "edit in place"): skip scope confirmation and the questions above. Apply critical and moderate fixes (or the scope the brief names), leave unverifiable specifics untouched with an inline `[needs verification]` marker, save per the Git-aware rule (pasted content: return the full edited text in the final message), and report the diff summary with assumptions. When the brief lists what to keep (facts, numbers, links, citations, hedges), that list wins over audit findings: leave the item and name it in the diff summary. Nobody can answer a question mid-run, so make the reasonable call, state it in one line, and continue; stay inside the brief and report anything outside it in one line.

### Never

- Edit without showing the diagnosis first, or save edits without a confirmed scope (the user's, or the autonomous brief's).
- Rewrite the entire piece when targeted fixes suffice, change the author's voice, or add content, sections, or ideas not in the original.
- Claim a step you did not run or a result you did not verify.

## Output format

Diagnostic phase: render the canonical `content-audit` report (per-axis 0 to 10 table, overall 0 to 100, verdict, prioritized findings with evidence and fix direction, what's working, recommended next step), then ask: "Proceed with all critical + moderate fixes, or focus on specific findings?"

Edit phase: apply the edits for the confirmed scope, then render a plain-prose diff summary:

```
Diff summary

- Removed: {N} filler phrases, {N} hedging constructions, {N} passive voice instances
- Rewrote: intro hook ({why}), conclusion ({why}), 2 sections for answer-first structure
- Preserved: author's voice rhythm, specific number claims, named entities
- Flagged-unverified: {list; left in place with inline [needs verification] marker}
- Saved: {path} (in-place / -edited.md / -humanized.md)
```

Don't re-render the full audit report after editing. For a re-score, run a read-only audit with the `content-audit` skill on the new file.

## Checklist

- [ ] Content type detected and confirmed; entity inventory done.
- [ ] Diagnosis shown and the scope confirmed (or the autonomous defaults stated).
- [ ] Every edited specific verified or left untouched and flagged.
- [ ] The author's voice is preserved; no content added.
- [ ] Saved per the Git-aware rule; diff summary delivered.

## Composition / References

- `content-audit` (diagnosis), `content-humanize` (humanization technique), `content-voice` (AI-pattern review), `content-grounding` (entity triage), `content-geo` (answer-first structure).
