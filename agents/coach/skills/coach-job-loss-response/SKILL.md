---
name: coach-job-loss-response
title: "Job Loss Response: Severance, Deadlines, First 30 Days"
description: "Employee-side plan after a layoff: severance agreement review points, release deadlines, final pay, health cover, unemployment timing, first 30 days."
license: Apache-2.0
compatibility: "No external tools required. US rules are given with sources; a web search tool helps confirm state rules."
rules:
  - match((?i)\b(laid off|layoff|let go|redundan\w+|made redundant)\b)
  - match((?i)\bseverance\b)
  - match((?i)\b(fired|terminated|lost my job|job loss)\b)
  - match((?i)\b(release|separation)\s+agreement\b)
  - semantic(I was just laid off what should I do first)
  - semantic(should I sign this severance agreement)
---

## Overview

A layoff starts several clocks at once: the time to sign a release, the time to elect health cover, the time to claim unemployment benefits, and the time to exercise stock options. Most people are told about none of them in the room. This skill gives the employee side in a fixed order: what to ask before signing anything, which deadlines run, and what to do in the first 30 days.

It is general information, not legal advice. It rules on nothing about one person's contract. Questions about whether a release is fair, discrimination, retaliation, a non-compete or an immigration status need an employment lawyer; the benefits and unemployment paperwork after the first days is a separate task. Say that in plain words when the question reaches that point. This skill is US-first; outside the US it supplies the question list only and the person looks up their country's rules.

## Mental model

- Nothing has to be signed in the meeting. A release is a contract: the employer offers money, the employee gives up claims. Time to read it is part of the deal.
- Deadlines come from three sources: the federal law, the state law, and the paperwork the employer hands over. The paperwork date is the one people miss.
- The first week is for stopping damage (deadlines, cover, cash). Job search starts after, not instead.

## Rules

### Before signing anything

1. Ask for the separation or release agreement and every plan document in writing, and ask when it must be signed.
2. Do not sign in the meeting. A release that waives age-discrimination claims for workers aged 40 or older is valid only if the employer follows the Older Workers Benefit Protection Act (OWBPA): written in plain language, names the Age Discrimination in Employment Act, advises consulting an attorney, gives at least 21 days to decide (45 days in a group layoff, with a written list of the job titles and ages of the people selected and not selected) and 7 days after signing to revoke, and pays something beyond what the employee already earned. A material change to the offer restarts the clock unless both sides agree otherwise in writing. Source: EEOC; 29 CFR 1625.22.
3. For a person under 40, ask what deadline the agreement itself sets, and ask for an extension in writing if it is short.

### Severance review points

| Point | Question to put to the employer or the lawyer |
|---|---|
| Money | Amount, weeks of pay, lump sum or installments, and what stops the installments (a new job? a breach claim?) |
| Release scope | Which claims are waived, and does it cover claims the employee does not yet know about |
| Final pay | Last day of pay, accrued vacation or PTO payout, unpaid expenses, bonus or commission earned but not yet paid; state law sets the due date |
| Health | Months of employer-paid premium, if any; the date coverage ends |
| Equity | What happens to vested and unvested stock options and RSUs, and the exercise window after the last day |
| Non-compete and non-solicit | Whether they apply, how long, where; whether the employer will waive or narrow them |
| Reference | The neutral reference the employer will give: dates and title only, or more; who to call |
| Unemployment | Whether the employer contests a claim; whether the agreement says anything about it |
| Mutual terms | Non-disparagement that binds both sides; agreed wording for the departure announcement |
| Return of property and confidentiality | What must be returned, by when, and what the employee may keep (contacts, samples of own work) |

Negotiating is normal: more weeks, a longer health-cover period, and an extension to the exercise window are the usual asks. Preparing the script is negotiation coaching; the contract wording is for a lawyer.

### Deadlines to put in the calendar on day 1

