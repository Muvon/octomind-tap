---
name: octomind-cli
title: "Octomind CLI & Session Commands"
description: "Reference for driving the octomind binary: the run, server, acp, login, config, tap, untap, vars, send, evaluate, workflow, and completion commands and their flags, the interactive slash commands, provider API-key environment variables, .env precedence, and OCTOMIND_* overrides. Activate when a user asks how to invoke octomind, which flag or slash command does what, how to resume or daemonize a session, or which environment variable a provider reads."
license: Apache-2.0
compatibility: "Requires: octomind binary on PATH. macOS/Linux/Windows."
domains: octomind
rules:
  - match((?i)\boctomind (run|server|acp|login|tap|untap|vars|send|evaluate|workflow|completion)\b)
  - match((?i)\bslash command\b)
  - match((?i)/(done|list|model|effort|cache|mcp|skill|loglevel|status|reply|rename|usage|workflow)\b)
  - semantic(which octomind command or flag do I use)
metadata:
  version: "1.1"
  tags: "octomind cli session-commands environment"
---

## Overview

This skill covers how to drive Octomind from the outside: the subcommands and flags of the `octomind` binary, the slash commands inside a running session, and the environment variables that select providers and redirect state. Config file fields belong to the `octomind-config` skill; how manifests resolve belongs to `octomind-runtime`.

Answer from this reference rather than guessing flag names. When a user reports behaviour that contradicts it, check `octomind --version` and `octomind <command> --help` first — they are the ground truth.

## Mental model

Three surfaces, three lifetimes:

- CLI flags — per invocation, never persisted (`--model`, `--schema`, `--sandbox`).
- Slash commands — per session; `/model` and `/effort` save to the session file, `/loglevel` is runtime-only.
- Config and environment — durable across sessions.

A change belongs on the narrowest surface that survives long enough. Never edit config for a one-off run.

## Rules

### Subcommands

Bare `octomind` behaves like `octomind run` with the default role.

| Command | Purpose |
|---------|---------|
| `run [TAG]` | Interactive or non-interactive session — the main command |
| `server [TAG]` | WebSocket server for remote sessions (`--host` default `127.0.0.1`, `--port`/`-p` default `8080`, `--sandbox`, repeatable `--allow-origin`) |
| `acp [TAG]` | Agent Client Protocol agent over stdio for editors (`-n`, `-r`, `--resume-recent`, `-m`, `--sandbox`, `--hook`) |
| `login [chatgpt]` | Sign in to an Octomind account (stores the hub key as `OCTOHUB_API_KEY`); `login chatgpt` lets `chatgpt:<model>` run on a ChatGPT plan |
| `config` | Create, validate, display, or upgrade configuration |
| `tap [TAP] [PATH]` | Add a tap (`user/repo` clones `github.com/user/octomind-repo`; with PATH it links a local directory); bare lists taps |
| `tap init <user/repo>` | Scaffold a new tap from the default tap's scaffold, validate it, git-init it, register it (`--agent domain:spec`, `--dir`) |
| `untap <TAP>` | Remove a tap |
| `vars` | Placeholder variables and resolved values (`-p/--preview`, `-e/--expand`) |
| `send --name <NAME> [MESSAGE]` | Inject a message into a running named session; message from stdin when omitted |
| `evaluate [FILE]` | Ask the evaluation model typed questions about a JSON state (`{"state", "questions"}` from FILE or stdin), answers printed as JSON; `-m` overrides the model |
| `workflow [NAME\|FILE]` | Run a multi-step workflow; bare lists tap workflows (`--dry-run`, `--format jsonl`) |
| `completion <SHELL>` | bash, zsh, fish, elvish, or powershell completions |

Hidden helpers: `octomind complete run` prints every runnable tag (tap agents plus config roles), `octomind complete workflow` every tap workflow name — handy for scripting and discovery.

### TAG resolution

