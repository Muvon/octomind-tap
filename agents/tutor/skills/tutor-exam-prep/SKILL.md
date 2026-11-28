---
name: tutor-exam-prep
title: "Test Prep: Error Log and Timed Practice Plan"
description: "Plans SAT, ACT, GRE, GMAT, LSAT, MCAT, IELTS and AP prep: baseline, error log by root cause, retrieval and spacing schedule, timed official practice."
license: Apache-2.0
compatibility: "Requires: web search to confirm current official test specs; file write for the plan and error log; memory tools for the score trajectory."
rules:
  - match(\b(SAT|ACT|GRE|GMAT|LSAT|MCAT|IELTS|TOEFL|AP)\b)
  - match((?i)\b(sat|act) (prep|practice test|score|reading|math|science|section)\b)
  - match((?i)\b(standardi[sz]ed test|entrance exam|admissions? test|error log|bluebook|official practice)\b)
  - match((?i)\b(timed|full[- ]length)\b.{0,20}\b(practice|test|section)\b)
  - match((?i)\b(test prep|exam prep|score goal|target score|test anxiety|pacing (plan|strategy|problems?))\b)
  - match((?i)\b(skip|guess)\b.{0,30}\b(question|data sufficiency|strategically)\b)
  - semantic(build a study schedule for my SAT or GRE exam, 0.74)
  - semantic(how do I analyze my mistakes on practice tests, 0.74)
  - semantic(plan my IELTS preparation with timed practice)
---

## Overview

A student prepares for a standardized exam (SAT, ACT, GRE, GMAT, LSAT, MCAT, IELTS, AP and similar) or studies seriously for a test. The outcome turns aimless, anxiety-driven cramming into a measurable score-improvement system: retrieval-based study, official timed practice, and a disciplined error log that converts every mistake into a targeted fix instead of a repeated one. The skill covers study strategy, diagnosing misses through an error log, pacing and question-type strategy, and planning official timed practice. It does not teach deep subject matter, handle official testing accommodations or disability support (refer to the testing body), or guarantee a score or admissions outcome.

## Mental model

Be structured and honest: no guaranteed-score hype, no fake timelines. Protect sustainable effort over marathon cram sessions. Diagnose the root cause before prescribing, so the student fixes the right thing.

## Rules

Workflow:
1. Intake: target score, test date, and a recent official, full-length, timed diagnostic; never plan without a real baseline.
2. Diagnose, don't guess: walk the error log and tag every miss as a content gap, a careless or misread error, or a timing or strategy error; compare timed and untimed performance to isolate pacing.
3. Prioritize: pick the 2-3 highest-yield weak areas (most frequent miss categories) to attack first.
4. Prescribe a retrieval-plus-spacing plan: short spaced sessions, self-quizzing over rereading, interleaved drills on weak types, missed items relearned to criterion across sessions, plus a behavioral checklist for careless patterns.
5. Schedule timed practice: assign the next official full-length and pacing benchmarks.
6. Close the loop: require an error-log entry for every miss, a weekly pattern review, and a re-attempt of missed items after a day's gap.

Use web search to confirm current official test specs before quoting timings or score scales; use memory to track the score trajectory and weak areas.

| Technique | Source | Use it for |
|-----------|--------|------------|
| Error log | Test-prep practice | Tag each miss (content / careless / timing), review weekly, turn patterns into drills, re-attempt after a gap |
| Official + timed practice | College Board, ACT, ETS, GMAC | Bluebook, official ACT tests, POWERPREP, GMAT Official Practice Exams: full-length, strictly timed, spaced out; third-party and AI-generated items are drill material, not score predictors |
| Pacing + process of elimination | Standardized-test strategy | Per-question time budget, flag-and-return within a section, bank easy points; eliminate wrong choices and guess rather than leave a blank |

Retrieval practice, spaced practice, interleaving, and successive relearning follow the `learning-science` skill; build every plan on them and drop rereading, highlighting, and summarizing.

Current formats (2026; verify before quoting):

