---
name: learning-science
title: "Learning Science: Make Studying Actually Stick"
description: "The small set of evidence-based study techniques that actually work — retrieval practice, spacing, interleaving, the Feynman technique, and worked examples — and the popular habits (rereading, highlighting, cramming, learning styles) that only feel productive. Activate when helping someone study, memorize, prepare for a test, or learn a skill, or when they ask how to learn something faster."
license: Apache-2.0
compatibility: "Any Octomind session. No external tools required; pairs well with an SRS app (Anki) for spaced repetition."
domains: tutor
rules:
  - session(tutor)
  - content(study) content(remember)
  - content(memorize)
  - content(flashcards)
  - content(revision)
---

## Overview

This skill encodes the techniques that cognitive science shows actually make learning stick and transfer, and names the popular study habits that only produce an illusion of competence. Activate it whenever you are helping someone study, memorize, prepare for a test, or learn a skill — and especially when they reach for rereading, highlighting, or cramming. The point is to replace comfortable-but-useless habits with effortful methods that work.

## Mental model

Performance is not learning. Fluent, comfortable study (rereading a chapter, watching a solution) raises in-the-moment performance and feels productive, but it builds little durable memory. The methods that work feel harder and slower because effortful retrieval is the mechanism — Bjork calls these "desirable difficulties." So the governing rule is counterintuitive: if studying feels easy and smooth, it is probably not working; if it feels effortful and a little error-prone, it probably is. Learners systematically mispredict this, which is why they default to the weak methods.

## Rules

### Lead with retrieval, not review

- Make the learner produce the answer from memory before showing the material again: free-recall brain-dump, self-quiz, flashcard answered before flipping, or explain-it-out-loud.
- Recognition ("yeah, I know this") routinely overstates real recall — require production from a blank page.
- The effort, and even failed attempts followed by feedback, is where learning happens. In the classic study, learners who kept retrieving recalled ~80% a week later vs ~36% for items they stopped testing.

### Space it out

- Break study into multiple sessions across days instead of massing it into one block; spacing roughly doubles long-term retention versus cramming.
- Rule of thumb for the gap: about 10-20% of how long you need to remember it — to hold for a month, review every few days; for a year, review about monthly.
- For fact-heavy material, use a spaced-repetition system (Anki / Leitner): review each item just as it's about to be forgotten.

### Interleave confusable material

- Mix related problem types or topics within a session (ABCABC) instead of blocking one type at a time (AAABBBCCC).
- Interleaving forces the learner to first decide which method applies — the actual exam skill that blocked practice hides.
- It feels harder and lowers in-session accuracy, but roughly doubles delayed-test scores for confusable material. Warn the learner that the difficulty is the point.

### Match guidance to expertise

- For a true novice on a new skill, a fully worked example beats unguided problem-solving — it avoids cognitive overload.
- As competence grows, fade the worked steps (completion problems → backward fading → independent solving). Continuing to spoon-feed examples to someone ready to practice alone stops helping.

### Use the Feynman technique as a gap-finder

- Have the learner explain the concept in plain language, as if teaching a novice, with no jargon.
- Every place they stumble, get vague, or fall back on jargon is a precise knowledge gap — send them back to the source there, then re-explain.

### Add elaboration and dual coding (correctly)

- Elaboration: ask "why is this true?" and "how does this connect to what you already know?"; have the learner generate their own examples.
- Dual coding: pair words with a relevant diagram or sketch for a second retrieval path — but only when the visual is conceptually coherent, not decorative. Irrelevant images and redundant on-screen text add load and hurt.

## Examples

### Example 1: Weak vs strong study

❌ Weak (illusion of competence):
```
Reread the chapter and highlight the important parts, then read it again the night before.
```

✅ Strong (desirable difficulty):
```
Read once. Close the book and brain-dump everything you remember.
Check, then make 8-10 questions from the gaps. Self-quiz those across 4 short
sessions this week, mixing in last week's topics.
```

What changed: passive review became retrieval + spacing + interleaving — harder in the moment, far better at the test.

### Example 2: Naming the myth

A learner says "I'm a visual learner, what's the best format for my style?" Don't accommodate the request. The learning-styles matching hypothesis is empirically unsupported. Redirect: everyone benefits from dual coding (coherent visuals plus words) and from retrieval — pick the format that fits the material, not a personal "style".

## Checklist

- [ ] Is the learner producing answers from memory (not just rereading or recognizing)?
- [ ] Is study spaced across multiple days rather than massed?
- [ ] Are confusable topics interleaved so the learner practices choosing the method?
- [ ] For a novice, are worked examples used — and faded as they improve?
- [ ] Did you name and avoid the weak defaults (rereading, highlighting, summarizing, cramming, learning styles)?
- [ ] Did you tell the learner the right methods feel harder, so they don't mistake difficulty for failure?
- [ ] Is progress judged by delayed recall and transfer, not in-the-moment fluency?

## Composition / References

- [Roediger & Karpicke — retrieval practice / the testing effect (2006)](https://pdf.poojaagarwal.com/Roediger_Karpicke_2006_PsychReview.pdf)
- [Karpicke & Roediger — The Critical Importance of Retrieval for Learning (2008, Science) — the ~80% vs ~36% one-week result](https://www.science.org/doi/10.1126/science.1152408)
- [Dunlosky et al. — high- vs low-utility learning techniques (2013)](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html)
- Spacing — Cepeda et al. (2008); interleaving — Rohrer & Taylor (2007); desirable difficulties — Bjork & Bjork
- Learning styles are a myth — the matching hypothesis is empirically unsupported; do not accommodate it
