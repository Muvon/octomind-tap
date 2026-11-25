---
name: release-notes-writing
title: "Release Notes Writing"
description: "Write user-facing release notes from verified changes, with concrete outcomes and migration instructions for breaking changes."
license: Apache-2.0
domains: developer
rules:
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut)\b.{0,60}\brelease[ -]+notes\b)
---

## Overview

Explain the impact of a release to users and operators who have no access to the diff.

## Rules

- Resolve the range or read the supplied change set. Verify each public behavior at the intended end revision. Check the spelling of commands, flags, options, and versions against the source.
- Lead with breaking changes. State who is affected, what stops working, and what action restores their workflow. Flag missing migration evidence for maintainer review.
- Group related entries by user-facing impact. Explain what changed and why it matters in plain language. Use project terminology and omit incidental refactors or CI churn.
- Give a baseline, measurement, and conditions for performance claims. Omit a quantified claim when the measurement is unavailable.
- When updating a file, use the existing release format, add the new section at the top, and preserve prior releases.

## Checklist

- [ ] Public names and behaviors match the code.
- [ ] Each breaking change has a verified action or a flagged evidence gap.
- [ ] Notes, changelog, and README use the same change decisions when drafted together.
