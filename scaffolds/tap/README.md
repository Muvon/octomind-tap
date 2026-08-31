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
| `__AGENT_DOMAIN__` | `team` unless overridden with `--agent` |
| `__AGENT_SPEC__` | `assistant` unless overridden with `--agent` |
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
   agent runs immediately: `octomind run <domain>:<spec>`.

## Design boundary

The scaffold copies the tap architecture and authoring foundation, not the
community catalog. It includes one local `core` capability so the starter
agent works with the current source-tap-local static capability resolver.
Public agents, skills, workflows, capabilities, and dependency installers are
not copied.

