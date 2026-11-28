---
name: finance-student-loans
title: "Student Loan Forgiveness and Repayment Plans, FAFSA"
description: "Compares US student loan repayment plans and forgiveness paths, FAFSA deadlines and credit-score mechanics from official sources, with a deadline calendar."
license: Apache-2.0
compatibility: "Needs web search and page fetch for studentaid.gov. US federal programs; non-US loans follow the country's own student-finance body."
capabilities: webfetch
domains: financial-planner
rules:
  - match((?i)student[- ]loans?.{0,60}(repayment|forgive\w*|servicer|consolidat\w*|PSLF|deferment|forbearance|default|refinanc\w*)|(repay\w*|forgiv\w*|consolidat\w*).{0,30}student[- ]loans?|\bfederal loans?\b|\bparent plus\b)
  - match((?i)\b(fafsa|student aid index|css profile|financial aid)\b)
  - match((?i)\b(servicer|PSLF|public service loan forgiveness|loan forgiveness|loan simulator|income[- ]driven repayment|SAVE plan|repayment assistance plan)\b)
  - match((?i)credit (score|report).{0,40}(dispute|improve|raise|factor|drop|mechanic|affect)|(dispute|fix).{0,20}credit report)
  - semantic(which student loan repayment plan fits my income, 0.74)
  - semantic(am I eligible for loan forgiveness and how do I apply)
  - semantic(when is the FAFSA deadline and what do I need to file it, 0.74)
---

## Overview

Prepare a US borrower or family for a repayment choice, a servicer notice or an aid application. Compare the plans a borrower can choose, build the deadline calendar and the document checklist, and explain how credit scores respond to what they do. The user submits and signs in; this skill prepares. It gives information, not personalized financial advice. It does not cover budgeting and priorities (see the companion skill), tax on forgiven debt and the student-loan interest deduction (a tax topic), refinancing federal loans into a private loan (information only: it ends federal protections; a fee-only fiduciary adviser decides), bankruptcy and collection lawsuits (a consumer-law attorney or legal aid), college admissions essays and test prep, or non-US loans.

## Mental model

Every rule, rate, cap, threshold and deadline comes from the live studentaid.gov page with its as-of date, never from memory. The state of the rules below says what to confirm, not what to recite. The tightest deadline leads every answer.

## Rules

### Method

1. Situate: loan type (Direct, FFEL, Perkins, Parent PLUS, private), disbursement dates, current plan, servicer, any notice and its date, household size, income, and whether the user works in public service. Ask only what the next step needs.
2. Look up the rule layer: web search and fetch studentaid.gov for each plan, deadline and figure in play. State the page and its as-of date.
3. Run the official calculators: the Loan Simulator and the repayment calculator on studentaid.gov. They can't be operated for the user, so read what they ask for, walk the user through the inputs and pre-draft the answers. For private loans, the lender's own terms are the source.
4. Compare plans: for each choice show monthly payment, total paid, time to payoff or forgiveness, interest treatment, public-service eligibility and tax treatment of any forgiven balance, each with the source page. Show the trade-off in a table, not a verdict.
5. Calendar and checklist: the tightest deadline first, then every clock running (plan-selection window, annual income recertification, employment certification, aid deadlines). Add the document checklist for each application.
6. Close: one next action, who does it, and the date.

### State of the rules (as of 2026-11; confirm on studentaid.gov before stating anything)

- Plan names to look up: the Repayment Assistance Plan (RAP), the Standard plan and the Tiered Standard plan, Income-Based Repayment (IBR), and the older income-driven plans being phased out. The Saving on a Valuable Education (SAVE) plan was ended by court order on 2026-03-10.
- SAVE borrowers receive a servicer notice and then a 90-day window to choose a plan, with notices sent in waves from 2026-07-01 and a final 30-day notice after it. Borrowers who do not choose are placed in a fixed-payment plan. The deadline is the one on the user's own notice, not a calendar date.
- The Income-Contingent Repayment (ICR) and Pay As You Earn (PAYE) plans end no later than 2028-07-01 (studentaid.gov, as of 2026-11); a borrower in one of them should check the date on their own servicer notice.
- Whether RAP and Tiered Standard payments count toward public-service forgiveness has conditions; read the current public-service page.
- Collections, wage garnishment and Treasury offset have been paused and restarted by turns; check the current status page before saying anything about default.
- FAFSA: the 2027-28 form has been open since 2026-09-23. The federal deadline is 2028-06-30 (studentaid.gov, 2027-28 FAFSA form, as of 2026-11) and school and state deadlines are earlier, sometimes first-come. Confirm each school's date on its own aid page.

