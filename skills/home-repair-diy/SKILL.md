---
name: home-repair-diy
title: "DIY Home Repair or Call a Pro: Triage With Safety Gates"
description: "Diagnoses home problems for DIY home repair, classifies each job DIY-green, yellow or pro-red, and walks safe repairs. Use for leaks, outlets or quotes."
license: Apache-2.0
compatibility: "Needs web access for current local cost ranges, codes and appliance service guidance."
capabilities: filesystem-write
domains: handyman
rules:
  - match((?i)\b(step-by-step|walk me through|walkthrough)\b.{0,80}\b(replac\w+|patch\w*|re-?caulk\w*|install\w*|unclog\w*|fix\w*|repair\w*|swap\w*|troubleshoot\w*|faucet|drywall|cartridge)\b)
  - match((?i)\b(replac\w+|patch\w*|re-?caulk\w*|install\w*|unclog\w*)\b.{0,50}\b(faucet|cartridge|drywall|shower|exhaust fan|toilet|sink|drain|gutters?|thermostat|window|door|deck|furnace)\b)
  - match((?i)\b(tools?\s+(list|needed|i need)|shopping list)\b)
  - match((?i)\bpreventive\b.{0,20}\bmaintenance\b|\bmaintenance\s+schedule\b|\b(weatherstripping|caulking)\b)
  - match((?i)\b(gurgl\w+|drains?\s+(really\s+)?slowly|water stain|drafty|cold drafts?|sagging|horizontal crack)\b)
  - match((?i)\b(contractor|handyman|plumber|electrician)\b.{0,40}\b(quote|bid|hire|deposit|fair price)\b)
  - match((?i)\b(diagnos\w+|troubleshoot\w*)\b.{0,60}\b(toilet|outlet|dryer|faucet|window|sink|heater|fan|drafts?)\b|\brepair walkthrough\b)
  - match((?i)\b(fix|troubleshoot|handle)\b.{0,15}\b(it\s+)?myself\b|\bsafe to fix\b|\bdiy[- ]or[- ]pro\b|\btenant can handle\b)
  - semantic(there is a leak under my sink, what should I do, 0.74)
  - semantic(can I fix this electrical outlet myself or should I hire someone)
  - semantic(is this contractor quote fair for repairing my roof, 0.74)
  - semantic(walk me through a home repair step by step, 0.74)
---

## Overview

Use this skill when something in a home is broken, leaking, sparking or worn, or when the user asks whether to fix it themselves. It produces a likely cause with a way to confirm it, a verdict (DIY-green, DIY-yellow or pro-red), and for DIY jobs the exact parts, tools and numbered steps with safety checks first. It protects the person's safety first and their wallet second. A triage that ends at a professional counts as a success.

This skill does not rule on appliance-warranty claims or building-permit questions; point to the manual and the local authority.

## Mental model

Some jobs are legally restricted or lethal when done wrong: gas, mains electrical, structure, roofs at height, asbestos and lead. Those go to a licensed professional every time, however confident the user is. Everything else is a question of risk and reversibility. Calm, concrete steps matter more than reassurance, and a leak feels like an emergency until it is triaged into steps.

## Rules

Workflow:

1. Triage. Is anything actively flooding, sparking, smelling of gas or visibly sagging? If yes: emergency steps first (shutoff location, evacuate for gas, kill the breaker), professional second, diagnosis later.
2. Diagnose. Ask for symptoms one at a time: what, where, since when, what changed recently. Narrow to one or two likely causes and say how to confirm each ("dye tablet in the tank; if the bowl colors, it's the flapper").
3. Gate. Classify the confirmed job: DIY-green (low risk, reversible), DIY-yellow (doable with care; name the risks and the point of no return) or pro-red (licensed trade, safety or legal trigger). State the class and why.
4. Equip. For DIY jobs give exact parts, with how to identify the right size or model before buying, and tools at the cheapest tier that works. Name parts precisely ("3/8-inch compression fitting", "GFCI outlet") so the hardware-store trip works the first time.
5. Walk through. Numbered steps with the safety check up front (water off; breaker off and verified with a tester), a "you should now see X" checkpoint per step, and the undo path where one exists.
6. Prevent. After the fix, give a one-line prevention habit and offer a seasonal maintenance schedule. Store home facts (age, systems, past fixes) in memory with the user's confirmation.

Hard red lines, always a licensed professional:

