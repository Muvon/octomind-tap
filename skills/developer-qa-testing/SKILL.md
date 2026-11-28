---
name: developer-qa-testing
title: "Test Plan: Risk-Based QA Planning and Bug Reports"
description: "Design risk-based test plans and cases, diagnose flaky tests, write precise bug reports and release verdicts. Use for QA strategy rather than test code."
license: Apache-2.0
compatibility: "Requires a project with a runnable test command for execution; otherwise delivers a manual plan."
capabilities: versioning devdocs
domains: developer
rules:
  - match((?i)\b(test plan|test strategy|exploratory test\w*|regression[- ]suite|release[- ]readiness|automation strategy)\b)
  - match((?i)\b(write|file|draft|document)\b.{0,30}\b(bug report|defect record|defect)\b|\bbug report\b)
  - match((?i)\bflaky\b.{0,30}\btests?\b|\btests?\b.{0,30}\bflak(y|iness)\b)
  - match((?i)\b(can|should) we ship\b|\b(is it|are we) ready (to ship|for release)\b|\btell me honestly if it.s ready\b)
  - match((?i)\b(unit|integration|contract)\b.{0,40}\b(end-to-end|e2e)\b.{0,60}\b(split|level|decide|belongs?)\b)
  - match((?i)\b(edge cases?|test cases?)\b.{0,40}\b(read|list|find|each|by reading)\b)
  - match((?i)\b(reproduce|repro)\b.{0,40}\b(write (it )?up|report|defect|bug)\b)
  - semantic(what should we test and what should we automate for this feature, 0.72)
  - semantic(write a test plan with risk based cases for this release, 0.72)
  - semantic(why is this test flaky and how do we stabilize it, 0.72)
  - semantic(write a clear bug report with steps and expected result, 0.72)
  - semantic(give me a release go or no-go verdict, 0.72)
---

## Overview

Design tests from risk, not from coverage vanity: what would hurt most if it broke, what is most likely to break, and the smallest set of cases that would catch it. Apply real test-design techniques (boundaries, equivalence classes, decision tables, state transitions), run tests through the shell where a runner exists, and write bug reports precise enough to fix without a follow-up question. Testing provides information about risk; it does not bless a release.

This work covers test plans and strategy, test-case design, edge-case discovery from reading the code, automation strategy (what to automate at which pyramid level), flaky-test diagnosis, regression-suite curation, exploratory-testing charters, bug reports, and release-readiness verdicts grounded in what was and was not tested.

It does not cover implementing the features under test or fixing the bugs found, writing UI or end-to-end test code (the `e2e-testing` skill holds the locator, auth-state and isolation mechanics), writing the test code itself (the `developer-test-implementation` skill), security penetration testing (cover functional abuse cases; exploitation is out of scope), performance and load work beyond smoke-level checks (the `performance-profiling` skill), or CI infrastructure.

## Rules

### Method

1. Understand the change. Read the code, the diff or the spec; map what it touches in one parallel block: file outline for module shape, then targeted reads of the risky regions; symbol search for named symbols; semantic code search for behavior; call-graph search for consumers and blast radius. Flag untestable-as-described requirements now, not at the end ("fast" is not testable; "p95 under 300ms" is).
2. Assess risk. Rank the surface by damage times likelihood: money paths, data loss, auth and irreversible actions first; cosmetic last. The plan allocates effort by this ranking, explicitly.
3. Design cases. Apply the techniques below to the risky surfaces; every case has preconditions, steps and an expected result. Include the negative and abuse cases developers skip: wrong types, empties, duplicates, concurrent submits, out-of-order operations, unicode, timezone and DST edges.
4. Execute what is runnable. Use the existing runner via shell, respecting the project's own commands from its config and docs; runner and framework API specifics come from the devdocs reference, not memory. Report results verbatim, failures with full output. No runner: deliver the manual execution plan.
5. Report. Bugs in the anatomy below; the release verdict states what was tested, what was not, and residual risk, never a bare "LGTM".
6. Persist. Write the project's test commands, conventions, flaky history and past escapes to memory; suites and plans to files.

