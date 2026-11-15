---
name: vehicle-ev-ownership
title: "EV Home Charging & Used Battery Health Guide"
description: "EV home charging, used-EV battery health checks, range and cold-weather numbers, incentive status. Use when buying or running an electric car."
license: Apache-2.0
compatibility: "Requires: web search and web page fetching."
capabilities: webfetch
domains: vehicle
rules:
  - match((?i)\b(ev|evs|electric (car|vehicle)|battery (health|degradation|warranty)|state of health|level 2 charger|home charger|wallbox|charging at home|ev tax credit|ev incentive)\b)
  - match((?i)\b(used (ev|electric)|buy(ing)? an? (ev|electric)|ioniq|leaf|bolt|model [3sxy]|id\.[3-7])\b)
---

## Overview

This skill answers the questions that come with owning an electric car: how healthy a used battery is, what home charging takes, how far the car really goes in cold weather, and which incentives exist now. Use it when someone is considering, buying or living with an EV. The outcome is a pass/fail battery check for a used car, a home-charging plan with the questions to ask an electrician, planning numbers for range, and the current incentive status with the source. High-voltage parts are work for professionals only; this skill never guides it.

## Mental model

An EV's value sits in its battery, so check the battery before the paint. Real range depends on temperature, speed and charging habit, and incentives are policy that changed in 2025. State each number with its source and date, and tell the buyer what to re-check.

## Rules

### Used-EV battery health

| Check | Pass | Pause or walk |
|---|---|---|
| Battery state-of-health (SoH) | An independent SoH report from a diagnostic provider (a short test through the OBD port) or a dealer report, with the date and the odometer | Only the dashboard range figure or the seller's word |
| Fit with age | SoH is consistent with the car's age and mileage; fleet data show about 2.3% capacity lost per year on average, up to about 3.0% per year with heavy DC fast charging above 100 kW and about 1.5% per year with mostly AC or lower-power charging (Geotab, Jan 2026) | A large gap against the average with no explanation |
| Same-model spread | The report is compared with other cars of the same model: one 500,000-test study found up to 13.5% SoH difference between examples of the same model (Aviloo, vendor-reported, 2026) | Treated as equal to the model's average |
| Battery warranty | In writing: years, miles, the capacity floor, and whether it transfers to a second owner; the remaining term covers the buyer's plans | Unknown terms, or the warranty ends on transfer |
| Charge port and charging | Both AC and DC charging started on a real charger during the test; no port damage or heat marks | Refused test, error messages, or charging stops early |
| Warnings and recalls | No battery or high-voltage warnings; recalls checked by VIN with the regulator and completed | Open battery recall |
| Climate history | Notes on hot-climate use (Geotab: about 0.4% per year faster loss in hot climates) | Not asked |

- A health figure reads one thing: capacity. A study noted that about 1% of used EVs hid a battery fault the health figure could not see, so keep the independent inspection (Aviloo, vendor-reported, via trade press, 2026).
- On-board readouts depend on the car's own battery management system and can differ from an independent test.
- High-voltage inspection and repair are for qualified technicians. Don't guide it.

### Home charging

- Level 1 uses a standard outlet (120 V in North America) and adds about 5 miles of range per hour; most new EVs include the cord (AFDC). Level 2 uses a 240 V circuit and adds about 25 miles per hour in the AFDC's current figure; older AFDC material says 10-20 miles per hour, and fueleconomy.gov says speed varies a lot by car (a few to about 40 miles per hour). Say it as a range and use the car's own maximum AC rate.
- Estimate the need first: miles driven per day x the car's miles per kWh = kWh per day; divide by the charger's kW to get hours. If hours are below the time the car is parked, Level 1 may be enough.
- A Level 2 charger needs a dedicated circuit. A licensed electrician checks the panel capacity, the run length and the permit. Don't guide panel or circuit work.
- Questions for the electrician: spare panel capacity, circuit amperage, cable run and cost, permit and inspection, and whether the utility offers a cheaper night rate.
- Charger and install incentives: federal, state and utility programs change. Look up the current status on irs.gov for federal credits and on the AFDC laws and incentives search for state and utility programs.

### Range planning numbers

- Advertised range is a test figure. Cold lowers it: at 20 F (about -7 C), AAA (2019) and fueleconomy.gov report about 41% less range with cabin heating on, and fueleconomy.gov about 12% less with the heater off; AAA's 2026 testing reports about 39% less. DOE (2024) reports heat pumps cut the heating draw by about 38% at 20 F.
- Plan with a lower usable range than advertised: in cold weather use the 20 F figures above; for road trips use the `travel-road-trip` skill's reserve and charging rules.
- DC fast charging slows as the battery fills; plan stops that charge to about 80% rather than 100%, and arrive at the next charger with a stated reserve.
- Frequent heavy fast charging goes with faster battery loss (Geotab figures above), so use home or lower-power charging for daily needs.

### Incentives

- The federal new clean vehicle credit (30D) and used clean vehicle credit (25E) end for vehicles acquired after 30 Sep 2025. A vehicle counts as acquired when a written binding contract is signed and a payment (including a down payment or trade-in) is made; the credit can still be claimed in the year the buyer takes possession (IRS FAQ). As of 2026-11, a purchase after that date has no federal vehicle credit.
- State, local and utility incentives, registration fees and charger rebates differ. Search the AFDC laws and incentives database for the buyer's state and say when it was checked.
- Look up the current status on irs.gov before telling a buyer anything about federal credits, because law can change again.

## Examples

Bad: "Battery shows 92% on the dash, so it's fine."
Good: "Ask for an independent battery health report with date and odometer, the battery warranty terms in writing, and proof both AC and DC charging worked. The dash figure is the car's own estimate."

Bad: "You'll get the $7,500 credit."
Good: "The federal credit ended for cars acquired after 30 Sep 2025 (IRS). Check your state's incentives in the AFDC database and your utility's charger rebates; I checked on [date]."

## Checklist

- [ ] An independent battery health report is requested, with date and odometer.
- [ ] Battery warranty terms and transferability are in writing.
- [ ] Home charging need was calculated from daily miles before recommending a charger level.
- [ ] Cold-weather range loss and fast-charging taper are included in any trip plan.
- [ ] Incentive claims name the source and the check date.
- [ ] No high-voltage or panel work was guided.

## Composition / References

- Pairs with `travel-road-trip` for EV trips and with the used-car inspection guide for the walk-through of one listing.
- IRS FAQ on credit changes: https://www.irs.gov/newsroom/faqs-for-modification-of-sections-25c-25d-25e-30c-30d-45l-45w-and-179d-under-public-law-119-21-139-stat-72-july-4-2025-commonly-known-as-the-one-big-beautiful-bill-obbb
- Fuel economy in cold weather: https://www.fueleconomy.gov/feg/coldweather.shtml
- AAA 2026 temperature study: https://newsroom.aaa.com/2026/05/aaa-study-reveals-temperature-impacts-on-ev-and-hybrid-performance-efficiency-and-costs/
- DOE 2024 cold-weather record: https://www.energy.gov/sites/default/files/2024-10/Impact_of_Cold_Ambient_Temperature_on_BEV_Performance_v15_TechEditFinal_12Sep2024__0.pdf
- Charging levels: https://afdc.energy.gov/fuels/electricity-stations ; https://www.fueleconomy.gov/feg/charging.shtml
- Battery degradation: https://www.geotab.com/press-release/ev-battery-health-degradation-fast-charging-study/ (Jan 2026) ; Aviloo study coverage: https://electrive.com/2026/09/02/battery-health-of-used-evs-varies-significantly
