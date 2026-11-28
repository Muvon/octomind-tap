---
name: developer-test-implementation
title: "Mutation Testing and Code Coverage: Writing Tests"
description: "Write behavior-proving tests in any language, close risk-ranked coverage gaps, set up mutation testing tooling, and prove each new test fails first."
license: Apache-2.0
compatibility: "Requires the project's own test runner; coverage and mutation tools are those of the project's language."
capabilities: versioning devdocs
domains: developer
rules:
  - match((?i)\b(write|add|implement|create)\b.{0,30}\b(unit|integration|property[- ]based|regression) tests?\b)
  - match((?i)\b(write|add)\b.{0,15}\btests (for|covering|around)\b)
  - match((?i)\b(improve|increase|raise|close|measure)\b.{0,25}\bcoverage\b|\bcoverage (gaps?|report)\b)
  - match((?i)\bmutation (testing|tests?|score|tool\w*)\b|\bsurvived mutants?\b)
  - semantic(add tests that verify this behavior and fail when it breaks, 0.72)
  - semantic(write unit tests for this function and cover the gaps, 0.72)
  - semantic(which parts of the code lack tests and how risky is that, 0.72)
  - semantic(set up mutation testing to check my tests are strong, 0.72)
---

## Overview

Write tests that verify behavior, not implementation, and treat coverage as a map of what is certainly untested, never as proof that anything is well tested. A test earns its place by failing when the behavior breaks; assertion quality and mutation resistance define a suite, percentages do not.

The skill covers unit, integration, property-based and UI or end-to-end tests (the `e2e-testing` skill holds the locator, auth-state, isolation and flake mechanics for browser and mobile); closing coverage gaps ranked by risk; setting up coverage and mutation tooling in the project's language; triaging survived mutants into missing assertions; test-double hygiene; diff-coverage gates for new code; and making legacy code testable enough to test.

It does not cover test strategy, plans, exploratory charters, bug reports or release verdicts (the `developer-qa-testing` skill decides what deserves testing; this one makes those tests exist and proves they bite), fixing the product bugs the tests expose, CI infrastructure, security penetration testing, or performance and load engineering beyond a regression benchmark (the `performance-profiling` skill).

## Rules

### Method

1. Map the target in one parallel block: file outline for module shape, then targeted reads; symbol search for symbols; semantic code search for behavior; call-graph search for consumers. Find the project's existing test framework, runner commands and coverage config. Those are the law: no new frameworks uninvited.
2. Measure. Run the suite with coverage via shell, in branch mode where the tool supports it. Read the report as a ranked list of untested behavior: money paths, auth, data loss and irreversible actions first; getters and glue last. Exclude generated and vendored code from metrics instead of writing junk tests for it.
3. Write tests: public API in, observable outcome out; one behavior per test; name states unit, scenario and expected result. Every risky function gets its boundaries (0, 1, max, max+1, empty, unicode) and its negative cases. Pure logic (parsers, formatters, serialization round-trips, math) gets a property-based test with the language's shrinking library alongside the example tests. Parsers and decoders fed untrusted bytes also get a fuzz target where the toolchain has one (Go native fuzzing, cargo-fuzz, Atheris, Jazzer).
4. Prove the tests. Every new test is observed failing before it counts: break the behavior (or run the mutation tool on the touched module) and confirm red, then restore and confirm green. A test never seen red proves nothing.
5. Report: coverage delta on touched code with verbatim runner output, survived mutants mapped to the assertions they expose as missing, and what remains untested with the reason.
6. Persist the runner, coverage and mutation commands, conventions and agreed thresholds to memory; tests go to the project's test tree.

Read code with outlines, file reads and code search; shell runs the project's own test, coverage and mutation commands only.

### Coverage discipline

- Coverage identifies untested code; it cannot certify tested code. High line coverage with weak assertions is the classic false green, which is what mutation testing exposes.
- Gate on diff coverage of changed lines, not the repo-wide total. Chasing a global number manufactures assertion-free tests; 70 to 85 percent overall is where mature suites live, and 100 percent usually marks vanity tests.
- Prefer branch coverage over line coverage for conditional logic: a covered line with an untested else-branch is an untested line.

### Toolchain by language

Defaults when the project has not chosen (a 2026 snapshot; confirm maintenance status and exact flags via devdocs, not memory).

| Language | Runner and coverage | Property-based | Mutation |
|---|---|---|---|
| Python | pytest + pytest-cov (branch=true) | Hypothesis | mutmut |
| JS/TS | vitest/jest + v8/istanbul | fast-check | StrykerJS |
| Rust | cargo nextest/test + cargo-llvm-cov | proptest | cargo-mutants |
| Go | go test -coverprofile (branch-blind: statements only) | rapid, native `go test -fuzz` | Gremlins |
| Java/Kotlin | JUnit 5 + JaCoCo | jqwik (maintenance mode) | PIT |
| C#/.NET | xUnit + Coverlet | FsCheck | Stryker.NET |
| Ruby | RSpec/Minitest + SimpleCov | prop_check | mutant |
| PHP | PHPUnit/Pest + PCOV | Eris | Infection |
| Swift | Swift Testing/XCTest + swift test --enable-code-coverage | swift-property-based | muter |

### Test doubles

- Mock only what you do not own: network, clock, randomness, filesystem, third-party APIs, behind your own thin wrapper, mocking the wrapper.
- Prefer fakes (working in-memory implementations) over interaction mocks. Mocking your own code couples tests to implementation and passes while production fails.
- A test that mocks every dependency is written at the wrong level: move up to an integration test with fakes.

### Mutation testing, economically

Run incrementally on changed files and critical modules with a score gate; whole-repo runs are nightly jobs at most. Each survived mutant is a missing or weak assertion: strengthen the test or, if the mutant is truly equivalent, record why.

### Situations

- "Cover this module" or "improve coverage": measure, risk-ranked gap list, tests for the top risks, delta report.
- "Get us to N% coverage": state once that a diff-coverage gate plus risk-ranked tests beats a global target, then execute what is decided.
- "Are our tests any good?": a mutation run on the chosen module, a survived-mutant report with fixes.
- "Test this new code or diff": behavior tests with boundaries and negatives; a property test where logic is pure.
- Ambiguous: ask one question (usually "which paths hurt most if broken?"), then proceed.

## Output format

Tests in the project's existing framework, style, naming and directory layout. Coverage report: a per-file before and after table (line and branch) for touched code, the runner command, and the verbatim output tail. Mutant triage as `mutant → surviving because → fix`. Tooling setup as minimal config diffs in the project's own config files.

## Checklist

- [ ] Every new test observed failing (break-then-restore, or mutation) before it counted.
- [ ] No assertion weakened or deleted to hit a threshold; private internals not tested through export hacks (untestable code is flagged for refactor).
- [ ] Project's existing framework and conventions respected.
- [ ] Coverage and mutation results reported verbatim; what remains untested named in every report.

## Composition / References

- `developer-qa-testing` decides what to test; `e2e-testing` covers browser and mobile mechanics; `performance-profiling` covers benchmarks.
