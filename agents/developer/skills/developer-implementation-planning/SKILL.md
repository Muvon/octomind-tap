---
name: developer-implementation-planning
title: "Implementation Planning: Parallel Task Plans"
description: "Turn a spec or rough ask into a phased plan with disjoint file ownership, merge gates and spec coverage. Use before splitting work across workers."
license: Apache-2.0
compatibility: "Requires read access to the repository; shell is used to find the project's real build and test commands."
rules:
  - match((?i)\b(write|draft|create|produce|make|build|revise|update)\b.{0,30}\b(implementation|execution|delivery|phased|rollout|migration)?\s*plan\b)
  - match((?i)\b(break|split|decompose|turn|map)\b.{0,40}\b(into|out)\b.{0,30}\b(tasks|phases|parallel|streams|work streams)\b)
  - match((?i)\bparalleli[sz]\w*\b|\bparallel (streams|tasks|work|workers)\b|\bnon-overlapping\b)
  - match((?i)\b(file ownership|own(s|ership)? of files|coverage (matrix|table)|merge gates?|dependency-ordered)\b)
  - match((?i)\bplan\b.{0,60}\b(phases|streams|workers|checkpoints)\b)
  - semantic(turn this spec into a phased plan whose tasks can run in parallel, 0.72)
  - semantic(break this feature into tasks that separate workers can build at once, 0.72)
  - semantic(plan the order of work and merge checkpoints for this change, 0.72)
  - semantic(who owns which files in this multi-part implementation, 0.72)
---

## Overview

Convert a behavioral spec, or a one-line free-form ask, into an execution plan that can be fanned out to parallel workers and merged back into one coherent change. Think in dependency graphs and file ownership: what must happen first, what can run at the same time without two workers touching the same file, and what proves the result matches the spec.

The skill covers task decomposition, phase and dependency design, parallel stream assignment, file-ownership partitioning, contract-first sequencing, merge and validation gates, spec-to-task coverage, effort and risk calls, and plan revisions. It does not write the behavioral spec (requirements authoring), implement code, or review diffs.

Two modes:
- Interactive (default): a human is present; resolve ambiguity by asking.
- Autonomous: active when the task carries "AUTONOMOUS", "non-interactive", "use defaults" or "use your judgment". No questions; document defaults in Assumptions and mark irreducible gaps [NEEDS CLARIFICATION].

## Rules

### Phase 1: ground the plan

Run one parallel context block before planning: memory recall on the task domain and past decisions; knowledge lookup for recorded conventions; README, ARCHITECTURE, CONTRIBUTING and any spec file given; semantic code search on the functionality touched; file outline then narrow reads on the files a change will land in; call-graph search for component coupling; symbol search for named symbols; shell for the project's real build and test commands. Web search only for external standards.

Come out knowing which files exist and will change (verified path:line), the module boundaries that make parallelism safe, the exact verification commands, and whether the input is a complete spec or a rough ask.

### Phase 2: close the gaps

Score the input against: scope boundaries, target architecture and stack, data and contract shapes shared across tasks, integration points, non-functional budgets, migration and rollout, test strategy, done-criteria.
- Interactive: at most 5 numbered questions per round, each multiple-choice or answerable in 5 words or fewer, grounded in what you found ("the repo does A here and B there — which?"). Never ask what exploration already answered.
- Autonomous: apply the option you would have recommended and log it in Assumptions.

### Phase 3: decompose

1. List every unit of work the spec implies, then merge units smaller than a meaningful commit.
2. Cut phases on real dependency boundaries: a phase ends where later work needs its output. Contracts, schemas, types and shared interfaces go in the earliest phase so every later stream can code against a frozen shape.
3. Inside each phase, assign tasks to parallel streams. A task is [P] only if its owned file set is disjoint from every other [P] task in the phase.
4. Give every task an owns list (exact paths), a depends-on list (task IDs) and a verify line.
5. Add one merge gate per phase: integrate, run the project's commands, check the phase's exit criteria.
6. Map every spec requirement to at least one task. An uncovered requirement is a defect, as is a task tracing to no requirement.

### Phase 4: deliver

Emit the plan in the conversation. Write a file only when asked: `plans/<NNN>-<slug>.md`, next free number. Then memorize the decomposition decisions and the parallelism boundaries found.

### Parallelism safety

A task may carry [P] only if all hold: disjoint owned files; no dependency on an unfinished task; no shared mutable state (migrations, lockfiles, generated indexes, route tables, barrel exports); its contract inputs are already frozen. Shared-file work becomes one serialized task, or a phase-1 contract task plus per-stream additive files.

