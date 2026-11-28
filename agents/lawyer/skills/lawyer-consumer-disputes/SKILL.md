---
name: lawyer-consumer-disputes
title: "Demand Letters, Chargebacks and Refund Disputes"
description: "Consumer dispute strategy: refunds, chargebacks, demand letters, debt-collector replies, credit-report disputes, small-claims prep, with deadlines."
license: Apache-2.0
compatibility: "Needs web search to verify current deadlines and rules, and file access to save case files and letters. Information and drafts, not legal advice."
capabilities: filesystem-write memory-read memory-write
rules:
  - match((?i)\b(escalation letter|final demand|regulator complaint|billing[- ]dispute|dispute letter|credit[- ]report dispute|lawsuit[- ]answer|debt buyer|subscription cancellation|keeps? (billing|charging|reporting))\b)
  - match((?i)\b(write|draft|prepare)\b.{0,80}\b(letter|complaint|response)\b.{0,100}\b(refund|replacement|warranty|charge|cancel\w*|debt|credit|collector|dealer|merchant)\b)
  - match((?i)\b(evidence checklist|filing steps)\b.{0,80}\bsmall[- ]claims?\b|\bsmall[- ]claims?\b.{0,80}\b(evidence|filing|checklist)\b)
  - match((?i)\b(demand letter|chargeback|charge back|small[- ]claims?|validation letter|debt validation|credit report dispute|dispute (a |the )?charge)\b)
  - match((?i)\b(debt collector|collection agency|collector keeps calling|collectors? (is |are )?calling)\b)
  - match((?i)\b(won'?t refund|refus\w+ (to )?(give me )?(a )?refund|wrong on my credit report|error on my credit report|unauthori[sz]ed charge|can'?t cancel (my )?subscription)\b)
  - semantic(write a demand letter to get a refund from a company)
  - semantic(how do I dispute a chargeback or a credit card charge)
  - semantic(a debt collector is harassing me, how should I reply)
  - semantic(prepare me for small claims court over a faulty product, 0.74)
---

## Overview

Most consumer disputes are won by the person who knows the deadline, cites the right rule and keeps a paper trail. This skill maps a person's leverage in everyday fights (refunds refused, unauthorized charges, subscriptions that will not end, debt collectors, credit-report errors) and drafts the letters and filings they send themselves. It provides legal information and document preparation, not legal advice or representation. It does not cover representation and court appearances, disputes above small-claims scale or with real legal complexity, drafting binding contracts, immigration matters, insurer claim denials, medical-provider billing disputes, or pre-payment scam triage and first-hour scam recovery; name those as out of scope and suggest a lawyer or specialist in that field.

## Mental model

The honest read comes first, including "you likely have no claim" when true. Each step comes with the next one: where the dispute goes if ignored, and when to hand it to a human lawyer. The paper trail is the strategy: dates, names, screenshots taken before accounts get closed, tracked or certified mail (or email with read receipt) for anything that matters.

## Rules

### Workflow

1. Ingest: what happened, when, amounts, jurisdiction, what has been tried, what the user wants (refund, deletion, silence, principle). Use `remember(["consumer disputes", "deadlines", "case log"])` to recall earlier case state.
2. Deadline check first: many consumer rights are deadline-gated. Establish the tightest applicable window before anything else and verify current rules for the user's jurisdiction by web search. Consumer law shifts; never cite a rule from memory as current.
3. Map leverage: which rule, which forum, what remedy.
4. Draft the letter or response, factual and unemotional: what happened, what rule applies, what remedy, by what date, what happens next if ignored.
5. Escalation ladder: deliver step N+1 with step N: where this goes if ignored, and when to route to a human lawyer.
6. `memorize()` case state: what was sent, to whom, deadlines pending.

### Deadline anchors by jurisdiction

Verify current figures by web search before drafting; these decide cases.

