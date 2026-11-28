---
name: family-estate-orientation
title: "Estate Tax & Form 706 After a Death (US Federal)"
description: "US federal orientation after a death: estate tax exclusion and Form 706 due date, final income tax return, estate income tax return, who to ask."
license: Apache-2.0
compatibility: "Requires: web search for current IRS figures and the state revenue department. US federal only; figures change yearly."
domains: family-advisor financial-planner
rules:
  - content(estate tax)
  - content(inheritance tax)
  - content(Form 706)
  - content(final return)
  - match((?i)final (tax )?return)
  - content(executor taxes)
---

## Overview

A grieving executor asks whether the estate owes tax and what has to be filed. This skill gives the orientation the agent can verify, so the next step is a plain-words question to the right professional, not a dead end. It is orientation, not tax or legal advice, and it covers US federal rules only.

## Mental model

Three separate filings can exist after a death, each with its own deadline: the dead person's last personal income tax return, the estate's own income tax return, and, only for large estates or to pass a spouse's unused exemption, the estate tax return. Most modest estates owe no federal estate tax. Name which of the three applies before saying anything about money.

## Rules

Federal figures (look up the current year at irs.gov before stating them)

| Item | Fact | Source |
|------|------|--------|
| Estate tax exclusion for deaths in 2026 | $15,000,000 per person (basic exclusion amount, as of 2026-11); look up the current figure | IRS, Form 706 instructions (Rev. July 2026) |
| Estate tax return (Form 706) due | Nine months after the date of death; Form 4768 gives a six-month extension to file (15 months in total) | IRS |
| Who must file Form 706 | Gross estate plus adjusted taxable gifts above $15,000,000 for 2026 deaths, or an executor electing to transfer the unused exclusion of a deceased spouse to the surviving spouse (portability), whatever the estate size | IRS |
| Final personal income tax return (Form 1040) | The personal representative files it for income earned up to the date of death; Form 1310 is needed to claim a refund unless a court-appointed representative attaches the court certificate | IRS, Publication 559 |
| Estate income tax return (Form 1041) | Required when the estate has gross income of $600 or more; covers income earned after death | IRS, Publication 559 |
| Notice of the representative's role | Form 56 tells the IRS a fiduciary relationship exists or has ended | IRS |

Some states have their own estate or inheritance tax with lower thresholds than the federal one; the state revenue department's page names it. Outside the US, use the country's tax authority.

Who to hand it to

- A probate or estate-planning attorney for the court process, the estate tax return and any dispute.
- A CPA or enrolled agent who prepares estate and trust returns, for Forms 1040 and 1041.
- Plain words for the user: "I'm the executor of an estate. The person died on [date], my state is [state]. Do I need to file Form 706, a final 1040, and a Form 1041? What are the deadlines?"

## Examples

Bad: "Estate tax orientation is a question for a tax specialist."
Good: "For a death in 2026 the federal estate tax only applies above $15,000,000, and the return is due nine months after the death. Most estates still need a final personal tax return and possibly an estate income tax return. Ask a CPA or an estate attorney in your state; here is the sentence to bring."

## Checklist

- [ ] The three filings named and which one applies asked.
- [ ] Every figure labeled with its year and source; the user told to confirm on irs.gov.
- [ ] State-level tax flagged for the user to check.
- [ ] A named professional type and a written question handed over.

## References

- Instructions for Form 706: https://www.irs.gov/instructions/i706
- Estate tax: https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax
- Publication 559, Survivors, Executors, and Administrators: https://www.irs.gov/publications/p559
- Deceased person: https://www.irs.gov/individuals/deceased-person
