# User Tap Scaffold

This directory is the canonical source for repositories created by:

```bash
octomind tap init <owner/name>
```

`scaffold.toml` defines the render contract. `root/` is copied to the new
repository after tokens are replaced in both paths and file contents.

## Render tokens

| Token | Example for `acme/team` |
|-------|--------------------------|
| `__TAP_ID__` | `acme/team` |
| `__TAP_OWNER__` | `acme` |
| `__TAP_NAME__` | `team` |
| `__TAP_REPOSITORY__` | `octomind-team` |
| `__AGENT_NAME__` | `team` unless overridden with `--agent <name>`; the starter agent's name |
| `__YEAR__` | Current four-digit year |

The renderer must fail if any `__TOKEN__` remains after rendering. It must
also refuse to write into a non-empty destination unless an explicit future
overwrite policy says otherwise.

The renderer reads through symlinks and writes real files, so files shared
with the community tap (e.g. `root/templates/*`, `root/deps/lib/platform.sh`)
exist once here and are symlinked from the repository root.

## After rendering

`octomind tap init` finishes the bootstrap in the destination directory:

1. Marks `[post_create] executable` entries executable.
2. Runs `[post_create] validate` (`bash scripts/check.sh`) and fails loudly
   on any error.
3. Runs `git init`.
4. Registers the directory as a local tap for `<owner/name>`, so the starter
   agent runs immediately: `octomind run <name>`.

The starter agent is the base agent `agents/<name>/default.toml`; its directory
`agents/<name>/` is the namespace `<name>`. A generated
tap accepts variants: `agents/<name>/<variant>.toml` is started with
`octomind run <name>:<variant>`, and `<name>:default` names the base agent.
`scripts/check.sh` checks the variant name, the `# Agent:` header and that a
variant carries no `# Uses:` header.

A variant is the exception, not the default. The generated `AGENTS.md` and
`README.md` tell the tap's authors to add one only when a skill cannot do the
job: the agent needs its own system prompt and identity, its own capability set
(fewer or different tools), its own model, or its own safety rules. Extra
instructions, or extra tools on top of the base agent, are a skill. A specialty
inside a field is a skill of that namespace, and a skill that two or more
namespaces use is shared. The community tap's own lint rejects variants
(`AGENT_VARIANT`); the generated `scripts/check.sh` accepts them.

## Design boundary

The scaffold copies the tap architecture and authoring foundation, not the
community catalog. It includes one local `core` capability for the starter
agent; other agents reference community capabilities as `octomind/<name>`,
which resolve from the baseline tap with their dependencies. Public agents,
skills, workflows, capabilities, and dependency installers are not copied.
