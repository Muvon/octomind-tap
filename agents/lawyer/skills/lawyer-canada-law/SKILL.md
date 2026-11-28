---
name: lawyer-canada-law
title: "Canadian Law Research: Federal, Provincial, Quebec"
description: "Canadian federal law in English or French with a legislation database, Charter rights and citation checks; provincial and Quebec civil law via CanLII."
license: Apache-2.0
compatibility: "Needs web search and the Canadian legislation database tools. Federal Acts are in the database; provincial law comes from CanLII."
capabilities: legal-ca
rules:
  - match((?i)\b(charter (right|rights|section)|section \d+ charter|supreme court of canada|\d{4} SCC \d+|competition (act|tribunal)|criminal code of canada|section \d+ of the criminal code|code criminel|lcap|loi canadienne|légitime défense|federal government institutions)\b)
  - match((?i)\b(ottawa|toronto|vancouver|montreal|montréal|calgary)\b.{0,160}\b(act|statute|code|contract|agreement|lease|federal|regulat\w+|court|law)\b)
  - match((?i)\b(canada|canadian|ontario|quebec|québec|british columbia|alberta|manitoba|saskatchewan|nova scotia)\b.{0,80}\b(law|laws|legal|legislation|statute|court|lawyer|rights|tenant|landlord|dismissal|employer)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+(canada|ontario|quebec|québec|british columbia|alberta)\b)
  - match((?i)\b(charter of rights|pipeda|casl|canlii|criminal code of canada|code civil du québec|notwithstanding clause|droit (canadien|québécois))\b)
  - semantic(what are my rights as an employee under Canadian law, 0.74)
  - semantic(what does the Quebec Civil Code say about my lease or contract, 0.74)
  - semantic(what Charter rights does a person arrested in Canada have, 0.74)
---

## Overview

This skill covers Canadian legal information in English or French (Canada is officially bilingual): federal Acts, Charter rights, obligations and procedures, legislation and case-law research, citation validation, and document and contract review. A legislation database covers key federal Acts (such as PIPEDA, CASL, the Criminal Code, the Privacy Act and the Competition Act) with full-text search, currency checks and citation support. Anything outside the database is researched on Justice Laws and CanLII by web search. Provincial and territorial law is researched through CanLII and official provincial sites, with a clear note that it sits outside the federal database. It does not cover non-Canadian law.

## Mental model

Canada has federal law, 10 provinces and 3 territories with their own laws, and Quebec's civil law tradition. The first question is always which level applies and whether Quebec civil law differs. Citations are only usable after the database confirms them.

## Rules

### Research tools

- `search_legislation`: full-text search across all provisions with BM25 ranking.
- `get_provision`: retrieve a specific provision by statute and chapter or section.
- `check_currency`: check whether a statute is in force, amended or repealed.
- `validate_citation`: validate a citation against the database (zero-hallucination check).
- `build_legal_stance`: aggregate citations from statutes for a legal topic.
- `format_citation`: format citations per Canadian conventions (full, short, pinpoint).
- `list_sources`: list the statutes actually in the database; call it when unsure whether an Act is covered.
- `about`: server info, capabilities and coverage summary.

Use web search for statutes not in the database (laws-lois.justice.gc.ca), Supreme Court of Canada decisions, provincial legislation and case law (CanLII), bill progress (parl.ca LEGISinfo) and recent developments.

### Research protocol

1. Identify the jurisdiction: federal or provincial/territorial, and which province.
2. `search_legislation` with relevant terms.
3. `get_provision` for exact statutory text.
4. `check_currency` to confirm the statute is still in force.
5. `validate_citation` before citing.
6. Web search for SCC decisions (scc-csc.ca) and provincial legislation (CanLII).

Verify against current official sources (laws-lois.justice.gc.ca); law changes.

### Constitutional framework

- Constitution Act, 1867: division of powers, federal (s. 91) versus provincial (s. 92).
- Constitution Act, 1982: Canadian Charter of Rights and Freedoms.
- Charter rights: fundamental freedoms, democratic rights, mobility, legal rights, equality.
- Section 33, the notwithstanding clause: provinces can override some Charter rights.
- Federal powers: criminal law, trade and commerce, banking, immigration, POGG.
- Provincial powers: property and civil rights, education, health, municipalities.

### Two legal traditions

| Common law provinces/territories | Quebec |
|---|---|
| 9 provinces + 3 territories | Province of Quebec |
| English common law tradition | Civil law (Code civil du Québec) |
| Case law is binding precedent | Doctrine and legislation primary |
| Contract, tort, property law | Obligations, property, family law |

Courts: Supreme Court of Canada (9 justices) → provincial Courts of Appeal / Federal Court of Appeal → superior courts / Federal Court → provincial courts (small claims, family, criminal) and administrative tribunals.

### Employment law

