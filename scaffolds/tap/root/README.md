# __TAP_ID__

An Octomind tap for private or public agents, capabilities, skills, dependency
installers, and workflows.

This repository was created from the official user-tap scaffold maintained by
the Octomind community tap.

## Start

The scaffold includes one runnable agent:

```bash
octomind run __AGENT_DOMAIN__:__AGENT_SPEC__
```

When working from a checkout that has not been registered yet:

```bash
octomind tap __TAP_ID__ "$(pwd)"
octomind run __AGENT_DOMAIN__:__AGENT_SPEC__
```

Validate the repository after changes:

```bash
bash scripts/check.sh
```

## Contents

| Path | Purpose |
|------|---------|
| `agents/<domain>/<spec>.toml` | Runnable agent manifests |
| `capabilities/<name>/` | Tool and dependency providers used by agents and skills |
| `deps/<org>/<tool>.sh` | Idempotent dependency installers and companion documentation |
| `skills/<name>/SKILL.md` | Reusable AgentSkills instruction packs |
| `workflows/<name>.toml` | Multi-step pipelines run with `octomind workflow` |
| `templates/` | Starting points for new tap artifacts |
| `scripts/check.sh` | Local and CI validation entrypoint |

`AGENTS.md` is the operational source of truth for humans and coding agents
working in this repository.

## Add an artifact

Create an agent:

```bash
mkdir -p agents/developer
cp templates/agent.toml agents/developer/backend.toml
```

Create a skill:

```bash
mkdir -p skills/release-process
cp templates/skill.md skills/release-process/SKILL.md
```

For a capability, dependency installer, or workflow, start from the matching
file under `templates/` and follow `AGENTS.md`.

The Octomind tap authoring agent can also maintain this repository:

```bash
octomind run octomind:tap
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

