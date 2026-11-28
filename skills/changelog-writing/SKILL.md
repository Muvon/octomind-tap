---
name: changelog-writing
title: "Changelog Writing"
description: "Classify verified changes and write structured Keep a Changelog entries with accurate versions and tag-based comparison links."
license: Apache-2.0
compatibility: "Requires git and read access to the repository; comparison links need real tags."
domains: developer
rules:
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut|classify)\b.{0,60}\bchangelog\b)
  - match((?i)\bkeep a changelog\b|\bCHANGELOG\.md\b.{0,30}\b(entries|entry|unreleased)\b)
  - semantic(add entries for the changes since the last tag to the changelog, 0.72)
  - semantic(update the changelog file with a new section and compare links, 0.72)
  - semantic(which changes since the last tag belong under added and fixed, 0.72)
---

## Overview

Turn a commit range or supplied diff into a code-grounded record of noteworthy changes for project users and operators. Maintain the canonical changelog. Use CHANGELOG.md unless a target is supplied.

For a standalone file update, require a starting ref. A draft or a classification can use an explicitly supplied diff without one.

## Rules

- Resolve the requested refs or read the supplied diff. Verify each candidate entry against the code at the selected end revision (it may differ from the working tree). Treat commit subjects as pointers to the code. Check names, public compatibility and migration evidence.
- Group one entry per logical change under Added, Changed, Deprecated, Removed, Fixed or Security, using the headings that apply. Omit empty headings and incidental churn. Describe the visible behavior and the affected public surface.
- Treat SemVer and change headings as separate decisions. A backward-incompatible public API change is major, backward-compatible public functionality or a public API deprecation is minor, and a backward-compatible bug fix is patch. Apply the project's documented policy where it governs the release.
- Put pending changes under Unreleased unless the user supplies a release version. Keep Unreleased at the top. When cutting a release, move approved entries to the dated version section and preserve earlier sections. Use an ISO calendar date. Keep a supplied version identifier distinct from a recommended bump.
- Check comparison refs against actual tags, verify version links, and preserve existing link conventions. Use the canonical format when bootstrapping a file.
- Ask before resolving an ambiguous version collision or converting a different format.
- Preserve released history. Report an empty user-facing range without editing. Ground concrete names, behavior and performance claims in evidence; omit unsupported claims and internal churn.

## Output format

Follow the requested format for a classification or draft. For a changelog, write one user-facing entry per logical change under the applicable canonical headings. Edit only the target changelog when the request calls for an edit.

## Checklist

- [ ] Each entry traces to a verified change.
- [ ] Proposed version impact follows public compatibility.
- [ ] Released sections and existing links are preserved, and new comparison refs resolve.

## References

- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
- `release-notes-writing` covers narrative release notes for the same range.
