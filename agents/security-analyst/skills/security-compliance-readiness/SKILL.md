---
name: security-compliance-readiness
title: "SOC 2 and GDPR Compliance Readiness: DPIAs, Policies"
description: "Maps GDPR, CCPA, SOC 2 compliance, ISO 27001, NIS2, and DORA duties to team actions: data maps, DPIAs, policy drafts, questionnaires. Not legal advice."
license: Apache-2.0
compatibility: "Requires: web search and web fetch for regulator texts and current thresholds. Jurisdiction-dependent claims need counsel."
rules:
  - match((?i)\b(gdpr|ccpa|cpra|iso ?27001|nis2|hipaa|pci[- ]dss|cyber resilience act)\b)
  - match(\bDORA\b)
  - match((?i)\bsoc ?2\b.{0,80}\b(readiness|gap|control checklist|trust services|type (i|ii)|observation|evidence|first audit)\b)
  - match((?i)\b(privacy policy|data map|dpia|data protection impact|records of processing|data[- ]subject (request|access)|dsar|lawful basis|cookie (banner|consent))\b)
  - match((?i)\b(answer|draft|fill( out| in)?|complete|respond to)\b.{0,40}\b(security|vendor|customer) questionnaire\b|\b(vsaq|caiq|sig lite)\b)
  - match((?i)\bnotification clocks?\b|\bnotify\b.{0,30}\b(regulator|authorit\w+|supervisory authority|data protection authority)\b|\bbreach[- ](notification|response) (memo|orientation)\b)
  - semantic(what do we need to do to get SOC 2 or ISO 27001 ready)
  - semantic(help me fill in this customer security questionnaire, 0.74)
  - semantic(do a data protection impact assessment and draft the GDPR privacy policy)
---

## Overview

This skill translates regulatory frameworks (GDPR, CCPA/CPRA, SOC 2, ISO 27001, and the EU security relatives NIS2, DORA, and the Cyber Resilience Act) into what a software team or small business must actually do: data maps, lawful bases, DPIAs, control checklists, policy drafts, and questionnaire answers. It is educational and draft-producing, not a law firm. Teach the pattern, search the current specifics, mark every jurisdiction-dependent claim for counsel, and never bless anything as "compliant": readiness is assessable here, compliance is a lawyer's word.

## Rules

### What this skill covers

Applicability triage (which regimes touch this product), data mapping and records of processing, lawful-basis analysis, privacy-policy and notice drafts, DPIA structure and drafting, data-subject-request procedures, SOC 2 and ISO 27001 readiness (gap assessment, control checklist, evidence habits), security-regime applicability (NIS2, DORA, CRA, PCI DSS), breach-response orientation including which notification clocks apply, and vendor security-questionnaire answers.

Not covered: legal rulings, contracts, and representation (mandatory escalation to a lawyer for enforcement, disputes, and DPAs with big customers), application-security testing, LLM-specific injection defense, AI Act classification and AI governance programs, and infrastructure hardening implementation.

### Steps

1. Scope the exposure: what is built, what personal data flows through it, where users and servers sit, headcount and revenue (thresholds care), and B2B versus B2C. Applicability comes from users' locations, not the company's address: a Delaware SaaS with EU users is in GDPR scope.
2. Map the data first. You cannot protect or lawfully process what you haven't inventoried. Per flow: what data, from whom, why (purpose), lawful basis, where stored, who touches it (processors), retention, and cross-border paths. This map is the foundation artifact for everything else.
3. Gap-assess against the applicable regimes, using the patterns below plus web search for current thresholds, court shifts, and adequacy status. Fetch the regulator's primary text with the `knowledge` tool rather than trusting summaries. Label every regime-specific number "verify current".
4. Draft the artifacts (policies, notices, DPIAs, procedures, questionnaire answers) grounded in the actual data map, never boilerplate that claims practices the product doesn't have. A privacy policy that overpromises is evidence against you.
5. Build the habits. Compliance is a loop, not a document: review dates on every artifact, evidence collection as a routine (SOC 2 lives or dies here), and a re-check trigger list (new data type, new vendor, new market, new AI feature).
6. Escalate honestly: enforcement letters, a breach with real exposure, customer DPA redlines, and novel legal questions go to a lawyer for the user's jurisdiction, with your prepared factual summary. Persist the data map and decisions to memory or files.

### GDPR working knowledge (pattern level; verify specifics per case)

- Lawful bases: consent is the last resort, not the default. Contract necessity, legal obligation, and legitimate interest (with a documented balancing test) usually fit better. Consent must be granular, withdrawable, and un-bundled from service access.
- Data-subject rights: access, rectification, erasure, portability, objection. One month to respond (extendable once). You need a working procedure, not a policy paragraph.
- Roles: the controller decides why and how; the processor acts on instructions. Every processor needs a DPA, and sub-processors are disclosed.
- Transfers out of the EEA: an adequacy decision, or SCCs plus a transfer impact assessment. The EU-US Data Privacy Framework survived the General Court (Latombe, September 2025) but an appeal is pending at the CJEU (C-703/25 P): keep SCCs as the fallback and search for the current status.
- Breach: 72 hours to the supervisory authority when risky, and affected individuals when high-risk. The clock starts at awareness. An internal incident log is required even for non-notified events.
- DPIA triggers: systematic profiling, large-scale sensitive data, public monitoring, new-technology processing (AI features commonly qualify). Structure: description, necessity and proportionality, risks to individuals, mitigations, residual risk and sign-off.
- Privacy by design defaults: minimize collection, purpose-bind, a retention schedule with actual deletion, pseudonymize where feasible.
- The Digital Omnibus GDPR amendments (proposed November 2025) are still under negotiation: don't treat them as law until adopted.

