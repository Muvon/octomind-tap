---
name: changelog-writing
title: "Changelog Writing"
description: "Classify verified changes and write structured Keep a Changelog entries with accurate versions and tag-based comparison links."
license: Apache-2.0
domains: developer
rules:
  - session(tap-developer-changelog-)
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut)\b.{0,60}\bchangelog\b)
---

## Overview

Turn a commit range or supplied diff into a record of noteworthy changes for project users.

## Rules

- Resolve requested refs and review the range and file changes. Use the selected end revision for evidence when it differs from the working tree. Treat commit subjects as pointers to the code.
- Group one entry per logical change under Added, Changed, Deprecated, Removed, Fixed, or Security. Omit empty headings and incidental churn. Describe the visible behavior and affected public surface.
- Treat SemVer and change headings as separate decisions. A backward-incompatible public API change is major, backward-compatible public functionality or a public API deprecation is minor, and a backward-compatible bug fix is patch. Apply the project's documented policy where it governs the release.
- Keep Unreleased at the top. When cutting a release, move approved entries to the dated version section and preserve earlier sections. Use an ISO calendar date. Keep a supplied version identifier distinct from a recommended bump.
- Check comparison refs against actual tags and preserve existing link conventions. Use the canonical format when bootstrapping a file.

## Checklist

- [ ] Each entry traces to a verified change.
- [ ] Proposed version impact follows public compatibility.
- [ ] Released sections and existing links are preserved, and new comparison refs resolve.

## References

- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)