### Sizing

A task is one worker, one coherent change, roughly 1 to 4 hours or under about 10 files. Split anything larger on a file or behavior boundary; merge anything trivial into its neighbor.

| Phase count | Use when |
|---|---|
| 1 | Single behavior change, no shared contract |
| 2 to 3 | Typical feature: contracts, implementation streams, integration |
| 4 to 6 | Migration, multi-surface, or rollout-gated work |
| more than 6 | Split into separate plans; one oversized plan degrades execution |

Each phase states an exit criterion that is checkable by command or by inspection, never "looks done".

### Risk and wording

- For each task that touches a protected surface (public API, migrations, generated code, auth) note the guardrail and the rollback. High-risk tasks never run [P] with anything.
- Every task line must be executable by a worker who sees only that line plus the spec: what to change, where, against which contract, and how it is verified.
- Estimates are relative (S, M, L) unless the user asks for time.

### Situations

- Free-form one-liner: explore, then clarify; do not silently invent a spec.
- Full spec attached: skip straight to gap-scoring and ask only about decomposition-relevant gaps.
- "you decide": apply your recommended option and record it in Assumptions.
- "save it" or "write the plan": write `plans/<NNN>-<slug>.md` and report the path.
- Revision request: update the affected phases and the coverage table, re-emit the status line.
- Autonomous: no questions, one pass, stop after the status line.

## Examples

- ❌ "T-004 [P]: update the API layer" → ✅ "T-004 [P] (stream B): add POST /sessions handler per contract in T-001. owns: src/api/sessions.rs. depends-on: T-001. verify: cargo test api::sessions"
- ❌ Two [P] tasks both editing src/routes.rs → ✅ T-002 registers all new routes once, after both stream tasks land.
- ❌ "Phase 2 done when the feature works" → ✅ "Phase 2 exit: `pnpm test` green and FR-003, FR-004 scenarios pass."

## Output format

````markdown
# Plan: <name>

## Objective
<One paragraph: what ships and why. Zero context assumed.>

## Inputs
- Source: <spec file / pasted spec / free-form ask>
- Verified context: `path/file.rs:42:67` — <why it matters>

## Assumptions
- <assumption> — default applied and why

## Approach
<3-8 lines: the shape of the solution and the decomposition rationale — why these phases, where the parallel seams are.>

## Execution Graph
```
Phase 1 ──► Phase 2 ─┬─ stream A ─┐
                     └─ stream B ─┴─► merge ──► Phase 3
```

## Phase <n> — <name>
Goal: <one line>  ·  Exit: <checkable criterion>

| ID | P | Stream | Task | Owns | Depends | Size | Verify |
|----|---|--------|------|------|---------|------|--------|
| T-001 | | — | <imperative task> | `path` | — | M | `<command>` |
| T-002 | [P] | A | … | `path` | T-001 | S | `<command>` |

Merge gate: <integration step + commands to run>

## Coverage
| Requirement | Tasks |
|-------------|-------|
| FR-001 | T-002, T-005 |

## Risks
| Risk | Task | Mitigation / rollback |
|------|------|-----------------------|

## Guardrails
- Protected surfaces: <never modify …>
- Forbidden moves: <no new deps, no refactors beyond the diff, …>

## Out of Scope
- <excluded or deferred>

## Validation
- `<exact project command>` — proves <requirements>
- Final acceptance: <how the merged result is checked against the spec>

## Open Questions (only if markers remain)
- <collected [NEEDS CLARIFICATION] markers>

PLAN STATUS: READY
````

The last line is always exactly `PLAN STATUS: READY` or `PLAN STATUS: NEEDS CLARIFICATION`; the latter if and only if a [NEEDS CLARIFICATION] marker remains. Orchestrators branch on this line.

## Checklist

- [ ] No task marked [P] that shares an owned file, a migration, or an unfrozen contract with another parallel task.
- [ ] Every cited path verified with tools.
- [ ] Every spec requirement covered; every task traces to a requirement.
- [ ] Every task has an owns list, a depends-on list and a verify line.
- [ ] No implementation code or algorithms; tasks describe what and where, not how.
- [ ] The plan ends with the PLAN STATUS line, READY only when no marker remains.

## Composition / References

- `spec-authoring` writes the behavioral spec this plan consumes.
- `developer-context-scouting` produces the file map used in phase 1.
