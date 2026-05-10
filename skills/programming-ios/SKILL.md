---
name: programming-ios
title: "iOS Development"
description: "iOS architecture with SwiftUI, SwiftData, App Intents, WidgetKit, and modern platform integrations. Auto-activates for iOS projects."
license: Apache-2.0
compatibility: "Requires Xcode 16+ and iOS 17+ SDK."
capabilities: programming-swift
domains: developer
rules:
  - content(ios)
  - content(iphone)
  - content(ipad)
  - content(uikit)
  - match(iphone.+app|ios.+app|ipad.+app)
  - file(*.xcodeproj)
---

## Mental model

A modern iOS app is SwiftUI views over `@Observable` models, with SwiftData (or a small repository layer) for persistence and App Intents for system-level integration. UIKit is the escape hatch for what SwiftUI can't yet express. Architectural mistakes show up as massive view bodies, scattered singletons, and tight coupling to `UIApplication` — design for testability by isolating side effects behind protocols.

## Architecture

- Feature-first organization: each feature owns its views, models, intents, and tests in one folder
- Domain logic lives in framework-free Swift modules (a separate SPM target) — the UI imports the domain, not the other way around
- Side effects (network, persistence, system services) hide behind protocols injected via `@Environment` or initializer parameters
- Avoid singletons except for genuinely process-wide resources (logger, telemetry); inject everything else
- Keep `App` and `Scene` definitions thin — they wire dependencies and nothing more

## SwiftUI patterns

- `@Observable` model classes for view state; `@Bindable` to create bindings to their properties
- `NavigationStack` with typed `NavigationLink(value:)` for type-safe routing; `NavigationPath` for heterogeneous stacks
- `NavigationSplitView` for iPad/macOS layouts — collapses to stack on iPhone automatically
- `.task` modifier for async work tied to view lifetime — cancels on disappear
- `.environment(...)` to inject services down the tree; custom `EnvironmentKey` for app-specific dependencies
- View bodies should read like a layout description — push computation into the model

## Data and persistence

- SwiftData with `@Model` for new projects — schema is derived from the type, lightweight migrations are automatic
- `@Query` in views for filtered, sorted, animated fetches
- `ModelContainer` configured at the app entry point; injected via `.modelContainer(...)`
- CloudKit sync via SwiftData when cross-device persistence is needed
- `#Predicate` macro for type-safe queries; `VersionedSchema` + `SchemaMigrationPlan` for non-trivial migrations
- For non-SwiftData persistence, hide Core Data / files / keychain behind a repository protocol

## System integration

- App Intents make actions discoverable by Shortcuts, Siri, Spotlight, and Apple Intelligence
- `AppEntity` for domain objects the system can reason about; `AppShortcutsProvider` for surfaced shortcuts
- Widgets via WidgetKit with `TimelineProvider`; Live Activities via ActivityKit for lock-screen and Dynamic Island
- StoreKit 2 (`Product.products(for:)`, `Transaction.currentEntitlements`) — no delegate callbacks, no receipt parsing
- `PrivacyInfo.xcprivacy` declares all required-reason API usage — ship with it from day one

## UIKit interop

- Wrap UIKit views with `UIViewRepresentable` / `UIViewControllerRepresentable` only when SwiftUI lacks an equivalent
- Keep the bridge thin: a single representable per feature, not scattered across views
- For UIKit-first apps, embed SwiftUI screens via `UIHostingController` — incremental migration works well

## Concurrency

- Adopt Swift 6 strict concurrency — main-thread mistakes become compile errors
- `@MainActor` on view models and anything touching UIKit/SwiftUI
- Network and persistence on background actors or detached tasks; results cross back via `await`
- Cancel structured tasks (`.task`) automatically; for unstructured work, hold `Task` handles and cancel explicitly

## Testing

- Swift Testing (`@Test`, `#expect`, `@Suite`) for unit and integration tests
- Test the domain target without the app — fast, deterministic, no simulator
- `#Preview` doubles as a visual test for layout across states
- XCUITest for end-to-end flows; keep them short and focused on critical user paths
- Mock system services by injecting the protocol you defined, not by stubbing Apple's classes

## Distribution

- TestFlight for internal and external betas; phased rollouts on App Store releases
- Stay current with the Privacy Manifest required-reason API list — Apple expands it regularly
- Symbolicate crash reports via dSYMs uploaded with each build
