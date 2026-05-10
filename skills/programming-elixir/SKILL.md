---
name: programming-elixir
title: "Elixir Development"
description: "OTP-first architecture, pattern matching, supervision design, and Phoenix conventions. Auto-activates in Elixir projects."
license: Apache-2.0
compatibility: "Requires Elixir and Erlang/OTP."
domains: developer
rules:
  - file(mix.exs)
  - content(elixir)
---

## Mental model

Elixir is a functional language built on the BEAM, a runtime designed for concurrency, isolation, and fault tolerance. The big architectural lever is OTP — supervision trees and lightweight processes — not language features. "Let it crash" is not a slogan; it's the design: code the happy path, let supervisors restart on failure, and avoid defensive programming. Most maintenance pain comes from treating processes like threads, from rescuing too eagerly, and from spreading business logic across GenServers when plain modules would do.

## Functional core

- Pure functions in modules form the bulk of a codebase; processes are for state, isolation, and concurrency — not for organization
- Multi-clause functions with pattern matching replace `if`/`else`/`case` chains
- Pipe (`|>`) when data flows linearly; `then/2` when the value isn't the first argument
- `with` for happy-path chains of `{:ok, _}` / `{:error, _}` — the canonical control-flow construct for fallible pipelines
- Tagged tuples for return values: `{:ok, value}` / `{:error, reason}` — never raise for expected outcomes
- Structs (`defstruct`) for typed data; `@type` and `@spec` on the public API

## OTP architecture

- A supervision tree is the application skeleton — children listed in the `Application` module's `start/2`
- Each process has one job; if a process needs to do two things, it's two processes
- `GenServer` for stateful services with a clear public API (`MyServer.call(...)` wrapping `GenServer.call`)
- `DynamicSupervisor` for children started at runtime; `PartitionSupervisor` for sharded workloads
- `Task` and `Task.Supervisor` for one-shot async work
- Choose restart strategies deliberately: `:one_for_one` for independent children, `:rest_for_one` when later children depend on earlier ones
- Let processes crash on unexpected input — the supervisor restarts cleaner state than rescue blocks paper over

## Concurrency patterns

- Processes are cheap (millions on a node) — spawn freely when isolation helps
- Send messages, don't share state; the BEAM gives you message-passing for free
- Long-running work in a `Task` under a supervisor, not in a controller or LiveView callback
- Backpressure via GenStage / Flow / Broadway when producers can outpace consumers
- Time-outs on every `GenServer.call`; the default 5 seconds is rarely what you want for slow operations

## Error handling

- `with` for chained fallible operations — one path for success, one clause per failure shape
- Tagged tuples for expected failures; `raise` only for genuinely exceptional conditions
- Provide context in errors: `{:error, {:not_found, %{type: :user, id: id}}}` beats `{:error, :not_found}`
- Rescue at system boundaries (HTTP handlers, message consumers) where you must respond to the outside world

## Ecto and persistence

- Schemas describe database shape; changesets validate and cast at the boundary
- Keep query composition explicit: small named functions returning queryables, composed at the call site
- Multi-step writes use `Ecto.Multi` so the whole transaction rolls back on failure
- Avoid putting business logic in changesets — they validate data, they don't make decisions
- Migrations are forward-only in production; design rollback as a new migration

## Phoenix and LiveView

- Contexts (`Accounts`, `Billing`, `Inventory`) are the public API for a domain — controllers and LiveViews call contexts, not Ecto directly
- LiveView holds UI state in `socket.assigns`; long work goes to a `Task` and streams results back via `handle_info`
- Streams (`stream/3`) for large lists — they avoid sending the full collection on every diff
- Channels for low-level WebSocket needs that LiveView doesn't fit
- Function components and slots for composable UI; keep template logic minimal

## Testing

- ExUnit with `async: true` for tests that don't touch shared state — the BEAM's isolation makes most tests parallelizable
- Pattern-match in `assert`: `assert {:ok, %User{name: "Ada"}} = create_user(params)`
- `describe` blocks group tests around a function; `setup` and `setup_all` for fixtures
- Mox for behaviour-based mocks; define a behaviour, swap implementations in tests
- Test contexts and pure modules directly; LiveView/controller tests are integration tests

## Common pitfalls

- `%{map | key: val}` only updates existing keys — `Map.put/3` for new
- `String.to_atom/1` on user input leaks memory (atoms aren't garbage-collected) — use `String.to_existing_atom/1`
- `Enum` materializes; `Stream` is lazy — use `Stream` for large or infinite sequences
- A `GenServer` that calls itself synchronously deadlocks — use `cast`, or restructure
