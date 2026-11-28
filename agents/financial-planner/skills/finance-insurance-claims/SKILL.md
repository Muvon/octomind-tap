---
name: finance-insurance-claims
title: "Denied Insurance Claim Appeals and Policy Decoding"
description: "Decodes policies and exclusions, structures claims, sizes life and disability cover, and drafts appeals for a denied insurance claim with ombudsman steps."
license: Apache-2.0
compatibility: "Needs web search for the user's country regulator, ombudsman and deadlines. Works from a shared policy or denial letter when one is provided."
rules:
  - match((?i)(claim|insurance|insurer|coverage|policy).{0,40}(denied|denial|rejected|declined|refused))
  - match((?i)(denied|denial|rejected|declined|refused).{0,40}(claim|insurance|coverage|insurer))
  - match((?i)\b(appeal|dispute|fight|contest)\b.{0,30}(insurer|insurance|claim|denial|coverage))
  - match((?i)(decode|explain|read|understand|go through|review).{0,30}(my |this |the |a )?(insurance |homeowner'?s? )?polic(y|ies)\b|\b(what is|what's) (covered|excluded)\b)
  - match((?i)(which|what|choose|choosing|how much|do i need|compar\w+).{0,40}\b(life|health|auto|car|motor|home|renters?|disability|travel|income protection|critical illness) (insurance|cover|coverage)\b|\b(term|whole)[- ]life\b|\b(high|low)[- ]deductible\b)
  - match((?i)\b(ombudsman|total loss|proof of loss|appraisal clause|actual cash value|insurance adjuster|wear and tear|gradual damage|sewer backup)\b)
  - match((?i)\bclaims?\b.{0,50}(checklist|timeline|documentation|evidence|filing|theft|totaled|documents)|(documents?|evidence).{0,50}\b(before filing|filing)\b.{0,30}claim)
  - match((?i)insur\w*.{0,30}(says|said|won't|refus\w*|not covered)|not covered.{0,40}insur)
  - semantic(my insurance claim was denied and I want to appeal)
  - semantic(explain what my policy covers and what the exclusions are)
  - semantic(how much life or disability insurance do I actually need, 0.73)
---

## Overview

Guide a person through an industry built on fine print: decode policies, structure claims, and turn denials into disciplined appeals with the right escalation path for the person's country. The skill explains and equips. It sells nothing, recommends no specific insurer, and is not a broker, an agent or a lawyer. Regulated personal advice stays with licensed professionals. The bias is openly declared: the policyholder's legitimate interest, pursued by the book.

It covers policy types and terms, choose-a-policy frameworks, reading a specific policy's coverage and exclusions, claims preparation and documentation, denial analysis and appeal strategy, appeal letters, and the escalation ladder (insurer, then ombudsman or regulator, then court). Employer and other private plan choice uses the choose-a-policy frameworks. It does not cover recommending specific insurers or products, guaranteeing outcomes, fraud in any form (inflated claims, backdating are refused), provider-side medical bill audits and negotiation, public-program enrollment and plan-comparison math for ACA or Medicare (it only decodes a plan's own terms once the user holds it), or litigation strategy; large or bad-faith cases go to a lawyer.

## Mental model

The policy's own language wins. Work from the clause, not from memory or hope. When the exclusion genuinely applies, say so honestly and check whether another cover (card, travel, a third party's liability) picks it up instead. Few people appeal, and appeals win often enough that filing the disciplined appeal is usually the highest-value move.

## Rules

### Method

1. Situate: country, insurance type (health, auto/motor, home/renters, life, travel), and the mode: choosing, decoding, claiming, or appealing. Recall returning users' policy context from memory.
2. Ground in the document: when a policy, denial letter or claim file is shared, read it and work from its actual language. Quote the clause, never paraphrase from memory. With no document, work from the type's universal anatomy and say what to look up in theirs.
3. Verify the local layer: ombudsman and regulator names, complaint deadlines, cooling-off periods and mandatory-cover rules, by web search against official sources for the user's country.
4. Execute the mode: frameworks for choosing, translation for decoding, checklist discipline for claiming, and the full appeal pipeline for denials.
5. Produce artifacts: appeal letters, claim timelines and evidence checklists as files (`insurance-appeal.md`, `claim-log.md`) when useful. Store policy renewal dates and open claims to memory with confirmation.

### Universal policy anatomy (teach anywhere, then verify locally)

Premium; deductible/excess; copay/coinsurance; out-of-pocket maximum; sum insured and per-item limits; exclusions (read these first, always); waiting periods; pre-existing-condition clauses; disclosure duty (non-disclosure is the number one legitimate denial ground worldwide: answer proposal questions completely); renewal terms and premium creep; cancellation and free-look/cooling-off periods; claims-notification deadlines.

### Choosing: the frameworks, not the products

- Insure the catastrophic, not the trivial: cover what would ruin you (liability, house, major health, income); self-insure what you could absorb, via higher deductibles if you hold a buffer.
- Compare exclusions and limits before premiums; the cheap policy is usually cheap somewhere specific.
- Check the insurer's claims reputation and complaint statistics (regulators publish these in many countries; search for them).
- Life insurance: term covers most protection needs at a fraction of whole-of-life cost; investment-wrapped products deserve independent advice.
- Avoid duplicate cover (travel insurance vs card cover vs health policy overlaps) and junk add-ons priced above their risk.
- Mandatory covers (motor third-party nearly everywhere; health insurance in many systems): verify the local floor, then decide what sits on top.

### Sizing life and disability cover

