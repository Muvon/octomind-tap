---
name: programming-kotlin
title: "Kotlin Development"
description: "Idiomatic Kotlin — null-safety discipline, coroutines and Flow, expression-oriented style, and Android/Compose conventions. Auto-activates in Kotlin projects."
license: Apache-2.0
compatibility: "Requires JDK + Gradle with Kotlin 2.x (K2 compiler); Android SDK for Android targets."
domains: developer
rules:
  - file(build.gradle.kts)
  - file(settings.gradle.kts)
  - content(kotlin)
---

## Mental model

Kotlin is pragmatic conciseness with compiler-enforced null-safety. Idiomatic Kotlin is expression-oriented (`when`, `if` as expressions, single-expression functions) and immutable-first. The two failure modes are opposite: writing Java in Kotlin (mutable beans, null-check boilerplate, util classes), and scope-function golf that nobody can read. Clarity beats cleverness; the compiler beats convention.

## Language — the idioms that matter

- `val` by default; `var` is a flag for deliberate mutability. Collections: read-only types (`List`, `Map`) in signatures, mutable ones as local implementation detail
- Data classes for values; sealed interfaces/classes for closed hierarchies with exhaustive `when` (no `else` on sealed matches — let the compiler catch new cases)
- Null-safety is a design tool, not syntax tax: model absence with `?` types, handle with `?.`, `?:`, and early returns. `!!` is a bug report to your future self; `lateinit` only for framework-injected lifecycles
- Extension functions to give existing types domain vocabulary — not to hide business logic where nobody looks for it
- Scope functions sparingly and conventionally: `let` for null-safe transforms, `apply` for object configuration, `also` for side effects — nesting two is the readability ceiling
- Expression style: single-expression functions, `when` over if-chains; named + default arguments over builders and telescoping overloads
- Delegation over inheritance: `by lazy` for expensive init, `by` interface delegation over deep hierarchies

## Coroutines — structured or broken

- Structured concurrency always: launch inside a scope that owns the lifecycle (`coroutineScope`, `viewModelScope`, `SupervisorJob` services). `GlobalScope` is a leak with a name
- suspend functions are main-safe by contract: they switch their own dispatcher (`withContext(Dispatchers.IO)`) — callers never have to know
- Inject dispatchers (constructor parameter, default `Dispatchers.Default/IO`) — hardcoded dispatchers make code untestable
- Cancellation is cooperative: long CPU loops check `isActive`/`ensureActive`; never swallow `CancellationException` in a generic catch
- Flow for cold streams (emits per collector); StateFlow for observable state (always has a value); SharedFlow for events. Convert callbacks with `callbackFlow` + `awaitClose`
- Parallel fan-out: `coroutineScope { things.map { async { ... } }.awaitAll() }` — an `async` you never await is a swallowed error

## Android specifics (when the target is Android)

- Jetpack Compose is the default UI for new work: state hoisting (stateless composables take value + lambda), `remember`/`rememberSaveable` deliberately, ViewModel exposes `StateFlow<UiState>` collected via `collectAsStateWithLifecycle`
- Unidirectional data flow: UI sends events up, state flows down — no business logic in composables
- One immutable `UiState` data class per screen beats a dozen loose observable fields
- Repository layer owns data source choice; ViewModels never touch Android framework types the emulator can't fake (keeps them JVM-testable)

## Multiplatform (KMP)

- Production-ready pattern: share business logic, models, and networking (`commonMain`); keep platform UI native or use Compose Multiplatform where team skills fit
- `expect`/`actual` for the thin platform seam — the smaller the actual surface, the healthier the module

## Ecosystem defaults

- Gradle with Kotlin DSL and version catalogs (`libs.versions.toml`); K2 compiler is the current baseline
- Serialization: `kotlinx.serialization` (`@Serializable`) for Kotlin-first codebases
- Lint discipline: ktlint or detekt wired into CI, not into arguments

## Testing

- JUnit 5 or kotest per repo convention; MockK for mocks (`coEvery` for suspend functions) — mock boundaries, not data classes
- Coroutines: `runTest` + injected `TestDispatcher`; assert Flow emissions with Turbine (`flow.test { ... }`)
- Compose UI: `createComposeRule` for behavior-level checks; keep logic in ViewModels so most tests stay on the JVM