`run`, `server`, and `acp` take an optional TAG: a plain role name matched against `[[roles]]` in config, or a tap agent tag in `domain:spec` form resolved through installed taps. Omitted, it uses `default` from config — except when resuming, where the session's own role is restored. Model priority, highest first: `--model`, the role's model, a `[taps]` entry for that tag, then the main `[model]` profile.

### `octomind run` flags

| Flag | Effect |
|------|--------|
| `--name` / `-n` | Named session: created if new, resumed if it exists |
| `--resume` / `-r [SESSION]` | Resume by name; bare `--resume` opens the interactive picker (error when non-interactive) |
| `--resume-recent` | Resume the most recent session for this directory |
| `--format` | `plain` or `jsonl`; setting it makes the run non-interactive |
| `--model` / `-m` | Override model, `provider:model` |
| `--daemon` | Keep the session alive for messages delivered with `octomind send` |
| `--sandbox` | Restrict filesystem writes to the working directory |
| `--hook` | Activate a `[[hooks]]` webhook by name; repeatable |
| `--schema` | JSON Schema file constraining the final reply |

Interactivity: with `--format` unset and stdin a TTY, the session is interactive. Otherwise input is read from stdin, and empty stdin is an error. `--daemon` is non-interactive and needs `--format`; attached to a terminal its initial input is empty.

`--schema` constrains the final reply for the session's lifetime; tool calls still flow underneath. Models without structured-output support fail fast. It is not persisted — pass it again on resume.

### `octomind config` flags

Mutating (saved to the config file): `--model`, `--log-level none|info|debug`, `--mcp-providers`, `--mcp-server name,url=X|command=Y,args=Z`, `--system` (`default` resets), `--markdown-enable`, `--markdown-theme`.

Inspect or maintain: `--show`, `--validate`, `--list-themes`, `--upgrade`.

`--api-key` parses but is always rejected at runtime — keys live in the environment, never in config. Bare `octomind config` creates a default config only when none exists.

### Session slash commands

| Group | Commands |
|-------|----------|
| Session | `/help`, `/exit` (`/quit`), `/clear`, `/list [PAGE]`, `/new [TITLE]`, `/rename [TITLE]` |
| Output | `/copy [last\|assistant\|user\|all]`, `/reply [N\|words]` (quote an earlier reply into the prompt) |
| Monitoring | `/info`, `/status [agents [id]\|monitors\|jobs]`, `/report [day\|week\|month] [here]`, `/usage`, `/share`, `/analyze` |
| Runtime switches | `/model [MODEL]`, `/role [ROLE]`, `/effort [none\|low\|medium\|high\|xhigh\|max]`, `/loglevel [none\|info\|debug]` |
| Context | `/context [all\|assistant\|user\|tool\|system\|large]`, `/done` |
| Media | `/image [PATH]`, `/video [PATH]` |
| Tools | `/mcp [list\|info\|full\|health\|dump\|validate]`, `/skill [NAME\|PAGE\|PATTERN]` |
| Config-driven | `/run [COMMAND]`, `/prompt [NAME]` |
| State | `/plan`, `/schedule [list\|add\|edit\|remove]`, `/learning [list\|show\|delete\|clear\|evolution]`, `/workflow [NAME [INPUT]]` |
| Account | `/login` |

Behaviour worth knowing:

- `/model` and `/effort` save to the session file, not global config. `/loglevel` is runtime-only.
- `/role` accepts a config role name or a tap tag.
- `/done` force-compresses context, bypassing threshold and cost guards, then starts lesson extraction in the background.
- `/mcp` is read-only. Runtime server management is the `mcp` tool of the `runtime` server.
- `/plan` only displays the supervisor-owned plan; nothing in the session can edit it.
- `/workflow` lists tap workflows, `/workflow <name>` shows the definition, `/workflow <name> <input>` runs it (blocking).
- `/share` uploads the session and prints a URL. `/analyze` uploads nothing — it serves a token-gated local bridge for the web viewer.
- `/?` shows in autocomplete but is not dispatched; use `/help`.

