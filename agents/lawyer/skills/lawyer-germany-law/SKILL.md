---
name: lawyer-germany-law
title: "German Law Research: Bundesrecht, BGB, DSGVO"
description: "German federal law (Bundesrecht) fetched live from gesetze-im-internet.de, in German or English: BGB, tenancy, employment, DSGVO, deadlines."
license: Apache-2.0
compatibility: "Needs web search and the German federal statute tools. Federal law only; Landesrecht comes from Land legislation sites."
capabilities: legal-de
rules:
  - match((?i)\b(germany|german|deutsch\w*)\b.{0,80}\b(law|laws|legal|legislation|statute|court|lawyer|rights|tenant|landlord|dismissal|employer)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+germany\b)
  - match((?i)\b(bgb|stgb|hgb|bdsg|kschg|gesetze-im-internet|bürgerliches gesetzbuch|mietpreisbremse|dsgvo|rechtsanwalt|arbeitsrecht|mietrecht)\b)
  - match((?i)\b(kündigung|kuendigung|mieterhöhung|widerruf|verjährung|rechtsberatung|rechtsinformation|bundesrecht)\b)
  - semantic(what are my rights as a tenant under German law)
  - semantic(what does German law say about dismissal protection at work)
  - semantic(does this data handling comply with the German DSGVO)
---

## Overview

This skill covers German federal legal information (Bundesrecht) in German or English: statutes, rights, obligations and procedures, legislation and case-law research, citation checks against the statutory text, EU cross-references, and document review. Statutes come live from gesetze-im-internet.de, the official Bundesministerium der Justiz portal; case law and EU cross-references come from web search. State law (Landesrecht) of the 16 Bundesländer is researched on the official Land legislation sites, with a clear note that it sits outside federal law. It does not cover non-German law. Respond in German or English according to the user's preference.

## Mental model

Hierarchy: GG → EU regulations (directly applicable; directives via German statutes) → Bundesgesetze → Bundesverordnungen → Landesrecht. Richterrecht is persuasive, though BVerfG decisions bind (§ 31 BVerfGG). A citation counts as validated only when `get_paragraph` returns the provision. Figures that change yearly are stamped with their year; confirm them by web search before relying on them.

## Rules

### Research tools

- `download_law`: fetch a statute by its short name (for example `bgb`, `hgb`, `stgb`, `bdsg`).
- `list_contents`: table of contents of a downloaded statute, to locate the right provision.
- `get_paragraph`: verbatim text of one provision; takes `law_name` (for example `bgb`) and `paragraph` with the `§ ` prefix (for example `§ 823`).

Use web search for federal court decisions (BVerfG, BGH, BVerwG, BAG, BSG, BFH, BPatG), Drucksachen and Plenarprotokolle (dip.bundestag.de), the EU directives and regulations behind a German statute (eur-lex.europa.eu), legal commentary (Kommentare), and anything not on gesetze-im-internet.de.

### Research protocol

1. Rechtsgebiet identifizieren: which area of law (Zivilrecht, Strafrecht, Öffentliches Recht, Arbeitsrecht and so on)?
2. Gesetz laden: `download_law` for the statute, `list_contents` to locate the provision (German terms).
3. Vorschrift abrufen: `get_paragraph` for exact statutory text; quote from it, never from memory.
4. Rechtsprechung: web search for relevant federal court decisions.
5. Zitat prüfen: the portal serves the current consolidated version, so a successful fetch also confirms currency.
6. EU-Bezug: web search for the EU directive or regulation behind EU-derived German law (DSGVO and others).
7. Rechtliche Stellungnahme: combine statutory text, case law and EU basis into the answer.

The 16 Bundesländer have their own laws (especially public law, education, police), so clarify the jurisdiction. Verify against current official sources (gesetze-im-internet.de); law changes.

### Gerichtssystem (court system)

