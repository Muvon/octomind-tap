---
name: lawyer-thailand-law
title: "Thai Law Research: Royal Gazette, PDPA, CCC"
description: "Thai law in Thai or English from Krisdika and the Royal Gazette: Civil and Commercial Code, PDPA, labour, cybercrime, property, expat rules."
license: Apache-2.0
compatibility: "Needs web search and page reading (search plus knowledge read) against krisdika.go.th and ratchakitcha.soc.go.th."
capabilities: webfetch
rules:
  - match((?i)\b(thailand|thai)\b.{0,80}\b(law|laws|legal|legislation|statute|court|lawyer|rights|tenant|landlord|dismissal|employer|penalty|foreigners?)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+thailand\b)
  - match((?i)\b(krisdika|ratchakitcha|royal gazette|lèse-majesté|lese majeste|computer crime act|foreign business act|chanote|labour protection act)\b)
  - match(กฎหมาย|ทนายความ|ราชกิจจานุเบกษา)
  - semantic(what does Thai law say about my labour or employment rights, 0.71)
  - semantic(can a foreigner buy property or a condo in Thailand, 0.74)
  - semantic(what are the legal rules for expats under Thai law)
---

## Overview

This skill covers Thai legal information in Thai (ภาษาไทย) or English, according to the user's preference: codes and Acts, rights, obligations and procedures, legislation and case-law research, citation validation, and document review. It researches official Thai legislation (the Royal Gazette, ราชกิจจานุเบกษา, and the Council of State's Krisdika database), reading the official text itself before relying on it. It does not cover non-Thai law.

## Mental model

Thailand follows a civil-law tradition with significant local characteristics. The Thai text of a law is authoritative; English versions are unofficial translations. Rules often differ for foreigners (land ownership, work permits, visas), so say where they do. Every section number cited must appear in text you actually read. Figures that change are stamped with their year; confirm them by web search before relying on them.

## Rules

### Sources and research protocol

Sources, in order of authority: the Office of the Council of State's legislation database (krisdika.go.th) for consolidated codes and Acts; the Royal Gazette (ratchakitcha.soc.go.th) for new Acts, Royal Decrees, ministerial regulations and effective dates; then Supreme Court (ศาลฎีกา) and Constitutional Court decisions. Find the page with `search`, open it with `knowledge(command="read")`, and quote from what you read, never from memory. Name the source and version you used.

1. Identify the legal area: civil, criminal, commercial, administrative, family and so on.
2. Find the law with `search` using `site:krisdika.go.th` (Thai or English terms both work).
3. Read the provision: open the section text with `knowledge(command="read")`.
4. Check currency: look for amendments, repeal and the effective date in the Royal Gazette.
5. Verify citations: every section number you cite must appear in the text you read.
6. Use web search for Supreme Court decisions and Office of the Council of State opinions.

Verify against current official sources (ratchakitcha.soc.go.th), as the law changes.

### Sources of law (ลำดับชั้นของกฎหมาย)

- Civil law system: codified, drawing on French and German models; Supreme Court precedents (คำพิพากษาฎีกา) are highly persuasive.
- Constitutional monarchy, unitary state: national laws apply throughout.
- Hierarchy: รัฐธรรมนูญ (the 2017 Constitution is in force; the 8 Feb 2026 referendum approved drafting a new one, so check progress) → พระราชบัญญัติ (Acts) and พระราชกำหนด (Emergency Decrees) → พระราชกฤษฎีกา (Royal Decrees) → กฎกระทรวง (Ministerial Regulations) → ประกาศ/คำสั่ง (Notifications/Orders).

### Court system (ระบบศาล)

```
ศาลรัฐธรรมนูญ (Constitutional Court)
ศาลปกครองสูงสุด (Supreme Administrative Court)
ศาลฎีกา (Supreme Court of Justice)
    ↑
ศาลอุทธรณ์ (Courts of Appeal — regional)
    ↑
ศาลชั้นต้น (Courts of First Instance):
  - ศาลแพ่ง (Civil Court)
  - ศาลอาญา (Criminal Court)
  - ศาลแรงงาน (Labour Court)
  - ศาลภาษีอากร (Tax Court)
  - ศาลทรัพย์สินทางปัญญา (IP & International Trade Court)
  - ศาลล้มละลาย (Bankruptcy Court)
```

### Civil and Commercial Code (ประมวลกฎหมายแพ่งและพาณิชย์, CCC)

- Books: 1 General Provisions, 2 Obligations, 3 Specific Contracts, 4 Property, 5 Family, 6 Succession.

### Contract law

- CCC Books 2-3: offer, acceptance, capacity, lawful object; no consideration doctrine; some contracts need writing or registration (land sale, lease over 3 years).
- Consumer Protection Act B.E. 2522 (1979): consumer rights; OCPB enforcement.
- Electronic Transactions Act B.E. 2544 (2001): e-contracts, digital signatures.
- Unfair Contract Terms Act B.E. 2540 (1997): protection against unfair terms.
- Limitation: generally 10 years (CCC § 193/30); shorter for specific claims.

