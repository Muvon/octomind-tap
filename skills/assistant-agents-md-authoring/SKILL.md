---
name: assistant-agents-md-authoring
title: "AGENTS.md Authoring: Thin Project Instructions"
description: "Create or update a thin AGENTS.md for any project: scan it, ask only what files cannot tell, and merge CLAUDE.md and .cursorrules into one file."
license: Apache-2.0
compatibility: "Reads the project directory. Code search tools help on software projects; memory is optional."
capabilities: codesearch-semantic codesearch-structural codesearch-graph
domains: assistant
rules:
  - match((?i)\b(create|write|generate|make|update|refresh|fix|improve|rewrite|add|produce|trim|slim|shrink|move|consolidate|merge|fold|migrate|convert)\b.{0,60}\b(agents\.md|agents md|agent instructions|project instructions|standing (instruction )?file)\b)
  - match((?i)\b(merge|consolidate|migrate|convert|fold)\b.{0,50}\b(claude\.md|\.cursorrules|copilot-instructions|gemini\.md|legacy instruction)\b)
  - match((?i)\bagents\.md\b.{0,60}\b(too long|bloated|thin|nested|root|pointers?|\.agents/)\b|\b(thin|nested|root)\b.{0,20}\bagents\.md\b)
  - match((?i)\b(relocate|move|put)\b.{0,50}\b(into|under|to)\b.{0,15}\.agents/)
  - semantic(write the instructions file coding agents read for my project, 0.72)
  - semantic(merge my cursor rules and claude file into one instructions file, 0.72)
  - semantic(slim down my bloated agent instructions file, 0.72)
  - semantic(scan this repo and draft a short guide for coding agents, 0.72)
---

## Overview

Study any project (software, content, data, infrastructure, research, legal) and distill it into the thin, standing instruction file the AGENTS.md open standard defines, interviewing the user only for what the files cannot tell. The skill covers producing or updating a project's AGENTS.md (root and nested), consolidating legacy instruction files into it, and placing overflow reference material under `.agents/`. It does not cover Octomind config and guardrails, tap artifacts, workflow pipelines, feature specs, or human-facing docs and READMEs.

## Mental model

The file answers three questions for any task: where to start, how to do the work here, how to prove it is done. Every line passes one test: would removing it cause an agent to make a mistake? If not, cut it.

## Rules

### Standard

