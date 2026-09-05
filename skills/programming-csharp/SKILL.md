---
name: programming-csharp
title: "C# / .NET Development"
description: "Modern C# and .NET: nullable contracts, async ownership, data access, and explicit failure handling. Auto-activates in .NET projects."
license: Apache-2.0
compatibility: "Requires the project's modern .NET SDK and target framework; newer language/API features are version-gated."
domains: developer
rules:
  - file(*.sln)
  - file(*.csproj)
  - file(global.json)
  - file(Directory.Build.props)
  - content(c#)
  - content(csharp)
  - content(dotnet)
---

## Overview

Use for modern .NET implementation and review, including libraries and services. Write explicit contracts with the existing framework and project conventions; avoid adding architecture or replacing working tools as incidental cleanup.

## Mental model

The compiler checks declared contracts, while runtime boundaries still validate real input. Keep values, service lifetimes, asynchronous work, and database units of work explicit; concise syntax is useful when it makes these easier to inspect.

## Version gate

Verified 2026-09-05: .NET 10 LTS and C# 14 are stable. Check `global.json`, target frameworks, `LangVersion`, nullable settings, and CI SDKs before selecting APIs. Don't set `latest` or `preview` to make an example compile; the target framework's default language version normally supplies the supported pairing.

C# 12 supplies primary constructors and collection expressions. C# 14 adds extension members, field-backed property accessors using `field`, and null-conditional assignment. Use them where ownership remains clear: a primary-constructor parameter is not automatically a property, and `obj?.Property = value` deliberately skips an update when null rather than validating a required receiver.

## Values and public contracts

- Enable nullable analysis for new code; migrate existing projects within scope. Nullable annotations and `!` have no runtime validation effect. Check deserialized data and public inputs; suppress warnings only for an invariant the compiler cannot express.
- Use records for value semantics and ordinary classes for identity. `init`, `readonly`, and record `with` do not freeze referenced objects; copy or use immutable collections when ownership requires isolation. EF entities usually need reference identity.
- A `required` member requires initialization by callers; it does not prove a non-null or domain-valid value. Validate invariants in constructors/factories or the established validation boundary.
- Use pattern matching for clear closed decisions. An enum can contain unnamed numeric values; reject unknown external values rather than assuming switch coverage proves input validity.
- Follow `.editorconfig` for braces and namespace style. Use LINQ for readable transformations; account for deferred execution and repeated enumeration. Don't replace a clear loop with a chain of side effects.
- Keep generic abstractions, interfaces, and result wrappers proportional to the boundary. Use existing dependency injection and error conventions consistently.

## Async and resource ownership

- Await asynchronous I/O through the call chain. Avoid `.Result`, `.Wait()`, and sync-over-async wrappers; don't use `Task.Run` to wrap naturally asynchronous I/O.
- Pass cancellation tokens to operations that can cancel, including HTTP, database calls, and async enumeration. Treat caller cancellation separately from an operational failure or timeout.
- `Task.WhenAll` is suitable for independent bounded work; it does not automatically cancel siblings. Give fan-out a concurrency limit and define partial-failure handling.
- Own background work with the application's background-service/lifecycle mechanism. `async void` is for required event-handler signatures; observe other work through Task-returning APIs.
- Use `ConfigureAwait(false)` where library code must avoid a caller's synchronization context; keep context when UI code needs it. It does not move work to a dedicated background thread.
- Dispose owned resources with `using`/`await using`. Don't dispose injected resources owned by the container. Reuse HTTP connections via a long-lived HttpClient with appropriate `PooledConnectionLifetime` or factory-managed clients; per-request client construction is not the default.

## Services, persistence, and failures

- Match DI lifetime to ownership. Don't capture scoped services in singletons; create a scope for each background unit of work. Validate required configuration early instead of silently substituting defaults.
- DbContext is a unit of work and is not thread-safe. Await each operation or use separate contexts for actual parallel operations. Keep transactions and optimistic-concurrency behavior explicit.
- For EF reads, project only needed columns and use no-tracking when identity/change tracking is unnecessary. Inspect SQL for N+1 queries and pagination; an in-memory provider does not verify production SQL semantics.
- Catch exceptions where recovery or translation is meaningful; preserve the stack with `throw;`. Log structured context once at the responsible boundary. Don't convert canceled, unauthorized, or failed operations into empty successful responses.
- Retry only bounded transient failures when the operation is safe to repeat. Test failure and cancellation paths with the existing test framework; don't add a new assertion library by habit.

## Example

An injected, reused HttpClient keeps ownership outside this operation while failures remain visible:

```csharp
using System.Net.Http.Json;

public sealed record Profile(string Name);

public static class Profiles
{
    public static async Task<Profile> LoadAsync(
        HttpClient client, Uri uri, CancellationToken cancellationToken)
    {
        var profile = await client.GetFromJsonAsync<Profile>(
            uri, cancellationToken).ConfigureAwait(false);
        if (profile is null || string.IsNullOrWhiteSpace(profile.Name))
            throw new InvalidDataException("Profile requires a name.");
        return profile;
    }
}
```

The .NET SDK's implicit usings are assumed. HTTP, JSON, and cancellation failures propagate; validation rejects a missing or invalid payload.

## Checklist

- [ ] Syntax and APIs fit SDK, language version, and target frameworks.
- [ ] Nullability, required members, and external validation agree.
- [ ] Async operations, cancellation, disposal, and DI lifetimes have owners.
- [ ] Database concurrency and failure semantics remain explicit.
- [ ] Relevant checks were run when authorized; omissions are reported.

## References

- [.NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview) and [C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)
- [Nullable references](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references) and [record semantics](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record)
- [HttpClient lifetimes](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines)
- [DbContext ownership](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/)
