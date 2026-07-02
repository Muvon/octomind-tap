---
name: ats-optimization
title: "ATS Optimization & Per-Job Tailoring"
description: "How modern applicant tracking systems rank resumes in 2026 and how to tailor a resume per job posting so it clears them — keyword strategy grounded in the candidate's real experience, job-title placement, coverage targets, parser-safe formatting, and the anti-stuffing rules that current ATS actively penalize. Truthful tailoring only."
license: Apache-2.0
compatibility: "For resume/application agents (coach:resume, coach:screener). Pairs with resume-conventions and cover-letter."
domains: career
rules:
  - career(ats)
  - career(resume)
  - career(tailor)
  - match(\bATS\b)
  - match(\bapplicant tracking system\b)
  - match(\btailor\s+(my|the|this)\s+(resume|cv)\b)
  - match(\b(optimi[sz]e|beat|pass)\s+.{0,20}(ats|applicant tracking)\b)
  - semantic(tailor this resume to a job posting so it passes ATS)
  - semantic(optimize my resume keywords for this job)
  - semantic(why is my resume getting rejected by applicant tracking systems)
---

## Overview

An applicant tracking system (ATS) is the software between a submitted resume and a human recruiter. In 2026 the major systems (Workday, Greenhouse, iCIMS) rank with semantic and skills-graph matching, not literal keyword counting — so the winning move is truthful, per-job tailoring, and the losing move is keyword stuffing, which current systems flag as manipulation.

This skill encodes how they rank and how to tailor a resume to a specific posting without fabricating anything. The ethic is non-negotiable: every keyword must map to real experience the candidate actually has.

## Instructions

### How modern ATS ranks (2026)

Context beats frequency. One line — "led a $12M platform migration across 4 teams" — outscores five bare repetitions of "platform migration". Skills-graph matching means the system understands related terms, but it still under-recognizes synonyms, so mirroring the posting's exact phrasing matters.

Density is policed. Workday's 2026 ranking flags resumes with unnaturally high keyword density as manipulation. If "project management" appears 15 times in a two-page resume, that hurts, not helps. Aim for natural placement, not saturation.

The job title is the single highest-value keyword. Recruiters search the ATS by target job title first; candidates whose resume carries the target title (in the summary or a recent role) are far more likely to surface. Include the posting's exact title somewhere near the top when it is truthful to do so.

### Per-job tailoring workflow

1. Extract the posting's priority signals: the exact job title, 15–20 priority keywords/skills, required vs preferred qualifications, and the recurring language the posting uses for each.
2. Map each priority keyword to a real item in the candidate's master resume. If it maps, mirror the posting's phrasing in that bullet. If it does NOT map to real experience, it does not go in — flag it as a gap instead.
3. Rewrite achievement bullets to lead with the mirrored keyword inside a quantified accomplishment (action + scope + result), not as a bare skill token.
4. Reorder the skills section and role bullets so the most posting-relevant items come first.
5. Place the target title and 3–4 top keywords naturally in a 2–3 sentence professional summary.
6. Compute coverage: aim for roughly 60–80% of the posting's priority keywords represented, all truthfully. Below that, callback odds drop; stuffing above it triggers density penalties.

### Coverage and honesty gates

- Truthfulness gate (hard): every claim, keyword, metric, title, and skill on the tailored resume must be supported by the candidate's master resume or explicitly confirmed by them. No invented employers, dates, degrees, tools, or numbers. This is the highest-cost failure — it surfaces in interviews and reference checks even when it clears the ATS.
- No invisible/white-text keywords, no keyword lists jammed into headers/footers, no density-stuffing. Current ATS and recruiters catch all three.
- Gaps are reported, not faked. When the candidate genuinely lacks a required qualification, surface it honestly with options: an adjacent-experience reframing that is still true, a note that it is a stretch, or an upskilling suggestion — never a fabricated line.

### Parser-safe formatting

Resumes are parsed before they are read. Keep the machine able to read them:
- Single column. No tables, text boxes, columns, graphics, icons, skill bars, or photos in the parsed body (photo rules are locale-specific — see resume-conventions).
- Standard section order: contact, summary, skills, experience, education, certifications.
- Standard fonts (Arial, Calibri, Times New Roman) at 10–12pt; 1–2 pages for a resume (length is locale-specific — see resume-conventions).
- No critical info in headers/footers — many parsers drop them.
- Standard section headings ("Experience", not "Where I've Made an Impact").

### Match report

When auditing or delivering, produce a short, auditable match report: coverage percentage, the priority keywords matched (with the real experience each maps to), the keywords deliberately omitted because they had no truthful basis (the gaps), and any density or formatting risks. This makes the tailoring reviewable and keeps it honest.

## Examples

Posting says "Kubernetes", candidate ran container orchestration on Kubernetes in a prior role:

Weak (bare token): `Skills: Kubernetes, Docker, CI/CD`

Strong (mirrored, quantified, truthful): `Migrated 40+ services to Kubernetes, cutting deploy time from 25 min to under 4 and eliminating weekend release windows.`

Posting requires "5 years of Go", candidate has 2:

Wrong (fabrication): silently write "5+ years of Go".

Right (gap, honest): keep the real "2 years of Go" and flag in the report: "Posting asks 5y Go, you have 2 — reframe around depth (shipped X in Go) or treat as a stretch application; do not inflate."
