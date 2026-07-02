---
name: resume-conventions
title: "Global Resume & CV Conventions"
description: "Country-by-country conventions for job-application documents in 2026 — resume vs CV terminology, length, whether to include a photo, GDPR/consent clauses, date and locale formatting, and personal-data norms. Adapt an application to the target market so it reads correctly and stays legally safe wherever it's sent."
license: Apache-2.0
compatibility: "For resume/application agents (coach:resume, coach:screener). Pairs with ats-optimization and cover-letter."
domains: career
rules:
  - career(resume)
  - career(cv)
  - career(localize-resume)
  - match(\b(resume|cv)\s+(format|convention|for)\s+.{0,20}(germany|france|uk|us|europe|canada|australia|asia)\b)
  - match(\b(cv|resume)\s+photo\b)
  - match(\bGDPR\s+.{0,15}(cv|resume|application)\b)
  - semantic(what resume format should I use for a job in another country)
  - semantic(should my CV have a photo for this country)
  - semantic(do I need a GDPR clause on my CV)
---

## Overview

A job-application document that is perfect for one country can be wrong — or legally risky — in another. The word for it, the expected length, whether it carries a photo, and what personal data belongs on it all change by market. This skill encodes the 2026 conventions so an application is adapted to where it is actually being sent.

Detect the target market first (from the posting's location/company, or ask), then apply that market's conventions. When the target is genuinely ambiguous, ask rather than guess — the wrong convention (a photo where it is illegal to consider one, or a GDPR clause missing in the EU) is a real failure.

## Instructions

### Terminology and length

| Market | Document name | Typical length |
|---|---|---|
| US / Canada | Resume (CV = academic only) | 1–2 pages |
| UK / Ireland | CV | ~2 pages |
| Continental Europe | CV | 2–3 pages |
| Australia / NZ | Resume or CV | 2–4 pages |
| Academic / research (any country) | CV | as long as the record needs (6+ pages fine) |

"Resume" is primarily a US/Canada term; most of the world says "CV" for the same short professional document. Use the name the target market uses.

### Photo

- US, UK, Canada, Australia, Ireland: no photo. Anti-discrimination norms mean a photo can create legal risk for the employer and get the application screened out. Never include one.
- Germany: traditionally a professional passport-style photo was expected, but since the 2006 AGG anti-discrimination law it has become increasingly optional — many current German applications omit it, and no employer may require one. So treat it as the candidate's choice: a professional photo is safe and still common, and omitting it is now fully acceptable. Note the choice; don't force either way.
- France, Spain, much of continental Europe, and much of Asia: photo still commonly expected, though the same optional-shift is spreading.
- When unsure, default to no photo for US/UK/CA/AU/IE (there it is a hard rule), and for photo-culture markets present it as an accepted-but-optional choice rather than a mandate; ask when it materially matters.

### Personal data and GDPR

- EU / EEA applications: include a short GDPR consent clause permitting the employer to process the personal data in the application (a one-line "I consent to the processing of my personal data for recruitment purposes in accordance with GDPR" is the common form). Under GDPR, employers may only collect data necessary for the hiring decision and must not retain unsuccessful applicants' data beyond a short window.
- Personal data norms differ: date of birth, marital status, nationality, and a photo are normal on a German/French CV but are omitted (and can be discriminatory to request) in the US/UK. Include only what the target market expects and the candidate consents to.
- Never add sensitive personal data the candidate did not provide, and never omit a GDPR clause on an EU-targeted application.

### Locale formatting

- Dates: US `MM/DD/YYYY` or `Month YYYY`; most of the rest of the world `DD/MM/YYYY` or `Month YYYY`. Use the target market's order; be consistent throughout.
- Spelling: match the market's English variant (US vs UK spelling) when the application language is English.
- Contact: phone in the target country's international format; a city/country line rather than a full street address is now standard and privacy-safe.
- Language: if the posting is in a non-English language, the application should be in that language unless the posting says otherwise — hand the localization to the localize workflow / content-locale-humanize for native fluency.

### Adaptation checklist

Before finalizing, confirm for the detected market: correct document name, length in range, photo present-or-absent per the rule, GDPR clause present if EU/EEA, dates and spelling in the local convention, and no personal data the market forbids or the candidate did not consent to.

## Examples

Same candidate, US software role: 1-page resume, no photo, no DOB, `Month YYYY` dates, US spelling, city/state line, no GDPR clause.

Same candidate, German software role: 2-page Lebenslauf/CV, `DD.MM.YYYY` dates, a GDPR consent line, structured and thorough — a professional photo optional (traditional but no longer expected post-AGG). Same facts, adapted to the market.
