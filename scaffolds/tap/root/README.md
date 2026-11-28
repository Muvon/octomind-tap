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
| `agents/<name>/config.toml` | Runnable agent manifests, one directory per agent |
| `agents/<name>/skills/<skill>/SKILL.md` | Skills used by that agent only |
| `capabilities/<name>/` | Tool and dependency providers used by agents and skills |
| `deps/<org>/<tool>.sh` | Idempotent dependency installers and companion documentation |
| `skills/<skill>/SKILL.md` | Skills shared by two or more agents, bound with `domains:` |
| `workflows/<name>.toml` | Multi-step pipelines run with `octomind workflow` |
| `templates/` | Starting points for new tap artifacts |
| `scripts/check.sh` | Local and CI validation entrypoint |

`AGENTS.md` is the operational source of truth for humans and coding agents
working in this repository.

## Add an artifact

Create an agent:

```bash
mkdir agents/<name>
cp templates/agent.toml agents/<name>/config.toml
```

Create a skill that only that agent uses:

```bash
mkdir -p agents/<name>/skills/release-process
cp templates/skill.md agents/<name>/skills/release-process/SKILL.md
```

A skill that two or more agents use goes in `skills/<skill>/SKILL.md` instead, with
`domains:` naming those agents.

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
