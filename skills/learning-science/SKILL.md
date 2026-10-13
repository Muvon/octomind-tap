---
name: learning-science
title: "Learning Science: Make Studying Actually Stick"
description: "The small set of evidence-based study techniques that actually work: retrieval practice, successive relearning, spacing, interleaving, self-explanation, and worked examples, plus how to use AI tutors without outsourcing the thinking, and the popular habits (rereading, highlighting, cramming, learning styles) that only feel productive. Activate when helping someone study, memorize, prepare for a test, or learn a skill, or when they ask how to learn something faster."
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
- Give corrective feedback after the attempt; retrieval without feedback lets errors stick.

### Relearn to criterion (successive relearning)

- Within a session, keep retrieving each item until it is recalled correctly at least once, then drop it for that session.
- Repeat the whole set in later spaced sessions until recall is fast and correct. Retrieval-to-criterion plus spacing is among the strongest classroom-tested methods (Rawson & Dunlosky).
- Enforce the criterion: learners who drop items when they merely feel known drop them too early and lose the benefit.

### Space it out

- Break study into multiple sessions across days instead of massing it into one block; for the same total time, spaced study gives substantially better long-term retention than cramming.
- Rule of thumb for the gap (Cepeda et al., 2008): roughly 20-40% of the retention interval when that interval is about a week, shrinking to about 5-10% when it is a year. For an exam next week, review every day or two; to hold something for a year, review roughly monthly.
- For fact-heavy material, use a spaced-repetition system. Anki's FSRS scheduler is the current default choice: keep desired retention near 0.90, press Again whenever recall failed (Hard counts as a pass), and cap new cards so daily reviews stay sustainable.

### Interleave confusable material

- Mix related problem types or topics within a session (ABCABC) instead of blocking one type at a time (AAABBBCCC).
- Interleaving forces the learner to first decide which method applies — the actual exam skill that blocked practice hides.
- The benefit is real but moderate on average (meta-analytic g ≈ 0.42, Brunmair & Richter 2019) and depends on similarity: largest for confusable categories and problem types, small or absent for unrelated material. Interleave things the learner mixes up, not everything.
- It feels harder and lowers in-session accuracy. Warn the learner that the difficulty is the point.

### Match guidance to expertise

- For a true novice on a new procedure, a fully worked example beats unguided problem-solving — it avoids cognitive overload.
- As competence grows, fade the worked steps (completion problems → backward fading → independent solving). Continuing to spoon-feed examples to someone ready to practice alone stops helping (expertise reversal).
- For conceptual understanding, a short attempt at a well-designed problem before instruction (productive failure, pretesting) can beat instruction-first, provided the explanation follows the attempt (Sinha & Kapur 2021 meta-analysis). Don't leave novices to flounder on procedures with no instruction coming.

### Use self-explanation (the Feynman technique) as a gap-finder

- Have the learner explain the concept in plain language, as if teaching a novice, with no jargon. Self-explanation and explaining to others are well supported (Chi; Fiorella & Mayer); the Feynman label is a convenient name, not separate evidence.
- Every place they stumble, get vague, or fall back on jargon is a precise knowledge gap — send them back to the source there, then re-explain.

### Add elaboration and dual coding (correctly)

- Elaboration: ask "why is this true?" and "how does this connect to what you already know?"; have the learner generate their own examples.
- Dual coding: pair words with a relevant diagram or sketch for a second retrieval path — but only when the visual is conceptually coherent, not decorative. Irrelevant images and redundant on-screen text add load and hurt.

### Use AI tutors as a coach, not an answer machine

- The evidence splits on design. In a field experiment with ~1,000 high-school math students, an unrestricted GPT-4 chat raised practice scores but lowered later exam scores by 17% versus no AI; a tutor version that gave hints instead of answers removed most of that harm (Bastani et al., PNAS 2025). Structured AI tutors built on good pedagogy have produced large short-term gains (Kestin et al., Scientific Reports 2025; a World Bank trial in Nigeria, 0.31 SD in six weeks).
- So the rules are the same as for a human tutor: the learner attempts first, the AI gives the next hint rather than the solution, the learner explains the result back, and final retrieval happens without the AI.
- Treat AI output as material to check, not to copy. Asking the AI to quiz the learner, generate practice questions, or critique the learner's own explanation keeps the thinking on the learner's side.

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

A learner says "I'm a visual learner, what's the best format for my style?" Don't accommodate the request. The learning-styles matching hypothesis is empirically unsupported (Pashler et al., 2008, and later reviews). Redirect: everyone benefits from dual coding (coherent visuals plus words) and from retrieval — pick the format that fits the material, not a personal "style".

## Checklist

- [ ] Is the learner producing answers from memory (not just rereading or recognizing), with feedback after each attempt?
- [ ] Is study spaced across multiple days, with items relearned to criterion rather than dropped when they feel familiar?
- [ ] Are confusable topics interleaved so the learner practices choosing the method?
- [ ] For a novice, are worked examples used — and faded as they improve?
- [ ] If an AI tool is in the loop, does the learner attempt first and get hints, not finished answers?
- [ ] Did you name and avoid the weak defaults (rereading, highlighting, summarizing, cramming, learning styles)?
- [ ] Did you tell the learner the right methods feel harder, so they don't mistake difficulty for failure?
- [ ] Is progress judged by delayed recall and transfer, not in-the-moment fluency?

## Composition / References

- [Roediger & Karpicke — retrieval practice / the testing effect (2006)](https://pdf.poojaagarwal.com/Roediger_Karpicke_2006_PsychReview.pdf)
- [Karpicke & Roediger — The Critical Importance of Retrieval for Learning (2008, Science) — the ~80% vs ~36% one-week result](https://www.science.org/doi/10.1126/science.1152408)
- [Dunlosky et al. — high- vs low-utility learning techniques (2013)](https://www.psychologicalscience.org/publications/journals/pspi/learning-techniques.html)
- [Cepeda et al. — Spacing effects in learning: a temporal ridgeline of optimal retention (2008)](https://pubmed.ncbi.nlm.nih.gov/19076480/)
- [Brunmair & Richter — Similarity matters: a meta-analysis of interleaved learning (2019)](https://doi.org/10.1037/bul0000209)
- Successive relearning — Rawson & Dunlosky (2022 review); productive failure — Sinha & Kapur (2021, Review of Educational Research); desirable difficulties — Bjork & Bjork
- [Bastani et al. — Generative AI without guardrails can harm learning (PNAS 2025)](https://doi.org/10.1073/pnas.2422633122)
- Kestin et al. — AI tutoring outperforms in-class active learning (Scientific Reports 2025); De Simone et al. — World Bank Policy Research Working Paper 11125 (2025)
- Learning styles — Pashler, McDaniel, Rohrer & Bjork (2008, Psychological Science in the Public Interest): the matching hypothesis is unsupported; do not accommodate it
