---
name: developer-diff-briefing
title: "Diff Briefing: Plain-Language Review Cards"
description: "Turn a diff, commit, branch or uncommitted changes into plain-language review cards with traced risk and source links. Use to brief a change."
license: Apache-2.0
compatibility: "Requires git and a checked-out repository; permalinks need an origin remote."
capabilities: versioning
rules:
  - match((?i)\b(brief|summari[sz]e|explain)\b.{0,40}\b(this|the|my|current|latest|last|a)\s+(diff|commit|branch|PR|pull request|uncommitted changes|staged changes)\b)
  - match((?i)\breview cards?\b|\bchange cards?\b|\bbrief (me )?on\b.{0,30}\b(changes|diff|commit|branch)\b)
  - match((?i)\bplain[- ](language|english)\b.{0,60}\b(change|changes|commit|PR|branch|refactor|merge)\b)
  - match((?i)\b(what|how)\b.{0,30}\b(PR|commit|branch|merge|refactor)\b.{0,40}\b(changes?|could break|might break)\b)
  - match((?i)\b(explain|summari[sz]e)\b.{0,40}\b(what|how)\b.{0,40}\b(changes?|behavio(u)?r)\b.{0,40}\b(users?|customers?|risks?|break)\b)
  - semantic(explain what this commit changes and who it affects, in plain language, 0.72)
  - semantic(brief me on the current uncommitted changes, 0.72)
  - semantic(summarize this pull request for a reviewer who has not read the code, 0.72)
  - semantic(what is risky about the changes on this branch, 0.72)
---

## Overview

Turn a code change into review cards for a reader who has not seen the code and may not be a developer: anyone the change affects. No line-by-line review. Say plainly what the system now does differently, why, who it affects, and what could go wrong. The diff is the footnote; the card is the review; identifiers are evidence, not narrative.

The skill covers behavioral review of an existing change. It does not write or edit code, changelogs or release notes, and it does not spec new behavior.

## Mental model

A claim is only as strong as the evidence you read. Every finding is traced to code you opened; the default verdict is "no finding". Findings are worth a busy engineer's time or they are omitted.

## Rules

### Input, by kind

- Pasted diff: use it as given.
- Commit or range: git_log plus git_diff.
- "Read current changes": git_status plus git_diff (unstaged and staged) in parallel.
- Branch: `git diff main...<branch>`.
- File paths: a diff scoped to them.
- Ambiguous: run git_status first. The default is everything uncommitted plus staged; staged versus unstaged is never a reason to ask. In an interactive session, ask one question only if truly needed. Under an autonomous brief, take the default and say so.
- Nothing to analyze: say exactly "Nothing to brief. Give me a diff, a commit hash, or ask me to read the current changes."

### Phases

Run phases 1 to 6 in order, each phase's independent calls in one parallel block.

Phase 1, retrieve:
- Full diff (paste, git_diff, or git_show). Commit messages are ground truth for intent; note when vague.
- `git log --follow -n 10 -- <file>` on changed files: is the change part of a series?
- `git remote get-url origin` (HTTPS form, strip `.git`; this is REPO_URL) and `git rev-parse HEAD` (COMMIT_SHA). Permalinks: REPO_URL/blob/COMMIT_SHA/path#L42-L67 (GitLab: REPO_URL/-/blob/COMMIT_SHA/path#L42-67). No repo, no remote, or uncommitted changes: plain `path/to/file` lines 42-67.

Phase 2, understand each added, removed or modified symbol:
- Outline the file, then read the changed block in the current file with enough context to see its role (callers, return value, state touched).
- Changed signature: read the full body. Changed type or struct: find where it is constructed or pattern-matched; those are impact candidates.

Phase 3, trace impact of every changed public symbol or behavior:
- Semantic code search on what the symbol does (not its name), call-graph search outward from the file, symbol search for call sites, instantiations and trait or interface implementations.
- Read call sites one level deep (two in hot paths); judge whether each consumer breaks, degrades or silently changes.
- Diff-only (paste-only, or symbol not in the tree): confidence caps at MEDIUM; never BREAKING without a traced caller.

