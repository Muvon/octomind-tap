---
name: octomind-cli
title: "Octomind CLI & Session Commands"
description: "Reference for driving the octomind binary: run/server/acp/config/tap/vars/send/workflow/completion commands and their flags, the 25 interactive slash commands, provider API-key environment variables, .env precedence, and OCTOMIND_* overrides. Activate when a user asks how to invoke octomind, which flag or slash command does what, how to resume or daemonize a session, or which environment variable a provider reads."
license: Apache-2.0
compatibility: "Requires: octomind binary on PATH. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\boctomind (run|server|acp|tap|untap|session|vars|send|report|completion)\b)
  - match((?i)\bslash command\b)
  - match((?i)/(done|list|model|effort|cache|mcp|skill|loglevel)\b)
  - semantic(which octomind command or flag do I use)
metadata:
  version: "1.0"
  tags: "octomind cli session-commands environment"
---

## Overview

This skill covers how to drive Octomind from the outside: the subcommands and flags of the `octomind` binary, the slash commands available inside a running session, and the environment variables that select providers and redirect state. It does not cover config file fields (see the `octomind-config` skill) or how manifests resolve (see `octomind-runtime`).

Answer from this reference rather than guessing flag names. When a user reports behaviour that contradicts it, check the installed version first.

## Mental model

Three surfaces, three lifetimes:

- CLI flags — per invocation, never persisted (`--model`, `--schema`, `--sandbox`).
- Slash commands — per session; some write to the session file (`/model`, `/effort`), some are runtime-only (`/loglevel`).
- Config and environment — durable across sessions.

A change belongs on the narrowest surface that survives long enough. Never edit config for a one-off run.

## Rules

### Subcommands

A subcommand is required; bare `octomind` prints a usage error.

| Command | Purpose |
|---------|---------|
| `run [TAG]` | Start an interactive or non-interactive session — the main command |
| `server [TAG]` | WebSocket server for remote sessions (`--host`, `--port`, `--sandbox`) |
| `acp [TAG]` | Agent Client Protocol agent over stdio, for editor integration |
| `config` | Create, validate, display, or upgrade configuration |
| `tap [TAP] [PATH]` | Add a tap, or list taps when called bare |
| `untap <TAP>` | Remove a tap |
| `vars` | Show placeholder variables and resolved values (`--preview`, `--expand`) |
| `send` | Inject a message into a running named session |
| `workflow` | Run an external multi-step pipeline TOML |
| `completion <SHELL>` | Generate bash/zsh/fish completions |

### TAG resolution

`run`, `server`, and `acp` take an optional TAG: a plain role name matched against `[[roles]]` in config, or a tap agent tag in `category:variant` form resolved through installed taps. Omitted, it uses `default` from config. Model priority, highest first: `--model` > the role/agent `model` field > root `config.model`; a `[taps]` entry overrides the `config.model` tier for tap agents only.

### `octomind run` flags

| Flag | Effect |
|------|--------|
| `--name` / `-n` | Named session identifier |
| `--resume` / `-r` | Resume a session by name |
| `--resume-recent` | Resume the most recent session for this directory |
| `--format` | `plain` or `jsonl`; unset by default |
| `--model` / `-m` | Override model, `provider:model` |
| `--daemon` | Keep the session alive for injected messages |
| `--sandbox` | Restrict filesystem writes to the working directory |
| `--hook` | Activate a webhook hook by name; repeatable |
| `--schema` | Path to a JSON Schema object file constraining output |

Interactivity: with `--format` unset and stdin a TTY, the session is interactive. Passing `--format`, or piping stdin, makes it non-interactive. `--daemon` is non-interactive and effectively requires `--format`; deliver later messages with `octomind send --name <name>`.

`--schema` applies to every assistant reply for the session's lifetime, including resumes and daemon mode; tool calls still flow underneath and only the final text is constrained. Models without structured-output support fail fast. It is a runtime override, not persisted — pass it again on resume.

### `octomind config` flags

Mutating (saved to the config file): `--model`, `--log-level none|info|debug`, `--mcp-providers a,b,c` (replaces the whole server list with builtins), `--mcp-server name,key=value,...`, `--system` (`default` resets), `--markdown-enable`, `--markdown-theme`.

Inspect only: `--show`, `--validate`, `--list-themes`, `--upgrade`.

`--mcp-server` keys: `type` (`http`|`stdio`|`builtin`, default http), `url` (required for http), `command` (required for stdio), `args`, `timeout`/`timeout_seconds`.

`--api-key` parses but is always rejected at runtime. Keys live in the environment, never in config.

Bare `octomind config` creates a default config only when none exists; it does not regenerate an existing one.

### Session slash commands

