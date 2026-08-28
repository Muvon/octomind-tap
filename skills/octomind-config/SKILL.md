---
name: octomind-config
title: "Octomind Configuration Reference"
description: "Field-by-field reference for octomind's config.toml: root settings, performance and spending limits, [capabilities] and [taps] overrides, [[roles]] and [roles.mcp], [mcp] servers (builtin/http/stdio), [[hooks]], [[layers]], [[commands]], [[agents]], [[prompts]], [skills], [compression], [registry], multi-file merge, and template variables. Activate when a user asks how to configure, tune, validate, or upgrade octomind, add a role or MCP server, set limits or spending caps, or debug a config parse error."
license: Apache-2.0
compatibility: "Requires: octomind binary for `octomind config --validate`. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\bconfig\.toml\b)
  - match((?i)octomind config\b)
  - match((?i)\[\[?(roles|mcp\.servers|layers|commands|agents|prompts|hooks|compression|registry|capabilities|taps|skills)\]\]?)
  - semantic(configure octomind settings in config.toml)
metadata:
  version: "1.0"
  tags: "octomind config toml roles mcp"
---

## Overview

Octomind's configuration lives at `~/.local/share/octomind/config/config.toml` (`%LOCALAPPDATA%\octomind\config\config.toml` on Windows), overridable with `OCTOMIND_CONFIG_PATH`. This skill documents every section and field, so config answers cite real field names and defaults rather than plausible-sounding ones.

Supervisor tuning has its own skill (`octomind-supervisor`); this one covers everything else in the file.

## Mental model

The file has three kinds of section, and they fail differently:

- Scalars with defaults — omit them and you get the default.
- Strict sections — `[supervisor]` and its required keys are a hard parse error when missing. Octomind owns that schema and fails loudly instead of degrading silently.
- Required-field tables — `[[layers]]` and `[[commands]]` require `input_mode`, `output_mode`, and `output_role`; omitting any fails config loading.

So a config error is usually a missing required key, not a wrong value. Validate after every edit: `octomind config --validate`. Never modify `version` — it drives `--upgrade`.

## Rules

### Root-level settings

| Field | Type | Default | Meaning |
|-------|------|---------|---------|
| `version` | u32 | template ships `8` | Schema version. Do not modify. |
| `log_level` | string | `"info"` | `none`, `info`, `debug` |
| `model` | string | `"octohub:auto"` | Default model, `provider:model` |
| `default` | string | `"assistant:concierge"` | Default TAG for `run`/`acp`/`server` |
| `max_tokens` | u32 | `32768` | Global max tokens |
| `sandbox` | bool | `false` | Restrict writes to CWD; Linux Landlock 5.13+, macOS Seatbelt |
| `telemetry` | bool | `true` | Anonymous usage counts; never code, prompts, or paths |
| `auto_capabilities` | bool | `true` | Automatic capability activation on user messages |
| `system` | string | none | Legacy global system-prompt fallback; prefer per-role `system` |

`default = "assistant:concierge"` is a tap agent from the built-in tap, not a role in this file — searching for a `concierge` role finds nothing. A bare tag without a colon resolves against `[[roles]]`; `category:variant` resolves against taps.

### Performance and limits

| Field | Default | Meaning |
|-------|---------|---------|
| `mcp_response_tokens_threshold` | `20000` | Hard truncation ceiling for MCP responses; `0` = unlimited |
| `max_session_tokens_threshold` | `200000` | Session ceiling, also the hard compression ceiling; validation fails above 2,000,000 |
| `max_retries` | `1` | API retry attempts |
| `retry_timeout` | `30` | Exponential-backoff base, seconds |
| `request_timeout_seconds` | `300` | Per-request HTTP timeout; `0` = none |
| `reasoning_effort` | `"medium"` | `low`/`medium`/`high`/`xhigh`/`max`; ignored by non-thinking models |
| `cache_keepalive_enabled` | `false` | Idle cache pings; provider-aware, currently Anthropic only |
| `cache_keepalive_max_idle_seconds` | `1800` | Stop pinging after this idle time; validation fails above 86400 |