| Jurisdiction | Anchor rules |
|---|---|
| US | Credit-card billing error: written dispute within 60 days of the statement (FCBA). Debit/EFT fraud: report within 2 business days to cap loss at $50, within 60 days of the statement to cap at $500 (EFTA/Reg E). Debt collector: dispute in writing within the 30-day validation period in the validation notice (FDCPA/Reg F; collectors limited to 7 calls in 7 days per debt). Credit report: bureau must investigate within 30 days, 45 if you add information (FCRA). |
| UK | Faulty goods: 30-day short-term right to reject, then repair/replace, then price reduction or final rejection (Consumer Rights Act 2015). Credit card purchases £100-£30,000: card issuer jointly liable (s.75 Consumer Credit Act 1974). Debit card or under £100: chargeback (card-scheme time limits, often 120 days). Financial firm: Financial Ombudsman after the final response or 8 weeks, within 6 months of the final response. |
| EU | 14-day withdrawal right for online and distance purchases; since 19 Jun 2026 online sellers must offer an electronic withdrawal button (Directive 2023/2673). Minimum 2-year legal guarantee for goods, with defects in the first year presumed to exist at delivery. Right-to-repair rules (Directive 2024/1799) apply from 31 Jul 2026: choosing repair extends the guarantee by 12 months for contracts concluded from that date; national laws implement it unevenly, so check the member state's statute. |
| Australia | Consumer guarantees under the Australian Consumer Law cannot be excluded and have no fixed expiry (they last as long as is reasonable for the item); a major failure lets the consumer choose refund, replacement or compensation. Financial firms go to AFCA (free): lodge within the earlier of 6 years from when you knew of the loss or 2 years from the firm's internal dispute resolution (IDR) response (AFCA Rules, 8 October 2026 edition, rule B.4.3.1; AFCA may accept late complaints in special circumstances). Small claims via state tribunals. |
| Canada | Provincial consumer protection acts govern (Quebec's is the strongest); card chargebacks under issuer policies. Ontario's Consumer Protection Act, 2023 is enacted but not in force (as of 2026-11, in force on proclamation), so the 2002 Act still applies; cooling-off and limitation periods differ by province, so look up the province's act before stating a deadline. |

### Chargeback or demand letter

Unauthorized or undelivered card charges: issuer dispute first (free, fast, bank-side leverage). Service quality fights and non-card payments: demand letter to the merchant. Never both simultaneously without disclosure; parallel games backfire.

### Debt collectors

Everything in writing. Admit nothing about old debts: partial payment or written acknowledgment can restart limitation periods in many places, so flag this loudly. Check whether the debt is time-barred, demand validation, and never ignore a served lawsuit: a default judgment converts a maybe-debt into a certain one. Answering a suit is the point where you prepare and a human files or a lawyer takes over.

### Demand letter anatomy

Facts in timeline order, then the rule or promise breached, then the exact remedy and amount, then a deadline (10-14 days typical), then the stated next step (regulator complaint, small claims). One page. Anger deleted; specificity kept.

### Regulator complaints

Regulator complaints are free leverage: financial regulators, ombudsmen, consumer-protection agencies and state attorneys general forward complaints, and companies answer them. Mention the intended complaint in the demand letter, then follow through.
- US: the CFPB portal faced funding and staffing fights in 2025-26, so file with the state AG (and reportfraud.ftc.gov) as well.
- Subscriptions: the FTC's federal click-to-cancel rule was vacated in July 2025, so cite ROSCA and the state's automatic-renewal law. In the UK the DMCCA 2024 subscription rules are not yet in force, but its unfair-practice bans (fake reviews, drip pricing) are, since April 2025.

### Small-claims prep

Check the jurisdiction's current limit live (2026 examples: England and Wales £10,000; Ontario $50,000; US states roughly $2,500-$25,000). Compile the evidence pack (contract, communications, photos, the ignored demand letter) and rehearse the two-minute version of the story. The demand letter that was ignored is exhibit one.

## Examples

- "They won't refund me": deadline check, then chargeback-versus-demand-letter routing, then the draft.
- "A collector keeps calling": validation letter plus a rights summary; served papers mean answer preparation and a strong push to a lawyer.
- "This is wrong on my credit report": dispute letters to the bureau and the furnisher with evidence attached.
- "Can I sue?": small-claims fit check with honest odds; above the limit or complex, refer to a lawyer in the jurisdiction.
- Weak case: say so directly; a doomed letter wastes the user's leverage and time.

## Output format

Working documents as Markdown:
- Case map: `dispute-[merchant].md` with the facts timeline, leverage analysis, deadlines and escalation ladder.
- Letters: `demand-[merchant].md`, `validation-[collector].md`, `credit-dispute-[bureau].md`, send-ready, blanks marked.
- Small claims: `small-claims-[merchant].md` with the evidence checklist, filing steps and story outline.

## Checklist

- [ ] The tightest deadline leads the answer, verified for the user's jurisdiction.
- [ ] Every draft is factual, one page, and names the next escalation step.
- [ ] Nothing drafted is deceptive or threatens beyond stated legal remedies.
- [ ] A served lawsuit is never left unanswered; the user is pushed to a lawyer at representation, complexity or courtroom lines.
- [ ] Case state (what was sent, to whom, deadlines pending) is saved with `memorize()`.
