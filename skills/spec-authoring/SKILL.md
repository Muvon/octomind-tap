---
name: spec-authoring
title: "Behavioral Spec Authoring"
description: "How to write a behavioral spec an autonomous agent can implement with zero unstated assumptions: EARS requirement patterns, the requirements/constraints/verification triple, wording discipline, the clarification protocol for interactive and autonomous runs, and the thin-spec file split. Activate when writing, revising, or reviewing a feature spec or acceptance criteria."
license: Apache-2.0
compatibility: "Language-agnostic. Needs a codebase to ground the spec in and filesystem/search access to verify every cited path."
domains: developer
rules:
  - match((?i)\b(write|draft|create|update|revise|produce|review)\b.{0,40}\bspec(ification)?\b)
  - match((?i)\bspec[- ]driven\b|\bacceptance criteria\b|\bEARS\b|\brequirements (doc|document|section)\b)
  - semantic(turn this request into testable requirements before coding)
  - semantic(write a spec for this feature)
---

## Overview

A spec is the contract between intent and code. An autonomous implementer follows it exactly — including its gaps: underspecified intent does not get corrected, it gets implemented. The spec's job is to make every requirement checkable, every boundary explicit, and every unresolved question visible rather than guessed.

Write a spec when the work is not describable in one sentence. Skip it when it is.

## Mental model

Three ingredients, three jobs. All three are required; none substitutes for another.

| Ingredient | Answers | Lives in |
|---|---|---|
| Requirements | What must be true when done | EARS statements, one per test |
| Constraints | What the implementer may not do | Guardrails: forbidden moves, protected surfaces, budgets |
| Verification | How done is proven | The exact command that must exit 0 |

Requirements without constraints let the implementer widen scope. Constraints without requirements produce a cautious no-op. Either without a verification command is unfalsifiable prose.

Two properties govern everything else.

- Depth scales with unfamiliarity. A variant of something already built needs three EARS lines and a command; a new subsystem needs a short design section first. Padding a familiar change with ceremony costs as much as under-specifying a novel one.
- The spec is thin and dies at merge. It is not a design document, a task list, or a store of decisions. Standing repo knowledge belongs elsewhere.

## Rules

### Requirements use EARS

Fixed clause order, `shall` as the only normative verb, one requirement per statement. The patterns cover the failure modes implementers actually produce — a spec written only in `When` clauses specifies the happy path and leaves error behavior to chance.

| Pattern | Template | Use for |
|---|---|---|
| Ubiquitous | The <system> shall <response> | Always-true properties, budgets, invariants |
| Event-driven | When <trigger>, the <system> shall <response> | User actions, API calls, the happy path |
| State-driven | While <state>, the <system> shall <response> | Behavior that holds as long as a condition does |
| Unwanted | If <trigger>, then the <system> shall <response> | Errors, invalid input, failures |
| Optional | Where <feature enabled>, the <system> shall <response> | Flags, optional components, per-tenant config |
| Complex | While <state>, when <trigger>, the <system> shall <response> | Precondition plus trigger |

`If/then` is reserved for unwanted behavior. Cover every happy path with an error path, every input with an empty/invalid/boundary case, every multi-actor flow with a concurrent case, every external dependency with an unavailable case.

### Wording discipline

- One requirement, one thought. Split on "and"/"or" — a compound statement is two untestable requirements.
- No pronouns. Repeat the noun so each statement stands alone.
- No vague terms: fast, robust, properly, gracefully, user-friendly, appropriate, some, several, many. Replace each with a number, threshold, or enumerated list. Give numeric ranges, never "many".
- One canonical term per concept. Never synonym-swap.
- Requirements state what the system shall do, never how. Code appears only as behavioral evidence: an input→output pair, a payload shape, an error body, a command with expected output.

### Traceability and verification

- Give every requirement a stable ID (FR-001…). Scenarios and acceptance criteria reference the FRs they cover; every FR is covered by at least one — an uncovered FR is a defect.
- Scenarios use literal values ("editor", "Enter a valid email"), never placeholders, so a tester can lift them into a test verbatim.
- Acceptance criteria are binary pass/fail, never "looks correct".
- Name the exact project command that proves the work: the test/build/lint invocation, mapped to the requirements it proves. A spec whose verification section says "test it" is not a spec.

### Constraints, not instructions

Guardrails carry what the implementer may not do — a boundary list, not a process description. Constraints outperform instructions: "no TODOs, no partial implementations" works; "remember to finish" does not.

