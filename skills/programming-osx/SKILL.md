---
name: programming-osx
title: "macOS Development"
description: "macOS window and command ownership, AppKit/SwiftUI integration, sandboxed files, and distribution. Auto-activates for Mac app projects."
license: Apache-2.0
compatibility: "Requires Xcode and the project's supported macOS SDK/deployment target; signing tools for distribution."
capabilities: programming-swift
domains: developer
rules:
  - content(macos)
  - content(osx)
  - content(appkit)
  - content(cocoa)
  - match(mac.+app|macos.+app|osx.+app|desktop.+app)
---

## Overview

Use for native macOS app implementation and review. Focus on windows, commands, files, sandbox boundaries, and distribution; preserve the application's SwiftUI/AppKit architecture and deployment contract.

## Mental model

A Mac app may have many independently focused windows and continue running with none visible. Model document, scene, and process lifetimes separately. File access and helper execution depend on explicit user/system authority, not just a path or process-wide singleton.

## Platform gate

Verified 2026-09-05: Xcode/macOS 26.x is the stable family; Xcode/macOS 27 is beta. Apple's compatibility table distinguishes compiler, build SDK, host OS, and deployment target. Check these independently before adopting APIs; use actual symbol availability, not the installed machine's OS, as the minimum-version contract.

MenuBarExtra, NavigationSplitView, and SMAppService are available from macOS 13; Observation and SwiftData from macOS 14. Keep a supported AppKit implementation when it fits. Avoid speculative compatibility layers or raising deployment targets just to use a newer spelling.

## Windows, commands, and UI

- Use WindowGroup for independently instantiable windows, Window for a unique utility window, and DocumentGroup when document ownership fits. Keep window-specific selection, navigation, and drafts out of a process-global model.
- Route commands to the focused scene/selection using focused values or the established responder chain. Disable unavailable actions and provide keyboard shortcuts; don't locate a target with `NSApplication.shared.windows.first`.
- Store scene restoration values separately from documents. `@SceneStorage` is for lightweight restoration, not durable user content. Validate restored identifiers against current files and permissions.
- Use native Table, sidebar, toolbar, Settings, and menu patterns where suitable. Preserve keyboard focus, selection, undo/redo, VoiceOver labels, and resizing; don't port touch-only interaction unchanged.
- Use system controls/materials for macOS 26 styling, applying Liquid Glass to navigation/control surfaces deliberately. Test contrast and reduced transparency instead of layering decorative effects over content.
- Bridge AppKit with representables or hosting views/controllers at a clear boundary. Update existing native objects rather than recreating them on every render; remove observers and break callback ownership cycles during teardown.
- A menu-bar app needs explicit open/settings/quit behavior. `LSUIElement` controls Dock presence; it does not define the entire window-activation policy. Use MenuBarExtra or NSStatusItem according to actual behavior required.

## Files and sandbox boundaries

- Separate App Sandbox from Hardened Runtime: sandbox entitlements constrain resource access; hardened runtime and signing govern execution protections. Direct distribution does not require the same sandbox policy as the Mac App Store.
- Let users select external files through supported panels/document APIs. Persist security-scoped bookmarks when access must survive relaunch; resolve stale bookmarks and refresh them through the documented flow.
- For a security-scoped URL, balance each successful `startAccessingSecurityScopedResource()` with `stopAccessingSecurityScopedResource()`. Keep access active for the whole operation; denial is an error, not a reason to retry through an unrestricted path.
- Use coordinated/document-aware access for externally managed documents. Preserve file contents and surface save conflicts; don't replace an unreadable document with an empty one or delete data to recover from migration failure.
- Store credentials in Keychain. Grant only entitlements needed by the feature; a broadly permissive entitlement is not a fix for an unexplained access failure.

## Helpers, lifecycle, and distribution

- Keep UI state on its intended actor and long-running work outside the UI execution path. Closing a window and quitting the process are distinct events; explicitly own tasks, observers, and subprocesses.
- Use SMAppService for supported login-item/helper registration. Handle enabled, disabled, and approval-required states explicitly; don't repeatedly register to defeat a user's choice. Give XPC services and extensions narrow interfaces and validate requests.
- Don't add privileged helpers or system extensions unless the requested feature requires their privileges. Entitlement eligibility and approval flow must be verified for the actual extension type.
- For direct distribution, follow Developer ID signing, hardened runtime, notarization, and ticket stapling requirements for the artifact. Sign nested code correctly and test the delivered package on a clean machine; local development launch does not prove Gatekeeper behavior.
- Preserve the existing update channel. If updates are part of the task, verify authenticity, compatibility, and recoverable failure; don't add an updater dependency solely as a best-practice recommendation.

## Example

Keep authority alive and guarantee balanced cleanup for a resolved security-scoped URL:

```swift
import Foundation

enum FileAccessError: Error { case denied }

func withFileAccess<T>(
    to url: URL, perform operation: (URL) throws -> T
) throws -> T {
    guard url.startAccessingSecurityScopedResource() else {
        throw FileAccessError.denied
    }
    defer { url.stopAccessingSecurityScopedResource() }
    return try operation(url)
}
```

This helper is for security-scoped URLs; ordinary container URLs use their normal access path. Keep large synchronous I/O out of UI execution.

## Checklist

- [ ] Symbol availability and deployment target agree; beta APIs are identified.
- [ ] Window focus, scene restoration, and document ownership are explicit.
- [ ] File access, cleanup, denial, and save conflicts are handled.
- [ ] Helpers and distribution use the intended entitlements and lifecycle.
- [ ] Relevant sandbox, UI, and distribution checks ran when authorized; limits are stated.

## References

- [Xcode/SDK matrix](https://developer.apple.com/xcode/system-requirements)
- [Security-scoped access](https://developer.apple.com/documentation/foundation/url/startaccessingsecurityscopedresource())
- [SMAppService](https://developer.apple.com/documentation/servicemanagement/smappservice)
- [Notarization](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution)
- [Distribution testing](https://developer.apple.com/documentation/xcode/packaging-mac-software-for-distribution)
- [Liquid Glass](https://developer.apple.com/videos/play/wwdc2025/219/)
