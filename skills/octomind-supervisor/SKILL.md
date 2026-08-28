---
name: octomind-supervisor
title: "Octomind Supervisor & Learning"
description: "Reference for octomind's out-of-band control plane: the self-report token, deterministic loop/no-progress/recovery detectors, the verify-gate and its free pre-gates, adaptive external planning, condense, steer, recite, and cross-session lessons plus orientation memory, together with the strict [supervisor] config sections. Activate when a user asks why a turn was re-run or gated, what the sup status line is, how lessons or orientation are stored and recalled, why tool output was condensed, or how to tune [supervisor.gate], [supervisor.learning], [supervisor.plan], or [supervisor.condense]."
license: Apache-2.0
compatibility: "Requires: octomind binary. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bsupervisor\b)
  - match((?i)\bverify.?gate\b)
  - match((?i)\[supervisor)
  - match((?i)\b(orientation memory|cross.session learning|condense)\b)
  - semantic(why did octomind re-run or gate my turn)
metadata:
  version: "1.0"
  tags: "octomind supervisor learning verify-gate condense"
---

## Overview

The supervisor is a control plane running beside the agent loop, never inside the transcript. It watches each turn, steers the agent off dead ends, verifies completion claims, narrows oversized tool output, and carries lessons and orientation across sessions. Learning is one mechanic among several.

Use this skill to explain supervisor behaviour a user is observing, and to tune the `[supervisor]` sections. Its config is strict: a missing section or required key is a hard parse error.

## Mental model

Free signals gate expensive ones. Every turn produces two zero-cost signals — the agent's self-report and deterministic counters. When they agree, the supervisor acts with no model call at all. A model runs only on disagreement, on a completion claim, or on an oversized tool round.

The verify-gate is the reward signal: it labels a run pass or fail, so the system only learns from work it has evidence was correct.

Everything mid-trajectory is advisory. The supervisor steers, it never blocks a route or silently rewrites context.

## Rules

### The closed loop

Every turn, free: self-report fused with detectors. On conflict or a `done` claim, the verify-gate runs. On pass, distill writes lessons and orientation. Next turn or session, recall injects them. When a detector fires, steer queues an advisory re-anchor.

### Self-report

The agent ends each turn with a compact structured handoff carrying `state`, `focus`, `next`, and `carry`. The supervisor parses it and strips it before display, so the user never sees it. It feeds conversation compression as an attention hint, grounded against the transcript — never evidence on its own. Credential values are forbidden in `carry`; only opaque pointers.

| State | Effect |
|-------|--------|
| `done` | Arms the verify-gate |
| `need_input` | Treated as a question, passed through, never gated |
| `blocked` | Triggers a steer note |
| `exploring` / `progressing` | Fused with the counters |

### Detectors

Deterministic, free, every turn, with fixed thresholds that are behaviour rather than knobs. Two derive from information novelty — a mutation always advances state, a read advances only when its result is new.

- Loop — the same result repeats three times running. Keyed on the result, so reworded calls returning the same thing still count.
- No-progress — five actions with zero novelty.
- Recovery — command-shaped checks keep failing with no later success from the same check.

The power is fusion: a counter saying "no progress" while the agent reports `progressing` is the real stuck signal. Any `done` defers to the gate; no-progress while `exploring` waits; loop, recovery, or unexcused no-progress steers.

### Verify-gate

Armed by a `done` self-report when `[supervisor.gate].enabled`. Free pre-gates run first: mutation-without-check (state changed but no successful command ran since), and plan-complete (more than the final phase still open). Machine-checkable plan assumptions are monitored during execution; a broken one emits `reassess`.

Only if those pass does an independent model verify the result against the request. Pass labels the run verified and permits distill. Gaps inject an advisory and re-run the turn within a fixed budget, hard-stopping on exhaustion. Indeterminate fails closed for the turn.

Set `verifier_model` to a different model family than the agent model — a same-family verifier inherits the same blind spots and rubber-stamps them.

### Steer and recite

Steer queues an advisory re-anchor at the next safe point when a detector fires; re-emission backs off by doubling when the agent provably ignores it. Recite re-injects the live goal at the context tail on already-compacted sessions so intent stays in the recency window. Both are always on and unconfigurable.

### Condense

When a tool round returns results above `[supervisor.condense].tokens_threshold`, one cheap-model call decides per result what the task needs. Fully relevant results are kept byte-for-byte. Partly relevant ones are reduced to line ranges — the condenser sees a numbered copy and answers with ranges, and kept lines are reconstructed verbatim, so nothing can be mis-copied. Irrelevant ones are replaced by a deterministic notice, never a model-written summary.

It is recoverable: the full original spills to a session file first and every condensed result carries the path. It runs only for plain-text results when the role has a local file-reading tool, only in the main session, and any condenser error leaves results untouched. The `mcp_response_tokens_threshold` prefix-cut still applies afterwards as the hard ceiling.

### Lessons and orientation

Two cross-session memories share one backend under `[supervisor.learning]`.

- Lessons — procedural do/avoid rules extracted from user corrections. Scope is either `scoped` (default, stored under `learning/{project}/{role_base}/`, retrieved by relevance) or `global` (stored under `learning/_/`, injected once per session by importance with no relevance gating). The role component truncates at the colon, so `developer:general` stores under `developer/`.
- Orientation — durable descriptive understanding of the subject, stored with `memory_type = "orientation"` and recalled as working assumptions to verify, never as truth.

The storage rule: cache what is expensive to re-derive, never what one search recovers. A symbol's location is cheap; an architectural decision is not.

The loop self-corrects. Entries in context when a run passes gain importance; entries present when a run fails after retries decay and are dropped below a floor. Extraction is quote-first — every lesson carries a verbatim user quote, and a batched verifier drops any lesson whose quote the transcript does not support.

Extraction runs after `/done` or during auto-compaction. Cadence (three user messages) and the per-retrieval injection cap (five) are fixed constants.

### Delegation

`tap run` and `agent_*` spawn a context-isolated child that sees only the prompt string — no transcript, no prior tool output. The handoff must therefore carry the goal, established facts, constraints, and expected deliverable. The child reports its own verified or unverified verdict back to the parent, which folds it into detector and gate state.

### Configuration

```toml
[supervisor]
enabled = true
model = "octohub:auto"

[supervisor.learning]
enabled = true
model = "octohub:auto"
backend = "file"

[supervisor.gate]
enabled = true
verifier_model = "openai:gpt-5-mini"
max_tokens = 8192

[supervisor.plan]
enabled = true
model = "octohub:auto"

[supervisor.condense]
enabled = true
tokens_threshold = 5000
model = "anthropic:claude-haiku-4-5"
```

`[supervisor.learning].backend` accepts `"file"` or `"mcp"`; the MCP backend adds `[supervisor.learning.store]` and `[supervisor.learning.retrieve]`, each with a `tool` name and a `field_map` where an empty string omits a field.

Detectors, recitation, and the free pre-gates have no configuration. Note the strictness asymmetry: the sections are required, but an omitted field inside them takes the code default — `enabled` defaults to `false` for learning, which is on out of the box only because the shipped template sets it explicitly.

### Mechanics at a glance

| Mechanic | When | Cost | Config |
|----------|------|------|--------|
| Self-report, detectors, steer, recite | Every turn | Free | None |
| Free pre-gates | On `done` | Free | `[supervisor.gate]` |
| Verify-gate | On `done`, pre-gates passed | Model, rare | `[supervisor.gate]` |
| Condense | Oversized tool results | Model, cheap | `[supervisor.condense]` |
| Distill | End of a verified run | Model, cheap | `[supervisor.learning]` |
| Recall | Session start and per turn | Embedding | `[supervisor.learning]` |

## Examples

### Example 1: verifier in the same family

❌ Bad:
```toml
[supervisor.gate]
verifier_model = "anthropic:claude-sonnet-4"   # agent model is also Anthropic
```

✅ Good:
```toml
[supervisor.gate]
verifier_model = "openai:gpt-5-mini"
```

What changed: an independent family catches blind spots the agent's own family shares and would otherwise approve.

### Example 2: condense threshold above the hard ceiling

Keep `[supervisor.condense].tokens_threshold` well below `mcp_response_tokens_threshold`. Set higher, condensation never fires before the hard prefix-cut truncates the result, and the task-aware narrowing is wasted.

### Example 3: "the agent keeps redoing the same thing"

That is the loop detector's territory, not a config problem. The counter fires on a repeated result and queues an advisory. Look for a genuinely repeated tool result; disabling the supervisor removes the warning without fixing the repetition.

## Checklist

- [ ] `[supervisor]` and its required subsections present — no section deleted to disable a mechanic?
- [ ] `verifier_model` from a different family than the agent model?
- [ ] `[supervisor.condense].tokens_threshold` comfortably below `mcp_response_tokens_threshold`?
- [ ] Cheap models on learning, plan, and condense; the strong model reserved for the run?
- [ ] Delegation prompts carry full context, since the child sees only the prompt string?
- [ ] Behaviour attributed to the right mechanic before recommending a config change?

## Composition / References

- Pairs with `octomind-config` for every non-supervisor section of `config.toml`.
- Pairs with `octomind-cli` for `/done` and `/learning`, which drive these mechanics from a session.
- Octomind docs: `doc/usage/14-supervisor.md`, `doc/usage/13-learning.md`, `doc/reference/03-config-reference.md`
