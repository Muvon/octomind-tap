---
name: octomind-tap-maintenance
title: "Tap Registry Maintenance: Agents, Skills, Capabilities"
description: "Create and maintain tap registry artifacts, agent manifests, capabilities, dep scripts and skills, lint-clean and resolvable with bin/load."
license: Apache-2.0
compatibility: "Requires: a tap checkout with bash, Python 3.11+ and the octomind binary on PATH. macOS/Linux."
capabilities: runtime
domains: octomind
rules:
  - match((?i)\b(tap|registry)\b.{0,40}\b(agents?|skills?|capabilit(y|ies)|dep\s+scripts?|manifests?)\b)
  - match((?i)\b(lint-manifests|lint-skills|lint-capabilities|lint-deps|validate-capabilities|setup-symlinks|bin/load)\b)
  - match((?i)\b(write|create|add|author)\b.{0,30}\b(an?\s+)?(octomind\s+)?(agent\s+manifest|capability|dep\s+script|SKILL\.md)\b)
  - semantic(add a new agent or skill to my tap registry, 0.72)
  - semantic(write a new capability with a provider file and dep script, 0.72)
  - semantic(why does this tap manifest fail lint, 0.72)
  - semantic(resolve an agent manifest and check the capabilities merge, 0.72)
---

## Overview

A tap registry holds agent manifests (`agents/<name>.toml`), capabilities with the dep scripts behind them (`capabilities/<name>/`, `deps/<org>/<tool>.sh`), and skills (`skills/<name>/SKILL.md`). This skill is the working method for creating and maintaining them so that everything shipped is lint-clean and resolves with `bin/load`.

The authoring specifications are the `tap-agent-authoring`, `tap-capability-authoring`, `tap-deps-authoring` and `tap-skill-authoring` skills; this skill adds the surrounding procedure and checks. The local `config.toml`, workflow pipelines and AGENTS.md files are outside it.

## Mental model

Agents declare what they need, never how to get it. The runtime resolves each capability name to a provider file and merges its wiring into the manifest. One agent serves one field of work, and what a specialty adds to it lives in a skill bound to that agent, so the manifest stays short and the depth is loaded when a request needs it.

## Rules

### Which tap to edit

Work in the current directory when it is a tap (it has `agents/` or `capabilities/` at the root). Otherwise use the user's own local tap: run `octomind tap`, where user taps are listed first and local ones show their path (`(local: …)`); a personal tap is often registered as `my/tap`. Ask when there is none. Entries in user taps shadow same-named entries from the built-in `muvon/tap`. Never edit the built-in tap's checkout under the data directory: it is a managed clone that updates on its own.

### Working sequence

1. Read the repo's AGENTS.md and look at two or three existing entities of the same kind before writing.
2. Load the authoring skill for the entity and follow it: the `tap-agent-authoring` skill for agents, `tap-capability-authoring` for capabilities, `tap-deps-authoring` for dep scripts, `tap-skill-authoring` for skills. Changing capability triggers or skill `semantic()` phrases also means the `tap-model-training` skill, and so does anything under `model/`: weights, the embed pipeline and a release only count once `MODEL_REVISION` in octomind names the new hub commit and the calibrated thresholds ship with it.
3. Reuse before creating: check `capabilities/` for an existing capability or provider before adding one, and `skills/` before writing a skill.
4. Write the smallest correct change, then run the checks below for everything you touched and fix every failure before reporting.

### Checks

- Agents: `bash scripts/lint-manifests.sh agents/<name>.toml` and `bin/load <name>`.
- Capabilities: `bash scripts/setup-symlinks.sh`, `bash scripts/lint-capabilities.sh capabilities/<name>`, `bash scripts/validate-capabilities.sh`; `scripts/mcp-versions.sh test <name>` for npx and uvx servers.
- Deps: `bash scripts/lint-deps.sh deps/<org>/<tool>.sh`.
- Skills: `bash scripts/lint-skills.sh skills/<name>`.

