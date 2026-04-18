---
name: programming-elixir
title: "Elixir Development"
description: "Elixir/OTP conventions, pattern matching, GenServer, supervision trees, Phoenix, and functional programming best practices. Auto-activates in Elixir projects."
license: Apache-2.0
compatibility: "Requires Elixir and Erlang/OTP."
domains: developer
---

# Elixir Development

## Conventions

- Idiomatic Elixir — pattern matching over conditionals, pipes over nesting
- "Let it crash" — don't defensively catch errors; let supervisors restart
- `{:ok, _}` / `{:error, _}` tuples — NOT exceptions for control flow
- Immutability — all data is immutable; "updating" returns new data
- OTP first — use GenServer/Supervisor/Agent/Task
- `@impl true` on ALL behaviour callbacks
- `defp` for internal functions — only expose what's needed
- `@spec` on all public functions

## Pattern Matching

- Multi-clause functions over `if`/`else`/`case` nesting
- Destructure in function arguments — not inside body
- Guards (`when is_binary/is_integer`) for type constraints

## Pipe Operator

- Data flows left to right: `user |> Map.get(:email) |> String.downcase()`
- First argument is always piped
- Use `then/1` when piped value isn't the first argument

## Error Handling

- `with` blocks for chaining failable operations
- `{:ok, _}` / `{:error, _}` for expected failures
- `raise`/`rescue` ONLY at system boundaries
- Provide context: `{:error, {:not_found, id}}`

## OTP Patterns

- GenServer: always provide client API wrapping `GenServer.call`/`cast`
- Supervisor: `:one_for_one` default, `:rest_for_one` for dependent children
- Agent: for simple state when GenServer is overkill
- Task / Task.Supervisor: for async one-off work
- DynamicSupervisor: for children started at runtime

## Testing

- ExUnit with `async: true` for concurrent tests
- `describe` blocks to group related tests
- `setup` / `setup_all` for fixtures
- `assert` with pattern matching: `assert {:ok, %User{}} = fetch_user(id)`
- Mox for behaviour-based mocking

## Common Pitfalls

- `%{map | key: val}` only updates EXISTING keys — use `Map.put/3` for new
- Atoms from user input are never GC'd — use `String.to_existing_atom/1`
- Enum vs Stream: use Stream for large/lazy collections

## Tooling

| Command | Purpose |
|---------|---------|
| `mix compile` | Compile |
| `mix test` | Run tests |
| `mix format` | Format code |
| `mix format --check-formatted` | CI format check |
| `mix credo --strict` | Lint |
| `mix dialyzer` | Static type analysis |
| `mix deps.get` | Fetch dependencies |
| `mix phx.server` | Phoenix dev server |
