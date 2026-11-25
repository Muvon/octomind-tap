---
name: source-to-draft
title: "Editorial Briefs and Drafts from Raw Material"
description: "Trace a usable editorial angle to raw notes or transcripts, prepare a source brief, and shape a short blog draft without inventing details."
license: Apache-2.0
domains: content
rules:
  - session(tap-content-draft-)
  - match((?i)\b(editorial brief|article outline|short blog draft)\b.{0,70}\b(from|using|based on)\b.{0,30}\b(raw notes|meeting notes|transcript|voice memo|brain[ -]?dump)\b)
  - match((?i)\b(raw notes|meeting notes|transcript|voice memo|brain[ -]?dump)\b.{0,80}\b(into|as)\s+(an?\s+)?(editorial brief|article outline|short blog draft)\b)
---

## Overview

Use the source material to find a supported angle and make a brief, outline, or short blog draft. An editorial brief can serve any downstream format.

## Rules

1. Read the material in full. Inventory claims, named entities, emotional beats, surprising details, contradictions and gaps. Retrieve relevant user-confirmed preferences for voice and audience.
2. Propose two or three angles with one-line rationales. Ask at most one question per turn when a missing fact would change the result. Confirm the angle and format before drafting, or select them and state assumptions when the user delegates that decision.
3. When preparing a brief, preserve source paths or verbatim material according to the requested output. Include the supported angle, audience, outline, load-bearing specifics and confirmed voice notes when the contract calls for them. Report unavailable source material as requested by the caller.
4. In a short blog draft, trace names, figures, quotations, versions, prices and URLs to supplied material, confirmed facts, or relevant verified sources. Fix weak sections and fix or surface critical audit findings before delivery. Include a short audit summary and revision options when presenting the draft.
5. Hand off a source brief for platform-native posts or research-heavy articles. Save a draft only on request. Store durable voice preferences only after user confirmation.

## Checklist

- [ ] The angle and format are confirmed or expressly delegated.
- [ ] Each concrete claim traces to evidence.
- [ ] The output follows the brief, draft, or handoff contract.