Phase 4, confidence is a count of evidence. Factors: (1) read the changed code in the file, (2) read at least one real consumer, (3) commit message matches the code (or there is none).
- HIGH `●●●`: all three, or the first two with no commit message.
- MEDIUM `●●○`: factor 1 and either 2 or 3.
- LOW `●○○`: factor 1 only. State what you could not verify.
- Factor 1 missing: no card.

| Claim | Required evidence |
|---|---|
| X is affected | you read how X uses the changed code |
| Breaking change | a caller depends on the old behavior |
| No downstream impact | local or private symbol, and semantic and call-graph search found no consumers (exported or public: use the impact radius wording below) |
| Intent was Y | the commit message says so, or context makes it unambiguous |
| Risk: edge case Z | you traced the path where Z occurs |
| R<n> open | you traced the path, then searched it for a guard and for a test that exercises it, and found neither |
| Divergence: drift | you read at least two instances of the established pattern; fewer is a question |

No evidence: "Unable to determine: <what was missing>", or omit. Confidence cannot exceed what the card's Source proves: every affected or BREAKING claim links its call site, or the claim is deleted or the card drops to LOW. A check you cannot point at counts as failed.

Phase 5, cross-cutting. Changed error handling (missing, weakened, added), interface contracts (signatures, return and error types), concurrency (locks, channels, async boundaries), auth and permission checks, and data schema or serialization always get their own card or an explicit risk entry, whatever the diff size.

Phase 6, intent versus reality:
1. Does the code do what the message says? "No behavior change" yet a return value changed, or a fix that silently changes other behavior: flag it. Vague or missing message: say intent is unverifiable.
2. Does it fit the patterns seen in phases 2 and 3? A different error style, a second way to do something done one way, bypassing an abstraction everything else uses: drift.
3. Is it half of something (a field never read, a function never called, a migration without rollback, an unused feature flag)? First rule out: exported or public symbol, dynamic dispatch via trait or interface, serialization or reflection, a handler registered elsewhere (callback, route, CLI), FFI export. If you cannot rule one out, or the search is incomplete, it is a question, never drift and never silence.

Only real signals go in divergence. Then write the triage, the cards and the file list, and stop. No confirmation requests, no preamble, no summary or sign-off.

### Grouping

One card per intent, any file count: a rename across 15 files is 1; a feature and its tests is 1; an auth refactor plus rate limiting is 2; a bug fix plus unrelated cleanup is 2. Never one card per file, or per commit when commits share intent.

### Plain language

Intent, what changed, impact radius, risk, questions and divergence must read for someone who never opened the repo: name components by role ("the completion checker", not "parse_verdict"), describe behavior instead of language or framework jargon, keep paths and identifiers in Source and snippets. Plain does not mean longer. Test: a non-developer stakeholder follows what changed and who it affects.

### Pragmatic filter

Before every risk, impact or divergence finding ask: a real failure mode or five unlikely conditions? Felt by a caller, or technically true but irrelevant? Real drift or a style that works fine? Would you raise it in a 10-minute PR review with a busy team? If not, omit it.
- A real risk is obvious in one sentence ("Redis down = rate limiting disabled"); an essay is hedging.
- A risk or impact appears in one card only.
- Pragmatic is not permissive: flag a real HIGH even if uncomfortable; drop a contrived MEDIUM.
- Skip formatting, import order, whitespace, style, praise, hedging and filler. Mention tests only when they reveal non-obvious system behavior.

### Exposure versus residual

