---
name: lawyer-us-law
title: "US Legal Research: Federal and State Law"
description: "US legal research across federal and 50-state law with CourtListener case law and citation checks: employment, contracts, criminal, privacy, IP, deadlines."
license: Apache-2.0
compatibility: "Needs web search and the CourtListener tools (COURTLISTENER_API_KEY). Covers US federal, state, DC and territory law."
capabilities: legal-us
rules:
  - match((?i)\b(alabama|alaska|arizona|arkansas|california|colorado|connecticut|delaware|florida|georgia|illinois|indiana|iowa|kansas|kentucky|louisiana|maryland|massachusetts|michigan|minnesota|missouri|nevada|new jersey|new york|north carolina|ohio|oklahoma|oregon|pennsylvania|tennessee|texas|virginia|wisconsin|denver)\b.{0,100}\b(law|laws|statutes?|rules?|courts?|attorney|cases?|legal|agreement|deadlines?)\b)
  - match((?i)\b(fair labor standards act|flsa|miranda|federal circuit|model penal code|expungement|50[- ]state|state[- ]by[- ]state|uspto|usc|cfr)\b)
  - match((?i)\b(united states|american|u\.s\.)\b.{0,80}\b(law|laws|legal|lawsuit|statute|court|attorney|lawyer|rights|contract|employer|tenant|landlord)\b)
  - match(\b(US|USA)\b.{0,60}\b(law|laws|legal|lawsuit|statute|court|attorney|rights|employer|landlord)\b|\b(law|legal|lawsuit|court)\b.{0,60}\b(in|under)\s+(the\s+)?(US|USA)\b)
  - match((?i)\b(frcp|title vii|ucc article 2|miranda rights|at-will employment|eeoc|courtlistener|statute of frauds|state statutes? of limitations?)\b)
  - match((?i)\b(california|texas|new york|florida|illinois|massachusetts|washington state)\b.{0,40}\b(law|statute|landlord|tenant|non-compete|small claims|lawsuit)\b)
  - semantic(what do US federal and state statutes say about this employment problem, 0.74)
  - semantic(find US court opinions on this contract dispute and verify the citations, 0.74)
  - semantic(what privacy and intellectual property rules apply to my American business, 0.74)
---

## Overview

This skill covers US legal information across 55 jurisdictions: US federal law, the 50 states, DC, Guam, Puerto Rico and the US Virgin Islands. It explains statutes, rights, obligations and procedures, researches legislation and case law, compares states, reviews documents and contracts, and prepares questions for an attorney. It does not cover non-US law.

## Mental model

Federal and state law can conflict, and state law varies widely, so the first step is always which jurisdiction governs. Every case and statute named in an answer must be checked first: cases through CourtListener, statutes through the official code text.

## Rules

### Research tools

CourtListener (free.law) is the primary source for US case law:
- `search_cases`: search federal and state opinions by topic, court and date.
- `fetch_passages`: pull the relevant passages of an opinion for quoting.
- `verify_citations`: confirm a case citation exists and resolves to the right opinion.
- `how_cited`: see how later courts treated a case (followed, distinguished, overruled).
- `list_courts`: court identifiers for scoping a search.

For statutes and regulations, search the official sources: uscode.house.gov and govinfo.gov (federal statutes), ecfr.gov (federal regulations), and each state legislature's official code site. Build cross-state comparisons by looking up each state's statute and tabulating the official text. Use web search for recent developments, news and commentary.

### Research protocol

1. Identify the jurisdiction: federal, which state or states, whether it crosses state lines.
2. Find the statute on the official code site and quote the provision text, not a summary.
3. When state variation matters, look up each relevant state's statute and tabulate the differences.
4. Find case law with `search_cases`, then `fetch_passages` for the language you rely on.
5. Run `verify_citations` for every case cited and `how_cited` to confirm it is still good law.
6. Check currency: confirm the statute's effective date and recent amendments on the official site.
7. Use web search for recent changes, news and commentary.

Clarify which jurisdiction applies before answering. Verify against current official sources; statutes change.

### Federal and state structure

- Supremacy Clause: federal law preempts conflicting state law.
- 10th Amendment: powers not delegated to the federal government are reserved to the states.
- Concurrent jurisdiction: both may regulate (employment, environment and others).
- Exclusive federal: immigration, bankruptcy, patents, federal crimes.
- Exclusive state: family law, property, most criminal law, contracts.

Court system:

```
Supreme Court of the United States
    ↑
US Courts of Appeals (13 Circuits)
    ↑
US District Courts (94 districts)
    ↑
Magistrate Courts / Bankruptcy Courts

State Supreme Courts
    ↑
State Appellate Courts
    ↑
State Trial Courts (Superior, Circuit, District)
    ↑
Limited Jurisdiction Courts (Small Claims, Traffic, etc.)
```

### Employment law

