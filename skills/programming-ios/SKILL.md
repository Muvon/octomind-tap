---
name: programming-ios
title: "iOS Development"
description: "iOS platform patterns, SwiftUI, SwiftData, App Intents, WidgetKit, StoreKit 2, and modern iOS SDK practices. Auto-activates for iPhone and iPad projects."
license: Apache-2.0
compatibility: "Requires Xcode 16+ and iOS 18+ SDK."
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

# iOS Development

## Conventions

- SwiftUI first — UIKit only for components without SwiftUI equivalent
- SwiftData for persistence — prefer over Core Data for new projects (iOS 17+)
- NavigationStack for navigation — NavigationView is deprecated
- App Intents for Siri, Shortcuts, and Apple Intelligence integration
- Privacy manifests (PrivacyInfo.xcprivacy) required — declare all API usage reasons
- Target current and previous major iOS version as minimum deployment target
- Human Interface Guidelines compliance — platform-native look and feel

## SwiftUI Patterns

- NavigationStack with value-based NavigationLink for type-safe programmatic navigation
- NavigationPath for heterogeneous navigation state management
- NavigationSplitView for iPad multi-column layouts — collapses to stack on iPhone
- @Observable model classes — not ObservableObject/@StateObject for new code (iOS 17+)
- @Bindable for creating bindings to @Observable model properties in views
- @Environment for dependency injection — custom EnvironmentKey for app services
- .task modifier for async work tied to view lifecycle — cancels automatically on disappear
- ViewThatFits and AnyLayout for adaptive layouts across size classes
- Custom containers with ForEach(subviewOf:) API (iOS 18+)
- onScrollGeometryChange for tracking scroll position and reacting to scroll state (iOS 18+)
- MeshGradient for multi-directional color transitions with control point grids (iOS 18+)

## Data & Persistence

- SwiftData with @Model macro — automatic schema generation and lightweight migration
- @Query in SwiftUI views for filtered, sorted, animated data fetching
- ModelContainer configured at app entry point — inject via .modelContainer modifier
- CloudKit sync via SwiftData for seamless iCloud persistence
- @Attribute(.unique) for single-property deduplication, #Unique for compound constraints (iOS 18+)
- @Relationship for object graphs with cascade/nullify delete rules
- #Predicate macro for type-safe, compile-checked queries
- VersionedSchema + SchemaMigrationPlan for non-trivial schema migrations

## App Intents & Intelligence

- AppIntent protocol for actions exposed to Shortcuts, Siri, and Spotlight
- AppEntity for domain objects discoverable by the system
- @Parameter with type-safe validation for intent inputs
- AppShortcutsProvider for suggested shortcuts surfaced proactively
- @AssistantIntent(schema:) within App Intent Domains for Apple Intelligence integration (iOS 18+)

## WidgetKit & Live Activities

- TimelineProvider with TimelineEntry for widget content scheduling
- Live Activities via ActivityKit — real-time updates on lock screen and Dynamic Island
- Dynamic Island presentations: compact, expanded, minimal — design for all three
- Interactive widgets with AppIntent-backed Button and Toggle (iOS 17+)
- Push-based widget updates via APNs for server-driven content refresh

## StoreKit 2

- Product.products(for:) async API — no delegate callbacks
- Transaction.currentEntitlements for checking active purchases and subscriptions
- SubscriptionStoreView and ProductView for system-provided purchase UI
- StoreKit Testing in Xcode for local purchase simulation without sandbox accounts
- Transaction.updates AsyncSequence for real-time purchase monitoring

## Testing

- Swift Testing (@Test, #expect, #require) for unit and integration tests
- @Suite for test grouping, @Test(arguments:) for parameterized tests
- XCTest for UI automation — XCUIApplication, XCUIElement accessibility queries
- #Preview macro as living documentation — verify layout across devices and data states
- Test plans in Xcode for organizing configurations (language, region, arguments)
- Simulator testing via xcodebuild — target specific device and OS combinations
