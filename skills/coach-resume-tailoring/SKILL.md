---
name: coach-resume-tailoring
title: "Resume Tailoring to a Job Posting: Truthful Package"
description: "Fit a master resume to one job posting and write the cover letter: keyword mapping, market conventions, gap report, PDF and Word files, never fabricated."
license: Apache-2.0
compatibility: "Requires the resume-rendering tools (see that skill); web fetch reads a posting URL; web search confirms market conventions. macOS/Linux."
capabilities: shell resume-render documents webfetch
domains: coach
rules:
  - match((?i)\b(tailor|tailoring|customi[sz]e|adapt|tweak|revise|convert|rewrite|fix)\b.{0,40}\b(resume|cv)\b)
  - match((?i)\b(extract|work|map)\b.{0,40}\bkeywords?\b|\bgap report\b)
  - match((?i)\b(apply|address|resolve)\w*\b.{0,40}\bfindings\b|\baudit findings\b)
  - match((?i)\badapt\w*\b.{0,30}\b(conventions?|format)\b|\bwrite\b.{0,20}\bcover letter\b)
  - semantic(fit my resume to this job posting and write the cover letter, 0.74)
  - semantic(apply the audit findings to my tailored resume, 0.72)
  - semantic(tailor my master resume to this job description and map the keywords)
  - semantic(list the gaps between my resume and what the posting asks for)
---

## Overview

Tailor an existing resume to a specific job posting and write the matching cover letter. This is document production, not career coaching: direction advice, strategy and interview prep are separate work. The input is a master resume plus a target posting; the output is an ATS-optimized, country-correct application package that reads as truthfully and specifically as possible, as ready-to-send PDF and Word files.

Covered: reading the master resume and the target posting, extracting the posting's priority keywords, title and requirements, tailoring the resume (bullets, summary, skills order) truthfully, writing the cover letter, adapting to the target country's conventions, applying findings from an audit, and producing an honest gap report. Not covered: career direction, mock-interview drilling, independently scoring the package (the application-screening skill), and submitting applications. Never auto-apply or post anywhere: produce documents for the human to submit.

## Mental model

Truthful tailoring: mirror the posting's language and priorities, but only ever using experience, skills, titles, dates and numbers that are real for this candidate. Fabrication is the one thing never done. Order of work, always: tailor to the posting, adapt to the market, ground in the truth. Be specific and quantified (achievements as problem solved plus scope plus result, never bare skill tokens), human rather than template, and honest about gaps.

## Rules

### Truthfulness gate

Hard and non-negotiable: every keyword, metric, title, date, employer, degree and skill on the tailored resume and cover letter must be supported by the master resume or the candidate's explicit input. No invented experience, no inflated numbers, no white text, hidden AI-prompt text or density keyword-stuffing, no auto-submitting. A gap is reported honestly, never faked.

### Skills this work draws on

- `ats-optimization`: how modern ATS ranks, the per-job tailoring workflow, coverage targets, the truthfulness gate, parser-safe formatting and the match report.
- `resume-conventions`: the target market's document name, length, photo rule, data-processing clause custom and locale formatting.
- `cover-letter`: cover-letter structure, grounding and avoiding template tells.
- `content-voice`: human phrasing for the cover letter and summary.
- `resume-rendering`: the resume as RenderCV YAML, the ATS-safe theme settings, the PDF and DOCX files and the text-layer check.
- `document-export`: the cover letter PDF and Word exports and the PDF check.

Read them and apply them verbatim.

### Typical run

1. Intake. Read the master resume (file) and the job posting (file, fetched URL or pasted). Capture the candidate's real experience verbatim as the ground truth. Extract the posting's exact title, 15-20 priority keywords, and required vs preferred qualifications. Detect the target market (from the posting's location and company; ask if genuinely ambiguous). If either the resume or the posting can't be read, say so plainly and stop; never invent a candidate history or a job's requirements.
2. Tailor. Map each priority keyword to real experience; mirror the posting's phrasing only where it maps; rewrite bullets as quantified achievements; reorder skills; write the summary with the target title. Adapt name, length, photo, consent clause and dates to the market.
3. Cover letter. Write it grounded in the tailored resume and the specific company and role.
4. Gap report. List requirements the candidate genuinely doesn't meet, with honest options (true adjacent-experience reframing, mark as stretch, or upskill), never a fabricated line.
5. Files. Write the tailored resume as RenderCV YAML, render `<First>_<Last>_Resume.pdf` (market paper size), run `doc-export check` and read the text layer top to bottom, then produce the DOCX twin and the cover letter PDF as `resume-rendering` describes. A date or section out of order in the text layer is fixed before delivery.
6. Audit findings. When applying findings, resolve every one without reintroducing anything already fixed and without breaking the truthfulness gate; re-render and re-check. Criticals first.

Fetch a posting URL with knowledge(command="read", source="<url>"). Use web search to confirm a target market's current convention or a role's standard keyword vocabulary when unsure: verify, don't guess, and never claim a source you didn't check. remember() the candidate's master resume and prior tailoring decisions at the start; memorize() durable facts about the candidate and their target roles (never fabricated content).

### Common situations

| Situation | Response |
|-----------|----------|
| Master resume and posting given | Intake, tailor, cover letter, gap report |
| Posting is a URL | Fetch it; if unreachable, say so and stop (don't invent requirements) |
| Target country unclear | Ask once, then proceed |
| "Just the resume" / "just the cover letter" | Scope to that |
| Audit findings supplied | Apply them, criticals first, truthfulness intact |

### Don'ts

- Never fabricate or inflate experience, skills, titles, dates, employers, degrees or numbers; it is the highest-cost failure and surfaces in interviews and reference checks.
- Don't keyword-stuff, use invisible or white text or hidden AI-prompt instructions, or jam keyword lists into headers and footers; screening tools and recruiters flag all of them.
- Don't include a photo where the market expects none (US, UK, CA, AU, IE), and add a data-processing consent clause only where the market expects it (for example Poland) or the posting asks for one.
- Don't leave a genuine gap silently faked.

## Output format

Deliver the tailored resume as PDF (plus DOCX when a portal or recruiter wants Word), the cover letter as PDF, the RenderCV YAML source, and a short match and gap report with the text-layer check result. Save in the working directory (in place, git-aware if inside a repo); return text inline only when the user asks for text. Preserve the candidate's real content; only tailoring, ordering, phrasing and market adaptation change. Never write staging or backup copies unless asked.

## Checklist

- [ ] Both inputs were read; the market is known.
- [ ] Every line traces to the master resume or the candidate's confirmed input.
- [ ] The cover letter is specific to this company and role.
- [ ] The gap report lists real gaps with honest options.
- [ ] The text-layer check ran and its result is reported.
- [ ] Nothing was submitted anywhere.

## Composition / References

- `ats-optimization`, `resume-conventions`, `cover-letter`, `resume-rendering`, `document-export`, `content-voice` skills, as listed above.
- `coach-application-screening` skill: the independent audit of the finished package.
