---
name: vehicle-used-car-inspection
title: "Used Car Inspection Checklist: Listing Walk-Through"
description: "Builds a checklist for one used-car listing: seller questions, VIN and history research, in-person checks, red flags, and when to get a pro inspection."
license: Apache-2.0
compatibility: "Requires web search and page fetching to read the listing and cite official recall and history sources. Looking up a VIN with a third party needs the user's approval."
capabilities: webfetch
domains: mechanic
rules:
  - match((?i)\b(pre-?purchase|ppi)\b.{0,40}\b(inspection|brief|mechanic)\b|\binspection\s+(checklist|brief)\b)
  - match((?i)\b(seller|dealer|listing|craigslist|marketplace)\b.{0,100}\b(questions?|red[- ]flags?|checklist|history|vin)\b)
  - match((?i)\b(questions?|red[- ]flags?|checklist)\b.{0,60}\b(seller|dealer|listing)\b)
  - match((?i)\btest[- ]drive\s+plan\b|\bwalk[- ]?(around|through)\b.{0,40}\b(checklist|used|in\s+person)\b)
  - match((?i)\bvin\s+(research|check|history)\b)
  - match((?i)\bwhat\s+to\s+(check|look\s+at|look\s+for)\b.{0,60}\b(in\s+person|used|seller|before)\b)
  - match((?i)\bworth\s+paying\s+for\s+(an?\s+)?inspection\b)
  - semantic(I am going to see a used car tomorrow, what should I check before buying it, 0.72)
  - semantic(questions to ask a private seller before buying a used car, 0.74)
  - semantic(checklist for inspecting a used car in person before I buy it, 0.70)
  - semantic(check the vehicle history report and spot red flags in the listing)
---

## Overview

This skill turns one specific used-car listing into a practical plan for what deserves a closer look before any money changes hands: identity and history gaps, visible defects, unsafe test-drive conditions, and reasons to pay an independent professional. The outcome is a prioritized checklist, the seller questions, the history research plan and a brief for an independent pre-purchase inspection. It does not diagnose or repair an existing fault, review a repair quote or schedule service.

## Mental model

Think like a trustworthy independent mechanic, not a seller. Separate a seller's claim from an observation and from a verified record. Uncertainty is named honestly, and a clean-looking listing is not a clean bill of health. An inspection fee can be cheap insurance, but no report guarantees a trouble-free car.

## Rules

### Procedure

1. Intake: read the listing or supplied text and collect country, asking price and currency, make, model, year, engine or powertrain, odometer with units, seller type, VIN if available, and any history reports or service records. If there is no listing, ask for its URL or pasted details; don't substitute a generic checklist as if it were tailored.
2. Research: fetch the live listing details, manufacturer information, official recall sources and credible model-specific fault evidence. Cite URLs and access dates, and label inaccessible or unverified claims.
3. Screen: compare vehicle identity and mileage across the listing, documents and available records. Identify missing evidence and draft targeted questions before the visit.
4. Walk through, in this order: documents and cold arrival, exterior, body and tires, cabin and electrics, safe under-bonnet observations, stationary start, then an optional lawful test drive only if it is safe.
5. Gate: classify each finding as stop and walk away, pause for evidence or professional assessment, or ordinary wear. Don't turn suspected defects into diagnoses or guessed repair bills.
6. Brief: give a prioritized checklist and an independent inspection request tailored to this car, with the checks still outstanding and explicit conditions before any purchase decision.

### Evidence and history rules

- Research current sources and cite them. Never invent prices, specifications, laws, model defects, VIN results, references, or claims of having inspected the car physically.
- VIN: ask the buyer to compare visible vehicle identifiers with the registration or title and service documents. A decoder identifies a specification, not ownership, theft status, accident history or authenticity by itself.
- Match history checks to the country: official recall and inspection or odometer records where available, plus reputable accident, theft, title or write-off, and outstanding-finance sources. Explain coverage gaps and the limits of paid reports.
- A lookup not actually run is a check to run, not a passed check. Don't submit identifiers or personal documents to third parties without explicit authorization, and avoid reproducing unnecessary personal data.
- Ask the seller for a genuinely cold start, service invoices, timing-belt evidence where applicable, accident, flood and structural repairs, warning-light explanations, the reason for selling, and consent to an independent inspection.

### In-person checks

