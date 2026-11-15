---
name: travel-entry-rules
title: "Travel Entry Rules – EES, ETIAS, ETA, ESTA & Fees"
description: "Table of entry systems and fees: EU EES and ETIAS, UK ETA, US ESTA, Canada eTA, Australia ETA, Thai TDAC, and passport validity. Use for entry checks."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
capabilities: webfetch
domains: travel
rules:
  - match((?i)\b(etias|uk eta|eta (uk|canada|australia)|electronic travel (authori[sz]ation|authority)|entry/exit|esta|tdac|arrival card|visa[- ]free|visa waiver|entry requirements?|passport validity)\b)
  - match((?i)\b(do i need a (visa|passport)|passport (valid|expir)|real id|confirmid)\b)
---

## Overview

This skill holds the dated facts about electronic entry systems, so a trip plan can say which ones apply, what they cost and where to apply. Use it in the "verify the frame" and "before you go" steps of a trip plan. The outcome is a short entry-check list per destination with the official link, the fee as of the date below, and the passport rule. It flags what to check; it does not decide whether a person may enter.

## Mental model

Entry rules change often and scam sites copy official ones. The table below is a starting point dated 2026-11. Re-check the official page for the traveler's passport before relying on any row, and link that page in the plan. A system that is not yet running is not a requirement, and a site that takes fees for it is not official.

## Rules

### Entry systems (verified 2026-11)

| Destination | System | Status and fee | Official source |
|---|---|---|---|
| Schengen area | Entry/Exit System (EES) | Started in phases 12 Oct 2025; fully operational since 10 Apr 2026 at the external borders of the 29 Schengen countries. It does not apply at Cyprus and Ireland, which are not in the Schengen area. No fee, no advance application: biometrics are taken at the first border crossing, so queues are longer. | home-affairs.ec.europa.eu (EES news, 28 Apr 2026); travel-europe.europa.eu (EES page on who it does not apply to) |
| Schengen area | ETIAS | Not in operation as of 2026-11; no applications are collected. No confirmed start date: the EU page said last quarter of 2026, then Euronews (12 Aug 2026) reported the launch postponed indefinitely, with the EU saying it will announce the date several months before launch. Announced fee is EUR 20 when it starts. Look up the current position on the EU's official travel site before relying on it. Warn that any site taking ETIAS fees today is unofficial. | travel-europe.europa.eu (ETIAS page); Euronews, 12 Aug 2026 |
| United Kingdom | Electronic Travel Authorisation (ETA) | Needed by visa-exempt visitors, EU and US citizens included. GBP 20 online or in the UK ETA app; valid 2 years or until the passport expires, whichever is sooner. | gov.uk/eta/apply |
| United States | ESTA (Visa Waiver Program) | USD 40 (CBP, for applications paid after 30 Sep 2025); valid 2 years or until the passport expires. CBP published a notice on 10 Dec 2025 proposing mandatory social media history (5 years) as an ESTA field; no confirmation that it is in force was found, so check the ESTA site. Apply only on esta.cbp.dhs.gov. | esta.cbp.dhs.gov; Federal Register 2025-22461 |
| United States | REAL ID for domestic flights | Enforced since 7 May 2025. Without a compliant ID or passport, TSA ConfirmID costs USD 45. | tsa.gov/real-id |
| Canada | electronic Travel Authorization (eTA) | For visa-exempt travelers arriving by air. CAD 7; valid up to 5 years or until the passport expires; linked to the passport used to apply (a new passport needs a new eTA). Canadian dual citizens travel on a Canadian passport. | canada.ca (eTA pages) |
| Australia | Electronic Travel Authority (ETA, subclass 601) | AUD 20 service charge, non-refundable, paid in the Australian ETA app. Eligible passports differ; check the Home Affairs page. | eta.homeaffairs.gov.au; immi.homeaffairs.gov.au |
| Thailand | Thailand Digital Arrival Card (TDAC) | Free on the official site; submit in the 3 days before arrival. Not a visa. Third-party sites that charge are agents. | tdac.immigration.go.th; Thai embassy pages |

### Passport validity

- Schengen: the passport must be valid at least 3 months after the planned departure from the Schengen area, and issued within the previous 10 years on the day of entry (Your Europe and the Commission's Home Affairs site).
- Other countries commonly set their own minimum, often longer. Don't assume the Schengen rule; read the destination's official entry page and the airline's travel-document check.
- Check blank pages and damage rules on the same official page.

### How to use the table

1. Put each row that applies to the traveler's passport and route into the plan's "Before you go" section, with the fee, the deadline and the official link.
2. Date-stamp the check ("checked 2026-11-15") and tell the traveler to re-check close to departure.
3. If a row may have changed since 2026-11, search the official source first and say which source you used.
4. Visa law, residence, work rights and immigration status are legal questions: say so, and point the traveler to the legal domain through the global assistant. Travel insurance questions go to the finance domain's insurance help.

## Examples

Bad: "You'll need to apply for ETIAS before your Paris trip."
Good: "ETIAS is not running and has no confirmed start date, so there is nothing to apply for. EES biometric registration will happen at your first Schengen border: pad arrival-day plans and tight connections. Passport must be valid 3 months past departure. Checked 2026-11-15 on travel-europe.europa.eu."

Bad: "ESTA costs about $40, apply on any ESTA site."
Good: "ESTA is USD 40 as of 2026-11, applied for only at esta.cbp.dhs.gov. A proposal to require 5 years of social media history was published in Dec 2025; check the site for whether it applies now."

## Checklist

- [ ] Each system listed applies to this passport and route, or is marked not applicable.
- [ ] Every fee carries an as-of date and an official link.
- [ ] ETIAS is described as not operating, with no apply instruction.
- [ ] Passport validity was checked against the destination's own rule.
- [ ] Legal and insurance questions were routed, not answered.

## Composition / References

- Pairs with `travel-packing` (documents section) and `travel-road-trip` (border and toll guidance).
- EES: https://home-affairs.ec.europa.eu/news/main-differences-between-ees-and-etias-what-travellers-need-know-2026-04-28_en (28 Apr 2026)
- EES exceptions: https://travel-europe.europa.eu/ees/whom-does-ees-not-apply_en ; https://www.diplomatie.gouv.fr/en/presse-et-ressources/decouvrir-et-informer/actualites/ees-le-nouveau-systeme-europeen-de-gestion-des-frontieres-entre-en-service-le-10-avril-2026
- ETIAS: https://travel-europe.europa.eu/etias_en ; https://www.euronews.com/2026/08/12/europe-has-officially-delayed-the-roll-out-of-the-etias-travel-permit-indefinitely (12 Aug 2026)
- UK ETA: https://www.gov.uk/eta/apply
- ESTA: https://esta.cbp.dhs.gov ; https://www.federalregister.gov/documents/2025/12/10/2025-22461/agency-information-collection-activities-revision-arrival-and-departure-record-form-i-94-and (10 Dec 2025)
- REAL ID and ConfirmID: https://www.tsa.gov/real-id
- Canada eTA: https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/eta.html
- Australia ETA: https://www.eta.homeaffairs.gov.au/ETAS3/etas
- Thailand TDAC: https://tdac.immigration.go.th ; https://dubai.thaiembassy.org/en/content/thailand-digital-arrival-card-tdac
- Passport validity: https://europa.eu/youreurope/citizens/travel/entry-exit/non-eu-nationals/index_en.htm
