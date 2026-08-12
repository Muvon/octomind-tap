---
name: programming-csharp
title: "C# / .NET Development"
description: "Modern idiomatic C# — nullable reference types, records, async discipline, minimal APIs, and EF Core patterns. Auto-activates in .NET projects."
license: Apache-2.0
compatibility: "Requires .NET SDK 8+ (LTS) — modern cross-platform .NET, not .NET Framework."
domains: developer
rules:
  - file(global.json)
  - file(Directory.Build.props)
  - content(csharp)
  - content(dotnet)
---

## Mental model

Modern .NET is cross-platform, fast, and batteries-included — the framework almost always already has the thing (DI, config, logging, HTTP, JSON, testing hooks). C# rewards using its current idioms: file-scoped namespaces, records, pattern matching, nullable reference types. The main anti-patterns are .NET-Framework-era habits (service locators, `.Result` blocking, config soup) and fighting the framework instead of composing with it.

## Language — write current C#

- Nullable reference types ON (`<Nullable>enable</Nullable>`) in every project; treat warnings as errors — `null` bugs move to compile time. Never silence with `!` where a real check belongs
- Records for immutable data (`record Order(string Id, decimal Total)`); `with` expressions for updates; classes for identity + behavior
- Pattern matching over type-checks: switch expressions, property patterns (`order is { Total: > 100, Status: OrderStatus.Paid }`), list patterns where they clarify
- Primary constructors and collection expressions (`[1, 2, ..rest]`) in new code; file-scoped namespaces always
- LINQ for querying and transformation; a `foreach` when it's clearer or hot-path (LINQ allocates) — measure before optimizing either way
- `Span<T>`/`Memory<T>` only where profiling justifies it — correctness first, then allocations

## Async discipline (where .NET codebases die)

- async all the way down: never `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` on async code — that's the classic deadlock + threadpool-starvation combo
- `CancellationToken` parameters flow through every async public API and reach the actual I/O call
- Library code: `ConfigureAwait(false)`; application code (ASP.NET Core has no sync context): don't bother
- `IAsyncEnumerable<T>` for streams; `Task.WhenAll` for genuine parallel fan-out; `ValueTask` only on proven hot paths
- Fire-and-forget is a bug until proven otherwise — unobserved task exceptions vanish; use a background service or at minimum log continuations

## Architecture defaults

- Built-in DI with constructor injection; lifetimes deliberate: singleton for stateless services, scoped for per-request state, transient rarely — never resolve scoped from singleton (captive dependency)
- Options pattern (`IOptions<T>` bound to config sections) over raw `IConfiguration` reads scattered through code
- Minimal APIs for services and small apps; controllers when filters/conventions/versioning earn their weight — match the repo
- One `HttpClient` policy: `IHttpClientFactory` always — naked `new HttpClient()` per request exhausts sockets
- Structured logging via `ILogger<T>` with message templates (`"Order {OrderId} failed"`) — never string interpolation into log calls

## EF Core without surprises

- `AsNoTracking()` for read-only queries — tracking is the default and costs memory
- Project to DTOs in the query (`Select`) rather than loading entities and mapping after
- N+1 is the classic failure: eager-load deliberately (`Include`) or restructure the query; log/inspect generated SQL for anything hot
- Migrations in version control, applied deliberately (not `EnsureCreated` in production); no lazy-loading proxies in new designs

## Errors

- Exceptions for exceptional; catch specifically, enrich with context, rethrow with `throw;` (never `throw ex;` — it resets the stack trace)
- Result-object patterns only as a whole-team convention, not a per-file experiment
- `using`/`await using` declarations for disposables; implement `IAsyncDisposable` where cleanup does I/O

## Testing

- xUnit as the default runner; assertion library per repo convention (note: FluentAssertions v8+ moved to a paid license for commercial use — check before adding it; xUnit asserts or its forks cover most needs)
- `[Theory]` + `[InlineData]`/`[MemberData]` for input matrices — the table-driven idiom
- Integration tests with `WebApplicationFactory<T>` hitting the real pipeline; Testcontainers for real databases
- Mock only process boundaries you don't own; in-memory EF provider lies about SQL semantics — use SQLite in-memory or Testcontainers instead
