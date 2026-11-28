---
name: doctor-guideline-anchors
title: "Health Guidelines: Current US Thresholds and Screening"
description: "Current US guideline positions for blood pressure, diabetes, lipids, cancer screening, childhood vaccines and obesity drugs, with checks to run."
license: Apache-2.0
compatibility: "Requires: web search or the medical-reference tools to confirm the current guideline version; US positions, with NICE, ESC or WHO equivalents elsewhere."
domains: doctor
rules:
  - match((?i)\b(screening|mammograph\w*|colonoscopy|pap smear|cervical screening)\b)
  - match((?i)\b(vaccines?|vaccination|immuni[sz]ations?)\b.{0,80}\b(schedule|recommend\w*|evidence|effective\w*|prevent\w*|guidelines?|studies)\b)
  - match((?i)\b(diabetes|prediabetes|hypertension|blood pressure|cholesterol|ldl|chronic kidney disease|ckd|hypothyroidism)\b.{0,100}\b(guidelines?|goals?|targets?|thresholds?|cut-?offs?|diagnos\w+|stages?|criteria|managed|monitored)\b)
  - match((?i)\b(guidelines?|uspstf|aha|cdc)\b.{0,60}\b(recommend\w*|say|says|screening|schedule|stage|goal)\b)
  - match((?i)\b(wegovy|zepbound|semaglutide|tirzepatide|glp-1)\b.{0,40}\b(obesity|weight loss|approved)\b)
  - semantic(what are the current guideline targets for blood pressure, cholesterol and A1C)
  - semantic(at what age should I start cancer screening such as colonoscopy or mammogram)
  - semantic(which vaccines are recommended for children and when are they due)
---

## Overview

A person asks what the current guideline says: a blood pressure goal, a diagnosis threshold, when to start a screening test, which vaccine schedule applies. The outcome is the current published position with its source and date, a flag where sources disagree, and the questions to bring to a clinician. Guidelines change, so every figure is checked against the current version before it is quoted.

## Rules

- Check for a newer version before quoting any row below; say which guideline and year the figure comes from.
- Use NICE, ESC or WHO equivalents outside the US.
- A guideline gives population thresholds; the personal goal is the clinician's call.

| Topic | Current position |
|-------|------------------|
| Blood pressure (2025 AHA/ACC) | Hypertension ≥ 130/80; goal < 130/80 for most adults; stage 1 (130-139/80-89): medication together with lifestyle change for selected adults with cardiovascular disease, previous stroke, diabetes, chronic kidney disease, or 10-year PREVENT risk ≥ 7.5% (AHA/ACC guideline, Hypertension 2025; ahajournals.org); otherwise 3-6 months of lifestyle change first, then medication if still ≥ 130/80 |
| Diabetes (ADA Standards of Care 2026) | Diabetes: HbA1c ≥ 6.5% or fasting glucose ≥ 126 mg/dL, confirmed; prediabetes: 5.7-6.4% or 100-125 |
| Lipids (2026 ACC/AHA) | LDL-C goals by risk: < 100 / < 70 / < 55 mg/dL; Lp(a) measured once in adulthood |
| Screening (USPSTF) | Mammography every 2 years at 40-74; colorectal 45-75; lung low-dose CT at 50-80 with ≥ 20 pack-years; cervical 21-65 (final 2018: cytology every 3 years at 21-29; HPV alone every 5 allowed at 30-65; a December 2024 draft adding self-collected HPV had no final version as of 2026-11, so check) |
| Childhood vaccines (US) | Since January 2026 the CDC schedule and the American Academy of Pediatrics schedule differ; a court order of 16 March 2026 (AAP v. Kennedy, D. Mass.) stayed the CDC's 5 January 2026 changes, and as of 2026-11 the CDC page (cdc.gov/vaccines/hcp/imz-schedules) posts the 2 July 2025 schedule as current, so check the current status; show both, say they differ, and send the family to the pediatrician and state health department |
| Obesity drugs | Injectable semaglutide and tirzepatide, plus oral options (Wegovy pill Dec 2025, orforglipron Apr 2026) |

## Examples

Bad: "Hypertension starts at 140/90."
Good: "The 2025 AHA/ACC guideline defines hypertension as 130/80 or higher, with a goal under 130/80 for most adults. Whether medication fits you depends on your cardiovascular risk: ask your clinician for your PREVENT score."

## Checklist

- [ ] Guideline name and year stated with each figure.
- [ ] Current version checked for the row quoted.
- [ ] Conflicting sources (for example CDC and AAP schedules) both shown.
- [ ] Personal goal left to the clinician.
