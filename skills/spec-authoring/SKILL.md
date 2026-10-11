---
name: spec-authoring
title: "Behavioral Spec Authoring"
description: "How to write a behavioral spec an autonomous agent can implement with zero unstated assumptions: EARS requirement patterns, the requirements/constraints/verification triple, proof forms (scenario, property, check), wording discipline, spec layering and split rules (repo/feature/task, parent-child), divergence-based clarification for interactive and autonomous runs, and the scratchpad rewrite discipline. Activate when writing, revising, or reviewing a feature spec or acceptance criteria."
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

Open `reference/spec-template.md` when emitting a spec: it holds the exact section order, the per-task-type section rules, and the save layout.

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
- Say each behavior once. A requirement states it, one proof pins it, and nothing restates it. A small change (≤3 requirements) fits in about 300 words; every extra line costs human review and dilutes what the implementer must hold.
- The spec is thin and dies at merge — one spec is one mergeable outcome: the thing you would review and ship as a whole. It is not a design document, a task list, or a store of decisions; standing repo knowledge belongs in AGENTS.md.

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

`If/then` is reserved for unwanted behavior, and its response carries the exact user-facing message or status — that is where error handling lives. For the inputs, flows, and dependencies the change touches, cover the happy path with an error path, each input with an empty/invalid/boundary case, each multi-actor flow with a concurrent case, each external dependency with an unavailable case. Don't invent corner cases the change can't reach.

### Wording discipline

- One requirement, one thought. Split on "and"/"or" — a compound statement is two untestable requirements.
- No pronouns. Repeat the noun so each statement stands alone.
- No vague terms: fast, robust, properly, gracefully, user-friendly, appropriate, some, several, many. Replace each with a number, threshold, or enumerated list. Give numeric ranges, never "many".
- One canonical term per concept. Never synonym-swap.
- Requirements state what the system shall do, never how. Code appears only as behavioral evidence: an input→output pair, a payload shape, an error body, a command with expected output.

### Acceptance and verification

Every requirement is proven at least once in Acceptance, by the lightest form that pins it, and stated nowhere else. Restating one behavior as a scenario, an error-table row, and a criterion triples review cost and tells the implementer nothing new.

| Form | Shape | Use for |
|---|---|---|
| Scenario | Scenario (FR-001): Given <literal state>, when <action>, then <observable outcome>. | One concrete flow, with literal values a tester lifts verbatim |
| Property | Property (FR-002): For any <input class>, <relation that holds>. | A rule over a whole input space: validation, transforms, ordering, idempotency, round-trips, permissions, refactor equivalence |
| Check | Check (FR-003): <binary condition> | Budgets and non-functional qualities the forms above can't express |

- Prefer a property wherever a rule covers many inputs: one line replaces a list of examples, and the implementer can generate tests from it.
- Give every requirement a stable ID (FR-001…). An FR with no proof is a defect; the validator rejects it.
- Scenarios use literal values ("editor", "Enter a valid email"), never placeholders.
- Every proof is binary pass/fail and rejects a plausible wrong implementation. If a stub, a hard-coded happy path, or an off-by-one build would pass it, sharpen it.
- Name the exact project command that proves the work, mapped to the FRs it proves. A spec whose verification section says "test it" is not a spec.

### Constraints, not instructions

Guardrails carry what the implementer may not do — a boundary list, not a process description. Constraints outperform instructions: "no TODOs, no partial implementations" works; "remember to finish" does not.

- Protected surfaces: never modify <public API, shipped migrations, generated code>.
- Forbidden moves: no new dependencies, no refactors beyond the diff, no contract changes.
- Hard budgets: measurable numbers, not adjectives.
- Invariants: what must remain true after the change.
- A forbidden move that seems necessary is a stop-and-report, not a judgment call.

Never dictate process to a competent implementer. Specify outcomes and boundaries; the how is theirs.

### Clarification — interactive and autonomous

Find ambiguity by divergence, not self-rating — agents reliably overrate how well-specified a task is. For each area of the ambiguity taxonomy (functional scope · data model · interaction flow · non-functional qualities · integrations · edge cases and failure handling · constraints and tradeoffs · terminology · completion signals), sketch the two most plausible readings a competent implementer could take. Same observable behavior: Clear. Different observable behavior: a divergence to resolve. Rank divergences by impact — scope, then security, privacy, and data integrity, then user-visible behavior, then technical detail.

Interactive (a human is present):

- Ask only about divergences that materially change the spec, highest impact first — max 5 per round, numbered.
- Every question is multiple-choice with 2–4 lettered options and the recommended one marked, or answerable in ≤5 words. "1a, 2c, 3: admins only" must be a valid reply.
- Ground options in findings: "I see two patterns in the codebase: A or B?"
- Never ask what exploration already answered. Ask WHICH errors and HOW, not "handle errors?".
- Iterate rounds until no high-impact ambiguity remains.

Autonomous (no human can answer):

- Ask nothing. Apply the option you would have recommended and record every applied default under Assumptions — one line each, with the reason.
- Where no default is safe, insert `[NEEDS CLARIFICATION: <specific question>]` inline at the exact spot. Reserve markers for scope, security, privacy, and data-integrity divergences; lower-impact ones always get a recorded default. Never guess silently.
- Any remaining marker forces `SPEC STATUS: NEEDS CLARIFICATION`; orchestration routes those to the human.

An assumption is acceptable only when recorded and verifiable. A silent default is a defect.

### Layers: one spec, one reviewable outcome

Three layers, three scopes. A spec never lives at the repo layer, and a task never becomes its own spec.

