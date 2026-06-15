---
name: octomind-workflow
title: "Octomind Workflow Design & Syntax"
description: "Complete guide for octomind workflow files — pipeline design (pattern selection, step decomposition, sentinel handoff contracts, loop convergence, context economics) plus the exact TOML syntax for the external orchestrator that chains octomind run subprocesses. Covers sequential/parallel/loop/conditional steps, parallel fan-out (count/min_success/max_parallel) and dynamic match fan-out, variable substitution, session modes, pre-flight validation, and the CLI. Activate when designing, authoring, validating, or debugging a workflow .toml file."
license: Apache-2.0
compatibility: "Requires: octomind CLI with the `workflow` subcommand. Workflows are stdin-driven; every referenced role must be an installed role or tap-agent tag."
domains: octomind
rules:
  - content(workflow)
  - file(*workflow*.toml)
  - grep(\[\[steps\]\], *.toml)
---

## Overview

`octomind workflow <file.toml>` is an external orchestrator: it chains multiple `octomind run` invocations into a multi-step pipeline. Each step is an independent subprocess running `octomind run --format jsonl`; outputs flow between steps by name. Human-facing per-step output and progress go to **stderr**; **stdout** is the machine channel — empty by default, or one JSON Line per step (the last is the final result) with `--format jsonl` (see [CLI](#cli)). This skill covers both halves of authoring one: how to design the pipeline so it does an efficient, reliable job, and the exact TOML syntax. It applies to any task domain — content, research, review, code, operations.

## Mental model

A workflow is a predefined code path: you decide the steps in advance, the orchestrator executes them deterministically. This is the opposite of an agent dynamically directing its own process — if you cannot enumerate the steps at authoring time, a workflow is the wrong tool; use a single agent run instead.

A workflow file is a list of named steps executed top to bottom. A step either runs a role once (sequential), or groups sub-steps that run concurrently (parallel), repeatedly (loop), or by a branch test (conditional). Every step name becomes a `{{name}}` variable holding that step's full text output, available to any later step. `{{input}}` holds the raw stdin. Forward references are rejected before anything runs.

Each step starts with a fresh context. That is the architecture's strength — no accumulated drift, the critic never sees the generator's reasoning — and its obligation: a step knows only what its prompt template passes in. Orchestration lives entirely in this external file, not in any role or config (the former in-session `[[workflows]]` block and `/workflow` command were removed).

The runtime data flow:

```
stdin ─► octomind workflow file.toml
            │  per-step → octomind run --format jsonl (subprocess)
            ├─ stderr: per-step responses + progress, cost, tokens, totals (human)
            └─ stdout: empty by default · JSONL events with --format jsonl (machine)
```

## Designing the workflow

### Pattern selection

Start from the task shape, not from the syntax. Use the fewest steps that work — a one-step workflow is legitimate, and a single `octomind run` with a good role is often enough. Success probability decays with step count (every handoff is lossy), so the burden of proof is on adding a step, never on omitting it.

| Task shape | Pattern | Primitive |
|------------|---------|-----------|
| Cleanly decomposes into fixed subtasks, each easier than the whole | Prompt chaining | Sequential steps |
| Distinct input categories handled better separately, and classification is accurate | Routing | Conditional |
| Independent subtasks, knowable upfront, no shared output | Parallelization: sectioning | Parallel |
| Same task needs diverse perspectives or higher confidence | Parallelization: voting | Parallel (`count` for best-of-N of one role) + aggregator step |
| Output improves measurably against clear criteria via iteration | Evaluator-optimizer | Loop |
| A prior step emits a list; the same task runs once per item, item count unknown until runtime | Dynamic fan-out (map) | Parallel with `match` |
| Each runtime subtask needs a *different* task or role, decided at runtime | Orchestrator-workers (heterogeneous) | Not supported — use a single agent run |

Routing has a precondition: it only pays off when the classifier step is reliably accurate. A router that misclassifies a meaningful share of inputs is worse than one general prompt.

### When to split a step

Split work into a separate step only when at least one gate holds:

1. A different persona genuinely changes behavior (critic vs author, domain expert vs formatter) — not just a different paragraph of the same instructions.
2. A different model is warranted (cheap extraction vs expensive reasoning).
3. You need a gate there — a conditional or loop exit must inspect this intermediate output.
4. The output is independently verifiable (against a rubric, a pattern, source material) in a way the merged output wouldn't be.
5. The parts are independent and fan-out saves wall-clock time.

The handoff-artifact test: for every boundary, name the artifact that crosses it in one sentence ("an outline", "a list of extracted claims", "a verdict + critique"). If the honest answer is "the same content, slightly transformed", merge the steps. Steps that only reformat the previous output belong inside the producing step's prompt.

### Handoff contracts

Step stdout is an API, not a chat. Every step's prompt ends by stating that the output IS the artifact: "Output only the report — no preamble, no commentary." A step that explains its choices pollutes `{{step}}` for everything downstream.

Gates (`exit_when`, `condition`) match substrings or regexes, so the emitting step must produce a machine-checkable sentinel:

- Use a key:value token, never a bare word: `VERDICT: APPROVED`, not `APPROVED` (bare words false-positive on prose like "cannot be approved").
- Make both outcomes distinct positive tokens — `VERDICT: APPROVED` / `VERDICT: REVISE` — and match the gate on the positive one. Never define an outcome as absence or negation ("NOT APPROVED" contains "APPROVED").
- Demand the exact line in the emitting prompt, last line, stated explicitly: "End with exactly one line: `VERDICT: APPROVED` or `VERDICT: REVISE`. Nothing after it."
- Routers emit one token from a closed set enumerated verbatim in their prompt: "Output exactly one line: `CATEGORY: BILLING` or `CATEGORY: TECHNICAL`."
- When precision matters, anchor with a regex: `matches = '(?m)^VERDICT: APPROVED'` instead of `contains`.
- Test the contract both ways: run the gate's regex against a captured known-bad output (must not match) and a known-good one (must match). A sentinel tested only on the happy path is untested.

### Loops that converge

The evaluator-optimizer loop (generator ↔ critic) needs explicit convergence design or it runs to `max_iterations` every time:

- Keep `max_iterations` at 2–3. Iterations beyond that rarely improve output and double cost; worst-case loop cost = iterations × calls-per-iteration.
- The critic gets a finite rubric and a binary verdict — critique first (specific, referencing concrete failures), verdict as the last line. No 1–5 scores: they are uncalibrated and unmatchable by a substring gate.
- Tell the critic to approve: "If every rubric item passes, emit VERDICT: APPROVED — do not invent new criteria." Without this, the critic always finds something and the loop never exits.
- The generator must receive the critique, not just "try again". With `session = "continue"`, iteration 2+ replaces the templated prompt with the most recent prior step's raw output — the critique flows in automatically while the session retains the original instructions. Put rubric and format instructions in the templated prompt (sent on iteration 1); later iterations rely on session memory.
- A loop that hits `max_iterations` exits with the last iteration's outputs and a warning — the workflow continues. Design downstream steps to tolerate an unapproved artifact, or gate on the verdict with a conditional after the loop.

### Parallel: sectioning vs voting

Sectioning runs independent subtasks concurrently (per-aspect analysis, per-source research). Sections must be knowable at authoring time and must not need each other's output — if branch B would benefit from branch A's result, it's a chain, not a fan-out.

Voting runs the same input through diverse roles for confidence. Use an odd branch count and a mechanical aggregator step: "Output the verdict that appears in at least 2 of the 3 reviews." The aggregator's prompt deserves as much care as the branches — a sloppy synthesizer throws away the fan-out's value.

### Fan-out controls and dynamic match

Three optional fields tune a parallel block:

- `count = N` on a single sub-step runs it N times unchanged (same role/model/prompt) — best-of-N sampling for voting, cheaper to write than copy-pasting the branch; the model's non-determinism supplies the diversity. The N outputs accumulate under the sub-step's name.
- `min_success = M` lets the block pass when only M of its replicas succeed — tolerance for a flaky branch (a web search that 502s, a model that times out). Omit for strict (all must succeed).
- `max_parallel = K` caps concurrency via a semaphore; replicas beyond K queue. Use it to respect API rate limits or bound peak spend when the branch count is large.

When the number of branches is not knowable at authoring time — a planner step emits a list and you want one branch per item — add a `match` regex to the parallel block. This is the **bounded** orchestrator-workers pattern: the *same* task template maps over a runtime-sized list (not heterogeneous dispatch).

- `match` is a regex over the **previous step's output**; each match is one branch. Capture group 1 is the item text (the regex must define one).
- The block holds **exactly one** sub-step — the per-item template.
- The block's own name is the **loop variable**: inside the template `{{<block-name>}}` is *this branch's one item*. The accumulated output of all branches lands under the **sub-step's name** — that is what a later step reads. (Referencing the block name downstream is a pre-flight error; it is loop-scoped.)
- Branch count is unknown until runtime, so bound spend with the top-level `max_cost` and concurrency with `max_parallel`; `min_success` here is an absolute count.

The planner's contract matters as much as a gate's: tell it to emit each item wrapped in an exact delimiter the `match` regex targets — e.g. "wrap each task in `<task>…</task>`" paired with `match = "(?s)<task>(.*?)</task>"`.

### Context and cost

- Pass only the variables a step needs. Default: the immediate predecessor's output. Interpolating `{{step1}} {{step2}} {{step3}}` everywhere "just in case" recreates context rot manually — model accuracy degrades as input grows, long before the window fills.
- Summarize evidence, never artifacts. A distillation step before a long input crosses into a reasoning step is high-signal compression; summarizing an artifact downstream steps must reproduce verbatim loses critical detail. Never chain two summarizations of the same content.
- In long step prompts, put data first, instructions last: `<input>{{prev}}</input>` then the task.
- Use per-step `model` overrides deliberately: a smaller, cheaper model for extraction, classification/routing, formatting, and summarization; the strong model for generation, synthesis, and evaluation.

### Anti-patterns

| Anti-pattern | Why it fails | Fix |
|--------------|--------------|-----|
| Step that only reformats the previous output | Extra call, extra drift | Fold formatting into the producing step |
| Habitual "polish" step at the end | Lossy compounding, no measurable gain | Add only with a rubric and a gate |
| Artifact + commentary in one output | Pollutes every downstream `{{var}}` | "Output only the artifact" |
| Bare-word or prose exit condition | False positives, loop never exits or exits early | Key:value sentinel, last line |
| Routing on shaky classification | Misroutes compound the error downstream | Route only with a reliable closed-set classifier |
| Validation only at the end | Garbage from step 2 gets elaborated, not fixed | Gate early steps; failures must trace to a step |

## File format

```toml
name        = "my-workflow"        # required
description = "Optional human description"

[[steps]]                          # sequential (the default kind)
name    = "outline"                # required, unique across the whole file
role    = "demo:writer"            # required: installed role or tap-agent tag (placeholder shown)
prompt  = """
{{input}}

Produce a structured outline. Output only the outline.
"""                                # required
session = "fresh"                  # "fresh" (default) | "continue"
timeout = 0                        # seconds; 0 = no timeout (default)
retries = 0                        # extra attempts on failure (default 0)
# model = "<provider>:<model>"     # optional per-step model override
# workdir = "path/to/dir"          # optional working directory; default = orchestrator cwd
```

Role tags in this skill are placeholders — substitute roles actually installed in your setup.

## Step types

A `[[steps]]` table is sequential unless it sets exactly one of `parallel`, `loop`, or `conditional` to `true`. Setting more than one is a hard error.

| Kind | Flag | Required fields | Behaviour |
|------|------|-----------------|-----------|
| Sequential | (none) | `name`, `role`, `prompt` | Runs `octomind run` once with the resolved prompt. |
| Parallel | `parallel = true` | `name`, ≥2 `[[steps.run]]` (or **exactly 1** + `match`) | Sub-steps run concurrently; next top-level step waits for all. With `match`, one branch runs per regex match of the previous step's output (dynamic fan-out). |
| Loop | `loop = true` | `name`, ≥1 `[[steps.run]]`, `exit_when` | Sub-steps run sequentially each iteration until `exit_when` matches or `max_iterations` hit. |
| Conditional | `conditional = true` | `name`, `condition`, ≥1 `[[steps.run]]`, `on_match`/`on_no_match` | Branch: run the sub-step names listed by the matching branch. |

Sub-steps inside `[[steps.run]]` are sequential steps and accept the same optional fields (`session`, `timeout`, `retries`, `model`, `workdir`). Parallel sub-steps cannot reference each other — only outer scope. Conditional `on_match` / `on_no_match` list sub-step names to run; skipped sub-steps resolve to empty strings in later substitutions. A loop that reaches `max_iterations` without matching exits with the last iteration's outputs and a stderr warning — the workflow does not fail.

### Parallel fan-out fields

On the parallel **block** table:

| Field | Default | Meaning |
|-------|---------|---------|
| `match` | _(none)_ | Regex over the previous step's output; one branch per match (capture group 1 = item). Presence ⇒ dynamic mode: exactly one sub-step, the per-item template. |
| `min_success` | _(all)_ | Minimum replicas that must succeed for the block to pass. 1..total replicas (an absolute count under `match`). |
| `max_parallel` | _(unbounded)_ | Max replicas running concurrently (semaphore). Must be ≥1. |

On a parallel **sub-step**:

| Field | Default | Meaning |
|-------|---------|---------|
| `count` | _(1)_ | Run this sub-step N times unchanged (best-of-N). Must be ≥2. Parallel sub-steps only; rejected elsewhere and on a `match` template (there the match count *is* the fan-out). |

**Aggregation.** After a parallel block: `{{<sub-step>}}` = that sub-step's output, with replicas (`count` or `match` items) joined under `── <label> ──` headers; `{{<block>}}` (static blocks) = every sub-step joined. Under `match` the block name is the loop variable, **not** an aggregate — read the sub-step name for the joined result. Failed replicas (under `min_success`) are skipped in the joins.

## Condition shape

`exit_when` and `condition` share one table shape:

| Key | Meaning |
|-----|---------|
| `output` | Step name whose output to test. Omit → most recent step's output. |
| `contains` | Substring match. |
| `matches` | Rust regex match. |

Exactly one of `contains` or `matches` must be set. Regex patterns must compile or pre-flight fails.

## Variable substitution

| Variable | Value |
|----------|-------|
| `{{input}}` | The raw stdin content. |
| `{{step_name}}` | Full text output of a previously completed step. |
| `{{parallel_block}}` | Static parallel block → every sub-step's output joined under `── name ──` headers. Under a `match` block this name is instead the per-branch loop variable (template-scoped; see [Parallel fan-out fields](#parallel-fan-out-fields)). |
| `{{fanned_substep}}` | A sub-step with `count`, or the single template of a `match` block, → all its replica/branch outputs joined. This is the name a step after a `match` block reads. |

Variable names match `[A-Za-z_][A-Za-z0-9_-]*`. A `{{var}}` referencing a step that has not completed before this prompt is a pre-flight error. `input` is reserved and cannot be a step name.

## Session modes

| Mode | Behaviour |
|------|-----------|
| `fresh` (default) | Brand-new session every invocation; no state persists. |
| `continue` | First run sends the templated prompt and remembers the session ID. Subsequent runs (loop iter 2+, or a retry) resume that session — `/done` compresses prior context first, and the templated prompt is replaced with the most recent prior step's raw output. |

The continue-session prompt-replacement rule is what makes the generator↔critic loop work without re-feeding instructions each iteration. Each step owns its own session ID; in a loop, sub-steps accumulate independent histories. The session is ephemeral to a single `octomind workflow` invocation.

## Working directory

Each step optionally sets `workdir` — the directory its subprocess runs in. Omitted → the orchestrator's cwd. Relative paths resolve against the orchestrator's cwd; resolution happens at execution time, so a directory created by an earlier step is legal, but a missing directory fails the step hard. The workdir determines the subprocess's project context (config, roles, `{{CWD}}`/`{{GIT_*}}` placeholders inside the role — note: workflow prompt placeholders still expand in the orchestrator's cwd). For `continue` sessions the `/done` compression runs in the same workdir as the step. Use it to point steps at different repos/projects from one workflow.

## Validation rules

All checked before any step runs (hard-fail):

- File exists and is valid TOML; workflow has at least one step.
- Step names are unique across the whole file, including all sub-steps; non-empty; none named `input`.
- Every `{{var}}` references `input` or a step that completes before the referencing step.
- Parallel: ≥2 sub-steps. Loop: ≥1 sub-step and an `exit_when` with `contains` or `matches`. Conditional: a `condition` with `contains` or `matches`, plus `on_match` and/or `on_no_match` whose names all exist among the block's sub-steps.
- Parallel fan-out: `count` only on parallel sub-steps and ≥2; `min_success` in range 1..total-replicas; `max_parallel` ≥1. A `match` block: its regex compiles, it has **exactly one** sub-step, is **not** the first step, and its template carries no `count`.
- `matches` regexes compile; `exit_when.output` / `condition.output` reference known steps.
- `model` and `workdir`, when set on any step, are non-empty. Workdir existence is checked at execution time, not pre-flight.

Role existence is not checked at pre-flight — an unknown role fails when its subprocess spawns. Verify roles exist, and test each step's prompt standalone via `octomind run`, before composing.

## CLI

```bash
echo "quarterly sales summary from the attached notes" | octomind workflow myflow.toml   # run
octomind workflow myflow.toml --dry-run                # validate + print plan, no spawn, no stdin
```

stdin is required unless `--dry-run`; empty stdin is a hard error. **stderr** carries each step's assistant message, progress lines, per-step cost/token stats, and the final total — the human view. **stdout** is the machine channel: nothing by default (a plain run is meant to be watched on stderr), or with `--format jsonl` one JSON `assistant` event per step as it completes (the last is the final result) plus a final aggregated `cost` event. `--dry-run` validates the file, resolves the execution graph, and prints the plan to stdout without spawning subprocesses or reading stdin.

Retries rerun the same step. Pure text-in/text-out steps are naturally safe to retry; steps whose role touches the outside world (writes files, calls APIs) are not — keep `retries = 0` there or make the role idempotent.

## Out of scope

Not supported — use shell composition or call `octomind run` directly: `--var key=value` injection (stdin is the only input), workflow definitions inside `default.toml`, named-workflow lookup (explicit path only), cross-invocation `continue`-session persistence, step artifacts on disk, and heterogeneous orchestrator-workers (a runtime-decided *different* task per worker — the same-task-per-item case IS supported, via `match`).

## Examples

### Generator ↔ critic loop with a sentinel contract

```toml
name = "report-with-review"

[[steps]]
name   = "draft"
role   = "demo:writer"
prompt = """
<input>
{{input}}
</input>

Write the report. Output only the report — no preamble, no commentary.
"""

[[steps]]
name           = "refine"
loop           = true
max_iterations = 3
exit_when      = { output = "critic", matches = '(?m)^VERDICT: APPROVED' }

  [[steps.run]]
  name    = "reviser"
  role    = "demo:writer"
  session = "continue"
  prompt  = "Improve this report:\n{{draft}}\n\nOutput only the report."

  [[steps.run]]
  name    = "critic"
  role    = "demo:critic"
  session = "continue"
  prompt  = """
Review the report against this rubric only: factual claims sourced; structure follows brief; no filler.
Critique each failing item with specifics. If every rubric item passes, emit the approval — do not invent new criteria.

<report>
{{reviser}}
</report>

End with exactly one line: VERDICT: APPROVED or VERDICT: REVISE. Nothing after it.
"""

[[steps]]
name   = "final"
role   = "demo:writer"
prompt = "Format this report for publication. Output only the formatted report:\n{{reviser}}"
```

Iteration 1 sends both templated prompts; from iteration 2 the `continue` rule feeds the critic's raw output (critique + verdict) to the reviser, and the revised report to the critic, while both sessions retain their original instructions.

### Closed-set routing

```toml
name = "triage"

[[steps]]
name   = "classify"
role   = "demo:triage"
prompt = "Classify this request. Output exactly one line: CATEGORY: BILLING or CATEGORY: TECHNICAL.\n\n{{input}}"

[[steps]]
name        = "route"
conditional = true
condition   = { output = "classify", contains = "CATEGORY: BILLING" }
on_match    = ["billing"]
on_no_match = ["technical"]

  [[steps.run]]
  name   = "billing"
  role   = "demo:billing"
  prompt = "Resolve this billing request:\n{{input}}"

  [[steps.run]]
  name   = "technical"
  role   = "demo:support"
  prompt = "Resolve this technical request:\n{{input}}"
```

### Dynamic fan-out — map a template over a runtime list

```toml
name = "research-map"

[[steps]]
name   = "plan"
role   = "demo:planner"
prompt = """
Break this into 3–7 independent sub-questions.
Output ONLY the sub-questions, each wrapped exactly as <task>…</task>:

{{input}}
"""

[[steps]]
name         = "research"                  # block name = the loop variable
parallel     = true
match        = "(?s)<task>(.*?)</task>"    # one branch per <task> item
max_parallel = 4
min_success  = 1

  [[steps.run]]
  name   = "researcher"                    # sub-step name = accumulated output
  role   = "demo:researcher"
  prompt = "Research this thoroughly. Output only findings:\n{{research}}"   # {{research}} = THIS branch's item

[[steps]]
name   = "summary"
role   = "demo:writer"
prompt = "Synthesize all findings into one report:\n\n{{researcher}}"   # every branch joined
```

`plan` emits the list; `match` splits it into one branch per `<task>`. Inside the template, `{{research}}` (the block name) is the single item for that branch; downstream, `{{researcher}}` (the sub-step name) is every branch's output joined. The two names are distinct on purpose — the block is the loop, the sub-step is the work. Bound the runtime-sized fan-out with `max_parallel` and the top-level `max_cost`.

### Common mistake — forward reference

```toml
# WRONG: outline references {{review}}, which runs later → pre-flight error
[[steps]]
name   = "outline"
role   = "demo:writer"
prompt = "Refine using {{review}}"   # {{review}} not yet available

[[steps]]
name   = "review"
role   = "demo:critic"
prompt = "Review {{outline}}"
```

## Checklist

Design:

- [ ] Could a single `octomind run` do this job? Every step justified by a splitting gate (persona, model, gate, verifiability, parallelism)?
- [ ] Can you name the handoff artifact for every step boundary in one sentence?
- [ ] Every step prompt ends with "output only the artifact" and passes only the variables it needs?
- [ ] Every gate matches a key:value sentinel that the emitting prompt demands on its last line, with both outcomes as positive tokens?
- [ ] Loops: `max_iterations` 2–3, binary verdict, finite rubric, critic instructed to approve when the rubric passes?
- [ ] Parallel branches independent of each other; voting uses an odd count plus a mechanical aggregator? Dynamic `match` block: planner emits an exact delimiter, template reads the block name, downstream reads the sub-step name, fan-out bounded by `max_cost`/`max_parallel`?
- [ ] Cheap vs strong `model` considered per step?

Syntax and testing:

- [ ] `name` set at top level; every step `name` unique; none named `input`; each sequential step has `role` and `prompt`?
- [ ] Each `{{var}}` is `input` or an earlier step (no forward refs)?
- [ ] `contains` or `matches` on every `exit_when`/`condition`; regexes compile; loops bounded; long-running steps have a `timeout`?
- [ ] Every referenced role is installed (pre-flight does not check this)?
- [ ] Steps with `workdir`: the directory exists by the time the step runs (pre-flight does not check this)?
- [ ] Each step tested standalone via `octomind run`; gate patterns tested against a known-bad output (no match) and a known-good one (match)?
- [ ] `octomind workflow file.toml --dry-run` prints the expected plan; one golden end-to-end run done, including the forced `max_iterations` path?

## References

- `octomind workflow <file.toml> --dry-run` — validate and inspect the resolved plan
- Octomind docs: workflows usage guide (`doc/usage/09-workflows.md` in the octomind source)
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the workflow patterns this skill's design layer is grounded in
