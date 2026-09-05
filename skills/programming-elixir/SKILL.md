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

## Overview

Write Elixir as clear data transformations with explicit process and failure ownership. Research baseline: 2026-09-05, Elixir 1.20 stable, with gradual compiler type inference across language constructs. Inspect the project's Elixir/Erlang requirements and locked Phoenix/Ecto versions first. Elixir 1.20 requires OTP 27+; select a documented compatible pair rather than independently upgrading runtimes.

## Mental model

Modules organize behavior; processes own concurrent activity and state. Supervision restores failed processes, not lost database transactions or external side effects. Validate untrusted input and represent expected failures explicitly; let unexpected defects fail where a deliberate supervision boundary can handle them.

## Functions, data, and current typing

- Use functions and pattern matching for ordinary domain logic. A GenServer is not required to encapsulate a module or make it "OTP-first."
- Use clauses and guards when they clarify accepted shapes. Validate untrusted input before entering functions whose patterns assume internal invariants; don't add catch-all success defaults to hide malformed data.
- Keep `{:ok, value}`/`{:error, reason}` contracts consistent. Use `with` for dependent fallible steps, but normalize ambiguous failure shapes in their owning functions. A large `else` reconstructing which step failed signals unclear contracts.
- Use `case` for branching and pipes for linear transformations; do not force every condition into `with`. Keep error reasons useful to callers without leaking sensitive input.
- Elixir 1.20 infers types through expressions, guards, clauses, and dependency information. Treat verified-bug/dead-code warnings as evidence to investigate. This is not complete compile-time proof of program correctness.
- Keep `@spec` and `@type` for documented contracts and existing analysis tools. Do not invent new set-theoretic annotation syntax: user-supplied signatures and typed structs for that system remain future work in the 1.20 release.
- Structs provide a known shape, not automatic field validation. Use changesets or explicit constructors for boundary checks; `@enforce_keys` does not validate values.
- Keep external keys as strings or map them through an explicit allowlist. Unbounded `String.to_atom/1` can exhaust the atom table; `to_existing_atom/1` still raises and does not prove an atom is allowed for this operation.
- Use `Stream` for deferred traversal when needed; consume it deliberately. Avoid assuming laziness removes the memory cost of a later full materialization.

## Process and task ownership

- Introduce a GenServer when serial access to state or a managed lifecycle is needed. Long callbacks block its mailbox; move independent work to supervised tasks with explicit result handling.
- Choose supervision strategy from dependency relationships: `:one_for_one` for independent children, `:rest_for_one` when later children depend on earlier ones. Specify restart/shutdown policy; a Task normally has temporary restart behavior.
- `Task.async` links caller and task, so task failure can terminate its caller. Use supervised `async_nolink` when that coupling is undesirable, and consume results, failures, and monitor messages.
- Bound fan-out with `Task.async_stream` or equivalent limits. Set concurrency according to downstream capacity, with a deliberate timeout policy. Lazy input alone does not make unbounded spawning safe.
- Task closures copy captured data into another process. Extract only required values; avoid capturing an entire LiveView socket or large state object.
- A `GenServer.call` timeout does not cancel work already accepted by the server. Account for uncertain completion before retrying a mutation; a cast provides no processing acknowledgement.
- Do not synchronously call a GenServer from itself; direct self-calls fail rather than becoming useful serialization. Keep internal computation in functions, or redesign the interaction.
- Supervision is not durable job storage. Work that must survive node loss needs the application's durable job mechanism and idempotent effects.

## Persistence and Phoenix boundaries

- Changesets cast allowed external fields, validate domain rules, and translate declared database constraint failures. Back race-sensitive invariants with actual database constraints; preflight checks alone are insufficient.
- Use `Ecto.Multi` for named dependent database operations when it improves clarity. Handle the failed operation and reason; returned `changes_so_far` contains prior operation results, while the transaction's database writes roll back. Transactions do not make external API calls reversible.
- Respect existing Phoenix context APIs so controllers and LiveViews share authorization and domain rules. Avoid blanket rules forbidding meaningful domain validation in changesets.
- Authorize protected operations on the server, including LiveView events. A hidden button and a successful initial mount do not establish ongoing authorization.
- In supported LiveView versions, use `assign_async`/`start_async` for lifecycle-managed work, with loading/error rendering. Capture needed values before starting work; avoid blocking callbacks with `Task.await`.
- Use streams for large changing collections when their identity/update model fits. They reduce retained collection state; they do not remove the need for query limits or pagination.

## Example

Accept only known external values without creating atoms or disguising errors:

```elixir
defmodule Visibility do
  @spec parse(term()) :: {:ok, :public | :private} | {:error, :invalid_visibility}
  def parse("public"), do: {:ok, :public}
  def parse("private"), do: {:ok, :private}
  def parse(_), do: {:error, :invalid_visibility}
end
```

The final clause returns an explicit expected failure. Internal callers can pattern-match the result without rescuing exceptions or silently selecting a default.

## Checklist

- Verify Elixir/OTP compatibility and supported library APIs.
- Keep process boundaries motivated by concurrency/lifecycle, not code organization.
- Check expected failures, compiler warnings, atom handling, and boundary validation.
- Check task links, bounded work, timeouts, duplicate effects, and transaction limits.
- Use installed formatter, compilation checks, ExUnit, and existing analysis tools when authorized. Format checks alone do not prove compilation or behavior; use async tests only when their shared resources are isolated.

## References

- [Elixir stable documentation](https://elixir-lang.org/docs/) and [1.20 typing release](https://elixir-lang.org/blog/2026/06/03/elixir-v1-20-0-released/)
- [Elixir 1.20 OTP requirements](https://elixir.hexdocs.pm/1.20.0/changelog.html)
- [Official code anti-patterns](https://elixir.hexdocs.pm/code-anti-patterns.html)
- [Task ownership and concurrency](https://elixir.hexdocs.pm/Task.html)
- [GenServer call semantics](https://elixir.hexdocs.pm/GenServer.html) and [supervision policies](https://elixir.hexdocs.pm/Supervisor.html)
- [Ecto changesets](https://ecto.hexdocs.pm/Ecto.Changeset.html) and [transactions with Multi](https://ecto.hexdocs.pm/Ecto.Multi.html)
- [LiveView async operations and streams](https://phoenix-live-view.hexdocs.pm/Phoenix.LiveView.html)