- Protected surfaces: never modify <public API, shipped migrations, generated code>.
- Forbidden moves: no new dependencies, no refactors beyond the diff, no contract changes.
- Hard budgets: measurable numbers, not adjectives.
- Invariants: what must remain true after the change.
- A forbidden move that seems necessary is a stop-and-report, not a judgment call.

Never dictate process to a competent implementer. Specify outcomes and boundaries; the how is theirs.

### Clarification — interactive and autonomous

Scan the draft against the ambiguity taxonomy and mark each area Clear / Partial / Missing: functional scope · data model · interaction flow · non-functional qualities · integrations · edge cases and failure handling · constraints and tradeoffs · terminology · completion signals.

Interactive (a human is present):

- Ask only about Partial/Missing areas that materially change the spec — max 5 per round, numbered.
- Every question is multiple-choice with 2–4 lettered options and the recommended one marked, or answerable in ≤5 words. "1a, 2c, 3: admins only" must be a valid reply.
- Ground options in findings: "I see two patterns in the codebase: A or B?"
- Never ask what exploration already answered. Ask WHICH errors and HOW, not "handle errors?".
- Iterate rounds until no high-impact ambiguity remains.

Autonomous (no human can answer):

- Ask nothing. Apply the option you would have recommended and record every applied default under Assumptions — one line each, with the reason.
- Where no reasonable default exists, insert `[NEEDS CLARIFICATION: <specific question>]` inline at the exact spot. Never guess silently.
- Any remaining marker forces `SPEC STATUS: NEEDS CLARIFICATION`; orchestration routes those to the human.

An assumption is acceptable only when recorded and verifiable. A silent default is a defect.

### The file split

| Artifact | Scope | Lifetime |
|---|---|---|
| spec.md | One feature or change | Dies when merged |
| AGENTS.md | The repo: commands, conventions, env quirks | Standing, kept thin |
| tasks.md | Independently verifiable steps | While the work spans sittings |
| scratchpad.md | The agent's live working state | Rewritten, never appended |

The scratchpad is working memory held outside the context window: current state, what was learned, what remains. Rewrite it frequently instead of appending — an appended file becomes a log whose current state is buried under stale history. The test for any line in any of these files: would removing it cause a mistake? If not, cut it.

### Adapt by task type

- Bug — lead with Problem Statement (what breaks, who is affected), Reproduction Steps (numbered, expected vs actual), Root Cause (verified file:line); scenarios describe the fixed behavior plus regression invariants; omit user stories.
- Refactor / performance — add Current State and Target State grounded in file:line; scenarios become behavior invariants (what must not change); add risks and rollback.
- Brownfield behavior change — state the verified current truth, then tag each requirement ADDED / MODIFIED / REMOVED.
- Beyond ~30 requirements — split into independently verifiable milestones, each with its own acceptance criteria. One oversized spec degrades implementer recall.

## Examples

Requirement, vague → testable:

```text
❌ The system should handle uploads efficiently and robustly.
✅ FR-004: When a file larger than 10 MB is uploaded, the system shall
   reject the request with status 413 and body {"error":"file_too_large"}.
✅ FR-005: The system shall complete a 10 MB upload within 5 seconds at
   100 concurrent uploads.
```

Constraint, instruction → boundary:

```text
 Remember to keep the API stable and don't break anything.
✅ Guardrails:
   - Protected surface: the public JSON contract in api/v1/schema.rs — additive changes only.
   - Forbidden: no new dependencies, no renames outside the touched module.
   - Invariant: existing clients sending only `name` continue to succeed.
```

## Checklist

- [ ] Every requirement is one EARS statement, singular, with `shall` and no vague term?
- [ ] Happy path, error path, boundary, concurrency, and dependency-unavailable cases each covered?
- [ ] Every requirement has an ID and at least one scenario or acceptance criterion; every criterion is binary?
- [ ] Constraints are imperative boundaries (protected surfaces, forbidden moves, budgets, invariants) — not process instructions?
- [ ] The verification section names the exact command that must exit 0 and maps it to the requirements it proves?
- [ ] Every cited path was verified with tools?
- [ ] Interactive: ≤5 grounded, multiple-choice questions per round? Autonomous: every default recorded, no silent assumption?
- [ ] No `[NEEDS CLARIFICATION]` marker remains while the spec claims to be ready?
- [ ] Does every line change what gets built or how it is verified? Delete the lines that change neither.

## Composition / References

- EARS — Alistair Mavin, Rolls-Royce (2009): https://alistairmavin.com/ears/
- The closing status line is a machine-checked handoff sentinel; keep its spelling and position exact so orchestration can branch on it.