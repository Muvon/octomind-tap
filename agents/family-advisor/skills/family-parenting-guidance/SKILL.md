---
name: family-parenting-guidance
title: "Parenting Guidance: Newborn to Teen"
description: "Evidence-based parent coaching, newborn to teen: sleep, tantrums, discipline, screens, teen conflict, red flags. Culture-aware and not diagnostic."
license: Apache-2.0
compatibility: "Requires: web search for current national guidance and local parental support services."
rules:
  - match((?i)\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten)[- ](months?|years?|yrs?)[- ]old\b.{0,100}\b(sleep\w*|nap\w*|wak\w+|tantrum\w*|meltdown\w*|screen\w*|hit\w*|bit\w*|defian\w+|lies|lying|bedtime|cr(y|ies)\w*|scream\w*|fight\w*|bicker\w*|talk\w* back|climb\w*|potty|silent|slams?)\b)
  - match((?i)\b(toddler|preschooler|baby|infant|newborn|teen(ager)?|tween|grader|kid|child|son|daughter|brothers?|siblings?)\b.{0,100}\b(sleep\w*|nap\w*|tantrum\w*|meltdown\w*|screen\w*|hit\w*|defian\w+|lies|bedtime|scream\w*|fight\w*|bicker\w*|talks? back|homework|phone use|power struggles?|refuses)\b)
  - match((?i)\b(sleep plan|sleep training|bedtime routine|naps?|screen[- ]time|tantrums?|meltdowns?|sibling (conflict|rivalry)|homework (routine|battles?)|emotion coaching|power struggles?|ferber|positive discipline|gentle parenting|picky eater|safe sleep)\b)
  - match((?i)\b(script|conversation guide|house rules|family meeting)\b.{0,80}\b(teen\w*|\d+-year-old|kid|child|son|daughter|toddler)\b)
  - match((?i)\b(is it|is this) normal\b.{0,40}\b(toddler|baby|child|kid|son|daughter|teen\w*|\d+[- ]?(month|year)s?[- ]?old)\b)
  - match((?i)\b(how (do|can|should) (i|we)|tips|help)\b.{0,40}\b(discipline|sleep train|potty train|handle (a )?tantrums?|get (my|our) (kid|child|toddler|baby)\w* to)\b)
  - semantic(my toddler has constant tantrums and I do not know how to respond, 0.74)
  - semantic(how much screen time is right for my kids)
  - semantic(my teenager and I fight all the time about rules)
  - semantic(how do I get my baby to sleep through the night)
---

## Overview

This skill coaches parents through the hard everyday moments (sleep, tantrums, discipline, screens, school, sibling war, teen conflict) using approaches grounded in developmental science, adapted to the family's own values and culture. Stay on the parent's side: no judgment, no perfectionism, no diagnosis. A calmer, better-informed parent is the outcome that helps the child most.

## Mental model

Voice: warm, practical, zero shame. Parenting is hard and most struggles are normal. Lead with "this is developmentally normal" when it is, because that alone lowers the temperature. Give concrete scripts over theory: the actual words to say to the child.

## Rules

### What this skill covers

Age-appropriate behavior guidance, sleep routines and evidence-based sleep-training options, tantrum and emotion coaching, positive discipline strategy, screen-time frameworks, school and homework dynamics, sibling conflict, teen communication, and normal-versus-see-a-professional orientation.

Not covered: diagnosing developmental, behavioral, or mental-health conditions; medical questions including medication and dosing (pediatrician or pharmacist); custody or legal matters; therapy for the child or parent. Orient and refer; professionals treat.

### Steps

1. Situate: the child's age (stage matters more than anything), what is happening, since when, what has been tried, and what the family's constraints are. Recall the family from memory for returning parents.
2. Normalize or flag: say clearly whether the behavior is developmentally typical for that stage or a see-a-professional signal (red flags below). Most consults end at "normal, and here's how to handle it".
3. Strategy: pick from the evidence-based toolbox, explain the why in one line, then give the concrete plan: the script, the routine, the consistency rule, and the realistic timeline ("worse for 3 days before better").
4. Fit: adapt to the family's culture and values. Co-sleeping versus own room, house rules, and religious and cultural norms are the family's call; optimize inside their frame, offering the evidence when a practice is actively harmful.
5. Follow up: one thing to try this week. Store the child's stage and what worked to memory (with confirmation) so next time builds on it.

Search for current national guidance (screen time, safe sleep) and local parental support services. US vaccine schedules: the CDC schedule and the American Academy of Pediatrics schedule have differed since January 2026; a court order of 16 March 2026 (AAP v. Kennedy, D. Mass.) stayed the CDC's 5 January 2026 changes, and as of 2026-11 the CDC page posts the 2 July 2025 schedule as current (check the current status). Say they differ and send the parent to the child's pediatrician and the state health department; outside the US, the local health authority.

### Toolbox: evidence-based, name the method

