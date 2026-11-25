---
name: math-misconceptions
title: "Math Misconceptions and Counterexamples"
description: "Diagnose and repair a math misconception with short counterexamples for fractions, operations, algebra, functions, or statistics."
license: Apache-2.0
domains: tutor
rules:
  - session(tap-tutor-math-)
  - match((?i)\b(math|algebra|fractions?|statistics|calculus)\b.{0,40}\b(misconception|why|confus\w*)\b)
---

## Overview

Use a diagnostic example when a learner can perform a procedure but applies it to the wrong cases.

## Rules

Ask the learner to predict what happens in the example, test it, and explain where the original rule fails.

| Topic | Misconception | Counterexample the learner can test |
|---|---|---|
| Operations | Multiplying always makes bigger; "= means compute" | 6 × ½ = 3; 3 + 4 = 5 + 2 |
| Fractions | 1/8 > 1/4 because 8 > 4; add numerators and denominators | Cut the same pizza into 8 and 4 pieces; 1/2 + 1/2 is not 2/4 |
| Signs | Two negatives always give a negative; subtracting a negative makes less | A number line: 5 − (−2) = 7 |
| Algebra | (a + b)² = a² + b²; cancel terms instead of factors | a = 3, b = 4: 49 versus 25; (x + 2)/2 is not x + 1 at x = 2 |
| Variables | A letter is a label for an object ("a" for apples), or always stands for one fixed value | Substitute two different numbers and compare the results |
| Functions and limits | A limit is the value at the point; a limit can never be reached | f(x) = (x² − 1)/(x − 1) has a limit of 2 at 1 and is undefined at 1 |
| Statistics | A p-value is the probability the hypothesis is true; correlation shows cause | Simulate many tests of a true null: p < 0.05 appears about 5% of the time |

## Checklist

- [ ] The example targets the learner's observed misconception.
- [ ] The learner tests the revised rule on a different problem.
