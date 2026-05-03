---
name: programming-swift
title: "Swift Development"
description: "Swift 6 conventions, concurrency, SPM, macros, testing, and idiomatic patterns. Auto-activates in Swift package projects."
license: Apache-2.0
compatibility: "Requires Swift 6.0+ toolchain."
capabilities: programming-swift
domains: developer
rules:
  - file(Package.swift)
  - content(swift)
---

# Swift Development

## Conventions

- Swift 6 language mode for strict concurrency — opt into complete data-race safety (set `swiftLanguageMode: .v6` in Package.swift)
- Value types preferred — struct over class unless reference semantics required
- Protocol-oriented — protocol + extension over inheritance hierarchies
- Access control — default to private/internal, explicit public API surface
- @Sendable and actor isolation — mark closures and types crossing isolation boundaries
- Swift Testing over XCTest for new test targets
- Formatted — code must follow swift-format style
- SPM (Package.swift) for dependency management — no CocoaPods/Carthage for new projects

## Concurrency

- Strict concurrency checking — Swift 6 language mode enforces Sendable at compile time, data races become errors
- Actors for mutable shared state — prefer actor over class + lock
- async/await for all asynchronous code — no completion handlers in new code
- TaskGroup for structured parallel work — child tasks scoped to parent lifetime
- AsyncSequence / AsyncStream for event streams and bridging callback APIs
- @MainActor for UI-bound code — isolate all UI state mutations
- Sendable conformance — value types are Sendable by default, audit reference types
- Never block an actor — offload CPU-heavy work with a custom executor or explicit dispatch; Task.detached only to drop actor isolation inheritance
- Task cancellation — check Task.isCancelled, use try Task.checkCancellation() cooperatively

## Type System

- Typed throws (Swift 6) — `func parse() throws(ParseError)` for precise error signatures (single error type only)
- Noncopyable types (~Copyable) — single-ownership semantics for structs and enums only (classes cannot be ~Copyable)
- @Observable macro (Observation framework) — replaces ObservableObject/@Published
- Opaque types (`some Protocol`) for stable API return types — prefer over existentials
- Existential types (`any Protocol`) only when runtime polymorphism is needed
- Result builders for DSL construction — SwiftUI, RegexBuilder

## Macros

- Swift macros generate code at compile time — significant boilerplate reduction
- @attached macros modify declarations (@Observable, @Model), @freestanding macros are standalone expressions (#Predicate, #Preview)
- Use built-in macros first: @Observable, #Predicate, #Preview, @Model
- Custom macros require separate macro target in Package.swift with SwiftSyntax dependency
- Test macros with assertMacroExpansion — verify generated code

## Error Handling

- throws for recoverable errors — catch at appropriate call-site boundary
- Typed throws for library APIs — callers know exact error types without docs
- Result<T, E> for stored errors and async callback bridges
- try? for optional conversion when error details unneeded
- try! only in tests/prototypes — never in production paths
- Never fatalError in library code — return Result or throw

## Testing

- Swift Testing framework (@Test, #expect, @Suite) for all new test code
- XCTest for UI tests (XCUIApplication), performance tests (XCTMetric), and Objective-C test code
- #expect(expression) over XCTAssertEqual — better diagnostics and failure messages
- @Test(.tags(.networking)) for trait-based organization and selective execution
- @Test(arguments: cases) for parameterized data-driven tests
- Both frameworks coexist — swift test runs both Swift Testing and XCTest targets

## Performance

- Value types (struct, enum) — stack-allocated, no reference counting overhead
- Copy-on-write for large value types — use isKnownUniquelyReferenced for custom COW
- Generics over protocol existentials in hot paths — enables compiler specialization
- @inlinable for performance-critical public library functions
- Lazy collections (lazy.map, lazy.filter) for chained transformations on large data
- Avoid unnecessary heap allocations — prefer stack storage and inline buffers
