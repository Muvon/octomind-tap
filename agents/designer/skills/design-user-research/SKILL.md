---
name: design-user-research
title: "Thematic Analysis for User Research: Quotes, Personas"
description: "Turn interviews and usability notes into coded themes (thematic analysis) traced to verbatim quotes; build personas, plan usability tests or card sorts."
license: Apache-2.0
compatibility: "Works from transcripts, notes, or feedback exports in the working directory. No special tools."
rules:
  - match((?i)\b(synthesi[sz]e|code|analy[sz]e|summari[sz]e|cluster|pull\s+out|turn)\b.{0,60}\b(interviews?|transcripts?|user\s+research|survey\s+(responses|answers)|open-ended|usability\s+sessions?|user\s+feedback|support\s+tickets?)\b)
  - match((?i)\b(themes?|affinity[\s-]map\w*|thematic\s+analysis|insight\s+nuggets?|atomic\s+insights?|(research|insight)\s+repository|jobs[\s-]to[\s-]be[\s-]done|JTBD|verbatim\s+quotes?)\b)
  - match((?i)\b(discussion\s+guide|interview\s+(script|guide|study)|leading\s+questions?|double-barreled|sample\s+(plan|adequacy)|(enough|sufficient)\b.{0,20}\bparticipants?)\b)
  - match((?i)\b(contradict\w*|disagree\w*|confidence)\b.{0,50}\b(interviews?|findings|participants?|transcripts?|readout)\b)
  - match((?i)\b(plan|script|design)\b.{0,25}\b(usability\s+tests?|card\s+sorts?|user\s+tests?)\b|\bSUS\s+scor\w+|\b(create|make|build|write|draft)\b.{0,20}\bpersonas?\b)
  - semantic(what did users say about this in our interviews, 0.78)
  - semantic(turn these interview notes into themes with supporting quotes, 0.78)
  - semantic(build user personas from our customer feedback, 0.78)
  - semantic(plan a usability test with tasks and participants, 0.78)
  - semantic(run a card sort to organize our navigation, 0.78)
---

## Overview

This skill turns raw qualitative data, such as interview transcripts, open-ended survey answers, support tickets, and usability session notes, into coded themes, evidence-linked insights, and research artifacts teams use. Analysis is the biggest time sink in research; the goal is to compress it without losing rigor. The non-negotiable is traceability: every theme cites the verbatim quotes and participants behind it. An insight that can't be traced to evidence is an opinion, and is labelled as one.

It covers qualitative coding (descriptive first pass, then analytical themes), thematic analysis across sessions, affinity mapping, atomic insight nuggets (evidence, insight, recommendation), evidence-grounded personas and jobs-to-be-done statements, confidence grading, contradiction hunting, research repository structure and tagging, study-design feedback (question quality, sample adequacy), and usability-test and card-sort plans (task scripts, success measures, sample size, SUS scoring).

It does not recruit participants or run live sessions, evaluate a UI against heuristics, do market or competitor research, run survey statistics beyond descriptives, or decide product priorities: it supplies the evidence and the decision belongs to the product owner.

## Mental model

What users say is not what they do. Frequency is not importance. A claim is only as strong as the participants and quotes behind it, so every step keeps the path from a recommendation back to raw words.

## Rules

Method:

1. Ingest: read every source file; catalog participants, method, and study question. Replace names and identifying details with participant IDs (P01, P02) in everything you write. Recall prior studies to connect.
2. Code: line-by-line descriptive codes close to the data, tagged with participant and source location. Codes use the participants' language before yours.
3. Theme: cluster codes into descriptive themes, then analytical themes that answer the study question. A theme needs 3 or more participants, or it is flagged as an outlier signal, not a pattern.
4. Stress-test: hunt for disconfirming quotes for every theme and count them in. Check whether themes differ by segment. Note what the data cannot answer.
5. Deliver the synthesis report plus atomic nuggets for the repository, connected to prior studies' themes where they corroborate or contradict. Record the theme map and open questions for future studies.

Evidence rules:

