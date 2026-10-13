---
name: octomind-workflow
title: "Octomind Workflow Design & Syntax"
description: "Guide for octomind workflow files: pipeline design (pattern selection, step decomposition, sentinel handoff contracts, loop convergence, context economics) plus the exact TOML syntax for the external orchestrator that chains octomind run subprocesses. Covers sequential, parallel (static, count, dynamic fan-out), loop, conditional, and graph-routed steps, variable substitution, session modes, pre-flight validation, tap workflows, and the CLI. Activate when designing, authoring, validating, or debugging a workflow .toml file."
license: Apache-2.0
compatibility: "Requires: octomind CLI with the `workflow` subcommand. Workflows are stdin-driven; every referenced role must be an installed role or tap-agent tag."
domains: octomind
rules:
  - content(workflow)
  - file(*workflow*.toml)
  - grep(\[\[steps\]\], *.toml)
---

## Overview

`octomind workflow <file.toml|name>` is an external orchestrator: it chains `octomind run --format jsonl` subprocesses into a multi-step pipeline, passing outputs between steps by name. This skill covers how to design a pipeline that is efficient and reliable, and the exact TOML syntax. It applies to any domain.

## Mental model

A workflow is a predefined code path: you fix the steps at authoring time and the orchestrator executes them deterministically. If you cannot enumerate the steps in advance, use a single agent run instead.

Each step starts with a fresh context and knows only what its prompt template passes in — no drift, but also no implicit memory. Every step name becomes a `{{name}}` variable holding that step's full output; `{{input}}` is stdin.

```
stdin ─► octomind workflow file.toml
            ├─ per step → octomind run --format jsonl (subprocess)
            ├─ stderr: each step's reply, progress, cost, tokens, totals
            └─ stdout: empty, or JSONL events with --format jsonl
```

## Designing the workflow

### Pattern selection

Use the fewest steps that work. Every handoff is lossy, so the burden of proof is on adding a step.

| Task shape | Pattern | Primitive |
|------------|---------|-----------|
| Fixed subtasks, each easier than the whole | Prompt chaining | Sequential |
| Distinct input categories, accurate classifier | Routing | Conditional or graph edges |
| Independent subtasks known upfront | Sectioning | Parallel |
| Same task, diverse perspectives | Voting | Parallel + aggregator |
| N similar items produced by an earlier step | Fan-out | Dynamic parallel (`source` + `match`) |
| Output improves against clear criteria | Evaluator-optimizer | Loop |
| Cycles or multi-way routing | State machine | Graph mode |
| Subtasks unknowable before runtime | Orchestrator-workers | Not a workflow — single agent run |

### When to split a step

Split only when a different persona, a different model, a gate on the intermediate output, independent verifiability, or parallel speedup demands it. For every boundary, name the artifact that crosses it in one sentence; if it is "the same content, slightly transformed", merge the steps.

### Handoff contracts

Step output is an API. End every prompt with "Output only the <artifact> — no preamble." Gates match substrings or regexes, so the emitting step must produce a machine-checkable sentinel:

- Key:value tokens, never bare words: `VERDICT: APPROVED`, not `APPROVED`.
- Both outcomes as distinct positive tokens (`VERDICT: APPROVED` / `VERDICT: REVISE`); never define one as the absence of the other.
- Demand the exact last line in the emitting prompt and anchor with `matches = '(?m)^VERDICT: APPROVED'` when precision matters.
- Test the gate against a known-good output (must match) and a known-bad one (must not).

### Loops that converge

- `max_iterations` 2–3; worst-case cost is iterations × calls per iteration.
- The critic gets a finite rubric and a binary verdict on the last line, and is told to approve when every rubric item passes.
- With `session = "continue"`, iteration 2+ replaces the templated prompt with the most recent prior step's raw output, so the critique reaches the reviser while the session keeps its original instructions.
- Hitting `max_iterations` exits with the last outputs and a warning; the workflow continues. Gate on the verdict afterwards if an unapproved artifact must not ship.

### Context and cost

- Pass only the variables a step needs — usually the immediate predecessor.
- Summarize evidence, never artifacts that must be reproduced verbatim.
- In long prompts put data first, instructions last: `<input>{{prev}}</input>` then the task.
- Per-step `model`: cheap models for extraction, routing, formatting; strong ones for generation and evaluation. Set `max_cost` to bound runaway spend.

## File format

```toml
name        = "my-workflow"        # required
description = "Optional description"
# max_cost  = 2.5                  # USD cap, checked between steps

[[steps]]                          # sequential (default kind)
name    = "outline"                # unique across the file
role    = "demo:writer"            # installed role or tap tag (placeholder shown)
prompt  = """
{{input}}

Produce a structured outline. Output only the outline.
"""
session = "fresh"                  # "fresh" (default) | "continue"
timeout = 0                        # seconds, 0 = none
retries = 0                        # extra attempts on failure
# model = "<provider>:<model>"     # forwarded as --model
# workdir = "path"                 # resolved against the orchestrator cwd at run time
# skills = ["skill-name"]          # forwarded as OCTOMIND_SKILLS
# capabilities = ["websearch"]     # forwarded as OCTOMIND_CAPABILITIES
```

Unknown keys are ignored silently, so check spelling against this reference.

## Step types

A `[[steps]]` table is sequential unless it sets exactly one of `parallel`, `loop`, or `conditional` to `true`.

| Kind | Required | Behaviour |
|------|----------|-----------|
| Sequential | `name`, `role`, `prompt` | One `octomind run` |
| Parallel | `name`, ≥2 `[[steps.run]]` | Sub-steps run concurrently; the next step waits for all |
| Loop | `name`, ≥1 `[[steps.run]]`, `exit_when` | Sub-steps repeat until `exit_when` matches or `max_iterations` (default 10) |
| Conditional | `name`, `condition`, ≥1 `[[steps.run]]`, `on_match` and/or `on_no_match` | Runs the listed sub-steps; skipped ones resolve to empty strings |

