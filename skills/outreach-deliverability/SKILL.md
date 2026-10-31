---
name: outreach-deliverability
title: "Cold Email Deliverability – SPF, DKIM and DMARC"
description: "Cold email deliverability guidance for SPF, DKIM, and DMARC setup, sending domains, email warmup, volume caps, and list hygiene. Use when planning outreach infrastructure or diagnosing spam placement and bounces."
license: Apache-2.0
compatibility: "Needs DNS access for the sending domain to apply changes. Any OS."
domains: marketing sales launch
rules:
  - content(deliverability)
  - content(spam folder) content(email)
  - content(warmup) content(domain)
  - content(spf) content(dkim)
---

## Overview

Outreach fails silently when mail lands in spam. Deliverability is infrastructure plus behaviour: authenticated sending domains, gradual volume, clean lists, and messages that readers do not mark as spam. This skill specifies the setup and the diagnostic order. It designs and diagnoses; it does not send.

Mailbox-provider rules change. The figures below are the commonly cited working norms; confirm against the current Google, Yahoo, and Microsoft sender guidelines before committing a plan.

## Mental model

Mailbox providers score sender reputation from authentication, complaint rate, bounce rate, and engagement. Reputation attaches to the domain and the IP. A cold campaign borrows reputation; a complaint spike spends it. Protect the primary domain by sending outreach from separate domains.

## Rules

### Infrastructure

- Separate sending domains for outreach, never the primary company domain. Close variants of the brand are common practice.
- Each sending domain has SPF, DKIM, and a DMARC record. Start DMARC at `p=none` with reporting, aligned with the From domain.
- A few mailboxes per domain, each with a real name and signature. Do not spread volume across dozens of throwaway domains.
- Bulk-sender rules: Google applies them at about 5,000 messages a day to personal Gmail accounts, Yahoo to bulk senders without a published number, and Microsoft at 5,000+ a day to Outlook.com since 5 May 2025. All three require SPF and DKIM passing plus an aligned DMARC record.
- Gmail and Yahoo also require one-click unsubscribe on marketing mail, and cold outreach counts: RFC 8058 `List-Unsubscribe` plus `List-Unsubscribe-Post: List-Unsubscribe=One-Click`, honoured within 2 days.

### Warmup and volume

- Warm new domains 2 to 4 weeks with low, rising volume and real replies before campaign traffic.
- A cap in the region of 30 sends per mailbox per day is a practitioner norm, not a provider rule. Raise it only while metrics stay healthy.
- Sudden volume jumps are a spam signal. Ramp gradually.

### Hygiene

- Verify addresses before sending. Target bounces under about 2%.
- Remove hard bounces, unsubscribes, and complaints immediately and permanently.
- No purchased lists and no scraped lists with unclear provenance.
- Never re-contact someone who opted out, on any domain or sequence.

### Content

- Plain text, one link, no attachments, no open-tracking pixel on first touch.
- No spam trigger words and no misleading subjects.
- Individual copy: identical bodies at scale are easier to cluster and filter.

### Targets and thresholds

| Metric | Working target |
|--------|----------------|
| Spam complaint rate | Under 0.1%, hard ceiling 0.3% |
| Bounce rate | Under about 2% |
| Replies and meetings | The success measure; opens are a diagnostic only |

### Diagnostic order

When mail is not landing, check in this order and change one thing at a time:

1. Authentication: SPF, DKIM, DMARC pass and align.
2. Domain age and warmup state.
3. List quality and bounce rate.
4. Volume and sending pattern.
5. Copy: spam words, links, tracking, length.
6. Complaints and blocklists.

### Shared rules

Use the `outreach-cold-copy` skill for the message itself and the `outreach-compliance` skill for consent and opt-out rules.

## Examples

Bad: "Send 500 a day from our main domain starting tomorrow."

Good: "Two new domains, two mailboxes each, SPF/DKIM/DMARC live, 3 weeks warmup, then 20 sends per mailbox per day on a verified list, stopping if complaints pass 0.1%."

## Checklist

- [ ] Outreach sent from separate domains, not the primary one?
- [ ] SPF, DKIM, and DMARC pass and align on each sending domain?
- [ ] Warmup of 2 to 4 weeks before campaign traffic?
- [ ] Lists verified, bounces under about 2%, opt-outs suppressed permanently?
- [ ] Complaint threshold and a kill rule defined?
- [ ] Current provider guidelines re-checked rather than relying on this list?

## Composition / References

- Pair with `outreach-cold-copy` and `outreach-compliance`.
- This skill covers email only. LinkedIn automation violates its User Agreement; keep those touches manual.
