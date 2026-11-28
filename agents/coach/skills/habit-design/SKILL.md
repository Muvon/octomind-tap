---
name: habit-design
title: "Build or Break a Habit: Cue, Friction and Recovery"
description: "Build or break an everyday habit using a small starting behavior, a concrete cue, reduced friction, and an if-then recovery plan."
license: Apache-2.0
rules:
  - match((?i)\b(build|start|break|change|stick (to|with))\b.{0,45}\b(habits?|daily routine)\b)
  - match((?i)\b(habit stack(ing)?|habit loop|habit recipe|habit formation)\b)
---

## Overview

Design a repeatable everyday behavior and rehearse a restart after a lapse. Clinical or dangerous behavior needs qualified help.

## Procedure

1. Clarify the target — one specific habit to build or break, and the identity behind it ("who do you want to become?").
2. Readiness check — ask how ready they are and what pulls them both ways; if they're still ambivalent, explore pros/cons and their own reasons (motivational-interviewing style) before tactics.
3. Deconstruct the loop — for a bad habit, map cue → craving → response → reward and find the trigger; for a good habit, find a reliable anchor.
4. Shrink it — define the under-2-minute / under-30-second tiny version so it can't fail on a hard day.
5. Design the cue — write the explicit recipe: habit stack ("After I ___, I will ___") or if-then plan; engineer the environment so good cues are obvious and bad cues invisible.
6. Build the reward — add an immediate celebration (Fogg's "Shine") or a satisfying tracker to close the loop.
7. Relapse-proof it — pre-identify high-risk situations, write coping if-then plans, and install "never miss twice" plus the abstinence-violation reframe.
8. Set expectations — realistic timeline (about two months median, often much longer, not 21 days), define the next check-in and what one daily "vote" looks like.

remember() the person's active habits and past attempts; memorize() the recipe, high-risk situations, and progress.

## Methods

| Framework | Originator | Core mechanic |
|-----------|------------|---------------|
| Habit loop + Four Laws | James Clear, Atomic Habits | Make it obvious/attractive/easy/satisfying (invert to break); habit stacking; 2-minute rule |
| Identity-based habits | James Clear | "Every action is a vote" for the person you want to be |
| Tiny Habits B=MAP | BJ Fogg, Stanford | Behavior = Motivation × Ability × Prompt; anchor + tiny behavior + celebration; design for ability, not motivation |
| Implementation intentions | Peter Gollwitzer | If-then plans (d≈0.65 in 2006; d≈.27-.66 across 642 tests, Sheeran et al. 2025); for breaking: "If urge to X, then Y instead" |
| Readiness / stages of change | Prochaska & DiClemente; Miller & Rollnick | Useful for spotting ambivalence; stage-matched programs haven't beaten generic ones in trial syntheses (Riemsma 2003, Romain 2018), so check readiness, don't run a rigid stage script |
| Relapse prevention | Marlatt & Gordon | High-risk situations, coping skills, defuse the abstinence-violation effect |
| Habit-formation timing | Lally et al. 2010; Singh et al. 2024 review | Medians 59-66 days, means 106-154 days, individual range 4-335; one miss barely matters |

Treat a lapse as evidence for adjusting the plan, and avoid fixed promises about how quickly a habit forms. For dangerous substance withdrawal, including alcohol or benzodiazepines, advise medical supervision before stopping; persistent, severe paralysis or anhedonia can be clinical and belongs with a licensed clinician.

Starting too big is the number-one reason habits die in week one. A bad environment beats good intentions every time, so design the cue and the friction, not just the person. Don't frame willpower as a tank that runs out: ego depletion failed large multi-lab replications (Hagger et al. 2016; Vohs et al. 2021).

## Output

Produce a concrete recipe the person can run today:
- Habit — the specific behavior, build or break, and the identity it serves
- Tiny version — the under-2-minute starting behavior
- Cue — the habit stack or if-then ("After I ___, I will ___")
- Environment — what to make obvious / what to make invisible
- Reward — the immediate celebration or tracker
- Relapse plan — high-risk situations + coping if-then + "never miss twice"

Save to `habit-[name-slug].md` in the working directory only if asked.

## Checklist

- [ ] The person can name the cue, tiny action, and immediate reward.
- [ ] A lapse has a specific recovery plan.
- [ ] Save a file only when requested.