```
Bundesverfassungsgericht (BVerfG) — Constitutional Court

Bundesgerichtshof (BGH) — Civil & Criminal
Bundesverwaltungsgericht (BVerwG) — Administrative
Bundesarbeitsgericht (BAG) — Labor
Bundessozialgericht (BSG) — Social Security
Bundesfinanzhof (BFH) — Tax
    ↑
Oberlandesgerichte (OLG) / Oberverwaltungsgerichte
    ↑
Landgerichte (LG) / Verwaltungsgerichte
    ↑
Amtsgerichte (AG) / Arbeitsgerichte / Sozialgerichte / Finanzgerichte
```

Civil first instance: the AG up to €10,000 Streitwert since 1 Jan 2026 (§ 23 Nr. 1 GVG, was €5,000) plus tenancy and neighbour disputes regardless of value; above that the LG, where a Rechtsanwalt is mandatory (§ 78 ZPO). Appeal (Berufung) needs a Beschwer above €1,000 (§ 511 ZPO) unless admitted.

### Bürgerliches Recht: BGB (civil law)

- Allgemeiner Teil (§§ 1-240): legal capacity, declarations of intent, agency.
- Schuldrecht (§§ 241-853): contract law, tort law, unjust enrichment. Kaufvertrag (§§ 433-479), Werkvertrag (§§ 631-651), Dienstvertrag (§§ 611-630). Deliktsrecht: § 823 BGB (general tort), § 826 BGB (intentional damage contra bonos mores).
- Sachenrecht (§§ 854-1296): property law, ownership, mortgages.
- Familienrecht (§§ 1297-1921): marriage, divorce, custody, maintenance.
- Erbrecht (§§ 1922-2385): inheritance, wills, intestate succession.

### Handels- und Gesellschaftsrecht

- HGB, GmbHG, AktG, PartGG; InsO: managing directors must file for insolvency within 3 weeks of illiquidity and 6 weeks of over-indebtedness (§ 15a InsO).

### Arbeitsrecht (employment law)

- Kündigungsschutzgesetz (KSchG): unfair dismissal protection where the business has more than 10 employees (§ 23) and the employment lasted over 6 months (§ 1). The Kündigungsschutzklage must be filed within 3 weeks of receiving the written notice (§ 4), the deadline people miss most.
- Arbeitszeitgesetz (ArbZG): 8h/day, up to 10h if averaged to 8h; a switch to a weekly maximum was in draft in 2026, so check whether it passed.
- Bundesurlaubsgesetz (BUrlG): minimum 24 Werktage on a 6-day week, i.e. 20 days on a 5-day week.
- Kündigungsfristen (§ 622 BGB): employee 4 weeks to the 15th or end of a month; employer 1 month to month-end after 2 years, rising to 2 months at 5 years, 3 at 8, 4 at 10, 5 at 12, 6 at 15 and 7 at 20 years; contracts or collective agreements may differ.
- Mutterschutzgesetz (MuSchG): maternity protection. Betriebsverfassungsgesetz (BetrVG): works council rights.
- Mindestlohngesetz (MiLoG): statutory minimum wage; 2026: €13.90/h, 2027: €14.60/h (MiLoV5).
- AGG: General Equal Treatment Act (Allgemeines Gleichbehandlungsgesetz).

### Strafrecht (criminal law)

- StGB / StPO: right to silence (§ 136 StPO); Pflichtverteidiger in serious cases (§ 140 StPO); fines in Tagessätzen or imprisonment.

### Datenschutzrecht (data protection)

- DSGVO (GDPR): EU regulation, directly applicable. BDSG: Federal Data Protection Act; supplements the DSGVO.
- BfDI: Federal Commissioner for Data Protection; enforcement.
- Bußgelder: up to €20M or 4% of global turnover.

### Mietrecht (tenancy law)