### Provider environment variables

Most providers read `<PREFIX>_API_KEY` for their model prefix — `groq:` reads `GROQ_API_KEY`, `openrouter:` reads `OPENROUTER_API_KEY`. It is a per-provider contract, not a universal rule. Exceptions worth knowing: `google-vertex:` uses `GOOGLE_VERTEX_CREDENTIAL_FILE` (or `GOOGLE_APPLICATION_CREDENTIALS`) plus optional `GOOGLE_VERTEX_PROJECT_ID`/`GOOGLE_VERTEX_LOCATION`; `amazon:` uses `AWS_BEARER_TOKEN_BEDROCK` (a Bedrock API key, not SigV4 keys) plus `AWS_BEDROCK_REGION`; `cloudflare:` needs `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`; `moonshot:`/`kimi:` share `MOONSHOT_API_KEY`; `opencode-zen:`/`opencode-go:` share `OPENCODE_API_KEY`; `octohub:` reads `OCTOHUB_API_KEY`, which `octomind login` writes.

Many providers accept a `<PREFIX>_API_URL` endpoint override; `local:` with `LOCAL_API_URL` targets any self-hosted OpenAI-compatible server. The `cli:BACKEND/MODEL` meta-provider runs an installed coding CLI and needs no key.

### Octomind environment variables

| Variable | Effect |
|----------|--------|
| `OCTOMIND_DATA_DIR` | Redirect durable state: config, sessions, logs, cache, learning, taps |
| `OCTOMIND_CONFIG_PATH` | Primary config file; its parent becomes the config dir for multi-file merge |
| `OCTOMIND_SKILLS` | Comma-separated exact skill names preloaded at session start |
| `OCTOMIND_CAPABILITIES` | Comma-separated capabilities force-enabled at start; domain and env gates still apply |
| `OCTOMIND_TELEMETRY` | `0`/`false`/`off`/`no` disables telemetry for the run |
| `DO_NOT_TRACK` | Cross-tool opt-out, honoured before `OCTOMIND_TELEMETRY` and config |
| `OCTOMIND_SHARE_URL` | Web viewer base for `/share` and `/analyze` |
| `RUST_LOG` | Tracing filter; in CLI mode it enables the stderr subscriber |

### .env precedence

Two files load, later winning: user-scope `<config_dir>/.env`, then project-local `./.env`. Both override the system environment.

## Examples

### Example 1: one-off model change

❌ Bad:
```bash
octomind config --model openai:gpt-5   # rewrites global config for one task
```

✅ Good:
```bash
octomind run developer:general -m openai:gpt-5
```

What changed: the narrowest surface that survives long enough — a flag, not a persisted setting.

### Example 2: non-interactive with structured output

```bash
echo "List the top 3 TODOs" | octomind run developer:general \
  --format jsonl --schema todos.schema.json
```

Piped stdin already forces non-interactive mode; `--format jsonl` makes the stream machine-readable.

### Example 3: daemon plus webhook

```bash
octomind run --name ci-watcher --daemon --format jsonl --hook github-push
echo "status?" | octomind send --name ci-watcher
```

`--daemon` without `--format` is the common mistake.

## Checklist

- [ ] Flag or slash command named exactly as `--help` and the tables above show?
- [ ] One-off change expressed as a CLI flag rather than a config edit?
- [ ] `--daemon` paired with `--format` and a `--name`?
- [ ] API key set via environment or `.env`, never suggested for config.toml?
- [ ] Provider variable is the exact name that provider reads, including the documented exceptions?
- [ ] Session-scoped answers use slash commands; durable ones route to `octomind-config`?

## Composition / References

- Pairs with `octomind-config` for anything inside `config.toml`.
- Pairs with `octomind-runtime` for how a TAG resolves to a manifest.
- Octomind docs: `doc/reference/01-cli-reference.md`, `doc/reference/02-session-commands.md`, `doc/reference/04-environment-variables.md`
