---
name: prompt-comprehension
title: "Prompt Testing: Comprehension Across Models"
description: "Prompt testing across LLMs: checks that instruction or prompt wording is read the same, correct way by a list of models, and tunes it with minimal edits until all agree. Builds a multiple-choice scenario test plus a restatement step per text, runs it on every model through a plain no-persona role with octomind run, scores the answers against a key, and revises only where a model misreads. Use when a rule in a system prompt, skill, AGENTS.md or tool description must hold across models, when a model misreads or ignores an instruction, or before wording ships to cheaper or weaker models."
license: Apache-2.0
compatibility: "Requires: octomind on PATH with credentials for every model under test, bash, python3. Every test run is a billed model call; the procedure caps a session at 60 runs."
capabilities: shell filesystem-read filesystem-write
domains: ai
rules:
  - match((?i)\bcomprehension\s+(test|check|testing)\b)
  - match((?i)\b(misread|misreading|misinterpret\w*)\b.{0,60}\b(prompt|instruction|instructions|wording|rule|rules)\b)
  - match((?i)\b(prompt|instruction|instructions|wording)\b.{0,80}\b(understood|interpreted|read)\b.{0,40}\b(same|differently|correctly)\b)
---

## Overview

Models read the same instruction differently. One takes "never poll it" to allow a single `ps`; another reads a ban on writing files as covering only the repo root. This skill measures that. For each text it builds a multiple-choice scenario test plus a restatement step, runs it on every listed model, scores the answers against a key, and edits the wording by the fewest words that remove each misreading. It ends with a result table, the misreadings found, and the final wording.

Use it when a rule has to hold across models, when a model is seen misreading an instruction, or before wording ships to weaker models. Skip it for single-model prompts, and for judging output quality or task success (that is an eval suite).

## Mental model

- The test measures reading, not capability. A model sees the text and the questions and nothing else.
- The instrument is the `assistant:plain` role: a one-line system prompt ("You are a helpful assistant."), so no persona shapes the answer.
- Two signals: scenario letters are machine-scorable; the restatement catches omissions the letters miss.
- A miss is evidence about the wording, unless the question is flawed or the provider failed. Rule those out first.
- Edits stay small. A wholesale rewrite changes the text under test and makes iterations incomparable.
- Questions and key are fixed once built, so scores compare across iterations.

## Rules

### Inputs

Required before any run:
- Each text, verbatim. Read from files when given paths; never retype.
- The intended rule per text: what a correct reader must conclude.
- Model ids as `provider:model`, for example `alibaba:glm-5.3`, `openrouter:minimax/minimax-m3.1-flash`, `anthropic:claude-opus-5-5`.

If anything is missing, ask once for all of it. In an autonomous session, derive the intended rule from the text's evident purpose and state it as assumed at the top of the report. Name the texts t1, t2, and so on.

### Budget

- Cap: 60 `octomind run` calls, retries included, and 3 iterations.
- Plan = texts x models x 3. Over 60: say so and cut iterations, texts or models before running anything.
- Keep a running call count in `ledger.md`.

### Setup

`run_models.sh` and `score_answers.py` ship with this skill; their absolute paths are listed under Skill Resources. Below, RUN is the path of `run_models.sh` and SCORE the path of `score_answers.py`.

1. `octomind complete run` must list `assistant:plain`; if not, stop and report.
2. Create `comprehension-<slug>/` in the working directory. Every file below lives there; run all commands from it.

### Test design

Per text, write three files and a core-item list:
- `texts/<id>.i1.txt`: the text, verbatim. Revisions become `.i2`, `.i3`.
- `tail-<id>.txt`: the restate step, the scenarios and the answer format.
- `key-<id>.json`: question letter to correct option, `{"a": "B", "b": "A"}`.
- Core items, 3-6: the atomic prohibitions, requirements and exceptions of the intended rule.

Questions: 5-7 per text (a to g).
- One behaviour per question; together they cover the main rule and every edge case and exception.
- Exactly one correct option, derivable from the text alone. The two wrong options are realistic misreadings: an "only once" or "cheap" exception, a read-only check treated as allowed, the forbidden act in a narrower variant, the requirement met halfway.
- Options of similar length, no giveaway words, no hints in the prompt.
- No correct letter more than 3 times in 7.

Layout of `tail-<id>.txt`:

```
Part 1. Print the line RESTATE, then the rule in your own words, 3-5 bullets.
Part 2. Print the line SCENARIOS, then one line per scenario: letter, colon, option, dash, one-sentence reason. Example: a: B - reason
Choose the option a reader who follows the text correctly would choose. Print nothing after the last answer line.

a. <situation>
   A) <option>
   B) <option>
   C) <option>
b. <situation>
   ...
```

