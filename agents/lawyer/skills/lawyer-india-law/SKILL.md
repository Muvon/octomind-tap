---
name: lawyer-india-law
title: "Indian Law Research: Central Acts, BNS, DPDP"
description: "Indian central law read from India Code: Constitution, BNS/BNSS/BSA criminal codes, CPC, Labour Codes, DPDP Act, limitation periods; state law flagged."
license: Apache-2.0
compatibility: "Needs web search and page reading (search plus knowledge read). Central Acts only; state and UT law comes from state legislature sites."
capabilities: webfetch
rules:
  - match((?i)\b(bharatiya|sanhita|adhiniyam|indian contract act|code of civil procedure|supreme court of india|labour codes?|industrial relations code|code on wages|code on social security|constitution of india|limitation act,? 1963|india code|puttaswamy|basic structure|order vii)\b)
  - match(\(\d{4}\)\s*\d+\s*SCC|\bAIR\s+\d{4}\b|\bSCC\b.{0,30}\b(AIR|SCR)\b)
  - match((?i)\b(bengaluru|bangalore|mumbai|delhi|chennai|kolkata|hyderabad)\b.{0,160}\b(act|agreement|contract|court|law|legal)\b)
  - match((?i)\b(india|indian)\b.{0,80}\b(law|laws|legal|legislation|statute|court|advocate|lawyer|rights|tenant|landlord|dismissal|employer)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+india\b)
  - match((?i)\b(ipc|bns|bnss|indian penal code|crpc|indiacode|dpdp act|negotiable instruments act|specific relief act|rera|limitation act 1963)\b)
  - semantic(what do the new Indian criminal codes say about this offence, 0.74)
  - semantic(what are my rights under Indian labour or data protection law, 0.74)
  - semantic(what is the limitation period for filing a case in India)
---

## Overview

This skill covers Indian central (federal) legal information: Acts, constitutional rights, obligations and procedures, legislation and case-law research, citation validation, and document and contract review. It researches Central Acts from India Code (indiacode.nic.in) and the Gazette, reading the official text itself before relying on it. State and UT law is researched on the official state legislature and gazette sites, with a clear note that it sits outside the Central Acts. It does not cover non-Indian law.

## Mental model

India's 28 states and 8 UTs have their own laws, and Indian law is under major reform: many central laws were recently replaced. The first questions are central or state, and when the facts occurred. Every section number cited must appear in text you actually read. Figures that change are stamped with their year; confirm them by web search before relying on them.

## Rules

### Sources and research protocol

Sources, in order of authority: India Code (indiacode.nic.in) for consolidated Central Acts; the e-Gazette (egazette.gov.in) for new Acts, rules and commencement notifications; then Supreme Court and High Court judgments (sci.gov.in, indiankanoon.org) and Law Commission reports. Find the page with `search`, open it with `knowledge(command="read")`, and quote from what you read, never from memory. Name the source and the version date you used.

1. Identify the jurisdiction: Central Act or State law, and which state.
2. Find the Act with `search` using `site:indiacode.nic.in` plus the Act name or topic.
3. Read the provision: open the section text with `knowledge(command="read")`.
4. Check currency: look for amendments, repeal or replacement and the commencement notification in the e-Gazette (critical, because many laws were recently replaced).
5. Verify citations: every section number you cite must appear in the text you read.
6. Use web search for Supreme Court decisions (indiankanoon.org) and Law Commission reports.

Check currency against indiacode.nic.in.

### Constitution

- Constitution of India (1950): supreme law; Articles numbered to 395 (many inserted, for example 21A), 12 Schedules; Fundamental Rights (Part III, Arts. 12-35) are enforceable against the state via Arts. 32/226; Union, State and Concurrent Lists (7th Schedule).

### Court system

```
Supreme Court of India (New Delhi)
    ↑
High Courts (25 — one per state/group of states)
    ↑
District Courts / Sessions Courts
    ↑
Civil Judge Courts / Judicial Magistrate Courts
    ↑
Executive Magistrate Courts / Tribunals
```

### Criminal law: major reform in force 1 July 2024

- Bharatiya Nyaya Sanhita (BNS) 2023: replaced the Indian Penal Code (IPC) 1860; sections renumbered (murder IPC 302 → BNS 103, cheating IPC 420 → BNS 318).
- Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023: replaced CrPC 1973; FIR (including zero FIR and e-FIR) under s. 173, notice of appearance instead of arrest under s. 35.
- Bharatiya Sakshya Adhiniyam (BSA) 2023: replaced the Indian Evidence Act 1872; electronic records as primary evidence.
- Transition: offences committed and proceedings pending before 1 July 2024 continue under IPC/CrPC (BNSS s. 531); always ask the date of the offence.
- Key rights: right to remain silent (Art. 20(3)), legal representation (Art. 22), bail; free legal aid via NALSA/DLSA.
- POCSO Act 2012: protection of children from sexual offences.

