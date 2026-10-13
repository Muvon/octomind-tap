---
name: octomind-runtime
title: "Octomind Runtime & Tool Surface"
description: "Explains how octomind assembles a session at runtime: tap resolution of domain:spec tags, manifest placeholders, built-in tool servers, capability activation and the deterministic embedding auto-activator, domain and env gating, LRU eviction of the tool surface, skill discovery and activation, Agent Plugins, local .agents/tools scripts, and sandbox mode. Activate when a user asks why a tool or skill did or did not appear, how a tag resolves, how capability auto-activation decides, why a capability was evicted or refused, or where skills and taps live on disk."
license: Apache-2.0
compatibility: "Requires: octomind binary. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bauto.?activat)
  - match((?i)\b(LRU|eviction|domain gating|tool surface)\b)
  - match((?i)\b(tap|capability|skill) (resolution|resolve|priority)\b)
  - match((?i)\.agents/(tools|skills|plugins)\b)
  - semantic(why is this tool or skill not available in my session)
metadata:
  version: "1.1"
  tags: "octomind runtime capabilities skills taps"
---

## Overview

This skill explains how a session's tool surface comes to exist: how a tag resolves through taps into a manifest, which tools are built in, how capabilities turn into running MCP servers, how the auto-activator decides without an LLM in the loop, and how skills, plugins, local tools, and the sandbox fit in.

It covers resolution, not authoring — writing manifests, capabilities, deps, and skills belongs to the `tap-*` authoring skills.

## Mental model

Every exposed tool costs prompt tokens on every turn, and a wide tool zoo makes the model pick wrong tools. So the surface starts small and grows on demand: capabilities load when intent matches, and the least-recently-used one is evicted when the active set is full.

Two layers stack. Static comes from the role's manifest at boot; dynamic is what a capability adds at runtime. Eviction may tear down only the dynamic layer — a server the role statically owns is never killed.

## Rules

### Tap resolution

A tap is a Git repo or local directory holding `agents/<domain>/<spec>.toml`, `capabilities/<name>/`, `skills/<name>/`, `deps/<org>/<tool>.sh`, `workflows/<name>.toml`, and optionally `plugins/`. `octomind tap user/repo` clones `github.com/user/octomind-repo` into `<data_dir>/taps/user/octomind-repo`; `octomind tap user/repo <path>` links a local directory instead. The built-in `muvon/tap` is always present as the last-priority fallback.

Priority: user taps in the order added, then the built-in tap. The first tap providing a tag, skill, capability, or workflow wins. A capability can be pinned explicitly: `octomind/<name>` for the baseline tap, `<org>/<name>` for a connected tap.

Running a `domain:spec` tag: fetch the manifest (cached per `[registry].cache_ttl_hours`), expand `capabilities = [...]`, resolve `{{INPUT:KEY}}` (persistent store `inputs.toml`, prompted once) and `{{ENV:KEY}}` (environment, else prompted and saved to `./.env`), run `[deps] require` scripts before MCP init, inject the tag as the role name, merge into config, start the session. In non-interactive child runs a missing value is an error, not a prompt.

### Built-in tools

| Server | Tools | Granted by |
|--------|-------|------------|
| `core` | `recall` (only when compression attention is enabled) | `core` capability |
| `orchestration` | `tap`, `schedule`, `monitor` | `orchestration` capability |
| `runtime` | `mcp`, `agent`, `skill`, `capability` | `runtime` capability |
| `agent` | `agent_<name>` per `[[agents]]` entry | `agent` capability |
| `local` | scripts in `.agents/tools/` | always, per workdir |

There is no plan tool: planning is supervisor-owned and only displayed via `/plan`.

