---
name: octomind-config
title: "Octomind Configuration Reference"
description: "Field-by-field reference for octomind's config.toml: the [model] profile and its per-boundary overrides, limits and spending caps, [capabilities] and [taps] overrides, [[roles]] with [roles.model] and [roles.mcp], [mcp] servers (builtin, http, stdio), [[hooks]], [[layers]], [[commands]], [[agents]], [[prompts]], [skills], [timing], [compression], [registry], multi-file merge, project guardrails, and template variables. Activate when a user asks how to configure, tune, validate, or upgrade octomind, add a role or MCP server, set limits or spending caps, or debug a config parse error."
license: Apache-2.0
compatibility: "Requires: octomind binary for `octomind config --validate`. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bconfig\.toml\b)
  - match((?i)octomind config\b)
  - match((?i)\[\[?(model|roles|roles\.model|mcp\.servers|layers|commands|agents|prompts|hooks|compression|registry|capabilities|taps|skills|timing)\]\]?)
  - semantic(configure octomind settings in config.toml)
metadata:
  version: "1.1"
  tags: "octomind config toml roles mcp"
---

## Overview

Octomind's configuration lives at `~/.local/share/octomind/config/config.toml` (`%LOCALAPPDATA%\octomind\config\config.toml` on Windows), overridable with `OCTOMIND_CONFIG_PATH` or relocated with `OCTOMIND_DATA_DIR`. This skill documents the sections and fields so config answers cite real names and defaults. The shipped template (`config-templates/default.toml` in the octomind source, also what `octomind config --show` reflects) is the authority when this page and the binary disagree.

Supervisor tuning has its own skill (`octomind-supervisor`).

## Mental model

The file is strict. Octomind owns the schema and fails loudly instead of degrading silently:

- Required sections — `[model]`, `[skills]`, `[timing]`, `[compression]`, `[supervisor]` and its mechanic tables, plus the root scalars. A missing one is a parse error; `octomind config --upgrade` migrates older files (the template is at `version = 21`; never edit `version` by hand).
- One model contract — `[model]` is the complete baseline profile. Roles (`[roles.model]`), `[compression.model]`, and `[supervisor.model]` are partial overrides: omitted fields inherit from `[model]`.
- Required-field tables — `[[layers]]` and `[[commands]]` require `name`, `description`, `command`, `input_mode`, `output_mode`, `output_role`; only `workdir` is optional.

So a config error is usually a missing key, not a wrong value. Validate after every edit: `octomind config --validate`.

## Rules

### Root settings

| Field | Default | Meaning |
|-------|---------|---------|
| `log_level` | `"info"` | `none`, `info`, `debug` |
| `default` | `"assistant:concierge"` | Tag used when `run`/`acp`/`server` get none |
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

`default = "assistant:concierge"` is a tap agent, not a role in this file. A tag without a colon resolves against `[[roles]]`; `domain:spec` resolves against taps.

### `[model]`

```toml
[model]
name = "octohub:auto"        # provider:model
reasoning_effort = "medium"  # none, low, medium, high, xhigh, max
max_tokens = 32768           # 0 = provider default
temperature = 0.3            # 0.0–2.0
top_p = 0.7                  # 0.0–1.0
top_k = 20                   # 0–1000
max_retries = 1
retry_timeout = 30           # backoff base, seconds
request_timeout_seconds = 300  # 0 = none
```

These fields used to be root scalars (`model`, `max_tokens`, `reasoning_effort`, ...); `--upgrade` moves them. Sampling values are sent only where the provider accepts them — the provider layer drops them for models that reject sampling parameters and while extended thinking is on.

### `[capabilities]` and `[taps]`

```toml
[capabilities]
websearch = "brave"          # use capabilities/websearch/brave.toml instead of default.toml

[taps]
"developer:general" = "ollama:glm-5"   # model name only
```

Model priority, highest first: runtime override (`--model`, `/model`), the role's model, the `[taps]` entry, then `[model].name`. A `[taps]` value replaces only the model name; the rest of the profile is inherited.

### `[[roles]]`

Fields: `name`, `system`, `welcome` (all required), optional `[roles.model]` override table (or `model = "provider:model"`), and `[roles.mcp]`. Flat `temperature`/`top_p`/`top_k` on a role are still accepted (tap manifests use them) and folded into the role's model override. Roles in config override tap agents of the same name.

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

### `[[layers]]`, `[[commands]]`, `[[agents]]`, `[[prompts]]`

`[[layers]]` and `[[commands]]` share one schema: `name`, `description`, `command` (`"octomind acp <role>"`), `input_mode` (`last`|`all`|`summary`), `output_mode` (`none`|`append`|`replace`|`last`|`restart`), `output_role` (`assistant`|`user`), optional `workdir`. Model and prompt live in the referenced role, never in the layer. Commands run as `/run <name>`.

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

`cache_ttl_hours` (`24`) governs tap manifest caching.

### Multi-file configuration

All `*.toml` in the config directory merge: `config.toml` first, then other files alphabetically, then `mcp-*.toml` last. Arrays of tables concatenate with same-name entries deduplicated (last wins); scalars are overridden by later files. Runtime `mcp` persistence writes `<config_dir>/mcp-<name>.toml` with `auto_bind`.

### Project guardrails (not config.toml)

`<workdir>/.agents/guardrails.toml` holds `[[pipe]]` (transform or reject user input), `[[guard]]` (block a tool call), `[[hook]]` (script after a tool result), and `[[validator]]` (script after the final reply). It loads at session start; a parse error means no authored rules, never a crash. Validators there always run, independent of `[skills] auto_validation`.

### Template variables

Expanded in role `system` and `welcome`: `{{CWD}}`, `{{ROLE}}`, `{{DATE}}`, `{{SHELL}}`, `{{OS}}`, `{{BINARIES}}`, `{{GIT_STATUS}}`, `{{GIT_TREE}}`, `{{README}}`, `{{CONTEXT}}`, `{{SYSTEM}}`. `octomind vars` lists them with live values. Anything else stays literal.

## Examples

### Example 1: layer missing required modes

❌ Bad:
```toml
[[layers]]
name = "task_refiner"
description = "Refines requests"
command = "octomind acp task_refiner"
```

✅ Good:
```toml
[[layers]]
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
- [ ] Model settings in `[model]`, `[roles.model]`, `[compression.model]`, or `[supervisor.model]` — not at the root?
- [ ] Every `[[layers]]`/`[[commands]]` entry has `description` and all three modes?
- [ ] Every `[[mcp.servers]]` has `timeout_seconds` and `tools`, plus `url` for http or `command` for stdio?
- [ ] Secrets referenced as `{{ENV:KEY}}` or set in `.env`, never written into the file?
- [ ] Override files that must win named `mcp-*.toml`?

## Composition / References

- Pairs with `octomind-cli` for the `octomind config` flags that mutate this file.
- Pairs with `octomind-supervisor` for `[supervisor]`, which is documented separately.
- Pairs with `octomind-runtime` for how capabilities and taps resolve into a role's tool surface.
- Octomind docs: `doc/reference/03-config-reference.md`, `doc/usage/03-configuration.md`, `doc/usage/06-roles.md`, `doc/usage/10-commands-and-layers.md`, `doc/usage/18-guardrails.md`
