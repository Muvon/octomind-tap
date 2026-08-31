# Capabilities

Capabilities are the only supported way for agents to declare tools and
dependencies. Create providers at:

```text
capabilities/<name>/<provider>.toml
```

Add `config.toml` for discovery triggers and point `default.toml` at the active
provider with a relative symlink. Start from `templates/capability.toml`.

The scaffold includes only `core`, which is sufficient for the starter agent.
It intentionally does not copy the community capability catalog.

