---
name: vehicle-maintenance
title: "Car Maintenance Schedule – Service Due Dates & Log"
description: "Car maintenance schedule builder that works from the manufacturer's documents for one exact car, picks normal or severe service, calculates next due by time and distance, reconciles service records, and keeps car-maintenance.md up to date. Use when the user asks what service is due, for a car maintenance schedule or service intervals, or to log completed work."
license: Apache-2.0
compatibility: "Requires: web search, web page fetching and file writing."
capabilities: webfetch
domains: vehicle
rules:
  - content(maintenance)
  - content(servicing)
  - match((?i)\b(service (schedule|intervals?)|next service|oil change|due next|what('s| is) due|log (the )?service)\b)
---

## Overview

This skill turns the manufacturer's service requirements for one exact vehicle into a practical plan and a readable tracker file, `car-maintenance.md`. Use it when the user asks what service is due, wants a maintenance schedule, or reports completed work. The outcome is a source-backed schedule, a list of unknowns, and next due dates and distances the user can trust. A tidy checklist is useful only when its intervals fit the car. When the session is checking a car someone is about to buy rather than one the user owns, use the schedule only to judge which service records the seller should show; don't create or update a tracker.

## Mental model

The maker's own document for the exact year, engine and market is the only authority. Dealer upsells, forum intervals and another model year's manual are not requirements. Every deadline comes from a confirmed date or odometer reading plus a sourced interval. Anything without evidence stays unknown, never assumed done. Cheapest correct upkeep, named honestly, with safety first.

## Rules

### Vehicle profile

Collect before assigning numbers: make, model, model year, engine or powertrain, market, current odometer with units, in-service date if known, service records, and driving conditions such as towing, short trips, dust, extreme temperatures or prolonged idling. Reuse what the session already knows about the car.

### Finding the maker's schedule

- Search live for owner manuals, maintenance booklets and official service pages matching that exact year, engine and market. Read the relevant pages with `knowledge(command="read", source="<url>")` rather than relying on search snippets; this also handles PDFs.
- Cite per source: document title, URL, edition or year, page or section, and access date.
- Check whether the maker's severe-service definition applies to the stated conditions and explain the schedule chosen. Severe service may shorten only particular items; don't shorten every interval or replace the maker's rule with a universal annual oil change.
- Never invent intervals, fluid specifications, capacities, torque values, prices, laws or references. Label missing maker information as unverified and say how to obtain it.
- Hybrids and EVs: verify the powertrain-specific schedule. Fewer oil changes do not mean no brake, coolant, tire or inspection requirements.

### Calculating what is due

- Compute next service from the confirmed completion date and odometer, by both time and distance, whichever comes first.
- Keep fixed milestones separate from repeating intervals and from oil-life-monitor instructions.
- Unknown history is not completed maintenance. Record it as unknown, seek evidence, and propose a professional baseline assessment without claiming the car is safe until then.
- Keep the original miles or kilometers next to any labeled conversion. Record the odometer's observation date. Calendar dates projected from estimated driving are labeled as estimates.
- Separate recommended inspection from required replacement. Follow the maker's monitor and reset rules; don't suggest resetting a reminder without completed service.
- Sort items into overdue, due now, next due, condition-based inspection and unknown history. Safety items go to a professional rather than getting an invented baseline.
- Any physical job follows the session's DIY gate and safety line. Warning signs mean stop and triage now, not wait for the interval.

### Tracker file

- Read any existing `car-maintenance.md` first. Create or update it with `text_editor` or `batch_edit`, preserve prior entries, and don't overwrite unrelated records.
- Contents: profile and units; source references; service history with evidence; the table `item | maker interval/conditions | last date/odometer | next date/odometer | status | source`; an update log.
- Keep estimated dates apart from verified deadlines.
- Never mark work completed without the user's confirmation or a matching service record.
- A new receipt or odometer reading: reconcile with existing history, update only the supported items, recalculate next due.
- After saving, verify the file and report its path and the next due items. Store stable car facts with `memorize` after the user confirms them; skip memory writes in AUTONOMOUS runs.

### Output shape

Return the confirmed vehicle profile, the source-backed schedule, unknowns, and the next three actions.

### Running without a human

- Chatting directly: if exact fitment or mileage is missing, ask one focused question before assigning numeric due intervals.
- Brief marked AUTONOMOUS or non-interactive: ask nothing. State the missing fields, save a provisional tracker, and leave unsupported deadlines unknown rather than guessing.

## Examples

Unknown history:
- Bad: "Oil change done at 60,000 km, so the 12-month brake fluid check is probably fine too."
- Good: "Oil change recorded at 60,000 km on 2025-03-02 (receipt). Brake fluid: no record, status unknown. Ask for the invoice or book a baseline check."

Severe service:
- Bad: "You drive short trips, so I halved every interval."
- Good: "The manual (title, p. 42, accessed today) lists short-trip driving as severe service for oil and filter only. Those two use the shorter interval; the rest stay normal."

Reset request:
- Bad: "Reset the service light so it stops nagging."
- Good: "Reset it after the service is done and logged, using the manual's reset procedure. Is there an invoice to add?"

## Checklist

- [ ] Profile has make, model, year, engine, market, odometer with units and date, and conditions, or the gaps are stated.
- [ ] Every interval cites document title, URL, edition or year, page or section, and access date.
- [ ] Normal versus severe service is decided and explained per item.
- [ ] Next due is computed by time and distance, whichever comes first.
- [ ] Unknown history is marked unknown, not done; estimated dates are labeled.
- [ ] Original units and any conversion both appear.
- [ ] `car-maintenance.md` was read first, prior entries are intact, and the update log has a new line.
- [ ] No item is marked completed without confirmation or a record.

## Composition / References

- Works inside a session that already handles symptom triage, the DIY gate, recalls and car memory; this skill adds scheduling and tracking only.
- Sources are the maker's owner manual, maintenance booklet and official service pages for the exact car.
