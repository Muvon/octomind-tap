---
name: assistant-knowledge-base
title: "Knowledge Base Curation: .box Notes"
description: "Write structured .box notes for the project's knowledge base and answer questions from indexed knowledge with cited sources. Use for durable project facts."
license: Apache-2.0
compatibility: "Needs the knowledge tool with an indexed project box and write access to the project directory."
capabilities: knowledge
domains: assistant
rules:
  - match((?i)\b(what do we know|what does the (knowledge base|box|project) (say|know)|what our knowledge base says)\b)
  - match((?i)\b(search|check|query|extract|read)\b.{0,40}\b(the |our )?(knowledge base|\.box|indexed notes)\b)
  - match((?i)(\.box/?|knowledge base|box notes?|org box)\b.{0,60}\b(note|notes|decision|convention|readme|map|folders?|reorgani[sz]e|supersede|promote)\b|\b(note|notes|decision)\b.{0,60}(\.box|knowledge base|org box))
  - match((?i)\b(write|add|save|capture|store|record|update|supersede|promote|reorgani[sz]e|consolidate|curate|draft)\b.{0,60}(\.box|knowledge base|box note|org box|durable (facts?|notes?|knowledge)))
  - match((?i)\bpromote\b.{0,40}\b(memory|facts)\b.{0,30}\bnotes?\b)
  - semantic(capture this decision as a durable project note, 0.72)
  - semantic(what does our knowledge base say about this topic, 0.72)
  - semantic(write a note recording this convention for the project box, 0.72)
  - semantic(reorganize our project notes and mark outdated decisions as superseded, 0.72)
---

## Overview

Own the project's durable knowledge: the `.box/` directory of markdown files that octobrain auto-indexes into the project scope and every agent can search. Two jobs, both grounded: write durable knowledge as retrieval-optimized notes, and answer questions or extract data from the indexed knowledge base with cited sources.

Knowledge is not memory. Memory (memorize and remember) holds volatile state such as user profile, session context and in-flight work that can change or lose meaning. The box holds only durable truths any agent may need: decisions with rationale, domain facts, constraints, conventions, integrations.

This skill covers creating, updating, superseding and reorganizing `.box/` notes, maintaining `.box/README.md` (map and authoring rules), answering "what do we know about X", extracting data with provenance, and promoting durable facts out of memory into notes. It does not cover domain work, writing any file outside `.box/`, curating memory, or answering project-knowledge questions from general knowledge.

The default box is `.box/` in the current working directory unless the user names another location. The org box (the `<host>/<org>/octobrain-box` repo) is read like any indexed source and never written: propose the addition to the user. Placement test: would another project reuse this unchanged? Then it belongs in the org box. Reference org notes from project notes, never copy them; when the two conflict, the project note wins.

## Rules

### Reading: question or extraction request

1. One parallel block: `knowledge(command="search")` with 2 to 3 differently phrased queries; add `knowledge(command="match")` with an exact regex when the ask names literals (config keys, error strings, flags, ids).
2. Snippets insufficient: `knowledge(command="read")` the specific file. Never answer beyond what the sources support.
3. Deliver the answer or extracted data with a Sources list of file paths. Nothing found: say the knowledge base has nothing on it, name the closest hits, stop. Never fill the gap from general knowledge.

### Writing: durable knowledge arrives (from the user, a brief, or memory)

1. Durable test: write only if all four hold.
   - Context-independent: true outside this session ("we deploy via X", not "the deploy just failed").
   - Concept-oriented: a fact, decision, rule or procedure, not an event or progress note.
   - Persistent: still true and useful next month; expiring facts get a `review=` date in the meta line.
   - Cross-agent: a different agent would benefit, not just this conversation.
   Any fail means it belongs in memory, not the box; say so instead of writing.
2. Dedup gate: search and match the box for the concept first. An existing note covers it: update that note in place. Never write a near-duplicate.
3. Write the note per the format below. A new file gets its line in the README map.
4. Empty box on first write: bootstrap `.box/README.md` with the map and a condensed copy of the authoring rules, then write the first note.
5. Just-written notes may not be indexed until the next box sync: verify writes by reading the file, not by search.

### Promoting: "build the knowledge base" or "consolidate what we know"

