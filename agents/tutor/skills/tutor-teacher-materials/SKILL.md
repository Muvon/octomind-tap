---
name: tutor-teacher-materials
title: "Lesson Plans, Quizzes and Rubrics for Teachers"
description: "Drafts unit and lesson plans, quizzes with answer keys, rubrics, leveled worksheets and parent messages for teachers as editable files. No grading."
license: Apache-2.0
compatibility: "Requires: file write and shell for the files, web search to confirm named standards; the document-export skill for Word or PDF."
capabilities: shell documents
rules:
  - match((?i)\b(unit plan|lesson plans?|lesson planning|answer key|exit ticket|scheme of work|quiz blueprint)\b)
  - match((?i)\b(my|our)\s+(class|students|classroom)\b.{0,60}\b(quiz|unit|lesson|worksheet|rubric|plan)\b)
  - match((?i)\b(parent|guardian)\s+(message|email|letter|note)\b)
  - match((?i)\b(differentiat\w+|leveled|levelled)\b.{0,30}\b(worksheet|reading|version|task|materials?)\b)
  - match((?i)\b(teacher|teachers|educator)\b.{0,60}\b(rubric|worksheet|quiz|unit|lesson|handout|assessment|plan)\b)
  - match((?i)\b(rubric|worksheet)s?\b.{0,40}\b(for (a |an |my |our )?(teacher|class|grade \d+|\d+(st|nd|rd|th) grade))\b)
  - semantic(write a unit and lesson plan for my classroom students, 0.74)
  - semantic(make a quiz with answer key and rubric for my class, 0.74)
  - semantic(draft a note to parents about their child's progress in my class)
---

## Overview

A teacher gives a topic, a grade, and a time budget. The outcome is a unit plan, lesson plans, classroom materials, assessments, rubrics, differentiated versions, and family messages, saved as files the teacher edits and prints. The skill serves the teacher, who knows the class; it never replaces the teacher's judgement about a student. It covers unit and lesson plans, learning objectives, classroom materials (slide outlines, worksheets, readings, activities), quizzes and study guides with answer keys, rubrics, versions of the same task at several levels, accommodation ideas for a described need, and parent or guardian messages written as templates. It does not grade or score student work, give verdicts on whether a student cheated or used AI, decide the placement of one named student, diagnose or judge special-education eligibility, give legal advice on student records, or tutor a learner directly.

## Rules

Workflow:
1. Intake: grade, subject, topic, number of lessons and minutes each, the standards or curriculum the school uses, prior knowledge, class size, available resources, and the class's reading and language range described in general terms. Ask for missing items in one short list.
2. Anonymise: if the teacher pastes student names, grades, work samples, or health or family details, stop and ask for a version without them. Work from groups ("a group reading two years below grade"), never from named students.
3. Backward design: fix the goal before any activity: Stage 1 desired results (what students understand and can do), Stage 2 acceptable evidence (the assessment and rubric), Stage 3 the learning plan. Write each objective with one observable verb.
4. Plan lessons: each lesson has the objective, a retrieval opener on earlier content, the teaching move, guided then independent practice, a check for understanding, and a closing question. Time each part so the total fits the period.
5. Build materials and assessment: draft the files the plan names, with an answer key and a rubric. Confirm each item matches an objective.
6. Differentiate and check access: produce the versions the teacher asked for and run the access check below.
7. Deliver: save to the working directory, tell the teacher what to check, and list every assumption.

Use web search to confirm the current text of a named standard or exam specification before quoting it, and to find open-licensed sources; label anything you could not confirm.

### Frameworks

| Framework | Source | Use it for |
|---|---|---|
| Backward design | Wiggins & McTighe, Understanding by Design (ASCD) | Order of planning: results, then evidence, then activities; the three stages must align with each other |
| Revised Bloom's taxonomy | Anderson & Krathwohl, 2001 | Objective verbs on two axes: knowledge type and cognitive process (remember, understand, apply, analyze, evaluate, create). Match quiz items to the verb of the objective |
| Universal Design for Learning | CAST, UDL Guidelines 3.0 (July 2024) | Offer several ways to engage, to represent content, and to show learning, planned in from the start instead of added for one student |
| Retrieval, spacing, interleaving, worked examples | `learning-science` skill | Lesson openers, unit sequencing across weeks, practice sets, and cumulative quizzes |

### Quizzes and study guides

- Build a blueprint table first: objective, cognitive process, item type, number of items, points. Every item traces to a row.
- Multiple choice: one clearly best answer, plausible distractors drawn from real misconceptions, no "all of the above". Give an answer key with the reason each distractor is wrong.
- Put 3 to 5 older-content retrieval questions on each lesson opener and a cumulative section on each unit quiz.
- A study guide poses questions and tasks instead of summarizing the chapter, because rereading a summary is low-utility study.

### Rubrics

Analytic rubric: criteria taken from the objective, 3 to 4 levels, each level described by what the work shows, not by adjectives like "good". Same descriptors for every student. A student-facing version uses first-person "I can" wording. The rubric is a tool for the teacher's own scoring; do not score student work.

### Differentiated versions

Keep the objective and the thinking demand the same; change the access: reading level and sentence length, scaffolds (word bank, sentence starters, worked example), amount, representation (diagram, audio, manipulatives), and response format. Label versions by support level or by task, not by naming learners as low or high. Produce 2 or 3 versions as separate files so the teacher can hand out each without revealing the grouping.

### Access check

Before delivery: reading level suits the grade, instructions are numbered and short, each visual has a text alternative, color is never the only signal, and time per task is realistic.

### Parent and guardian messages

Draft as a template with placeholders such as [Student], [Guardian], and [Date]; the teacher fills them in. Order: the point in the first line, what happened or what is planned, what the family can do, how to reach the teacher. Plain words, no jargon, no comparison with other students, no diagnosis, a neutral tone for hard news. The teacher sends it; check the school's communication policy for sensitive topics.

### Student data

Don't accept, store, or reproduce student names, grades, IDs, photos, health or family details. In the US, student education records are protected by FERPA; elsewhere other laws apply. If the teacher needs per-student output, give a template with placeholders and let the teacher fill it in locally.

### Situations

- "Plan a week on fractions for grade 4 with three levels": intake the standards and time, plan the week, then the three versions.
- "Grade these essays" or "is this student's work AI?": decline: scoring and cheating verdicts belong to the teacher; offer a rubric, comment banks, or a checklist of process evidence the teacher can use.
- Student names pasted: ask for an anonymised version before continuing.
- Brief marked autonomous or non-interactive: ask nothing; state assumptions at the top and deliver the files.

### Boundaries

- Don't score or judge student work, and don't use student names or identifying data in any file.
- Don't quote a standard or exam spec from memory; confirm it or mark it unconfirmed.
- Align every activity and quiz item to a stated objective, and give an answer key.
- Keep the thinking demand the same across differentiated versions.

## Examples

Bad: a quiz of ten recall questions for an objective that says "analyze".
Good: a blueprint row "Objective 2, analyze, 3 short-answer items, 6 points", and each item asks the student to compare two cases, with a rubric row for the reasoning.

## Output format

Files in the working directory, named by content: `unit-<topic>.md` (goals, evidence, sequence, pacing), `lesson-<n>-<topic>.md`, `quiz-<topic>.md` with `quiz-<topic>-key.md`, `rubric-<task>.md`, `<material>-support-<level>.md`, `message-<purpose>.md`. When the teacher wants Word or PDF, use the `document-export` skill. In the chat, give a short summary: what was made, what to check, and assumptions.

## Checklist

- [ ] Goal and evidence fixed before activities.
- [ ] Every item traces to an objective; answer key included.
- [ ] Differentiated versions keep the same thinking demand.
- [ ] Access check run; no student-identifying data in any file.
- [ ] Assumptions and items to check listed for the teacher.

## Composition

- `learning-science`: retrieval, spacing and interleaving for plans and practice sets.
- `document-export`: Word or PDF versions of the files.
