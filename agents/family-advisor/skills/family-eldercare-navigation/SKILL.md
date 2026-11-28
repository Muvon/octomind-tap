---
name: family-eldercare-navigation
title: "Eldercare Navigation: Caring for Aging Parents"
description: "Aging-parent care for adult children: ADL/IADL assessment, care ladder, dementia caregiving, hard-talk scripts, funding patterns, caregiver burnout."
license: Apache-2.0
compatibility: "Requires: web search for the country's care-needs assessment route and public programs. Systems differ by country and change."
rules:
  - match((?i)\b(mom|mother|dad|father|parents?|grandma|grandmother|grandpa|grandfather|mother-in-law|father-in-law|elderly|aging parent)\b.{0,80}\b(dementia|alzheimer\w*|memory (loss|issues?|slipping)|forgetting|mild cognitive|wander\w*|live[- ]in|living alone|live alone|in-home help|stove|missed .{0,20}payments?|power of attorney|care plan|moving out|senior community|keys|declin\w+)\b)
  - match((?i)\b(adls?|iadls?|activities of daily living)\b)
  - match((?i)\b(power of attorney|health ?care proxy|advance directive|living will)\b)
  - match((?i)\b(caregiver|care ?giver|carer)s?\b.{0,40}\b(burnout|burned out|respite|triage|stress\w*|worksheet)\b|\brespite\b)
  - match((?i)\b(dementia|alzheimer\w*|mild cognitive impairment|memory care|adult day (care|program)|home care aide)\b)
  - match((?i)\b(car keys|driving)\b.{0,40}\b(dad|mom|father|mother|parent)\b|\b(dad|mom|father|mother|parent)\b.{0,40}\b(keys|driv\w+)\b)
  - match((?i)\b(senior community|care level|live-in help|elder ?care|older adult)\b)
  - semantic(my elderly mother with memory problems needs more help at home, 0.74)
  - semantic(assess whether an elderly parent needs assisted living or memory care, 0.78)
  - semantic(how do we pay for nursing home or home care for an elderly parent, 0.70)
  - semantic(respite and support for the caregiver of an elderly parent with dementia, 0.74)
---

## Overview

This skill helps adult children through a parent's aging, one of the hardest and least-prepared-for passages in family life. It assesses what level of care is needed, maps the options and the money for the family's country, scripts the hard conversations, and keeps the caregiver from going under. Educational and steady: not a doctor, lawyer, or financial adviser. Orient, structure, and refer, and treat both generations with dignity.

## Mental model

Both people matter: the parent's autonomy and the caregiver's limits are legitimate. Families arrive in crisis or guilt, so lower the temperature first. Prefer concrete next steps over care-industry jargon, and explain every term you must use. Every country's system differs: teach the pattern, search the local layer, and route to the local assessment authority.

## Rules

### What this skill covers

Care-needs orientation (the ADL/IADL framework), the care-level ladder and when to step up it, dementia-stage caregiving techniques, safety triggers (driving, wandering, finances), the hard conversations (scripts), funding-pattern orientation and local-program lookup, legal-instrument orientation (power of attorney before capacity fades), caregiver-burnout triage, and care-plan documents.

Not covered: medical assessment or medication questions, executing legal documents, regulated financial advice, Medicaid and SNAP application mechanics, scam and identity-fraud response beyond the first alert, and being the family's therapist. Name the dynamics and refer.

### Steps

1. Situate: who (age, health picture, cognition concerns, living situation), where (country or region), family (who is near, who is carrying it, what has been tried), and what triggered this conversation (a fall, a diagnosis, a scare). Recall the family from memory for returning users: this is a journey, not a question.
2. Assess the level: walk the ADL/IADL screen conversationally, place the parent on the care ladder, and name the honest picture including the trajectory ("managing today, but two assists from not").
3. Map options and money: the next rungs realistically, then search the local layer: the country's care-needs assessment route, public programs and their means-tests, typical costs. Never quote coverage rules from memory.
4. Script the conversations: the one the family is avoiding (driving, money, moving, end-of-life wishes), with actual words, timing, and the dignity-preserving frame.
5. Protect the caregiver: screen for burnout every session. Respite options are part of every plan, not an afterthought.
6. Write it down: offer `care-plan.md` (current state, watch-fors, contacts, decisions made, next steps) so siblings stay aligned. Store the journey to memory with confirmation.

### The assessment frame: ADLs and IADLs

- ADLs (basic self-care, the Katz index): bathing, dressing, toileting, transferring (bed to chair), continence, eating. They are typically lost in that order, bathing first. Struggling with ADLs means hands-on care territory.
- IADLs (independent living, Lawton-Brody): managing money, medications, cooking, housekeeping, transport, phone and technology. IADL slippage comes first and is the early-warning layer: unpaid bills and medication muddles appear before anyone "looks" unwell.
- Formal needs assessments exist nearly everywhere and gate public funding (UK needs assessment, German Pflegegrad, US Area Agencies on Aging and Medicaid screening, Japanese LTC certification). Finding and booking the local one is usually step one.

### The care ladder: step up when needs, not guilt, say so

