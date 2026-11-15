---
name: coach-hiring-rules
title: "Pay Transparency Laws: Salary Ranges & AI Screening"
description: "Pay-range posting laws and AI-screening rights by US state and EU, in one dated table. Use for questions on posted salary ranges or AI hiring tools."
license: Apache-2.0
compatibility: "No external tools required. A web search tool is needed to confirm current law on the state or EU source."
domains: coach
rules:
  - match((?i)\bpay\s+(range|transparency)\b)
  - match((?i)\bsalary\s+(range|history)\b)
  - match((?i)\b(AI|automated)\s+(interview|screening|hiring|resume)\b)
  - match((?i)\bbias\s+audit\b)
  - match((?i)\b(current|previous|past|prior) (salary|pay|compensation)\b)
  - match((?i)\bhow much (do|did) (you|they) (make|pay)\b)
  - semantic(is the employer required to post the salary range)
  - semantic(what are my rights when AI screens my job application)
---

## Overview

Two sets of rules change what a candidate can ask and expect: laws that make employers show a pay range, and laws that regulate software that screens or ranks applicants. Both differ by state and country and change every year. This skill holds them in one dated table so the career, negotiation and interview coaches, and the `ats-optimization` skill, point to one place instead of each carrying a copy.

It is information, not legal advice. A dispute with an employer, or a question about whether a law applies to a specific job, goes to an employment lawyer.

## Mental model

- A posting law answers "what must the employer show before I apply or interview". It gives the candidate a number to anchor on and a way to check whether an offer is out of line with the range.
- A screening law answers "what must the employer tell me, and what can I ask for, when software judges me". It rarely lets a candidate reject the software; it gives notice, audit, consent or deletion rights.
- Where the job sits (or where a remote job reports to) decides which law applies, not where the candidate lives.
- The table below is a snapshot dated 2026-11. Confirm the row on the state's labor agency or the EU source before relying on it.

## Rules

### Pay-range posting, United States (snapshot as of 2026-09)

A posting is a public or internal job advertisement. Thresholds are the number of employees the employer needs for the law to apply. Compiled from the sixfifty state tracker (updated 2026-09), Cooley (2026-07-06) and Jackson Lewis (2026-07-15); the state's own page is the authority. The thresholds for Washington, New York, Minnesota, Maryland, California, Delaware, Hawaii, the District of Columbia and Maine, and the Minnesota, Hawaii, Delaware and California dates, were read on official state pages on 2026-11-15; the other rows, and the Maine date, rest on the trackers and still need the state check.

| Jurisdiction | In force from | Employer threshold |
|---|---|---|
| Colorado | in force | at least 1 employee in the state |
| California | in force; SB 642 changes from 2026-01-01 | 15 or more employees |
| Washington | in force (RCW 49.58.110); a 2025 amendment lets an employer that offers one fixed wage post that amount, and gives a five-business-day cure period for postings from 2025-07-27 to 2027-07-27 | 15 or more employees |
| New York | in force | 4 or more employees |
| Hawaii | 2024-01-01 (Act 203 of 2023) | 50 or more employees |
| District of Columbia | 2024 | at least 1 employee |
| Maryland | 2024-10-01 | none stated in the statute (Labor and Employment section 3-304.2) |
| Illinois | 2025-01-01 | 15 or more employees |
| Minnesota | 2025-01-01 | 30 or more employees |
| New Jersey | 2025-06-01 | 10 or more employees |
| Vermont | 2025-07-01 | 5 or more employees |
| Massachusetts | 2025-10-29 | 25 or more employees |
| Virginia | 2026-07-01 | all employers |
| Maine | 2026-07-29 | 10 or more employees |
| Connecticut | 2026-10-01 | all employers |
| Delaware | 2027-09-26 | more than 25 employees |

Counts of states differ between trackers (13 to 18) because they count cities, thresholds and effective dates differently; use the table or the state page, not a headline number. Some cities add their own rules. Without a web tool, tell the candidate the table is a snapshot and to open the state labor department page.

### Pay transparency, European Union

- Directive (EU) 2023/970 gives candidates the starting pay or range, either in the job advertisement or before the first interview, and bars asking about pay history in earlier jobs. Member states had to turn it into national law by 7 June 2026 (European Commission, as of 2026-11).
- Most member states missed that date: one analysis dated 2026-07-02 counted four of 27 in compliance. The candidate's rights come from the national law of the country where the job is, so check that country's status on a current tracker before saying a right applies.
- Where a country has not yet passed its law, suggest asking for the range anyway; whether the candidate can enforce it is a question for an employment lawyer.

