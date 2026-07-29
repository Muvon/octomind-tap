---
name: issue-diagnosis
title: "Issue Diagnosis"
description: "Method for resolving reported issues (bug reports, feature requests) the way a project maintainer would: understand the reported behavior, find the upstream resolution when one exists, survey the full surface the change belongs to, implement in the project's own pattern, and verify against the report. Activate when the task is a reported issue against a codebase."
license: Apache-2.0
compatibility: "Language-agnostic. Applies to any codebase; upstream research applies when the project has a public home."
domains: developer
rules:
  - match((?i)reported issue|bug report|issue tracker)
  - match((?i)###\s*(describe the bug|bug summary|problem|expected behavior|reproduction|actual outcome|proposed solution))
  - match((?i)resolve the .{0,20}issue)
---

# Issue Diagnosis

## Overview

A reported issue describes a symptom from the reporter's point of view; the merged resolution is usually broader than the report's literal words. This skill is the path from report to maintainer-grade resolution. It matters most when the issue looks trivial — one-sentence requests are where half-fixes ship.

## Instructions

### 1. Understand the reported behavior

- Restate what the reporter observed and what they expected. The gap between those two is the actual requirement — not the sentence in the title.
- The report's framing can be wrong or partial: a reporter's proposed solution describes their guess, not the project's design. Weigh it as one hypothesis.
- When the reported behavior can be observed directly, observing it before and after the change is the strongest evidence available that the change addresses the report — the symptom's absence alone is not; observe what the change actually produces.

### 2. Find the upstream resolution (public projects)

- Search the project's issue tracker and changelog for this report, linked discussion, or an existing fix.
- Resolve the chain in order: the issue page itself → the pull request linked as closing it → that pull request's actual diff. An issue number is not a PR number; never fetch a PR by the issue's number or trust an artifact not confirmed to match this issue.
- When upstream work exists, align with it exactly: names, signatures, parameter names, call conventions, which layer owns the change, and every file the upstream diff touches — an upstream-touched surface not visited is an unfinished step.
- Private code, or nothing public found: note that and continue; the rest of the method applies unchanged.

### 3. Survey the surface

- Map every surface the change belongs to: the abstraction that owns the behavior, each of its implementations, and every wrapper, facade, or sibling that proxies the same contract.
- Search for types holding a reference to (or inheriting from) the one being changed — each proxying layer mirrors a new public member. Search the new name repo-wide and reconcile every hit.

### 4. Implement in the project's own pattern

- A new member follows the pattern its class already uses: when every existing member delegates to an inner component, the new member delegates too — create the inner primitive it needs rather than inlining what the pattern delegates.
- A new parameter that makes an existing name ambiguous (a second kind of key/id/name in one signature) renames both so each says what it identifies.
- A thin delegate forwards its arguments positionally, as received; keywords only where the target demands them.
- Follow the project's conventions for a change of this kind — look at how comparable merged changes were shaped (annotations, changelog entries, docs).

### 5. Contain the blast radius

- Pick the narrowest fix point the reported scenario actually passes through.
- Changing a widely-shared helper's contract (error type, raise condition, return shape) to solve one caller's case is a blast-radius mistake: if the cause genuinely lives in the shared helper, enumerate its other callers and check them; otherwise guard at the reported path.
- Fix the cause, not the symptom: wrapping the failing operation to absorb its error, or special-casing the visible symptom while the producing logic stays unchanged, ships the bug hidden.

### 6. Verify against the report

- The bar is the reporter's expected behavior, produced and observed — not "no longer crashes" and not "my new code runs".
- Re-read the report at the end: every part of the reported gap addressed, at every surveyed surface.

## Pitfalls

- The trivial-looking request: a one-line feature ask that actually spans a layered surface (base + implementations + wrappers). Depth of delivery is not scope creep; the request names the capability, complete delivery of it is the request.
- Fetching upstream artifacts by the issue's number — the closing PR almost always has a different number.
- The band-aid: try/except (or equivalent) around the crash site with a fallback path. The crash disappears, the behavior remains wrong, and hidden control-flow bugs ride along.
- The over-general fix: patching the shared primitive every flow depends on, satisfying the reported case and quietly breaking others.
- Verifying with a search or a read: locating code proves nothing about behavior; only the reported scenario's actual outcome does.
