---
name: doctor-interaction-checks
title: "Drug Interaction Check: Procedure and High-Risk Pairs"
description: "Step-by-step interaction check for a medication list, with FDA-label-sourced high-risk pairs: clopidogrel, simvastatin, nirmatrelvir/ritonavir, apixaban."
license: Apache-2.0
compatibility: "Requires: the medical-reference tools or web search for the current FDA label. Information only; the prescriber or pharmacist decides."
domains: doctor
rules:
  - content(interaction)
  - content(interactions)
  - content(taking together)
  - content(Paxlovid)
  - content(clopidogrel)
  - content(simvastatin)
  - match((?i)can i take .* with .*)
---

## Overview

A person lists two or more medicines and asks whether they mix. The outcome is a short table of pairs, each with the mechanism, the severity from the label, and the question to take to a prescriber or pharmacist. This skill adds the procedure and the pairs that the general interaction tables do not name. The agent never says to stop or change a dose.

## Mental model

Most serious interactions come from two causes: one drug changes how fast the liver enzyme (CYP) or transporter (P-gp) clears another, or two drugs add the same effect (bleeding, sedation, serotonin, potassium). Check the enzyme and the effect, then read the current label for the exact wording.

## Rules

Procedure

1. Write the full list: prescription, over-the-counter, supplements, doses, and start dates. Ask what was added or stopped recently; some effects last after a drug is stopped.
2. For each drug, pull the current FDA label (`get-drug-details`) and read the contraindications and drug-interaction sections.
3. Check each pair for an enzyme or transporter route, then for an additive effect.
4. Classify each pair from the label's own words: contraindicated, avoid, dose change, monitor.
5. Return the table and the questions for the prescriber or pharmacist. Say which pairs you could not check.

Pairs sourced from FDA labels (read the current label before quoting; labels change)

| Pair | What the label says |
|------|---------------------|
| Clopidogrel with omeprazole or esomeprazole | Avoid combining: both lower clopidogrel's antiplatelet activity through CYP2C19; dexlansoprazole, lansoprazole and pantoprazole had a less pronounced effect |
| Simvastatin with strong CYP3A4 inhibitors such as clarithromycin, erythromycin, itraconazole | Contraindicated; if a short course of the inhibitor is needed, simvastatin is to be suspended during it |
| Nirmatrelvir with ritonavir (Paxlovid) with other medicines | Contraindicated with drugs that depend heavily on CYP3A for clearance when high levels cause serious reactions, and with strong CYP3A inducers (for example carbamazepine, phenytoin, rifampin); cannot be started right after an inducer is stopped. Any medicine list needs a check against the current label |
| Apixaban with a combined P-gp and strong CYP3A4 inhibitor (ketoconazole, itraconazole, ritonavir) | For people on 5 mg or 10 mg twice daily the label directs a 50% dose reduction; people already on 2.5 mg twice daily should avoid the combination; clarithromycin needs no adjustment |

CYP450 enzyme reference (inhibitors raise the other drug's level, inducers lower it)

| Enzyme | Inhibitors (reduce metabolism) | Inducers (increase metabolism) |
|--------|-------------------------------|--------------------------------|
| CYP3A4 | Ketoconazole, erythromycin, grapefruit | Rifampin, carbamazepine, St. John's Wort |
| CYP2D6 | Fluoxetine, paroxetine, bupropion | None significant |
| CYP2C9 | Fluconazole, amiodarone | Rifampin |
| CYP1A2 | Fluvoxamine, ciprofloxacin | Smoking, charcoal-broiled meat |

Pairs not covered here (tramadol with serotonergic antidepressants, ACE inhibitor with trimethoprim and potassium) are not sourced in this skill: look up the current label and mark the result "label not checked in this skill".

## Examples

Bad: "Clopidogrel and omeprazole interact; stop the omeprazole."
Good: "The clopidogrel label says to avoid omeprazole and esomeprazole because they reduce its antiplatelet effect through CYP2C19; other acid reducers had a smaller effect. Ask your prescriber or pharmacist which acid reducer fits you before changing anything."

## Checklist

- [ ] Full list, including supplements and recent changes.
- [ ] Current label read for each drug.
- [ ] Pair severity quoted from the label, not from memory.
- [ ] Unchecked pairs named.
- [ ] No instruction to stop or change a dose.

## References

- Plavix label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2022/020839s078lbl.pdf
- Paxlovid label (2026 revision): https://www.accessdata.fda.gov/drugsatfda_docs/label/2026/217188s017lbl.pdf
- Simvastatin label (Zocor): https://www.accessdata.fda.gov/drugsatfda_docs/label/2020/019766s101lbl.pdf
- Eliquis label: https://www.accessdata.fda.gov/drugsatfda_docs/label/2025/202155s039s040lbl.pdf