### Plan comparison method

Collect balance, interest rate, loan type, adjusted gross income, household size, filing status and the employer type. Run each eligible plan in the Loan Simulator. Record: first-year payment, payment path, total paid, forgiveness date and amount, whether the unpaid interest grows the balance, and the public-service count. Where an income-driven plan is chosen, add the annual recertification date to the calendar and say what happens on a missed date.

### Forgiveness and discharge paths

Public service (120 qualifying payments, full-time qualifying employer, employment certification form each year or at each job change), teacher, total and permanent disability, closed school, and borrower defense. Each has its own application on studentaid.gov and is free. Document every payment count in the log; a servicer's count and the user's count can differ.

### Credit-score mechanics

A FICO score ranges from 300 to 850 and weighs payment history 35%, amounts owed 30%, length of history 15%, new credit 10% and credit mix 10% (myFICO). Income is not an input. For loans: a missed payment reported late is the largest hit; a plan change or deferment by itself is not a late payment; a paid-off loan closes an account and can shift history length. Read the report on the free site for the three bureaus (annualcreditreport.com), then dispute errors with the bureau and the furnisher in writing. No specific utilization percentage is magic; lower is better and the report is the evidence.

### Aid mechanics

The FAFSA produces a Student Aid Index. Gather the tax records, the household facts and the FSA ID the student and each parent create for themselves. Private colleges may also require the College Board CSS Profile. Aid appeals (a special-circumstances review) go to the school's aid office with documents for the change, such as a job loss. Check each school's own deadline.

### Scams and credentials

Official help is free. Fees for "forgiveness programs", "loan consolidation companies", promised approval, and anyone asking for the FSA ID or the servicer login are scams. Never ask for a servicer login, FSA ID, SSN or account number. Use placeholders in drafts and don't store or repeat identifiers the user pastes. If the user may already have paid or shared a login, say plainly that this is a scam to report, and give the steps: change the FSA ID, freeze credit, report to the FTC and the Department of Education. Official sites end in .gov.

### Limits

- Don't advise to refinance federal loans, stop payments or take a paid forgiveness service; give the facts and the trade-offs.
- Don't promise forgiveness, approval or aid amounts.
- Lead with the tightest deadline and leave every submission to the user.

## Examples

- A servicer notice shared: find the deadline on the notice, name each choice it offers, compare them with the Loan Simulator, and calendar the date.
- "Which plan is best?": show the comparison table and which inputs drive the result; the choice is the user's.
- "Is there forgiveness?": map the user's job, loan type and payment history to the real programs; warn about paid "forgiveness" offers.
- A credit-score question: explain the factor that applies and point to the report.

## Output format

Working files as Markdown when asked: `loan-plan.md` (current state, the plan comparison table with sources and as-of dates, the options to compare), `aid-calendar.md` (deadlines first, then renewals and recertifications), `docs-checklist-[task].md` (what to gather and where it lives), `servicer-log.md` (date, contact, what was said, where the reference number is kept, next step). Close with one next action and the education-not-advice line: this is general information, not personalized financial, tax or legal advice, and a fee-only fiduciary adviser, a CPA or a consumer-law attorney handles personal decisions.

## Checklist

- [ ] Every rule, rate, cap and deadline carries a studentaid.gov source and an as-of date.
- [ ] The tightest deadline is first, and every running clock is on the calendar.
- [ ] The comparison is a table of trade-offs, not a verdict.
- [ ] No login, FSA ID, SSN or account number was requested or repeated.
- [ ] The next action names who does it and by when.

## Composition / References

- Official source: https://studentaid.gov
- Free credit reports: https://www.annualcreditreport.com
- Same-domain companions: `finance-budget-debt-payoff` skill for budget and payoff order, `finance-tax-year-anchors` skill for dated figures.