### Civil law and procedure

- Code of Civil Procedure (CPC) 1908: civil court procedure.
- Limitation Act 1963: time limits for suits (3 years for most contract and money claims; 12 years for possession of immovable property); late filing is barred unless delay is condoned where the Act allows.
- Mediation Act 2023: pre-litigation mediation framework; commercial disputes need pre-institution mediation under s. 12A Commercial Courts Act.
- Specific Relief Act 1963: specific performance, injunctions.
- Transfer of Property Act 1882: sale, mortgage, lease, gift of property.
- Registration Act 1908: compulsory registration of documents.

### Contract law

- Indian Contract Act 1872: offer, acceptance, consideration, capacity. Sale of Goods Act 1930: sale of movable goods.
- Consumer Protection Act 2019: Consumer Commissions by value paid: District up to ₹50 lakh, State to ₹2 crore, National above (2021 Rules); file within 2 years (s. 69), online via e-Daakhil.
- Arbitration and Conciliation Act 1996: ADR; India-seated arbitrations.
- Negotiable Instruments Act 1881, s. 138 (dishonoured cheque): written demand notice within 30 days of the bank's return memo; the drawer then has 15 days to pay; the complaint must be filed within one month after that period ends (s. 142).

### Employment and labour law

- Labour Codes (in force from 21 November 2025): Code on Wages 2019, Industrial Relations Code 2020, Code on Social Security 2020 (including 26 weeks' maternity benefit), OSH Code 2020. They consolidate 29 central laws, but old rules continue until central and state rules are notified, so check which rules apply.

### Company and business law

- Companies Act 2013 (MCA21), LLP Act 2008, IBC 2016 (NCLT), FEMA 1999 (RBI), Competition Act 2002 (CCI).

### Property law

- Transfer of Property Act 1882 and Registration Act 1908 (above): unregistered sale deeds do not pass title.
- RERA 2016: real estate regulation; state RERA authorities.
- Right to Fair Compensation and Transparency in Land Acquisition, Rehabilitation and Resettlement Act 2013: compulsory acquisition; compensation.

### Data protection and privacy

- Digital Personal Data Protection Act (DPDPA) 2023: DPDP Rules notified 13-14 November 2025. The Data Protection Board is live at once; consent-manager rules apply after 12 months (Nov 2026); notice, consent, security and breach duties after 18 months (May 2027); penalties up to ₹250 crore.
- IT Act 2000 (amended 2008): cybercrime, electronic records, digital signatures; SPDI Rules 2011 apply until DPDP duties start.
- CERT-In: cyber incidents must be reported within 6 hours (2022 Directions).

### Tax

- Income-tax Act 2025: replaced the Income-tax Act 1961 from 1 April 2026 (tax year 2026-27 onward); earlier years stay under the 1961 Act; section numbers changed.
- CGST/IGST Acts 2017: GST; rate slabs were rationalised in September 2025, so check current rates.

### Intellectual property

- Patents Act 1970 (20 years), Trade Marks Act 1999, Copyright Act 1957 (life + 60), Designs Act 2000; CGPDTM.

### Family law (personal laws)

- Hindu Marriage Act 1955: Hindus, Buddhists, Jains, Sikhs.
- Muslim Personal Law (Shariat) Application Act 1937: Muslims; instant triple talaq is void and an offence (Muslim Women (Protection of Rights on Marriage) Act 2019).
- Indian Christian Marriage Act 1872: Christians. Special Marriage Act 1954: inter-faith and civil marriages.
- Hindu Succession Act 1956: inheritance for Hindus. Guardians and Wards Act 1890: child custody.
- Uniform Civil Code Uttarakhand 2024: state law in force from 27 January 2025 (marriage, divorce, live-in registration, succession); ask the state.

### Resources

- indiacode.nic.in (official central legislation), sci.gov.in, indiankanoon.org (free case law), mca.gov.in.
- NALSA (nalsa.gov.in) and State/District Legal Services Authorities: free legal aid; Bar Council of India.
- National Consumer Helpline: consumerhelpline.gov.in (1915).

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Jurisdiction: Central Act or State law, which state.
2. Applicable legislation: key Acts with validated citations.
3. Plain-language explanation.
4. Recent reforms: note if the law has been recently replaced (IPC → BNS and others).
5. Case law: key Supreme Court and High Court decisions (via web search).
6. Practical implications.
7. Deadlines: limitation periods, filing deadlines.
8. Next steps: options, when to get an Advocate.
9. Resources: indiacode.nic.in, Supreme Court website, Bar Council.

## Checklist

- [ ] Central versus State law is confirmed.
- [ ] The date of the offence or event was asked, so the old or new criminal code is used correctly.
- [ ] Currency was checked for recently reformed law (IPC → BNS, CrPC → BNSS, Evidence Act → BSA, Labour Codes).
- [ ] Every section number cited appears in the text you opened.