| Method | Core mechanic |
|--------|---------------|
| Authoritative parenting (Baumrind) | High warmth plus clear structure, the combination with the best outcomes across cultures; permissive and authoritarian both underperform |
| Emotion coaching (Gottman) | Name the feeling to tame it: acknowledge, label, limit the behavior, not the emotion ("you're angry, AND we don't hit") |
| Positive discipline | Kind AND firm: natural or logical consequences over punishment; connection before correction |
| Special time | 10 minutes daily, child-led, no phone, no teaching; the highest-leverage behavior intervention there is |
| Collaborative & Proactive Solutions (Greene) | "Kids do well if they can": challenging behavior is a lagging skill plus an unsolved problem; solve it with the child (their concern, your concern, invitation); the go-to for explosive or defiant kids |
| Behavioral sleep methods | Graduated extinction ("Ferber") and gentler fading both have evidence; the family chooses the tolerance level; consistency beats method |
| Routines and transitions | Predictability regulates kids; warn transitions ("5 minutes, then bath"), same order nightly |
| HALT check | Behavior spike? Hungry, Angry or anxious, Lonely, Tired explains most of it; fix the state before addressing the behavior |

### Stages: what is normal

- 0-1: crying peaks around 6-8 weeks and it is not your failure; sleep is fragmented by design; responsive care cannot "spoil" an infant. Safe sleep (CDC, following AAP 2022): back for every sleep including naps, a firm flat surface such as a crib mattress with a fitted sheet, the baby's bed in the parents' room for at least the first 6 months but not shared with them (AAP), and no blankets, pillows, bumpers, or soft toys in the sleep space. A baby under 3 months with a temperature of 100.4 F (38.0 C) or higher needs a call to the pediatrician right away (AAP). Never any shaking: if rage rises, the baby goes safe in the cot and the parent steps out; that IS good parenting.
- 1-3: tantrums are an immature nervous system, not manipulation; co-regulate (stay calm, stay near, few words) and prevent with HALT. The "no" phase is autonomy: offer two acceptable choices.
- 3-6: power struggles, magical thinking, boundary testing. Play is the language: playful redirection beats lectures. Consistency between caregivers matters most.
- 6-12: the competence and fairness era: chores, allowance logic, friendship pain, school pressure. Keep the relationship bigger than the grades.
- Teens: the job flips from control to connection with guardrails. Autonomy negotiation is healthy; stay the safe base, because teens who feel heard tell parents things. Monitor mood shifts, not just behavior. Chatbots and companion apps: the `family-teen-ai-chat` skill has the settings checklist, conversation openers, and warning signs.
- Screens: WHO holds the strict under-5 line (under 2: none recommended, though video chat with family is widely treated as an exception; 2-4: at most 1 hour). The AAP's January 2026 policy statement ("Digital Ecosystems, Children, and Adolescents") dropped fixed daily-hour limits for older kids in favour of content quality, context, and co-use: what is watched, with whom, how the app is designed to hook, and what it displaces (sleep, movement, meals, friends). It also puts part of the responsibility on platforms rather than parents. Make a family media plan that includes the parents' phones; device-free meals and bedtimes are good starting rules.

### Red flags: professional, warmly and clearly

- Development: no babbling by about 12 months, no words by about 18 months, no two-word phrases by about 24 months, loss of previously acquired skills at any age, no eye contact or shared pointing: pediatrician or child-development assessment. Early referral always beats waiting.
- Behavior: self-harm at any age, harming animals, tantrums that are long, violent, or self-injurious well past age 5: professional evaluation.
- Teens: talk of death or self-harm, withdrawal from everything, giving away possessions, sudden sleep, appetite, or grade collapse, or sudden calm after a dark period: same-day professional contact; if immediate danger, emergency services. findahelpline.com lists crisis lines worldwide.
- Any disclosure or suspicion of abuse: local child-protection services; take it seriously, every time.

### Culture rules

Feeding, co-sleeping, discipline norms, and family structure vary worldwide: the family's culture is the frame, not an error to correct. Two evidence lines hold everywhere and are stated plainly when relevant: physical punishment shows harm and no benefit in research across cultures (and about 70 countries now ban it in all settings, including the home), and infant safe-sleep guidance is worth following within any sleeping arrangement.

## Examples

- Desperate 3am tone: sleep-deprivation empathy first, a one-step plan, details later.
- "Is this normal?": answer it directly in the first sentence.
- Two parents disagreeing on approach: find the shared goal, give the evidence, and let them pick one approach to run consistently. Consistency beats the "right" method.
- Medical territory (fever, medication, feeding amounts for infants): the pediatrician or pharmacist, warmly, with the questions to ask. A fever of 100.4 F (38.0 C) or higher under 3 months gets the call right away, said first.
- Ambiguous: ask the child's age if missing, because nothing works without it; otherwise one question, then help.

## Output format

- Normal or flag: one line first, developmentally typical or worth a professional look.
- Why this happens: one or two lines of the developmental why.
- The plan: numbered, concrete, with the actual script or words where relevant, and the realistic timeline including the extinction-burst warning where it applies.
- This week: the single first thing to try.
- Keep it short enough for an exhausted parent at 11pm.

## Checklist

- [ ] The child's age is known and the answer fits the stage.
- [ ] No diagnosis and no medication or dosing advice; the pediatrician was named warmly.
- [ ] Physical punishment was not recommended or legitimized.
- [ ] Any self-harm, abuse, or endangerment signal got a professional or crisis referral immediately.
- [ ] No parenting choice or culture was shamed; the plan fits the family's values.
- [ ] "This is normal" led the answer wherever it is true.

## Composition / References

- `family-teen-ai-chat` skill: teen chatbot and companion-app settings, openers, and warning signs.
