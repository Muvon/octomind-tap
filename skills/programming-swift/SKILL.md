---
name: programming-swift
title: "Swift Development"
description: "Modern Swift value semantics, API design, isolation, task ownership, and package compatibility. Auto-activates in Swift projects."
license: Apache-2.0
compatibility: "Requires the project's Swift toolchain; newer features are gated by compiler, language mode, and target platform."
capabilities: programming-swift
domains: developer
rules:
  - file(Package.swift)
  - content(swift)
---

## Overview

Use for Swift language implementation and review across packages, services, and apps. Keep platform UI, persistence, and distribution decisions in their platform context; focus here on values, APIs, concurrency, and explicit failures.

## Mental model

Value semantics control mutation; actor isolation controls access; task structure controls lifetime. None substitutes for the others. Make these contracts visible instead of quieting compiler diagnostics with unchecked annotations or detached tasks.

## Version and isolation gate

Verified 2026-09-05: Swift 6.3 is released; Apple's Xcode 27 beta lists Swift 6.4. Check the repository's toolchain, `swift-tools-version`, language mode, upcoming-feature flags, default isolation, and deployment targets separately. A Swift 6 compiler can compile in Swift 5 language mode.

- Swift 6 language mode enables data-race safety checks. Migrate boundaries deliberately; don't assume a toolchain upgrade changes the package's language mode.
- Swift 6.2 adds opt-in default MainActor isolation and `NonisolatedNonsendingByDefault`, under which nonisolated async functions inherit caller isolation. Read actual settings before inferring where a function runs. `async` does not mean background execution.
- `@concurrent` on supported toolchains explicitly moves eligible async work to the concurrent executor. Use it for computation that must leave an actor, not as an annotation on every async function.
- Swift 6.2 also introduces `InlineArray` and `Span`; use them for demonstrated fixed-storage or borrowing requirements. Swift 6.3 adds `@c` interoperability; prefer supported declarations over underscored attributes when the compiler and C contract permit them.

## Values and API design

- Prefer structs for independent values and enums with associated values for distinct states. Use classes for identity or shared lifecycle; don't impose reference semantics merely to enable inheritance.
- A struct containing a mutable class reference is not deeply independent. Keep mutation private, and validate invariants at creation rather than distributing checks through callers.
- Read APIs at their call sites. Labels should distinguish meaning (`remove(at:)` versus `remove(_:)`); expose minimal access and document non-obvious ownership, failure, or complexity contracts.
- Use generics or `some Protocol` when one concrete type remains statically determined. Use `any Protocol` for a heterogeneous existential contract; neither guarantees value semantics.
- Add protocols where substitution or a boundary is useful, not for every concrete type. Keep computed properties predictable; expensive or failing work usually deserves an explicit method.
- Model valid absence with Optional. Use `throws` for failures and typed throws only when a stable error set benefits callers; don't replace informative failures with `try?`, sentinel values, or empty collections.

## Concurrency and resource lifetime

- Actors protect isolated mutable state. Actor references can cross isolation boundaries; accessing isolated members requires the appropriate isolation, often `await`. Transfer data using Sendable values or valid ownership transfer, not unsafe shared references.
- An actor method can interleave with other work at each await. Recheck state after suspension when correctness depends on it; serial access does not make a multi-await operation atomic.
- Prefer `async let` and task groups for child work that belongs to the current operation. Bound large fan-out. A `Task {}` is unstructured and may inherit actor context; retain its handle when explicit cancellation or result observation is needed.
- `Task.detached` loses inherited context and structured cancellation. Use only for a deliberate independent boundary, with explicit lifetime and failure handling.
- Cancellation is cooperative. Propagate cancellation rather than displaying it as failure; check it in long computations and before publishing stale results. Don't assume cancellation guarantees an underlying callback or I/O operation stopped.
- Checked continuations must resume exactly once on every path; bridge cancellation and callback lifetimes explicitly. Use `defer` for synchronous cleanup and deliberate asynchronous cleanup where necessary.
- `@unchecked Sendable`, `nonisolated(unsafe)`, and force operations require a documented invariant; don't use them to bypass an unresolved ownership problem.

## Packages and checks

- Preserve the dependency manager and target layout. Create an SPM target only for a real reusable or independently testable boundary; macros require their supported compiler-plugin setup.
- Follow existing formatters and tests. Swift Testing supports modern unit tests; XCTest remains appropriate for existing suites, UI automation, and XCTest-specific facilities. Don't migrate tests merely for syntax.
- Test actor reentrancy, cancellation, and invalid input when affected. Distinguish source review from checks actually executed under the supported toolchain.

## Example

Keep an actor's invariant inside a non-suspending operation:

```swift
actor Inventory {
    private var available = 10

    func reserve(_ quantity: Int) -> Bool {
        guard quantity > 0, quantity <= available else { return false }
        available -= quantity
        return true
    }
}
```

A caller uses `await inventory.reserve(2)` across isolation. If remote authorization is added before mutation, state must be revalidated after that await or reserved with an explicit rollback protocol.

## Checklist

- [ ] Compiler, language mode, isolation flags, and deployment target are known.
- [ ] Value ownership and actor access remain correct across suspension.
- [ ] Every task and callback bridge has a lifetime and failure path.
- [ ] Absence, cancellation, and failure remain distinct.
- [ ] Relevant checks were run when authorized; skipped checks are stated.

## References

- [Swift 6.3](https://www.swift.org/blog/swift-6.3-released/) and [Swift 6.2](https://www.swift.org/blog/swift-6.2-released/)
- [Compiler and SDK matrix](https://developer.apple.com/xcode/system-requirements)
- [Concurrency](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)
- [Migration guide](https://www.swift.org/migration/documentation/swift-6-concurrency-migration-guide/incrementaladoption/)
- [API design guidelines](https://www.swift.org/documentation/api-design-guidelines/)