### Layout

```
agents/<name>.toml                 one [[roles]], capabilities = [...] at top level
capabilities/<name>/config.toml    triggers (+ optional domains)
capabilities/<name>/<provider>.toml  [deps], [roles.mcp], [[mcp.servers]]
capabilities/<name>/default.toml   symlink to the active provider (real file for core, agent, orchestration)
deps/<org>/<tool>.sh + .md         installer + companion doc
skills/<name>/SKILL.md             frontmatter + body
workflows/<name>.toml              public workflows
bin/load                           resolves capabilities into the merged manifest
scripts/                           lint, validation, symlink setup, MCP pin management
```

The agents are the files under `agents/`, one per field of work. A new subject or format for an existing field is a skill bound to that agent with `domains:`; a new agent is added only for a new field of work, named by what it owns. Tapping or clicking a native app or a web page belongs to `operator`, writing or changing source to `developer`.

### Capabilities

Agents declare capabilities, never MCP servers. At runtime octomind resolves each name to `capabilities/<name>/default.toml` (or the provider chosen in the user's `[capabilities]` config) and merges `[deps] require`, `server_refs`, `allowed_tools` and `[[mcp.servers]]` (deduplicated by name); `bin/load` mirrors this for local checks. Manifests never name a provider.

- Tiers: `core` for every agent; domain capabilities as needed; `agent` for agents that run their own configured sub-agents; `orchestration` for agents that start copies of themselves or hand tasks to other agents; `runtime` only for `octomind`. A skill that needs a tool the agent lacks lists it in its own `capabilities:` frontmatter.
- `allowed_tools`: `server:*` exposes all of a server's tools; `server:tool`, bare names and trailing-`*` prefixes narrow it.
- Every `server_refs` entry needs a matching `[[mcp.servers]]` block unless it is a built-in (`core`, `octofs`, `agent`, `octocode`).
- Secrets go in stdio `env` or http `headers` as `{{ENV:EXACT_VAR_NAME}}`; octomind passes `env` to the child and withholds the capability until the variable is set. Never put secrets in `args`.
- npx and uvx servers pin an exact version.
- To see what exists, list `capabilities/` and read each provider's `# Description:` header.

### Manifests

Required: `# Agent:`, `# Title:` and `# Description:` headers, top-level `capabilities`, and one `[[roles]]` with `system` and `welcome`. Forbidden: `name`, `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`, and sampling parameters (`temperature`, `top_p`, `top_k`). The system prompt uses XML blocks in canonical order with no `{{CWD}}`, `{{DATE}}` or `{{SYSTEM}}`; those belong in `welcome`. Behaviour comes from the prompt. The full specification is in the `tap-agent-authoring` skill.

Multi-step pipelines are not manifest content: they are `workflows/*.toml` run by `octomind workflow`. `[[commands]]` exists only in a user's local config.

### Placeholders

`{{INPUT:KEY}}` and `{{ENV:KEY}}` resolve when a manifest loads (stored inputs; environment, or a prompt saved to `./.env`), and `{{ENV:KEY}}` in server `env` and `headers` resolves again at spawn. `{{CWD}}`, `{{DATE}}` and the other prompt placeholders expand only in `system` and `welcome`, never inside capability values.

## Checklist

- [ ] The right tap is being edited, not the built-in clone.
- [ ] An existing capability or skill was checked before a new one was created.
- [ ] The manifest has no `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`, `name` or sampling parameters.
- [ ] Every lint for the touched entity type passes and `bin/load` resolves the agent.
- [ ] Capability or trigger changes were checked against the model training procedure.

## Composition / References

- The `tap-agent-authoring`, `tap-capability-authoring`, `tap-deps-authoring` and `tap-skill-authoring` skills hold the authoring specifications.
- The `tap-model-training` skill covers trigger and embedding model changes.
- The `octomind-workflow-engineering` skill covers workflow pipelines.