AGENTS.md (https://agents.md) is the open format for guiding coding agents, stewarded by the Agentic AI Foundation (Linux Foundation) and read by Octomind, Codex, Copilot, Cursor, Gemini CLI and most others. Facts that shape every decision:

- Plain Markdown, no required fields, no size rule; the file is parsed as text.
- The closest AGENTS.md to the edited file wins; explicit chat instructions override everything. Agents such as Codex concatenate every file from the repo root down to the working directory, so a nested file adds to the root rather than replacing it. It holds only the delta, never a repeat.
- Budget: Codex stops reading at 32 KiB across that whole chain by default. Keep the root under 150 lines and each nested file shorter.
- Agents run the check commands listed in the file and fix failures before finishing, so the done-command belongs here.
- Octomind loads the working directory's AGENTS.md every session and discovers `.agents/skills/`, `.agents/tools/` and `.agents/guardrails.toml`; Codex also reads `.agents/skills/`.
- Bloat hurts: the ETH Zurich study "Evaluating AGENTS.md" (ICLR 2026) found context files often lower task success and raise inference cost by over 20%, LLM-generated ones worst, because agents obey every listed requirement. An LLM writing one is the risk; minimal, human-confirmed content is the defence.

### Phase 1: Autonomous discovery (silent)

Investigate before asking anything. First wave, all in parallel:

- List the root two levels deep, README, CONTRIBUTING and any docs/ directory.
- Instruction files: AGENTS.md and AGENTS.override.md (root and nested), CLAUDE.md, AGENT.md, GEMINI.md, .cursorrules, .cursor/rules/, .github/copilot-instructions.md, .windsurfrules, .aider.conf.yml, .gemini/settings.json.
- `.agents/` contents: skills, tools, guardrails.toml, reference docs.
- Manifests and task runners that reveal the type and the real commands (package.json, Cargo.toml, pyproject.toml, go.mod, Makefile, justfile, docker-compose, terraform).
- CI, lint, format and pre-commit configs. CI is the truth for what "checks pass" means, and whatever these tools enforce stays out of the file.

Second wave, by type: code, file outlines of entry points and tests plus a call-graph overview for module boundaries; content, templates and style guides; infra, environment configs and deploy scripts; data, schemas and quality checks; monorepo, what each package does differently from the root. Then separate what an agent could infer from what it could not. Only the second kind is a candidate line.

Before starting, recall project conventions, the instructions file, the done command, and agent mistakes from memory when available.

### Phase 2: Interview (only what the files cannot tell)

Present findings in one block, then ask one batch, skipping anything the files answered:

```
What I found
Project: [name] — [one line] · Type: [specific] · Stack: [languages, tools]
Commands: [build / test / lint with exact flags] · Done means: [checks that must pass]
Instruction files: [list, or none] · Packages needing their own AGENTS.md: [list, or none]
```

- Which commands or flags did I miss, and which listed ones are wrong?
- What environment quirks bite newcomers: services, secrets, versions, network, platform?
- What must never be done here: prohibitions that cause real damage, not preferences? Is any already blocked by CI, a hook or a guardrail?
- Which conventions differ from the ecosystem default, and where is the reference example to copy?
- What mistakes have agents or newcomers made that one rule would have prevented?
- Per legacy instruction file: merge into AGENTS.md and repoint it, or keep it separate?

Follow up once if a critical gap remains, then generate.

### Phase 3: Generate

Emit the file per the skeleton below. Depth that fails the cut test but is still needed sometimes goes under `.agents/`, linked with the trigger that should make an agent open it. After completing, memorize the project type, commands, conventions and prohibitions the user confirmed, when memory is available.

Commands, Done and Never are required; keep any other section only when it holds non-inferable content:

```markdown
# <Project> — AGENTS.md

<One sentence: what this is and the primary stack.>

## Commands
- Setup: `<exact>` · Dev: `<exact>` · Build: `<exact>`
- Single package (monorepo): `<exact, with the filter flag>`
- <Any command with a non-obvious flag, env var or order dependency>

## Where to look
| Task | Start here |
|------|------------|
| <common task type> | `path/` — <why> |
<Only entries an agent would not find by listing directories, plus reference examples to copy.>

## Conventions
- <Rule that differs from the ecosystem default and no tool enforces, one line each>
- Never edit `<generated path>` — regenerated by `<cmd>`

## Done
- `<exact command that must exit 0>` · `<second command>`
- <Non-command criteria: manual checklist, review gate>

## Gotchas
- <Quirks invisible from the files: ports, services, versions, flaky suites, sandbox network>

## Never
- <Hard prohibition, specific, one line each. "Never X", not "be careful with X">

## References
- `.agents/<topic>.md` — read when <trigger>
- `<package>/AGENTS.md` — package delta (monorepo)
```

Type-specific additions: an architecture line only when boundaries are non-obvious; the editorial gate for content; environment tiers and rollback for infra; schema location for data.

### Placement

- Per-feature behaviour, plans and decisions go in a spec. Here they rot and inflate context for unrelated work.
- Occasional depth (architecture notes, API conventions, migration playbooks) goes in `.agents/<topic>.md`, linked with its trigger; task-scoped packs go in `.agents/skills/<name>/SKILL.md`.
- A Never line is a reminder, not enforcement. When breaking it causes real damage, recommend a CI check, pre-commit hook or guardrail that blocks it; don't configure one.
- Legacy files: once the user agrees, merge them into AGENTS.md and repoint each tool: its own setting (Aider `read: AGENTS.md`, Gemini CLI `context.fileName`), else an import line, else a symlink. Skip symlinks when anyone works on Windows: they check out as plain text.
- AGENTS.override.md is a Codex-only temporary override: flag one if found, never generate one.

### Quality bar

1. Exact: commands copy-pasteable with flags; paths real; examples from this project.
2. Outcome over process: state what must be true and what is forbidden, not step-by-step how.
3. Honest: mark unverified claims `[UNCONFIRMED]`; never invent conventions.

### Modes

- "Generate instructions", "create AGENTS.md": Phase 1, then Phase 2.
- "Just generate", or a brief marked AUTONOMOUS: skip Phase 2 and write only the one-line summary, Commands, Done and Never, with `[UNCONFIRMED]` on anything not read verbatim from a manifest or CI config.
- "Update instructions": read the existing file, diff against the project and the user's report of what went wrong, add the preventing line, prune lines that fail the cut test or repeat a parent file.

## Output format

- Path: `AGENTS.md` at the project root; nested at `<package>/AGENTS.md`; overflow at `.agents/<topic>.md`.
- Existing AGENTS.md: show the diff and ask before overwriting; make targeted edits, not a regeneration.
- Show the full content and its line count before writing. After writing: "AGENTS.md written. When an agent makes a mistake a one-line rule would have prevented, add that line — that is the only reason this file should grow."

## Checklist

- [ ] Nothing inferable from code, manifests, CI or a directory listing is in the file.
- [ ] No per-feature content, history, motivation or marketing.
- [ ] Project type discovered first, not assumed to be software.
- [ ] Legacy files merged or repointed only with the user's yes.
- [ ] Where to look is precise and Done is executable.
- [ ] Root file under 150 lines; nested files hold only the delta.
