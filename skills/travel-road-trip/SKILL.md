---
name: travel-road-trip
title: "EV Road Trip Planner – Daily Legs, Fuel & Charging Stops"
description: "Road trip planner: drivable daily legs, rest stops, overnight towns, fuel or EV charging plan for the exact vehicle. Use when planning a road or EV trip."
license: Apache-2.0
compatibility: "Requires: web search, web page fetching and a maps service."
capabilities: webfetch
domains: travel
rules:
  - match((?i)\broad[- ]?trips?\b)
  - content(driving)
  - content(drive)
  - match((?i)\b(ev charging|charging stops?|fuel stops?|campervan|motorhome|rental car|hire car)\b)
---

## Overview

This skill turns a journey into drivable days with worthwhile stops, sensible overnight towns and a fuel or charging plan that works for the actual vehicle. It adds driving legs, rest limits and fuel or charging to the session's skeleton and day detail. Sightseeing days stay in the itinerary. It starts from the itinerary already in the session when one exists and asks only for what is missing.

## Mental model

Check live sources rather than promising a route from memory. The best route leaves room for tired people, slow roads and an unexpectedly good lunch. A scenic detour is optional, not a reason to exhaust the driver. Show distance, wheel time, stop time and arrival window separately. Driving limits and accessibility are hard constraints.

## Rules

### Workflow

1. Intake: take dates, origin, finish and must-see stops from the itinerary in the session. Ask only for what is missing: party and mobility, drivers, daily driving limit, vehicle model and fuel type, and relevant range or charging details.
2. Verify the frame: use the maps tools for each leg, and web search plus `knowledge(command="read", source="<url>")` for official road closures, seasonal access, ferries, daylight, stop hours and operator information.
3. Skeleton: propose overnight towns and daily distances, and explain the main trade-off against one useful alternative. Fold this into the session's skeleton step and confirm before detailing.
4. Detail legs: separate map driving estimates from breaks, visits, congestion allowances and charging. Check that arrival windows fit opening hours and overnight access.
5. Fuel or charge: place reachable primary and backup stops against conservative usable range, and verify compatibility, access hours, payment requirements and any published prices.
6. Deliver: reconcile every day's elapsed time and energy needs, cite checked sources with dates, and flag anything the traveler must recheck before departure.

### Driving rules

- Cite live map routes and operator or official pages next to factual claims. Label inaccessible sources, conflicts and unverified details rather than inventing distances, prices, specifications, laws or references.
- Show local dates and time zones when crossing them. Separate driving time from total elapsed travel time and protect rest breaks and meal time.
- Don't optimize away rest or recommend driving while fatigued. Shorten the day or add an overnight when the user's limit cannot be met.
- EV planning uses the exact vehicle's connector, usable battery, supported charging rate and the user's consumption where available. Verify manufacturer specifications and label modeled energy use as an estimate.
- Account for weather, elevation, load, towing and charging taper. State departure and arrival charge assumptions and the reserve, and don't equate advertised range with reliable usable range.
- Verify charger connector, public access, hours and operator status. A listing is not a guarantee of availability, so include a reachable backup and a pre-departure recheck.
- For combustion vehicles, state tank and consumption assumptions, plan a reserve, and check remote-area fuel access. Don't plan to arrive empty.
- Link official border, driving, toll and safety guidance for the route. The traveler verifies requirements for their passport and license. Medical fitness-to-drive questions go to a clinician, and legal eligibility is not decided here.
- Booking, buying and paying stay draft-only until the user explicitly approves. Don't call a route or charger guaranteed safe or available.

### Output shape

- Route summary: dates, vehicle, overnight towns, constraints, assumptions and total distance.
- Leg table: day, start and end, distance, map driving time, breaks and visits, total elapsed time and arrival window.
- Stops: purpose, checked hours, access notes, source links and verification date.
- Fuel or charging table: location, distance since last stop, arrival reserve, estimated stop duration, compatibility and backup.
- Before you drive: closures, weather risks, official requirements links and unresolved checks.

### Running without a human

- Chatting directly: if a material gap remains after reading the session, ask one focused question, then proceed with labeled assumptions.
- Brief marked AUTONOMOUS or non-interactive: ask nothing and skip skeleton confirmation. State assumptions, detail the recommended skeleton, and mark vehicle-dependent feasibility provisional if specifications are missing.
- In both modes, keep the reserve range and a reachable fallback in the plan.

## Examples

Bad: "Make it scenic" answered by swapping the overnight town for a coastal one with no numbers.
Good: show the added distance and elapsed time before changing overnight towns, and let the traveler choose.

Bad: "We're exhausted" answered by keeping the 9-hour day and suggesting coffee.
Good: shorten the next leg, add an overnight if needed, and preserve safe refueling or charging options.

Bad: "Charge at the highway station, about 400 km range, you'll be fine."
Good: state the exact vehicle's connector and usable range as an estimate, the arrival reserve, the checked station hours and operator status, a reachable backup, and a recheck before departure.

## Checklist

- [ ] Every leg uses a maps-tools result, with map driving time kept separate from breaks, visits and elapsed time.
- [ ] Arrival windows fit checked opening hours and overnight access.
- [ ] Time zone crossings are shown with local dates.
- [ ] No day exceeds the stated driving limit; shortened days or added overnights are noted.
- [ ] Each fuel or charging stop has an arrival reserve, compatibility check and a reachable backup.
- [ ] EV energy use is labeled an estimate, with the vehicle specifications source cited.
- [ ] Official border, toll and safety links are included, with requirements left for the traveler to verify.
- [ ] Sources carry verification dates; unverified items are labeled and listed under Before you drive.

## Composition / References

- Starts from the itinerary in the session; pairs with `travel-budget` for fuel, charging and tolls costs and `travel-packing` for vehicle-trip luggage.
- Sources are live map routes, operator and official road pages, manufacturer vehicle specifications, and official border, toll and driving guidance for the route.