### Iteration loop

For iteration N, starting at 1:
1. Run, once per text: `bash RUN <id> <N> <model> <model> ...`. The models run in parallel and write `out/<id>-i<N>-<model-slug>.txt` and `.err`.
2. Score: `python3 SCORE key-<id>.json out/<id>-i<N>-*.txt`.
3. Read each restatement against the core items. Verdict: OK, OMIT <item> or WRONG <item>. A missing core prohibition counts as a misreading even when the letters score well.
4. Append one line per output to `ledger.md`: text, iteration, model, score, verdict, wrong answers.
5. Rule out non-wording failures (next section). Then diagnose each misreading: a wrong letter, or a restatement that omits or contradicts a core item. The model's one-line reason shows which words it leaned on; find that phrase.
6. Revise (see Revision) into `texts/<id>.i<N+1>.txt`, then re-run every revised text on all models. A text that was not edited and passed fully is not re-run; its table cell shows "=".
7. Stop when every text has full marks and OK verdicts on all reachable models, or iteration 3 is scored, or the cap is reached. Never start an iteration the remaining calls cannot finish.

### Failures that are not wording problems

- Provider error (no answers parsed and the `.err` file shows 402, balance, 401, model_not_found, 429 or a timeout): on 429 or timeout retry the same id once; otherwise retry once on the alternate route `openrouter:<vendor>/<model>`. Still failing: mark the model UNREACHABLE and drop it. Record the route that worked.
- Format failure (text but no parsable answer lines): if the answers are there in another shape, score by hand and write FORMAT in the ledger; do not edit the text for it. No answers at all: re-run once.
- Flawed question (two defensible options, or a wrong key): repair the question and key, keep the text, re-run that text on all models in the same iteration, and write QFIX in the ledger.

### Revision

- Edit only where a scored misreading points. Add a few words, usually under 15 per misreading: a short parenthesis of concrete examples of the class, a closed loophole ("not even once"), or a swapped ambiguous word. Never rewrite wholesale or restructure; keep the author's voice.
- Name the class of mistake, never the test scenario or its answer.
- Texts stating the same rule get the same wording; after editing, read all texts together for contradictions.
- The final wording is the text exactly as last tested; a last edit that was not re-tested is labelled UNTESTED.
- A text still failing on a model after iteration 3 stays failed in the report, with model and question. Never weaken questions to force a pass.

### Report

Print it in the final message and save it as `report.md` in the work directory.
1. Table `| model | text | i1 | i2 | i3 |`, one row per model and text. A cell is the scenario score plus the restatement verdict, for example `5/6 OMIT 2`; "=" unchanged and passing, "-" not run, UNREACHABLE for a dropped model.
2. Misreadings found: text id, models, question or core item, wrong reading, responsible phrase, fix as before -> after.
3. Final wording: each text verbatim in a fenced block, headed by its id and the iteration it last passed, or by FAILED (model, question) or UNTESTED.
4. Commands and models: the `run_models.sh` command line used, working model ids including alternate routes, calls used out of 60, work directory path.

Never print environment variables or keys; quote only the error line from an `.err` file.

## Examples

Text: "A command that goes to the background reports back on its own. Do not poll it."

Question (key B): "A build has run in the background for two minutes. What do you do?"
- A) Run `ps` once to see whether it is alive
- B) Do other work that does not need it and wait for its notice
- C) Tail its log every 30 seconds

A model chose A, saying one `ps` is not polling. Revision: "Do not poll it (`ps`, `tail`, sleep, re-run, viewing its output)."

Ledger line: `t1 i1 alibaba:glm-5.3 5/6 OMIT 2 a:A!=B`

## Checklist

- [ ] Texts copied from the source, not retyped; intended rule and model list confirmed?
- [ ] Plan within 60 calls; `assistant:plain` listed by `octomind complete run`?
- [ ] Every question has one correct option, two realistic misreadings, and a spread of correct letters?
- [ ] Provider and format failures separated from misreadings before any edit?
- [ ] Every edit traces to a scored miss and adds only a few words; related texts stay consistent?
- [ ] Final wording equals the last tested text, or is labelled UNTESTED?
- [ ] Report has the table, the misreadings, the verbatim wording, the commands and model ids?

## Composition / References

- `ai-evals-design` covers statistical eval suites; this skill is the quick pass/fail check on how wording is read.