`tap` actions: `discover` (match an intent against agents' `# Title:`/`# Description:` headers), `run` (background child; `role` + `prompt`, optional `workdir`; pass `session=<id>` to continue a run, otherwise the child starts with zero context), `list`, `stop`, `capability` (push an intent through the auto-activation path), and `workflow` (list, show, or run a tap workflow in the background). Run ids look like `tap-developer-general-a3f1c2`; results arrive in a later turn.

### Capability anatomy

`config.toml` carries a required non-empty `triggers = [...]` and optional `domains = [...]`; missing either file or triggers means the capability fails to resolve. `<provider>.toml` carries `[deps]`, `[roles.mcp]`, and `[[mcp.servers]]`; the provider comes from the `[capabilities]` config map, else `default`. Its `# Title:` and `# Description:` header feed `list` and `discover`.

The `capability` tool (on `runtime`): `list`, `discover` (semantic match over triggers, keyword fallback), `enable`, `disable`. Activation registers each server with a filter computed from `allowed_tools`; a server already in the role's static config is not re-registered, the capability extends its filter instead. A capability with no servers but non-empty `[deps]` is a toolchain capability — running the installers is the activation.

### Auto-activation

Runs before every API request when `auto_capabilities = true`, on fresh user messages only. Steps: skip system-managed text; strip XML blocks so pasted content cannot drive matches; bail if fewer than 8 non-whitespace characters remain; drop already-active, out-of-domain, and env-unready capabilities (any `{{ENV:KEY}}` in a server's `env` or `headers` that is unset); embed the intent once; score each capability as the mean of its top-3 trigger cosines.

| Constant | Value | Purpose |
|----------|-------|---------|
| `AUTO_ACTIVATE_THRESHOLD` | `0.65` | Minimum mean-of-top-3 cosine |
| `AUTO_ACTIVATE_MARGIN` | `0.06` | Required gap between top-1 and top-2 |
| `AUTO_ACTIVATE_TOP_K` | `3` | Triggers averaged per capability |

The embedding model is `muvon/octomind-embed` (int8 ONNX). The margin gate is why two near-tied capabilities cause abstention rather than a coin flip. With `[supervisor.evaluate] capabilities = true`, an evaluation model can veto a weak cosine winner or promote a pick when cosine abstained. Silent no-ops: toggle off, not a fresh user message, intent too short, embedding model still downloading, nothing eligible, or no score clearing the gate.

### Domain gating

The session domain is the part before the colon of the active role. An empty `domains` list means universal; a non-empty one restricts the capability. The gate applies everywhere — `list`, `discover`, auto-activation, `enable`, and `OCTOMIND_CAPABILITIES` — with no bypass. With no domain set, only universal capabilities survive.

### LRU eviction

At most four runtime-activated capabilities per session. Activating a fifth disables the least-recently-used first. Recency means successful tool use, not activation order. Eviction is the only auto-disable — no time decay. Capabilities preloaded from the manifest are static and never counted.

Shared servers are safe: each capability records which tools it registered per server, and the process is killed only when the role does not own the server statically and no other active capability references it.

### Skills

Discovery order, first name wins: tap `skills/` directories, `<workdir>/.agents/skills/`, `~/.config/agents/skills/`, Agent Plugin skill directories, then generated skills from learning evolution.

Three activation methods: `OCTOMIND_SKILLS` preloads at session start; declarative `rules:` auto-activate on fresh user messages when `[skills] auto_activation` is on and the skill's `domains:` contains the session domain (or `*`); manual `/skill <name>` or `skill(action="use")`. With `[supervisor.evaluate] skills = true`, an evaluation model may pick a skill from the domain pool when every rule abstained.

The parser reads `name`, `description`, `compatibility`, `license`, `allowed-tools`, `capabilities`, `domains`, and `rules`; other keys are ignored, and a skill missing `name` or `description` is skipped. Files under `scripts/`, `references/`, and `assets/` are listed with absolute paths in a Skill Resources section on activation. Declared `capabilities` are enabled with the skill.

### Agent Plugins

Directories with a `plugin.json` (Agent Plugins 1.0.0 schema) are scanned from tap `plugins/`, `<workdir>/.agents/plugins/`, and `~/.config/agents/plugins/`. Their `skills/<name>/SKILL.md` join skill discovery and their `mcp.json` declares MCP servers. A bad manifest rejects the plugin; a bad skill or server skips only that part.

### Local tools

An executable script at `<workdir>/.agents/tools/<name>` becomes a tool on the `local` server — rediscovered every turn, role-agnostic, no config. The filename is the tool name (`[A-Za-z0-9_-]+`). The leading comment block (`#`, `//`, or `--`, first 80 lines) declares `@description` and repeatable `@param NAME TYPE DESC`; prefix the name with `*` for required. Params arrive as JSON on stdin and as `OCTOMIND_PARAM_<NAME>` env vars; stdout is the result, non-zero exit is an error, default timeout 300 s.

### Sandbox

`sandbox = true` or `--sandbox` restricts filesystem writes to the launch directory at OS level — Landlock on Linux 5.13+, Seatbelt on macOS — including child processes, shell, and MCP servers.

## Examples

### Example 1: "the tool never showed up"

Work the chain in order: is the capability in the role's `capabilities` list or expected to auto-activate; does its `config.toml` have triggers; is the session domain in its `domains`; are its `{{ENV:}}` keys set; did the intent clear 0.65 with a 0.06 margin; was it evicted by the four-capability cap. Each step has a distinct fix.

### Example 2: auto-activation ignores a short message

❌ Bad: expecting `do it` to activate a capability.

✅ Good: state the intent — `query the postgres schema`.

What changed: messages under 8 non-whitespace characters are skipped deliberately; short acknowledgments embed noisily.

### Example 3: two database capabilities, neither activates

That is the margin gate abstaining on a near tie. Name the engine, or call `capability(action="discover", intent=...)` and enable explicitly.

## Checklist

- [ ] Symptom traced to a stage: tap resolution, placeholders, capability activation, domain or env gate, or eviction?
- [ ] Capability has `config.toml` with non-empty `triggers`?
- [ ] Session domain matches the capability's `domains`, or the list is empty?
- [ ] Skill auto-activation has both `rules:` and a matching `domains:` entry?
- [ ] Local tool executable, extensionless, and carrying an `@description` header?
- [ ] Eviction explanation checks static ownership and refcount before claiming a server was killed?

## Composition / References

- Pairs with `octomind-config` for `[capabilities]`, `[taps]`, `[skills]`, and `[registry]`.
- Pairs with `octomind-cli` for `octomind tap`, `/skill`, `/mcp`, and `OCTOMIND_*` variables.
- Octomind docs: `doc/usage/16-token-efficiency.md`, `doc/usage/15-skills.md`, `doc/usage/17-local-tools.md`, `doc/integration/04-tap-system.md`, `doc/usage/07-mcp-tools.md`
