---
name: tap-capability-authoring
title: "Capability Authoring"
description: "Guide for creating Octomind capabilities: the config.toml triggers file, provider files and the default.toml symlink, MCP server wiring with env and headers, version pins, setup-symlinks.sh registration, and the validation checklist. Activate when creating or editing capabilities/<name>/ files."
license: Apache-2.0
compatibility: "Requires: an Octomind tap checkout with scripts/lint-capabilities.sh and scripts/setup-symlinks.sh."
domains: octomind
---

## Overview

A capability is the layer between agents and MCP servers or toolchains: agents declare what they need (`capabilities = ["websearch"]`), the capability supplies the wiring. This skill covers the two files every capability needs, provider wiring, registration, and validation. Use it when an agent needs a tool no existing capability covers, or when adding a provider to an existing one.

## Mental model

One capability, two kinds of file:

- `config.toml` — routing metadata: required `triggers` (how users phrase the need) and an optional `domains` gate. It drives auto-activation, `capability discover`, and the tap's embedding model.
- `<provider>.toml` — how one tool fulfils the capability: `[deps]`, `[roles.mcp]`, `[[mcp.servers]]`. `default.toml` is a symlink to the active provider; users switch with `[capabilities] <name> = "<provider>"` in their config.

Agents never see providers, so implementations swap without touching agents.

## Rules

### Directory layout

```
capabilities/<name>/
  config.toml          triggers (+ optional domains)
  <provider-a>.toml    provider wiring
  <provider-b>.toml    optional alternative
  default.toml  → <provider-a>.toml
```

`default.toml` is always a symlink, except for the built-ins `core`, `agent`, and `orchestration`, which have real files and no `link` entries.

### config.toml

```toml
# capabilities/<name>/config.toml
triggers = [
  "search the web for recent news on this",
  "look up the latest docs online",
  "find sources about this topic",
]
# domains = ["developer"]   # omit = available in every domain
```

Author 5–15 short, concrete phrasings in the user's voice, not abstract descriptions. Use vocabulary specific to this capability; sibling capabilities that share generic verbs (all `messaging-*`, all `legal-*`) end in near-ties and the runtime abstains. A capability without `config.toml` or with empty triggers fails to resolve. Changing triggers changes the embedding model's training data — see the `tap-model-training` skill.

### Provider file

```toml
# capabilities/<name>/<provider>.toml
# Capability: <name>
# Provider: <provider>
# Title: Short Capability Title (5–60 chars)
# Description: What this provider supplies (20–160 chars). Requires FOO_API_KEY.

[deps]
require = ["org/tool"]              # each needs deps/<org>/<tool>.sh + .md

[roles.mcp]
server_refs = ["servername"]
allowed_tools = ["servername:*"]

[[mcp.servers]]
name = "servername"
type = "stdio"                      # stdio | http | builtin
command = "npx"                     # spawned directly, no shell expansion
args = ["-y", "some-mcp@1.4.2"]     # exact version pin
timeout_seconds = 60                # 1–3600, idle deadline reset by MCP progress
tools = []                          # required; [] = all
env = { FOO_API_KEY = "{{ENV:FOO_API_KEY}}" }
```

- Sections are optional per kind: deps-only (toolchains like `programming-python`), MCP-only, or both.
- The `# Title:`/`# Description:` header is what `capability list` and `discover` show; mention required env vars there.
- `allowed_tools`: `server:*` exposes everything; `server:tool` and trailing-`*` prefixes narrow it.
- Built-in server refs (`core`, `octofs`, `agent`, `octocode`) need no `[[mcp.servers]]` block; every other `server_refs` entry must have one with the same `name`.
- stdio servers take `env` (passed to the child) and optional `cwd`; http servers take `url` and optional `headers` (e.g. `Authorization = "Bearer {{ENV:TOKEN}}"`).
- `{{ENV:KEY}}` in `env` or `headers` resolves from the environment at spawn time. While any key the wiring references is unset, every load path skips the capability: an agent that lists it starts without its tools (no prompt), auto-activation passes it over, and `enable` refuses it. Use the exact variable name the server reads. Literal values in `env` are passed through as-is.
- `{{INPUT:KEY}}` is a text substitution from the user's persistent input store at manifest load; prefer `{{ENV:KEY}}` for anything a server reads from its environment.
- `bin/load` parses capability files with a simple regex TOML subset: keep arrays on one line and avoid inline nesting beyond what the examples show.