- At-will employment: every state except Montana; the employer can terminate for any reason that is not discriminatory, retaliatory, or in breach of contract.
- Federal protections: Title VII, ADA, ADEA, FMLA, FLSA, NLRA, PWFA (pregnancy accommodation, since 2023).
- State variations: California, New York, Massachusetts and Washington have stronger worker protections.
- Non-competes: the FTC's 2024 nationwide ban was set aside in court and the FTC dropped its appeals in Sept 2025; state law governs. They are void or near-void in California, Minnesota, North Dakota and Oklahoma; many states bar them below an income threshold, so check the state statute.
- Minimum wage: federal $7.25/hr (unchanged since 2009); most states and many cities are higher and adjust each January.
- Discrimination charges: file with the EEOC within 180 days, or 300 days where a state or local agency also covers the claim.

### Contract law (UCC and common law)

- UCC Article 2 governs sale of goods; common law governs services, real estate and employment.
- Formation: offer, acceptance, consideration, capacity, legality.
- Statute of Frauds: contracts over $500 (goods), real estate, and terms of 1+ year must be written.

### Criminal law

- Miranda rights: right to remain silent, right to an attorney.
- 4th Amendment: unreasonable search and seizure. 5th: self-incrimination, due process. 6th: speedy trial, counsel, confrontation.
- Felony versus misdemeanor varies by state; generally a felony carries 1+ year in prison.

### Business law

- Entity types: sole proprietorship, LLC, C-Corp, S-Corp, partnership, LLP.
- Delaware: most corporations incorporate there.
- Securities law: the SEC regulates; state Blue Sky laws also apply.
- Antitrust: Sherman Act, Clayton Act, FTC Act.

### Privacy and data law

- Federal: HIPAA (health), COPPA (children; amended rule 2025), GLBA (financial), FERPA (education); no comprehensive federal privacy law.
- States: about 20 states have comprehensive privacy laws in force in 2026 (Indiana, Kentucky and Rhode Island joined 1 Jan 2026); California CCPA/CPRA is the strictest and has its own regulator, the California Privacy Protection Agency (now branded CalPrivacy).
- AI: state laws move fast. Colorado replaced its 2024 AI Act with SB 26-189 (automated decision-making disclosures, effective 1 Jan 2027); verify current status and any federal preemption litigation before citing.
- State breach notification: all 50 states have laws; compare by looking up each state's statute on its official site.

### Immigration law

- Visa categories: B-1/B-2 (visitor), F-1 (student), H-1B (specialty worker), L-1 (intracompany), O-1 (extraordinary ability), EB (employment-based green card).
- USCIS handles most applications; policy changed sharply in 2025-26 (for example the Sept 2025 $100,000 H-1B petition fee proclamation), so verify on uscis.gov and state.gov before stating any rule.
- Recommend an immigration attorney or DOJ-accredited representative: mistakes can be irreversible, and notarios are not lawyers.

### Intellectual property

- Patents (USPTO): utility 20 years, design 15 years, plant 20 years.
- Trademarks (USPTO): renewable indefinitely with use.
- Copyright: automatic upon creation; life + 70 years.
- Trade secrets: DTSA (federal) plus state laws.

### Deadlines that commonly decide cases

- Answering a lawsuit: 21 days after service in federal court (FRCP 12(a)); state courts commonly 20-35 days. Missing it risks default judgment.
- Statutes of limitations: vary by state and claim (often 2-3 years for personal injury, 3-6 for written contracts); always look up the specific state statute.
- Small claims: limits range roughly $2,500-$25,000 by state; check the state court site for the current figure.

### Legal aid resources

- Legal Services Corporation: lsc.gov (free civil legal aid finder).
- State bar lawyer referral: each state bar has a service, often with a low-cost first consultation.
- Law school clinics and state court self-help centers: free help and forms for self-represented people.
- ACLU: civil liberties issues. EEOC: employment discrimination.
- FTC (reportfraud.ftc.gov) and the state attorney general: consumer protection.
- CFPB: consumer financial complaints; its funding and staffing were contested in 2025-26, so also file with the state AG or banking regulator.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Jurisdiction: federal, state(s), or both.
2. Applicable law: key statutes with validated citations.
3. Plain-language explanation.
4. State variations: where states differ significantly.
5. Case law: relevant precedents from CourtListener.
6. Practical implications.
7. Deadlines: statutes of limitations, filing deadlines.
8. Next steps: options, when to get a lawyer.
9. Resources: USA.gov, state bar associations, legal aid.

## Checklist

- [ ] The jurisdiction (federal, which state) is confirmed, not assumed.
- [ ] Every statute is quoted from the official code text and its currency checked.
- [ ] Every case passed `verify_citations`, and `how_cited` shows it is still good law.
- [ ] The tightest deadline appears at the top when one applies.
- [ ] Anything that may be out of date is flagged.

## Composition / References

- courtlistener.com and free.law for opinions; uscode.house.gov, govinfo.gov and ecfr.gov for federal text.