Sub-steps accept the same optional fields as sequential steps. Parallel sub-steps cannot reference each other.

Parallel extras: `count = N` (N ≥ 2) on a sub-step replicates it; `max_parallel` caps concurrency; `min_success` (1..total replicas) relaxes the all-must-succeed default. Dynamic fan-out: exactly one template sub-step plus `source = "<earlier step>"` and `match = "<regex with one capture group>"`. Each match spawns a branch; inside it `{{<block name>}}` is that branch's captured item, and the accumulated output lands under the sub-step's name.

### Graph mode

Setting `entry = "<step>"` or any `[[edges]]` switches to explicit routing. Edges have `from`, `to`, and optional `when` (condition shape); the first matching conditional edge wins, and each node needs exactly one unconditional edge declared last. `max_transitions` (required) bounds total hops, and routing ends at `$end`. Every node must be reachable with a route to `$end`. Referencing an output that the current route never produced fails at run time.

### Condition shape

`exit_when`, `condition`, and edge `when` take `output` (step name, default the previous step), plus exactly one of `contains` (substring) or `matches` (Rust regex).

## Variables

- `{{input}}` — stdin; `{{step_name}}` — output of an earlier step. Names match `[A-Za-z_][A-Za-z0-9_-]*`; `input` and `$end` are reserved.
- Built-in placeholders also expand: `{{DATE}}`, `{{CWD}}`, `{{SHELL}}`, `{{OS}}`, `{{BINARIES}}`, `{{ROLE}}`, `{{SYSTEM}}`, `{{CONTEXT}}`, `{{GIT_STATUS}}`, `{{GIT_TREE}}`, `{{README}}`.
- A `<context>path</context>` or `<context>path:start:end</context>` block in a prompt is replaced with that file's contents.

## Validation rules

Checked before any step runs: valid TOML with at least one step; unique, non-empty step names; every `{{var}}` is a builtin, `input`, or an earlier step; parallel ≥2 sub-steps (or one template with `source`+`match`); loop has `exit_when`; conditional branches name existing sub-steps; regexes compile; `model`/`workdir` non-empty when set; `count` only on parallel sub-steps; `max_cost` positive; graph constraints above. Not checked: role existence for local files (a bad role fails when its subprocess spawns) and workdir existence.

Workflows fetched from a tap are additionally restricted to public `domain:spec` tap roles, so they stay portable.

## CLI

```bash
octomind workflow                                  # list tap workflows
octomind workflow myflow.toml --dry-run            # validate + print plan, no spawn, no stdin
echo "notes..." | octomind workflow myflow.toml    # run a local file
echo "..." | octomind workflow <name>              # run a tap workflow
echo "..." | octomind workflow myflow.toml --format jsonl   # assistant event per step + final cost event on stdout
```

An argument containing `/` or ending in `.toml` is a file; anything else is looked up in taps' `workflows/`. stdin is required and must be non-empty unless `--dry-run`. Without `--format jsonl` stdout is empty: each step's reply, progress, and the totals go to stderr. To consume the final result programmatically, use `--format jsonl` and take the last `assistant` event.

Inside a session: `/workflow <name> <input>` runs a tap workflow; agents with the `orchestration` capability can use `tap(action="workflow")`.

Retries rerun the whole step — keep `retries = 0` on steps whose role writes files or calls external APIs unless they are idempotent.

## Examples

### Generator ↔ critic loop with a sentinel contract

```toml
name = "report-with-review"

[[steps]]
name   = "draft"
role   = "demo:writer"
prompt = "<input>\n{{input}}\n</input>\n\nWrite the report. Output only the report."

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
Review against this rubric only: claims sourced; structure follows brief; no filler.
Critique failing items specifically. If every item passes, approve — do not invent criteria.

<report>
{{reviser}}
</report>

End with exactly one line: VERDICT: APPROVED or VERDICT: REVISE.
"""
```

Iteration 1 sends both templated prompts; from iteration 2 the `continue` rule feeds the critique to the reviser and the revision to the critic.

### Dynamic fan-out

```toml
name = "fan-out"

[[steps]]
name   = "plan"
role   = "demo:planner"
prompt = "List the sub-questions for: {{input}}\nOne per line as: Q: <question>"

[[steps]]
name         = "q"
parallel     = true
source       = "plan"
match        = '(?m)^Q: (.+)$'
max_parallel = 4

  [[steps.run]]
  name   = "answers"
  role   = "demo:researcher"
  prompt = "Answer concisely: {{q}}"
```

### Common mistake — forward reference

```toml
[[steps]]
name   = "outline"
role   = "demo:writer"
prompt = "Refine using {{review}}"   # review runs later → pre-flight error
```

## Checklist

- [ ] Could a single `octomind run` do this? Every step justified by a splitting gate?
- [ ] Handoff artifact nameable for every boundary; prompts end with "output only the artifact"?
- [ ] Every gate matches a key:value sentinel the emitting prompt demands on its last line?
- [ ] Loops bounded at 2–3 with a binary verdict and an approve-when-passing critic?
- [ ] Cheap vs strong `model` chosen per step; `max_cost` set for open-ended runs?
- [ ] Every role installed (`octomind complete run`) and each step tested standalone?
- [ ] `--dry-run` clean; result consumed via `--format jsonl` when scripted?

## References

- `octomind workflow <file.toml> --dry-run` — validate and inspect the resolved plan
- Octomind docs: `doc/usage/09-workflows.md`; `config-templates/workflow*.toml` in the octomind source
- [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — the patterns behind the design layer