- Inspect panel gaps and paint mismatch, visible structural corrosion, water ingress, tire wear and age, seatbelts, the dashboard lamp self-check, and accessible fluid levels only as the manual permits. Don't open hot coolant systems or reach near moving parts.
- Pass or fail checks to record for each car:
  - OBD readiness monitors: read them with the buyer's own scan tool or at the pre-purchase inspection. EPA guidance lets inspection programs accept up to 2 unset non-continuous monitors on 1996 to 2000 cars and 1 on 2001 and newer (some states set different limits). Many unset monitors means codes or the battery were recently cleared: pause and ask why, since an unset monitor is not itself a fault.
  - Tire tread: at or below 2/32 in (about 1.6 mm) fails (NHTSA, nhtsa.gov/vehicle-safety/tires, as of 2026-11: replace at 2/32 in; penny test; 1.6 mm is the UK legal minimum, with 2 to 3 mm the usual advice to replace sooner). Uneven wear across one tire suggests alignment or suspension faults.
  - Tire age: the last four digits of the DOT code on the sidewall give the week and year of manufacture. NHTSA notes that some vehicle and tire makers recommend replacing tires 6 to 10 years old regardless of tread (as of 2026-11), so price a tire set in if they are near that age.
  - Flood signs. NHTSA (nhtsa.gov/hurricane-and-flood-damaged-vehicles, as of 2026-11) names the first three: a musty smell or strong air freshener; mud, dirt or water lines in hidden spots such as the trunk, glove box and under the dash; and unusual rust or corrosion for the car's age. The rest are common inspection practice: silt or water marks under carpets, fogging inside the lamps, rust on screws or seat bolts where water would not normally reach, corrosion in the fuse box. NHTSA also says to trace title history in NMVTIS because flood cars can carry clean titles. Any of these means pause or walk away.
  - VIN plates: the VIN on the dashboard plate, the door-jamb label and the paperwork must match character for character, and labels must look original and undisturbed. A mismatch or a tampered label is a stop.
- Test drive only with the seller's permission, a competent licensed driver and confirmed legal and insurance cover. Observe normal steering, braking, shifting, temperature and vibration on a safe route. No emergency maneuvers, no unsafe driving, no do-it-yourself fault reproduction.
- A red oil-pressure light, overheating or steam, a braking or steering change, a flashing check-engine light, grinding brakes or a fuel smell means stop safely and seek professional help; don't test-drive through it.
- Identity mismatches, unexplained odometer discrepancies, suspected flood or structural damage, concealed warning lamps, pressure for an immediate deposit, or refusal of an independent inspection justify pausing or walking away. If the seller refuses a cold start or an independent inspection, explain the risk and recommend walking away rather than arguing or paying a deposit.
- Recommend a buyer-chosen independent pre-purchase inspection before commitment, especially for uncertain history, modified cars, warning signs or expensive drivetrain risks. For a used hybrid or EV, also ask for an independent battery health report with date and odometer, and for the battery warranty terms and whether they transfer; use the `vehicle-ev-ownership` skill for the battery checks and have high-voltage inspection done by a qualified technician. Research any cost locally before quoting it.
- Don't clear codes, and don't treat an absence of fault codes as proof of health.

### Running without a human

A brief marked AUTONOMOUS or non-interactive: ask nothing. Produce the supported checklist with missing facts labeled and unavailable checks left pending.

## Output format

Return, in this order:
1. Listing identity, with verified facts kept apart from claimed facts.
2. Seller questions to ask before the visit.
3. Regional VIN and history checks, with links and status.
4. A checkbox walk-through ordered by visit stage. Each check names the action, the evidence to record, the red flag and the next decision.
5. The professional inspection brief, the unresolved risks, and the reasoning for proceed to inspection, pause or walk away. It is not a purchase or roadworthiness guarantee.

## Checklist

- [ ] The checklist is tailored to this listing and country, not generic.
- [ ] Verified, claimed and observed facts are kept apart.
- [ ] Every history lookup is marked run or still to run.
- [ ] Every cited standard carries its source and date.
- [ ] No physical check requires work under a jacked car or near high-voltage parts.
- [ ] The report states observation limits and leaves legal, title, insurance and roadworthiness to qualified local professionals.

## Composition / References

- `vehicle-repair-diagnosis` covers an existing fault or a repair quote.
- `vehicle-maintenance` covers the service schedule, useful for judging which service records the seller should show.
- `vehicle-buying` covers price research, loans and leases; `vehicle-ev-ownership` covers battery checks.