| Trigger | Why |
|---|---|
| Gas smell, gas-line or gas-appliance connection work | Explosion and CO risk; illegal unlicensed in most jurisdictions |
| Inside the electrical panel, new circuits, aluminum wiring | Lethal; fire risk persists after the mistake |
| Load-bearing walls, foundation cracks wider than 6 mm (1/4"), sagging structure | Collapse risk; requires engineering judgment |
| Suspected asbestos (US homes built before about 1980, UK buildings before 2000: pipe or loft insulation, textured ceilings, floor tiles) or lead paint (US homes built before 1978) | Airborne toxicity; testing before disturbance, regulated removal and disposal |
| Roof work above one story, tree limbs near power lines | Fall and electrocution: the top DIY killers |
| Refrigerant circuits (air conditioner, heat pump, refrigerator) | Venting refrigerant is prohibited in the US, and buying or handling it for stationary equipment requires EPA Section 608 certification; call a certified technician |
| Mold over about 10 sq ft (3 ft by 3 ft), or any mold after significant water damage | EPA says larger areas go to a remediation professional; fix the water source first. Under 10 sq ft a homeowner can clean with an N-95 respirator, gloves and goggles |
| Radon test result at or above 4 pCi/L | EPA's action level; a qualified radon mitigation contractor fixes it. Consider fixing between 2 and 4 pCi/L |

Safety rules:

- Verify-dead rule for any electrical work beyond swapping a bulb: breaker off and confirmed with a non-contact tester at the fixture. State it every time; never assume the breaker label is right.
- Like-for-like swaps follow current code, not the old install. A replaced receptacle in a kitchen, bathroom, laundry, garage, basement or outdoors gets GFCI protection; three-prong receptacles on ungrounded wiring need GFCI protection and the "No Equipment Ground" label.
- Renters: diagnosis is theirs; repairs above unclogging a drain are usually the landlord's legal duty. Say so and help write the maintenance request.
- Alarms and appliances: replace smoke alarms 10 years after the manufacture date printed on them (NFPA), test monthly, and replace any alarm that fails the test or gives an end-of-life chirp; follow the maker's replacement date for carbon monoxide alarms. Clean the clothes-dryer vent, exhaust duct and lint filter regularly (CPSC says "periodically"; check the dryer's manual for the interval). Set a water heater to no more than 120°F (49°C) to reduce scalds (CPSC).
- Jurisdiction humility: codes and what is legal to DIY differ by country and state. US electrical work follows the locally adopted NEC edition; the 2026 NEC is published but adoption lags, and many areas still enforce 2020 or 2023, so check the user's locality. In England and Wales, Part P makes new circuits, consumer-unit work and electrical work in bathroom zones notifiable. For permit-adjacent jobs, search the user's locale and say when a permit question needs the local authority.
- Cost honesty: give the realistic professional cost range (current, local where possible, from a search) next to the DIY cost, so the decision is informed. Sometimes the professional is cheap insurance.
- Hiring a contractor, checks before any deposit: verify the licence on the state or local licensing board's website and that the name matches the person you meet; get at least 3 written bids on the same written scope; read the contract for scope, price, start and finish dates, change-order process and a payment schedule tied to completed work; many places cap deposits (California: the lesser of $1,000 or 10% of the price), so look up the local limit; ask for a lien waiver or release from the contractor and every subcontractor and supplier, and don't make the final payment until you are satisfied and have them (FTC); check whether a permit is needed and who pulls it; get warranties in writing.
- Videos and manuals: for model-specific appliance repairs, search for the model number's service guidance instead of generalizing across brands.
- Don't guess part sizes or torque a "probably fits" part: identify exactly, then buy. Don't shame the call-a-pro choice.

Situations:

- "Water is coming out of X!": shutoff first, then diagnose.
- "Can I do this myself?": gate honestly by the classification, not by encouragement.
- "The pro quoted $N, is that fair?": search current local ranges, compare, and name what the quote should include.
- Photo or model number offered: use it to narrow parts and steps.
- Ambiguous: ask one clarifying question, then proceed.

## Output format

- Diagnosis: likely cause or causes, each with the confirm step.
- Verdict: DIY-green, DIY-yellow (risks named) or pro-red (trade named, realistic cost range).
- For DIY jobs: parts and tools (exact names, how to match sizes or models, rough cost); steps (numbered, safety check first, checkpoint per step, undo path); aftercare (what to watch for 24 to 48 hours, the prevention habit).
- Save a maintenance schedule to `home-maintenance.md` in the working directory when asked.

## Checklist

- [ ] Emergency shutoff steps came before diagnosis when anything was leaking, sparking or smelling of gas.
- [ ] The job has a green, yellow or red class with the reason stated.
- [ ] No gas, in-panel electrical, structural, asbestos, lead or above-one-story roof guidance was given.
- [ ] Electrical steps state breaker off plus tester-verified dead.
- [ ] Parts are identified exactly, not guessed.
- [ ] Costs and local rules came from a search of the user's locale.

## Composition / References

- The `home-rent-vs-buy` skill covers housing decisions, mortgages and tenant basics.
- Sources named in the rules: NFPA, CPSC, EPA, FTC, NEC, Part P.
