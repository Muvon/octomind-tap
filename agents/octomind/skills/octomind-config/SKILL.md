---
name: octomind-config
title: "Octomind Configuration Reference"
description: "Reference for octomind config.toml: model profile, roles, MCP servers, hooks, limits, spending caps. Use when configuring octomind or fixing a parse error."
license: Apache-2.0
compatibility: "Requires: octomind binary for `octomind config --validate`. macOS/Linux/Windows."
capabilities: runtime
rules:
  - match((?i)\b(add|edit|change|set|update|fix|remove|enable|disable|wire|upgrade|tune|adjust|flip|lower|give|merge)\b.{0,70}\b(config\.toml|octomind\s+config|my\s+config|guardrails\.toml|overlay\s+config)\b)
  - match((?i)\b(my|the|project)\s+config\.toml\b.{0,40}\b(won'?t|fails?|parse|error|invalid)\b|\bparse\s+error\b)
  - match((?i)\b(give|grant|add|create|wire)\b.{0,50}\b(role|mcp\s+server|hook)\b.{0,50}\b(access|config|filesystem)\b)
  - match((?i)\b(guardrails\.toml|octomind\s+config\s+--(validate|show|upgrade))\b|\[compression\.model\]|\[roles\.mcp\]|\[\[mcp\.servers\]\])
  - match((?i)\b(set|raise|lower|change|cap)\b.{0,40}\b(spending|session|cost|per-session)\s+(cap|limit|threshold)\b|\bmax_tool_calls\b)
  - semantic(configure octomind settings in config.toml, 0.72)
  - semantic(fix my octomind config file parse error, 0.72)
  - semantic(set a spending limit and choose a model for octomind, 0.72)
  - semantic(add an MCP server and hook to my octomind roles, 0.72)
metadata:
  version: "1.1"
  tags: "octomind config toml roles mcp"
---

## Overview

Octomind's configuration lives at `~/.local/share/octomind/config/config.toml` (`%LOCALAPPDATA%\octomind\config\config.toml` on Windows), overridable with `OCTOMIND_CONFIG_PATH` or relocated with `OCTOMIND_DATA_DIR`. This skill documents the sections and fields so config answers cite real names and defaults. The shipped template (`config-templates/default.toml` in the octomind source, also what `octomind config --show` reflects) is the authority when this page and the binary disagree.

Besydr, the plugin that does completion checks, planning and learning, has its own skill (`octomind-supervisor`).

The skill also covers changing the file: read it, make the smallest edit that achieves the goal, and prove the change parses. It does not cover tap registry artifacts, workflow pipelines, or secrets management beyond naming the right environment variable.

## Mental model

The file is strict. Octomind owns the schema and fails loudly instead of degrading silently:

- Required sections — `[model]`, `[skills]`, `[timing]`, `[compression]`, plus the root scalars (`max_identical_rounds` among them). A missing one is a parse error; `octomind config --upgrade` migrates older files (the template is at `version = 32`; never edit `version` by hand). Version 32 removed `[supervisor]`, its sub-tables and `[decision]`: the Besydr plugin does that work and is listed in the root `plugins` key.
- One model contract — `[model]` is the complete baseline profile. Roles (`[roles.model]`) and `[compression.model]` are partial overrides: omitted fields inherit from `[model]`.
- Required-field tables — `[[commands]]` requires `name`, `description`, `command`, `input_mode`, `output_mode`, `output_role`; only `workdir` is optional.

So a config error is usually a missing key, not a wrong value. Validate after every edit: `octomind config --validate`.

## Rules

### Editing procedure

1. Locate and read the config before touching it. `octomind config --show` prints the effective merged config; the file lives under the octomind config directory, with `config.toml` plus any additional files merged in.
2. State the goal in config terms: which section and which field changes the behaviour the user described. Load the `octomind-supervisor` skill when the change concerns the Besydr plugin: its `plugins` entry is in this file, its own settings are in Besydr's config file.
3. Make the minimal edit. Preserve existing formatting, comments and ordering; never reformat or reorder the file. When two fields could achieve the goal, pick the narrower one and say why.
4. Validate with `octomind config --validate`. A parse error is a hard failure: fix it and re-validate before reporting anything. A file that fails on a missing section usually needs `octomind config --upgrade`, not hand edits.
5. Confirm the effect with `octomind config --show` and report exactly which fields changed and what each does.

Useful commands: `octomind config --show` (effective merged config), `octomind config --validate` (the verifier for every edit), `octomind config --upgrade` (migrate an older config version), `octomind vars` (resolved template placeholder values), `octomind complete run` (every available role tag).

### Prefer the tap for reusable wiring

A role that other people or projects should be able to run belongs in a tap manifest with `capabilities = [...]`, not in hand-wired `[[roles]]` plus `[[mcp.servers]]` in a local config. Say so when a request is really a tap agent. Local config is for machine-specific settings: models, keys, limits, personal roles and overrides.

### Environment and secrets

Two `.env` files load in precedence order: the user-scope file alongside `config.toml`, then the project-local `./.env`, which wins. Both override the system environment, and an empty value counts as not set. Put an API key in a `.env` file and reference the variable name; never paste a secret value into `config.toml` or into a reply.

### Model settings in practice

Sampling values are dropped for models that reject them, so changing `temperature` does nothing on current Claude models: say so instead of tuning it. To turn Besydr off, set `enabled = false` on its `plugins` entry; to turn off one part of it, edit Besydr's config file. Don't add `[supervisor]` or `[decision]` tables: version 32 removed them and Octomind no longer reads them.

### Root settings

| Field | Default | Meaning |
|-------|---------|---------|
| `log_level` | `"info"` | `none`, `info`, `debug` |
| `default` | `"assistant"` | Tag used when `run`/`acp`/`server` get none |
| `sandbox` | `false` | Restrict writes to CWD; Linux Landlock 5.13+, macOS Seatbelt |
| `telemetry` | `true` | Anonymous usage counts; never code, prompts, paths, or env values |
| `auto_capabilities` | `true` | Capability auto-activation on fresh user messages |
| `mcp_response_tokens_threshold` | `20000` | Hard truncation ceiling per MCP response; `0` = unlimited |
| `max_session_tokens_threshold` | `200000` | Session ceiling; validation fails above 2,000,000 |
| `cache_keepalive_enabled` | `false` | Idle cache pings, currently Anthropic only |
| `cache_keepalive_max_idle_seconds` | `1800` | Stop pinging after this idle time; max 86400, `0` = until session ends |
| `enable_markdown_rendering` / `markdown_theme` | `true` / `"default"` | Themes: default, dark, light, ocean, solarized, monokai |
| `max_session_spending_threshold` | `0.0` | USD; prompts before continuing when exceeded |
| `max_request_spending_threshold` | `0.0` | USD; stops the current request when exceeded |
| `system` | unset | Legacy global prompt fallback; prefer per-role `system` |

`default = "assistant"` is a tap agent, not a role in this file. A name is looked up in `[[roles]]` first; if no role has that name, it resolves against taps and runs the agent of that name (the base agent tag is the namespace directory name, such as `assistant` for `agents/assistant/default.toml`; a variant is `<ns>:<variant>`).

### `[model]`

```toml
[model]
name = "octohub:auto"        # provider:model
reasoning_effort = "medium"  # none, low, medium, high, xhigh, max
max_tokens = 32768           # 0 = provider default
max_retries = 1
retry_timeout = 30           # backoff base, seconds
request_timeout_seconds = 300  # 0 = none
```

These fields used to be root scalars (`model`, `max_tokens`, `reasoning_effort`, ...); `--upgrade` moves them. The deprecated `temperature`, `top_p`, and `top_k` keys are accepted in old configs but ignored; octomind sends no sampling parameters, so do not set them.

### `[capabilities]` and `[taps]`

```toml
[capabilities]
websearch = "brave"          # use capabilities/websearch/brave.toml instead of default.toml

[taps]
developer = "ollama:glm-5"   # model name only, for the agent of that name
```

Model priority, highest first: runtime override (`--model`, `/model`), the role's model, the `[taps]` entry, then `[model].name`. A `[taps]` value replaces only the model name; the rest of the profile is inherited.

### `[[roles]]`

Fields: `name`, `system`, `welcome` (all required), optional `[roles.model]` override table (or `model = "provider:model"`), and `[roles.mcp]`. Deprecated sampling keys on a role are accepted in old configs but ignored. Roles in config override tap agents of the same name.

```toml
[[roles]]
name = "assistant"
system = "You are a helpful assistant."
welcome = "Ready. Working in {{CWD}}"

[roles.model]
reasoning_effort = "high"

[roles.mcp]
server_refs = ["core", "orchestration", "runtime", "filesystem", "agent"]
allowed_tools = ["core:*", "orchestration:*", "runtime:*", "filesystem:*", "agent:*"]
```

`server_refs` lists servers to enable; `allowed_tools` filters them, empty meaning all, `server:*` and trailing-`*` prefixes supported.

### `[mcp]` and `[[mcp.servers]]`

`[mcp].allowed_tools` is a global fallback when a role does not specify its own.

Builtin servers need no process: `core` (`recall`, only advertised when `[compression.attention]` or its governance is enabled), `orchestration` (`tap`, `schedule`, `monitor`), `runtime` (`mcp`, `agent`, `skill`, `capability`), `agent` (one `agent_<name>` tool per `[[agents]]` entry). The `filesystem` server default roles reference is the external octofs server supplied by the built-in tap.

Every server needs `name`, `type` (`builtin`|`http`|`stdio`), `timeout_seconds` (1–3600; an idle deadline that MCP progress notifications reset), and `tools` (filter list, `[]` = all). Optional `auto_bind = ["role"]` includes the server for those roles without a `server_ref`. HTTP adds `url` (required) and `headers`; stdio adds `command` (spawned directly, no shell), `args`, `env` (passed to the child), and `cwd`. Values in `headers` and `env` support `{{ENV:KEY}}`.

Authentication: a static `Authorization` header carries a bearer token and disables OAuth discovery. Without one, Octomind uses MCP Authorization Discovery (RFC 9728), registers via CIMD/DCR, and authenticates with PKCE.

### `[[hooks]]`

Webhook listeners: `name`, `bind` (e.g. `"0.0.0.0:9876"`, unique per hook), `script` (stdin = HTTP body, stdout = message to inject), `timeout` (default 30, 1–3600). Activate with `octomind run --daemon --format jsonl --hook <name>`.

### `[[commands]]`, `[[agents]]`, `[[prompts]]`

`[[commands]]` fields: `name`, `description`, `command` (`"octomind acp <role>"`), `input_mode` (`last`|`all`|`summary`), `output_mode` (`none`|`append`|`replace`|`last`|`restart`), `output_role` (`assistant`|`user`), optional `workdir`. Model and prompt live in the referenced role, never in the command. Commands run as `/run <name>`.

`[[agents]]`: `name`, `description`, `command` (any ACP server command), optional `workdir` (default `.`). Each becomes an MCP tool `agent_<name>` on the `agent` server.

`[[prompts]]`: `name`, `prompt`, optional `description`. Inserted via `/prompt <name>`.

Multi-step AI pipelines are not config — they are `octomind workflow <file.toml>`.

### `[skills]`

`auto_activation` (`true`) evaluates declarative rules on fresh user messages. `auto_validation` (`false`) runs tap skills' `validate` scripts at the end of each assistant turn. `validation_timeout` (`60`, `0` = unlimited), `max_retries` (`3`), `activation_timeout` (reserved, kept for compatibility).

### `[timing]`

Per-person calibration for `/report`'s human-time and energy estimate: `think_overhead_min`, `deliberation_factor`, `attention_window_min`, `review_weight`, `wait_weight`, `switch_cost_dhe`.

### `[compression]`

`threshold` (`70000` absolute tokens, `0` disables), `knowledge_retention` (`25`), `analysis_findings_max_tokens` (`6000`, `0` disables). Depth is computed per cycle from measured growth and the context ceiling, not configured. Keep scalar keys above the nested tables, or TOML assigns them to the table.

`[compression.model]` overrides the profile for folds; the template uses `reasoning_effort = "none"` because thinking models otherwise spend the output budget reasoning. `[compression.attention]` (`enabled = false`, `validator`, `telemetry`, `[compression.attention.governance]`) is the evidence-grounded compaction layer that also enables the `recall` tool.

### `[registry]`

`cache_ttl_hours` (`24`) governs tap manifest caching. `tap` (`"muvon/tap"`) names the built-in tap, which is always loaded last, after the taps the user added; `ref` names the branch, tag or commit of it to serve. Taps added with `octomind tap <user/repo>` follow their default branch.

### Multi-file configuration

All `*.toml` in the config directory merge: `config.toml` first, then other files alphabetically, then `mcp-*.toml` last. Arrays of tables concatenate with same-name entries deduplicated (last wins); scalars are overridden by later files. Runtime `mcp` persistence writes `<config_dir>/mcp-<name>.toml` with `auto_bind`.

### Project guardrails (not config.toml)

`<workdir>/.agents/guardrails.toml` holds `[[pipe]]` (transform or reject user input), `[[guard]]` (block a tool call), `[[hook]]` (script after a tool result), and `[[validator]]` (script after the final reply). It loads at session start; a parse error means no authored rules, never a crash. Validators there always run, independent of `[skills] auto_validation`.

### Template variables

Expanded in role `system` and `welcome`: `{{CWD}}`, `{{ROLE}}`, `{{DATE}}`, `{{SHELL}}`, `{{OS}}`, `{{BINARIES}}`, `{{GIT_STATUS}}`, `{{GIT_TREE}}`, `{{README}}`, `{{CONTEXT}}`, `{{SYSTEM}}`. `octomind vars` lists them with live values. Anything else stays literal.

## Examples

### Example 1: command missing required modes

❌ Bad:
```toml
[[commands]]
name = "task_refiner"
description = "Refines requests"
command = "octomind acp task_refiner"
```

✅ Good:
```toml
[[commands]]
name = "task_refiner"
description = "Refines requests"
command = "octomind acp task_refiner"
input_mode = "last"
output_mode = "none"
output_role = "assistant"
```

What changed: the three mode fields have no defaults — the first version fails loading.

### Example 2: model settings at the root

❌ Bad:
```toml
model = "openai:gpt-5"
reasoning_effort = "high"
```

✅ Good:
```toml
[model]
name = "openai:gpt-5"
reasoning_effort = "high"
# remaining profile fields as in the template
```

What changed: model settings live in the `[model]` profile; root scalars are the pre-upgrade layout.

### Example 3: overriding a server from a separate file

Put the override in `mcp-github.toml`, not `zz-github.toml`. Only the `mcp-*.toml` prefix guarantees loading after every regular file.

## Checklist

- [ ] `octomind config --validate` run after the edit and passing?
- [ ] `version` untouched; older layouts migrated with `--upgrade` rather than by hand?
- [ ] Model settings in `[model]`, `[roles.model]`, or `[compression.model]` — not at the root?
- [ ] Every `[[commands]]` entry has `description` and all three modes?
- [ ] Every `[[mcp.servers]]` has `timeout_seconds` and `tools`, plus `url` for http or `command` for stdio?
- [ ] Secrets referenced as `{{ENV:KEY}}` or set in `.env`, never written into the file?
- [ ] Override files that must win named `mcp-*.toml`?
- [ ] Comments, ordering and formatting of the user's file left as they were?
- [ ] The reported change names each field touched and its effect?

## Composition / References

- Pairs with `octomind-cli` for the `octomind config` flags that mutate this file.
- Pairs with `octomind-supervisor` for the Besydr plugin and its `plugins` entry.
- Pairs with `octomind-runtime` for how capabilities and taps resolve into a role's tool surface.
- Octomind docs: `doc/reference/03-config-reference.md`, `doc/usage/03-configuration.md`, `doc/usage/06-roles.md`, `doc/usage/10-commands-and-layers.md`, `doc/usage/18-guardrails.md`
