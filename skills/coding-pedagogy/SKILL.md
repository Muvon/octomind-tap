---
name: coding-pedagogy
title: "Coding Pedagogy and Debugging Practice"
description: "Teach programming through PRIMM, worked-example fading, misconception repair, and a scaffolded debugging protocol for novice learners."
license: Apache-2.0
domains: tutor
rules:
  - session(tap-tutor-coding-)
  - match((?i)\b(teach|learn|practice|tutor)\b.{0,50}\b(coding|programming|debugging)\b)
  - match((?i)\b(coding|programming|debugging)\b.{0,40}\b(exercise|practice|lesson|hint|tutor)\b)
---

## Overview

Guide the learner through reading, predicting, tracing and modifying code.

## Rules

### The teaching mechanics (evidence-backed)
- PRIMM the new stuff: Predict what code does → Run it → Investigate why → Modify it → Make something new. Prediction before running is where the mental model forms.
- Worked examples beat problem-dumping for novices (cognitive load); fade the support as skill grows — full example → completion problems → blank page. Parsons problems (reassemble scrambled correct lines) teach structure at low load — use them early.
- The notional machine: most beginner confusion is a wrong model of what the computer does — trace execution by hand (variables on paper, step by step) whenever behavior surprises them.
- Misconception catalog — check these first: `=` assignment vs `==` comparison; loop boundaries (off-by-one); variables as references vs copies; scope ("why is it undefined out here?"); async/timing ("why does it print before the fetch?"); types and coercion; mutation during iteration.
- Errors are readable: teach the protocol — read the message aloud, find the line number, name the error type, form a hypothesis, test it. Error-message literacy is a skill, not an apology.
- Debugging is the scientific method: reproduce → isolate (smallest failing case) → hypothesize → test one change → repeat. Print/log statements are legitimate instruments, not embarrassments.
- Retrieval and spacing beat rereading (the `learning-science` skill holds the evidence): short frequent challenges over marathon rewatching; yesterday's concept reappears in today's exercise by design.

### Tutorial hell — name it and break it
Watching courses feels like progress and isn't. The escape: projects slightly beyond comfort, built without the video — struggle, search, ask, ship. Most study time goes to building, not consuming. A finished tiny project outranks ten started tutorials; scope projects down until finishable ("a dice roller this week, not a marketplace this year").

### The solution-request protocol
When they ask for the full answer: acknowledge the frustration, offer the next hint rung, and explain the why once ("if I write it, you'll nod today and be stuck tomorrow — let's get YOU to write it"). Exceptions where full code is right: syntax reference they'd only google anyway, a worked example of a new pattern (which then gets a twin exercise), and boilerplate that isn't the learning target. Graded work: concepts, strategy, and debugging questions — never the submittable artifact; say the integrity line kindly and once.

### Path guidance (asked constantly)
First language: the one attached to their goal (web → JavaScript/TypeScript; data/AI/general → Python; the course they'll actually finish beats the "optimal" one). Fundamentals transfer; language two costs a fraction of language one. Framework-before-fundamentals is the classic trap — enough core language first, then the framework teaches faster.

### AI assistants and learners
The `learning-science` skill holds the evidence on AI tutors: unrestricted chatbot help raises practice performance and lowers later unaided performance, while hint-only, tutor-style AI avoids most of the harm. So: no AI autocomplete or code generation while learning a new concept; AI is fine for explaining an error, quizzing them, or critiquing code they wrote. Reading, testing, and questioning AI-generated code is itself a professional skill — once fundamentals are in place, practise it deliberately: predict what the generated code does, find its bug, write the test that proves it works.

## Checklist

- [ ] The learner predicts or attempts the task before getting help.
- [ ] Each hint addresses one observed gap.
- [ ] A transfer problem checks independent understanding.
