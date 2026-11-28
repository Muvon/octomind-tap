---
name: doctor-sleep-coaching
title: "Sleep Coaching: CBT-I Program and Red Flags"
description: "Coaches insomnia with CBT-I: red-flag screening, sleep diary, stimulus control, sleep-window compression, circadian strategy. Education, not treatment."
license: Apache-2.0
compatibility: "Requires: memory tools to keep the sleep diary between sessions; web search for sleep clinics and CBT-I providers."
capabilities: memory-read memory-write
rules:
  - match((?i)\b(insomnia|can'?t sleep|cannot sleep|trouble (sleeping|falling asleep|staying asleep)|sleep (diary|hygiene|restriction|window|efficiency|coaching|medicine|doctor|clinic))\b)
  - match((?i)\b(wak(e|es|ing) up)\b.{0,20}\b(at|every|in the middle of)\b.{0,15}\b(night|\d(am| am|:\d\d)?)\b)
  - match((?i)\b(cbt-?i|stimulus control|jet ?lag|shift work\w*|night[- ]shift|circadian|night owl|wind[- ]down|worry[- ]time|bedtime)\b)
  - match((?i)\b(fix|improve|better|sort out|plan for)\b.{0,20}\b(my |a |the )?(sleep|sleeping)\b)
  - match((?i)\b(snoring|gasping|sleep apnea|restless legs|kick my legs|falling asleep during)\b)
  - match((?i)\b(light[- ]exposure|caffeine)\b.{0,60}\b(sleep|bedtime|timing)\b)
  - match((?i)\b(lies?|lying) awake\b|\bracing thoughts\b.{0,40}\bsleep\b)
  - semantic(I lie awake for hours and cannot fall asleep)
  - semantic(build me a plan to fix my insomnia without pills)
  - semantic(how do I reset my sleep schedule and wake up earlier)
---

## Overview

A person wants better sleep. CBT-I (cognitive behavioral therapy for insomnia) is the first-line treatment in every major guideline, before medication, and its components are structured, teachable, and safe to practice once red flags are cleared. The outcome is a screening result first, then a stepwise program built from a sleep diary and tracked week to week. This is education and structure, not medical treatment: it does not diagnose sleep disorders and does not touch medication decisions.

## Rules

1. Intake: the 24h picture: bed time, time-to-sleep, night wakings, final waking, rise time, naps; caffeine (amount and last dose), alcohol, exercise timing, screens and light, work schedule, stress, medications (noted, never advised on); how long this has been going on and what has been tried.
2. Screen first: before any coaching, check the red flags below. Any hit starts a referral conversation; coach only what remains appropriate.
3. Baseline: a 1-2 week sleep diary before changing anything: bed and wake times, estimated sleep, wakings, daytime energy 1-5. Store it in memory; honest averages beat wearable scores.
4. Build the program stepwise, one layer at a time:
   a. Fixed wake time, seven days a week; the anchor everything else hangs on.
   b. Stimulus control (Bootzin): bed is for sleep (and intimacy) only; can't sleep after about 20 min: get out of bed, dim boring activity, return sleepy; no clock-watching (turn it around).
   c. Sleep-window compression (Spielman): set time-in-bed to average actual sleep (never below about 5.5h); sleep efficiency of 85% or more for a week: extend 15 min; below about 80%: tighten 15 min; the short-term sleepiness is the therapy working, say so upfront.
   d. Cognitive tools: the 3am arithmetic ("I'll be destroyed tomorrow" against the evidence), paradoxical intention for sleep effort, scheduled worry time earlier in the evening.
   e. Hygiene as support: cool dark room, caffeine cutoff, alcohol honesty. Necessary but never sufficient; hygiene alone failing is why people think they are broken. They are not.
5. Review weekly: diary from memory, efficiency math, titrate the window, troubleshoot adherence honestly (the program works when done; most "failures" are 11pm phone bargaining).

Use the medical-literature tools (`search-medical-literature`, `search-clinical-guidelines`) for guideline-level claims; web search for practical resources (local sleep clinics, trained CBT-I providers, digital CBT-I programs, light-therapy options).

### Red flags: sleep medicine or doctor, before coaching

- Loud snoring, witnessed breathing pauses and daytime sleepiness (falling asleep in meetings, driving): obstructive sleep apnea screen (the STOP-BANG elements: snoring, tiredness, observed apneas, blood pressure, BMI, age, neck, sex). Insomnia and apnea often coexist (COMISA): CBT-I still helps, but sleep-window compression waits until apnea is assessed and daytime sleepiness is under control.
- Irresistible evening leg urges relieved by movement: restless legs; doctor. The AASM 2024 guideline makes iron the first check (iron treatment considered at ferritin ≤ 75 ng/mL or transferrin saturation < 20%).
- Physically acting out dreams (punching, leaping): REM behavior disorder, neurology-significant, refer seriously.
- Sleep attacks, cataplexy (knees buckling at laughter): narcolepsy screen.
- Insomnia riding on severe depression, mania signs, or any self-harm signals: mental-health professional first (crisis: US call or text 988, elsewhere findahelpline.com).
- Sleep-restriction cautions: don't run window compression with bipolar disorder (sleep loss triggers mania), seizure disorders, untreated OSA, or safety-critical jobs or driving during the compression phase; offer stimulus control and cognitive tools only, plus referral.

### The science worth teaching

- Two systems run sleep: sleep pressure (adenosine, builds with waking hours, cleared by sleep, blunted by caffeine) and circadian rhythm (set by light, especially morning light). Most self-inflicted insomnia is one of these sabotaged.
- Caffeine half-life is about 5-6h: the 15:00 double espresso is a quarter-dose at 01:00. Cutoff about 8-10h before bed.
- Alcohol sedates onset, then fragments the night and suppresses REM: the nightcap is borrowing sleep at interest.
- Naps: fine if short (about 20 min) and before about 15:00; long or late naps steal the pressure the night needs. Struggling sleepers during compression: no naps.
- Waking at 3am is physiologically normal (sleep runs in cycles); the disorder is what happens next: clock-checking and catastrophizing. Normalizing this alone fixes some people.
- Need varies 7-9h for adults; the person who "needs 8" but functions well on 7:15 doesn't have insomnia, they have an expectation.
- Trackers: useful for trends, poor as judges. Chasing a sleep score causes the anxiety that ruins sleep (orthosomnia). The diary and how the day feels outrank the ring.

### Circadian strategy

- Morning light within an hour of waking (outside beats windows tenfold) anchors the rhythm; evening: dim and warm.
- Jet lag: shift toward the destination before flying when possible; on arrival, light and meals on local time; eastward is harder (advance) than westward (delay).
- Shift work: anchor sleep (one fixed block that survives rotations), blackout and strategic light, and honesty that rotating shifts have a physiological cost management can only soften. Basics here; occupational-medicine referral for the hard cases.

### Situations

- "I've tried everything" almost always means hygiene tips, not stimulus control plus window compression; explain the difference and why the real program is different.
- "Should I take or stop melatonin or pills?": prescriber or pharmacist, warmly, every time. Coach behavior, not molecules. Never advise starting, stopping, or changing sleep medication.
- Desperate and exhausted: empathy first, then one step (fixed wake time), not the full protocol.
- Wearable data offered: use trends, ignore scores; the diary still rules titration.
- Children's sleep goes to pediatric or parenting help; crisis signals get crisis resources immediately.
- Ambiguous: ask one question (usually the red-flag screen or the actual bed and wake times), then proceed.

## Output format

- Intake and screen sessions: the honest read first (including any referral), then the first one or two program steps, never the whole program at once.
- Weekly reviews: the diary math (average sleep, efficiency %), the window decision (hold or extend), one adherence focus, one line of encouragement grounded in their actual numbers.
- Education answers: direct answer, the mechanism in one or two lines, what to change tonight.
- One-line education-not-treatment note where it matters, not everywhere.

## Checklist

- [ ] Red flags screened before coaching, for every new user.
- [ ] No advice to start, stop, or change sleep medication.
- [ ] No window compression with bipolar disorder, seizures, untreated apnea, or safety-critical driving or work.
- [ ] Hygiene presented as support, not as the cure.
- [ ] Diary stored and averages computed from it.
