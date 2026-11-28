---
name: finance-budget-debt-payoff
title: "Snowball vs Avalanche: Debt Payoff Plan and Budget"
description: "Builds a household budget, debt payoff order and emergency fund from the user's numbers, using 50/30/20, snowball vs avalanche and a named priority order."
license: Apache-2.0
compatibility: "Needs web search for current rates and limits."
rules:
  - match((?i)\b(budget|budgeting)\b.{0,40}(plan|build|set up|create|help|fix|zero[- ]based|stick)|\b(make|build|create|set up) (me )?a budget\b)
  - match((?i)(pay(ing)? off|payoff|get out of|pay (things|it|them) off).{0,40}(debts?|credit cards?|card balances?|cards?|order))
  - match((?i)\b(snowball|avalanche)\b.{0,40}(debt|method|payoff)|\bdebt (snowball|avalanche)\b|\bdebt payoff\b)
  - match((?i)emergency (fund|savings)|\b50/30/20\b|\b(next|each additional) dollar\b|\bsinking funds?\b|\bstarter fund\b)
  - match((?i)\b(order of (operations|priorities)|financial priorities|money priorities|priority ladder)\b)
  - match((?i)\b(fire|financial independence)\b.{0,60}(math|years|savings rate|timeline|number)|savings rate.{0,60}(fire|financial independence|stop working|early retirement))
  - match((?i)(paycheck|take[- ]home).{0,60}(disappears|where (it|the money) goes|budget)|\b(paralyzed|overwhelmed)\b.{0,40}debt|tracking method)
  - semantic(build a monthly budget from my income and expenses, 0.74)
  - semantic(which debt should I pay off first, snowball or avalanche)
  - semantic(how big should my emergency fund be and how do I start it, 0.74)
---

## Overview

Turn money anxiety into a sequenced plan: what to do with the next dollar. The skill covers budgeting, debt-payoff strategy, emergency funds, saving, the order of operations, and savings-rate and FIRE math, using established frameworks instead of guilt or generic "spend less" advice. It is household money behavior. It does not pick securities, funds or brokerages, and it does not take filing positions or give legal or estate advice; those go to a fee-only fiduciary CFP, a CPA or an attorney. Student-loan repayment plans, college aid and credit-score mechanics are a separate topic: keep the budget and the payoff order here.

## Mental model

Every dollar has one best next job, decided by a named order of operations. Meet people where they are: when essentials exceed income, the lever is income or assistance, not willpower. Housing, transport and debt are where the money is.

## Rules

### Method

1. Intake: gather monthly take-home pay, essential vs discretionary expenses, each debt with balance, APR and minimum, current cash savings, retirement contributions and employer match, income stability, and dependents.
2. Triage: locate the user on the named order of operations and identify the single most pressing gap (no buffer, unmatched 401k, crushing-APR debt).
3. Budget frame: apply 50/30/20 as a quick sanity check, or zero-based / YNAB for line-item control. Build sinking funds for irregular bills.
4. Debt plan: if high-interest debt exists, pick snowball vs avalanche with the user. Set the target and the extra payment. Keep minimums on the rest.
5. Safety net: size the emergency fund (starter $1,000 first, then 3-6 months of essentials in a high-yield savings account) and slot it correctly.
6. Growth: once debt and buffer are handled, layer retirement (match, then IRA/HSA, then max) and, if relevant, savings-rate and FIRE math.
7. Close: one concrete next action plus the education-not-advice line.

Use web search for current rates and rules. Use memory to carry the plan between sessions.

### Frameworks

| Framework | Originator | Core mechanic |
|-----------|------------|---------------|
| 50/30/20 | Warren & Tyagi | After-tax pay: 50% needs, 30% wants, 20% savings + extra debt; adapt for high cost-of-living |
| Zero-based / YNAB | Jesse Mecham | Give every dollar a job; embrace true (irregular) expenses via sinking funds; age your money |
| Avalanche vs snowball | math-optimal vs Ramsey | Avalanche (highest APR) saves the most interest; snowball (smallest balance) wins on completion; pick by psychology |
| Emergency fund | personal-finance consensus | 3-6 months of essentials in a HYSA; starter $1,000 first; full fund after high-interest debt |
| Order of operations | r/PF flowchart; Money Guy | Budget + starter EF, then full 401k match, then high-interest debt, then full EF, then IRA/HSA, then max retirement (Ramsey's Baby Steps differ: pause all investing, including the match, until non-mortgage debt is gone) |
| Savings rate / FIRE | Mr. Money Mustache; Bengen | Time to FI tracks savings rate; FIRE number is about 25x expenses; the 4% rule is a heuristic, not a guarantee |

### Limits and special cases

- Capture the full employer 401k match before extra debt payments unless the debt is at a crushing rate: the match is a guaranteed return otherwise thrown away.
- Contribution limits and catch-ups change every year: take them from the `finance-tax-year-anchors` skill, quote the tax year with each figure, and look up a year the skill does not list on irs.gov.
- Children born 2025-2028 who are US citizens with an SSN can get a one-time $1,000 Treasury deposit into a "Trump account" when a parent elects it on IRS Form 4547. That is free money worth claiming. Further contributions (up to $5,000 a year) rank below the parent's own match, debt payoff and emergency fund.
- The Latte Factor is debunked. Don't lead with "cut the daily latte".
- Don't shame or moralize about poverty: a budget can't fix insufficient income.
- Don't quote the 4% rule or FIRE timelines as guarantees.
- In a crisis (eviction, utility shutoff, unmanageable debt), nonprofit help exists: NFCC.org for nonprofit credit counseling, 211.org for local assistance, and the state attorney general's consumer-protection office for collector or lender abuse.

## Examples

- "I have no idea where to start": put them on the flowchart and give one next step.
- "Should I skip the 401k match to pay low-rate debt?": no; grab the match first.
- "There's nothing left to cut": acknowledge the income lever and assistance options; don't shame.

## Output format

- Snapshot: income, essentials, debts with APRs, savings.
- Where you are: the order-of-operations step and the single most pressing gap.
- Budget: the method and the freed-up cash flow.
- Debt and safety net: the target, the method and the emergency-fund size.
- Next action: one concrete step, plus the guardrail.

Save to `money-plan.md` in the working directory when asked.

## Checklist

- [ ] The plan starts from the user's actual numbers.
- [ ] It is anchored to a named order of operations and names one next action.
- [ ] The employer match is placed ahead of low-rate debt.
- [ ] Every limit or rate is dated and sourced.
- [ ] The education-not-advice note and, where relevant, crisis resources are present.

## Composition / References

- Same-domain companions: `finance-tax-year-anchors` skill for contribution limits, `finance-retirement-planning` skill for retirement math.
