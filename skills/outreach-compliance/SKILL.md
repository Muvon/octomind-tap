---
name: outreach-compliance
title: "Cold Email Compliance – CAN-SPAM, GDPR and CASL"
description: "Cold email laws and CAN-SPAM Act compliance flags, plus GDPR, PECR, and CASL consent, identification, and opt-out checks. Use when preparing email, call, or message outreach to US, EU, UK, or Canadian recipients. Not legal advice."
license: Apache-2.0
compatibility: "Environment-independent. Any OS."
domains: marketing sales launch
rules:
  - content(compliance) content(outreach)
  - content(gdpr) content(email)
  - content(can-spam)
  - content(unsubscribe) content(cold)
---

## Overview

Outreach law depends on the recipient's location and on whether the message is commercial. This skill gives drafts the correct flags and tells the writer when to stop and send the question to counsel. It is a checklist for guardrails, not legal advice, and it never certifies a campaign as lawful.

Laws and enforcement change. State the recipient jurisdiction in the plan and confirm with counsel before scaling.

## Mental model

Four questions decide the guardrails: where is the recipient, is the address a corporate or personal one, is there consent or a recognised basis, and can the recipient opt out easily. Answer them per recipient group, not per campaign.

## Rules

### Jurisdiction flags

| Region | Commonly applicable position for B2B cold email | Flag |
|--------|-----------------------------------------------|------|
| US (CAN-SPAM) | Permitted without prior consent if truthful | Accurate sender and subject, physical postal address, working opt-out honoured within 10 business days |
| Canada (CASL) | Consent required; implied consent is narrow | Conspicuously published address plus message relevant to the recipient's role; identification and unsubscribe |
| Germany | Prior consent generally needed even for B2B email | Do not cold-email without counsel sign-off |
| UK (PECR/UK GDPR) | Corporate subscribers may be emailed with identification and an opt-out | Sole traders and personal addresses are treated differently |
| EU other | Varies by member state; GDPR applies to personal data | Record lawful basis and a data source |

### Calls and texts

Calls and texts follow separate rules: US Do-Not-Call and TCPA consent rules for texts and autodialled calls, and similar regimes elsewhere. Do not draft automated texts or call scripts that skip checking the registry.

### Always in every commercial message

- Truthful sender identity and subject.
- A working, free opt-out and a promise to honour it.
- A postal address where required.
- Suppression: opted-out addresses never re-enter any list or sequence.

### Personal data

Record the source of each contact and the reason you are contacting them. Collect only what the message needs. Do not scrape private data. Handle access and deletion requests promptly. Where EU or UK data is processed, note the lawful basis for the plan.

### Platform rules

LinkedIn's User Agreement bans automation of invites and messages; keep those touches manual. Respect each platform's terms before drafting any scripted flow.

### Sector flags

Securities communications such as investor outreach, health, finance, and political messages carry extra rules. Send these to counsel before use. For paid creator relationships, see the disclosure rules in the `outreach-influencer` skill.

### When to stop and escalate

Escalate to counsel when the recipient group includes Germany, Canada without clear implied consent, personal addresses, a regulated sector, or any list of unclear origin.

## Examples

Bad: "It's B2B so rules don't apply, send to the whole list."

Good: "List split by country. US and UK corporate addresses use identification and opt-out. Canada limited to published addresses with a relevant role. Germany held pending counsel."

## Checklist

- [ ] Recipient jurisdiction identified per group?
- [ ] Sender identity, address, and opt-out present in the draft?
- [ ] Opt-out suppression defined and permanent?
- [ ] Contact source and reason recorded?
- [ ] Platform terms respected, no LinkedIn automation?
- [ ] Regulated or uncertain groups sent to counsel?

## Composition / References

- Pair with `outreach-cold-copy` for the message and `outreach-deliverability` for sending.
- Type-specific notes live in `outreach-influencer` (disclosure) and `outreach-investor` (securities caution).
