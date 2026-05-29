---
name: octomind-workflow
title: "Octomind Workflow Syntax"
description: "Complete syntax reference for octomind workflow files — the external orchestrator that chains octomind run subprocesses. Covers the TOML format, sequential/parallel/loop/conditional step types, variable substitution, session modes, pre-flight validation rules, and the CLI. Activate when authoring, validating, or debugging a workflow .toml file."
license: Apache-2.0
compatibility: "Requires: octomind CLI with the `workflow` subcommand. Workflows are stdin-driven; every referenced role must be an installed role or tap-agent tag."
domains: octomind
rules:
  - content(workflow)
  - file(*workflow*.toml)
  - grep(\[\[steps\]\], *.toml)
---

## Overview

`octomind workflow <file.toml>` is an external orchestrator: it chains multiple `octomind run` invocations into a multi-step pipeline. Each step is an independent subprocess running `octomind run --format jsonl`; outputs flow between steps by name; the final step's output goes to stdout, so workflows compose with shell pipes. This skill is the exact TOML syntax for that file.

Workflows sit above sessions: orchestration lives entirely in this external file, not in any role or config. The former in-session `[[workflows]]` config block and `/workflow` command were removed — `octomind workflow <file.toml>` is the only orchestrator now.

## Mental model

A workflow file is a list of named steps executed top to bottom. A step either runs a role once (sequential), or groups sub-steps that run concurrently (parallel), repeatedly (loop), or by a branch test (conditional). Every step name becomes a `{{name}}` variable holding that step's full text output, available to any later step. `{{input}}` holds the raw stdin. Forward references are rejected before anything runs.

The runtime data flow:

```
stdin ─► octomind workflow file.toml ─► stdout (final step output)
            │  per-step → octomind run --format jsonl (subprocess)
            └─ stderr: per-step progress, cost, tokens, totals
```

## File format

```toml
name        = "my-workflow"        # required
description = "Optional human description"

[[steps]]                          # sequential (the default kind)
name    = "spec"                   # required, unique across the whole file
role    = "developer:general"      # required: installed role or tap-agent tag
prompt  = """
{{input}}

Write a tight implementation spec.
"""                                # required
session = "fresh"                  # "fresh" (default) | "continue"
timeout = 0                        # seconds; 0 = no timeout (default)
retries = 0                        # extra attempts on failure (default 0)
# model = "anthropic:claude-sonnet-4-6"  # optional per-step model override
```

## Step types

A `[[steps]]` table is sequential unless it sets exactly one of `parallel`, `loop`, or `conditional` to `true`. Setting more than one is a hard error.

| Kind | Flag | Required fields | Behaviour |
|------|------|-----------------|-----------|
| Sequential | (none) | `name`, `role`, `prompt` | Runs `octomind run` once with the resolved prompt. |
| Parallel | `parallel = true` | `name`, ≥2 `[[steps.run]]` | Sub-steps run concurrently; next top-level step waits for all. |
| Loop | `loop = true` | `name`, ≥1 `[[steps.run]]`, `exit_when` | Sub-steps run sequentially each iteration until `exit_when` matches or `max_iterations` hit. |
| Conditional | `conditional = true` | `name`, `condition`, ≥1 `[[steps.run]]`, `on_match`/`on_no_match` | Branch: run the sub-step names listed by the matching branch. |

Sub-steps inside `[[steps.run]]` are sequential steps and accept all the same optional fields (`session`, `timeout`, `retries`, `model`).

### Parallel

```toml
[[steps]]
name     = "review"
parallel = true

  [[steps.run]]
  name   = "security"
  role   = "security:owasp"
  prompt = "Security review of:\n{{spec}}"

  [[steps.run]]
  name   = "performance"
  role   = "developer:general"
  prompt = "Performance review of:\n{{spec}}"
```

Sub-steps cannot reference each other — only outer scope. The next top-level step starts after every sub-step completes.

### Loop

```toml
[[steps]]
name           = "refine"
loop           = true
max_iterations = 3                                       # default 10
exit_when      = { output = "tester", contains = "NO ISSUES" }

  [[steps.run]]
  name    = "developer"
  role    = "developer:general"
  session = "continue"
  prompt  = "Implement:\n{{spec}}"

  [[steps.run]]
  name    = "tester"
  role    = "developer:brief"
  session = "continue"
  prompt  = "Verify against spec:\n{{spec}}\n\nCode:\n{{developer}}"
```

`exit_when` is checked between iterations against a named step's output. Omit `output` to test the most recent step. If `max_iterations` is reached without matching, the loop exits with the last iteration's outputs and a stderr warning — the workflow does not fail.

### Conditional

```toml
[[steps]]
name        = "route"
conditional = true
condition   = { output = "spec", contains = "security" }
on_match    = ["deep-dive"]
on_no_match = ["quick-summary"]

  [[steps.run]]
  name   = "deep-dive"
  role   = "security:owasp"
  prompt = "Deep analysis:\n{{spec}}"

  [[steps.run]]
  name   = "quick-summary"
  role   = "developer:general"
  prompt = "One-line summary:\n{{spec}}"
```

