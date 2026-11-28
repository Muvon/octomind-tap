---
name: vehicle-repair-diagnosis
title: "Car Diagnosis: Noises, Leaks, OBD-II Codes and Quotes"
description: "Car diagnosis from symptoms: narrows noises, leaks, smells, dash lights and OBD-II codes to likely causes; checks a repair quote against local prices."
license: Apache-2.0
compatibility: "Requires web search for local part prices, labor rates and known issues. Recall lookups need the VIN and the user's approval to submit it."
capabilities: memory-write
domains: mechanic
rules:
  - match((?i)\b(grinding|whirring|squeal\w*|clunk\w*|rattl\w+|knock\w*|ticking|vibrat\w+)\b.{0,80}\b(noise|sound)\b)
  - match((?i)\b(coolant|fuel|exhaust)\s+(smell|leak\w*)|\bsmell\w*\b.{0,30}\b(coolant|fuel|exhaust)\b|\bclunk\w*|\brough\s+idle\b|\bstalling\b)
  - match((?i)\b(sounds?|is\s+it)\s+(fair|reasonable)\b|ripped\s+off|\b(quote|estimate)\b.{0,100}\b(is|was)\s+reasonable|decompos\w+\s+(a\s+|the\s+)?(repair\s+)?(quote|estimate))
  - match((?i)\b(replac\w+|chang\w+)\b.{0,40}\b(spark\s+plugs?|air\s+filters?|brake\s+pads?|bulbs?|wipers?|water\s+pump)\b)
  - match((?i)\bmaintenance\s+(schedule|plan|tracker|tracking\s+sheet)\b|\bput\s+together\s+a\s+schedule\b)
  - match((?i)\bdiy\s+(versus|vs\.?|or)\s+(a\s+)?mechanic\b|\btriage\s+(a\s+)?(symptom|noise|leak|smell)\b)
  - match((?i)\bp0\d{3}\b.{0,200}\b(next\s+steps?|fix\s+it\s+myself|gas\s+cap|scanner)\b|\bscan\s+result\b|\bobd-?ii?\s+scan\b|\bwhat\s+maintenance\s+(should|do)\b)
  - semantic(what could cause this leak or smell under my car)
  - semantic(this repair quote from the garage, is the price fair, 0.74)
  - semantic(I scanned an OBD code, what does it mean and can I fix it myself, 0.69)
---

## Overview

This skill narrows a car problem from symptom to likely causes and to an honest verdict: how serious it is, whether it is a DIY job, and whether a repair quote is fair. It adds the symptom tables, code interpretation and quote arithmetic that sit behind the triage tiers and the DIY gate. The outcome is a short, ordered diagnosis with a confirm step per cause, never a verdict presented as certain.

## Mental model

Most symptoms have boring causes. Triage first, then narrow with cheap confirm steps, and put safety above price. A code or a noise names a system, not a broken part.

## Rules

### Procedure

1. Profile: make, model, year, engine, mileage and region. Recall the car from memory for returning users.
2. Triage by tier before explaining. Red is stop driving (red oil-pressure light, temperature red or steam, brake warning with a pedal change, flashing check-engine light, steering change, grinding brakes, fuel smell). Orange is this week (steady check-engine light, ABS or traction light, battery or charging light, a new noise that changes with speed, braking or turning). Yellow is soon (tire pressure, minor oil seep, wear-indicator squeal, cosmetic).
3. Narrow: symptom to two or three likely causes ordered by probability, with a confirm step for each.
4. Gate: classify the work as DIY-green, DIY-yellow (risks named) or pro-red, and state why.
5. Guide or brief: for DIY, exact parts (and how to match them by VIN or engine code), tools, and numbered steps with the universal safety line first. For a professional, what to tell the mechanic, what the fix should roughly involve, and the quote check.
6. Prevent: name the interval habit that avoids a repeat. Store car facts to memory with the user's confirmation; skip memory writes in autonomous runs.

Recalls: check the VIN every time. US: NHTSA lookup at nhtsa.gov/recalls (open safety recalls from the last 15 years; the remedy is free at the dealer). UK: the DVSA recall check on gov.uk. Elsewhere: the national regulator or the manufacturer. Web search also covers local labor rates, part prices and model-specific known issues and technical service bulletins.

### Symptom quick tables

