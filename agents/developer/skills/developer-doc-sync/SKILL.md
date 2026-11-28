---
name: developer-doc-sync
title: "Doc Sync: Audit Docs Against Code"
description: "Audit docs for staleness against the code and git history, fix drifted claims with minimum-diff edits, and write new docs only when missing."
license: Apache-2.0
compatibility: "Requires git and shell; external link checks need curl and network access."
rules:
  - match((?i)\b(audit|sync|actuali[sz]e|refresh|update|check|scan|fix|bring)\b.{0,40}\b(docs|documentation|guide|docs page|doc page)\b)
  - match((?i)\b(stale|outdated|out of date|drifted|wrong|still (use|describe|mention)s?)\b.{0,60}\b(docs|documentation|guide|page|names)\b)
  - match((?i)\bdocs?\b.{0,40}\b(match|in sync with|drift\w*|in line with)\b.{0,30}\b(code|implementation|behavio(u)?r)\b)
  - match((?i)\b(write|create|document)\b.{0,30}\b(missing|new)?\s*(docs?/[\w.-]+|[\w-]+\.md|guide)\b.{0,80}\b(links?|promises?|mentions?|never created|doesn.t exist|no such file)\b)
  - match((?i)\b(link|links|linked|mention|mentions|promises?)\b.{0,50}\b(page|guide|file|section)\b.{0,50}\b(doesn.t exist|does not exist|never created|no such|missing)\b)
  - semantic(find documentation that no longer matches the code, 0.72)
  - semantic(the docs are out of date, fix them to match the code, 0.72)
  - semantic(check that every claim in our docs is still true, 0.72)
  - semantic(update the documentation after this refactor with minimal changes, 0.72)
---

## Overview

Keep every claim in a project's docs true to the code, fix drift, and write new docs only when something real is missing. Work as an evidence-driven engineer, not a copywriter: every assertion traces to a source of truth (the code on disk plus `git log` and `git blame`), every edit is minimum-diff, and every unverifiable claim is flagged or removed, never guessed.

Three modes:
- Audit: scan, classify staleness, report. No edits.
- Sync: audit, then fix everything drifted. The default for "actualize", "update" or "refresh the docs".
- Write: a new doc, only on explicit request or when an existing doc promises content that does not exist.

A documentation plan with drafts, requested by a brief, follows the brief's procedure and output contract; ground the drafts in the source and return them in the response. "Fix X" means fix only the docs covering X. CHANGELOG, release notes and historical records are append-only: surface their drift and leave existing records intact. A draft plan can include proposed entries.

## Rules

Name the next two or more tool calls and batch them. Verifying independent claims one at a time is wasted work.

### Phase 1: discovery (one parallel block)

- shell: `git ls-files '*.md' '*.mdx' '*.rst' '*.txt' '*.adoc'` and `git log -1 --format=%ci -- <doc>` per doc.
- Root manifests that exist (package.json, Cargo.toml, pyproject.toml, go.mod, Gemfile, composer.json, *.csproj, and so on).
- shell: `git log --since=<oldest-doc-date> --name-only --pretty=format:` for code changed since the docs.
- Directory listing for top-level structure; file outline for the public surfaces docs likely reference.
- Memory recall: doc conventions, project type, audience.
- Web search only when docs track external standards or APIs.

Then emit:

```
## 📊 Doc Inventory
- Corpus size: N docs (M lines total)
- Languages/formats: [md, rst, ...]
- Oldest doc: <path> (<date>)
- Code paths changed since oldest doc: K files
- Project type: <CLI / library / service / framework / monorepo>
```

### Phase 2: triage

| Level | Meaning |
|---|---|
| HIGH | Older than its referenced code; cites paths, symbols, commands, versions, config keys, env vars, install steps, APIs |
| MEDIUM | Architecture, flows, integration patterns, responsibilities |
| LOW | Narrative without code-bound claims; touch only on request |
| HISTORICAL | CHANGELOG, release notes, ADRs, migration logs; never edit |

Batch HIGH and MEDIUM by directory or topic (`docs/api/*`, `docs/guides/*`, root) for phase 3.

### Phase 3: verify every checkable claim (parallel across docs and claim types)

- Path or internal link: read it. Symbol: symbol search, signature matches. CLI flag: symbol search in the argparse, clap or cobra definitions. Env var or config key: symbol search the literal.
- Command or install step: manifest plus scripts. Version: manifest plus git tags. Snippet: the referenced APIs exist with the shown signature.
- External link: shell `curl -sIL -o /dev/null -w '%{http_code}' <url>`, only if requested.
- Architecture: spot-check 2 or 3 load-bearing assertions with call-graph and semantic code search. Behavior: semantic code search, then read the implementation.

Tags: VERIFIED, STALE (record the correct value and `file:line`), ORPHANED (deleted or renamed; find the rename with `git log -S<oldname>`), UNVERIFIABLE. No evidence means UNVERIFIABLE, never VERIFIED.

### Phase 4: plan (before any write, one block)

```
## 📝 Change Plan

### <doc/path.md> — <N> changes
- UPDATE: <claim> → <new value> (evidence: file.rs:42)
- DELETE: <claim> (orphaned, no replacement found)
- FLAG:   <claim> (unverifiable, load-bearing — leave HTML comment)

### <doc/path3.md> — RECOMMEND DELETION
70%+ stale, no current equivalent. Awaiting user confirmation.
```

An empty plan means leave the doc. A full-deletion candidate means stop and ask. Audit ends with the plan; sync shows it briefly and continues.

### Phase 5: execute (parallel across files, one batched edit per file)

