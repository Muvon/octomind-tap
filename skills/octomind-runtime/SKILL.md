---
name: octomind-runtime
title: "Octomind Runtime & Tool Surface"
description: "Explains how octomind assembles a session at runtime: tap resolution of category:variant tags, manifest placeholders, capability activation and the deterministic embedding auto-activator, domain gating, LRU eviction of the tool surface, skill discovery and the three activation methods, local .agents/tools scripts, and sandbox mode. Activate when a user asks why a tool or skill did or did not appear, how a tag resolves, how capability auto-activation decides, why a capability was evicted or refused, or where skills and taps live on disk."
license: Apache-2.0
compatibility: "Requires: octomind binary. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bauto.?activat)
  - match((?i)\b(LRU|eviction|domain gating|tool surface)\b)
  - match((?i)\b(tap|capability|skill) (resolution|resolve|priority)\b)
  - match((?i)\.agents/(tools|skills)\b)
  - semantic(why is this tool or skill not available in my session)
metadata:
  version: "1.0"
  tags: "octomind runtime capabilities skills taps"
---

## Overview

This skill explains how a session's tool surface comes to exist: how a tag resolves through taps into a manifest, how capabilities turn into running MCP servers, how the auto-activator decides without an LLM in the loop, and how skills, local tools, and the sandbox fit in.

It covers how resolution works, not how to author registry files — writing manifests, capabilities, deps, and skills belongs to the `tap-*` authoring skills.

## Mental model

Every exposed tool costs prompt tokens on every turn, and a wide tool zoo makes the model pick wrong tools. So the surface is deliberately small and grows on demand: capabilities load when intent matches, and the least-recently-used one is evicted when the active set is full.

Two independent layers stack. Static comes from the role's own manifest at boot; dynamic is what a capability adds at runtime. The distinction decides what eviction may tear down: a server the role statically owns is never killed, only the overlay tools a capability added on top of it.

## Rules

### Tap resolution

A tap is a Git repo or local directory holding `agents/<category>/<variant>.toml`, `capabilities/<name>/`, `skills/<name>/`, and `deps/<org>/<tool>.sh`. Manage them with `octomind tap [TAP] [PATH]` and `octomind untap`. The built-in `muvon/tap` is always present as last-priority fallback and can be neither added nor removed.

Priority: user-added taps in the order added, then the built-in tap. When several provide the same tag, the first-listed wins and a debug line is logged — the same first-wins rule applies to skills and capabilities.

Running a tag containing a colon triggers the full pipeline: fetch the manifest from taps (cached), expand `capabilities = [...]`, resolve `{{INPUT:KEY}}` and `{{ENV:KEY}}` placeholders, run `[deps] require` scripts before MCP init, inject the tag as the role name, merge into config, start the session. A missing credential prompts at the placeholder step, not at startup. Manifest caching is governed by `[registry].cache_ttl_hours`, with stale-serve plus background refresh.

Inside a session, the `tap` tool runs a tap role as a subagent: `discover`, `run`, `list`, `stop`. Each run returns an id like `tap-lawyer-sg-9b2c1d`, reusable to stop or resume it.

### Capability anatomy

A capability directory holds two kinds of file. `config.toml` carries capability-level metadata: a required `triggers = [...]` array driving auto-activation and `discover`, plus an optional `domains = [...]`. Missing `config.toml` or missing triggers means the capability fails to resolve. The `<provider>.toml` files carry the MCP wiring — `[[mcp.servers]]`, `server_refs`, `allowed_tools`, `[deps]` — with the provider chosen by the `[capabilities]` config map, defaulting to `default`.

Triggers live in `config.toml`, never in a provider file.

### The capability tool

Hosted by the builtin `runtime` server alongside `mcp`, `agent`, and `skill`. Actions: `list` (installed capabilities in the current domain, active ones marked), `discover` (semantic search over triggers by `intent`, dropping anything at or below a 0.2 cosine floor, returning up to five), `enable`, and `disable`. Enable and disable are idempotent.

Activation registers each `[[mcp.servers]]` block, computing a per-server tool filter from `allowed_tools` — namespace prefixes are stripped to bare names and patterns scoped to other servers are dropped. A server already in the role's static config is not re-registered; the capability extends the role's effective filter instead. A capability with no servers but a non-empty `[deps]` is a toolchain capability, and running the dep installers is the activation.

### Auto-activation

Runs before every API request when `auto_capabilities` is true, embedding the user message and matching it against hand-authored triggers — no LLM in the routing loop.

The decision: strip XML blocks so pasted content cannot drive matches, bail if the cleaned intent has fewer than 8 non-whitespace characters, drop out-of-domain and already-active capabilities before embedding, embed the intent once, then score each capability as the mean of the top-3 cosines against its triggers.

| Constant | Value | Purpose |
|----------|-------|---------|
| `AUTO_ACTIVATE_THRESHOLD` | `0.45` | Minimum mean-of-top-3 cosine |
| `AUTO_ACTIVATE_MARGIN` | `0.08` | Required gap between top-1 and top-2 |
| `AUTO_ACTIVATE_TOP_K` | `3` | Triggers averaged per capability |

