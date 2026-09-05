---
name: programming-ios
title: "iOS Development"
description: "iOS state ownership, SwiftUI/UIKit integration, persistence, lifecycle, and platform services. Auto-activates for iOS projects."
license: Apache-2.0
compatibility: "Requires Xcode and the project's supported iOS SDK/deployment target; newer frameworks require availability checks."
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

## Overview

Use for iPhone and iPad app implementation and review. Preserve existing UI and persistence choices; improve state ownership, lifecycle behavior, and platform integration without imposing a new architecture.

## Mental model

Views render state; owners decide its lifetime. Durable data, scene state, and temporary UI state are different concerns. A newer SDK does not raise the deployment target, and an app task is not a guarantee of background execution.

## Platform gate

Verified 2026-09-05: Apple's stable Xcode 26.x line includes Swift 6.3 and iOS 26.x SDKs; Xcode/iOS 27 are beta. Check the selected Xcode, language/isolation settings, minimum OS, entitlements, and framework availability before adding APIs.

Observation and SwiftData require iOS 17+; NavigationStack requires iOS 16+. Use `#available` only where supported older systems need a deliberate compatible implementation. Do not add speculative fallback trees for unsupported OS versions, or raise minimum deployment versions as incidental cleanup. Recheck Apple's live SDK submission requirements when preparing a release.

## State and UI ownership

- For supported SwiftUI code, use `@Observable` for observation, `@State` to own a model's stable view lifetime, and `@Bindable` only when bindings are needed. Observation alone does not imply MainActor isolation; declare UI-state isolation deliberately.
- Keep existing ObservableObject/UIKit implementations where they satisfy the task. Don't create a view model, protocol, or separate package for every view; extract logic when ownership, reuse, or testing warrants it.
- Give lists stable domain identifiers. Avoid generating UUIDs in computed view data or using array indices as identity for reorderable items; incorrect identity corrupts selection and local state.
- Express navigation as route values when useful. Validate deep links as untrusted input and reconcile restored routes with current authentication/data; restoration is not authorization.
- Use native controls and system surfaces so current platform styling and accessibility work together. For iOS 26 Liquid Glass, avoid recreating system materials or applying glass to every content surface. Check contrast, reduced transparency/motion, Dynamic Type, and keyboard/VoiceOver behavior.
- Support iPad resizing and multiple scenes. Keep per-window selection/navigation separate from shared domain state; don't assume a single active window or fixed screen dimensions.

## Tasks and persistence

- Use `.task(id:)` for asynchronous work whose lifetime follows a view and input. SwiftUI requests cancellation when that lifetime ends or the ID changes; work must cooperate, and stale results still need protection before updating state.
- Keep UI mutation on its intended actor. `Task {}` and async functions are not automatic background execution; move heavy computation through a deliberate concurrency boundary, not arbitrary detached tasks.
- For work surviving a screen, choose a longer-lived owner. Use supported background APIs for system-managed execution; don't assume a task keeps running after suspension or termination.
- SwiftData is an option, not a mandatory replacement for Core Data or an existing store. Make container/context ownership explicit; transfer identifiers or detached values between concurrency domains instead of sharing live context-bound models.
- Persist meaningful mutations at an explicit success boundary. Treat save/migration errors as errors; don't silently recreate the store or substitute an in-memory container in production.
- Version schemas when evolution requires it and test migration from real prior schemas. Automatic lightweight migration handles only compatible changes. CloudKit adds schema and entitlement constraints; do not assume local uniqueness or immediate cross-device consistency.

## System boundaries and checks

- Inject side-effect boundaries where substitution is useful; use concrete types or closures when sufficient. Keep UIKit representables thin and pair observer/delegate setup with teardown.
- StoreKit: distinguish cancellation, pending, and verified success. Grant entitlements only after appropriate verification, process updates/revocations, and finish transactions after delivery; make repeat delivery safe.
- App Intents and widgets run with their own lifecycle constraints. Revalidate authorization and durable state; don't depend on an open app scene or in-memory singleton.
- Request permissions at the relevant user action. Handle denial explicitly and store secrets in Keychain; inspect required-reason APIs and SDK privacy manifests for the actual dependencies.
- Use existing unit tests for state transitions and focused UI tests for user flows. Previews aid inspection but are not assertions. Verify device-only integration separately from simulator behavior.

## Example

Own an observable editor in its parent; borrow bindings in the child (iOS 17+):

```swift
import SwiftUI
import Observation

@MainActor @Observable final class Draft {
    var title = ""
}

@MainActor struct Editor: View {
    @State private var draft = Draft()
    var body: some View { TitleField(draft: draft) }
}

@MainActor struct TitleField: View {
    @Bindable var draft: Draft
    var body: some View { TextField("Title", text: $draft.title) }
}
```

Creating `Draft()` inside `body` would lose the intended owner and stable lifetime.

## Checklist

- [ ] APIs match deployment targets; beta features are identified.
- [ ] View, scene, task, and durable-data lifetimes are distinct.
- [ ] Cancellation and stale results cannot overwrite current state.
- [ ] Persistence and purchase failures remain visible and recoverable.
- [ ] Accessibility and relevant checks were verified when authorized; limits are stated.

## References

- [Xcode/SDK matrix](https://developer.apple.com/xcode/system-requirements)
- [Observation migration](https://developer.apple.com/documentation/swiftui/migrating-from-the-observable-object-protocol-to-the-observable-macro)
- [Task cancellation](https://developer.apple.com/documentation/swift/task/cancel())
- [SwiftData](https://developer.apple.com/documentation/swiftdata/) and [CloudKit integration](https://developer.apple.com/documentation/swiftdata/syncing-model-data-across-a-persons-devices)
- [StoreKit transactions](https://developer.apple.com/documentation/storekit/transaction)
- [Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)
