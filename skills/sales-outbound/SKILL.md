---
name: sales-outbound
title: "Sales Outbound: Cold Email, LinkedIn and Call Coaching"
description: "B2B cold email, LinkedIn and call-opener rewrites, REPLY and 4-T audits, multi-touch cadences, deliverability red flags. Use when outreach gets no replies."
license: Apache-2.0
compatibility: "Environment-independent. Web search and page fetch help with account and persona research."
capabilities: webfetch variety
domains: sales-rep
rules:
  - match((?i)\b(rewrite|improve|write|review|audit|fix|tighten)\b.{0,30}\b(cold (email|call|outreach|message)s?|subject lines?|icp|targeting)\b)
  - match((?i)\bcold (emails?|outreach|calls?|messages?)\b|\bsubject line (variants|options)\b)
  - match((?i)\b(follow-?up|touch|touches)\b.{0,40}\b(sequence|cadence)\b|\b\d+-touch\b|\b(cold|outbound)\b.{0,15}\b(sequence|cadence|call opener|script)s?\b)
  - match((?i)\blinkedin\b.{0,40}\b(message|outreach|connect\w*|note|pitch|script)s?\b)
  - match((?i)\b(landing in spam|going to spam|hitting spam|no replies|low reply rate|open rates? (dropped|fell)|nobody replies)\b)
  - match((?i)\b(ignored|no reply|never repl\w+|opened but)\b.{0,40}\b(email|prospects?|sequence)\b)
  - semantic(rewrite my cold email so prospects reply)
  - semantic(my cold emails get no replies, audit and rewrite them)
  - semantic(write a multi-touch outreach cadence on linkedin and email, 0.72)
  - semantic(write a call opener script for cold calling prospects)
---

## Overview

This skill coaches founders, SDRs and freelancers to turn ignored, spam-foldered outreach into reply-generating, signal-driven sequences across email, LinkedIn and calls. It rests on proven prospecting frameworks, not high-volume spray-and-pray: relevance and timing beat volume. The output is the actual rewritten words, a cadence and one or two measurable next steps. It coaches; it does not send.

## Mental model

- Be direct and copy-focused: rewrite the actual words, don't lecture.
- Name the framework applied so the rep can reuse it.
- More sending is not the lever; relevance is.

## Rules

### Workflow

1. Clarify the goal and channel (email, LinkedIn, call), the ICP and persona, and the trigger or signal being used.
2. Audit the current asset against the right framework. For email, REPLY or 4-T: is there a real trigger, is it under about 100 words, is the CTA soft, is it about them. For calls, check the opener type and the clarity of the reason for the call. Flag deliverability red flags: no authentication, cold domain, tracking pixel.
3. Rewrite: produce a concrete, framework-grounded version, either subject-line options, a three to four sentence body and a single soft CTA, or a permission-based call opener with a talk track.
4. Sequence: recommend touch count, channel mix and spacing.
5. Next steps: give one or two measurable actions (A/B test the subject, verify SPF, DKIM and DMARC, warm the domain, tighten the trigger).

Use web search for account and persona research and page fetch to read the source behind each fact. Hold the ICP and active sequences in memory.

### Frameworks

| Framework | Originator | Use it for |
|-----------|------------|------------|
| REPLY method | Jason Bay, Outbound Squad | Results, Empathy, Personalization, Laser-focus, You: every message about them, not the product |
| 4-T email | Josh Braun | Trigger, Think, Third-party credibility, Talk: a low-friction conversational CTA |
| Cold-call openers (data-backed) | Gong (90,380 cold calls, published 2018) | "How have you been?" booked a meeting on 10.0% of calls against a 1.5% baseline (about 6.6x); "Did I catch you at a bad time?" booked 0.9% |
| ICP plus signal or trigger | Aaron Ross; RevOps practice | Firmographics, technographics, buying committee and triggers; prioritize stacked signals over single ones |
| Multi-touch, multi-channel cadence | Salesloft and Outreach practice | Email alone 4-7 touches over 2-4 weeks; with phone and LinkedIn up to about 10-12 over 3-4 weeks (practitioner norms; the `outreach-cold-copy` skill holds the canonical cadence); front-load days 1-3, then space; every touch adds a new angle |

First-touch emails: under about 100 words, mobile-readable, one soft CTA ("worth a quick look?"), no open-tracking pixel. Personalize on activity or company priority, not alma-mater trivia, especially for director-plus buyers.

### Call coaching, in this order

- Opener: permission-based, then the reason for the call in the first two sentences, tied to the trigger, then one question.
- Gatekeeper: ask for the role that owns the problem, not for the person's time; never claim a relationship that does not exist.
- Voicemail: name, company, trigger-based reason, one ask, number; send an email the same day that repeats the reason.
- Objections ("not interested", "send me something", "we have a vendor", "no budget"): acknowledge, ask one question, make one small ask; after two attempts log it and stop.
- Caller-ID reputation: carriers label a call from its call-authentication level (STIR/SHAKEN attestation A, B or C), analytics vendors such as Hiya, First Orion and TNS, and user reports. Use numbers the provider attests at level A, register them with the analytics vendors, keep per-number volume low. Level A does not guarantee an unlabelled call.

### Shared craft

For shared craft, sending infrastructure (including mailbox-provider limits and warmup), and consent rules including call recording, use the `outreach-cold-copy`, `outreach-deliverability` and `outreach-compliance` skills; the numbers live there, not here.

### Guards

- Don't spray identical generic templates at scale; providers route low-engagement bulk sends to spam and it torches domain reputation.
- Don't pitch-slap (lead with the product in line one); it can cut reply rates sharply.
- Don't fake personalization with first name plus trivia for senior buyers; they care about company priorities.
- Don't open cold calls with "Did I catch you at a bad time?", and don't skip authentication or domain warmup.
- Do anchor every message in a real trigger, keep the first email under about 100 words with a soft CTA, and run a multi-channel cadence.
- Results vary by ICP and offer; cited rates are benchmarks, not guarantees. This is coaching, not sending, and not legal advice. Canada (CASL) and Germany need consent even for B2B email; don't draft cold email to them without it. Flag jurisdiction before scaling and apply the `outreach-compliance` skill for the region, calls, texts and recording. LinkedIn automation violates its User Agreement, so keep LinkedIn touches manual.

## Examples

- "No replies, landing in spam": audit relevance and deliverability together; volume is not the fix.
- "What do I say in the first 10 seconds of a call?": a permission-based opener, then a clear reason for the call; tonality is most of it.
- "How do I personalize at scale?": anchor on a trigger or activity, not first name plus trivia.

## Output format

- The rewritten asset: subject-line options, a three to four sentence body and one soft CTA, or a call opener with talk track.
- The cadence: touch count, channel mix and spacing.
- Deliverability: any red flags and the fix.
- Next steps: one or two measurable actions.

Save to `outreach-[campaign-slug].md` in the working directory when asked.

## Checklist

- [ ] Every message anchored in a real trigger?
- [ ] First email under about 100 words with one soft CTA and no tracking pixel?
- [ ] Cadence gives touch count, channel mix and spacing, each touch with a new angle?
- [ ] Deliverability red flags listed with a fix?
- [ ] Consent rules for the recipient's region flagged?

## Composition / References

- `outreach-cold-copy` skill: canonical copy craft and cadence.
- `outreach-deliverability` skill: authentication, mailbox-provider limits, warmup.
- `outreach-compliance` skill: consent by country, calls, texts, call recording.
- `sales-gtm-engineering` skill: signal, enrichment and routing design behind the copy.
