---
name: lawyer-australia-law
title: "Australian Law Research: Federal Acts at the Source"
description: "Australian federal law read from legislation.gov.au with AustLII case law; state and territory law flagged. Employment, consumer, privacy, family."
license: Apache-2.0
compatibility: "Needs web search and page reading (search plus knowledge read). Federal scope; state and territory law comes from state legislation sites."
capabilities: webfetch
rules:
  - match((?i)\(cth\)|\b(copyright act 1968|corporations act 2001|spam act 2003|bankruptcy act 1966|privacy act 1988|franchising code|competition and consumer act|small business exemption|adelaide|sydney|melbourne|brisbane|canberra)\b)
  - match((?i)\b(australia|australian|nsw|new south wales|queensland|victorian|western australia)\b.{0,80}\b(law|laws|legal|legislation|statute|court|tribunal|solicitor|rights|tenant|landlord|dismissal|employer)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+(australia|nsw|queensland|new south wales)\b)
  - match((?i)\b(fair work act|fair work commission|australian consumer law|legislation\.gov\.au|austlii|accc|afca|migration act 1958|privacy act 1988)\b)
  - semantic(what does Australian law say about unfair dismissal at work, 0.74)
  - semantic(my landlord in Australia will not return my bond, what are my rights, 0.74)
  - semantic(is this a privacy or consumer law breach under Australian legislation, 0.74)
---

## Overview

This skill covers Australian federal legal information: Acts, rights, obligations and procedures, legislation and case-law research, citation validation, and document and contract review. It researches Commonwealth Acts on the Federal Register of Legislation (legislation.gov.au), reading the current compilation itself before relying on it. State and territory law (much criminal, property and family law) is researched on the official state and territory legislation sites, with a clear note that it sits outside the federal compilation. It does not cover non-Australian law.

## Mental model

Federal law is only part of the picture: criminal, property and tenancy law vary by state and territory, so the first question is federal or state, and which state. Every section number cited must appear in text you actually read.

## Rules

### Sources and research protocol

Sources, in order of authority: the Federal Register of Legislation (legislation.gov.au) for the current compilation of each Act and its amendment history; aph.gov.au for bills; then High Court and Federal Court decisions (austlii.edu.au, hcourt.gov.au), state and territory legislation sites, and ALRC reports. Find the page with `search`, open it with `knowledge(command="read")`, and quote from what you read, never from memory. Name the source and the compilation date you used.

1. Identify the jurisdiction: federal or state/territory, and which state.
2. Find the Act with `search` using `site:legislation.gov.au` plus the Act name or topic.
3. Read the provision: open the current compilation with `knowledge(command="read")`.
4. Check currency: check the compilation date and any amending Acts or bills not yet incorporated.
5. Verify citations: every section number you cite must appear in the text you read.
6. Use web search for High Court decisions (austlii.edu.au) and ALRC reports.

Verify against current official sources (legislation.gov.au); law changes.

### Constitution and courts

- Constitution of the Commonwealth of Australia (1901): federal structure.
- Section 51: federal legislative powers (trade, corporations, taxation and others).
- Section 109: federal law prevails over inconsistent state law.
- Implied rights: freedom of political communication (implied constitutional right).

Courts: High Court → Federal Court / Federal Circuit and Family Court (FCFCOA) and state/territory Supreme Courts → District/County Courts → Magistrates/Local Courts. Tribunals include the Administrative Review Tribunal (ART, replaced the AAT in Oct 2024) and state tribunals (NCAT, VCAT, QCAT).

### Employment law

- Fair Work Act 2009: 11 National Employment Standards, modern awards, enterprise agreements; the Fair Work Commission handles unfair dismissal and general protections.
- Unfair dismissal: 6 months' service (12 months for small business); lodge with the FWC within 21 days of dismissal. For 2026 the high income threshold is $190,100 and the compensation cap $95,050 from 1 July 2026 (award or agreement coverage keeps access above the threshold).
- General protections: adverse action for exercising workplace rights; also a 21-day deadline when dismissed.
- Work Health and Safety Act 2011: model WHS framework (adopted by all jurisdictions except Victoria).
- Superannuation Guarantee: 12% (from 1 July 2025); Payday Super from 1 July 2026 requires super to reach the fund within 7 business days of each payday.
- Non-competes: enforceability currently depends on reasonableness (and NSW restraints legislation). A 2026 exposure-draft bill would ban them for workers under the high income threshold from 2027; it is not law yet.

### Consumer law

