---
name: hr-recruiting
title: "Structured Interview Kits, Scorecards, Job Descriptions"
description: "Takes a role from scorecard to signed offer: job description, sourcing plan, resume screen, structured interview kit and candidate messages."
license: Apache-2.0
compatibility: "Needs web access for pay-transparency rules and candidates' public work. Email drafting uses the connected email account; nothing sends without approval."
capabilities: messaging-email
domains: hr
rules:
  - match((?i)\b(candidate\s+communications?|offer\s+(email|letter|call))\b)
  - match((?i)\brole scorecard\b|\bscorecard\b.{0,30}\bjob description\b|\bjob description\b.{0,60}\b(attract|inflat\w+)\b|\bintake call\b)
  - match((?i)\b(interview\s+(loop|kit)|scoring\s+(rubric|guide)|anchored\s+scoring|asking consistent)\b)
  - match((?i)\bboolean\b|\bsourcing\s+(plan|strings?)\b|\bsearch strings?\b)
  - match((?i)\b(resumes?|cvs?)\b.{0,60}\b(against|screen|phone screen|shortlist)\b|\bscreen\b.{0,20}\b(resumes?|cvs?|candidates?|applicants?)\b)
  - match((?i)\b(debrief|hiring[- ](process\s+)?(metrics|funnel))\b|\boffer acceptance\b|\btime-to-fill\b)
  - match((?i)\b(hiring\s+(a|an)\b.{0,40}\b(who|with)|opening for|for (our|the) .{0,30}\bopening\b)\b)
  - semantic(write a job description and hiring scorecard for this role)
  - semantic(build an interview kit with structured questions for candidates, 0.74)
  - semantic(screen these resumes and shortlist candidates for the role, 0.74)
  - semantic(write sourcing outreach and a rejection note for job candidates, 0.70)
---

## Overview

Use this skill when a user is hiring. It builds the scorecard, writes a job description that attracts rather than filters, plans sourcing, screens resumes against the scorecard, designs a structured interview loop with anchored rubrics, and drafts every candidate message, so each person who does not get the job still leaves with a good impression. Hiring is judged against defined evidence, not gut feel: unstructured interviews predict little, and structure is the whole craft.

This skill does not cover the candidate's side of the table (resume and interview preparation, salary negotiation coaching), post-hire onboarding and performance, or employment-law rulings. A qualified employment lawyer answers those; this skill flags them.

## Mental model

The scorecard is the contract for the whole process: outcomes, competencies and the evidence source for each. Every later artifact traces back to it. Requirements, screens and rubrics all measure evidence of those outcomes, never proxies such as pedigree, name or gaps.

## Rules

Workflow:

1. Intake, before any job description: what will this person have accomplished in 12 months, what evidence would show they can, what is the level and range, who decides, and what is the real must-have list (cap at 5 or 6; everything else is trainable or negotiable).
2. Scorecard: outcomes, competencies and the evidence source for each (which interview, which work sample).
3. Job description, from the scorecard. Post-ready, honest about the hard parts, pay range included (legally required in many places). Set range and level with the `hr-comp-leveling` skill: a band from a sourced benchmark, an offer inside the band, an internal-equity check.
4. Source: a channel plan (inbound post, outbound search, referrals, communities), boolean strings for the outbound layer, a search of each target's public work for the personalization line, and personalized outreach drafts. The user approves every send first.
5. Screen: score resumes against the scorecard only, on evidence of the outcomes. Output per candidate: advance or decline, plus the evidence line that decided it. Flag maybes for human judgment instead of force-ranking noise.
6. Interview kit: per loop stage, what it tests (from the scorecard), the questions, the anchored rubric (what 1, 3 and 5 look like in observable behavior) and interviewer instructions. Ask the same questions of every candidate in a stage; comparison requires constants.
7. Close: a debrief format (independent scores before discussion, evidence before opinions), an offer draft, and warm, specific rejections for everyone else. Record the company's patterns (level ladders, tone, recurring roles) in memory for next time.

### Job description craft

- Structure: what you'll do (outcomes, not duties), what you'll bring (5 or 6 requirements at most), what you'll get (range, benefits, working mode), how the process runs (stages and timeline).
- Requirement inflation kills pipelines. Every inessential must-have filters out qualified people, and degree requirements the work does not need are the most common offender: state the skill, not the credential. Don't cite the "women apply only at 100% of requirements" statistic; it traces to an unpublished HP anecdote. Label nice-to-haves as such or delete them.
- Pay transparency: a growing set of US states and DC, including CA, CO, WA and NY, require a good-faith range in postings (the dated list with thresholds is in the `hr-comp-leveling` skill; it includes Maine and Virginia from July 2026 and Connecticut from October 2026, with Delaware in 2027). Many places ban asking for pay history. The EU Pay Transparency Directive requires the starting range before the interview, gender-neutral job titles and no pay-history questions; national rules vary while transposition, due June 2026, catches up. Check the jurisdiction with a search and post the range.
- Cut the culture clichés (fast-paced, rockstar, family): they signal nothing and repel some. Say the true specific thing instead ("you'll be the second designer; ambiguity is daily").

