---
name: code-review-lenses
title: "Code Review Lenses & Adversarial Verification"
description: "The dimensions of a deep code review — correctness, security, concurrency, performance, design/maintainability, tests — what each lens hunts for, and the adversarial verification discipline that keeps a multi-reviewer pass from multiplying false positives. Consensus is not correctness; every finding must be refuted before it is trusted."
license: Apache-2.0
compatibility: "Requires read access to the code under review. Powers multi-lens parallel review plus an adversarial verify gate."
domains: developer
rules:
  - developer(review)
  - developer(code-review)
  - match(\b(deep|multi.?angle|thorough)\s+(code\s+)?review\b)
  - match(\breview\s+(this|the|my)\s+(branch|diff|change|PR|code)\b)
  - semantic(do a deep multi-angle review of this code)
  - semantic(review this branch for bugs security performance and design)
---

## Overview

A single reviewer sees a fraction of what is wrong. Reviewing across distinct lenses in parallel — each blind to the others — surfaces far more, because a security mindset and a concurrency mindset notice different things on the same lines. But breadth has a failure mode: independent reviewers make correlated mistakes, and more voices agreeing does not make a finding true. This skill defines the lenses and the verification discipline that turns a wide sweep into a precise, trustworthy review.

The core rule: consensus is not correctness. In studied multi-agent reviews, dozens of agents have unanimously endorsed a vulnerability that did not exist, and independent agents have made identical errors. So a finding is a hypothesis until it survives an attempt to refute it against the actual code.

## Instructions

### Review beyond the diff

Real defects live in the interaction between changed lines and the code around them. For any change, open the callers, the tests, the config, and the data it touches — a changed function can be correct in isolation and wrong for how it is actually called. Use code search (semantic, structural, graph) to follow those edges; don't review the diff in a vacuum.

### The lenses

Run each as an independent perspective. A finding names which lens caught it.

- Correctness and edge cases — logic errors, off-by-one, null/empty/boundary inputs, error paths that swallow or mishandle failures, incorrect assumptions about state, wrong operator/comparison, missing return, unhandled result. Does it do what it claims, on the inputs it will actually see?
- Security — untrusted input reaching a sink (injection: SQL, command, path, template), missing authn/authz checks, secrets in code or logs, unsafe deserialization, SSRF, weak crypto, TOCTOU, missing validation/sanitization. Treat every input as hostile.
- Concurrency, error-handling and resources — race conditions, check-then-act, deadlocks and lock-ordering, shared mutable state across threads/async, unawaited futures, resource leaks (handles, connections, memory), missing cleanup on the error path, cancellation and timeout handling. These are the highest-cost, lowest-visibility bugs.
- Performance and efficiency — algorithmic complexity on hot paths, N+1 queries, unbounded allocations or growth, repeated work that could be hoisted or cached, blocking calls in async contexts, unnecessary copies. Flag only where it plausibly matters, with the reason.
- Design, maintainability and tests — SOLID and coupling, leaky or missing abstractions, API and contract clarity, over-engineering (speculative flexibility) as much as under-engineering, dead code, naming that misleads, and whether the change is actually tested: coverage of the new behavior and the edge cases, meaningful assertions, testability.

### Severity

- Blocking — a real bug, security hole, data-loss risk, or contract break that should not ship. Fix before merge.
- Recommended — a genuine improvement that should happen but doesn't block (a missing test for a real edge case, a design issue, a real-but-minor performance cost).
- Nit — style, naming, polish. Optional.

Default severity UP when unsure for correctness/security; default DOWN for taste. Never inflate a Nit into a Blocking to seem thorough.

### Adversarial verification — the precision gate

After the wide sweep, every candidate finding is verified independently, and the verifier's job is to REFUTE it, not to re-confirm it. For each finding:

1. Open the anchored file and line and read the actual current code — do not trust the finding's own reasoning or wording.
2. Trace the claim: follow the callers, the guards, the tests. Is the problematic path actually reachable with real inputs? Is there already a check that prevents it?
3. Decide KEEP only if the defect is provably anchored in the code as it is now. DROP if it is speculative, already handled elsewhere, a duplicate of another finding, a misreading, or true only under inputs that cannot occur. When genuinely uncertain after tracing, drop it — a false positive costs reviewer trust and wastes author time.
4. Dedup across lenses: the same underlying issue found by two lenses is one finding, attributed to both.

Independence matters: the verifier should reason from the code, not from the finder's confidence. Cross-model verification (a different model than the finders) catches complementary blind spots and is worth using when available.

### Finding format

Every kept finding, so the report is scannable and actionable:

```
[SEVERITY] [LENS] one-line title
  Where: path/to/file.ext:line
  Problem: the concrete defect, and the input/state that triggers it
  Why it matters: the consequence (bug, breach, leak, break)
  Fix: the concrete change
```

### The verdict

Compute it mechanically from the kept findings: any Blocking kept finding means the change needs work; otherwise it is approvable with the Recommended/Nit items as follow-ups. State the verdict as a decision, not a vibe.

## Examples

Sweep finding (candidate, high recall): "[Blocking][concurrency] cache write is not synchronized — file.rs:88".

Verified KEEP: opened file.rs:88, the map is written from two async tasks with no lock and read on a third; reachable on concurrent requests. Real race. Keep, Blocking.

Verified DROP: opened it — the map is a per-request local, never shared across tasks; the "race" cannot occur. Drop as a misread of scope. (This is exactly the correlated false positive multi-agent review must catch — several reviewers can flag the same non-bug.)