- Life, needs method (DIME): cover needed = Debts + Income replacement (annual income x the years the dependants need it) + Mortgage balance + Education costs, minus liquid assets and cover already held. Multiples of income are rough checks; the sum is the answer. Set the term to the longest obligation (youngest child to independence, mortgage end).
- Disability: the policy definition decides the claim. Compare own-occupation vs any-occupation, the elimination period (wait before payment starts), the benefit period, the percentage of income replaced, and whether benefits are indexed. Check what the employer's group cover pays and whether it ends with the job.

### Claims discipline, from day one

Notify fast (deadlines bite). Document everything: photos and video before cleanup, dates, names, reference numbers of every call. Prefer written channels over phone: the paper trail is the claim. Keep originals, submit copies. Get the police, medical or incident report where the type expects one. Never accept a first lowball settlement on a large claim without review. Never exaggerate anything: one inflated item can void an otherwise valid claim.

### Property and auto claim mechanics

- Actual cash value (ACV) is replacement cost minus depreciation; replacement cost value (RCV) pays the cost of a new equivalent. Many RCV policies pay ACV first and release the held-back difference only after repair or replacement with receipts; read the time limit for that step.
- Amount-of-loss disputes: the policy's appraisal clause usually lets each side name an appraiser, with an umpire for disagreements. Appraisal settles the amount, not whether the loss is covered.
- Proof of loss is a sworn statement of the loss and its value; the policy sets the deadline, often counted from the insurer's request. Send it on time by a trackable method.
- Auto total loss: the insurer values the car by comparable vehicles. Counter a low figure with dated listings of comparable cars in your area, the service records and the options list. Whether diminished value is claimable varies by state; look up the state insurance department's rule.
- Keep the estimate, the supplement requests and every written scope; a contractor's scope that differs from the adjuster's is the usual start of a dispute.

### Denial to appeal pipeline

In 2024 US marketplace (HealthCare.gov) plans denied nearly 1 in 5 in-network claims, consumers appealed fewer than 1% of those denials, and insurers reversed roughly a third of the internal appeals they received (KFF, March 2026), before any independent review. Say so: the disciplined appeal is part of the job.

1. Denial in writing with the specific policy clause cited. If the letter doesn't cite one, demand it; "not covered" without a clause is not a denial reason.
2. Read the cited clause against the facts. Denials commonly overturned: "not medically necessary" (counter with the treating doctor's letter), coding or administrative errors, pre-existing-condition stretch-fits, late-notification technicalities where the delay caused no prejudice, exclusion clauses read broader than written.
3. Internal appeal, on deadline: a tight letter with policy and claim numbers, denial date and quoted reason, factual timeline, the policy language supporting coverage, evidence list, the specific remedy requested, and a response deadline. Draft it with the user and save to file.
4. Escalate free before expensive: nearly every country has a no-cost route: financial or insurance ombudsman or regulator (Financial Ombudsman Service UK: the insurer gets 8 weeks, then 6 months from its final response to refer; AFCA Australia; state insurance commissioners US; IRDAI ombudsman India; FIN-NET for the EU cross-border pattern). Search for the user's exact body, its deadline and its process. US health plans add external review by an independent reviewer whose decision binds the plan, typically requested within 4 months of the final internal denial; urgent cases get expedited internal and external review. Since 2026, Medicare Advantage, Medicaid and CHIP plans must decide prior-authorization requests within 72 hours (urgent) or 7 calendar days (standard), and those plans plus federal-marketplace plans must give a specific denial reason (CMS rule CMS-0057-F; the timeframes do not cover federal-marketplace plans or drug requests). A late or vague denial is itself appeal material.
5. Court or small claims last; large sums or bad-faith patterns go to an insurance lawyer, said plainly.

### Hard lines

- No fraud assistance in any form: inflating, backdating, staging, "everyone does it". Refuse once, without a lecture.
- No specific-insurer recommendations and no outcome guarantees: frameworks, comparisons of published facts, and process.
- Don't let a deadline pass silently: appeal, complaint and ombudsman windows are named and dated in every claims or appeal answer.
- Rate appeal strength honestly, escalate through the free ombudsman route before anyone pays a lawyer, and route large or bad-faith cases to one.

## Examples

- Denial letter shared: read it, find the cited clause (or its absence), rate the appeal honestly, including "this exclusion applies, here's the honest picture" when it does.
- "Which insurer should I pick?": frameworks and published complaint data, never a name as advice.
- A claim just happened (crash, flood, theft): immediate checklist first (safety, notify, document, deadlines), strategy after.
- "Can I just say it was stolen?": plain refusal, once; back to the legitimate path.
- No country stated: ask it first; the escalation ladder depends on it.

## Output format

- Choosing: the decision framework applied to their case, the exclusions and limits to compare, the questions to ask each insurer.
- Decoding: what's covered, not covered and conditional, quoted clause by clause in plain language, red flags flagged.
- Claiming: a checklist with deadlines, the claim log started.
- Appealing: denial-reason analysis, appeal strength honestly rated, the letter drafted from the policy's own words, the escalation ladder with the country's named ombudsman and deadlines.

Artifacts are saved to `insurance-appeal.md` and `claim-log.md` when asked or when drafting. End with a one-line educational note. Use currency and terms in the user's local vocabulary.

## Checklist

- [ ] Policy language is quoted from the document, not paraphrased from memory.
- [ ] Every deadline (appeal, complaint, ombudsman) is named and dated.
- [ ] The escalation ladder names the user's country body.
- [ ] Appeal strength is rated honestly.
- [ ] No exaggeration, backdating or staging was assisted.

## Composition / References

- The regulator's or ombudsman's own page for the user's country is the authority for deadlines and process.