`on_match` / `on_no_match` list sub-step names to run. Skipped sub-steps resolve to empty strings in later substitutions.

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

Variable names match `[A-Za-z_][A-Za-z0-9_-]*`. A `{{var}}` referencing a step that has not completed before this prompt is a pre-flight error. `input` is reserved and cannot be a step name.

## Session modes

| Mode | Behaviour |
|------|-----------|
| `fresh` (default) | Brand-new session every invocation; no state persists. |
| `continue` | First run sends the templated prompt and remembers the session ID. Subsequent runs (loop iter 2+, or a retry) resume that session — `/done` compresses prior context first, and the templated prompt is replaced with the most recent prior step's raw output. |

The continue-session prompt-replacement rule is what makes the generator↔tester loop work without re-feeding the whole spec each iteration. Each step owns its own session ID; in a loop, `developer` and `tester` accumulate independent histories. The session is ephemeral to a single `octomind workflow` invocation.

## Validation rules

All checked before any step runs (hard-fail):

- File exists and is valid TOML; workflow has at least one step.
- Step names are unique across the whole file, including all sub-steps; non-empty; none named `input`.
- Every `{{var}}` references `input` or a step that completes before the referencing step.
- Parallel: ≥2 sub-steps. Loop: ≥1 sub-step and an `exit_when` with `contains` or `matches`. Conditional: a `condition` with `contains` or `matches`, plus `on_match` and/or `on_no_match` whose names all exist among the block's sub-steps.
- `matches` regexes compile; `exit_when.output` / `condition.output` reference known steps.
- `model`, when set on any step, is non-empty.

Role existence is not checked at pre-flight — an unknown role fails when its subprocess spawns. Verify roles exist before running.

## CLI

```bash
echo "build a JSON-to-CSV CLI in Rust" | octomind workflow myflow.toml   # run
octomind workflow myflow.toml --dry-run                                  # validate + print plan, no spawn, no stdin
```

stdin is required unless `--dry-run`; empty stdin is a hard error. stderr carries each step's assistant message, progress lines, per-step cost/token stats, and the final total. `--dry-run` validates the file, resolves the execution graph, and prints the plan without spawning subprocesses or reading stdin.

## Out of scope

Not supported — use shell composition or call `octomind run` directly: `--var key=value` injection (stdin is the only input), workflow definitions inside `default.toml`, named-workflow lookup (explicit path only), cross-invocation `continue`-session persistence, step artifacts on disk, structured JSON output from the workflow command.

## Examples

### Generator/tester GAN

```toml
name = "gan"

[[steps]]
name   = "spec"
role   = "developer:general"
prompt = "User request:\n{{input}}\n\nWrite an implementation spec."

[[steps]]
name           = "refine"
loop           = true
max_iterations = 3
exit_when      = { output = "tester", contains = "NO ISSUES" }

  [[steps.run]]
  name    = "developer"
  role    = "developer:general"
  session = "continue"
  prompt  = "Implement:\n{{spec}}"

  [[steps.run]]
  name    = "tester"
  role    = "developer:brief"
  session = "continue"
  prompt  = "Verify against spec:\n{{spec}}\n\nImplementation:\n{{developer}}"

[[steps]]
name   = "evaluator"
role   = "developer:general"
prompt = """
Score 1-10:
Spec: {{spec}}
Code: {{developer}}
Verdict: {{tester}}

SCORE: <n>/10
"""
```

### Common mistake — forward reference

```toml
# WRONG: spec references {{review}}, which runs later → pre-flight error
[[steps]]
name   = "spec"
role   = "developer:general"
prompt = "Refine using {{review}}"   # {{review}} not yet available

[[steps]]
name   = "review"
role   = "developer:brief"
prompt = "Review {{spec}}"
```

## Checklist

- [ ] `name` set at top level; every step `name` unique across the whole file; none named `input`?
- [ ] Each sequential step (and sub-step) has `role` and `prompt`?
- [ ] Each `{{var}}` is `input` or a step that completes earlier (no forward refs)?
- [ ] Parallel has ≥2 sub-steps; loop has `exit_when` + `max_iterations`; conditional branch names all exist?
- [ ] `contains` or `matches` set on every `exit_when` / `condition`; regexes compile?
- [ ] Loops bounded by `max_iterations`; long-running steps have a `timeout`?
- [ ] Every referenced role is installed (pre-flight does not check this)?
- [ ] `octomind workflow file.toml --dry-run` prints the expected plan with no errors?

## References

- `octomind workflow <file.toml> --dry-run` — validate and inspect the resolved plan
- Octomind docs: workflows usage guide (`doc/usage/09-workflows.md` in the octomind source)
