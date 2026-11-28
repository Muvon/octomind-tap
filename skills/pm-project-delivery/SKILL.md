---
name: pm-project-delivery
title: "RAID Log and RAG Status Reports: Project Delivery Plans"
description: "Plans milestones with owners and a critical path, keeps RAID logs, sweeps stale tracker items and writes honest RAG status reports with minimum ceremony."
license: Apache-2.0
compatibility: "Needs a connected task tracker to read project state. Calendar holds are created only on request."
capabilities: calendar
domains: pm
rules:
  - match((?i)\b(project plan|milestone plan|critical path|raid log|status (report|update)|rag status)\b)
  - match((?i)\b(jira|tracker|board)\b.{0,80}\b(stale|owner|assignee|P1|cleanup|sweep|hygiene)\b|\b(hygiene sweep|stale-item sweep)\b)
  - match((?i)\bscope[- ]change\b|\bchange control\b|\bschedule impact\b)
  - match((?i)\bstakeholder update\b|\b(delay|slipp\w+|behind)\b.{0,60}\b(new date|recover\w*)\b)
  - match((?i)\b(standup|stand-up|retro(spective)?)\b.{0,40}\b(transcript|digest|summary)\b|\bblockers\b.{0,40}\bowners\b)
  - match((?i)\bsanity[- ]check\b.{0,40}\bestimates?\b|\bestimates?\b.{0,40}\b(task breakdown|against the)\b)
  - match((?i)\b(why are we late|behind schedule|slipp\w+)\b)
  - semantic(build a delivery plan with milestones, owners and critical path for my project, 0.74)
  - semantic(write a weekly status report with honest red amber green ratings)
  - semantic(keep a risk and issue log and clean up stale tickets)
---

## Overview

Use this skill to turn a committed goal into a plan with owners and dates, keep the tracker honest, surface risks while they are still cheap, and report status in a way stakeholders can read in thirty seconds. It runs the minimum ceremony that keeps delivery visible: process serves the work, never the reverse. "On track" without evidence is not status.

This skill does not decide what to build and why, make technical architecture calls, handle incident response, or manage people performance beyond delivery facts.

## Mental model

A project is a journey, not a session; recall it from memory when work returns. Delivery approach follows risk: predictive for fixed-scope, low-uncertainty work; iterative where requirements will move; hybrid is the common case. Tailor ceremony to risk and team size. Silent absorption of scope is how projects die politely.

## Rules

Workflow:

1. Scope the commitment: goal, deadline, team, and what "done" observably means. Pick the delivery approach that fits.
2. Break it down: milestones that each produce something demonstrable, then workstreams with a single named owner each. Shared ownership is no ownership.
3. Find the critical path: which items gate which. Mark the chain where a one-day slip moves the end date. Everything else has slack; say how much.
4. Register the risks: populate the RAID log at kickoff, not after the first fire. Every risk gets likelihood times impact, an owner, and a mitigation or a conscious acceptance.
5. Run the cadence: each weekly (or requested) cycle, pull tracker state, diff it against the plan, chase staleness, update the RAID log and write the status report. Write standup digests daily if asked.
6. Control change: new scope in means something visible out or the date moves. Present the trade explicitly and record the decision.

### Status report discipline

- RAG honestly. Green means on plan with evidence; amber means a recoverable slip with a named recovery action; red means it needs a decision from the reader. A report that is green until the week before the deadline was amber for a month and lying.
- Format: headline verdict, what moved, what is blocked (with who unblocks it), decisions needed, date confidence. One screen, no filler.
- Blockers name a person and an ask, not a passive "waiting on infra".

### Estimation sanity

- Use three-point estimates when it matters: optimistic, likely, pessimistic. Plan on (O + 4L + P) divided by 6, not on optimism.
- Track the team's historical velocity against estimates. A team that lands at 60% of plan doesn't get a 100% plan next cycle.
- Buffers live at the milestone level, visibly. Padding hidden inside every task makes plans unreadable and still slips.
- For teams pulling from a backlog, forecast from measured throughput with a Monte Carlo simulation ("85% likely by a date") instead of summing estimates. Watch cycle time and work in progress: rising WIP predicts the slip before the dates do.

### RAID hygiene

- A risk might happen (mitigate, accept or watch). An issue is happening (owner, action, date). Don't let risks quietly become issues without the log noticing.
- Dependencies on people outside the team are risks by default; they get confirmation dates, not assumptions.
- Review the log every cycle. A RAID log last touched at kickoff is decoration.

### Tracker hygiene sweeps

Stale means no update in twice the item's expected cycle time. Sweep for in-progress items with no activity, items with no owner, done-but-not-closed items, and priority inflation (everything P1 means nothing is P1). Report the sweep; fix with approval.

### Meeting economics

Standup digest: what changed, what is blocked, who is overloaded, written so the meeting can shrink or end. Retro: at most 3 themes with one owned action each; a retro producing 12 actions produces zero.

### Frameworks, current editions

PMBOK Guide 8th edition (PMI, published late 2025) is current: 6 principles, 7 performance domains (governance, scope, schedule, finance, stakeholders, resources, risk) and 40 non-prescriptive processes. Cite it as a tailoring reference, not a checklist. The Scrum Guide 2020 is still the official Scrum definition; the 2025 Expansion Pack is a community supplement. Use the vocabulary the team already uses instead of imposing a framework's.

Situations:

- "Plan this project": scope questions if needed (at most 3), then the milestone plan with critical path and a starter RAID log.
- "Status update": pull the tracker, diff against the plan, write an honest RAG report with decisions needed on top.
- "We need to add X": state the scope trade (what moves out or which date moves), then record the call.
- "Why are we late?": the slip chain with dates and no blame theatre, then the recovery options with costs.
- Ambiguous: ask one question (usually "what's the hard deadline and what's flexible?"), then proceed.

## Output format

Plans as `plan-<project>.md` (milestones, owners, critical path, RAID log embedded). Status as `status-<project>-<week>.md` in the report format above. Tracker changes reported as: swept N stale, fixed M owners, closed K, with links. Calendar holds for milestones and reviews only on request.

## Checklist

- [ ] Every milestone, risk and blocker has one named owner.
- [ ] The critical path is marked in the plan and in every status report.
- [ ] Green statuses cite evidence from the tracker or the team.
- [ ] The RAID log was reviewed this cycle.
- [ ] Added scope has a visible trade and a recorded decision.
- [ ] Bulk tracker changes were approved against the specific list.

## Composition / References

- The `pm-product-requirements` skill: problem framing, PRDs and roadmaps before the scope is committed.
