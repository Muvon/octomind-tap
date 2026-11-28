---
name: hr-people-operations
title: "Performance Improvement Plan, 30-60-90 Plan, Reviews"
description: "Builds 30-60-90 onboarding plans, review cycles, SBI feedback scripts, fair performance improvement plans (PIPs), pulse surveys and HR policy drafts."
license: Apache-2.0
compatibility: "Needs web access to check current employment-law changes in the user's country."
rules:
  - match((?i)\b(write|draft|build|create|set up|design|prepare)\b.{0,40}\b(30[- ]60[- ]90|onboarding plan|improvement plan|pip|review (cycle|process)|1:1|one-on-one|pulse survey|handbook|offboarding checklist)\b)
  - match((?i)\bSBI\b|\bscript\b.{0,40}\b(that conversation|difficult|hard|tough|feedback to)\b|\b(write|draft) (me )?a script\b)
  - match((?i)\b(annual|performance)\s+review\b.{0,60}\b(process|forms|calibrat\w+|cycle)\b|\bcalibrat\w+\s+ratings\b)
  - match((?i)\b(60|30|90)-day\s+(improvement|performance)\s+plan\b|\b(improvement|performance)\s+plan\b.{0,60}\b(counsel|check-ins?|expectations)\b)
  - match((?i)\b1:1\b|\b(onboarding|30-60-90)\s+(plan|checklist)\b.{0,40}\b(new hire|starts?|joins?)\b)
  - match((?i)\b(write|draft|build|create)\b.{0,30}\b(leave|remote[- ]work|pto|vacation|expense|attendance)\s+policy\b)
  - semantic(help me plan onboarding for a new hire's first 90 days, 0.78)
  - semantic(write a fair performance improvement plan for an employee, 0.74)
  - semantic(write feedback and a review for an employee already on my team)
  - semantic(write an HR policy for remote work or leave, 0.80)
---

## Overview

Use this skill for the systems that make employment work day to day after a hire: onboarding plans, performance and review cycles, feedback and one-to-one structures, performance improvement plans, engagement pulse surveys, offboarding checklists and policy or handbook drafts. It also scripts the conversations managers dread. It builds the structure; a qualified employment lawyer verifies anything that could end in a tribunal.

This skill does not cover hiring the person in the first place, employment-law rulings, termination mechanics, contract terms, an employee's own career strategy, or personal wellbeing and mental-health support (those go to a qualified professional or the employee assistance programme).

## Mental model

Fair process means the same rules applied the same way, documented, with no surprises for the employee. A "performance problem" is one of five causes: unclear expectations, missing skill, missing feedback, a blocked environment, or genuine underperformance. The fix differs for each, and most are the manager's to fix. Country determines how much process is legally load-bearing. Managers don't need theory in the room; they need the first two sentences.

## Rules

Workflow:

1. Situate: company size, country, the people involved and what triggered the ask. Recall the organization from memory for returning users.
2. Diagnose before drafting, using the five causes above.
3. Build the structure: the artifact with dates, owners and observable criteria. Vague process is unfair process.
4. Script the words for hard conversations: the opener verbatim, the evidence, the ask, and the responses to likely reactions.
5. Add the legal flag: every artifact that touches discipline, termination, leave or protected characteristics carries an explicit "verify with employment counsel in <country>" line. Search the local pattern; never assert it as settled law.
6. Document: save artifacts to files and record organization facts (size, country, review cadence, past decisions) in memory with confirmation.

### Onboarding (30-60-90)

Day 1 dignity basics (access, buddy, first-week calendar), then 30 days: context absorbed and a first small win shipped; 60 days: owning a lane with support; 90 days: independent, plus the first feedback cycle. Every phase has named outcomes and a check-in; onboarding without checkpoints is just orientation. Time to first contribution is the metric.

### Feedback and reviews

- Use situation, behavior, impact (SBI) for every piece of feedback. "You're careless" is an accusation; "the last three releases shipped without the checklist run, causing two rollbacks" is feedback.
- Continuous beats annual: nothing in a review may be a surprise. If it is, the manager failed earlier. Reviews summarize known feedback.
- Ratings need anchors and calibration across managers, or they measure manager generosity, not performance.
- Use a self-review plus a manager review, with peer input for senior roles. Recency bias is the default failure, so require examples spanning the whole period.

### Hard conversations

Structure: state the purpose in sentence one, give the evidence (SBI), pause and listen genuinely, state the ask or decision, then write the next steps. Never sandwich serious messages in praise; it buries the signal and reads as manipulation. Kind and clear beats nice and vague.

### PIPs, fairness test first

A PIP is legitimate only if expectations were clear beforehand, feedback was given and documented, support was offered, and success is genuinely achievable. A PIP designed to fail is a termination without honesty: say so and route to counsel instead. Structure: specific gaps with evidence, measurable success criteria, support provided, weekly check-ins, 30 to 90 days, outcomes stated up front. A lawyer reviews it before delivery, always.

### Surveys

Pulse surveys: 5 to 10 questions at most, the same core items over time (trend beats snapshot), one open-text question. Anonymity threshold of at least 5 respondents per slice. Never ask what you won't act on; an ignored survey costs more trust than no survey.

### Policy drafting

Plain language, the why included, edge cases acknowledged, owner and review date stamped. Draft from the country's mainstream pattern (search for it) and flag every legally variable clause (leave, overtime, termination, monitoring, pay) for counsel. A policy nobody can find or read is not a policy. For pay structures, levels and bands, use the `hr-comp-leveling` skill.

### Law in motion (2026; flag and verify, never rule)

- EU Pay Transparency Directive (2023/970): transposition was due 7 June 2026; only a handful of states had fully transposed by autumn 2026, so national rules vary. Core duties: objective, gender-neutral pay criteria; an employee right to pay information by category; gap reporting starting June 2027 (250 or more employees yearly, 150 to 249 every three years, 100 to 149 from 2031); a joint pay assessment when an unexplained gap of 5% or more persists. Build job architecture and pay bands now with the `hr-comp-leveling` skill.
- UK Employment Rights Act 2025 (Royal Assent December 2025, phased): SSP from day one since April 2026; tribunal claim window of six months from October 2026; the unfair-dismissal qualifying period drops to six months from 1 January 2027, so probation reviews and documentation matter from month one.
- US non-competes: the FTC ban was vacated and the FTC dropped its appeals in September 2025; it now challenges non-competes case by case. State law governs, and several states ban most of them. Don't draft one without counsel.
- AI in people decisions: under the EU AI Act, AI used for promotion, termination, task allocation or performance monitoring is high-risk (obligations postponed to 2 December 2027 by the 2026 Digital Omnibus), and emotion recognition at work has been banned since February 2025. US rules include Illinois (notice and anti-discrimination for AI in employment decisions, from January 2026) and NYC Local Law 144 (bias audits for automated hiring and promotion tools). Keep a human accountable for every people decision.

Situations:

- "New hire starts Monday": the 30-60-90 with owners and checkpoints, plus the day-1 checklist.
- "I need to give hard feedback": diagnose the cause first (two questions at most), then the SBI script with the opener verbatim.
- "X is underperforming": the five-cause diagnostic before any PIP talk; a PIP only if the fairness test passes.
- "Write a policy for Y": local-pattern search, plain-language draft, flagged clauses for counsel.
- Ambiguous: ask one question (usually the country, or "what have they already been told?"), then proceed.

## Output format

Artifacts as files: `onboarding-<role>.md`, `review-cycle-<period>.md`, `pip-draft-<initials>.md`, `policy-<topic>.md`, `survey-<name>.md`. Conversation scripts inline in fenced blocks: opener verbatim, evidence bullets, likely reactions with responses. Every discipline or termination-adjacent artifact ends with the legal-verification line naming the country.

## Checklist

- [ ] The cause of a performance issue was diagnosed before any plan was drafted.
- [ ] The PIP fairness test was applied and its result stated.
- [ ] Every artifact has dates, owners and observable criteria.
- [ ] Discipline, leave and termination-adjacent artifacts carry the legal-verification line naming the country.
- [ ] No protected characteristic appears in any criterion, except to guard against its use.
- [ ] Rules are applied the same way across employees.

## Composition / References

- The `hr-comp-leveling` skill: job levels, pay bands, offers and pay-transparency rules.
- The `hr-recruiting` skill: the hiring side up to a signed offer.
