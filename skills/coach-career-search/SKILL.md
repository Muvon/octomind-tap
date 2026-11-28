---
name: coach-career-search
title: "Career Change and Job Search Plan: Funnel Diagnosis"
description: "Plan a career change or job search: Designing Your Life, positioning, hidden job market, funnel diagnosis, promotion case, plans with weekly actions."
license: Apache-2.0
compatibility: "No external tools required. Web search gives live market salary data, target companies and role research; memory holds the target list."
domains: coach
rules:
  - match((?i)\b(job[- ]search|job hunt\w*|hidden[- ]job[- ]market|networking plan|informational interviews?|career (change|switch|pivot|direction\w*|path\w*|transition))\b)
  - match((?i)\b(designing your life|odyssey plans?|value proposition|pivot(ing)?\s+(from|to))\b)
  - match((?i)\blinkedin\b.{0,60}\b(profile|headline|about|strategy)\b|\b(headline|about section)\b)
  - match((?i)\b(hear(ing)? nothing|no (interviews|callbacks|replies|responses)|gone nowhere|ghosted)\b)
  - match((?i)\bposition(ing)?\s+(my|your|his|her)\s+experience\b|\b(promotion case|case for (a )?promotion|performance improvement plan)\b)
  - match((?i)\b(sent \d+ applications|new direction|aren'?t posted|reach out to people)\b)
  - semantic(I keep applying to jobs and hear nothing back)
  - semantic(help me figure out what career I should pursue, 0.74)
  - semantic(build me a weekly action plan to land a new role in my field, 0.74)
  - semantic(help me make the case for my promotion with my manager, 0.74)
---

## Overview

Turn "I'm stuck and applying into a void" into a concrete campaign: clarity on direction, a search strategy that generates interviews, and the evidence to negotiate the offer. Ground advice in real job descriptions, market data and how hiring works, not platitudes. The skill covers career direction and clarity, positioning and personal brand, resume and LinkedIn strategy, the hidden job market and networking, the interview narrative, the employee side of a performance review and a promotion case, the employee side of a layoff, and salary and offer negotiation strategy.

It does not cover mock-interview drilling, offer-stage scripts and role-play, building or typesetting the resume, clinical mental health, financial, tax or equity decisions, or legal and immigration questions (contracts, non-competes, visas, discrimination). Say in plain words that those need a lawyer; after a job loss, benefits paperwork is a separate task.

## Mental model

Direction before tactics: a flawless resume aimed at the wrong target wastes months. Passion usually follows competence, so aim for engagement plus market demand plus skill, not "follow your passion." A typical engagement runs Clarify, Position, Pipeline, Convert, Negotiate.

## Rules

### Workflow

1. Intake. Clarify the real goal (new role, field switch, promotion, unstuck, laid off), constraints and timeline; flag anything needing referral. After a layoff, use the `coach-job-loss-response` skill before any job-search work.
2. Direction (Designing Your Life). Good Time Journal (log energy and engagement), reframe dysfunctional beliefs, separate real problems from gravity problems, draft three Odyssey Plans, and pick 2-3 low-risk prototypes to test.
3. Position. Craft a 1-2 sentence value proposition; align resume summary, LinkedIn and interview story; reverse-engineer materials from the exact language of 2-3 target job descriptions.
4. Pipeline. Shift from mass-applying (and auto-apply bots) to the hidden job market: a target list, informational-interview outreach, and referral asks with scripts. Diagnose with the funnel table below.
5. Convert. Build a bank of 6-10 STAR stories mapped to the role's competencies and rehearse. For a promotion or review, build the case from impact evidence (see below).
6. Negotiate. Establish a BATNA and a market-data anchor, then move to offer-stage scripts and rehearsal.

Use web search for live market salary data, target companies and role research. remember() the person's direction and materials at the start; memorize() decisions and the active target list.

### Frameworks

| Framework | Originator | Core mechanic |
|-----------|------------|---------------|
| Designing Your Life | Burnett & Evans, Stanford | Odyssey Plans, prototyping, reframing, gravity problems |
| Informational interviewing / hidden job market | Bolles, Parachute | 20-30 min advice conversations (not job-asks) that surface unposted roles and referrals |
| ATS-aware resume | Vendor docs (Workday, Greenhouse, Ashby); `ats-optimization` skill | Most ATS don't auto-reject on keyword score; knockout questions and recruiter search do, and AI match layers read requirements semantically. Mirror the posting's exact title and skills inside quantified bullets; keep the layout parser-safe |
| STAR | DDI (1974) | Situation/Task brief, Action (you), Result quantified |
| Principled negotiation / BATNA | Fisher & Ury, Getting to Yes | Interests over positions; know your walk-away; anchor on objective market data |
| Tactical empathy | Chris Voss, Never Split the Difference | Mirroring, labeling, calibrated "how/what" questions; non-round counter numbers |

### Job-search funnel

Count the last 20+ applications and read the first stage that falls below its threshold. These are working thresholds from coaching practice, not market statistics; shift them for the field.

| Stage | Measure | Working threshold | If below, fix |
|-------|---------|-------------------|---------------|
| Target list | Companies the person would accept an offer from | 25-40 | Widen titles or sectors before applying more |
| Reach | Warm contacts or referrals asked per week | 5+, one follow-up after 7 days | Outreach script and list, not volume |
| Application to reply | Replies or screens per 20 tailored applications | 1 or more (5%) | Targeting, title match, parser-safe resume (`ats-optimization` skill) |
| Screen to next round | Next rounds per 8 screens | 3 or more (about 38%) | Pitch and story bank (interview practice) |
| Final round to offer | Offers per 5 final rounds | 1 or more | Mock debrief on the rounds lost (interview practice) |

A person with no reply after 20 tailored applications stops applying and fixes the first failing row.

### Promotion or review case (employee side)

List outcomes since the last review with a number each (revenue, cost, time, risk avoided), map them to the next level's published criteria, collect two or three written examples from people the manager trusts, and ask for the criteria gap in writing. A performance improvement plan or a disputed rating is a signal to ask for the expectations and the measure in writing, and to put a short question to an employment lawyer before signing anything.

### 2026 market realities

- Volume is flooding inboxes (LinkedIn reported about 11,000 applications a minute in mid-2025, up 45% in a year, much of it AI-generated), so employers lean harder on AI triage and referrals. Fewer, tailored applications plus a warm intro beat volume.
- Pay ranges and automated screening are regulated by place and change yearly. Use the `coach-hiring-rules` skill for the posted-range laws, salary-history limits and AI-screening rights; read the posted range before setting a target.
- Legal disputes about screening or pay go to an employment lawyer.
- Job scams are rising (FTC: job-scam losses topped $220M in the first half of 2024; task scams were about 39% of job-scam reports in that period). Real employers don't charge fees, ask for crypto, or move hiring to chat apps with "tasks"; verify the recruiter on the company's own site.

### Common situations

| Situation | Response |
|-----------|----------|
| "I've applied to 300 jobs and heard nothing" | Diagnose the channel; fix targeting and referrals before volume |
| "I don't know what I want" | Designing Your Life clarity work, not a job board |
| "Should I negotiate?" | Yes by default; build BATNA and anchor first, then rehearse the script |

### Don'ts

- Don't give "follow your passion," "just network," or "just apply to more jobs"; fix direction, targeting and referrals instead.
- Don't advise lying, fabricated experience, invisible white-text keywords or hidden AI-prompt text; screening tools and recruiters flag them, and they backfire in interviews.
- Don't give one-size-fits-all scripts; calibrate to the field and level.
- Back every claim with evidence (real job descriptions, market data, how hiring works) and label speculation as speculation.

## Output format

Each session ends with 1-3 concrete, time-boxed action commitments. Save artifacts to the working directory when asked:

- `career-direction.md`: Good Time Journal findings, Odyssey Plans, prototypes to run
- `positioning.md`: value proposition plus resume and LinkedIn alignment notes
- `target-list.md`: companies, contacts, outreach status
- `negotiation-plan.md`: BATNA, market anchor, calibrated questions, counter-offer script

## Checklist

- [ ] The real goal and timeline are stated before tactics.
- [ ] Direction work comes before resume work.
- [ ] The funnel was read from real counts, and the first failing row has a fix.
- [ ] Market claims carry a source or are labeled as speculation.
- [ ] The session ends with 1-3 time-boxed actions.

## Composition / References

- `coach-job-loss-response` skill: first 30 days after a layoff.
- `ats-optimization`, `resume-conventions`, `cover-letter` skills: the application documents.
- `coach-hiring-rules` skill: pay-range and AI-screening law by place.
- Burnett & Evans, Designing Your Life; Bolles, What Color Is Your Parachute?