The margin gate is why two near-tied capabilities cause abstention rather than a coin flip. Silent no-ops: master toggle off, message not a fresh user message, intent too short, embedding model still downloading, no eligible capability, or no score clearing the gate.

Triggers rather than descriptions, because descriptions use abstract domain language while user messages are concrete and verbal. Triggers put the capability centroid where users actually write.

### Domain gating

The session domain is the category part of the active role — `developer` for `developer:general`. An empty `domains` list means universal; a non-empty one restricts the capability to those domains. The gate applies at every entry point with no bypass: `list` and `discover` silently omit out-of-domain capabilities, auto-activation filters them before embedding, and `enable` hard-fails with an error naming the role you would need. `OCTOMIND_CAPABILITIES` boot-loading goes through the same gated path. With no domain set at all, only universal capabilities survive.

### LRU eviction

The active set has a soft cap of four. Activating beyond it disables the least-recently-used capability first. Eviction is the only auto-disable mechanism — no time decay, no domain-shift eviction, because false-disable hurts more than carrying an idle capability.

Recency means real successful tool usage, not activation order; failed calls do not refresh the timestamp, so a flapping server stays evictable.

Shared servers are safe. Each capability records exactly which bare tool names it registered per server, and the kill decision is `!static_owned && refcount == 0`. Another active capability referencing the server, or the role statically owning it, means only this capability's tools are stripped while the process keeps running. So a chunky capability can be split into focused sub-capabilities pointing at the same binary without one tearing down the others.

### Skills

Discovered from three locations, first-wins by name: taps (`<tap>/skills/<name>/SKILL.md`), the project dir `<workdir>/.agents/skills/`, and the global dir `~/.config/agents/skills/`. Tap skills shadow universal ones.

Three activation methods: `OCTOMIND_SKILLS` preloads at session start; declarative `rules:` auto-activate, which requires both a non-empty `rules:` list and a `domains:` entry matching the current role, on fresh user messages only; and manual `/skill <name>` or the `skill` MCP tool.

The parser reads exactly `name`, `description`, `compatibility`, `license`, `allowed-tools`, `capabilities`, `domains`, and `rules`. Other keys are silently ignored, and a skill missing `name` or `description` is skipped entirely. Files under `scripts/`, `references/`, and `assets/` are listed with absolute paths in a `## Skill Resources` section on activation, so the model can open them on demand.

### Local tools

A shebang script at `<workdir>/.agents/tools/<name>` becomes an MCP tool under server `local` — auto-discovered, role-agnostic, no config. The filename is the tool name and must match `[A-Za-z0-9_-]+` with no extension; on Unix it must be executable. The leading comment block declares the schema with `@description` and repeatable `@param NAME TYPE DESC`, parsed with `#`, `//`, or `--` prefixes and stopping at the first non-comment line or after 80 lines. Parameters arrive as `OCTOMIND_PARAM_<NAME>` environment variables. Skills inject instructions; local tools expose executable actions.

### Sandbox

`sandbox = true` in config, or `--sandbox` per run, restricts all filesystem writes to the launch directory at OS level — Landlock on Linux 5.13+, Seatbelt on macOS. It binds child processes too, including shell and MCP servers.

## Examples

### Example 1: "the tool never showed up"

Work the chain in order: is the capability in the role's `capabilities` list or expected to auto-activate; does its `config.toml` have triggers; is the session domain in its `domains`; did the intent clear 0.45 with a 0.08 margin; was it evicted by the four-capability cap. Each step has a distinct fix, and guessing at the wrong one wastes the turn.

### Example 2: auto-activation ignores a short message

❌ Bad: expecting `do it` to activate a capability.

✅ Good: state the intent — `query the postgres schema`.

What changed: messages under 8 non-whitespace characters are suppressed deliberately, because short acknowledgments produce noisy embeddings that clear the threshold by coincidence.

### Example 3: two database capabilities, neither activates

That is the margin gate abstaining on a near tie, not a failure. Supply the disambiguating signal — name the engine, or call `capability(action="discover", intent=...)` and enable explicitly.

## Checklist

- [ ] Symptom traced to a specific stage: tap resolution, capability activation, domain gate, or eviction?
- [ ] Capability has `config.toml` with non-empty `triggers`?
- [ ] Session domain matches the capability's `domains`, or the list is empty?
- [ ] Skill auto-activation has both `rules:` and a matching `domains:` entry?
- [ ] Skill directory name equals its frontmatter `name`?
- [ ] Local tool executable, extensionless, and carrying an `@description` header?
- [ ] Eviction explanation checks static ownership and refcount before claiming a server was killed?

## Composition / References

- Pairs with `octomind-config` for `[capabilities]`, `[taps]`, `[skills]`, and `[registry]`.
- Pairs with `octomind-cli` for `octomind tap`, `/skill`, `/mcp`, and `OCTOMIND_*` variables.
- Octomind docs: `doc/usage/16-token-efficiency.md`, `doc/usage/15-skills.md`, `doc/usage/17-local-tools.md`, `doc/integration/04-tap-system.md`, `doc/usage/07-mcp-tools.md`
