---
name: octomind-supervisor
title: "Octomind Supervisor Work: Besydr Plugin"
description: "Explain Besydr plugin completion checks, tool admission, condensing, planning, loop notes, and learning. Use for reruns or old supervisor settings."
license: Apache-2.0
compatibility: "Requires: octomind binary, config version 32 or later; the besydr program (Octomind downloads it on first use). macOS/Linux/Windows."
rules:
  - match((?i)\bsupervisor\b)
  - match((?i)\bbesydr\b)
  - match((?i)\bplugins\s*=|\[\[plugins\]\])
  - match((?i)\bcompletion.?check\b)
  - match((?i)\[supervisor)
  - match((?i)\b(condense|cross.session learning|/learning)\b)
  - semantic(why did octomind re-run, check or block my turn)
metadata:
  version: "2.0"
  tags: "octomind besydr plugin supervisor completion-check learning"
---

## Overview

Since configuration version 32, Octomind has no built-in supervisor. The work the supervisor used to do (a completion check at the end of a turn, a check on tool calls before they run, condensing of long tool output, a plan manager, notes when the agent loops, lessons learned from sessions) is done by Besydr. Besydr is a separate program that Octomind runs as a plugin.

A plugin is a program that Octomind sends events to (session start, each prompt, before and after tool calls, the end of a turn) and whose answers Octomind applies.

Use this skill to explain behaviour a user sees from Besydr, to turn the plugin on or off, and to point users with old `[supervisor]` settings to where those settings went. Besydr's own pages are the source for its details: `https://besydr.com/docs/mechanics`, `/learning`, `/configuration`.

## Mental model

Two programs, two config files. Octomind decides whether the plugin runs: the root key `plugins` in `config.toml`. Besydr decides what it does while running: its own file. A switch for one Besydr part is never in `config.toml`.

Octomind keeps working without the plugin. It then runs as a plain agent loop. What disappears is every check and every learned lesson: no completion check, no tool admission check, no learning across sessions, no condensing of tool output, no plan manager.

## Rules

### Lists, starts and installs the plugin

A new configuration has one entry in the root key `plugins`. It is an inline table, so the key stays above the first `[table]` header of `config.toml`:

```toml
plugins = [
	{ name = "besydr", type = "stdio", command = "besydr", args = ["connect"], install_manifest = "https://cdn.besydr.com/latest.json", install_key = "uU5IoojVdfJZj5/fU4JQE8CXnmYXNBGo5nyLgWcNNrw=" },
]
```

- `type = "stdio"`: Octomind starts `besydr connect` and talks to it over standard input and output. That command joins the Besydr server shared by all your clients and starts it when it is not running.
- When `besydr` is not installed, Octomind downloads it on first use from the signed release `install_manifest` names. The release must be signed with `install_key`, or nothing is installed. Octomind never updates the program by itself.
- Provider keys: Besydr reads the OctoHub key that `octomind login` stores, so a logged-in user sets nothing.
- Configurations written before version 32 get this entry on upgrade, unless they already list a plugin named `besydr`.
- Besydr is free with Octomind and needs no licence there.

### Turn it off

- Add `enabled = false` to the `besydr` entry, or remove the entry. A plugin that is not listed, or has `enabled = false`, receives nothing.
- One run only: `-c 'plugins=[]'` runs Octomind with no plugin.
- Single Besydr parts (condensing, learning) are switched in Besydr's file, not in `config.toml`.
- There is no `supervisor.enabled` switch. `-c supervisor.enabled=false` fails with `Unknown config override path 'supervisor.enabled'`.

### What Octomind still does without the plugin

- The agent loop, tools and MCP servers, sessions and cost accounting.
- Compaction of long conversations, including `/done`.
- The rules in `.agents/guardrails.toml`.
- Storage and display of the plan (`/plan`). The agent has no tool to change the plan; a plugin creates and advances it. Without a plugin `/plan` reports that there is no plan.
- The status line: the agent ends each response with a hidden line that reports its state. Octomind reads it and removes it before display.
- A hard stop for runaway tool loops: root key `max_identical_rounds` (default `10`). When that many tool rounds in a row repeat calls and results already seen since the last new result, the turn ends with a notice naming the repeated call. `0` turns the stop off. `-c max_identical_rounds=0` sets it for one run.
- Its own rules for which skill and which capability a request activates, which agent gets a delegated task, and which tool results a compaction summarizes.

### What Besydr does

Each part has a switch in Besydr's file. Several parts call a model, so they use your model account. `/info` in Octomind shows the calls, time and cost of each part that ran.

- Completion check (`[gate] enabled`, default on). Before work starts, Besydr writes a checklist from your request. When the agent stops at the end of a turn you started, Besydr compares the checklist with the tool calls, results and file changes. Pass: the turn ends. Gaps: the agent is sent back to work with the gaps as its next instruction. Unsettled (thin evidence): one note per user turn when `unsettled_advisory` is on, then the check runs again. Indeterminate (model unavailable or unusable answer): the turn ends and is recorded as unverified. At most 3 checks per turn. It is as good as the writing model and is not a code review.
- Tool admission (`[authorizer] enabled`, default on). A call is allowed unless the writing model finds a conflict with your words or the agent's role and the decision model confirms it. A model that is unavailable, times out or is unsure allows the call. A confirmed conflict is a denied call with a reason quoting your words.
- Condensing of large tool output (`[condense] enabled`, `tokens_threshold` default 5000, `adaptive`). A plain-text result above the threshold is cut to the chunks that report a failure, hold the requested data, or name a path or line to act on. Kept lines are copied from the original. The full original is saved to a file whose path the shortened result names. Results under 512 tokens are never candidates. `tokens_threshold = 0` turns it off.
- Plan manager (`[plan] enabled`). The agent signals that work has dependent phases; a separate model call creates, advances, holds or revises the plan. In Octomind `/plan` shows it.
- Loop and no-progress notes. No switch, thresholds fixed: the same calls and results for 3 rounds, 5 rounds with nothing new, or failed commands with no later success. The note is advice and never blocks a call.
- Advice note (`[advise] enabled`). A model writes the loop or failure note instead of the plain one. One in four eligible signals gets the plain note on purpose, so the effect can be compared.
- Standing rules. No switch. A rule you state for the rest of the session ("from now on, never push to main") is kept in your exact words, repeated with every later request and kept through compaction. At most 8 rules of at most 200 characters.
- Learning (`[learning] enabled`, default on). Lessons from your corrections and rules, added to later sessions. In Octomind `/learning` comes from the plugin, with the sub-commands `list`, `show`, `delete`, `clear` and `evolution`. Generated skills and rules (`[learning.evolution] enabled`) are off by default and need `[gate] enabled = true`.
- Hindsight (`[hindsight] enabled`) scores handed-back turns for the chance you will correct them. It acts on nothing and is counted in `/info`. Project document sections (`[inject] enabled`) add the part of a document that `AGENTS.md` references and that fits the file being worked on; no model is called.
- Judgements for Octomind. Octomind asks its plugin to decide four things: which skill, which capability, which agent for a delegated task, and which tool results a compaction may drop. Besydr answers with its decision model.

### Besydr's configuration

- Find it with `besydr config`: it prints the config file path, the data directory, the model and the decision model, and whether their key variables are set. It never prints a key. By default the file is `<data directory>/config/config.toml`; the data directory is `~/.local/share/besydr` on Linux and macOS.
- The file is strict: every key present, unknown keys an error, `version` must be `1`. Restart the server after an edit.
- `[model]` writes text (checklist, completion check, plans, lessons). `[decision]` `model` answers short typed questions and writes no text. Both default to `octohub:auto`. `[model]` keys include `name`, `reasoning_effort`, `max_tokens`.
- Other tables: `[server]`, `[sessions]`, `[learning]`, `[learning.evolution]`, `[gate]`, `[authorizer]`, `[hindsight]`, `[advise]`, `[plan]`, `[condense]`, `[inject]`.
- Judgements have no switch: with Besydr connected, all four always go to the decision model. `[decision]` holds only `model` and `recall` (ask the decision model whether each recalled lesson fits the request), and an unknown key there is an error. Octomind's page `doc/usage/14-supervisor.md` still names `skills`, `capabilities`, `taps` and `compression` switches; Besydr has none of them.

### Where the old settings went

- `[supervisor]`, all `[supervisor.*]` tables and `[decision]` are removed from `config.toml`; Octomind no longer reads them.
- The upgrade saves them unchanged to `besydr-carry/supervisor.toml` beside `config.toml`. Besydr reads that file once, on its first run, and takes matching settings into its own file.
- `supervisor.max_identical_rounds` became the root key `max_identical_rounds`. `supervisor.enabled = false` became `enabled = false` on the `besydr` entry.
- The commands `evaluate` and `distill` are removed from the `octomind` program. Octomind has no evaluation model of its own. Overrides like `-c supervisor.gate.enabled=false` name nothing.
- Lessons Octomind learned earlier are imported by Besydr on its first run.

### When the plugin does not answer

- Octomind goes on without that answer and queues a notice. A busy plugin that says so is waited for, at most one hour.
- After 3 unanswered events in a row the plugin is paused for 30 seconds, then tried again. Each failed try doubles the pause, up to 10 minutes. One answered event ends it with the notice `plugin 'besydr' answers again`.
- A plugin that cannot be started is off for that session; the next session tries again.
- Notices go to standard error, only when it is a terminal and the format is not `jsonl`. A paused or unstartable plugin is also reported by `octomind run` as an error on standard error, and by the ACP and WebSocket servers in their log file.

## Examples

### Example 1: switching the plugin off

Bad: `supervisor.enabled = false` in `config.toml`, or `-c supervisor.enabled=false`. Octomind rejects the key.

Good: `enabled = false` on the `besydr` entry in `plugins`, or `-c 'plugins=[]'` for one run.

### Example 2: switching off one part

Bad: looking for a `[condense]` or `[supervisor.condense]` table in `config.toml`.

Good: set `condense.enabled = false` (or `tokens_threshold = 0`) in Besydr's file; `besydr config` shows where it is.

### Example 3: "the agent keeps redoing the same thing"

Two things can act. Besydr's loop note is advice only. The hard stop is Octomind's `max_identical_rounds`, which ends the turn. Name which one fired before suggesting a change.

### Example 4: "why was my turn sent back?"

Most likely the completion check found gaps. The message lists them. Turn it off with `gate.enabled = false` in Besydr's file.

## Checklist

- [ ] Told the user that Octomind has no supervisor and Besydr does the work as a plugin?
- [ ] Plugin switched in `config.toml` (`plugins` entry), Besydr parts switched in Besydr's file?
- [ ] Behaviour attributed to the right part (completion check, tool admission, condensing, loop note, `max_identical_rounds`) before recommending a change?
- [ ] For `/learning` or `/plan` problems: checked that the plugin is connected?
- [ ] Old `[supervisor]` settings: pointed to `besydr-carry/supervisor.toml` and Besydr's file, not to `config.toml`?

## Composition / References

- Pairs with `octomind-config` for the root key `plugins` and the rest of `config.toml`.
- Pairs with `octomind-cli` for `/done`, `/plan`, `/learning` and `/info`.
- Octomind docs: `doc/usage/14-supervisor.md`, `doc/usage/13-learning.md`, `doc/integration/05-plugins.md`, `doc/troubleshooting/02-migration-guide.md`.
- Besydr docs: `https://besydr.com/docs` (mechanics, learning, configuration).
