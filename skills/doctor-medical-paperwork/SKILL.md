---
name: doctor-medical-paperwork
title: "Letter of Medical Necessity & Prior Authorization Drafts"
description: "Drafts letters of medical necessity, prior-authorization packets, records requests and leave forms from supplied records, with a fact-to-source table."
license: Apache-2.0
compatibility: "Requires: filesystem write for the drafts. US forms and deadlines; check the current form version on the agency site."
domains: doctor
rules:
  - content(letter of medical necessity)
  - content(prior authorization)
  - content(prior-authorization)
  - content(prior auth)
  - match((?i)request.*(medical )?records)
  - content(medical records request)
  - content(FMLA)
  - content(disability form)
  - match((?i)(write|draft|fill).*(letter|form).*(doctor|insurance|denial|leave))
---

## Overview

A person gives the agent records and asks for a document a clinician or payer needs: a letter of medical necessity, a prior-authorization packet, a records request, or a leave or disability form. The outcome is a draft built only from the supplied records, a table that proves each clinical fact, a list of what is missing, and blank signature blocks for the clinician.

## Mental model

The draft is a convenience for the clinician, not a clinical document. Every sentence that states a medical fact must trace to a page the user supplied; everything else is a blank or a question.

## Rules

1. Name the document type and who signs it before drafting.
2. Build the fact-to-source table first: fact, source document and date, location (page or line), quote. A fact with no row is not written.
3. Draft from the table in the record's own words. Do not diagnose, infer a condition, estimate prognosis, or strengthen or soften a clinician's wording.
4. Leave signature, license number and every attestation ("I certify", work-capacity opinions, medical-necessity statements) blank and marked for the clinician.
5. End with the missing list: records not supplied, payer criteria not answered, dates, and questions for the clinician.
6. Keep identifiers (Social Security, policy and member numbers) out unless the form requires them; mark blanks.

By document type

| Document | Build it this way | Rule sourced from |
|----------|-------------------|-------------------|
| Letter of medical necessity | Ask the payer for its written criteria for the service; answer each criterion with a sourced fact; list treatments tried and the dates and results as recorded | Payer criteria |
| Prior-authorization packet | Request form, the letter, the fact table, a criteria checklist, attachments by name, in the order the payer lists | Payer |
| Records request | Written request to the provider for named records, in a stated format, with where to send them; under the HIPAA right of access the provider must act within 30 calendar days and may extend once by up to 30 more days with written notice of the reason and the date | HHS, HIPAA right of access |
| FMLA certification | The employer's request starts a window of at least 15 calendar days to return the clinician's completed certification; an incomplete one must be fixed within 7 calendar days of the employer's written notice; the employee pays any cost of the certification; the Department of Labor's optional forms are WH-380-E (employee's own condition) and WH-380-F (family member's) | US Department of Labor, Fact Sheet 28G |
| Other disability or leave form | Follow the insurer's or employer's own form; the clinician completes the medical sections | The form |

## Examples

Bad: "Mr. R has severe chronic back pain unresponsive to conservative therapy and requires an MRI."
Good: "The 2026-03-04 clinic note (page 2) records low back pain for 14 weeks and states physical therapy was tried 2026-01 to 2026-02 without improvement. Payer criterion 3 asks for 6 weeks of therapy: the note supports it. Missing: the neurological exam, which the clinician must add. Signature and attestation: left for the clinician."

## Checklist

- [ ] Document type and signer named.
- [ ] Fact-to-source table complete before any prose.
- [ ] No fact without a source row; no diagnosis added.
- [ ] Signature and attestation blank.
- [ ] Missing list included; deadlines stated with their source.

## References

- HHS, individuals' right to access health information: https://www.hhs.gov/hipaa/for-professionals/privacy/guidance/access/index.html
- Department of Labor, Fact Sheet 28G, medical certification under the FMLA: https://www.dol.gov/agencies/whd/fact-sheets/28g-fmla-serious-health-condition
- Department of Labor, health care provider certification: https://www.dol.gov/agencies/whd/fmla/certification-of-a-serious-health-condition
