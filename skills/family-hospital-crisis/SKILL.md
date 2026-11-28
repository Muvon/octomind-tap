---
name: family-hospital-crisis
title: "Parent in the Hospital: Status, Discharge and Funding Rules"
description: "US hospital-crisis rules for an older parent: observation vs inpatient, the skilled-nursing 3-day rule, discharge appeal, PACE, VA aid, estate recovery."
license: Apache-2.0
compatibility: "Requires: web search for the state Medicaid agency and the Medicare quality improvement organization. US only; 2026 dollar figures change yearly."
domains: family-advisor
rules:
  - content(observation status)
  - content(discharge planning)
  - content(skilled nursing)
  - content(estate recovery)
  - content(Aid and Attendance)
  - content(PACE)
  - match((?i)(mom|dad|mother|father|parent).*(hospital|\ber\b|emergency).*(fell|fall|admitted|discharge))
---

## Overview

An older parent is in the hospital and the family has days, not weeks, to decide on care after discharge. This skill holds the US rules that families trip over: how the hospital labels the stay, what Medicare pays afterwards, how to appeal a discharge, and which programs and estate rules matter for the money. It is orientation; the agent never decides a medical or legal question.

## Mental model

Two clocks run at once: the discharge date, and the hospital label (inpatient or outpatient observation) that decides what Medicare covers after discharge. Ask both questions on day one.

## Rules

Status and skilled nursing

- Observation services are outpatient services. A person under observation is an outpatient even overnight; Part A pays nothing for the stay and Part B covers doctor and hospital outpatient services (Medicare.gov).
- If observation lasts more than 24 hours, the hospital must give the Medicare Outpatient Observation Notice (MOON). Ask for it and ask the hospital to state in writing whether the parent is inpatient or outpatient and why.
- Skilled nursing facility coverage under Original Medicare needs a medically necessary inpatient stay of at least 3 days in a row. The admission day counts, the discharge day does not, and time under observation or in the emergency room does not count. The person generally enters the facility within 30 days of leaving the hospital and needs daily skilled care ordered by a doctor. Some Medicare Advantage plans and accountable care organization waivers waive the 3 days. 2026 costs per benefit period: days 1 to 20 are $0 after the $1,736 deductible; days 21 to 100 are $217 a day; after day 100 the person pays all (Medicare.gov, 2026).
- Medicare does not pay for long-term custodial care.

Discharge notice and fast appeal

- The hospital must give "An Important Message from Medicare about Your Rights" within 2 days of admission and before discharge; if not received, ask for it.
- To appeal a discharge, follow the directions on the notice and request the fast appeal no later than the planned discharge day. An independent reviewer, the Beneficiary and Family Centered Care Quality Improvement Organization (BFCC-QIO), decides. If the request is on time, the person can stay in the hospital while waiting and owes only the usual deductible or coinsurance; if the reviewer finds services should end, the person generally owes nothing through noon of the day after the decision. Medicare Advantage plans follow different rules; read the plan's notice. The QIO for each state is named on the notice and at Medicare.gov.
- Ask the hospital case manager for a written discharge plan and the names of facilities that have beds.

Funding programs to screen before the money runs out

| Program | What it is | Check |
|---------|------------|-------|
| Medicaid estate recovery | States must seek repayment from the estate of a person 55 or older for nursing facility, home and community-based and related hospital and drug services; states may not recover while there is a surviving spouse, a child under 21, or a blind or disabled child of any age; undue-hardship waivers must exist (Medicaid.gov) | State Medicaid agency; an elder-law attorney before any asset move |
| PACE | All-inclusive care for people 55 or older who live in a PACE service area, are certified by the state as needing nursing-home level of care, and can live safely in the community; offered only in some states (Medicaid.gov, Medicare.gov) | The state's PACE list |
| VA Aid and Attendance | An extra monthly amount for a person already receiving a VA pension who needs help with daily activities, is bedridden, is in a nursing home, or has very limited vision; forms VA 21-2680 (medical examiner part) and, in a nursing home, 21-0779 (VA.gov, updated 2026-05-08) | VA pension eligibility, accredited representative |
| Medicare Savings Programs and Extra Help | Pay Medicare premiums and cost sharing and cut drug costs; apply through the state Medicaid office (Medicare.gov) | The family-medicare-aca-enrollment skill |

Never move the parent's assets to qualify for Medicaid without an elder-law attorney: look-back rules apply.

## Examples

Bad: "Medicare will cover rehab after the hospital."
Good: "Ask today: is Mom inpatient or under observation? Medicare covers skilled nursing only after 3 inpatient days in a row, and observation days do not count. Get the status in writing, and if the planned discharge is tomorrow, the appeal request is due by then."

## Checklist

- [ ] Status (inpatient or observation) and the day count asked first.
- [ ] MOON or Important Message from Medicare requested if missing.
- [ ] Discharge date and appeal deadline written down.
- [ ] Funding programs screened; the estate-recovery rule stated; attorney named for asset moves.
- [ ] Every dollar figure labeled 2026 with its source.

## References

- Inpatient or outpatient status: https://www.medicare.gov/coverage/inpatient-hospital-care/inpatient-outpatient-status
- Skilled nursing facility care: https://www.medicare.gov/coverage/skilled-nursing-facility-snf-care
- Fast appeals: https://www.medicare.gov/providers-services/claims-appeals-complaints/appeals/fast-appeals
- Medicaid estate recovery: https://www.medicaid.gov/medicaid/eligibility-policy/estate-recovery
- PACE: https://www.medicaid.gov/medicaid/long-term-services-supports/program-of-all-inclusive-care-for-elderly
- VA Aid and Attendance: https://www.va.gov/pension/aid-attendance-housebound/