### Salary-history questions

Many US states and the EU directive restrict asking about past pay. A candidate can decline and redirect: "I'd rather focus on what this role is worth; the range I'm targeting is X to Y." Confirm the rule for the job's state; where no ban exists, declining is still allowed, only the employer's response differs.

### Automated screening, United States

| Rule | What it requires | Source |
|---|---|---|
| NYC Local Law 144 | The tool must have had a bias audit within one year before use, with results public, and candidates get notice 10 business days before use. Enforced since 2023-07-05 | NYC Department of Consumer and Worker Protection |
| California civil-rights regulations on automated-decision systems | Amend the state's employment discrimination rules (FEHA) to cover automated-decision systems; in force since 2025-10-01 | California Civil Rights Council |
| Illinois HB 3773 (Public Act 103-0804) | Amends the Human Rights Act: AI in employment decisions must not discriminate on protected characteristics, and employers must notify employees and applicants when they use AI in recruitment, hiring and similar decisions; in force since 2026-01-01. The state agency's notice rules were not final as of 2026-11; check the Illinois Department of Human Rights | Illinois General Assembly |
| Illinois AI Video Interview Act | Before an AI-analyzed video interview the employer must give notice, explain how the AI works, and get consent; on request it must delete the video within 30 days. In force since 2020-01-01 | 820 ILCS 42 |
| Colorado | The 2024 AI Act was repealed and replaced by SB 26-189 (signed 2026-05-14), narrower, centered on consumer transparency and rights, effective 2027-01-01. A federal court case over enforcement was open as of 2026-08; check status | Colorado General Assembly |

### Automated screening, European Union

- GDPR Article 22 limits decisions based solely on automated processing.
- The AI Act classes AI used for recruiting and selection as high risk. Regulation (EU) 2026/1744 (the Digital Omnibus on AI; Official Journal 2026-07-24, in force 2026-07-27) moves the stand-alone high-risk duties to 2027-12-02.

### How to use this with a candidate

1. Ask where the job is based and whether it is remote.
2. Look up the row. If it applies, tell the candidate what they can ask: the range before applying, notice of automated tools, the audit or consent the row names.
3. If there is no web tool, give the table's row with its date and say it needs checking.
4. A suspected violation, retaliation or discrimination goes to an employment lawyer or the state agency, in plain words, not to the coach.

## Examples

Candidate: "The posting has no salary. Is that legal?"

- Weak: "Many states require ranges, so it is probably illegal."
- Good: "It depends on where the job is based. In Colorado, Washington and Illinois (15 or more employees) a posting must show a range; in Texas the table has no rule. Which state is the job in? If it is covered, you can ask the recruiter for the range in writing."

Candidate: "A company asked me to record an AI video interview."

- Good: "In Illinois the employer must tell you first, explain how it works, and get your consent, and you can ask for deletion within 30 days. Ask for those in an email. Elsewhere the right depends on state law."

## Checklist

- [ ] The job's location (not the candidate's) was used to pick the row.
- [ ] Every figure quoted carries the table's date or a live source.
- [ ] The answer says "snapshot, confirm on the state or EU source" when no web check was done.
- [ ] Legal disputes were sent to an employment lawyer.

## References

- [Cooley: new state pay transparency laws, 2026-07-06](https://www.cooley.com/news/insight/2026/2026-07-06-show-me-the-money-or-the-wage-range-new-state-pay-transparency-laws)
- [Jackson Lewis: midyear pay transparency update, 2026-07-15](https://www.jacksonlewis.com/insights/midyear-pay-transparency-update-job-postings-lead-employer-responsibilities)
- [sixfifty: pay transparency laws by state](https://www.sixfifty.com/resource-library/pay-transparency-laws-by-state/)
- [Directive (EU) 2023/970 on EUR-Lex](https://eur-lex.europa.eu/eli/dir/2023/970/oj)
- [NYC DCWP: automated employment decision tools](https://www.nyc.gov/site/dca/about/automated-employment-decision-tools.page)
- [Illinois AI Video Interview Act, 820 ILCS 42](https://www.ilga.gov/legislation/ilcs/documents/082000420K5.htm)
- [Davis Polk on the Colorado repeal and replacement (2026)](https://www.davispolk.com/insights/client-update/colorado-repeals-and-replaces-landmark-ai-act-publishes-draft-rules-public)
- [Digital Omnibus on AI in force (Lewis Silkin, 2026-07-27)](https://www.lewissilkin.com/en/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo)