Two separate verdicts.
- Exposure: how much the change could hurt if wrong, judged by what it touches. 🔴 auth or permissions, money, data schema, serialization or migration, concurrency, public contracts, deletion. 🟡 behavior other components or users observe. 🟢 isolated. More work cannot lower it; it tells the reader how closely to look.
- Residual: findings still open in the code. Every risk failure mode with no guard on its path and no test exercising it, plus every 🔀 intent mismatch and 🧩 incomplete change. Number them R1, R2 and so on in card order. Architectural drift and questions are not residual.
- A careful auth change is 🔴 exposure with 0 residual; a trivial helper with an unguarded crash path is 🟢 exposure with 1 residual.

## Output format

Three layers, strict.

Layer 1, triage, always first:

```
## 📦 Brief: <one-line description of the overall changeset>
<Subsystem not self-evident: one plain sentence on what it does. Omit when obvious.>
**Exposure:** 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW · **Residual:** N open (R1, R2…) · **Cards:** N

| # | Change | Risk | Confidence |
|---|--------|------|------------|
| 1 | <one-line behavioral summary> | 🔴/🟡/🟢 | ●●● / ●●○ / ●○○ |
```

One row per card; summaries are behaviors.

Layer 2, cards, one per logical change, at most 5. When more are warranted, write 5 and add: "⚠️ This changeset should be split. Too many independent concerns to review safely as one unit."

```
<details>
<summary>Card N/M: <title, behavior not filename> · 🔴/🟡/🟢 · ●●●/●●○/●○○</summary>

**INTENT**
One sentence: why the change was needed, not what it does.

**WHAT CHANGED**
- At most 5 bullets of behaviors, not files, lines or identifiers.
- ❌ "Modified timeout parameter in api.ts line 47" → ✅ "External API calls now timeout after 5s instead of hanging indefinitely"

**IMPACT RADIUS**
- Affected components by role, the effect operators or users observe, BREAKING if applicable; each appears in Source.
- Nothing found: local or private → "Isolated change — no downstream impact detected." Exported or public → "No internal consumers found; external API consumers not verifiable." Diff-only → "Unverified — diff-only."

**RISK**
🔴 HIGH / 🟡 MEDIUM / 🟢 LOW. Always present; traced failure modes only. Prefix each open one (no guard, no test) with its ID: "R1 — Redis down = rate limiting disabled".
LOW → "No significant risk. Change is isolated / well-guarded / trivially reversible."
HIGH or MEDIUM needing two sentences to justify probably isn't.

**QUESTIONS** (omit if nothing is genuinely unclear)
Decisions that look intentional but could be accidental, never what more reading would answer.

**DIVERGENCE** (omit if phase 6 found nothing real)
- 🔀 Intent mismatch: "Commit says X but code does Y"
- 🧭 Architectural drift: "Rest of module does X this way; this introduces a second way that will cause confusion"
- 🧩 Incomplete change: "Field Z is added but never read — looks like part of a larger change"
One sentence each. Intent mismatch and incomplete change carry their R<n> ID.

📎 **Source**
- [`path/to/file.rs#L42-L67`](REPO_URL/blob/COMMIT_SHA/path/to/file.rs#L42-L67) — <what this block is>
</details>
```

An inline snippet only for a single critical condition, expression or signature (8 lines or fewer) that resolves ambiguity prose cannot and bears on risk or questions; otherwise link.

Layer 3, source, always last:

```
<details>
<summary>📂 Files changed (<N> files, ~<X> lines)</summary>

- [`path/to/file.rs`](REPO_URL/blob/COMMIT_SHA/path/to/file.rs) — <role of this file in the change>
</details>
```

## Checklist

- [ ] Every finding traced with a tool and backed by a Source link; none asserted from the diff alone.
- [ ] No "no downstream impact" for an exported symbol.
- [ ] Narrative sections free of identifiers and jargon.
- [ ] Empty questions and divergence omitted; at most 5 cards; output stops after the source section.
- [ ] Exposure and residual stated separately; R-numbers match card order.

## Composition / References

- `code-review-lenses` covers multi-lens bug and security review; this skill explains a change in plain language.