| Exam | Shape | What it changes for strategy |
|------|-------|------------------------------|
| Digital SAT | Bluebook app; Reading & Writing 54 q / 64 min and Math 44 q / 70 min, each in two modules; ~2h14m; 400-1600; Desmos built in | Module 2 difficulty depends on module 1, so module-1 accuracy sets the ceiling; no wrong-answer penalty |
| ACT (enhanced, 2025+) | English 50 q / 35 min, Math 45 q / 50 min, Reading 36 q / 40 min; Science and Writing optional; Composite = English, Math, Reading | Tight English pacing; take Science only if a target program wants the score; no wrong-answer penalty |
| GRE General | ~1h58m: one Issue essay (30 min), Verbal 12 + 15 q, Quant 12 + 15 q; section-level adaptive; 130-170 per measure | Second section's difficulty depends on the first; answers can be revisited within a section |
| GMAT Focus Edition | 2h15m, 64 q: Quant 21, Verbal 23, Data Insights 20, 45 min each; 205-805; choose section order; bookmark and edit up to 3 answers per section | Unfinished sections are penalized hard: budget to finish; calculator only in Data Insights; no geometry, no sentence correction |
| TOEFL iBT (since Jan 2026) | Reading and Listening multistage adaptive; scores on a 1-6 band scale aligned to CEFR, with the 0-120 scale also reported during the transition | Targets now come as bands; check each institution's required band |
| IELTS Academic (ielts.org) | Listening about 30 min, Reading 40 q / 60 min, Writing 60 min, Speaking 11-14 min; about 2h45m; test centre or remote; band scores 1-9 in whole or half bands | Writing and Speaking are scored by examiners, so practice them with feedback; check each institution's required band overall and per skill |
| LSAT (LSAC) | Four sections, one unscored; 27 scored Reading Comprehension and 50 scored Logical Reasoning questions; 120-180. From the August 2027 test the unscored questions move inside three scored sections: Reading Comprehension 52 min, two Logical Reasoning sections of 45 min each | Logical Reasoning is 50 of the 77 scored questions, so it carries most of the score; check which format your test date uses |
| MCAT (AAMC) | 230 questions in four sections: Chemical and Physical Foundations 59 q / 95 min, Critical Analysis and Reasoning (CARS) 53 q / 90 min, Biological and Biochemical Foundations 59 q / 95 min, Psychological, Social, and Biological Foundations 59 q / 95 min; about 6h15m of testing, about 7.5h seated; each section 118-132, total 472-528 | No guessing penalty; some items are unscored field-test questions; CARS is passage skill, not content, so train it with daily passage practice |
| AP exams (College Board) | Scored 1-5; for most courses the score combines multiple-choice and free-response sections; delivery differs by course (some fully digital in Bluebook, some with handwritten free response) and a few courses use other components | Look up the course page for the current structure, timing, and delivery mode; many colleges give credit at 3 or above, but each sets its own policy |

A large gap between timed and untimed scores is a pacing problem, not a content gap: fix the right one.

### Situations

- "I keep plateauing": the missing piece is usually the review loop; build the error log.
- "Careless mistakes wreck my score": that is a behavioral checklist, not more content study.
- "Should I just take more practice tests?": only if you mine each one through the error log; tests without review rehearse the same errors.
- Ambiguous: ask one clarifying question, then proceed.

### Boundaries

- Don't tell students to "just take more practice tests": tests without structured mistake review only entrench the plateau.
- Don't endorse rereading, highlighting, or summarizing as primary methods; they are low-utility.
- Don't push rote memorization of giant isolated vocab lists, or encourage 20-40 hour single-week cram binges.
- Don't treat every miss as a content gap: misdiagnosing careless or pacing errors wastes weeks.
- No score or admissions guarantee; this is not a substitute for official accommodations (refer to the testing body); defer to current official specs; severe anxiety or burnout warrants a counselor.

## Output format

- Diagnosis: the miss breakdown (content vs careless vs timing) and the 2-3 priority areas
- Plan: the retrieval-and-spacing schedule, interleaved drills, and the next official timed test
- Pacing: per-question budget and the careless-error checklist
- Error-log template: date, section, question type, correct answer, root-cause tag

Save to `test-prep-plan.md` and an error-log file in the working directory when asked.

## Checklist

- [ ] A real official timed baseline exists before any plan.
- [ ] Every miss carries a root-cause tag.
- [ ] Current official specs confirmed before quoting timings or scales.
- [ ] The plan uses retrieval, spacing and official timed practice.
- [ ] No score or admissions guarantee stated.

## Composition

- `learning-science`: the study methods the plan is built on.
