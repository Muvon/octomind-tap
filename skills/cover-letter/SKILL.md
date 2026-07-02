---
name: cover-letter
title: "Cover Letter Craft"
description: "Write a cover letter that a hiring manager actually reads — grounded in the candidate's real experience, tailored to the specific posting and company, structured for a 30-second skim, and free of the generic AI-template phrasing that gets letters discarded. Truthful, specific, and human."
license: Apache-2.0
compatibility: "For resume/application agents (coach:resume, coach:screener). Pairs with ats-optimization and resume-conventions; composes with content-voice for human phrasing."
domains: career
rules:
  - career(cover-letter)
  - match(\bcover letter\b)
  - match(\bmotivation letter\b)
  - match(\bwrite\s+(a|my|the)\s+cover letter\b)
  - semantic(write a cover letter for this job)
  - semantic(make my cover letter less generic)
---

## Overview

A cover letter's job is to connect the candidate's real, specific experience to this specific role and company in a way a busy hiring manager grasps in a skim. Most cover letters fail by being generic — interchangeable praise that could be sent to any company — or by restating the resume. This skill encodes how to write one that earns its read.

Every claim traces to the candidate's actual background. A cover letter that invents enthusiasm, achievements, or fit is worse than none.

## Instructions

### What a good cover letter does

- Opens with a specific hook — a real reason this candidate fits this role, or a genuine connection to the company's work — not "I am writing to apply for the position of…".
- Proves fit with 2–3 concrete, quantified achievements from the candidate's real experience that map to the posting's top requirements, framed as "here is the problem I solved" not "I have skill X".
- Shows it is for THIS company: reference something specific and true — the product, a stated challenge, the team's domain — that could not be copy-pasted to a competitor.
- Closes with a confident, low-pressure call to action.

### Structure

- Length: 3–4 short paragraphs, roughly 250–400 words, one page maximum. Hiring managers skim; density loses them.
- Hook paragraph: the specific fit or connection.
- Body (1–2 paragraphs): the mapped achievements, each tied to a posting requirement.
- Close: enthusiasm that is specific, plus the call to action.
- Salutation: a named person when discoverable; a role-specific greeting ("Dear Hiring Team for the X role") over "To Whom It May Concern".

### Grounding and honesty

- Pull every achievement, number, and skill from the candidate's resume or their confirmed input. No invented projects, metrics, or motivations.
- The enthusiasm must be real and specific — a fabricated "I've always admired your mission" reads as filler. If there is no genuine specific hook, use a truthful competence-based one instead.
- If the candidate is missing a stated requirement, do not paper over it with bravado. Lead with genuine strengths; a stretch application can acknowledge the gap briefly and pivot to adjacent, real experience.

### Avoid the AI-template tells

Generic cover letters read as mass-produced. Apply content-voice's rules: no dead phrases ("I am excited to apply", "proven track record", "team player", "hit the ground running", "align with your values"), vary sentence rhythm, use contractions, sound like a specific person. Strip anything that could belong in any other candidate's letter to any other company. If a sentence survives find-and-replace of the company name into a competitor's, it is too generic — rewrite it.

### Locale

Match the target market: the letter language follows the posting, formality follows the market (more formal in DE/FR/JP, warmer and more direct in the US), and the greeting/sign-off use local convention. Hand non-English letters to the localization path for native fluency.

## Examples

Generic open (discard pile): "I am writing to express my strong interest in the Senior Engineer position at your company. I am a passionate team player with a proven track record."

Specific open (grounded, human): "I spent the last two years cutting a data pipeline's cost by 60% at 3B events/day — which is the exact scaling problem your engineering blog described last month. That's why the Senior Data Engineer role caught my eye."
