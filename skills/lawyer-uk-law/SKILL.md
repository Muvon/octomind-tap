---
name: lawyer-uk-law
title: "UK Law Research: England, Scotland, N. Ireland"
description: "UK law research from legislation.gov.uk with point-in-time versions, amendment tracking and assimilated EU law: employment, contracts, tenancy, data."
license: Apache-2.0
compatibility: "Needs web search and the legislation.gov.uk tools. Covers England and Wales, Scotland and Northern Ireland."
capabilities: legal-uk
domains: lawyer
rules:
  - match((?i)\b(uk|u\.k\.|united kingdom|british|england|welsh|wales|scottish|scotland|northern ireland|english law)\b.{0,80}\b(law|laws|legal|legislation|statute|court|tribunal|solicitor|barrister|rights|tenant|landlord|dismissal|employer)\b)
  - match((?i)\b(law|legal|legislation|court|tribunal|rights)\b.{0,60}\b(in|under|of)\s+(the\s+)?(uk|united kingdom|england|scotland|wales|northern ireland)\b)
  - match((?i)\b(legislation\.gov\.uk|employment rights act|renters'? rights act|equality act 2010|consumer rights act|assimilated law|retained eu law|acas early conciliation|section 21 eviction)\b)
  - semantic(what does UK law say about my employment rights)
  - semantic(can my landlord in England evict me and what notice is needed, 0.74)
  - semantic(has this UK statute been amended and what did it say earlier, 0.72)
---

## Overview

This skill covers UK legal information across England and Wales, Scotland and Northern Ireland: legislation, rights, obligations and procedures, statute and case-law research, assimilated (formerly retained) EU law, and document and contract review. Legislation comes live from legislation.gov.uk, including point-in-time versions and amendment tracking. It does not cover non-UK law.

## Mental model

The UK has three legal systems, so the first question is which one applies. Post-Brexit EU-derived law survives only as assimilated law. A Royal Assent date is not a commencement date: many 2025 Acts commence in stages by regulations, so every provision needs a status check before it is stated as law.

## Rules

### Research tools

Live UK legislation from legislation.gov.uk:
- `leg_search`, `leg_search_advanced`, `leg_search_new`: search legislation by title, text, type and year.
- `leg_get`, `leg_get_section`, `leg_get_contents`: fetch an Act or SI, a single section, or its table of contents.
- `leg_get_version`: point-in-time version of a provision (the law as it stood on a date).
- `leg_status`: in-force or repealed status of a document.
- `leg_changes_affecting`, `leg_changes_by`: amendment tracking in both directions (what amended this; what this amends).
- `leg_types`, `leg_updates`: legislation types (including assimilated EU law) and the updates feed.
- `leg_sparql`: structured queries against the legislation.gov.uk data.

Use web search for recent case law (The National Archives Find Case Law at caselaw.nationalarchives.gov.uk, BAILII), bill progress (bills.parliament.uk), commencement regulations, news and Law Commission reports.

### Research protocol

1. Identify the jurisdiction: England and Wales, Scotland, or Northern Ireland.
2. Search with `leg_search`, then retrieve the exact text with `leg_get_section` (`leg_get_version` for the law on a past date).
3. Check currency with `leg_status` plus `leg_changes_affecting` to confirm the provision is in force and catch amendments.
4. Quote only provisions you retrieved; never cite from memory.
5. Use web search for case law, commencement regulations, the original EU act behind assimilated law, and recent developments.

Confirm which UK legal system applies and verify against current official sources (legislation.gov.uk). Assimilated law was renamed and partly revoked by the Retained EU Law (Revocation and Reform) Act 2023.

### The three systems

| Jurisdiction | Courts | Key differences |
|---|---|---|
| England and Wales | Supreme Court → Court of Appeal → High Court → Crown/County Courts | Common law; most legislation |
| Scotland | Supreme Court → Court of Session / High Court of Justiciary → Sheriff Courts | Scots law (mixed civil/common); distinct family and property law |
| Northern Ireland | Supreme Court → Court of Appeal → High Court → Crown/County Courts | Largely mirrors England and Wales but with some distinct legislation |

In England and Wales civil claims start in the County Court (High Court for large cases), criminal cases in the Magistrates' or Crown Court; tribunals handle employment, immigration and benefits.

### Employment law

- Employment Rights Act 1996: core employment rights. The Employment Rights Act 2025 (Royal Assent 18 Dec 2025) phases in amendments through 2027.
- Equality Act 2010: protected characteristics are age, disability, gender reassignment, marriage and civil partnership, pregnancy and maternity, race, religion or belief, sex, sexual orientation.
- National Living Wage: 2026: £12.71/hr for 21+ from 1 April 2026; rates change every April.
- Unfair dismissal: 2 years' continuous employment until 31 Dec 2026; the 2025 Act cuts this to 6 months and removes the compensatory cap from 1 Jan 2027 (as of 2026-11).
- Day-one rights from April 2026: statutory sick pay from the first day of absence, paternity leave and unpaid parental leave.
- Tribunal claims: ACAS early conciliation is required before most claims. The limit is 3 months less one day from the act or dismissal, and 6 months where the act or dismissal is on or after 1 Oct 2026 (for a series of acts, the last must fall on or after that date); earlier acts keep 3 months (as of 2026-11).
- Redundancy pay after 2 years; TUPE 2006; IR35 for contractors.

### Contract law

- Consumer Rights Act 2015: consumer goods, services, digital content, unfair terms. Unfair Contract Terms Act 1977 for business contracts.
- Limitation Act 1980: 6 years for contract and most tort claims, 12 for deeds, 3 for personal injury (Scotland: mostly 5-year prescription).
- Small claims: England and Wales small claims track up to £10,000; Scotland simple procedure up to £5,000; Northern Ireland small claims up to £5,000.
- Digital Markets, Competition and Consumers Act 2024: the CMA can fine directly for consumer-law breaches (up to 10% of global turnover) since 6 April 2025; fake reviews and drip pricing are banned; the subscription-contract rules are not yet in force (expected 2027 at the earliest).

### Property law

- HM Land Registry; conveyancing runs exchange to completion; leasehold reform is ongoing (Leasehold and Freehold Reform Act 2024 commencing in stages).
- Renters' Rights Act 2025 (England): from 1 May 2026 section 21 no-fault evictions ended and assured shorthold tenancies became assured periodic tenancies; landlords need a section 8 ground; the landlord database and ombudsman follow in later phases.
- Wales uses the Renting Homes (Wales) Act 2016 (occupation contracts); Scotland uses private residential tenancies. The rules differ.

### Criminal law

- PACE 1984 governs police powers and detention; right to free legal advice at the police station; the CPS decides whether to prosecute.
- Magistrates' Court: summary and either-way offences; up to 12 months' custody for either-way offences (since Nov 2024).
- Crown Court: indictable offences; jury trial. The Courts and Tribunals Bill (2026) proposes ending the defendant's right to elect jury trial for either-way offences; check bills.parliament.uk for its stage.

### Data protection and privacy

- UK GDPR plus Data Protection Act 2018, amended by the Data (Use and Access) Act 2025; most changes in force from 5 Feb 2026 (SI 2026/82: recognised legitimate interests, looser automated decision-making rules, wider cookie exemptions).
- Complaints: from 19 June 2026 controllers must run a complaints process; people should normally complain to the organisation first, then the regulator.
- ICO: enforcement body, being restructured as the Information Commission under the 2025 Act.
- PECR: cookies and electronic marketing; fines now reach UK GDPR levels.

### Other areas (verify specifics on legislation.gov.uk)

- Business: Companies Act 2006 (Companies House identity verification phasing in from Nov 2025), Insolvency Act 1986, Competition Act 1998 (CMA).
- IP: CDPA 1988 (copyright life + 70 years), Trade Marks Act 1994, Patents Act 1977; separate UK and EU rights post-Brexit.
- Family: no-fault divorce since April 2022 (Divorce, Dissolution and Separation Act 2020); Children Act 1989 welfare principle; Child Maintenance Service.
- Immigration: points-based system (Skilled Worker, Student, Family); EU Settlement Scheme status; rules change by Statement of Changes several times a year, so check gov.uk/ukvi.

### Legal aid and resources

- Citizens Advice (Citizens Advice Scotland, Advice NI) and GOV.UK: free general guidance.
- Legal aid: Legal Aid Agency (England and Wales), Scottish Legal Aid Board, Legal Services Agency NI.
- Find a solicitor: Law Society (and Law Society of Scotland / of NI); barristers via barcouncil.org.uk, some by direct public access.
- Shelter (housing), ACAS (employment, early conciliation), ICO (data protection).
- Ombudsmen: Financial, Housing and Legal Ombudsman are free alternatives to court.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Jurisdiction: England and Wales, Scotland, Northern Ireland, or UK-wide.
2. Applicable legislation with validated citations.
3. Plain-language explanation.
4. Post-Brexit points where EU history matters.
5. Key case law.
6. Practical implications.
7. Deadlines (limitation, tribunal, notice periods), first if urgent.
8. Next steps and when to get a solicitor.
9. Resources: GOV.UK, Citizens Advice, legal aid.

## Checklist

- [ ] Which of the three UK legal systems applies is confirmed, not assumed.
- [ ] Every provision quoted was retrieved with `leg_get_section`, and `leg_status` shows it in force.
- [ ] Commencement was checked, not just Royal Assent.
- [ ] Assimilated-law status is noted where EU history matters.
- [ ] The tightest deadline appears first when one applies.

## Composition / References

- legislation.gov.uk for statutes; caselaw.nationalarchives.gov.uk and BAILII for case law; bills.parliament.uk for bills.
