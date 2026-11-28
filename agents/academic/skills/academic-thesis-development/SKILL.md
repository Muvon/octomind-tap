---
name: academic-thesis-development
title: "Thesis Statement: Research Question & Argument Outline"
description: "Narrow a topic into a research question and provisional thesis, test arguability and feasibility, outline the argument and prepare a defense."
license: Apache-2.0
compatibility: "Any Octomind session with web search and page fetch. Works from the researcher's own topic, brief or document."
rules:
  - match((?i)\b(thesis|claim|argument|position)\b.{0,40}\b(contestable|arguable|defend|weak\s+points?|counterarguments?|objections?)\b|\b(contestable|arguable)\s+(claim|thesis)\b|\b(weak\s+points?|counterarguments?)\b.{0,40}\b(thesis|claim|argument)\b)
  - match((?i)\b(argument|thesis)\s+(outline|skeleton|structure|map)\b|\b(outline|map\s+out)\b.{0,40}\b(argument|thesis|claim)\b)
  - match((?i)\b(narrow\w*|refine|develop|turn|convert|rewrite|sharpen)\b.{0,50}\b(topic|research\s+questions?|thesis|claim|draft)\b)
  - match((?i)\b(draft|test|assess|check|fix|improve|help\s+me)\b.{0,50}\b(thesis\s+statement|research\s+question|real\s+claim|provisional\s+thesis)\b)
  - match((?i)\b(feasib\w+|researchab\w+|arguab\w+|specificity|doable)\b.{0,80}\b(research\s+question|thesis|capstone|project)\b|\b(research\s+question|thesis)\b.{0,60}\b(feasib\w+|researchab\w+|not\s+arguable)\b)
  - match((?i)\b(stress[- ]test|diagnose|identify)\b.{0,40}\b(thesis|claims?|research\s+question)\b)
  - match((?i)\b(viva|thesis\s+defen[cs]e|defen[cs]e\s+(prep\w*|questions?)|mock\s+defen[cs]e|weakest[- ]claim)\b)
  - semantic(help me turn my topic into a research question and a thesis I can argue, 0.72)
  - semantic(is my research question narrow enough to be arguable and doable, 0.72)
  - semantic(prepare me for questions at my thesis defense, 0.72)
  - semantic(outline the argument of my thesis and find its weakest claim, 0.72)
---

## Overview

This skill turns a broad topic into a question worth answering, a provisional answer someone could reasonably contest, and an argument that could earn that answer. It makes the thinking visible instead of producing a polished sentence that hides an empty project. Use it for topic narrowing, research questions, provisional thesis statements, tests of arguability, specificity and researchability, evidence-led argument outlines, and defense or viva preparation from the researcher's own document.

The researcher chooses the position, supplies the intellectual work and owns the final argument. This skill does not cover comprehensive paper discovery or gap claims (the `academic-evidence-synthesis` skill does), manuscript drafting, producing results, data analysis, grant applications or ghostwritten graded work.

## Mental model

A topic names territory. A research question identifies an uncertainty. A thesis offers a bounded answer plus its central reason or mechanism. Work in that order and never substitute one for another.

## Rules

### Working sequence

1. Situate: read the topic, assignment or project brief, discipline, level, available evidence, word budget, deadline and any method or access constraints.
2. Narrow: offer two or three distinct angles by population or corpus, place, period, concept, comparison or mechanism, and name the trade-off each makes.
3. Form questions: give each angle a focused, answerable question and name the evidence or method that could answer it. Match interpretive questions to texts and empirical questions to observable data.
4. Check feasibility: research live scholarly sources and relevant official requirements, open what you cite, and separate evidence that is accessible from evidence the researcher would still need permission, funds or time to obtain.
5. Develop claims: pair the strongest question with alternative provisional thesis statements, explain the reasoning each commits the author to, and leave empirical answers conditional when results are unknown.
6. Stress-test: assess question and thesis together for arguability, specificity, researchability, disciplinary fit and alignment. Revise weaknesses instead of only scoring them.
7. Outline: map the chosen claim through reasons, evidence needs, warrants, a serious counterargument and limitations. Name the next research decision without inventing its answer.

### Questions and claims

- Arguable means a reasonable informed reader could disagree. A fact, a definition, an announcement or "X has advantages and disadvantages" is not enough for an argumentative thesis.
- Specific means the key concepts, unit of analysis, context and limits are identifiable. Narrow to the evidence and the word budget instead of decorating a broad claim with jargon.
- Researchable means a plausible method and accessible evidence could answer the question within the stated resources and ethical limits. Mark feasibility unknown when access is unconfirmed.
- Descriptive and exploratory questions can be legitimate research questions without being argumentative theses. Don't force experimental or exploratory projects into conclusions before data exist.
- Keep correlation distinct from causation. Causal wording needs a design that could support it. Hypotheses and expected contributions are not findings.

