---
name: pm-product-requirements
title: "Product Requirements Document (PRD): Stories, RICE, OKRs"
description: "Turns fuzzy ideas into problem statements, PRDs, user stories, RICE-scored roadmaps and OKRs, with an explicit never list. Use when deciding what to build."
license: Apache-2.0
compatibility: "Needs web access for competitor scans. Backlog sync needs a connected task tracker."
domains: pm
rules:
  - match((?i)\b(write|draft|create)\b.{0,30}\b(prd|product requirements? document|one-pager|product brief)\b.{0,40}\b(for|covering|with)\b)
  - match((?i)\b(score|rank|prioriti[sz]e)\b.{0,40}\b(with|using|by)\s+(rice|moscow)\b|\brice[- ]scor(ed|e)\b)
  - match((?i)\b(turn|reframe|rewrite)\b.{0,60}\bproblem statement\b|\bdiscovery (questions|plan)\b|\breframe\b)
  - match((?i)\b(competitive|competitor)\s+(scan|analysis)\b|\bcompar\w+\b.{0,30}\bhow\b.{0,60}\b(handle|price|pricing)\b)
  - match((?i)\b(slice|split)\b.{0,40}\b(roadmap|releases?)\b|\bexplicitly out of scope\b|\bnon-goals?\b)
  - match((?i)\b(dedupe|deduplicate|merge duplicates|worth keeping)\b|\btag\b.{0,30}\btheme\b)
  - match((?i)\bprioriti[sz]\w*\s+(list|backlog|roadmap)\b|\b(feature (requests|ideas))\b.{0,60}\b(rank\w*|score|prioriti\w+)\b)
  - match((?i)\b(write|draft|set|define|create)\b.{0,30}\b(okrs?|key results|roadmap|success metrics?)\b|\b(break|split)\b.{0,20}\binto\s+(user\s+)?stories\b)
  - semantic(turn my rough product idea into a clear problem statement and PRD, 0.71)
  - semantic(write user stories and acceptance criteria for this feature)
  - semantic(prioritize my roadmap using RICE and set OKRs)
---

## Overview

Use this skill to decide what to build and why. It turns fuzzy ideas, stakeholder requests and messy backlogs into problem statements, PRDs, user stories, prioritized roadmaps and OKRs that a team can execute and a leader can defend. The instinct is problem-first: what the user needs and what evidence exists come before any solution. The best PRD is known for what it excludes.

This skill does not cover technical design documents and API specs, delivery tracking and risk registers, fundraising decks, idea-stage market validation for a company that does not exist yet, or UX audits of existing interfaces.

## Mental model

A feature request is a symptom of a job the user wants done. Evidence decides priority, not the seniority of the requester. Discovery effort should be proportional to how hard a decision is to reverse. When evidence is thin, the answer is the cheapest experiment, not a longer document.

## Rules

Workflow:

1. Frame the problem: who has it, how often, what they do today, what it costs them. If the request arrives as a solution ("add an export button"), reverse it into the underlying job first. No document starts until the problem statement survives "so what?".
2. Gather evidence: pull prior product context from memory; search competitors and prior art; ask for usage data, support themes or customer quotes. Label every claim as evidence-backed or assumption. Assumptions get a validation plan, not a hidden promotion to fact.
3. Define success: one primary metric that moves if this works, guardrail metrics that must not regress, and the time window. "Engagement" is not a metric; "week-4 retention of new signups" is.
4. Write the artifact (see Output format). Scope has three lists: now, later, never. The never list (non-goals) prevents the scope creep that kills delivery.
5. Prioritize: score candidates with RICE by default (reach times impact times confidence, divided by effort); switch to MoSCoW when the ask is a release cut. Show the scoring table so the ranking is arguable. A priority order nobody can argue with is a priority order nobody checked.
6. Sync the tracker: when connected, create or update issues from the agreed stories, one issue per story, with acceptance criteria in the body. Confirm before bulk operations.

### PRD anatomy (one-pager first, expand only if asked)

Problem (with evidence), then users and jobs to be done, then success metrics and guardrails, then scope (now, later, never), then a solution sketch (the lightest thing that could work), an eval plan for any AI or LLM behavior, risks and open questions, and a launch checklist. A PRD that leads with the solution is returned to sender.

### User stories

Format: As a (specific user), I want (capability) so that (outcome). Write acceptance criteria in Given/When/Then, 3 to 7 per story; more means the story needs splitting. Stories are vertical slices a user could notice; "build the database table" is a task, not a story. Check every story against INVEST: independent, negotiable, valuable, estimable, small, testable.

### Prioritization discipline

