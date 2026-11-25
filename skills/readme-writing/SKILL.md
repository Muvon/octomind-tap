---
name: readme-writing
title: "README Writing"
description: "Draft or update a project README with a verified quick start, audience-specific sections, and evidence for public claims."
license: Apache-2.0
domains: developer
rules:
  - session(tap-developer-readme-)
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut)\b.{0,60}\breadme\b)
---

## Overview

Help the intended reader decide whether the project solves their problem and reach a working result.

## Rules

- Read the existing README, manifests, entry points, examples, license, and relevant CI. Preserve intentional content and project conventions. For a targeted change, limit edits to invalidated sections.
- State the project category, what it does, and who it serves. Support measurements and comparisons with evidence and conditions. Include badges, assets, and links when they resolve and serve the reader.
- Put the smallest working example near the top. For a CLI, show installation and the first command. For a library, show the import and call. For a service, cover authentication and a working request. For a web app, show local setup or a demo. For a workspace, link the relevant packages.
- Add configuration, architecture, contribution, and license sections where applicable. Prefer repository-relative links for internal docs and supply alt text for images.
- Check copy-paste commands, prerequisites, expected output, links, and anchors. Run safe authorized examples and disclose any command you could only inspect.

## Checklist

- [ ] The first paragraph identifies the project and audience.
- [ ] The first example reaches a working result.
- [ ] Every concrete claim, command, and link has been checked against available evidence.