### Screening discipline

- Score against scorecard evidence, not proxies. Brand-name employers, degree pedigree and unexplained-gap suspicion are noise. Gaps are not signals; nobody explains a gap in a resume screen.
- Never infer or use protected characteristics (age, gender, ethnicity, family status, disability, and proxies such as graduation year or name). If the user asks for a filter that touches one, decline it plainly and offer the lawful evidence-based alternative.
- Best predictors, per current meta-analytic estimates (Sackett et al. 2022): structured interviews (about .42) and job-knowledge tests (about .40), then work samples (about .33) and cognitive ability (about .31). Unstructured interviews and resume proxies predict much less. Recommend the smallest realistic work sample (2 hours or less, paid if substantial) for the top competency.

### AI in hiring (2026; flag, verify, never rule)

- Your own screens are decision support: a human makes and owns every advance or decline. Where automated tools substantially assist hiring decisions, rules may apply: NYC Local Law 144 (independent bias audit within the past year, public summary, candidate notice 10 business days ahead), Illinois (AI notice and anti-discrimination, from January 2026), California's FEHA rules on automated-decision systems (from October 2025), and the EU AI Act, where recruitment and screening AI is high-risk (obligations from 2 December 2027) and emotion recognition of candidates is already banned. Flag these when the user's tooling or location makes them relevant.
- Candidate-side AI: set and state a policy for AI use in applications and work samples. For remote hires, verify identity at a live stage; proxy and deepfake interviews are a real fraud pattern.

### Structured interviews

- Prefer behavioral past-evidence questions ("walk me through a time you actually...") over hypotheticals, with follow-up probes for situation, action, result and their specific role.
- Write anchored rubrics per question before the loop starts. "Good communicator" is not an anchor; "explained a technical decision so a non-engineer in the room could restate it" is.
- Collect independent written scores before the debrief discussion; group talk before scores manufactures consensus.

### Candidate experience

- Every applicant gets an answer; every post-interview rejection gets a human-sounding, specific-but-safe note within a week. Ghosting is brand damage compounding at scale.
- Outreach is personalized to the person's actual work (one specific line at minimum), states the role, level, range and why them, in 80 to 120 words. No "rockstar ninja opportunity" spam.

### Metrics that matter

Pipeline pass-through by stage, time in stage (not just time to hire), offer-accept rate and source of hire. A funnel that loses everyone at one stage is a broken stage, not a talent shortage.

Situations:

- "We're hiring a <role>": the intake questions (the 12-month outcomes question first), then scorecard and job description in one pass.
- "Screen these resumes": a scorecard check (build it first if missing), then the verdict table.
- "Design the interview loop": stages mapped to scorecard competencies, a kit per stage.
- A request to filter on age, school tier, gap history or similar: decline the proxy, offer the evidence-based alternative, continue.
- Ambiguous: ask one question (usually the 12-month outcomes), then proceed.

## Output format

Artifacts as files: `scorecard-<role>.md`, `jd-<role>.md`, `interview-kit-<role>.md`, `sourcing-<role>.md`. Screens as a table: candidate, verdict, deciding evidence, flags. Outreach, offer and rejection drafts in fenced blocks headed by recipient and channel, batched for approval.

## Checklist

- [ ] The scorecard exists and every artifact traces to it.
- [ ] Must-have requirements are capped at six; the rest are labeled nice-to-have.
- [ ] The posting jurisdiction was checked and the pay range is included where required.
- [ ] No protected characteristic or proxy appears in any screen, string or rubric.
- [ ] Rubrics are anchored in observable behavior and written before the loop.
- [ ] Candidate-facing text contains no invented pay, titles or process commitments.
- [ ] Nothing was sent without approval of the exact draft.
- [ ] Employment-law questions (contracts, visas, terminations, AI-tool compliance) were flagged for a qualified employment lawyer.

## Composition / References

- The `hr-comp-leveling` skill: levels, bands, offer math and the pay-transparency list.
- The `hr-people-operations` skill: onboarding and everything after the hire.
