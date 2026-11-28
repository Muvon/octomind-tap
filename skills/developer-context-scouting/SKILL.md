---
name: developer-context-scouting
title: "Context Scouting: Task Plus File References"
description: "Map a codebase for a raw task and return the same task with verified file:line entry points. Use to scout before a large change, without editing."
license: Apache-2.0
compatibility: "Requires read access to the repository; memory and knowledge lookups use the configured stores."
domains: developer
rules:
  - match((?i)\bexplore the codebase and return\b)
  - match((?i)\b(entry points?|file references?|verified references?|<context>|context block|file:line)\b)
  - match((?i)\b(ground|refine|curate|enrich|narrow)\b.{0,40}\b(task|ticket|request)\b)
  - match((?i)\b(trace|locate|find|map)\b.{0,40}\b(code paths?|entry points?)\b)
  - match((?i)\b(return|restate|hand)\w*\b.{0,40}\b(task|ticket)\b.{0,50}\b(references?|locations?|pointers)\b)
  - semantic(find the entry points in the codebase for this task and return file references, 0.72)
  - semantic(return this task with verified file references, 0.72)
  - semantic(map the code for this task and list where to start, 0.72)
  - semantic(scout the repo before a large change without editing anything, 0.72)
---

## Overview

Take a raw task, explore the codebase, and return a refined version of the same task with precise, verified file entry points. The result is context for whoever implements next. This is read-only work: no code, no implementation approaches, no requirements the user did not state. Preserve the user's original intent, structured and concise, with file references.

The skill does not write or edit code, propose architecture, add requirements, or interview the user. It grounds the task; it does not reshape it.

## Mental model

Zero hallucination is the core principle. One invented path wastes an entire downstream session. Every path you output was confirmed to exist with a tool. Every statement in the refined task traces to the user's own words (reworded for clarity, never for content) or to a fact you confirmed (a file exists, a signature, a memory recall). A gap is flagged inline, never filled with a guess.

## Rules

### Phase 1: explore (autonomous, all parallel, one tool block)

Run these together:
- memory recall: multi-term queries about the task domain, past decisions, patterns. Always in the first block.
- knowledge lookup: the project knowledge base for recorded decisions, conventions, domain terms.
- semantic code search: descriptive queries about the functionality the task touches.
- directory listing: project structure and config files.
- file outline: on files that look relevant from search results.
- call-graph search: component relationships.

Read further as needed. Search and outlines reveal key files; read targeted ranges to find exact entry points. A task that names specific features gets a symbol search for those symbols, types and functions. Narrow progressively: directory, file, function, line range.

Goal: the minimal set of files (at most 10) a developer needs open to start working.

### Phase 2: resolve ambiguity (never block on the user)

You gather context on request; you do not interview.
- Ambiguity you can settle from the code: settle it (the established pattern, the obvious owner, the single matching module).
- An entry point you cannot settle: include the most likely candidates and mark it inline in Entry Points as `# UNRESOLVED: <what's ambiguous>`. The implementer decides.
- Do not stop to ask. A best-effort context with a flagged unknown beats a stalled run.

### Phase 3: output

Produce the refined task in this exact format:

```
### Task
<The user's original task, reworded for clarity and structure. Preserve intent exactly. Number the steps only if the task naturally has several parts. Do not decompose a single task into artificial steps.>

### Entry Points
<For each relevant file, one line on why it matters for the task>

- `path/to/file.ext:NN:MM` — <what's here and why it's relevant>
- `path/to/other.ext:NN:MM` — <what's here and why it's relevant>

<context>
path/to/file.ext:NN:MM
path/to/other.ext:NN:MM
</context>
```

### File references

- Use `filepath:start_line:end_line` inside the context block (1-indexed, inclusive).
- Prefer narrow ranges (the function, struct or block) over whole files. Small files (under 50 lines) and config files use the full range (1:N).
- At most 10 references per context block. Order by relevance, most important first.
- Every path inside the context block also appears in Entry Points with its explanation.

### Task refinement

- Preserve the user's intent verbatim; restructure, don't rewrite.
- Remove ambiguity by grounding in codebase facts ("the X module at path/to/x.rs").
- If the user references something that does not exist, say so explicitly.
- Do not remove anything the user asked for, even if you think it is wrong.

### Reading efficiently

- Uncertain about a file: outline it first. Small file (under 200 lines) with known structure: read it whole. Large file: outline, then targeted ranges.
- Finding code: symbol search or semantic code search first; it may avoid reading entirely.
- Independent operations go in one parallel block; go sequential only when one result feeds the next.
- Stop once entry points are found, or ambiguity is resolved or flagged. After the output, do not summarize what you did; the output is the deliverable.

### Leave out

No implementation plan or approach, architecture analysis, risk assessment, "considerations" or "notes" section, suggestions beyond what was asked, test strategy, or timeline. No sections beyond Task and Entry Points. No code snippets.

## Checklist

- [ ] Every path confirmed to exist with a tool.
- [ ] No requirement added that the user did not state.
- [ ] At most 10 references in the context block, each also explained in Entry Points.
- [ ] Unsettled entry points flagged `# UNRESOLVED`.
- [ ] Nothing after the deliverable.

## Composition / References

- `spec-authoring` turns a grounded task into a behavioral spec.
- `developer-implementation-planning` turns a grounded task or spec into a phased plan.
