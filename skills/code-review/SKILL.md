---
name: code-review
title: "Code Review Checklist for Pull Requests"
description: "Code review checklist and guidelines for giving and receiving constructive feedback on pull requests. Activate when reviewing a PR, preparing code for review, or establishing review standards."
license: Apache-2.0
compatibility: "Language-agnostic. Applicable to any software project using pull requests."
---

## Overview

This skill provides a structured approach to code review: what to check, how to communicate feedback, and how to receive it. Activate it when reviewing a PR, preparing your own code for review, or establishing review norms for a team.

## Instructions

### Reviewer Checklist

#### Correctness
- [ ] Does the code do what the PR description says?
- [ ] Are edge cases handled (empty input, null, overflow, concurrent access)?
- [ ] Are error paths handled and errors propagated correctly?
- [ ] Are there any obvious logic bugs or off-by-one errors?

#### Design
- [ ] Is the change the right approach, or is there a simpler solution?
- [ ] Does it follow existing patterns in the codebase?
- [ ] Is the scope appropriate — does it do one thing?
- [ ] Are new abstractions justified, or is this over-engineering?

#### Readability
- [ ] Are names clear and intention-revealing?
- [ ] Is complex logic explained with comments (the why, not the what)?
- [ ] Is the code easy to follow without needing to trace through many files?

#### Tests
- [ ] Are new behaviors covered by tests?
- [ ] Do tests test behavior, not implementation details?
- [ ] Are failure cases tested, not just the happy path?

#### Security
- [ ] Is untrusted input validated, and does it stay out of query/command/path/template sinks?
- [ ] Are secrets/credentials handled safely (not logged, not hardcoded)?
- [ ] Are permissions/authorization checks in place on every new entry point?
- [ ] Do error paths fail closed (deny on exception, no stack traces or internals in responses)?

#### Dependencies and supply chain
- [ ] Does every new package exist on its registry, under the exact intended name? AI-suggested names are sometimes hallucinated, and attackers register them (slopsquatting).
- [ ] Is it maintained, license-compatible, and pinned through the lockfile?
- [ ] Could a few lines of code, the stdlib, or an existing dependency replace it?

#### Performance
- [ ] Are there any obvious N+1 queries or unnecessary allocations in hot paths?
- [ ] Is caching used appropriately?

### Giving Feedback

Be specific: point to the exact line and explain the concern.

Label every comment with [Conventional Comments](https://conventionalcomments.org/): `<label> [decorations]: <subject>`, then optional discussion.
- Labels: `praise`, `nitpick`, `suggestion`, `issue`, `todo`, `question`, `thought`, `chore`, `note`
- Decorations: `(blocking)`, `(non-blocking)`, `(if-minor)` — e.g. `issue (blocking): …` for a must-fix, `nitpick (non-blocking): …` for taste

Be constructive: suggest an alternative, don't just say "this is wrong." Pair each `issue` with a concrete fix or a question.

Praise sincerely with `praise:` when something is genuinely good — one specific line, not filler.

Respond fast: acknowledge a review request within one business day, even if the full review comes later. Slow reviews push authors toward bigger, riskier PRs.

AI-written code gets the same bar as human code: verify that every API, flag, and config key it uses actually exists in the pinned version.

### Receiving Feedback

- Don't take it personally — the review is about the code, not you
- Ask for clarification if a comment is unclear
- Respond to every comment (resolve, fix, or explain why you disagree)
- If you disagree, explain your reasoning — the reviewer may have missed context

### PR Size Guidelines

Google's engineering practices: about 100 lines is usually a reasonable change, 1000 lines is usually too large, and spread matters — 200 lines in one file can be fine while the same 200 across 50 files is not. Split refactors from behavior changes, and stack dependent PRs instead of growing one.

Large PRs get shallow reviews. Smaller PRs get better feedback faster.

## Examples

### Good feedback comment

```
issue (blocking): This function panics on empty input (line 42). The
`unwrap()` on `items.first()` will crash if the slice is empty. Consider
returning `Option<T>` or checking `items.is_empty()` first.
```

### Bad feedback comment → fix it

```
# Bad
This is wrong.
Why did you do it this way?

# Good
suggestion (non-blocking): Using a HashMap here would reduce lookup from
O(n) to O(1). Since this runs on every request, it may be worth the memory.
```

### PR description template

```markdown
## What
Brief description of the change.

## Why
The problem this solves or the feature this adds.

## How
Key implementation decisions and trade-offs.

## Testing
How you verified this works.
```

## References

- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
- [Conventional Comments](https://conventionalcomments.org/)