### User interface and spending

`enable_markdown_rendering` (`true`), `markdown_theme` (`default`, `dark`, `light`, `ocean`, `solarized`, `monokai`), `max_session_spending_threshold` and `max_request_spending_threshold` (USD, `0.0` = no limit). Session threshold prompts before continuing; request threshold stops execution.

### `[capabilities]` and `[taps]`

```toml
[capabilities]
codesearch = "octocode"        # picks capabilities/codesearch/octocode.toml

[taps]
"developer:general" = "ollama:glm-5"
```

`[capabilities]` routes a capability name to a non-default provider. `[taps]` sets a model per tap agent, acting at the `config.model` tier — it applies only when neither `--model` nor the agent's own role model is set, and only to tags containing a colon.

### `[[roles]]`

Fields: `name` (required), `model`, `system`, `welcome`, `temperature` (0.0–2.0), `top_p` (0.0–1.0), `top_k` (1–1000). Roles in config override tap-provided agents of the same name.

```toml
[[roles]]
name = "assistant"
temperature = 0.3
system = "You are a helpful assistant. Working directory: {{CWD}}"

[roles.mcp]
server_refs = ["core", "runtime", "filesystem", "agent"]
allowed_tools = ["core:*", "runtime:*"]
```

`[roles.mcp].server_refs` lists servers to enable; `allowed_tools` filters them, empty meaning all, wildcards supported.

### `[mcp]` and `[[mcp.servers]]`

`[mcp].allowed_tools` is a global fallback used when a role does not specify its own.

Builtin servers need no process: `core` (`recall`), `orchestration` (`tap`, `schedule`, `monitor`), `runtime` (`mcp`, `agent`, `skill`, `capability`), `agent` (one `agent_<name>` tool per `[[agents]]` entry). The `filesystem` server that default roles reference is not a builtin — it is an external stdio server backed by `octofs`, supplied by the built-in tap, exposing `view`, `text_editor`, `batch_edit`, `extract_lines`, `shell`, `workdir`.

Common server fields: `name`, `type` (`builtin`|`http`|`stdio`), `timeout_seconds` (required; per-operation, reset by tool-call progress), `tools` (filter, wildcards ok), `auto_bind` (role names to auto-include for). HTTP adds `url` (required) and `headers` (values support `{{ENV:KEY}}`). Stdio adds `command` (required) and `args`.

Authentication: a static `Authorization` header carries a bearer token and disables OAuth discovery. Without one, Octomind uses MCP Authorization Discovery (RFC 9728), registers via CIMD/DCR, and authenticates with PKCE.

### `[[hooks]]`

Webhook listeners: `name`, `bind` (e.g. `"0.0.0.0:9876"`), `script`, `timeout` (default 30, range 1–3600). Activate with `octomind run --daemon --hook <name>`.

### `[[layers]]`, `[[commands]]`, `[[agents]]`, `[[prompts]]`

`[[layers]]` and `[[commands]]` share one schema: `name`, `description`, `command` (`"octomind acp <role>"`), `input_mode` (`last`|`all`|`summary`), `output_mode` (`none`|`append`|`replace`|`last`|`restart`), `output_role` (`assistant`|`user`), and optional `workdir`. The three modes have no defaults — omitting any fails loading. Model and prompt live in the referenced `[[roles]]` entry, never in the layer. Layers are ACP orchestration units; commands are typed as `/run <name>`.

Multi-step AI pipelines are not config — they are `octomind workflow <file.toml>`.

`[[agents]]`: `name`, `description`, `command`, optional `workdir`. Each becomes an MCP tool `agent_<name>`.

`[[prompts]]`: `name`, `description`, `prompt`. Injected verbatim via `/prompt <name>`; no variable substitution.

### `[skills]`

`auto_activation` (`true`) evaluates declarative rules on every user message. `auto_validation` (`false`) runs skill `validate` scripts at end of turn — it gates only SKILL.md validators, not guardrail `[[validator]]` entries, which always run. Also `activation_timeout` (reserved), `validation_timeout` (`60`, `0` = unlimited), `max_retries` (`3`).