- Canada Labour Code: federally regulated private sector (about 6% of workers, 2024): banks, telecoms, airlines, interprovincial transport, federal Crown corporations.
- Provincial employment standards cover most workers.
- Human rights: Canadian Human Rights Act (federal); provincial human rights codes. Prohibited grounds include race, sex, age, disability, religion and sexual orientation.
- Federal benefits: Employment Insurance Act; Canada Pension Plan.
- Wrongful dismissal: outside Quebec, common-law reasonable notice usually far exceeds the statutory minimum unless a valid termination clause limits it; termination clauses are frequently struck down.

### Criminal law

- Criminal Code of Canada: federal; applies across all provinces.
- Charter rights: s. 7 (life, liberty, security), s. 8 (unreasonable search), s. 10 (right to counsel), s. 11 (fair trial).
- Right to silence: you cannot be compelled to testify against yourself.
- Youth Criminal Justice Act: for persons 12-17.
- Crown prosecutors are provincial (most crimes) or federal (federal offences).

### Privacy and data protection

- PIPEDA: federal private-sector privacy law (plus provincial laws in Quebec, Alberta and BC). Privacy Act: federal public sector.
- Reform: Bill C-27 (CPPA and AIDA) died at prorogation in January 2025. Bill C-36, the Protecting Privacy and Consumer Data Act, tabled June 2026, would replace PIPEDA's privacy part with a new commission and a private right of action; it is not law yet, so check LEGISinfo. No federal AI statute is in force.
- Quebec Law 25: fully in force since Sept 2024; GDPR-like, with penalties up to 4% of worldwide turnover.
- OPC: Office of the Privacy Commissioner of Canada.
- Breach notification: mandatory under PIPEDA for real risk of significant harm.
- CASL: anti-spam law; express or implied consent is needed for commercial electronic messages.

### Other federal areas

- Business: CBCA (federal) or provincial incorporation; Competition Act (Competition Bureau; private access to the Tribunal widened 2024-25); BIA and CCAA insolvency; securities regulated provincially (CSA coordinates).
- Tax: Income Tax Act and Excise Tax Act (GST 5%, HST in participating provinces); CRA administers, Quebec collects its own income tax and QST.
- Immigration: IRPA; Express Entry, Provincial Nominee Programs, family sponsorship; IRCC levels and caps change yearly, so check canada.ca.
- IP: Patent Act (20 years), Trademarks Act, Copyright Act (life + 70 years), Industrial Design Act; CIPO.

### Property law (provincial)

- Land titles system: Torrens-based in most provinces.
- Residential tenancy: provincial legislation; strong tenant protections.
- Quebec: the Code civil du Québec governs property.

### Family law (provincial)

- Divorce Act: federal; divorce, parenting orders (formerly custody), support.
- Provincial family law: property division, common-law relationships.
- Best interests of the child is the primary consideration.
- Quebec: Code civil du Québec; distinct rules for civil unions.

### Deadlines and small claims (provincial, verify)

- Limitation periods: basic period 2 years from discovery in Ontario, BC and Alberta; 3 years in Quebec; others vary.
- Small claims in 2026: Ontario up to $50,000 (since Oct 2025); BC Civil Resolution Tribunal handles most claims up to $5,000 and Provincial Court small claims up to $35,000; Quebec Small Claims Division up to $15,000 (no lawyers); check other provinces live.

### Resources

- Justice Laws: laws-lois.justice.gc.ca (official federal legislation, bilingual).
- CanLII: canlii.org (free case law and legislation database).
- Supreme Court of Canada: scc-csc.ca. Justice Canada: justice.gc.ca.
- CRA: canada.ca/cra. IRCC: canada.ca/immigration. OPC: priv.gc.ca (privacy).
- Legal aid: each province and territory has a plan (for example Legal Aid Ontario, Legal Aid BC, Commission des services juridiques).
- Law societies: each province has one with lawyer referral (Ontario's referral service gives a free 30-minute consultation); Ontario paralegals can handle small claims.
- Human rights: provincial human rights tribunals; complaint deadlines are short (one year in Ontario and BC).

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Jurisdiction: federal or provincial, which province or territory.
2. Applicable legislation: key Acts with validated citations.
3. Quebec distinction: note where Quebec civil law differs.
4. Plain-language explanation.
5. Case law: key SCC and appellate decisions (via web search).
6. Practical implications.
7. Deadlines: limitation periods, filing deadlines.
8. Next steps: options, when to get a lawyer.
9. Resources: laws-lois.justice.gc.ca, CanLII, legal aid.

## Checklist

- [ ] Federal versus provincial is confirmed, and Quebec civil law differences are noted.
- [ ] Every citation passed `validate_citation` before it was quoted.
- [ ] `check_currency` confirmed each statute is in force.
- [ ] The answer uses the user's language (English or French).
- [ ] Anything outside the federal database is flagged as researched on CanLII or provincial sites.
