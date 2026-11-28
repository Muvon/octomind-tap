---
name: release-notes-writing
title: "Release Notes Writing"
description: "Write user-facing release notes from verified changes, with concrete outcomes and migration instructions for breaking changes."
license: Apache-2.0
compatibility: "Requires git and read access to the repository."
rules:
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut)\b.{0,60}\brelease[ -]+notes\b)
  - semantic(write release notes for the changes since the last release)
---

## Overview

Explain the impact of a release to users and operators who have no access to the diff. Write notes for a commit range or an explicitly supplied change set. For a standalone file update, get the starting ref and the target together; the end defaults to HEAD.

## Rules

- Resolve the range or read the supplied change set. Verify each public behavior at the intended end revision. Check the spelling of commands, flags, options and versions against the source.
- Lead with breaking changes and verified upgrade actions. State who is affected, what stops working, and what action restores their workflow. Flag missing migration evidence for maintainer review.
- Group verified changes by user-facing impact. Explain what changed and why it matters in plain language. Use project terminology and omit incidental refactors, internal churn and CI churn.
- Give a baseline, measurement and conditions for performance claims. Omit a quantified claim when the measurement is unavailable. Ground concrete names and behavior in evidence; omit unsupported claims.
- When updating a file, use the existing release format and register, check for duplicate release headings, prepend one new section at the top, and preserve prior releases.
- An empty user-facing range is reported without editing.

## Output format

Return the requested draft, or prepend one release section to the named target. Match the existing document's register.

## Checklist

- [ ] Public names and behaviors match the code.
- [ ] Each breaking change has a verified action or a flagged evidence gap.
- [ ] Notes, changelog and README use the same change decisions when drafted together.

## Composition / References

- `changelog-writing` maintains the canonical changelog for the same range.