- Australian Consumer Law (ACL): Schedule 2 of the Competition and Consumer Act 2010.
- Consumer guarantees are automatic and cannot be excluded.
- Misleading conduct: section 18 ACL; a broad prohibition.
- Unfair contract terms: B2C and small-business B2B; prohibited with penalties since November 2023.
- ACCC: Australian Competition and Consumer Commission; enforcement.
- Scams Prevention Framework Act 2025: obligations on banks, telcos and digital platforms to prevent and respond to scams, phased in by sector rules.
- AFCA: free external dispute resolution for complaints against banks, insurers, super funds and other financial firms.
- Small claims: run by state and territory tribunals and local courts (NCAT, VCAT, QCAT and others); limits vary, so check live.

### Contract law

- Common law formation; the ACL overlays consumer contracts; Electronic Transactions Act 1999 for e-signatures.
- Limitation periods: generally 6 years (varies by state).

### Criminal law

- Mostly state and territory law (own Criminal Codes or common law, bail acts); federal offences under the Criminal Code Act 1995 (AFP); right to silence and to legal representation.

### Privacy and data protection

- Privacy Act 1988: Australian Privacy Principles (APPs); applies to entities with more than $3M turnover.
- Notifiable Data Breaches (NDB) scheme: mandatory breach notification.
- OAIC: Office of the Australian Information Commissioner; enforcement.
- Privacy Act reform: Privacy and Other Legislation Amendment Act 2024. A statutory tort for serious invasions of privacy has been in force since 10 June 2025; automated-decision transparency in privacy policies applies from 10 Dec 2026; a Children's Online Privacy Code is in development; further tranches (including removing the small business exemption) are not yet legislated.
- Online safety: the social media minimum age of 16 applies from 10 Dec 2025 (platforms must take reasonable steps).

### Business and corporations law

- Corporations Act 2001 and ASIC: company formation, directors' duties, reporting; insolvency (personal: Bankruptcy Act 1966).
- Competition and Consumer Act 2010: antitrust; ACCC enforcement; mandatory, suspensory merger notification to the ACCC from 1 Jan 2026.

### Property law

- Primarily state law: each state has its own property legislation.
- Torrens title system: indefeasible title upon registration.
- Residential Tenancies Acts: state-based; strong tenant protections.
- Foreign Investment Review Board (FIRB): foreign property purchases.

### Family law

- Family Law Act 1975: federal; divorce, property settlement, parenting arrangements.
- No-fault divorce: 12 months' separation required.
- Property settlement: since 10 June 2025 the Act sets out the property steps in statute and requires courts to consider the economic effects of family violence.
- Best interests of the child: primary consideration in parenting matters.
- Federal Circuit and Family Court of Australia (FCFCOA): jurisdiction over family matters.

### Immigration

- Migration Act 1958: visa framework. Department of Home Affairs: visa applications.
- Visa categories: skilled (189, 190, 491), employer-sponsored (482 Skills in Demand, which replaced the TSS in Dec 2024; 186), family, student, visitor.
- Paid immigration assistance: only registered migration agents (OMARA register) or Australian legal practitioners; check the register.
- Australian citizenship: Australian Citizenship Act 2007.

### Intellectual property

- Patents Act 1990 (20-year standard patent), Trade Marks Act 1995, Designs Act 2003 (IP Australia); Copyright Act 1968 (life + 70 years, automatic).

### Resources

- Federal Register of Legislation: legislation.gov.au. AustLII: austlii.edu.au (free case law database).
- ACCC: accc.gov.au (consumer protection). ASIC: asic.gov.au (corporations).
- Fair Work Ombudsman: fairwork.gov.au. OAIC: oaic.gov.au (privacy). AFCA: afca.org.au (financial complaints).
- Legal Aid: each state and territory has a Legal Aid Commission; community legal centres give free advice.
- Law societies: each state has one for solicitor referrals.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Jurisdiction: federal or state/territory, which state.
2. Applicable legislation: key Acts with validated citations.
3. Plain-language explanation.
4. State variations: where state law differs significantly.
5. Case law: key High Court and Federal Court decisions (via web search).
6. Practical implications.
7. Deadlines: limitation periods, filing deadlines.
8. Next steps: options, when to get a solicitor.
9. Resources: legislation.gov.au, legal aid, law societies.

## Checklist

- [ ] Federal versus state or territory is confirmed, and state matters are flagged as outside the federal compilation.
- [ ] Every section number cited appears in the compilation text you opened.
- [ ] The compilation date and any pending amendments are named.
- [ ] The tightest deadline (for example the 21-day dismissal window) appears when one applies.
