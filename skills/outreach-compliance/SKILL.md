---
name: outreach-compliance
title: "Outreach Compliance – Email, Calls and Recording Laws"
description: "Outreach law checks by region: email consent, opt-out, calls, texts, call recording. Use before contacting leads in the US, EU, UK, Canada or APAC."
license: Apache-2.0
compatibility: "Environment-independent. Any OS."
domains: marketing sales launch
rules:
  - content(compliance) content(outreach)
  - content(gdpr) content(email)
  - content(can-spam)
  - content(unsubscribe) content(cold)
  - content(tcpa)
  - content(call recording)
  - content(do not call)
  - content(casl)
  - content(pecr)
  - match((?i)\bcold\s+(email|emails|outreach|calls?|sequences?)\b)
  - match((?i)\b(germany|german|canada|canadian|uk|france)\b.{0,40}\b(cold|outreach|prospect\w*|leads?)\b)
---

## Overview

Outreach law depends on the recipient's location and on whether the message is commercial. This skill gives drafts the correct flags and tells the writer when to stop and send the question to counsel. It is a checklist for guardrails, not legal advice, and it never certifies a campaign as lawful.

Laws and enforcement change. State the recipient jurisdiction in the plan and confirm with counsel before scaling.

## Mental model

Four questions decide the guardrails: where is the recipient, is the address a corporate or personal one, is there consent or a recognised basis, and can the recipient opt out easily. Answer them per recipient group, not per campaign.

## Rules

### Jurisdiction flags

Rules as of 2026-11. Each row names the main rule and the flag for the draft; confirm the current text before scaling.

| Region | Commonly applicable position for B2B cold email | Flag |
|--------|-----------------------------------------------|------|
| US (CAN-SPAM) | Permitted without prior consent if truthful | Accurate sender and subject, clear identification as an ad or solicitation unless the recipient gave prior affirmative consent, physical postal address, working opt-out honoured within 10 business days |
| US states (privacy laws) | California's privacy act (CCPA) covers business contact data: its B2B exemption ended on 2022-12-31. It applies to firms meeting a threshold, for example annual gross revenue over USD 26,625,000 (as adjusted from 2025-01-01; re-adjusted every odd year) or data on 100,000 or more residents | Privacy notice at or before collection, honour opt-outs of sale or sharing. California residents can ask all registered data brokers to delete their data through one request (the Delete Act deletion platform, DROP), so re-check lists bought or enriched from a broker before each send |
| Canada (CASL) | Consent required. Implied consent covers a conspicuously published address, or one the person gave you, when the message relates to their business role and no refusal statement is attached | Identification, working unsubscribe honoured within 10 business days, unsubscribe address valid for 60 days after the send |
| Germany | Prior consent generally needed even for B2B email | Do not cold-email without counsel sign-off |
| France | Prior consent is not always required for B2B email when the message relates to the person's professional role (the regulator, CNIL, says so) | Tell the person who you are and why you have the address, give an opt-out, keep a tracking pixel out of the first touch as a precaution (the CNIL page on prospecting rules, as of 2026-11, does not address pixels; ask counsel) |
| EU other | Consent rules for emailing companies are set by each member state under the ePrivacy Directive (Article 13(5)); GDPR applies to every named person | Record the lawful basis and the data source; counsel confirms the country rule |
| UK (PECR/UK GDPR) | Corporate subscribers (companies, LLPs, government bodies) may be emailed with identification and an opt-out; sole traders and some partnerships are treated as individuals and need consent or a soft opt-in | PECR fines up to GBP 17.5 million or 4% of worldwide turnover since the Data (Use and Access) Act 2025 took effect |
| Switzerland | Opt-in for automated mass email advertising; a sender who got the address in a sale may mail similar products if an opt-out was offered then | Identify the sender, free and easy opt-out in every message |
| Australia | The Spam Act needs consent (express, or inferred from a relationship), sender identification and an unsubscribe facility. A published address gives inferred consent only when it is conspicuously published for a role (employee, director, officer, partner), publication was reasonably with that person's agreement, no "no unsolicited messages" statement accompanies it, and the message relates to that role | Withdrawal of consent takes effect after 5 business days (Schedule 2 clause 6); address harvesting is banned |
| New Zealand | The Unsolicited Electronic Messages Act needs consent, accurate sender details and a working unsubscribe | No address-harvesting software |
| Singapore | The Spam Control Act sets unsubscribe and labelling duties for bulk messages | Remove the address within 10 business days of an unsubscribe; B2B marketing calls and texts are outside the Do Not Call Registry |
| Japan | Opt-in for advertising email under the Act on Regulation of Transmission of Specified Electronic Mail, with exceptions for existing business relationships | Hold until counsel confirms the exception |
| India | The Digital Personal Data Protection Rules were notified in November 2025; most duties, including notice and consent, start about 18 months later (around May 2027) | Plan notices now; check the current start date |