- Every claim carries its evidence: theme, participant count, 2 to 3 verbatim quotes with source references. A stakeholder must be able to walk from any recommendation back to raw words.
- Confidence grades per finding: strong (multiple participants, unambiguous quotes, no contradictions), moderate (pattern present but mixed or thin), weak (interesting, needs another study). Weak findings ship as hypotheses, never as conclusions.
- Separate reported behavior from observed behavior in coding and weight observed higher. Stated willingness to pay is the least trustworthy quote type in the corpus.
- A theme mentioned by 3 of 12 participants who then abandoned the product outranks one mentioned by 10 in passing. Severity and consequence are part of the analysis.
- Personas are built from clustered observed behavior in the data (goals, pains, quotes per cluster), never from demographic guesswork. If the data can't support distinct clusters, say so instead of inventing them.
- Atomic nugget format keeps the repository queryable: one observation, its evidence, and its tag set (product area, user segment, journey stage, study). Reports expire; nuggets compound.
- Sample size depends on the method. About 5 users per segment surfaces most issues in a usability test; interview studies usually reach thematic saturation somewhere around 9 to 17 interviews (Hennink and Kaiser, 2022), more for diverse segments. Say "of the 6 people we spoke to", never "users think".
- AI-assisted synthesis is a first pass, not the analysis. Copy every quote from the source file and check it against the source (machine transcripts mishear; flag doubtful words rather than guess). Check every machine-suggested code against the passage it came from. Synthetic users and AI-generated personas are never evidence; outputs from them are hypotheses for real participants to test, labelled as such.
- Before quoting from or storing a corpus, check that participants consented to how it is being processed.
- Never invent or paraphrase quotes, present a single-participant anecdote as a pattern, blend reported and observed behavior, or generalize beyond the sample.

Usability-test plan, when asked to plan a test:

- A research question, then 5 to 8 realistic tasks. Each task is written as a goal with no interface words in it and has a pass or fail success criterion.
- Per task record completion, time on task, and errors, plus one open question.
- For a quantitative study use at least 20 users (NN/g).
- After the tasks, give the 10-item System Usability Scale. Score each item (odd items: response minus 1; even items: 5 minus response), sum, and multiply by 2.5 for 0 to 100. The mean across about 500 studies is 68 (MeasuringU), so report the score with a confidence interval, not as a grade.
- Card sort for navigation or labels: at least 15 participants per user group (NN/g); 5 participants correlate only 0.75 with the full result.
- Pilot the script with one colleague before real sessions. State consent and recording arrangements in every plan.

## Examples

- Transcripts are shared: run full coding and synthesis. If the study question is missing, ask for it, because synthesis without a question drifts. In a non-interactive run, infer the question from the corpus, state it as an assumption, and proceed.
- "What did users say about X?": query the corpus and answer with quotes and references.
- "Make personas": only from clustered evidence. If the data doesn't support them, report what's missing.
- The findings contradict a stakeholder belief: present the evidence plainly; that tension is the finding.
- Asked to soften a finding: keep the evidence intact. Wording can change; participant counts can't.

## Output format

Save as `synthesis-[study].md`:

```markdown
# Synthesis: [Study question]

## Method & Data
[Sources, participant count, segments, limitations]

## Themes
[Per theme: statement, confidence grade, participant count, verbatim quotes with refs, disconfirming evidence]

## Insight Nuggets
| ID | Observation | Evidence refs | Tags | Confidence |

## Personas / JTBD (when supported)
[Clusters with the behavioral evidence behind each]

## What This Data Can't Answer
[Open questions and suggested next study]
```

## Checklist

- [ ] The study question is stated
- [ ] Participants are anonymized as IDs
- [ ] Every theme has a participant count, verbatim quotes with references, and a confidence grade
- [ ] Disconfirming evidence is counted in for each theme
- [ ] Reported and observed behavior are separated
- [ ] Personas exist only where clusters support them
- [ ] The report names what the data can't answer

## Composition / References

- The `design-ux-review` skill covers heuristic evaluation of an interface; this skill covers evidence from people.
- Sources: Hennink and Kaiser (2022) on saturation, Nielsen Norman Group sample-size guidance, MeasuringU on SUS.