- §§ 535-580a BGB: lease provisions.
- Mietpreisbremse: new-lease rent capped at 10% above the ortsübliche Vergleichsmiete in designated areas (§ 556d); extended to 31 Dec 2029; designations are per Land, so check the Landesverordnung.
- Mieterhöhung: up to the Mietspiegel level, max. 20% in 3 years (15% in tight markets) (§ 558).
- Kaution: max. 3 Nettokaltmieten, payable in 3 instalments (§ 551).
- Kündigung: tenant 3 months (§ 573c); the landlord needs a berechtigtes Interesse (§ 573) and longer notice by tenancy length.
- Betriebskosten: only items in the BetrKV and the lease; objections within 12 months of receiving the statement (§ 556 Abs. 3).

### Steuerrecht (tax law)

- EStG, KStG, GewStG: income, corporate and trade tax.
- UStG: VAT 19% standard, 7% reduced; restaurant food (not drinks) at 7% permanently from 1 Jan 2026.
- AO: General Tax Code (Abgabenordnung); Einspruch against a Steuerbescheid within 1 month (§ 355 AO).
- Steuererklärung: due 31 July of the following year; with a Steuerberater, end of February of the second following year.

### Immaterialgüterrecht

- PatG (20 years), MarkenG, UrhG (life + 70), DesignG; registrations at the DPMA.

### Fristen (high-leverage deadlines)

- Regelverjährung: 3 years, running from the end of the year the claim arose and the creditor knew of it (§§ 195, 199 BGB); 2 years for defects in bought goods (§ 438).
- Widerruf of distance and off-premises contracts: 14 days (§ 355 BGB); from 19 June 2026 online shops must offer an electronic withdrawal button (§ 356a BGB), so confirm the final text.
- Mahnbescheid: Widerspruch within 2 weeks; Vollstreckungsbescheid: Einspruch within 2 weeks (§§ 692, 700 ZPO).
- Berufung: 1 month from service of the judgment (§ 517 ZPO).
- Erbrecht: Ausschlagung of an inheritance within 6 weeks of learning of the Erbfall (6 months if the deceased lived only abroad) (§ 1944 BGB); the Pflichtteil of an excluded child is half of the statutory share (§ 2303 BGB).

### Zitierweise (citation format)

- Statute: `§ 823 Abs. 1 BGB` or `Art. 20 Abs. 3 GG`.
- Case: `BGH, Urt. v. TT.MM.JJJJ – Az.` (senate + register + number/year). Never invent an Aktenzeichen; cite only one found by search.
- Confirm every statutory citation by fetching it with `get_paragraph` before quoting.

### Ressourcen (resources)

- gesetze-im-internet.de: official federal legislation; bundesverfassungsgericht.de and bundesgerichtshof.de: decisions.
- brak.de and anwaltauskunft.de: find a Rechtsanwalt.
- Beratungshilfe (Amtsgericht) and Prozesskostenhilfe: legal aid for low incomes.
- verbraucherzentrale.de: consumer advice centers. mieterbund.de: tenant associations.

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Rechtsgebiet: area of law and applicable statutes.
2. Gesetzestext: exact statutory provisions (retrieved via `get_paragraph`).
3. Erläuterung: plain-language explanation.
4. Rechtsprechung: relevant federal court decisions.
5. EU-Bezug: EU law basis where applicable.
6. Praktische Bedeutung: practical implications.
7. Fristen: deadlines and limitation periods (Verjährungsfristen).
8. Nächste Schritte: options, when to consult a Rechtsanwalt.
9. Ressourcen: gesetze-im-internet.de, BMJV, Rechtsanwaltskammer.

## Checklist

- [ ] Federal law versus Landesrecht is confirmed, and Landesrecht is flagged as outside federal law.
- [ ] Every provision was fetched with `get_paragraph` before it was quoted.
- [ ] No Aktenzeichen is cited unless a search returned it.
- [ ] Yearly figures carry their year and were confirmed by web search.
- [ ] The answer uses the user's language (German or English).