- Change only what is wrong; preserve voice, structure, surrounding prose and formatting quirks.
- Stale code blocks become copy-paste-runnable equivalents verified against the code. Renames use the new name, confirmed via `git log -S<oldname>`.
- Two plausible truths: use the evidenced one; tied means FLAG.
- A load-bearing unverifiable claim gets `<!-- TODO(doc-sync): verify — <what's unclear> -->`; a decorative one is deleted.
- Every added sentence answers a STALE or ORPHANED plan finding.

### Phase 6: re-verify

Re-run the checks on edited docs. No STALE or ORPHANED may remain except flagged items.

### Write mode

Triggered by a request, or by a doc pointing at a missing target ("See docs/architecture.md" that does not exist). Run phase 1 scoped to the topic. Identify the audience, the project type, and one Diátaxis type per page: tutorial (learning by doing), how-to (one task, experienced reader), reference (neutral facts mirroring code), explanation (why). Link out instead of mixing. Match the project's `docs/` convention, naming and voice. Use the minimum viable structure: no boilerplate sections, TODO placeholders or aspirational content; ground claims as in phase 3. Output the draft and ask "Write to <path>?"; an autonomous brief that names the path writes it and reports. No auto-generated API reference or catalog docs unless asked.

New prose reads on first pass for someone who has not seen the code. Define each term before reusing it. Put the outcome before the mechanism (what the reader gets, then how). Put internal names (config keys, module names) in code formatting only where the reader needs them to find something, and use the plain word elsewhere. Headings are plain noun phrases, never slogans. Keep honest qualifiers ("off by default", "opt-in") and verify absolute claims ("always", "never", "any") against the code.

### Evidence rules

- Every STALE or ORPHANED tag and plan UPDATE cites a `file:line` pointer. Every written line traces to a verified claim or an explicit flag; "it probably means X" is not evidence.
- User-facing docs prioritize accuracy and clarity, architecture docs current-state truth; historical docs are immutable; narrative rarely needs maintenance. Explanation drifting into a how-to is the commonest structural rot: flag it, don't restructure.
- Usual drift: old install commands, stale import paths, renamed config keys, deprecated flags, moved paths, lagging versions, "coming soon" on shipped features, diagrams of removed components, dead links, deprecated-API examples.
- Keep the existing voice, contraction habit, terminology, humor and opinion. You are the custodian, not the author.
- Never: rewrite accurate docs (style is not staleness); add unrequested sections (a surprise table of contents, an invented FAQ); move content between docs; merge or split docs unasked; fix typos or formatting in paragraphs you are not editing; add disclaimers, "last updated" footers, meta-commentary or boilerplate ("Welcome to the docs!"); touch docs outside scope; create docs in sync unless a missing target was referenced; edit historical records.
- After sync, memorize the directories needing most work, the commonest drift and the conventions learned; after write, the template chosen and why. Importance 0.6 to 0.8.

### Mode choice

"audit", "check", "review", "scan" means audit. "update", "actualize", "refresh", "sync", "fix" means sync. "write", "create a doc" means write. Ambiguous: ask "Audit (report only) or sync (audit + fix)?"; an autonomous brief means audit, and say so. Stop and ask on: a full-deletion candidate, contradictory ground truth (code against code, manifests disagreeing on a version), an empty stated scope. Emit the inventory, the plan (sync) and the final report, then stop; no confirmations between sync phases.

## Output format

Three layers in every mode; the triage reads in 5 seconds.

Layer 1, triage (first; skipped in write):

```
## 📚 Doc <Audit | Sync | Write>

<N> docs · <K> claims · <M> flagged

| Doc | Changes | Driver | Severity |
|-----|---------|--------|----------|
| `path/to/doc.md` | 3 | renamed CLI flags | 🔴 |
```

Changes is the number of claims affected (Issues in audit). Driver is the dominant cause in 4 words or fewer (`version bump`, `directory restructure`, `API rename`, `link rot`). Severity is 🔴 user-visible breakage, 🟡 developer-confusing, 🟢 cosmetic; the highest claim wins.

Layer 2, evidence (one collapsed card per row, same order):

```
<details>
<summary><code>path/to/doc.md</code> · <N> changes · <driver></summary>

| Was | Now | Source |
|-----|-----|--------|
| `<old claim, verbatim or short paraphrase>` | `<new value>` | `file:line` |
| `<old claim>` | _removed (orphaned)_ | `git: <commit-sha>` |

</details>
```

Was is the literal token, or a paraphrase of 60 characters or fewer. Now is the verified value or `_removed_`, `_renamed_`, `_flagged_`. Source is never empty. Audit columns: `Claim | Status | Current truth`. Write: the card is the full draft, then one `| Claim | Source |` table. More than 10 changes: a full table, and consider recommending deletion.

Layer 3, flags (omit if empty):

```
### ⚠ Needs review
- `path/to/doc.md:128` — <one line: what's unclear and why>
```

At most 120 characters per item. Drifted historical docs appear only here.

Never list clean docs. Tables only, no prose; plain `file:line` (URLs only if the repo URL was confirmed; never invent permalinks); no closing line. Empty results: audit gives `## 📚 Doc Audit` then `N docs scanned · all current.`; sync gives the same plus `· no changes needed.`; a refused write gives one line saying why.

## Checklist

- [ ] No claim stated without the symbol search, implementation read, manifest or `git log -S` that proves it; no change without a `file:line` pointer.
- [ ] Only facts changed, never voice, structure or style.
- [ ] Historical records untouched; drift in them listed under Needs review.
- [ ] Audit delivered the report; sync the report and a summary; write the draft and its grounding.
- [ ] Nothing stale found: one line, no trailing summary or offer.

## Composition / References

- `changelog-writing` and `release-notes-writing` own CHANGELOG and release-note entries; `readme-writing` owns README rewrites.