### CCPA/CPRA and the US patchwork

Applicability is threshold-based (revenue or records volume; verify current numbers). Rights: know, delete, correct, and opt out of sale or sharing (the GPC signal is honored). "Sale" is defined disturbingly broadly: adtech data flows count. The CPPA (CalPrivacy) regulations in force since 1 January 2026 add ADMT duties (comply by 1 January 2027), risk assessments (attestations due from April 2028), and cybersecurity audits (certifications phased April 2028 to 2030 by revenue). US state laws multiply yearly: search the map when a US audience matters.

### SOC 2 readiness

- Type I is design at a point in time; Type II is operating effectiveness over 3-12 months. Customers increasingly accept only Type II, so the observation window means starting the habits now.
- Security (the common criteria) is mandatory. Add Availability or Confidentiality only if customers demand them: each added criterion is added audit surface.
- The controls that fail most: offboarding (access revoked within 24 hours, with evidence), quarterly access reviews (documented, not "we looked"), change management (PRs and approvals as evidence), vendor review, tested backups, and an incident-response document that has been exercised once.
- ISO/IEC 27001: only the 2022 edition is certifiable; the transition from 2013 ended 31 October 2025. Annex A has 93 controls in four themes, and the Statement of Applicability justifies every inclusion and exclusion. SOC 2 evidence maps onto it, so build one control set and map both.
- Evidence discipline beats heroics: screenshots and exports collected monthly into an organized folder turn the audit from archaeology into paperwork.

### EU security regimes and payments (as of 2026-10; verify per case)

- NIS2: essential and important entities by sector and size; national transposition is uneven, so read the member-state law. Incidents: early warning at 24 hours, notification at 72 hours, final report at one month. Management bodies are personally accountable.
- DORA (EU financial entities, applies since 17 January 2025): ICT risk framework, register of ICT third-party arrangements, resilience testing. Major ICT incidents are reported within 4 hours of classification and no later than 24 hours after awareness.
- Cyber Resilience Act: since 11 September 2026, manufacturers of products with digital elements report actively exploited vulnerabilities and severe incidents through ENISA's Single Reporting Platform (24-hour early warning, 72-hour notification, final report). The rest applies from 11 December 2027.
- PCI DSS 4.0.1: all future-dated requirements became mandatory 31 March 2025 (payment-page script controls, MFA for all cardholder-data-environment access, targeted risk analyses).
- US public companies (SEC): Form 8-K Item 1.05 within four business days of determining an incident is material; annual cyber risk-management and governance disclosure in the 10-K.

### Questionnaires and policies

Answer what is true today: "No, planned for Q3" beats a yes that a breach later disproves. Misrepresentation in a questionnaire is contract-fraud territory. Policies state what you actually do, dated, owned, and review-scheduled. Copying a competitor's policy imports their practices as your promises.

## Examples

- "Does GDPR/CCPA apply to us?": triage questions (users where, what data, thresholds), then an applicability verdict with the reasoning, labeled as orientation.
- "Write our privacy policy": data map first (build it if missing), then a policy from actual practices, counsel flags marked.
- "We want SOC 2": the Type I versus II decision, a gap assessment, and an evidence-habit plan with the observation-window math.
- "We had a breach": the orientation checklist (contain, assess, log, notify decision), every clock that may apply (GDPR 72 hours, NIS2 24-hour early warning, DORA 4 hours after classification, SEC four business days, US state laws), then lawyer escalation prepared. Urgent and calm.
- Ambiguous: ask one question (usually "where are your users, and what personal data do you actually collect?"), then proceed.

## Output format

- Data maps as `data-map.md` tables: flow, data, purpose, basis, location, processors, retention.
- Gap assessments as: applicable regime, requirement, current state, gap, action, ranked by risk.
- Drafts (`privacy-policy.md`, `dpia-<feature>.md`, procedures) with every verify-with-counsel clause explicitly marked.
- Questionnaire answers as: question, honest answer, evidence pointer.

## Checklist

- [ ] The data map exists before any downstream artifact.
- [ ] Nothing is declared "compliant" and no legal advice is given; jurisdiction rulings went to counsel.
- [ ] No draft or answer claims a practice the team doesn't have.
- [ ] Every threshold, deadline, and transfer-framework status was searched and labeled "verify as of <date>".
- [ ] Enforcement contact, real breaches, and DPA negotiations were escalated to counsel with the facts prepared.

## Composition / References

- `threat-modeling` skill: design-level security analysis that feeds a DPIA's risk section.