Noises:
- Squeal on braking: wear indicators, pads soon.
- Grinding on braking: pads gone or rotors, red.
- Clunk over bumps: sway-bar links or ball joints.
- Click when turning: CV joint.
- Whine rising with road speed: wheel bearing.
- Whine rising with engine RPM: accessory or pulley.
- Ticking rising with RPM: check the oil level first, then lifters.
- Knock deep in the engine: red, stop.
- Belt squeal at cold start: belt or tensioner.
- Hum or roar: tires (cupping) versus bearing (changes in curves).

Leak colors:
- Brown or black: engine oil.
- Red or pink: transmission or power steering.
- Bright green, orange or pink with a sweet smell: coolant.
- Clear and oily near the wheels or firewall: brake fluid, red.
- Clear water under the A/C: normal condensation.

Smells:
- Rotten egg: catalytic converter.
- Sweet: coolant.
- Burning oil: a leak onto hot parts.
- Acrid electrical: wiring, red.
- Fuel: red.

Dashboard: red means stop safely now, with the engine off for oil or temperature. Amber means book it and drive gently. A flashing check-engine light is an amber light with red behavior.

### OBD-II codes

OBD-II is mandatory on US cars from model year 1996, EU petrol cars from 2001 and diesels from 2004. A code is a letter plus four digits: P powertrain, B body, C chassis, U network. P0xxx is generic across makes; P1xxx is manufacturer-specific. A code names the misbehaving system, not the broken part: P0420 means "catalyst efficiency low", commonly an oxygen sensor, not automatically a new catalytic converter. Read the code (a cheap reader or a borrowed scan tool), give the code and freeze-frame data to the mechanic, and never authorize replacing parts off a single code.

### Quote sanity check

1. Break the quote into parts, labor hours, rate and consumables. No itemization means walk.
2. Search the current part price (OEM versus named quality aftermarket brands) and typical book hours for the job (flat-rate guides) in the user's region.
3. Fair is roughly parts at retail within 30% plus book hours times the local rate. Flag duplicated overlapping labor, "flushes" bundled onto unrelated repairs, and replacing paired parts that don't require pairing.
4. A quote above about a typical day's labor cost earns a second quote from an independent shop, always. Asking for the old parts back is normal and keeps everyone honest.
5. Driver-assist cars: windshield replacement, wheel alignment, and bumper or ride-height work need the ADAS camera or radar recalibrated. A quote that omits it is incomplete, and one that bills it should name the procedure.

Do this without calling the shop dishonest; name what to ask instead.

### Used-car quick checks

- History first, by region: odometer, accident and finance checks through the local system (ask the country; examples are Carfax or AutoCheck, UK MOT history and HPI, EU service book and national registers), and match the VIN on the body and documents.
- Inspect cold: cold start (smoke color, rattle), panel gaps and paint mismatch (accident), tire wear evenness (alignment or suspension), fluids (milky oil means head gasket; burnt-smelling ATF), rust at structural points, all electrics.
- Test drive: brakes stop straight, steering centered, gearbox smooth cold and hot, no vibration at highway speed.
- The best money spent is a pre-purchase inspection by an independent mechanic. A seller who refuses it means walk.
- Timing-belt cars (not chain) without proof of a belt change on schedule: budget the job into the price.

## Examples

Code handling:
- Bad: "P0420, replace the catalytic converter."
- Good: "P0420 means catalyst efficiency is low. Check the downstream oxygen sensor and exhaust leaks first; a converter is the expensive last step."

Quote:
- Bad: "That price is a rip-off."
- Good: "Labor is 4.5 hours against a book time of 2.2. Ask the shop what the extra time covers, and get a second quote since the job is large."

## Output format

- Triage: a tier with a one-line reason.
- Likely causes: two or three, ordered, each with its confirm step.
- Verdict: DIY-green, DIY-yellow (risks named) or pro-red (what to tell the shop and a rough fair-cost range from current search).
- DIY: parts and tools with exact fitment guidance, then numbered steps, safety first, a checkpoint per step.
- Quote check: the itemized breakdown against the ranges found, and a one-line verdict ("fair", "get a second quote: labor doubled").

## Checklist

- [ ] Triage tier is stated first, with an upgrade trigger for any keep-driving advice.
- [ ] Causes are possibilities with confirm steps, not verdicts.
- [ ] No parts replacement is recommended off a single code.
- [ ] The DIY class is stated and no red-class work is guided.
- [ ] A quote was compared with current local ranges before judging it.
- [ ] A recall check by VIN was pointed to for the user's country.

## Composition / References

- `vehicle-maintenance` covers service schedules and the tracker file.
- `vehicle-used-car-inspection` covers a full walk-through of one listing.
- `vehicle-buying` covers price, loans and leases; `vehicle-ev-ownership` covers electric cars.
