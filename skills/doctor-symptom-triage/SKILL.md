---
name: doctor-symptom-triage
title: "ER or Urgent Care: Symptom Triage by Urgency Tier"
description: "Sorts a symptom into ER now, same-day or urgent care, routine or self-care, with infant fever, child breathing, dehydration and poison-control rules."
license: Apache-2.0
compatibility: "Requires: web search to confirm local emergency numbers. US thresholds; outside the US use the national health service equivalent."
domains: doctor
rules:
  - content(should I go to the ER)
  - content(emergency room)
  - content(urgent care)
  - content(is this serious)
  - content(infant fever)
  - content(poison control)
  - match((?i)\b(baby|infant|newborn|toddler|child|kid|son|daughter|\d+[- ](week|month)[- ]old)\b.*(fever|temperature|breathing|wheez|vomit|throwing up|diarrhea|rash|dehydrat))
---

## Overview

A person describes a symptom and asks where to go: emergency room, urgent care, the doctor, or home. The outcome is one tier, the reason in one line, what to do before getting there, and the signs that move the person up a tier. This is orientation, not diagnosis.

## Mental model

Ask the single question that decides the tier first: is there a sign that threatens breathing, circulation or consciousness? If yes, the tier is emergency and everything else waits. A baby under 3 months with a fever of 100.4 F (38.0 C) is the one exception that gets an immediate phone call to the pediatrician instead. Only after that sort by speed of change and age. Children, pregnancy and people on blood thinners or with a weak immune system move up one tier for the same symptom.

## Rules

Tiers

| Tier | Action | Typical triggers |
|------|--------|------------------|
| Emergency now | Call emergency services (US 911) or go to the ER | Chest pain or pressure; trouble breathing; stroke signs (BE FAST); cannot be woken or is confused; bluish or gray lips or face (the AAP names bluish; gray is an added caution); ribs or collarbone pulling in with each breath; passed out; seizure; severe bleeding that does not stop |
| Same day | Call the doctor or nurse line now; urgent care if the office is closed | Fever or vomiting in a child with any sign listed under Children; a baby under 3 months with a temperature of 100.4 F (38.0 C) or higher (call the pediatrician right away; go to the ER if the office cannot be reached); dehydration signs; a symptom getting worse over hours; pain that stops normal activity |
| Routine | Book within days to weeks | Symptoms that are stable, mild or long-running; medication reviews; screening questions |
| Self-care | Home care with named upgrade triggers | Mild cold, minor cuts, mild stomach upset in a well-hydrated adult |

Children (American Academy of Pediatrics, healthychildren.org)

- Under 3 months (12 weeks) with a temperature of 100.4 F (38.0 C) or higher: call the doctor right away; go to the ER if the office cannot be reached. Do not give fever medicine before the baby is seen.
- Fever in any child: call the doctor if it rises above 104 F (40 C) repeatedly, lasts more than 24 hours under age 2, or lasts more than 3 days (72 hours) at age 2 or older, or if the child looks very ill, is unusually drowsy or very fussy, has severe headache, or repeated vomiting. A fever with a stiff neck: ER now. A fever with a seizure: call emergency services.
- Breathing, call 911 for: severe trouble breathing (struggling for each breath, can barely speak or cry), passed out or stopped breathing, bluish lips or face when not coughing. Go to the ER now for: any trouble breathing under age 1; ribs pulling in with each breath; trouble breathing with loud wheezing or stridor (a harsh sound when breathing in). Call the doctor now for: bluish lips or face only during coughing, soft wheezing, breathing much faster than normal, less severe trouble breathing. If no doctor or nurse calls back within 30 minutes, go to the ER.
- Croup (barking cough): call 911 for struggling for each breath or constant severe stridor, bluish lips or face when not coughing, drooling or great trouble swallowing. Go to the ER now for ribs pulling in, or stridor at under age 1. Call the doctor now for stridor heard now, non-severe trouble breathing, or bluish lips only during coughing.
- Dehydration signs: no urine for more than 8 hours, dark urine, very dry mouth and tongue, no tears. Call the doctor now. A child who cannot be woken or is not moving: 911. A child who is hard to wake, not alert when awake, has a stiff neck, vomits blood, or vomits green bile (not yellow stomach juice): ER now. A baby under 12 weeks with vomiting 2 or more times (not normal spit-up): call the pediatrician right away. Any other baby under 1 year with vomiting: contact the doctor within 24 hours.

Poison

- US Poison Help: 1-800-222-1222, free, confidential, 24 hours a day, every day, with interpreters (HRSA). Calls go to the poison center for the caller's area.
- If the person has collapsed, is having a seizure or is not breathing, call emergency services first, then poison help.
- Have ready: the product or plant, amount, time, the person's age and weight.
- Outside the US, find the national poison line by web search and name it.

Adults

- Chest pain or pressure; trouble breathing; stroke signs (BE FAST: balance, eyes, face droop, arm weakness, speech, time): emergency now.
- Pregnancy, new symptoms after surgery, or a diabetic with confusion: one tier up.

## Examples

Bad: "Fever in a 6-week-old is common; give infant acetaminophen and watch."
Good: "Call the pediatrician right away. A fever of 100.4 F or higher in a baby under 3 months needs a call to the pediatrician now, and the ER if the office cannot be reached."

## Checklist

- [ ] Age, symptom, start time and speed of change asked or stated as missing.
- [ ] One tier named with its one-line reason.
- [ ] Upgrade triggers listed for any tier below emergency.
- [ ] Emergency number and poison line given when relevant.
- [ ] No diagnosis, no medicine dose.

## References

- AAP fever: https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/When-to-Call-the-Pediatrician.aspx (read 2026-11-15)
- AAP symptom checker, breathing, croup and vomiting with diarrhea: https://www.healthychildren.org/English/tips-tools/symptom-checker/Pages/symptomviewer.aspx?symptom=Breathing+Trouble
- AAP urgent care, ER or pediatrician: https://www.healthychildren.org/English/family-life/health-management/Pages/urgent-care-ER-or-pediatrician-a-parent-guide.aspx
- Poison Help: https://poisonhelp.hrsa.gov/faqs/calling-poison-help/index.html
