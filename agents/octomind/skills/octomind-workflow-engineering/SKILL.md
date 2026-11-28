---
name: octomind-workflow-engineering
title: "Octomind Workflows: Design, Dry-Run, Tune"
description: "Build and run octomind workflow pipelines: pick step types, verify roles, dry-run before spending tokens, then tune cost and loops."
license: Apache-2.0
compatibility: "Requires: octomind binary on PATH and at least one runnable role. macOS/Linux/Windows."
capabilities: runtime
rules:
  - match((?i)\b(create|build|design|write|tune|debug|chain|fix|add|convert)\b.{0,40}\b(octomind\s+)?workflows?\b)
  - match((?i)\b(pipeline|workflow)\b.{0,50}\b(steps?|classif\w+|fan-?out|loop|sequential|parallel)\b|\b(steps?)\b.{0,50}\bpipeline\b|\bparallel\b.{0,30}\bsteps?\b)
  - match((?i)\boctomind\s+workflow\b|\b[\w-]+\.workflow\.toml\b|\b(workflows|pipelines)/[\w-]+\.toml\b|\b[\w-]+\.toml\b.{0,80}\b(steps?|dry-?run)\b)
  - match((?i)\bdry-?run\b|\bstep\s+(references?|wiring|failure)\b|\bexit\s+(condition|when)\b|\bexit_when\b|\bfan-?out\b|\bmax_iterations\b)
  - match((?i)\bper-step\b|\b(max_cost|timeout|retries)\b.{0,50}\b(step|pipeline|workflow)\b|\b(step|pipeline|workflow)\b.{0,50}\b(max_cost|timeout|retries)\b)
  - match((?i)\bjsonl\b.{0,60}\bsteps?\b|\bloop\b.{0,40}\b(never\s+stops?|re-?runn\w+|exit)\b)
  - semantic(chain several octomind runs into a pipeline and run it, 0.72)
  - semantic(write a workflow file with sequential and parallel steps, 0.72)
  - semantic(dry run this pipeline before spending tokens, 0.72)
  - semantic(add a loop step to my workflow and cap the cost, 0.72)
---

## Overview

A workflow chains independent `octomind run` subprocesses, driven by `octomind workflow <file.toml|name>`. Outputs flow between steps by name, each step's reply and the cost totals stream to stderr, and `--format jsonl` puts machine-readable step events on stdout. This skill is the operating procedure for building one: design the stages, wire existing roles to steps, validate before spending tokens, run it, and keep cost honest.

It adds the working method on top of the `octomind-workflow` skill, which holds the exact TOML field syntax and step options; load it before writing the file. Authoring the roles a workflow calls, and general install or config questions, are outside this skill.

## Mental model

Think in stages. Each step is one job for one role, with its own context. The dry run is free and the run is not, so every edit is followed by a dry run, and cost is read from the totals after each run.

## Rules

### Working sequence

1. Clarify the goal: what stages, what the final output should be, and what stdin will carry. Ask one question if the stage breakdown is ambiguous.
2. Discover roles. Never invent a role tag. `octomind complete run` prints every runnable tag (tap agents plus config roles), one per line; `octomind tap` lists only taps. Verify a role exists before wiring it.
3. Draft the file with the field syntax from the `octomind-workflow` skill. Use `{{input}}` for stdin and `{{step_name}}` for upstream outputs; never reference a step that runs later.
4. Dry-run: `octomind workflow file.toml --dry-run` validates structure and prints the resolved plan without spawning anything or reading stdin. Fix every error before running.
5. Run: `echo "<request>" | octomind workflow file.toml`. Watch stderr for each step's reply, progress, cost and token stats; the totals show where a pipeline runs hot. When a script needs the result, add `--format jsonl` and take the last `assistant` event from stdout; without it stdout is empty.
6. Tune: assign cheap models to utility steps (briefs, classifiers, routers), bound every loop with `max_iterations`, set `max_cost` for open-ended runs, and set `timeout` on steps that hit external dependencies.

### Step-type selection

| Need | Step type |
|------|-----------|
| One role, one pass | sequential (default) |
| Independent reviews or analyses at once | `parallel = true` (two or more sub-steps) |
| Generate, critique, fix until clean | `loop = true` with `exit_when` |
| Branch on a prior output | `conditional = true` with `condition` |
| One branch per item an earlier step listed | `parallel = true` with `source` and `match` (one capture group) |
| Cycles or multi-way routing | graph mode: `entry`, `[[edges]]`, `max_transitions` |

### Operating rules

- Dry-run before every run and after every edit: it catches unresolved variables, forward references and structural errors.
- Pre-flight does not check that roles exist for local workflow files (tap workflows are restricted to public tap roles); an unknown role fails only when its subprocess spawns. Confirm role tags during discovery.
- stdin is the only input. There is no `--var` injection. Empty stdin is a hard error.
- Use `session = "continue"` only inside loops where the generator and tester pattern needs accumulated context; on iteration 2 and later the prompt is automatically replaced with the prior step's raw output. Otherwise leave it `fresh`.
- Cost discipline: utility steps get cheap models through the per-step `model`; reserve strong models for the real work. Read the stderr totals after a run and report where the spend went.
- Keep each step's prompt focused: one job per step.
- Don't run a workflow before a clean dry run. Bound every loop with `max_iterations`; an unbounded loop burns tokens.

### Useful commands

- `octomind workflow file.toml --dry-run`: validate and inspect the plan.
- `octomind workflow`: list tap workflows.
- `octomind complete run`: list every runnable role tag.
- `echo ping | octomind run <role> --format plain`: confirm a role resolves and answers before wiring it.
- `octomind vars`: see resolved template placeholder values.

## Output format

Save workflow files as standalone, portable TOML, defaulting to `<name>.workflow.toml` in the working directory unless the user names a path. No edits to any role config or default are needed. After a dry run or run, report the resolved plan or the per-step cost and token totals from stderr.

A vague multi-stage goal gets the proposed step breakdown first, confirmed before writing. A brief marked autonomous or non-interactive skips the confirmation: write the proposed breakdown, dry-run it, and list assumptions with the result. When a step fails, read its stderr stats, isolate the failing step, dry-run the fix and re-run.

## Checklist

- [ ] Every role tag was verified with `octomind complete run`.
- [ ] No step references a step that runs later.
- [ ] A clean `--dry-run` precedes every run.
- [ ] Every loop has `max_iterations`; open-ended runs have `max_cost`.
- [ ] Utility steps use cheap models.
- [ ] The report states the plan or the cost totals per step.

## Composition / References

- The `octomind-workflow` skill holds the exact field syntax for every step type.
- The `octomind-cli` skill lists the `octomind workflow` flags.