| Clock | Rule | Source |
|---|---|---|
| Release | 21 days (45 in a group layoff) to decide, 7 days to revoke, for age 40 and over | EEOC |
| Layoff notice | The federal WARN Act requires employers with 100 or more employees to give 60 calendar days' written notice before a plant closing or a mass layoff of 50 or more at one site. Some states have their own laws | US Department of Labor |
| COBRA election | 60 days, starting when job-based coverage ends or when the election notice is received, whichever is later; coverage usually lasts up to 18 months; the person pays the full premium, up to 102% of the plan cost; applies to group plans of employers with 20 or more employees | US Department of Labor |
| Marketplace coverage | 60 days after losing job-based coverage to enroll. Outside open enrollment, dropping COBRA voluntarily does not open a new window | HealthCare.gov |
| Stock options | The plan sets the exercise window. Incentive stock options generally keep that tax treatment only if exercised within three months of leaving; later exercise turns them into non-qualified options. Confirm the plan's number in writing | Plan documents; tax advisor |
| Unemployment claim | Set by the state agency; ask it on day 1 whether severance changes when benefits start and whether the claim can open before the last day | State agency |

COBRA versus the marketplace is a cost comparison, not a rule: price both before the 60 days run out. Subsidy on the marketplace depends on household income and size, not on employment status.

### First 30 days, in order

1. Day 1-2: write down what was said and by whom; get the paperwork and plan documents; save personal files and contacts the employer allows; do not sign.
2. Day 1-3: open the unemployment claim or ask the state agency when to; ask HR for the written benefits end date.
3. Week 1: calendar every deadline in the table above; list monthly costs and the number of months of cash; pause nonessential spending.
4. Week 1-2: decide on health cover (COBRA or marketplace) and, if the agreement is significant, have a lawyer read it before the release deadline.
5. Week 2: negotiate the terms that can move; ask for a reference agreement; settle the equity exercise decision with a tax advisor.
6. Week 2-4: update resume and the target list (career coaching for direction, resume tailoring for the document, interview practice for the rounds); tell the network in a message that names the role wanted.
7. Day 30: review cash runway, claim status and applications; set the next 30-day target.

### Handoffs, said plainly

- A question about whether a clause is enforceable, a suspected discrimination or retaliation case, a non-compete dispute, or a visa that depends on the job: that is for an employment lawyer.
- Filing benefit paperwork, food or housing help, and tracking appeal deadlines after the first days: that is a separate benefits-paperwork task, not covered here.
- Distress, panic or hopelessness after the news: acknowledge it, then offer wellbeing support; any crisis or self-harm signal goes to emergency services or a crisis line (US: 988).

### Non-competes

The federal non-compete rule is not in effect: a court set it aside, and the Federal Trade Commission dropped its appeals on 2025-09-05 and now acts case by case. State law decides whether a non-compete binds, and states differ widely. Do not tell the person a non-compete is void or valid; give the question list and send the contract reading to the lawyer.

## Examples

Weak: "You should sign it, severance is generous."

Good: "Don't sign today. You are 52, so the law gives you at least 21 days to decide, or 45 if this is a group layoff, and 7 days to change your mind after you sign. Write the date you received it on the calendar and ask HR for the list of ages and job titles in the layoff group. Meanwhile, two clocks matter more: your health cover runs out on the date in your benefits letter, and you have 60 days to elect COBRA or enroll in a marketplace plan. Whether the release is fair is a lawyer's question; I can prepare the questions to ask."

## Checklist

- [ ] The person has not signed in the meeting and has the written deadline.
- [ ] Age 40 or over was asked, and the OWBPA clocks were given if so.
- [ ] Every row in the deadline table is on a calendar with a date.
- [ ] Health cover was priced both ways before the 60 days end.
- [ ] Contract or discrimination questions were sent to the lawyer domain in plain words.
- [ ] The first 30 days have an order with dates, not a list of ideas.

## References

- [EEOC: waivers of discrimination claims in employee severance agreements](https://www.eeoc.gov/laws/guidance/qa-understanding-waivers-discrimination-claims-employee-severance-agreements)
- [US Department of Labor: plant closings and layoffs (WARN)](https://www.dol.gov/general/topic/termination/plantclosings)
- [US Department of Labor: COBRA](https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/cobra)
- [HealthCare.gov: coverage options after losing a job](https://www.healthcare.gov/unemployed/coverage/)
- [HealthCare.gov: switching from COBRA to the Marketplace](https://www.healthcare.gov/unemployed/cobra-coverage/)
- [Antitrust analysis: FTC drops its non-compete rule appeals, 2025-09-05 (Weil)](https://antitrust.weil.com/client-alert-ftc-walks-away-from-rulemaking-but-not-the-fight-on-non-competes)
- `coach-hiring-rules` skill for pay-range and screening laws
