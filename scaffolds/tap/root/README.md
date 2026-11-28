# __TAP_ID__

An Octomind tap for private or public agents, capabilities, skills, dependency
installers, and workflows.

This repository was created from the official user-tap scaffold maintained by
the Octomind community tap.

## Start

The scaffold includes one runnable agent:

```bash
octomind run __AGENT_NAME__
```

When working from a checkout that has not been registered yet:

```bash
octomind tap __TAP_ID__ "$(pwd)"
octomind run __AGENT_NAME__
```

Validate the repository after changes:

```bash
bash scripts/check.sh
```

## Contents

| Path | Purpose |
|------|---------|
| `agents/<ns>/default.toml` | Base agent of a namespace, tag `<ns>`; `agents/<ns>/<variant>.toml` adds a variant with the tag `<ns>:<variant>` |
| `agents/<ns>/skills/<skill>/SKILL.md` | Skills used by that namespace: its base agent and every variant |
| `capabilities/<name>/` | Tool and dependency providers used by agents and skills |
| `deps/<org>/<tool>.sh` | Idempotent dependency installers and companion documentation |
| `skills/<skill>/SKILL.md` | Skills shared by two or more namespaces, bound with `domains:` |
| `workflows/<name>.toml` | Multi-step pipelines run with `octomind workflow` |
| `templates/` | Starting points for new tap artifacts |
| `scripts/check.sh` | Local and CI validation entrypoint |

`AGENTS.md` is the operational source of truth for humans and coding agents
working in this repository.

## Add an artifact

Create an agent:

```bash
mkdir agents/<name>
cp templates/agent.toml agents/<name>/default.toml
```

Create a skill that only that namespace uses:

```bash
mkdir -p agents/<name>/skills/release-process
cp templates/skill.md agents/<name>/skills/release-process/SKILL.md
```

A skill that two or more namespaces use goes in `skills/<skill>/SKILL.md` instead, with
`domains:` naming those namespaces.

Add a variant, `agents/<name>/<variant>.toml` with the tag `<name>:<variant>`,
only when a skill cannot do the job: the agent needs its own system prompt and
identity, its own capability set (fewer or different tools), its own model, or
its own safety rules. Extra instructions, or extra tools on top of the base
agent, are a skill; `capabilities:` in its frontmatter brings tools. A new field
of work is a new agent directory. `AGENTS.md` has the full rules.

For a capability, dependency installer, or workflow, start from the matching
file under `templates/` and follow `AGENTS.md`.

The Octomind tap authoring agent can also maintain this repository:

```bash
octomind run octomind
```

## Publish

Octomind maps tap id `__TAP_ID__` to GitHub repository
`__TAP_OWNER__/__TAP_REPOSITORY__`.

```bash
gh repo create __TAP_OWNER__/__TAP_REPOSITORY__ --private --source=. --push
```

Other users can then install it with:

```bash
octomind tap __TAP_ID__
```

Change `--private` to `--public` only when every included artifact and secret
reference is safe to publish.