### Version pins

Every registry-launched server (`npx`, `uvx`, including inside `sh -c`) pins an exact version (`pkg@X.Y.Z`, `pkg==X.Y.Z`), so a registry publish never changes what users run. `lint-capabilities.sh` enforces presence offline; `scripts/mcp-versions.sh check|update|test` handles drift and live MCP handshakes. Keep a deliberate older pin with a `# mcp-versions: hold <package>` comment and the reason beside it; `update` leaves it alone.

### Registration

Add both to `scripts/setup-symlinks.sh`:

```bash
link "my-capability" "provider.toml"
DECLARED=( ... "my-capability" )
```

Then run `bash scripts/setup-symlinks.sh` — it force-creates links, exits 1 on a missing provider file, and warns about undeclared directories.

### Dep scripts

Every `require = ["<org>/<tool>"]` needs `deps/<org>/<tool>.sh` plus a companion `.md`. `type: mcp` makes a server launchable (ensures `npx`/`uvx`), `type: dep` installs a CLI used directly. Load the `tap-deps-authoring` skill to write them.

### Creation checklist

1. `capabilities/<name>/config.toml` with triggers (and `domains` if domain-specific).
2. `capabilities/<name>/<provider>.toml` with header, wiring, pins, env.
3. Dep scripts and companion docs for every `require` entry.
4. `link` + `DECLARED` entries, then `bash scripts/setup-symlinks.sh`.
5. `bash scripts/lint-capabilities.sh capabilities/<name>`, `bash scripts/lint-deps.sh deps/<org>/<tool>.sh`, `bash scripts/validate-capabilities.sh`.
6. `scripts/mcp-versions.sh test <name>` for npx/uvx servers (missing-credential errors are fine if the server speaks MCP).
7. Reference `"<name>"` from agents; retrain the embedding model when triggers changed.

## Examples

### Example 1: MCP capability with an API key

```toml
# capabilities/websearch/tavily.toml
# Capability: websearch
# Provider: tavily
# Title: Web Search (Tavily)
# Description: Web search, content extraction, crawling, and site mapping via the Tavily API.

[deps]
require = ["tavily-ai/tavily"]

[roles.mcp]
server_refs = ["tavily"]
allowed_tools = ["tavily_search", "tavily_extract", "tavily_crawl", "tavily_map", "tavily_research"]

[[mcp.servers]]
name = "tavily"
type = "stdio"
command = "npx"
args = ["-y", "tavily-mcp@0.2.22"]
timeout_seconds = 60
env = { TAVILY_API_KEY = "{{ENV:TAVILY_API_KEY}}" }
tools = []
```

Bare tool names in `allowed_tools` narrow the surface to exactly those tools.

### Example 2: deps-only toolchain

```toml
# capabilities/programming-python/uv.toml
# Capability: programming-python
# Provider: uv
# Title: Python Runtime via uv
# Description: Python runtime and package management via uv and uvx.

[deps]
require = ["astral-sh/uv"]
```

### Example 3: common mistake — secret as an argument

❌ `args = ["-y", "some-mcp@1.0.0", "--api-key", "{{INPUT:KEY}}"]` — the secret shows up in process listings and the capability is never env-gated.

✅ `env = { SOME_API_KEY = "{{ENV:SOME_API_KEY}}" }` — delivered to the child, and auto-activation waits until the key exists.

## Checklist

- [ ] `config.toml` has 5–15 concrete, capability-specific triggers?
- [ ] Provider header has Title, Description, and required env vars?
- [ ] Every non-built-in `server_refs` entry has a matching `[[mcp.servers]]` block with `timeout_seconds` and `tools`?
- [ ] npx/uvx servers pinned to an exact version?
- [ ] Secrets passed via `env`/`headers` with `{{ENV:KEY}}` using the server's exact variable name?
- [ ] `link` and `DECLARED` updated; `setup-symlinks.sh`, `lint-capabilities.sh`, `lint-deps.sh`, `validate-capabilities.sh` all pass?

## References

- `templates/capability.toml`, `templates/capability-config.toml` — canonical templates
- `scripts/setup-symlinks.sh` — default provider links
- `scripts/mcp-versions.sh` — pin drift, updates, smoke tests
- `tap-deps-authoring` skill — dep scripts
