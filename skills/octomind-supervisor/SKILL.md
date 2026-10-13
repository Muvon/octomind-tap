---
name: octomind-supervisor
title: "Octomind Supervisor & Learning"
description: "Reference for octomind's out-of-band control plane: the self-report token, deterministic loop/no-progress/recovery detectors, the verify-gate on every turn stop, the supervisor-owned plan manager, condense, steer, recite, the optional tool authorizer, calibrated evaluation gates and hindsight, and cross-session lessons, orientation, and experience memory with optional evolution, together with the strict [supervisor] config sections. Activate when a user asks why a turn was re-run or gated, how the detectors work, why a tool call was blocked, how lessons are stored and recalled, why tool output was condensed, or how to tune any [supervisor.*] section."
license: Apache-2.0
compatibility: "Requires: octomind binary. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bsupervisor\b)
  - match((?i)\bverify.?gate\b)
  - match((?i)\[supervisor)
  - match((?i)\b(orientation memory|cross.session learning|condense|authorizer|hindsight)\b)
  - semantic(why did octomind re-run or gate my turn)
metadata:
  version: "1.1"
  tags: "octomind supervisor learning verify-gate condense"
---

## Overview

The supervisor is a control plane running beside the agent loop, never inside the transcript. It watches each turn, steers the agent off dead ends, verifies every stop before accepting it, manages the plan, narrows oversized tool output, and carries lessons and grounded knowledge across sessions.

Use this skill to explain supervisor behaviour a user observes and to tune the `[supervisor]` sections. The config is strict: the section and its mechanic tables must be present even when a mechanic is disabled.

## Mental model

Free signals gate expensive ones. Every turn produces two zero-cost signals — the agent's self-report and deterministic counters. A model call happens only at a turn stop, on an oversized tool round, on a plan signal, or (if enabled) before tool execution.

The verify-gate is the reward signal: a run counts as verified only when the turn changed state and a recognised check ran on the result. Learning credits only memories the agent reports as materially used.

Mid-trajectory everything is advisory: steering nudges, it never forces. The only blockers are the opt-in authorizer and project guardrails.

## Rules

### Self-report

With supervision on, the agent ends each response with a hidden structured status (`state`, `focus`, `next`, `carry`, plan signal, used memory ids). It is parsed and stripped before display. `focus`/`next`/`carry` feed compression as an attention hint, grounded against the transcript; credential values are forbidden in `carry`.

| State | Effect |
|-------|--------|
| `done` | Completion claim, checked by the verify-gate |
| `need_input` / `blocked` | Hand-back; the gate checks the blocker is genuine, otherwise sends the agent back |
| `exploring` / `progressing` | Fused with the counters |

### Detectors

Deterministic, free, fixed thresholds. Novelty compares the call target with its result, so a reworded call returning the same output is not new information, while a successful mutation always counts as progress.

- Loop — identical calls and results for 3 tool rounds without novelty.
- No-progress — 5 tool rounds without new receipts or successful mutations.
- Recovery — command executions keep failing with no later success for those calls.

All three only queue advisory steer notes. `done`, `blocked`, and `need_input` are left alone, and no-progress is suppressed while `exploring`. Repeated notes back off by doubling when the agent ignores them.

### Verify-gate

With `[supervisor.gate].enabled`, every stop of a user-owned turn — a `done` claim, a hand-back, or a turn ending without status — gets an independent model verification. Mutation and verification detectors supply context but cannot reject on their own; a saved artifact can satisfy an artifact request. Explicit user prohibitions on running checks are honoured: a forbidden check's absence is compliance.

- Pass — accepted; labelled verified only with execution evidence, otherwise unknown.
- Gaps — an advisory listing gaps is injected and the turn re-runs within a fixed budget; blocking findings first get a refutation pass.
- Indeterminate — transport failure or invalid protocol fails closed for the turn, recorded as unknown.

All supervisor calls use `[supervisor.model]` (inheriting `[model]`). There is no separate verifier model, so pointing `[supervisor.model]` at a different model family is the way to get an independent verifier.

### Plan manager

Planning is exceptional and supervisor-owned. The agent emits sparse `request`, `phase_complete`, or `reassess` signals; a separate call creates, advances, holds, or revises the plan. The agent has no plan tool; `/plan` displays it. Machine-checkable assumptions (e.g. `file_exists: src/foo.rs`) are monitored and a broken one triggers `reassess`.

### Steer and recite

Steer injects the advisory re-anchor note at the next safe point. Recite re-injects the live goal, plan, prohibitions, and verification policy near the request tail. Both are automatic.

### Condense

A plain-text tool result above `[supervisor.condense].tokens_threshold` (minimum 512) is a candidate. One call per round decides per candidate: fully relevant kept byte-for-byte; partly relevant reduced to line ranges reconstructed verbatim from the original; irrelevant replaced by a deterministic notice. The `mcp_response_tokens_threshold` prefix-cut runs first, so condense narrows only what the agent would have received. The narrowed body spills to a file whose path the result carries; condense runs only when the role has a local file-reading tool, only in the main session. `adaptive = true` lets a per-session multiplier move the threshold within 0.5x–2.0x.

### Authorizer (opt-in)

`[supervisor.authorizer] enabled = true` checks each pending tool batch against role instructions and user intent after native guards. Allow-first: only an independently confirmed conflict blocks, returned as a normal tool error. Judge failures allow the call.

### Evaluation gates and hindsight (opt-in)

`[supervisor.evaluate]` routes bounded yes/no questions at specific seams to a calibrated evaluation model (`model = "cloudflare:typesafe/jev"`, `typesafe:jev-latest`, or `octohub:auto`, keys from the environment). Each seam is one boolean, default `false`: `recall`, `skills`, `capabilities`, `authorizer`, `condense`, `compression`, `distill`, `plan`, `gate`, `evolution`. Any failure falls back to the pre-existing behaviour. `octomind evaluate` runs the same model by hand.

`[supervisor.hindsight]` (`enabled = false`, `model = "muvon/hindsight"`) is a local ONNX verifier that predicts whether the user's next turn will be a correction. Observe-only: scores are logged, shown, and tallied in `/info`.

### Lessons, orientation, and experience

All learning is file-backed under `<data_dir>/learning/`; there is no separate learning model.

- Lessons — short do/avoid rules from user corrections and stated rules, each carrying a verbatim user quote that a verifier must support. At most 3 per extraction. `scoped` (default) lives in `learning/{project}/{role_base}/` (role cut at the colon) and is recalled by relevance; `global` lives in `learning/_/` and is reconsidered every turn by importance.
- Orientation — grounded descriptive understanding, recalled as working assumptions to verify, never as truth.
- Experience — occasional longer records of non-obvious, hard-won knowledge with an outcome label and evidence handles.

Extraction runs after `/done`, at every auto-compaction fold, and at session end (a detached child). Each genuine user turn builds a fresh Active Memory Pack capped at 2,000 tokens (512 for global rules). Retention archives low-utility records to a cold store rather than deleting them; `/learning` lists, shows, deletes, and clears.

`[supervisor.learning.evolution]` (`enabled = false`) can compile recurring grounded memories into generated skills or guardrail candidates, promoted only after a randomized treatment-vs-control trial scored by verify-gate verdicts (`min_samples`, `noise_margin`, `cost_allowance`, `cost_per_gain`, `max_trial_uses`). It needs the gate enabled.

### Delegation

`tap(action="run")` and `agent_*` spawn a context-isolated child that sees only its prompt. The handoff must carry the goal, established facts, constraints, and expected deliverable. The child reports its measured outcome back; missing or failed handbacks count as unverified.

### Configuration

```toml
[supervisor]
enabled = true

[supervisor.model]            # optional overrides; omitted fields inherit [model]
name = "octohub:auto"
reasoning_effort = "medium"
max_tokens = 8192
temperature = 0.0

[supervisor.learning]
enabled = true

[supervisor.learning.evolution]
enabled = false

[supervisor.gate]
enabled = true

[supervisor.authorizer]
enabled = false

[supervisor.evaluate]
model = "cloudflare:typesafe/jev"
# recall, skills, capabilities, authorizer, condense,
# compression, distill, plan, gate, evolution = false

[supervisor.hindsight]
enabled = false
model = "muvon/hindsight"

[supervisor.plan]
enabled = true

[supervisor.condense]
enabled = true
adaptive = false
tokens_threshold = 5000
```

Detectors, steer, recite, and the detector thresholds have no configuration. Strictness asymmetry: the tables are required, but an omitted field inside them can take a code default — learning's `enabled` defaults to `false` in code and is on only because the template sets it.

## Examples

### Example 1: deleting a section to switch a mechanic off

❌ Bad: removing `[supervisor.condense]` entirely.

✅ Good:
```toml
[supervisor.condense]
enabled = false
adaptive = false
tokens_threshold = 5000
```

What changed: the table is required by the parser; `enabled` is the switch.

### Example 2: condense threshold above the hard ceiling

Keep `tokens_threshold` well below `mcp_response_tokens_threshold`. The prefix-cut runs first, so a higher threshold means nothing ever qualifies for condensing.

### Example 3: "the agent keeps redoing the same thing"

That is the loop detector's territory. It fires on repeated identical calls and results and queues an advisory. Disabling the supervisor removes the note without fixing the repetition.

## Checklist

- [ ] Every `[supervisor.*]` table present — mechanics switched off with `enabled`, not by deleting sections?
- [ ] Supervisor model set in `[supervisor.model]` (no per-mechanic or verifier model keys)?
- [ ] `[supervisor.condense].tokens_threshold` comfortably below `mcp_response_tokens_threshold`?
- [ ] Evolution enabled only together with the gate?
- [ ] Delegation prompts carry full context, since the child sees only the prompt string?
- [ ] Behaviour attributed to the right mechanic before recommending a config change?

## Composition / References

- Pairs with `octomind-config` for every non-supervisor section of `config.toml`.
- Pairs with `octomind-cli` for `/done`, `/plan`, `/learning`, and `octomind evaluate`.
- Octomind docs: `doc/usage/14-supervisor.md`, `doc/usage/13-learning.md`, `doc/reference/03-config-reference.md`