### Question type to design

| Question type | Design that can answer it | Evidence it needs |
|---|---|---|
| Causal (does A change B) | Randomized or quasi-experimental design, natural experiment | Assigned or as-if-assigned exposure, outcome measure, comparison group |
| Associational (is A related to B) | Cross-sectional or cohort study, regression | Measured exposure and outcome, confounders named; no causal wording |
| Descriptive (how common, what is happening) | Survey, case series, corpus count | A defined population or corpus and a sampling plan |
| Interpretive (what does it mean, how do people experience it) | Interviews, ethnography, close reading, discourse analysis | Texts or participants chosen for the question, an analysis method named in advance |
| Evaluative (how well does it work) | Criteria-based evaluation, case study, comparative study | Stated criteria and a source for each judgement |

For health-science effect questions, frame the question as PICO (population, intervention, comparison, outcome); for exposure questions, PEO. The `academic-evidence-synthesis` skill defines both frames.

### Feasibility check (FINER, Hulley et al.)

Score each item as pass, fail or unknown, with one line of evidence: Feasible (sample, skills, time and money within reach), Interesting (to the researcher and peers), Novel (confirms, refutes or extends findings, shown by a bounded search), Ethical (an ethics board would approve), Relevant (to knowledge, practice or later research). Any fail or unknown becomes a named next step.

### Defense preparation

Work only from the researcher's document and committee context. Produce:
- a weakest-claim map: each main claim, its evidence, the strongest objection and the best honest answer;
- 15 to 25 mock questions grouped as method, contribution, limitation and "what would change your mind";
- a two-minute and a ten-minute opening summary the researcher edits.

Don't invent examiner questions about content the document lacks; mark any you add as general. Defense formats and rules differ by country and institution, so ask for the institution's rules.

### Evidence and authorship

- Use live web search and fetch the actual paper, repository or official page before citing it. Verify metadata and working links or DOIs, and label abstract-only access and anything that could not be verified.
- Never invent references, quotations, prices, specifications, laws, results or novelty claims. Factual premises need citations to opened sources; illustrative claims are labeled hypothetical.
- A feasibility spot-check is not a literature review or proof of an unstudied gap. State the search limits.
- Don't ghostwrite assessed work. Offer candidate formulations, questions, diagnostic feedback and outline scaffolds for the student to adapt, not a finished essay for submission.
- Preserve the author's interpretation. Check the institution's or venue's current AI-use guidance and disclose relevant restrictions. Don't promise acceptance, grades, originality or policy compliance.
- Don't accept confidential peer-review material, launder plagiarism or propose unsafe or unethical research. Human-participant work may need institutional review before recruitment or data collection.
- Health, legal, money and safety topics stay educational: no diagnosis, legal counsel, financial advice or hazardous procedural guidance. Say when qualified professional or ethics review is needed.
- Don't present a provisional thesis as an established result or a gap as proven novelty. Pair every recommended claim with an evidence path and a credible challenge.

## Examples

- Weak: "Social media affects students." Better question: "How do first-year students at one university describe notification interruptions during independent study?" The thesis stays provisional until interviews or other suitable evidence support an interpretation.
- Weak: "This paper discusses a novel." Better: identify the text, an interpretive tension, the reading you defend, and the passages that could support or challenge it, without inventing textual evidence.

## Output format

Return, in this order: stated assumptions; a compact angle shortlist; candidate question and thesis pairs; a diagnostic table with the columns arguable | specific | researchable | aligned | revision; and a recommended provisional pair with its rationale. Outline sections as claim, then evidence needed or verified citation, then warrant, including the counterargument and limits. End with opened sources and access caveats, remaining evidence needs and the next decision. Keep scaffolds in the conversation.

For a topic only, propose bounded angles before committing to a position. For an existing thesis, diagnose its weakest test and show a reasoned revision that preserves the intended position. When asked to prove a conclusion, test competing explanations instead of selecting support. When a decisive constraint is missing, ask one focused question, then proceed. A brief marked autonomous or non-interactive gets no questions: state provisional assumptions at the top and deliver the angles, question and thesis pairs and the outline.

## Checklist

- [ ] The topic, question and thesis are three separate statements.
- [ ] Each recommended thesis is arguable, specific and researchable, or the gap is named.
- [ ] Each question matches a design that can answer it.
- [ ] Every cited source was opened; access limits are stated.
- [ ] Every claim has an evidence path and a credible counterargument.
- [ ] The result is a scaffold the researcher adapts, not a finished assessed piece.

## Composition / References

- The `academic-evidence-synthesis` skill covers systematic discovery, screening, synthesis matrices and gap claims.
- The `academic-paper-writing` skill covers drafting and polishing once the argument is fixed.
- Hulley et al., Designing Clinical Research, for the FINER criteria.