Run `remember()` with broad multi-term queries, run every recalled fact through the durable test, apply the dedup gate per surviving fact, write notes in batches, then report what was promoted and what stayed memory-only and why.

Batch independent searches, reads and edits in one block; go sequential only when an output feeds the next call.

### Layout: shallow, subject-based

```
.box/
  README.md                      map of content + authoring rules (reserved by octobrain: never indexed)
  overview.md                    what this project is — one orientation page
  glossary.md                    one ## per canonical term
  architecture/ domain/ guides/ reference/   subject folders — areas of the project, not doc types
  decisions/adr-NNNN-<slug>.md   one decision each — Context / Decision / Consequences
```

Folders are subject areas, at most 2 levels deep. Don't create a folder for fewer than 3 notes: loose topic pages live at the box root. No archive folder: retire by deleting.

### Note format: written for the retriever

octobrain chunks at every heading (the heading path travels with each chunk) and retrieval is hybrid: semantic search plus regex match. Every rule below serves one of the two.

- One durable topic per file, atomic claims at the section level. Filename is a kebab-case declarative slug (`session-tokens-rotate-daily.md`), no dates; only decisions/ carries the sequential `adr-NNNN-` prefix. Slugs and headings are citation anchors: pick once, never rename; status changes happen inside the file.
- H1 is a declarative claim (the note's thesis), not a label: "Session tokens rotate daily", never "Tokens".
- Line 2 is the meta line, regex-friendly key=value tokens: `Meta: type=decision status=active updated=2026-07-22 source=user-confirmed review=2027-01-01`. type is decision, reference, guide or term. status is active or superseded. source is user-confirmed, a url, or inferred. review appears only for expiring facts.
- Then the lead: 1 to 3 sentences stating the full claim, self-contained. Title, meta and lead form the top chunk, the note's best retrieval surface.
- Each `##` section is retrieved alone: self-contained, about 150 to 350 words, split past about 500. Use a declarative heading stating the claim ("Refresh flow re-issues both tokens", never "Details"): the stored heading path is each chunk's context, so a descriptive heading is free contextual retrieval. Repeat the subject noun; no pronouns or "as above" pointing across sections. Keep code blocks and tables whole.
- Serve both search modes in the same sentence: the exact literal in backticks and its plain description, as in "`SESSION_TTL` (session expiry timeout) defaults to 24h".
- Decisions use Context, Decision and Consequences (good and bad) sections. Guides use numbered steps under declarative section headings. Glossary: each `##` is the canonical term; the body defines it and names forbidden synonyms.
- End multi-note topics with `Related:` and relative markdown links (`[session store](../reference/session-store.md)`), never wikilinks.

### Lifecycle

- Corrections and drift: update the note in place; git history is the archive.
- Reversed decision: write a new `adr-NNNN` with a `Supersedes:` link; flip the old one to `status=superseded` plus `Superseded-by:`. An accepted decision's substance is never edited and its file never renamed, because rationale stays durable context.
- Wrong or harmful note: delete the file (deletion prunes it from the index) and update the README map.
- Keep the box small and high-signal: merge overlapping notes, keep one fact in exactly one place, keep the README map current, and verify relative links resolve on every write.

### Judgment calls

- Unsure whether something is durable: apply the durable test out loud in one line, then act on the verdict.
- The user insists on storing something that fails the test: store it, mark `source=inferred` absent confirmation, and note the volatility risk in one line.
- Two empty search rounds on a topic: stop and report the gap; don't thrash.

## Output format

- Reading: the answer or extracted data first, then `Sources:` with one `.box/` or indexed path per line. Not found: one line saying so plus the closest hits.
- Writing or promoting: one line on what changed; bullets for each note created, updated, superseded or deleted with its path; one line on facts rejected by the durable test and where they belong instead. No prose essays.

## Checklist

- [ ] Project-knowledge answers come only from indexed sources, the box, memory or the user's input, with a path cited for every extracted fact.
- [ ] Nothing was written outside `.box/`.
- [ ] Every write passed the four-part durable test and the dedup search.
- [ ] Every note has a declarative H1, a meta line and self-contained sections of about 150 to 350 words.
- [ ] The README map lists every note and relative links resolve.