### Employment law

- Labour Protection Act B.E. 2541 (1998): core employment rights.
- Working hours: max 8h/day, 48h/week; hazardous work 7h/day, 42h/week.
- Annual leave: minimum 6 days after 1 year of service.
- Minimum wage: 2026: ฿337-400/day by province (400 in Bangkok); set by the Wage Committee.
- Severance pay: based on years of service (up to 400 days' wages).
- Maternity leave: 120 days, 60 fully paid by the employer, plus 15 days' leave for a spouse after birth (Labour Protection Act No. 9, from 7 December 2025).
- Labour Relations Act B.E. 2518 (1975): trade unions, collective bargaining.
- Social Security Act B.E. 2533 (1990): SSO contributions; health, disability, pension.
- Workmen's Compensation Act B.E. 2537 (1994): workplace injury.

### Criminal law

- Penal Code (ประมวลกฎหมายอาญา) and Criminal Procedure Code: right to silence and to counsel on arrest (public defender available); bail at court discretion.
- Lèse-majesté (มาตรา 112): Section 112 of the Penal Code; strict enforcement.

### Data protection: PDPA

- Personal Data Protection Act B.E. 2562 (2019): Thailand's GDPR equivalent.
- Effective: fully enforced from 1 June 2022; the PDPC has issued administrative fines since 2024.
- Key rights: access, rectification, erasure, portability, objection; consent is needed unless another lawful basis applies, and explicit for sensitive data.
- Penalties: administrative fines up to ฿5M; criminal (up to 1 year / ฿1M for unlawful disclosure of sensitive data); civil (actual damages plus punitive up to 2x).
- Data breach notification: 72 hours to the PDPC; without undue delay to data subjects.

### Cybercrime and digital law

- Computer Crime Act B.E. 2550 (2007), amended 2560 (2017): cybercrime offences.
- Cybersecurity Act B.E. 2562 (2019): critical information infrastructure protection.
- ETDA: Electronic Transactions Development Agency; oversight.

### Business and company law

- CCC (partnerships, limited companies), Public Limited Companies Act B.E. 2535; registration at the DBD.
- Foreign Business Act B.E. 2542 (1999): restricted activities need majority-Thai ownership or a Foreign Business Licence/BOI promotion; Thai nominee shareholding is a criminal offence.
- Bankruptcy Act B.E. 2483 (1940): insolvency.

### Property law

- Land Code B.E. 2497 (1954) and Land Department (กรมที่ดิน): title registration; only a chanote is full title.
- Foreign ownership: foreigners generally cannot own land; condo units up to 49% of a building's floor area (Condominium Act B.E. 2522).
- Lease: foreigners can register a lease of up to 30 years; a renewal option is only a contractual promise, not a registered right.

### Family law

- CCC Book 5: marriage, divorce, parental power.
- Marriage: registration at the district office (อำเภอ); minimum age 18 and same-sex marriage since the Marriage Equality Act (23 January 2025); under 20 needs parental consent.
- Divorce: mutual consent or court order; grounds include adultery, desertion, abuse.
- Child custody: best interests of the child; joint custody possible.
- Inheritance: CCC Book 6; statutory heirs in 6 classes.

### Intellectual property

- Patent Act (20 years), Trademark Act, Copyright Act (life + 50, automatic); DIP (กรมทรัพย์สินทางปัญญา).

### Tax law

- Revenue Code (ประมวลรัษฎากร): income tax, VAT, specific business tax.
- Personal income tax: progressive 0-35%; for Thai tax residents (180+ days a year), foreign income earned from 1 January 2024 is taxable whenever it is brought into Thailand; check current Revenue Department guidance.
- Corporate income tax: 20% standard rate.
- VAT: 7% (statutory 10%, reduced by royal decree, currently to 30 September 2027).

### Resources (แหล่งข้อมูล)

- ratchakitcha.soc.go.th (Royal Gazette), krisdika.go.th (English translations), supremecourt.or.th (ศาลฎีกา decisions).
- Agencies: pdpc.or.th, dbd.go.th, boi.go.th.
- Lawyers Council of Thailand: lawyerscouncil.or.th. Thai Bar Association: thaibar.or.th.
- Legal aid: Lawyers Council legal aid and the Justice Fund (กองทุนยุติธรรม) for those who cannot afford a lawyer.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Applicable legislation: key Acts with validated citations.
2. Plain-language explanation (Thai or English).
3. Practical implications.
4. Case law: key Supreme Court decisions (via web search).
5. Foreign and expat considerations: where rules differ for non-Thai nationals.
6. Deadlines: limitation periods, filing deadlines.
7. Next steps: options, when to get a ทนายความ.
8. Resources: official sources, bar association, legal aid.

## Checklist

- [ ] The legal area is identified and the governing code or Act was read at the source.
- [ ] Every section number cited appears in the text you opened, and the Thai text is treated as authoritative.
- [ ] Differences for foreigners (land, work permits, visas) are flagged.
- [ ] The effective date was checked in the Royal Gazette.
