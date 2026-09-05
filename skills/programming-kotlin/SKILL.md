---
name: programming-kotlin
title: "Kotlin Development"
description: "Idiomatic Kotlin — null-safety, coroutine ownership, Flow delivery, and Android/Multiplatform boundaries. Auto-activates in Kotlin projects."
license: Apache-2.0
compatibility: "Requires the project's Kotlin toolchain; JDK for JVM targets, Android SDK for Android, platform tools for Native targets."
domains: developer
rules:
  - file(build.gradle.kts)
  - file(settings.gradle.kts)
  - content(kotlin)
---

## Overview

Use for Kotlin implementation and review across JVM, Android, and Multiplatform projects. Prefer concise expressions with visible ownership and failure semantics; preserve the repository's architecture and toolchain constraints.

## Mental model

Nullability describes absence, immutability describes ownership, and coroutine scopes describe lifetime. These are separate contracts: `val`, `List`, and `suspend` do not by themselves guarantee immutable data, thread safety, or background execution.

## Version gate

Verified 2026-09-05: Kotlin 2.4 is the stable language line. It stabilizes context parameters, explicit backing fields, and annotation use-site target changes. Explicit context arguments, context-parameter callable references, and collection literals remain experimental. Check the actual compiler, language/API version, Gradle plugin, JVM target, and platform compatibility before using new syntax.

Use context parameters for an existing contextual API need, not to obscure ordinary constructor dependencies. Explicit backing fields can expose a narrower public type without a second property. New annotation targeting can affect frameworks and generated code; verify effective targets during upgrades. Do not enable experimental features merely to shorten an example.

## Values and readable APIs

- Prefer `val`, but remember it fixes the reference, not its contents. `List<T>` is a read-only interface that may alias mutable storage; snapshot at ownership boundaries. Data-class `copy()` is shallow.
- Use data classes for values and sealed types for closed outcomes. Exhaustive `when` without a default exposes newly added cases; don't fabricate an unknown case unless external input really needs one.
- Normalize Java platform types at the interop boundary. Use `require` for invalid arguments and `check` for invalid state; `!!` needs a proven invariant, not optimism about input.
- Nullable returns represent expected absence. Don't use `?: emptyList()`, `getOrDefault`, or `runCatching` to turn parsing or network failures into valid-looking data.
- Prefer named arguments and small functions over nested scope functions. Use `let`, `apply`, and `also` only when their receiver and result remain obvious. Extensions should reveal domain vocabulary without hiding I/O in property-like access.
- Write explicit public return types. Prefer straightforward collections until sequence laziness or reduced intermediates benefits the actual workload; sequences are not automatically faster.

## Coroutines and streams

- Launch into a scope with an owner and cancellation policy. Use `coroutineScope` for related work that should fail together; supervision isolates child failures only when each failure has a handler. Avoid ownerless GlobalScope work.
- `suspend` does not switch threads. Blocking functions used by UI callers must move blocking work to an appropriate injected dispatcher; already-suspending network APIs usually need no IO wrapper. CPU-heavy work belongs on a suitable computation dispatcher.
- Propagate `CancellationException`; broad catches and `runCatching` can capture it. Long computations must check cancellation. Use `NonCancellable` only for narrowly bounded suspending cleanup, not to keep normal work alive.
- Await async results and bound fan-out when inputs are unbounded. A structured child can fail its parent before await; ignoring Deferred is not an error-handling policy.
- A `flow {}` is cold; StateFlow/SharedFlow are hot. StateFlow conflates equal values, so update with immutable snapshots and `update` for concurrent read-modify-write.
- SharedFlow is a broadcast mechanism, not durable event storage: with no subscribers, only replay values survive. Model important UI outcomes as state or an acknowledged durable operation when losing them would be incorrect.
- Use `callbackFlow` with `awaitClose` to unregister callbacks. Choose buffering and overflow behavior explicitly; don't silently drop business-critical values.

## Platform boundaries and verification

- Android: hoist Compose state and collect flows with lifecycle-aware APIs. Preserve functioning Views-based code; toolkit adoption is not an instruction to rewrite unrelated screens. Keep long-lived work out of view-owned scopes.
- Multiplatform: share logic that is actually portable; keep `expect`/`actual` seams small. Check each library's supported targets and stability rather than assuming JVM availability implies Native availability.
- Follow existing serialization, formatting, and test libraries. Test coroutine behavior with `runTest` and dispatchers sharing its test scheduler; cover cancellation, delayed collectors, and errors, not only successful emissions.

## Example

Keep cancellation distinct from a recoverable network failure:

```kotlin
import java.io.IOException

suspend fun <T> loadOrReport(
    load: suspend () -> T,
    report: (IOException) -> Unit,
): T {
    try {
        return load()
    } catch (failure: IOException) {
        report(failure)
        throw failure
    }
}
```

This JVM boundary reports only I/O failures; cancellation passes through unchanged. In ordinary lower-level code, simply propagate failures without catching.

## Checklist

- [ ] New syntax fits compiler, plugins, and target; experiments are explicit.
- [ ] Read-only interfaces do not leak unintended mutable aliases.
- [ ] Coroutine lifetime, cancellation, and stream delivery are defined.
- [ ] Absence and failure are distinct; fallback behavior is contractual.
- [ ] Relevant checks were run when authorized; skipped checks are stated.

## References

- [Release process](https://kotlinlang.org/docs/releases.html) and [Kotlin 2.4 changes](https://kotlinlang.org/docs/whatsnew24.html)
- [Collections](https://kotlinlang.org/docs/collections-overview.html)
- [Coroutine practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices)
- [SharedFlow contract](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-shared-flow/)
