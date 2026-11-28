---
name: lawyer-singapore-law
title: "Singapore Law Research: Statutes Online at Source"
description: "Singapore law read from Singapore Statutes Online: contracts, employment, criminal, company, data protection, property, immigration, strict enforcement."
license: Apache-2.0
compatibility: "Needs web search and page reading (search plus knowledge read) against sso.agc.gov.sg and court judgment sites."
capabilities: webfetch
domains: lawyer
rules:
  - match((?i)\b(companies act 1967|penal code 1871|employment act 1968|housing and development act|land titles act 1993|misrepresentation act 1967|sgca|sghc|slr|hdb resale|on sso)\b)
  - match((?i)\b(singapore|singaporean)\b.{0,80}\b(law|laws|legal|legislation|statute|court|lawyer|rights|tenant|landlord|dismissal|employer|penalty)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+singapore\b)
  - match((?i)\b(sso\.agc|singapore statutes|employment claims tribunal|tadm|absd|elitigation|siac)\b)
  - semantic(what does Singapore law say about my employment contract, 0.80)
  - semantic(how does Singapore's data protection law apply to my company, 0.74)
  - semantic(what are the penalties for this offence in Singapore, 0.74)
---

## Overview

This skill covers Singapore legal information: Acts, rights, obligations and procedures, legislation and case-law research, citation validation, and document and contract review. It researches Singapore legislation on Singapore Statutes Online (sso.agc.gov.sg), reading the current revised text itself before relying on it. It does not cover non-Singapore law.

## Mental model

Singapore has a common-law base with significant statutory modifications and local context, and enforcement is strict: penalties can be severe. English common law applies where there is no local statute (Application of English Law Act). Every section number cited must appear in text you actually read. Figures that change are stamped with their year; confirm them on the agency site (MOM, IRAS, ICA) before relying on them.

## Rules

### Sources and research protocol

Sources, in order of authority: Singapore Statutes Online (sso.agc.gov.sg) for the current version of each Act and subsidiary legislation, with its timeline of amendments; then Court of Appeal and High Court judgments (elitigation.sg, judiciary.gov.sg), ministry and AGC guidance, and recent developments. Find the page with `search`, open it with `knowledge(command="read")`, and quote from what you read, never from memory. Name the source and the version date you used.

1. Identify the legal area: contract, criminal, employment, company, property, family and so on.
2. Find the Act with `search` using `site:sso.agc.gov.sg` plus the Act name or topic.
3. Read the provision: open the current version with `knowledge(command="read")`.
4. Check currency: check the version date and the amendment timeline for changes not yet in force.
5. Verify citations: every section number you cite must appear in the text you read.
6. Use web search for Court of Appeal and High Court decisions (lawnet.sg, elitigation.sg).

Verify against current official sources (sso.agc.gov.sg); law changes.

### Court system

```
Court of Appeal (highest appellate court)
    ↑
Appellate Division of the High Court
    ↑
General Division of the High Court
    ↑
State Courts:
  - District Courts (civil up to $250K; offences with max. 10 years' imprisonment)
  - Magistrates' Courts (civil up to $60K; offences with max. 5 years, sentence up to 3 years)
  - Community Courts / Family Justice Courts / Employment Claims Tribunal
    ↑
Small Claims Tribunals (up to $20K, $30K by consent) / Community Disputes Resolution Tribunals (neighbour disputes)
```

Disputes hub: SICC (international commercial cases, foreign counsel can appear), SIAC arbitration under the International Arbitration Act (UNCITRAL Model Law), SIMC mediation. Common law, unitary state: binding precedent.

### Contract law

- Common law: offer, acceptance, consideration, intention, capacity.
- Contracts (Rights of Third Parties) Act: third-party enforcement.
- Unfair Contract Terms Act: reasonableness test for exclusion clauses.
- Consumer Protection (Fair Trading) Act: unfair practices; CASE.
- Electronic Transactions Act: electronic contracts and signatures.
- Limitation Act: 6 years for contract claims.

### Employment law

- Employment Act: core employment rights; covers all employees since April 2019 (except seafarers, domestic workers, public officers). Part 4 protections (hours, overtime, rest days) apply only to workmen earning up to $4,500/month and non-workmen up to $2,600/month.
- Key entitlements: annual leave (7-14 days), sick leave, public holidays (11 days).
- CPF: Central Provident Fund; mandatory savings (employer plus employee contributions).
- Work Injury Compensation Act: workplace injury compensation.
- Employment of Foreign Manpower Act: work pass requirements.
- Retirement and Re-employment Act: 2026: minimum retirement age 64, re-employment to 69 (from 1 July 2026).
- Platform Workers Act 2024: CPF and work-injury cover for ride-hail and delivery workers since 1 Jan 2025.
- Tripartite Guidelines on Fair Employment Practices: the operative anti-discrimination standard until the Workplace Fairness Act 2025 commences (expected by end-2027); check status.
- Employment Claims Tribunal: salary and wrongful-dismissal claims after mandatory TADM mediation.

### Criminal law

- Penal Code: main criminal statute; comprehensive.
- Criminal Procedure Code: procedure, arrest, bail, trial.
- Misuse of Drugs Act: death penalty for trafficking above thresholds; life imprisonment and caning possible only for couriers who meet s. 33B conditions.
- Public Order Act: demonstrations, assemblies. Maintenance of Religious Harmony Act: religious harmony.
- Right to counsel upon arrest; the right to contact a lawyer.
- Bail: available for most offences; denied for capital offences.

### Company law

- Companies Act, LLP Act, Business Names Registration Act (ACRA); Securities and Futures Act (MAS); Insolvency, Restructuring and Dissolution Act 2018.

### Data protection

- Personal Data Protection Act (PDPA) 2012: PDPC enforcement; notify the PDPC within 3 calendar days of assessing a breach notifiable; Do Not Call Registry for marketing.
- Fines up to 10% of Singapore turnover (organisations above $10M) or $1M, since 1 Oct 2022.

### Property law

- Land Titles Act: Torrens system; indefeasible title.
- Residential Property Act: restrictions on foreign ownership of landed property.
- Housing Development Act: HDB public housing; eligibility rules.
- Conveyancing and Law of Property Act: property transactions.
- Stamp Duties Act: ABSD 2026: foreigners 60%, citizens 0% first / 20% second / 30% third and further (some FTA nationals get citizen rates).

### Family law

- Women's Charter: marriage, divorce, maintenance, custody (non-Muslims); divorce by mutual agreement available since 1 July 2024.
- Administration of Muslim Law Act (AMLA): Muslim personal law; Syariah Court.
- Guardianship of Infants Act: child welfare.
- Intestate Succession Act: intestate inheritance (non-Muslims). Probate and Administration Act: estate administration.

### Immigration

- Immigration Act: entry, stay and departure.
- Employment Pass: 2026: at least $5,600/month ($6,200 financial services), rising with age, plus the COMPASS points test; new applications from 1 Jan 2027: $6,000 ($6,600 FS).
- S Pass: 2026: at least $3,300/month ($3,800 FS); from 1 Jan 2027: $3,600 ($4,000 FS).
- Work Permit: semi-skilled workers; sector quotas and levies.
- Permanent Residence and citizenship: discretionary, via ICA.

### Intellectual property

- Patents Act (20 years), Trade Marks Act, Copyright Act 2021 (life + 70, automatic), Registered Designs Act; IPOS.

### Online harms

- Online Safety (Relief and Accountability) Act 2025: the Online Safety Commission has operated since 29 June 2026; victims of intimate-image abuse, doxxing, harassment and stalking can seek takedown orders.

### Resources

- sso.agc.gov.sg (legislation), elitigation.sg (judgments), lawnet.sg (subscription case law).
- Legal Aid Bureau (mlaw.gov.sg) and Pro Bono SG: means-tested civil legal aid and free clinics; Law Society (lawsociety.org.sg) to find a lawyer.
- Agencies: acra.gov.sg, mom.gov.sg, pdpc.gov.sg, ica.gov.sg.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Applicable legislation: key Acts with validated citations.
2. Plain-language explanation.
3. Strict enforcement note: where Singapore has particularly strict rules.
4. Case law: key Court of Appeal and High Court decisions (via web search).
5. Practical implications.
6. Deadlines: limitation periods, filing deadlines.
7. Next steps: options, when to get an Advocate and Solicitor.
8. Resources: sso.agc.gov.sg, MOM, ACRA, PDPC.

## Checklist

- [ ] The legal area is identified and the governing Act was read at the source.
- [ ] Every section number cited appears in the text you opened.
- [ ] Strict-enforcement areas (drugs, public order) are not understated.
- [ ] The version date and any pending amendments are named.