The Singapore (10 business days) and Australia (5 business days) time limits are in Spam Control Act 2007 Second Schedule paragraph 2(7) (sso.agc.gov.sg/Act/SCA2007) and Spam Act 2003 Schedule 2 clause 6 (legislation.gov.au/C2004A01214/latest/text), as of 2026-11; read the current text before relying on them.

For any region not in the table, or when the row says counsel, send the question to counsel in that country.

When the contact's data was not collected from them, GDPR Article 14 requires telling them who you are, why you hold the data and where it came from: at the first contact if you use it to contact them, and within one month at the latest.

### Calls and texts

Calls and texts follow separate rules from email. Check the registry before drafting any call list or automated text.

United States (as of 2026-11):

- Calls and texts to US numbers fall under the Telephone Consumer Protection Act (TCPA) and the National Do Not Call Registry. Screen every list against the registry and your own opt-out list. Federal rules bar telephone solicitations to residential lines before 8 a.m. or after 9 p.m. at the called party's location (47 CFR 64.1200(c)(1)); some states set narrower hours.
- A voice generated by artificial intelligence counts as an artificial voice (FCC ruling of 2024-02-08), so AI calls need the same prior consent as prerecorded calls.
- The FCC's one-to-one consent rule (consent naming one seller) was vacated by the Eleventh Circuit on 2025-01-24 and never took effect.
- A person may revoke consent by any reasonable means and the sender must honour it promptly. In September 2026 the FCC narrowed the revoke-all rule: a stop request for informational messages can be limited to that category, a stop request for telemarketing still ends all telemarketing from that caller, and for informational messages, callers may designate exclusive opt-out methods (a stop-word reply, a key-press, a named website or number) if they disclose them clearly; the opt-out methods already required for marketing calls and texts do not change. The order (FCC 26-67) was published in the Federal Register on 2026-10-26 and takes effect 30 days later, so 2026-11-25 as of 2026-11.
- Since McLaughlin Chiropractic v. McKesson (Supreme Court, 2025-06-20), courts are not bound by FCC readings of the TCPA, so case law differs by circuit.
- Several states (for example Texas, Oklahoma, Florida, Maryland, Oregon, Utah, Pennsylvania, as named in a 2026 law-firm review; read each state's statute) have telemarketing and text laws stricter than the federal ones, with their own hours, frequency caps and consent forms. Apply the strictest rule that covers the recipient's state.

United Kingdom: screen call lists against the Telephone Preference Service (TPS) for individuals and the Corporate TPS (CTPS) for companies. Calling a registered number needs the person's explicit consent. Show the caller's number; do not withhold it.

Elsewhere: separate regimes exist; send call and text plans to counsel in that country.

### Recording calls and using AI notetakers

Recording is a separate consent question from calling.

- Federal law and most US states need consent from one party. About a dozen states need every participant to consent: California, Florida, Illinois, Maryland, Massachusetts, Montana, New Hampshire, Pennsylvania and Washington are named in a January 2026 law-firm survey. As of 2026-11 the state statutes confirm: California (Penal Code 632: consent of all parties to a confidential communication; section 637.2 civil damages are the greater of USD 5,000 per violation or three times actual damages), Florida (Stat. 934.03: lawful when all parties give prior consent), Maryland (Cts. & Jud. Proc. 10-402: all parties give prior consent) and Washington (RCW 9.73.030: consent of all participants; an announcement that is itself recorded counts as consent). Montana (45-8-213) bars recording a conversation with a hidden device without the knowledge of all parties. Illinois, Massachusetts, New Hampshire and Pennsylvania were not checked against their statutes. Read each state's statute before relying on the list.
- An AI notetaker bot that joins a meeting is a recording. A class action over such a tool (In re Otter.AI Privacy Litigation, Northern District of California) is pending as of 2026-11 and has no ruling on the merits.
- Rule: at the start of every call or meeting, say that it will be recorded or transcribed, and get a spoken yes from each person before the recorder or bot starts. If anyone declines, stop recording.
- For calls across borders, apply the strictest rule among the participants' locations.
- For recipients in the EU or UK, record the lawful basis and give a privacy notice for the recording as well.

### Always in every commercial message

- Truthful sender identity and subject.
- A working, free opt-out and a promise to honour it.
- A postal address where required.
- Suppression: opted-out addresses never re-enter any list or sequence.

### Personal data

Record the source of each contact and the reason you are contacting them. Collect only what the message needs. Do not scrape private data. Handle access and deletion requests promptly. Where EU or UK data is processed, note the lawful basis for the plan and send the Article 14 notice described above.

### Platform rules

LinkedIn's User Agreement bans automation of invites and messages; keep those touches manual. Respect each platform's terms before drafting any scripted flow.

### Sector flags

Securities communications such as investor outreach, health, finance, and political messages carry extra rules. Send these to counsel before use. For paid creator relationships, see the disclosure rules in the `outreach-influencer` skill.

### When to stop and escalate

Escalate to counsel when the recipient group includes Germany, Canada without clear implied consent, Switzerland, Japan, India, personal addresses, a regulated sector, any list of unclear origin, or a call plan that uses automated dialling, AI voices or recording.

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
