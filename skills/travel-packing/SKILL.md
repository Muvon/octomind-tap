---
name: travel-packing
title: "Packing List Generator – Weather-Based Trip Checklist"
description: "Packing list from itinerary, destination forecast, activities, laundry and baggage allowance, saved as a checkbox file. Use when asked what to pack."
license: Apache-2.0
compatibility: "Requires: web search, web page fetching and file writing."
capabilities: webfetch
domains: travel
rules:
  - content(packing)
  - content(pack)
  - content(luggage)
  - content(suitcase)
  - match((?i)\b(carry[- ]on|checked bags?|baggage allowance|what to (bring|wear))\b)
---

## Overview

This skill turns one trip's destination weather, activities, length and luggage limits into a checklist the traveler can pack from. It starts from the itinerary already built in the session when one exists and asks only for what is missing. The outcome is a saved checkbox file with quantities, bag allocation, the weather and baggage facts behind it, and a weight check.

## Mental model

Favor versatile layers and realistic laundry over just-in-case clutter. Light luggage is useful, but comfort, accessibility and essential equipment come first. Quantities and a reason beat a long list of possibilities. Separate essential, activity-dependent and optional items without shaming preferences. Verify what changes (forecast, allowances, restrictions) and save the result as a usable file, not a generic travel essay.

## Rules

### Workflow

1. Intake: read the itinerary in the session if there is one. Gather only what is missing: destinations and dates, travelers, duration, activities, accommodation and laundry access, existing equipment, and each carrier's fare or baggage allowance.
2. Weather: use web search for the destination forecast for the actual dates from a current meteorological source. Cover temperature range, precipitation, wind and relevant altitude differences.
3. Constraints: verify official carrier dimensions, weight and item limits, plus airport or authority rules for liquids, batteries and restricted equipment, on every relevant leg. Read the official pages with `knowledge(command="read", source="<url>")`.
4. Build: calculate clothing quantities around laundry intervals and activities, choose reusable layers, and assign documents, valuables and essentials to suitable bags.
5. Audit: check for missing activity essentials, redundant items, conflicting restrictions and weight assumptions against the strictest applicable allowance.
6. Save: create the file with `text_editor`, read it back to verify the contents, and return its exact path plus remaining checks and a forecast-refresh reminder.

### Packing rules

- Cite source URLs and verification dates for forecasts, baggage allowances, equipment specifications and restrictions. Don't invent prices, specifications, laws or references.
- A forecast is not a climate average. Beyond the forecast horizon, label seasonal guidance provisional and state when to refresh it. Don't fabricate daily weather.
- Match the actual operator, route, cabin and fare. If the ticket allowance is unknown, say the traveler must confirm it; don't declare a bag compliant.
- Express quantities per person unless an item is shared. Tie socks, underwear and outfits to trip duration and laundry access, with a stated small contingency.
- Distinguish measured weights from estimates. Total known and estimated weights separately and leave headroom rather than certifying an unweighed bag.
- Use the user's activity list, not imagined excursions. Technical or safety-critical equipment needs the operator's current requirements and qualified advice, not generic reassurance.
- Medication entries mean the traveler's existing prescribed supplies and documents. Don't recommend new drugs, doses or treatment, and refer medical questions to a clinician.
- Link official entry and restricted-item guidance for the traveler to verify. Don't make legal eligibility determinations or ask for passport numbers or medical records.
- Don't request credentials or store copies of sensitive documents.
- Don't overwrite an existing checklist without permission; create a unique suffixed filename when necessary.
- Buying equipment, booking and paying stay draft-only until the user explicitly approves.

### Output shape

Save `packing-<destination-slug>-<departure-date>.md` in the working directory; use `undated` if dates are unknown.

- Trip summary: destination, dates, duration, travelers, activities, laundry and luggage assumptions.
- Weather and baggage basis: checked facts, sources, dates and forecast coverage gaps.
- Markdown checkboxes grouped into documents, clothing, footwear, toiletries, existing medicines, electronics, activity equipment and departure checks.
- Each checkbox: item, quantity, bag allocation, and the reason when weather- or activity-dependent.
- Weight check: allowance, known subtotal, estimated subtotal, headroom and items still to weigh.
- Before departure: unresolved restrictions and the forecast-refresh date.

### Running without a human

- Chatting directly: if a material gap remains after reading the session, ask one focused question, then proceed with labeled assumptions.
- Brief marked AUTONOMOUS or non-interactive: ask nothing and skip confirmations. State assumptions, create the checklist, and label unverified weather or allowance constraints provisional. If a checklist file already exists, write a suffixed filename instead of asking.
- In both modes, report a write failure honestly.

## Examples

Bad: user says "carry-on only" and the reply is a full-size wardrobe with a note to check the airline later.
Good: prioritize reusable layers and laundry, then check the actual ticket's allowance and total the weight against the strictest leg.

Bad: "It's colder than expected" triggers a rebuilt list for the whole trip.
Good: revise the affected layers and weight totals only, keep the rest, and update the forecast-refresh date.

Bad: "Bag is 7 kg, fits the carry-on limit" with no source and no ticket details.
Good: "Allowance unconfirmed for this fare: traveler must confirm. Known subtotal 5.2 kg, estimated 2.0 kg, headroom unknown until the limit is checked."

## Checklist

- [ ] The saved file is named `packing-<destination-slug>-<departure-date>.md` (or `undated`) and was read back after writing.
- [ ] Forecast, allowances and restrictions each carry a source URL and a verification date.
- [ ] Forecast coverage gaps and seasonal guidance are labeled provisional with a refresh date.
- [ ] Every checkbox has a quantity and a bag allocation.
- [ ] Known and estimated weights are totaled separately against the strictest allowance.
- [ ] Medication entries list only existing prescribed supplies; no recommendations were made.
- [ ] No existing file was overwritten and no sensitive document copies were stored.
- [ ] Assumptions and unverified items are stated.

## Composition / References

- Starts from the itinerary in the session; hand the trip budget to `travel-budget` and driving legs to `travel-road-trip`.
- Sources are the carrier's own baggage pages, airport or authority restricted-item pages, and a current meteorological forecast.
