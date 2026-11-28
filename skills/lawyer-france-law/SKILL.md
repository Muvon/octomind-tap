---
name: lawyer-france-law
title: "French Law Research: Droit Français, Légifrance"
description: "French law in French or English with Légifrance legislation and EU cross-references: civil, labor, criminal, tenancy, consumer, RGPD."
license: Apache-2.0
compatibility: "Needs web search and the French legislation database tools. The database is a snapshot; recent reforms are confirmed on legifrance.gouv.fr."
capabilities: legal-fr
domains: lawyer
rules:
  - match((?i)\b(france|french|français|francais|droit français)\b.{0,80}\b(law|laws|legal|legislation|statute|court|lawyer|rights|tenant|landlord|dismissal|employer|droit)\b)
  - match((?i)\b(law|legal|legislation|court|rights)\b.{0,60}\b(in|under|of)\s+france\b)
  - match((?i)\b(code civil|code du travail|code pénal|légifrance|legifrance|rgpd|prud'?hommes|rupture conventionnelle|garde à vue|code de la consommation|cnil)\b)
  - match((?i)\b(licenciement|bail d'habitation|droit du travail|droit de la famille|conseil juridique)\b)
  - semantic(what does French law say about my dismissal or employment contract, 0.74)
  - semantic(what are my rights as a tenant under French law, 0.74)
  - semantic(que dit le droit français sur mon contrat de travail, 0.71)
---

## Overview

This skill covers French legal information (droit français) in French or English: codes and statutes, rights, obligations and procedures, legislation and case-law research, citation validation, and EU cross-references. A database of French legislation from Légifrance/DILA offers full-text search and EU cross-references. It does not cover non-French law. Respond in French or English according to the user's preference.

## Mental model

EU law applies directly in France. Hierarchy: Constitution de 1958 (bloc de constitutionnalité) → droit de l'UE (primauté) → lois organiques et ordinaires → ordonnances (Art. 38) → décrets et arrêtés. Jurisprudence is not formally binding but highly influential. The legislation database is a snapshot: `check_currency` reflects its build date, so anything reformed recently needs the consolidated version confirmed on legifrance.gouv.fr. Figures that change yearly are stamped with their year; confirm them by web search before relying on them.

## Rules

### Research tools

- `search_legislation`: full-text search across all provisions with BM25 ranking.
- `get_provision`: retrieve a specific provision by statute and article.
- `validate_citation`: validate a citation against the database (zero-hallucination check).
- `format_citation`: format citations per French conventions (full, short, pinpoint).
- `build_legal_stance`: aggregate citations from statutes for a legal topic.
- `check_currency`: check whether a statute is in force, amended or repealed.
- `get_eu_basis`: EU directives and regulations underlying a French statute.
- `get_french_implementations`: find French laws implementing an EU act.
- `search_eu_implementations`: search EU documents with French implementation counts.
- `get_provision_eu_basis`: EU law references for a specific provision.
- `validate_eu_compliance`: check implementation status of EU directives.
- `about`: server info, capabilities and coverage summary.

Use web search for Cour de cassation and Conseil d'État decisions, doctrine and recent developments.

### Research protocol

1. Identifier le domaine: droit civil, pénal, commercial, administratif, social?
2. Rechercher la législation: `search_legislation` (French terms preferred).
3. Récupérer les dispositions: `get_provision` for exact statutory text.
4. Vérifier la validité: `check_currency` to confirm the statute is still in force.
5. Valider les citations: `validate_citation` before citing.
6. Droit UE: `get_eu_basis` for EU-derived French law (RGPD and others).
7. Jurisprudence: web search for Cour de cassation, Conseil d'État, Conseil constitutionnel.

Verify against current official sources (légifrance.gouv.fr), as the law evolves.

### Organisation judiciaire (court system)

```
Conseil constitutionnel (constitutionality)
Conseil d'État (administrative supreme court)
Cour de cassation (judicial supreme court)
    ↑
Cours d'appel (Courts of Appeal — 36)
    ↑
Tribunaux judiciaires (civil/criminal — 164)
Tribunaux de commerce (commercial) — 12 renamed tribunaux des activités économiques (TAE) on trial 2025–2028, handling insolvency for all professionals
Conseils de prud'hommes (employment)
Tribunaux administratifs (administrative)
    ↑
Tribunaux de proximité (chambres détachées) / Tribunaux correctionnels et de police (chambres du tribunal judiciaire)
```

### Droit civil: Code civil

- Droit des personnes: capacité, état civil, personnalité juridique.
- Droit de la famille: mariage, divorce (Art. 229 et s.), filiation, autorité parentale.
- Droit des obligations: contrats (Art. 1101 et s.), responsabilité civile (Art. 1240 et s.). Réforme du droit des contrats 2016 (Ordonnance n° 2016-131, ratifiée par la loi n° 2018-287): contracts signed before 1 Oct 2016 follow the old articles.
- Prescription: 5 ans in personal and movable actions from when the holder knew the facts (Art. 2224); 2 ans for consumer claims by a professional (Art. L218-2 C. conso).
- Droit des biens: propriété, possession, usufruit.
- Successions: Art. 720 et s.; réserve héréditaire, quotité disponible.

### Droit du travail: Code du travail

- CDI/CDD: contrat à durée indéterminée/déterminée.
- Licenciement: cause réelle et sérieuse; procédure obligatoire; contest within 12 months of notification (Art. L1471-1); damages capped by the barème (Art. L1235-3) except for null dismissals.
- SMIC: 2026: €12.02 brut/heure (décret n° 2025-1228); revalued at least every 1 January.
- Durée du travail: 35h/semaine; heures supplémentaires majorées.
- Congés payés: 5 semaines minimum.
- Prud'hommes: specialised court for employment disputes.
- Rupture conventionnelle: mutual termination agreement.

### Droit pénal: Code pénal

- Crimes, délits, contraventions: three levels of offences.
- Garde à vue: police custody; right to a lawyer from the start (since 2011).
- Présomption d'innocence: constitutional principle.
- Prescription: 20 ans (crimes), 6 ans (délits), 1 an (contraventions).
- Cour d'assises: jury trial for crimes; crimes punishable by 15-20 years go to the cour criminelle départementale (professional judges) nationwide since 1 Jan 2023.

### Droit des sociétés: Code de commerce

- SARL, SAS/SASU (startups), SA, SCI (real estate holding); registration at the RCS via the guichet unique (formalites.entreprises.gouv.fr).

### Droit immobilier

- Vente immobilière: compromis → acte authentique (notaire obligatoire).
- Bail d'habitation: loi du 6 juillet 1989; strong tenant protections. Encadrement des loyers applies in Paris, Lyon, Lille and other designated cities; the experiment ends on 23 Nov 2026 unless Parliament extends it (the Senate adopted a two-year extension at first reading on 21 Oct 2026 and the bill awaits first reading in the Assemblée nationale, as of 2026-11-15). Check Légifrance for the outcome before stating whether caps apply.
- Bail commercial: statut des baux commerciaux; 3-6-9 lease.
- Copropriété: loi du 10 juillet 1965; syndic, assemblée générale.
- DPE (Diagnostic de performance énergétique): G-rated homes are non décents and cannot be newly let or renewed since 1 Jan 2025, F from 2028, E from 2034 (metropolitan France); rents of F/G homes are frozen.

### Protection des données

- RGPD (EU 2016/679) plus Loi Informatique et Libertés 1978; CNIL enforcement; amendes up to €20M or 4% of worldwide turnover.

### Droit de la consommation

- Code de la consommation; DGCCRF enforcement.
- Délai de rétractation: 14 jours for distance contracts.
- Garantie légale de conformité: 2 ans for new goods (Art. L217-3 et s.); the seller bears the burden of proof for defects appearing within that period.
- Résiliation en trois clics: online subscriptions must be cancellable online since 1 June 2023.

### Procédure civile

- Tentative préalable de résolution amiable (conciliation, médiation, procédure participative) is required before suing for sums up to €5,000 and neighbour disputes (Art. 750-1 CPC), or the claim is inadmissible.
- Réforme de l'amiable (décret n° 2025-660, from 1 Sept 2025): judges can order a mediation information meeting, with a civil fine for unjustified absence.

### Propriété intellectuelle

- Droit d'auteur: life + 70 ans, automatic. INPI: marques 10 ans renouvelables, brevets 20 ans, dessins et modèles 5 ans renouvelables jusqu'à 25.

### Droit administratif

- Recours pour excès de pouvoir before the tribunal administratif within 2 months of the decision (Art. R421-1 CJA); responsabilité de l'État for faute de service.

### Ressources

- legifrance.gouv.fr (legislation), service-public.fr (official guidance), courdecassation.fr and conseil-etat.fr (case law), cnil.fr.
- avocat.fr (CNB annuaire national): find a lawyer.
- Aide juridictionnelle: justice.fr (legal aid).
- INPI: inpi.fr (IP).

## Output format

Scale to the question: lead with the direct answer and include the sections below only when they change what the user should do, or on request. Deadlines and red flags always appear when present.

1. Domaine juridique: area of law and applicable codes/statutes.
2. Textes applicables: key provisions with validated citations.
3. Explication claire: plain-language explanation.
4. Droit UE: EU law basis where applicable.
5. Jurisprudence: key decisions from the Cour de cassation and Conseil d'État.
6. Implications pratiques.
7. Délais: prescription periods, procedural deadlines.
8. Prochaines étapes: options, when to consult an Avocat.
9. Ressources: légifrance.gouv.fr, service-public.fr, Barreau.

## Checklist

- [ ] The area of law and the applicable code are identified.
- [ ] Every citation passed `validate_citation`, and recently reformed provisions were confirmed on Légifrance.
- [ ] EU law is noted where it applies directly in France.
- [ ] French citation conventions are used.
- [ ] The answer uses the user's language (French or English).
