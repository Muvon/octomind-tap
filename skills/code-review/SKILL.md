---
name: code-review
title: "Code Review"
description: "Code review checklist and guidelines for giving and receiving constructive feedback on pull requests. Activate when reviewing a PR, preparing code for review, or establishing review standards."
license: Apache-2.0
compatibility: "Language-agnostic. Applicable to any software project using pull requests."
---

# Code Review Skill

## Overview

This skill provides a structured approach to code review: what to check, how to communicate feedback, and how to receive it. Activate it when reviewing a PR, preparing your own code for review, or establishing review norms for a team.

---

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
- [ ] Is complex logic explained with comments (the *why*, not the *what*)?
- [ ] Is the code easy to follow without needing to trace through many files?

#### Tests
- [ ] Are new behaviors covered by tests?
- [ ] Do tests test behavior, not implementation details?
- [ ] Are failure cases tested, not just the happy path?

#### Security
- [ ] Is user input validated and sanitized?
- [ ] Are secrets/credentials handled safely (not logged, not hardcoded)?
- [ ] Are permissions/authorization checks in place?

#### Performance
- [ ] Are there any obvious N+1 queries or unnecessary allocations in hot paths?
- [ ] Is caching used appropriately?

### Giving Feedback

**Be specific:** Point to the exact line and explain the concern.

**Distinguish severity:**
- `nit:` — minor style preference, take it or leave it
- `suggestion:` — improvement worth considering
- `question:` — genuinely unclear, needs explanation
- `issue:` — must be addressed before merge
- `blocker:` — serious correctness or security problem

**Be constructive:** Suggest an alternative, don't just say "this is wrong."

**Praise good work:** Acknowledge clever solutions or clean refactors.

### Receiving Feedback

- Don't take it personally — the review is about the code, not you
- Ask for clarification if a comment is unclear
- Respond to every comment (resolve, fix, or explain why you disagree)
- If you disagree, explain your reasoning — the reviewer may have missed context

### PR Size Guidelines

- **Ideal:** < 400 lines changed
- **Acceptable:** 400–800 lines (with good description)
- **Needs splitting:** > 800 lines — break into smaller PRs

Large PRs get shallow reviews. Smaller PRs get better feedback faster.

---

## Examples

### Good feedback comment

```
issue: This function panics on empty input (line 42). The `unwrap()` on
`items.first()` will crash if the slice is empty. Consider returning
`Option<T>` or checking `items.is_empty()` first.
```

### Bad feedback comment → fix it

```
# Bad
This is wrong.
Why did you do it this way?

# Good
suggestion: Using a HashMap here would reduce lookup from O(n) to O(1).
Since this runs on every request, it may be worth the extra memory.
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

---

## References

- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [Conventional Comments](https://conventionalcomments.org/)