Read code with outlines, file reads and code search; shell runs the project's own test and build commands only.

### Test-case design techniques (apply, don't recite)

- Equivalence partitioning: one representative per class of same-behavior inputs. Testing 5 values from one class is 4 wasted cases.
- Boundary values: at, just below and just above every limit (0, 1, max, max+1, empty, full). Off-by-one lives here; so do most escapes.
- Decision tables: for rule combinations (pricing, permissions, feature flags), enumerate, then prune impossible columns; combinatorial gaps hide in prose specs.
- State transitions: for anything with a lifecycle (orders, sessions, jobs), cover valid transitions, invalid ones attempted, and re-entry (what happens on retry, refresh, double-click).
- Pairwise: when full combinations explode, cover all value pairs; most interaction bugs involve two factors, not five.

### The pyramid, enforced economically

Many fast unit tests, fewer integration tests at the seams, few end-to-end tests on the money paths only. An inverted pyramid (end-to-end heavy) is slow, flaky and pinpoints nothing. Between services you do not deploy together, a consumer-driven contract test beats a shared end-to-end environment. Automate what is stable and repeated; exploratory testing stays human and charter-driven. Automating a UI that changes weekly is writing flaky tests on purpose.

### Accessibility is functional

Any UI change gets an accessibility pass: keyboard-only operation and visible focus, accessible names for controls, contrast, target size, error messages tied to their fields. Target WCAG 2.2 AA (the EU Accessibility Act, enforced since June 2025, legally references EN 301 549, which maps to WCAG 2.1 AA). Automated scanners catch only part of the issues, so pair them with a keyboard and screen-reader walk of the risky flows.

### Flaky tests: quarantine, then fix the cause

A flaky test is a bug in the test system, not noise. Quarantine it out of the gate the same day (a red gate people override is no gate), then root-cause it: timing and awaits, shared state between tests, order dependence, real network or clock dependence, or a genuine race in the product (the valuable kind: that one is a product bug). Retry-until-green destroys evidence. Every quarantined test gets an owner and an exit date. To diagnose, reproduce with repeat runs via shell, classify the cause, and propose the real fix, never a retry wrapper.

### Bug report anatomy

Title is symptom plus condition ("Checkout total drops discount when coupon applied after address change"), not "checkout broken". Body: environment and build, minimal repro steps (numbered, from a clean state), expected versus actual (verbatim output or screenshot), scope probe (what else it affects, what it does not), severity by user impact. One bug per report; a repro the developer can run beats ten paragraphs.

### Release verdicts

State what was tested (what, how), what was not tested (and why), bugs open by severity, and residual risk in one honest paragraph. A "ship" recommendation names the risk being accepted. You provide the information; the owner makes the call.

### Situations

- "Test this feature or diff": read code, rank risk, design cases, run the runnable part, report.
- "What should we automate?": a pyramid-placed list with the economic reasoning per item.
- "Can we ship?": the honest verdict format, never a bare yes.
- Ambiguous: ask one question (usually "what breaks the business if it breaks?"), then proceed.

## Output format

- Test plans as `test-plan-<feature>.md`: risk ranking, cases grouped by technique, automation split, open questions.
- Executable tests are written in the project's existing framework and conventions (match style; no new frameworks uninvited).
- Bug reports in the anatomy above, one per bug.
- Run results: command, verbatim tail of output, pass/fail table.

## Checklist

- [ ] Every plan includes negative, boundary and concurrency cases; a happy-path-only plan is returned with the missing cases added.
- [ ] Nothing reported as tested that was not run or manually executed; the verdict lists tested and not tested explicitly.
- [ ] No flakiness masked with retries or sleeps; no assertion weakened to pass a suite.
- [ ] Failures reported verbatim with reproduction steps, severity by user impact, one bug per report.

## Composition / References

- `e2e-testing` for browser and mobile test mechanics; `developer-test-implementation` for writing the tests; `performance-profiling` for profiling and load design.
