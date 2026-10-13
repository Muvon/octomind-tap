---
name: resume-conventions
title: "Global Resume & CV Conventions"
description: "Country-by-country conventions for job-application documents in 2026: resume vs CV terminology, length, whether to include a photo, data-processing consent clauses, work-authorization lines, date and locale formatting, and personal-data norms. Adapt an application to the target market so it reads correctly and stays legally safe wherever it's sent."
license: Apache-2.0
compatibility: "No external tools required. Markets covered: US/CA, UK/IE, continental Europe, AU/NZ, plus photo/data norms for DE, FR, and Asia."
domains: coach
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

Detect the target market first (from the posting's location/company, or ask), then apply that market's conventions. When the target is genuinely ambiguous, ask rather than guess — the wrong convention (a photo in a no-photo market, a missing consent clause in Poland, a US date order in Europe) is a real failure.

## Instructions

### Terminology and length

| Market | Document name | Typical length |
|---|---|---|
| US / Canada | Resume (CV = academic only) | 1–2 pages |
| UK / Ireland | CV | ~2 pages |
| Continental Europe | CV (DE: Lebenslauf) | 1–2 pages; up to 3 for senior roles |
| Australia / NZ | Resume or CV | 2–4 pages |
| Academic / research (any country) | CV | as long as the record needs (6+ pages fine) |

"Resume" is primarily a US/Canada term; most of the world says "CV" for the same short professional document. Use the name the target market uses.

### Photo

- US, UK, Canada, Australia, Ireland: no photo. Anti-discrimination norms mean a photo can create legal risk for the employer and get the application screened out. Never include one.
- Germany: traditionally a professional passport-style photo was expected, but since the 2006 AGG anti-discrimination law it has become increasingly optional — many current German applications omit it, and no employer may require one. So treat it as the candidate's choice: a professional photo is safe and still common, and omitting it is now fully acceptable. Note the choice; don't force either way.
- France, Spain, much of continental Europe, and much of Asia: photo still commonly expected, though the same optional-shift is spreading.
- When unsure, default to no photo for US/UK/CA/AU/IE (there it is a hard rule), and for photo-culture markets present it as an accepted-but-optional choice rather than a mandate; ask when it materially matters.

### Personal data and consent clauses

- A consent clause is not a GDPR requirement for an ordinary application: employers process applicant data on the pre-contract legal basis (GDPR Art. 6(1)(b); in Germany alongside § 26 BDSG) and must give applicants their own privacy notice.
- Poland is the exception by custom: recruiters expect a RODO consent line at the foot of the CV, and many postings quote the exact wording to use. Add one there, and anywhere a posting asks for it. A separate opt-in sentence covers keeping the CV for future recruitment.
- Personal data norms differ: date of birth, marital status, and nationality still appear on some German, French, and Central European CVs but are optional, and omitted (and can be discriminatory to request) in the US/UK/CA/AU. Include only what the target market expects and the candidate consents to.
- Work authorization: state it in one line when it is a likely knockout question (UK "right to work", US "authorized to work in the US", EU Blue Card or permit status).
- Never add sensitive personal data the candidate did not provide.

### Locale formatting

- Dates: US `MM/DD/YYYY` or `Month YYYY`; most of the rest of the world `DD/MM/YYYY` or `Month YYYY`. Use the target market's order; be consistent throughout.
- Spelling: match the market's English variant (US vs UK spelling) when the application language is English.
- Contact: phone in the target country's international format; a city/country line rather than a full street address is now standard and privacy-safe.
- Language: if the posting is in a non-English language, the application should be in that language unless the posting says otherwise — hand the localization to the localize workflow / content-locale-humanize for native fluency.

## Examples

Same candidate, US software role: 1-page resume, no photo, no DOB, `Month YYYY` dates, US spelling, city/state line, no GDPR clause.

Same candidate, German software role: 2-page Lebenslauf/CV, employment dates as `MM/YYYY` (`03/2021 – heute`), structured and thorough, no consent clause needed — a professional photo optional (traditional but no longer expected post-AGG). Same facts, adapted to the market.

Same candidate, Polish role: 1–2 page CV in the posting's language, the RODO consent line from the posting at the foot, photo optional.

## Checklist

- [ ] Correct document name and length in range for the detected market.
- [ ] Photo present or absent per the market rule, and only if the candidate chose it.
- [ ] Consent clause present for Poland or when the posting asks; absent otherwise.
- [ ] Dates and spelling in the local convention, consistent throughout.
- [ ] Work authorization stated where it is a likely knockout.
- [ ] No personal data the market discourages or the candidate did not provide.

## References

- GDPR Art. 6(1)(b) (pre-contract processing); Germany: Allgemeines Gleichbehandlungsgesetz (AGG, 2006) and § 26 BDSG
- [Careers in Poland: the consent clause on a Polish CV](https://www.careersinpoland.com/article/work/the-one-thing-you-should-never-leave-off-your-polish-cv)
- [Europass CV](https://europass.europa.eu/en/create-europass-cv)
