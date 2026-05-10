---
name: programming-swift
title: "Swift Development"
description: "Modern Swift architecture: value types, concurrency, protocol-oriented design, and SPM. Auto-activates in Swift package projects."
license: Apache-2.0
compatibility: "Requires Swift 6.0+ toolchain."
capabilities: programming-swift
domains: developer
rules:
  - file(Package.swift)
  - content(swift)
---

## Mental model

Swift is a value-oriented language with strong static typing and modern concurrency. The maintainable Swift codebase keeps domain logic in `struct`s and `enum`s, uses classes only for identity or shared mutable state, and isolates concurrency boundaries with actors and `@MainActor`. Reaching for class hierarchies and reference semantics by default produces fragile, hard-to-test code.

## Value-oriented design

- `struct` by default; reach for `class` only when you need identity, shared state, or Obj-C interop
- `enum` with associated values models finite, exhaustive cases — pattern-match instead of branching on optional fields
- Protocol-oriented composition: small protocols + extensions beat deep inheritance hierarchies
- Generics with associated types (`some Protocol`, `any Protocol`) let APIs stay value-typed while remaining flexible
- Avoid `AnyObject`-only protocols unless you genuinely need reference semantics

## Concurrency (Swift 6)

- Strict concurrency checking enforces `Sendable` at compile time — design data flow so values cross actor boundaries, not shared references
- Actors own mutable state — replace `class + lock` patterns with an `actor` that exposes async methods
- `@MainActor` for all UI-bound state and code; main-actor-isolated types can't be passed across boundaries without `await`
- `async`/`await` only — no completion handlers in new code; bridge old APIs with `withCheckedContinuation`
- Structured concurrency via `TaskGroup` / `async let` — child tasks are bounded by the parent; prefer over `Task { }` detached work
- `Task.detached` only when you need to escape actor inheritance — it's an exception, not a default

## Error handling

- `throws` for recoverable failures; typed throws (`throws(MyError)`) for library APIs where callers benefit from knowing the exact error type
- `Result<T, E>` for stored errors, callback bridges, and crossing async boundaries when needed
- `try?` only when the error genuinely doesn't matter; `try!` belongs in tests and prototypes, never in shipping paths
- Don't use exceptions for control flow — model expected outcomes as enum cases or `Result`

## API design

- Methods read like English at the call site — the first argument label completes the verb (`array.insert(x, at: 0)`)
- Initializers and factories are deliberate: provide the few configurations users actually need, not every permutation
- `@Observable` (Observation framework) replaces `ObservableObject`/`@Published` for new SwiftUI code
- Prefer `some Protocol` return types for stable APIs; `any Protocol` only when runtime polymorphism is required
- Mark internal types `internal` (the default) — `public` is an opt-in commitment

## SwiftUI patterns

- `NavigationStack` with value-based `NavigationLink` for type-safe routing
- `@Observable` model classes + `@Bindable` for two-way binding in views
- `.task` modifier for async work tied to view lifetime — cancels automatically
- Keep views small; push logic into observable models or pure functions
- Previews (`#Preview`) double as living documentation — make them work across data states

## Project layout and SPM

- Swift Package Manager for everything new — no CocoaPods/Carthage
- Split into targets along boundaries that compile and test independently; resist the "one big target" temptation
- Resources, plugins, and macros each get their own target
- Use `swiftLanguageMode: .v6` in `Package.swift` to opt into strict concurrency from day one

## Testing

- Swift Testing (`@Test`, `#expect`, `@Suite`) for new test code — better diagnostics, trait-based organization, parameterized tests
- XCTest only for UI automation (`XCUIApplication`) and Obj-C interop
- Test value types directly — no mocks needed; for protocols, provide a hand-written conforming type
- `#expect(throws: MyError.self) { try someCall() }` for error paths
