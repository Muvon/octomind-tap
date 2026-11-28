---
name: marketing-partner
title: "Partner Marketing: Affiliate and Referral Programs"
description: "Designs affiliate, referral, reseller and tech-partner programs: recruitment lists, incentive economics, co-marketing plans and cohort measurement."
license: Apache-2.0
compatibility: "Needs web search to find and verify partner candidates and marketplace terms. Plans only; sends nothing. Any OS."
rules:
  - match((?i)\b(design|set up|build|launch|rework|evaluate)\b.{0,30}\b(affiliate|referral|reseller|partner)\s+programs?\b)
  - match((?i)\bco-?marketing\s+(plans?|campaigns?|webinars?)\b|\bjoint\s+(webinar|campaign)s?\b)
  - match((?i)\b(partners?|affiliates?|resellers?)\b.{0,40}\b(recruit\w*|candidates?|list|ICP|incentiv\w*|onboarding kit|enablement|commission|payout|tiers?)\b)
  - match((?i)\b(partner[- ]sourced|partner cohorts?|agency partners?|tech(nology)?[- ]partners?|integration partners?)\b)
  - match((?i)\b(affiliates?|resellers?)\s+(for|of)\s+our\b)
  - semantic(design an affiliate program with commissions and a recruitment list, 0.73)
  - semantic(plan a joint webinar with a partner company that shares our audience, 0.71)
  - semantic(recruit resellers and agency partners and set their commission tiers)
  - semantic(set up partnerships with companies that reach our buyers and share revenue, 0.70)
---

## Overview

Use this skill to design programs that let other companies' audiences become a durable acquisition channel: affiliates, referral partners, resellers and agencies, and technology integration partners. The outcome is a partner program file with the leading program type, a named recruitment list, incentive economics, an enablement kit, a co-marketing plan and a measurement plan. Think in partner economics: what each side earns, and whether partner-sourced customers actually stay.

## Mental model

Be skeptical of logo-collecting. A partnership that produces no measured revenue is a press release, not a channel.

## Rules

### Workflow

1. Ingest: product, ACV, buyer profile, existing partnerships. Recall earlier partner program, partner ICP and incentives from memory.
2. Pick the type with the incentive table. Most companies should start with one type, run manually, before building a program.
3. Recruit list: run parallel web searches for who already reaches the buyer (newsletters, agencies, complementary tools, communities). Verify audience overlap with evidence, not vibes.
4. Design economics: incentive per the table, tier thresholds, payout terms.
5. Plan enablement and co-marketing: what a partner needs to sell in their own words, and one or two joint campaigns per tier.
6. Deliver the program file, then memorize type, incentives and target list.

### Incentives by partner type

| Partner type | Common incentive (practitioner norms, not rules) | Fits when |
|--------------|------------------|-----------|
| Affiliate | 20-30% recurring rev-share (12-month cap common) | Self-serve product, low-touch close |
| Referral | Flat fee or account credit per closed deal | Higher ACV, sales-assisted close |
| Reseller / agency | 15-30% margin + deal registration | Buyer outsources the work to agencies |
| Technology | Mutual leads, marketplace placement, co-marketing | Product completes another tool's workflow |

### Principles

- Measure partner-sourced cohorts on retention and expansion, not signup counts. Recurring revenue lives or dies past month one, and a partner sending churny customers is negative-value at any volume.
- Fewer than about 10 active partners is business development, not a program: run it manually, learn the pitch that lands, then systematize.
- Co-marketing requires audience-overlap evidence before commitment: a shared ICP named in writing, not "our audiences are similar".
- Tiers earn benefits from trailing performance, never from promises.

### Program mechanics

Write these into the terms as defaults the founder can change:

- Attribution: credit the partner whose tracked link or registered deal came first within the window, and write the window in days (a common range is 30 to 90, matched to your sales cycle). Self-serve products use link or coupon-code tracking. Sales-assisted products use deal registration, where the first valid registration holds the account for a stated period (for example 90 days) if the partner keeps working it.
- Payout timing and clawback: pay only on cash received, after the refund and chargeback period ends. Reverse commission on refunds, chargebacks and cancellations inside the recurring-commission cap.
- Fraud controls: ban self-referral and referral of the partner's own accounts, bidding on your brand or trademarked terms, coupon-site hijacking of last click, and incentivized signups. Review the first payout of every new partner by hand and set a minimum payout.
- Tracking: use an affiliate or partner tracking platform, or tagged links with a coupon code per partner, with unique IDs, a record of each referred account, and monthly reconciliation against billing. A partner who cannot see their own referrals will stop referring.
- Marketplace co-sell (cloud or app-store marketplaces): list only when buyers already hold a committed cloud budget or the marketplace is where your category is bought. Read the marketplace's current fee schedule, co-sell eligibility and listing-approval time before promising margin or dates.

### Disclosure

Disclosure is part of the program design. The FTC Endorsement Guides (16 CFR 255, revised 2023) require affiliates and partners to disclose the material connection clearly at the endorsement. The FTC reviews rule (16 CFR 465, in force since Oct 2024) bans bought reviews, sentiment-conditioned review incentives and undisclosed insider reviews. Write both into partner terms and the enablement kit. Affiliate links on partner sites carry rel="sponsored" (Google link spam policy). For non-US programs, check local rules (for example UK CMA, EU UCPD). For partner email outreach, specify consent and opt-out by region with the `outreach-compliance` skill and sending setup with the `outreach-deliverability` skill.

### Enablement kit minimum

One-pager in the partner's voice, demo script, objection answers, co-branded asset templates, and where their leads get tracked.

### Guards

- Don't recommend a program before about 10 manual partner wins.
- Don't count signups as partner success.
- Don't promise marketplace or co-marketing results without overlap evidence.
- Don't launch affiliates without disclosure rules.
- Don't draft legal terms; flag them for legal review.
- Do name real recruitment candidates, tie every incentive to closed and retained revenue, and compare partner cohorts against direct cohorts in every review.
- Direct sales pipeline, outbound, press relations and the integration build itself are outside this skill.

## Examples

- "Should we do partnerships?": apply the fit test. Does someone else already reach your buyer with trust you lack? If not, say partnerships are premature.
- "Set up an affiliate program": check self-serve fit first. If the close is sales-assisted, steer to referral economics.
- "Partner X wants to co-market": overlap evidence check, then a campaign plan or a documented pass.
- Vague request: ask one question: "Who already has your buyer's trust today?"

## Output format

Save as `partner-program-[product].md`:

```markdown
# Partner Program: [Product]

## Program Type & Rationale
[Which of the four types leads, and why the others wait]

## Partner ICP & Recruitment List
[Profile + 15-20 named candidates with the overlap evidence]

## Economics
[Incentive structure, tiers, payout terms, deal registration rules]

## Enablement Kit
[Contents list with owners: what is drafted here vs. what others produce]

## Co-Marketing Plan
[1-2 campaigns per tier with effort and expected contribution]

## Measurement
[Partner-sourced CAC, activation, retention, NRR vs. direct cohorts; review cadence]
```

## Checklist

- [ ] One leading partner type with the reason the others wait.
- [ ] Recruitment candidates are named, each with overlap evidence.
- [ ] Incentives tie to closed and retained revenue.
- [ ] Attribution window, payout timing, clawback and fraud controls are written.
- [ ] Disclosure rules are in the terms and the enablement kit.
- [ ] Legal terms are flagged for review, not drafted.

## Composition / References

- `outreach-compliance` skill: consent and opt-out for partner email.
- `outreach-deliverability` skill: sending setup for partner email.
