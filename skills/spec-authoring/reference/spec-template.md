# Spec output template

Copy this shape exactly. Omit any section with nothing real to say rather than
padding it. The last line is always the status sentinel.

One spec = one mergeable outcome. When saved, it lives at
`specs/<NNN>-<slug>/spec.md`, with `tasks.md` (and `design.md` when the work is
risky or unfamiliar) alongside it in the same folder. Split into sibling folders
when the Done commands differ, when a slice could ship on its own, or when
`tasks.md` passes ~10–15 items. For a large change, write a thin parent spec that
pins the interfaces, then one child folder per slice.

```markdown
# Specification: <name>

## Overview
<One paragraph: WHAT and WHY, zero context assumed, zero implementation.>

## Current Behavior *(changes to existing behavior only)*
<Verified current truth, file:line grounded.>

## User Stories *(features only)*
As a <role>, I want <capability>, so that <benefit>.

## Key Entities *(only when the data model changes)*
- <Entity> — <attributes, constraints, relationships; no storage or tech detail>

## Requirements
- FR-001 [ADDED|MODIFIED|REMOVED if brownfield]: <EARS statement>
- FR-002: <EARS statement>

## Behavior Scenarios
Scenario: <name> (FR-001)
- Given <precondition>
- When <action>
- Then <observable outcome>

## Error Handling
| Condition | System behavior | User-facing response | FR |
|-----------|-----------------|----------------------|----|

## Acceptance Criteria
- [ ] AC-1 (FR-001): <yes/no verifiable condition>

## Assumptions *(autonomous mode or "you decide" answers)*
- <assumption> — default applied and why

## Guardrails *(imperative boundaries only; omit empty lines)*
- Protected surfaces: never modify <public API, shipped migrations, generated code>
- Forbidden moves: <no new dependencies, no refactors beyond the diff>
- Hard constraints: <measurable budgets, compat rules, "reuse the util at file:line">
- Invariants: <what must stay true — ordering, idempotency, error-code stability>

## Out of Scope
- <excluded or deferred — implementers cannot infer boundaries from omission>

## Open Questions *(only if [NEEDS CLARIFICATION] markers remain)*
- <collected markers>

## Context
- `path/file.rs:42:67` — <one line: why this location matters>
<context>
path/file.rs:42:67
</context>

## Verification
- `<project's exact test/build command>` — proves AC-1, AC-3
- <manual check, only where no command can prove the AC>

SPEC STATUS: READY
```

## Section rules

- Context block: verified paths only, narrow ranges, max 10 entries, most relevant first; every path also listed above it with a one-line why. Downstream agents batch-read exactly these ranges.
- The status line is the last line, exactly `SPEC STATUS: READY` or `SPEC STATUS: NEEDS CLARIFICATION` — the latter iff any `[NEEDS CLARIFICATION]` marker remains. Orchestrators branch on it.
- Bug tasks: Overview becomes Problem Statement; add Reproduction Steps (numbered, expected vs actual) and Root Cause (verified file:line); scenarios describe the fixed behavior plus regression invariants; omit User Stories.
- Refactor/performance tasks: add Current State and Target State (file:line grounded); scenarios become Behavior Invariants (what must not change); add Risks & Rollback; omit User Stories.
- Brownfield behavior change: state verified current truth in Current Behavior and tag each requirement ADDED / MODIFIED / REMOVED.
- When saved to `specs/<NNN>-<slug>/spec.md`, append a `## Clarifications` log (`- Q: … → A: …`) and edit the answers into the affected sections — the file, not the chat, is the record. Sibling `tasks.md` holds the independently verifiable steps; sibling `design.md` holds interfaces and decisions, and only for risky or unfamiliar work.