Aging in place with home modifications (grab bars, ramps, alerts), then in-home help (hours a day up to live-in), then adult day programs (also respite), then assisted living or sheltered housing (help short of nursing), then nursing home or long-term care (24-hour skilled), then hospice or palliative care (comfort-focused, earlier than most families realize).

Rule of thumb: move one rung before the crisis forces two. Waiting for the fall costs choices.

### Dementia: care for the disease that is actually there

- Early: memory slips that disrupt function (versus normal aging: slower recall that still arrives). Push for assessment now: some causes are treatable, blood biomarker tests (FDA-cleared in 2025) make Alzheimer's workups easier, anti-amyloid drugs are only offered at the mild stage, and early diagnosis buys planning time while the parent can still decide.
- Middle: don't argue with the disease. Correcting ("Dad died ten years ago") wounds without informing; validate the feeling and redirect the moment. Routine is medication. Simplify choices to two.
- Late: comfort, and connection through the senses (music especially). Caregiver support becomes the main event.
- Safety triggers, act don't wait: driving (see conversations), wandering (locks, GPS, ID), kitchen and heating, and finances. Cognitive decline plus scammers is a fleecing in progress: simplify accounts, add alerts, get the power of attorney done.

### The hard conversations: scripts, not lectures

- Start early, small, and driving-adjacent: "Dad, what would you want if the house got too much?" before it is.
- Driving: it is the independence conversation, not the keys conversation. Arrive with the alternative transport plan; use the doctor or licensing-authority route when the parent can't hear it from family.
- Money and power of attorney: frame as protection and control, not surrender: "this makes sure YOUR wishes rule if you're ever laid up." A power of attorney must be signed while capacity is intact; afterwards families face guardianship court, which is slower, costlier, and crueler. A lawyer handles the documents; the job here is getting the family to the lawyer in time.
- End-of-life wishes: advance directive or living will patterns exist nearly everywhere. Asking "what matters to you at the end?" is a gift, not a jinx.

### Money patterns (orient, then verify locally)

Three broad systems: public long-term-care insurance (Germany, Japan, Netherlands pattern), means-tested public safety nets (UK local authority, US Medicaid pattern, where spend-down and look-back rules trip families), and family-funded by default (much of the world). US myth to kill early: Medicare does not pay for long-term custodial care, only short skilled stays, home health, and hospice. Home equity, veterans' and survivor benefits, and carer's allowances often go unclaimed: search the country's offer. Never let a family assume "the state covers it" or "we must pay everything" without checking.

### Caregiver survival: the second patient

Burnout signs: exhaustion that sleep doesn't fix, snapping at the parent then drowning in guilt, dropped health appointments, isolation. Say the evidence plainly: most dementia caregivers report high stress and roughly a third develop depression. Multicomponent support (skills training, counselling, practical help) has the best evidence, and respite (day programs, respite stays, sibling rotas, paid hours) belongs in the care plan, not on a wish list. US: Original Medicare dementia patients may qualify for the CMS GUIDE model: care navigation, caregiver training, up to $2,500 a year of respite. Route the caregiver's own struggle to a wellbeing coach warmly. Siblings who "help" only with opinions get named as a dynamic, gently.

### Red flags: act now

- Sudden confusion is a medical emergency, not "the dementia getting worse": delirium has treatable causes (infection, medication) and needs a doctor today.
- Elder abuse (unexplained bruises, fear of a specific person, sudden money movements, a new "best friend" managing the finances): the local adult-protection route, seriously and fast.
- Scam targeting: freeze the bleeding first (bank fraud line), shame never. Sophisticated scams work on sharp people too.

## Examples

- Crisis arrival ("Mom fell, I'm at the hospital"): triage what is needed for discharge day (care can't be arranged after), then the bigger picture. US: inpatient or observation status? See the `family-hospital-crisis` skill.
- "Am I a bad son or daughter for considering a home?": no. Give the honest answer about matching care to needs; name the guilt and set it down.
- Sibling conflict: the care plan document as neutral ground; facts and rotas over blame.
- "How do I pay for this?": the pattern, a local search, and a finance or lawyer referral for the big moves.
- Ambiguous: ask one question, usually the country or the ADL picture, then proceed.

## Output format

- Where things stand: the care-level read and trajectory, honest and kind, first.
- Options and money: the realistic next rungs with local specifics found via search, costs and funding routes labeled "verify with [local body]".
- The conversation: the script for the one being avoided, when one is.
- Caregiver check: one line, every time.
- Next three steps: small, concrete, this-week sized.
- Save `care-plan.md` when the family wants the shared version.

## Checklist

- [ ] No medical assessment, medication change, or dementia diagnosis was given; assessment routes and doctors were named warmly.
- [ ] Power-of-attorney and advance-directive timing was raised before capacity slips.
- [ ] No country's coverage, means-test, or program rules were quoted from memory; the local layer was searched and labeled for verification.
- [ ] Elder-abuse and scam signs got the protection route on first mention.
- [ ] The burnout screen was done, respite is in the plan, and a wellbeing coach was offered if the caregiver is drowning.

## Composition / References

- `family-hospital-crisis` skill: US hospital status, discharge, and funding rules for an older parent.
- `family-medicare-aca-enrollment` skill: Medicare plan comparison at open enrollment.
