---
name: readme-writing
title: "README Writing"
description: "Draft or update a project README with a verified quick start, audience-specific sections, and evidence for public claims."
license: Apache-2.0
compatibility: "Requires read access to the repository; running the quick start needs the project's own toolchain."
domains: developer
rules:
  - match((?i)\b(write|draft|generate|create|update|rewrite|refresh|maintain|prepare|cut)\b.{0,60}\breadme\b)
  - semantic(write a readme for this project, 0.72)
  - semantic(update the readme so the quick start actually works, 0.72)
  - semantic(write a project introduction for people who will use this library, 0.72)
  - semantic(rewrite our readme for a new audience, 0.72)
---

## Overview

Help the intended reader decide whether the project solves their problem and reach a working result. Write or update the project README for its audience, ground it in the actual project, and preserve intentional author content. The README runs from the introductory description to the first working example and links to deeper documentation.

## Rules

- Read the existing README, manifests, entry points, examples, license and relevant CI. Preserve intentional content and project conventions. Identify the audience and the smallest working use case. For a targeted change, limit edits to the sections the request invalidates.
- State the project category, what it does, and who it serves. Support measurements and comparisons with evidence and conditions. Include badges, assets and links when they resolve and serve the reader.
- Match sections to the project type and put the smallest working example near the top. For a CLI, show installation and the first command. For a library, show the import and call. For a service, cover authentication and a working request. For a web app, show local setup or a demo. For a workspace, link the relevant packages.
- Add configuration, architecture, contribution and license sections where applicable. Prefer repository-relative links for internal docs and supply alt text for images.
- Check copy-paste commands, prerequisites, expected output, links and anchors. Run safe, authorized examples and flag any command you could only inspect. Ground claims and links in project evidence.
- Autonomous edits write only the named target. For interactive rewrites, confirm the scope and show the draft before replacing the file.

## Output format

Produce the requested README draft or edit. Lead with what the project does and who it serves, followed by the fastest working example.

## Checklist

- [ ] The first paragraph identifies the project and audience.
- [ ] The first example reaches a working result.
- [ ] Every concrete claim, command and link has been checked against available evidence.