- RICE: reach (users per quarter), impact (3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal), confidence (100, 80 or 50%; below 50% means go validate, not guess), effort (person-weeks). Show the arithmetic.
- The loudest stakeholder's request enters the same scoring as everything else. Provenance is not priority.
- Use a Kano lens when the roadmap looks all-maintenance: basics must work before delighters earn their slot.
- Cut scope by shipping the smallest thing that tests the riskiest assumption, not the smallest thing that is easy.

### Metrics

- One north-star metric per product and 2 to 4 guardrails per launch (latency, churn, support volume, revenue).
- Prefer leading over lagging metrics where possible. Define the counter-metric for every growth metric (activation up plus support tickets up is not a win).
- Pre-register the decision rule: "if the metric doesn't move X% in Y weeks, we roll back, iterate or kill."

### AI features, the eval is the spec

Model behavior can't be fully specified in prose, so acceptance criteria become an eval set: 50 to 200 real or realistic inputs (including known failure modes, edge cases, and adversarial or unsafe requests) with expected outputs or graded rubrics. Set the quality bar per dimension (correctness, groundedness, tone, refusal behavior) before building, and add cost and latency per task as guardrails. Write a first draft, then refine it after reading real failure traces, because the useful failure categories only show up in actual outputs. LLM-as-judge scores count only once they are calibrated against human labels. Launch gate: the eval threshold is met and a human-reviewed sample passes. After launch, production failures feed back into the set. Include a human fallback for low-confidence cases.

### OKRs

An objective is a qualitative, time-boxed outcome that a team can influence and that is clearly achieved or not. Each has about 3 key results, each a measurable outcome with a baseline, a target and an owner, never a task or an activity verb such as "consult" or "analyze". Keep 3 to 5 objectives per team; more than 5 spreads effort (Google re:Work, "Set goals with OKRs", rework.withgoogle.com/intl/en/guides/set-goals-with-okrs, as of 2026-11). Score each key result 0.0 to 1.0 at the end of the period; Google's target for stretch goals is 0.6 to 0.7, and consistently hitting 1.0 means the goals were too easy. Label each key result stretch or committed (committed ones are expected at 1.0). Write the objective first, then the key results that would prove it, then the initiatives that might move them. Check each key result: can it be measured weekly, does the team control the lever, and could it be hit without the objective being true? If the last answer is yes, rewrite it. Link each objective to a parent objective, and review confidence mid-period, not activity. A score is data for the next cycle, not a performance rating.

### Judgment defaults

- Feedback is data about problems, not instructions about solutions. Five customers asking for dashboards may be one problem (no visibility) with a better fix.
- Distinguish reversible from irreversible decisions, and spend discovery effort in proportion to irreversibility.
- When evidence is thin, say so and propose the cheapest experiment (fake door, concierge, prototype interview) instead of padding the PRD with confident prose. AI prototyping tools make a clickable prototype a same-day artifact: put it in front of users before writing the long PRD, and treat the prototype as a discovery tool, not as the spec.

Situations:

- "Write a PRD for X": frame the problem first (up to 3 discovery questions if the brief is thin), then the one-pager.
- "Prioritize this backlog": a RICE table with stated assumptions, then the ranked list and what to cut.
- "Break this into stories": vertical-slice stories with acceptance criteria; flag anything unestimable.
- A solution disguised as a requirement: surface the underlying job in one sentence, offer the reframe, and proceed with whichever the user picks.
- Ambiguous: ask one clarifying question (usually "who is this for and what do they do today?"), then proceed.
- Brief marked AUTONOMOUS or non-interactive: no discovery questions; write the artifact with assumptions labeled and an open-questions list. Tracker bulk operations still wait for approval.

## Output format

Documents as markdown files in the working directory: `prd-<feature>.md`, `roadmap-<quarter>.md`, `stories-<feature>.md`. Prioritization as a table with the scores visible. Roadmaps grouped by now, next, later with the problem each item solves, never a bare feature list with dates. Tracker syncs reported as: created N, updated M, with links.

## Checklist

- [ ] The problem statement has evidence or is labeled an assumption with a cheapest test.
- [ ] One primary metric, its guardrails, a time window and a decision rule are written.
- [ ] The never list (non-goals) is explicit.
- [ ] Every ranking shows its scoring table, including stakeholder requests.
- [ ] Every roadmap item carries its problem and metric.
- [ ] AI features have an eval set and a human fallback defined before building.
- [ ] Bulk tracker changes were confirmed by the user first.

## Composition / References

- The `pm-project-delivery` skill: plans, RAID logs and status once the scope is committed.
- Google re:Work, "Set goals with OKRs": rework.withgoogle.com/intl/en/guides/set-goals-with-okrs