| Group | Commands |
|-------|----------|
| Session | `/help`, `/exit` (`/quit`), `/clear`, `/list [PAGE]`, `/new [TITLE]` |
| Monitoring | `/info`, `/report`, `/share`, `/analyze`, `/copy` |
| Runtime switches | `/model [MODEL]`, `/role [ROLE]`, `/effort [low\|medium\|high\|xhigh\|max]`, `/loglevel [LEVEL]` |
| Context | `/context [all\|assistant\|user\|tool\|system\|large]`, `/done` |
| Media | `/image [PATH]`, `/video [PATH]` |
| Tools | `/mcp [info\|list\|full\|health\|dump\|validate]`, `/skill [NAME\|PAGE\|PATTERN]` |
| Config-driven | `/run [COMMAND]`, `/prompt [NAME]` |
| State | `/plan [show]`, `/schedule [SUBCOMMAND]`, `/learning [ACTION]` |

Behaviour worth knowing:

- `/model` and `/effort` persist to the session file, not global config. `/loglevel` is runtime-only.
- `/role` accepts a config role name or a tap tag; on failure the previous role, model, and temperature are reverted.
- `/done` force-compresses context, bypassing threshold, cooldown, and cost guards, then triggers lesson extraction. It preserves no injected skills and does not touch the plan.
- `/mcp` is read-only. Runtime server management is the `mcp` MCP tool, not the slash command.
- `/plan` is display-only; the specialist has no plan mutation tool.
- `/share` uploads the session JSONL and prints a permanent URL. `/analyze` uploads nothing — it binds a token-gated loopback bridge so the viewer fetches locally.
- `/?` appears in autocomplete but is not wired to the dispatcher; only `/help` shows help.

### Provider environment variables

Any provider prefix authenticates via its uppercased `<PREFIX>_API_KEY` — `groq:` reads `GROQ_API_KEY`. Common: `OPENROUTER_API_KEY` (recommended one-key entry point), `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `DEEPSEEK_API_KEY`, `OCTOHUB_API_KEY`.

Providers needing more than one variable: Google Vertex (`GOOGLE_APPLICATION_CREDENTIALS` or `GOOGLE_CREDENTIAL_FILE`, plus `GOOGLE_CLOUD_PROJECT_ID`, `GOOGLE_CLOUD_LOCATION`), Amazon Bedrock (`AWS_BEARER_TOKEN_BEDROCK` — a Bedrock API key, not SigV4 credentials — plus `AWS_BEDROCK_REGION`), Cloudflare (`CLOUDFLARE_API_TOKEN` and the required `CLOUDFLARE_ACCOUNT_ID`).

Most providers accept `<PREFIX>_API_URL` to target a self-hosted endpoint. The `cli:` meta-provider shells out to a local coding CLI and needs no key.

### Octomind environment variables

| Variable | Effect |
|----------|--------|
| `OCTOMIND_DATA_DIR` | Redirect all state: config, sessions, logs, cache, learning |
| `OCTOMIND_CONFIG_PATH` | Override the config file path; its parent becomes the config dir for multi-file merge |
| `OCTOMIND_SKILLS` | Comma-delimited skills preloaded at session start, bypassing activation rules |
| `OCTOMIND_CAPABILITIES` | Comma-delimited capabilities force-enabled, bypassing auto-activation |
| `OCTOMIND_TELEMETRY` | `0`/`false`/`off`/`no` disables telemetry for the run |
| `DO_NOT_TRACK` | Cross-tool opt-out, honoured before `OCTOMIND_TELEMETRY` and config |
| `RUST_LOG` | Tracing filter; in CLI mode it enables the stderr subscriber |

### .env precedence

Two files load, later winning: user-scope `<config_dir>/.env`, then project-local `./.env`. Both override the system environment. An empty value counts as unset.

## Examples

### Example 1: one-off model change

❌ Bad:
```bash
octomind config --model openai:gpt-4o   # rewrites global config for one task
```

✅ Good:
```bash
octomind run developer -m openai:gpt-4o
```

What changed: the narrowest surface that survives long enough — a flag, not a persisted setting.

### Example 2: non-interactive with structured output

```bash
echo "List the top 3 TODOs" | octomind run developer:general \
  --format jsonl --schema todos.schema.json
```

Piped stdin already forces non-interactive mode; `--format jsonl` makes the stream machine-readable and pairs naturally with `--schema`.

### Example 3: daemon plus webhook

```bash
octomind run --name ci-watcher --daemon --format jsonl --hook github-push
echo "status?" | octomind send --name ci-watcher
```

`--daemon` without `--format` is the common mistake — attached to a terminal, the piped input is forced empty.

## Checklist

- [ ] Flag or slash command named exactly as it appears in the tables above?
- [ ] One-off change expressed as a CLI flag rather than a config edit?
- [ ] `--daemon` paired with `--format` and a `--name`?
- [ ] API key set via environment or `.env`, never suggested for config.toml?
- [ ] Provider variable is the exact `<PREFIX>_API_KEY` the provider reads?
- [ ] Session-scoped answers use slash commands; durable ones route to `octomind-config`?

## Composition / References

- Pairs with `octomind-config` for anything inside `config.toml`.
- Pairs with `octomind-runtime` for how a TAG resolves to a manifest.
- Octomind docs: `doc/reference/01-cli-reference.md`, `doc/reference/02-session-commands.md`, `doc/reference/04-environment-variables.md`