### `[compression]`

`knowledge_retention` (`25`), `analysis_findings_max_tokens` (`6000`, `0` disables), `threshold` (`70000` absolute tokens, `0` disables). Depth is computed, not configured: once past `threshold`, the ratio derives per cycle from measured growth and the context ceiling, always landing in [2.0, 16.0].

`[compression.decision]` picks the model doing the work: `model` (`openai:gpt-5-mini`), `max_tokens` (`16000`), `temperature` (`0.3`), `top_p`, `top_k`, `max_retries`, `retry_timeout`. Cheap and fast is the right choice.

### `[registry]`

`cache_ttl_hours` (`24`) governs tap manifest caching. Within the TTL the cache is served; once stale, the cached copy is still served while a background refresh runs.

### Multi-file configuration

All `*.toml` in the config directory merge: `config.toml` first, then others alphabetically, with arrays of tables concatenated, same-name entries deduplicated (last wins), and scalars overridden by later files. Files matching `mcp-*.toml` load last regardless of alphabetical order, so they reliably override servers defined in `mcp.toml`. The `mcp persist` command relies on this, writing `<config_dir>/mcp-<name>.toml` with `auto_bind`.

### Template variables

Substituted in role `system` and `welcome` at prompt-expansion time: `{{CWD}}`, `{{ROLE}}`, `{{DATE}}`, `{{SHELL}}`, `{{OS}}`, `{{BINARIES}}`, `{{GIT_STATUS}}`, `{{GIT_TREE}}`, `{{README}}`, plus `{{CONTEXT}}` and `{{SYSTEM}}` for layers. `{{HOME}}` is not substituted in prompts — it only appears in the `octomind vars` listing, so it stays literal in a role prompt. Use an absolute path or `{{CWD}}`.

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

What changed: the three mode fields have no defaults — the first version fails config loading outright.

### Example 2: model and prompt in the wrong place

❌ Bad:
```toml
[[layers]]
name = "reduce"
model = "openai:gpt-5-mini"
system = "Compress the transcript."
```

✅ Good:
```toml
[[roles]]
name = "reduce"
model = "openai:gpt-5-mini"
system = "Compress the transcript."

[[commands]]
name = "reduce"
description = "Compress session history"
command = "octomind acp reduce"
input_mode = "all"
output_mode = "replace"
output_role = "assistant"
```

What changed: layers delegate over ACP; model, prompt, and MCP config belong to the role the command references.

### Example 3: overriding a server from a separate file

Put the override in `mcp-github.toml`, not `zz-github.toml`. Only the `mcp-*.toml` prefix guarantees loading after `mcp.toml`; any other name risks being overwritten by alphabetical order.

## Checklist

- [ ] `octomind config --validate` run after the edit and passing?
- [ ] `version` left untouched?
- [ ] Every `[[layers]]`/`[[commands]]` entry has `input_mode`, `output_mode`, `output_role`?
- [ ] Every `[[mcp.servers]]` has `timeout_seconds`, plus `url` for http or `command` for stdio?
- [ ] `server_refs` names resolve to a builtin, a tap-provided server, or a declared `[[mcp.servers]]`?
- [ ] No API key written into the file — environment or `.env` instead?
- [ ] Override files that must win named `mcp-*.toml`?
- [ ] Model, system prompt, and MCP config placed in `[[roles]]`, not in a layer or command?

## Composition / References

- Pairs with `octomind-cli` for the `octomind config` flags that mutate this file.
- Pairs with `octomind-supervisor` for `[supervisor]`, which is strict and documented separately.
- Pairs with `octomind-runtime` for how capabilities and taps resolve into a role's tool surface.
- Octomind docs: `doc/reference/03-config-reference.md`, `config-templates/default.toml`, `doc/usage/03-configuration.md`, `doc/usage/06-roles.md`, `doc/usage/10-commands-and-layers.md`