| Layer | Artifact | Holds | Lifetime |
|---|---|---|---|
| Repo | AGENTS.md | Only what is true for every task: build and test commands, conventions, migration rules, env quirks | Written once, pruned rarely |
| Feature | `specs/<NNN>-<slug>/spec.md` | One mergeable outcome — requirements, constraints, Done command | Dies at merge |
| Feature, risky only | `specs/<NNN>-<slug>/design.md` | Interfaces, data flow, key decisions — short | Dies at merge |
| Execution | `specs/<NNN>-<slug>/tasks.md` | Independently verifiable steps, dependencies marked | Rewritten as the agent learns |
| Working memory | `scratchpad.md` | The agent's live state: current position, what was learned, what remains | Rewritten, never appended |

Per-feature content never goes in AGENTS.md: it rots and inflates context for every unrelated task. And tasks.md is not a spec — a spec per task over-splits, each task-agent optimises locally, and seams appear between them.

The scratchpad is working memory held outside the context window. Rewrite it frequently instead of appending — an appended file becomes a log whose current state is buried under stale history. The test for any line in any of these files: would removing it cause a mistake? If not, cut it.

### Split or keep one spec

The boundary is one review sitting = one spec = one verified outcome. Review capacity is the scarcest resource in the loop, so aim the spec at the shape that spends it best.

Split when any of these fires:

- Different Done commands. The verification boundary is the spec boundary — a slice proven by tests and a slice needing a migration dry-run cannot share one converge loop.
- Independently shippable. If slice A could merge without B, A is its own outcome.
- Different risk profiles. Split so the risky slice gets the gated treatment (design.md, adversarial review) while routine slices stay thin. Depth follows risk and unfamiliarity, not size.
- tasks.md past ~10–15 items, or a spec you would dread rereading in a week. It will go stale before it converges.

Don't split when the parts only make sense merged (one coherent behavior), share one test suite, or nobody would ever review them apart. That is one spec with a longer tasks.md.

For a genuinely big change, use parent/child instead of one monolith:

- Parent, thin (~30 lines): goal, non-goals, architecture decisions, and the interface contracts between slices. No EARS — the children own behavior.
- Children, one folder each: their own EARS, constraints, and Done command.

Write the parent first and pin the interfaces. Only then can the children run in parallel without silently drifting on shared assumptions. Both failure modes are symmetrical: a monolithic spec goes stale and has nothing stable to converge against, while spec-per-task fragments intent until every agent is locally optimal and globally wrong.

### Adapt by task type

- Bug — lead with Problem Statement (what breaks, who is affected), Reproduction Steps (numbered, expected vs actual), Root Cause (verified file:line); Acceptance proves the fixed behavior plus regression invariants; omit user stories.
- Refactor / performance — add Current State and Target State grounded in file:line; Acceptance holds behavior invariants (what must not change), usually as properties ("for any input, the output equals the pre-change output"); add risks and rollback.
- Brownfield behavior change — state the verified current truth, then tag each requirement ADDED / MODIFIED / REMOVED.
- Beyond ~30 requirements, or a tasks.md past ~10–15 items — apply the split rules above instead of growing one file.

## Examples

Requirement, vague → testable:

```text
❌ The system should handle uploads efficiently and robustly.
✅ FR-004: When a file larger than 10 MB is uploaded, the system shall
   reject the request with status 413 and body {"error":"file_too_large"}.
✅ FR-005: The system shall complete a 10 MB upload within 5 seconds at
   100 concurrent uploads.
```

Many examples → one property:

```text
❌ Scenario: "Ann" is accepted. Scenario: "" is rejected. Scenario: an 81-char name is rejected.
✅ FR-002: If a display name is outside 1–80 characters, then the system shall
   reject it with "Name must be 1–80 characters".
   Property (FR-002): For any string s, the system accepts s as a display name
   iff 1 ≤ length(s) ≤ 80.
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

- [ ] One review sitting = one spec = one verified outcome? Split rules applied (Done commands, shippability, risk, tasks.md size) — or deliberately not, because the parts share one behavior and one test suite?
- [ ] Is this a parent with thin children (interfaces pinned first) rather than one monolith?
- [ ] Per-feature content kept out of AGENTS.md; tasks.md lives inside the spec folder; scratchpad rewritten, not appended?
- [ ] Every requirement is one EARS statement, singular, with `shall` and no vague term?
- [ ] Happy, error, boundary, concurrency, and dependency-unavailable cases covered where the change touches them — and no invented ones?
- [ ] Every requirement has an ID and the one proof it needs (scenario, property, or check), with no behavior stated twice? Every proof binary and able to reject a plausible wrong implementation?
- [ ] Constraints are imperative boundaries (protected surfaces, forbidden moves, budgets, invariants) — not process instructions?
- [ ] The verification section names the exact command that must exit 0 and maps it to the requirements it proves?
- [ ] Every cited path was verified with tools?
- [ ] Ambiguity found by divergence (two plausible readings with different observable behavior) and ranked by impact, not by self-rating?
- [ ] Interactive: ≤5 grounded, multiple-choice questions per round? Autonomous: every default recorded, no silent assumption?
- [ ] No `[NEEDS CLARIFICATION]` marker remains while the spec claims to be ready?
- [ ] Does every line change what gets built or how it is verified? Delete the lines that change neither.

## Composition / References

- `reference/spec-template.md` — output skeleton, section rules by task type, folder layout when saved.
- EARS — Alistair Mavin, Rolls-Royce (2009): https://alistairmavin.com/ears/
- ClarifyGPT — ask only where plausible readings diverge: https://arxiv.org/abs/2310.10996
- Ambig-SWE — agents miss underspecification unless they probe for it: https://arxiv.org/abs/2502.13069
- nl2postcond — postconditions written from intent catch real bugs: https://arxiv.org/abs/2310.01831
- The closing status line is a machine-checked handoff sentinel; keep its spelling and position exact so orchestration can branch on it.