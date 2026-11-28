---
name: developer-memory-curation
title: "Project Memory Curation: Verified Code Anchors"
description: "Build and correct a project's long-term memory by anchoring each entry to verified code, de-duplicating and linking entries. Use to learn a codebase."
license: Apache-2.0
compatibility: "Requires the memory store and read access to the repository."
domains: developer
rules:
  - match((?i)\blearn (this|the|our) (project|codebase|repo|repository)\b)
  - match((?i)\b(project|long-term|codebase|stored|saved)\s+(memory|memories|notes)\b)
  - match((?i)\b(memory|memories)\b.{0,40}\b(entries|entry|graph|store|gaps?|build|duplicates?|corrections?)\b)
  - match((?i)\b(store|record|save|memorize|correct|fix|update)\b.{0,40}\b(in|to|the|our)\s+(memory|memories)\b)
  - match((?i)\b(remember this|first-time memory|memory build)\b)
  - match((?i)\b(stored|saved|memory)\b.{0,40}\b(entry|entries|note|notes)\b.{0,60}\b(wrong|out of date|stale|verify|code)\b)
  - semantic(study this codebase and store what you learn as long-term memory, 0.72)
  - semantic(correct the stored memory about this project, 0.72)
  - semantic(remove duplicate entries from the stored project memory, 0.72)
  - semantic(record what we learned about this repo so later sessions know it, 0.72)
  - semantic(link related memory entries and verify them against the code, 0.72)
---

## Overview

The product of this work is the project's long-term memory: a complete, structured, de-duplicated, retrievable knowledge base about this codebase that makes every later session faster and more correct. Read code to understand it; do not change it. In this mode write memories and nothing else: no source edits, no builds, no refactor proposals.

- "Learn the project": run the autonomous grounding pass, then report what was stored.
- "Update memory about X": recall X, verify against code, reconcile, store.

## Mental model

Memory is only as useful as it is true. Phase 1 is autonomous and grounded, and its verification step is never skipped. Phase 2 is user-directed polish.

## Rules

### Phase 1: autonomous grounding (zero assumptions)

1. Survey existing memory: recall with broad multi-term queries about the project (architecture, modules, conventions, decisions, entry points). Know what exists before adding.
2. Map the codebase in one parallel discovery block: list the working directory for structure, read README, config and manifest files, outline the main source files, semantic code search for cross-cutting concerns, call-graph search to trace component relationships.
3. Verify before recording, and cite the source. Every fact traces to a specific place you read (a file:line, a signature, a config value), and that anchor goes into the memory. If you cannot point to where it lives in the repo, do not store it. No inference dressed as fact.
4. Reconcile with existing memory. A new fact not present: memorize. Existing memory matches code: leave it. Existing memory contradicts code: memorize the corrected fact linked to the stale entry with relationship_type "supersedes" (retrieval ranks it first; the old one stays for history); forget only entries that were never true. Never duplicate something recall already returned.
5. Link related memories as you store them: pass related_to to memorize using the ids recall returned, for example `related_to=[{target_id: "<id>", relationship_type: "related_to"}]`, so recall surfaces connected context rather than isolated trivia.

### Phase 2: user-directed polish

1. After grounding, summarize what was stored in 2 or 3 lines and ask in one line what to deepen, correct or prioritize.
2. For each user request: recall the area first, verify against code, then reconcile (memorize, forget, relate). User corrections are ground truth: store them at high importance immediately.
3. Keep going until the user is satisfied the memory is complete and accurate.

Batch independent calls. Recall always goes in the first discovery block. Reading code one file at a time after the targets are known is wasted work: batch the reads.

### What makes a good memory entry

- Atomic: one self-contained fact or decision per entry. Multi-fact entries surface for queries that match only one part and pollute recall.
- Provenance: anchor each entry to its source (`path/to/file.ext:NN`, a signature, a config key). A fact a future session cannot trace is a fact it cannot trust.
- Retrieval-phrased: write each entry in the vocabulary a future query will use ("authentication middleware", "retry/backoff policy", "DB migration flow"), not internal jargon. Recall is semantic; phrasing is what surfaces it.
- Right granularity: function, class or module level, not whole-file dumps and not brittle single-line snapshots. Capture the durable shape, not the volatile detail.
- Capture: architecture and module boundaries, key entry points (file:line), data flow, naming and style conventions, build and test commands, external dependencies and integrations, deliberate design decisions and their rationale, known constraints and gotchas.
- Skip: transient state, line-by-line restatement of code, facts obvious from a glance at the repo ("it's a TypeScript project"), multi-step how-to procedures (those belong in skills or rules), anything that changes every commit, speculation.

### Grounding labels

- [CONFIRMED]: read directly in the repo or stated by the user. Store as ground truth.
- [INFERRED]: you concluded it. Verify against code before storing; if unverifiable, do not store it.

### Importance scale

| Kind | Importance |
|---|---|
| User-stated facts and corrections | 0.8 to 1.0 |
| Architecture, design decisions, entry points | 0.7 to 0.9 |
| Conventions, commands, integrations | 0.5 to 0.7 |
| Verified but minor details | 0.4 to 0.5 |

### Tool hierarchy (read-only)

1. Symbol search: exact symbol or pattern.
2. Semantic code search: descriptive multi-term queries about functionality.
3. Call-graph search: relationships from a known file.
4. File outline: layout before reading.
5. Ranged reads: only what you need.
6. Full read: only small or config files.

Use shell only for read-only inspection the tools cannot do (listing git history). Never edit, never run builds.

### De-duplication and consolidation

Recall before every memorize; it is the dedup gate. Then choose deliberately.
- New fact, no overlap: memorize.
- Existing entry still accurate but thinner: there is no in-place update. Memorize the richer entry with a supersedes link to the thin one, never a near-copy without the link.
- Existing entry contradicted by code: memorize the corrected one with a supersedes link to the stale id; forget only entries that were never true.
- Two facts are connected: link them with related_to and the matching relationship_type (depends_on, implements, extends, related_to) rather than merging them into one blob.

A bloated, redundant store retrieves worse than a small accurate one. Refine, don't accumulate.

### Situations

- A user corrects a fact: memorize immediately with source user_confirmed and high importance, superseding the wrong entry (or forgetting it, if it was never true).
- Ambiguous request: ask one targeted question grounded in what you found.
- Two empty recall-and-search rounds on an area: stop, report the gap, ask.

## Output format

After a grounding pass or a polish round, report briefly:
- 1 line: what was learned or changed at a high level.
- Up to 6 bullets grouped by area (Architecture, Conventions, Entry points, Decisions, Gotchas), each a one-phrase summary of what was stored or corrected.
- 1 line of counts: N memorized, N corrected, N linked.
- End phase 1 by asking what the user wants to deepen next.

No prose essays, no restating code.

## Checklist

- [ ] Nothing stored that was not confirmed in code or heard from the user.
- [ ] Recall run before every memorize; no duplicates created.
- [ ] Contradicted entries superseded, or forgotten when never true.
- [ ] No transient state or line-by-line code restatements stored.
- [ ] No source edited, no build run.

## Composition / References

- `developer-context-scouting` produces a task-specific map of entry points; this skill stores durable project knowledge.
