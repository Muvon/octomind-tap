---
name: programming-osx
title: "macOS Development"
description: "macOS app architecture: SwiftUI for Mac, AppKit interop, sandboxing, and distribution. Auto-activates for Mac app projects."
license: Apache-2.0
compatibility: "Requires Xcode 16+ and macOS 14+ SDK."
capabilities: programming-swift
domains: developer
rules:
  - content(macos)
  - content(osx)
  - content(appkit)
  - content(cocoa)
  - match(mac.+app|macos.+app|osx.+app|desktop.+app)
---

## Mental model

A modern Mac app is SwiftUI-first with AppKit as the escape hatch for advanced window management, custom NSView work, and APIs SwiftUI doesn't cover. The Mac-specific design vocabulary — toolbars, sidebars, inspectors, multiple windows, menu bar commands, drag and drop — must feel native. Cross-platform code (with iOS) belongs in a shared SPM target; platform-specific UI lives in a Mac-only target.

## SwiftUI on macOS

- `NavigationSplitView` (two or three columns) is the canonical sidebar/content/detail layout
- `Settings` scene for the preferences window — replaces the old `NSWindowController`-based pattern
- `MenuBarExtra` for menu-bar utilities — no `AppDelegate` boilerplate needed
- `WindowGroup` and `Window` scenes for multi-window apps; `@Environment(\.openWindow)` and `\.dismissWindow` for programmatic control
- `.inspector(isPresented:)` for the right-side property panel
- `.toolbar { ToolbarItem(placement: ...) { ... } }` for native toolbar items
- `.commands { CommandMenu("...") { ... } }` for custom menu items with keyboard shortcuts
- `Table` for multi-column sortable selectable data — the native Mac data display
- `@SceneStorage` for per-scene persistence; the system restores window frames automatically

## AppKit interop

- `NSViewRepresentable` / `NSViewControllerRepresentable` to embed AppKit in SwiftUI
- `NSHostingController` / `NSHostingView` to embed SwiftUI in AppKit-first apps
- Reach for `NSWindow` directly via `NSApplication.shared.windows` only for what SwiftUI can't express (window level, collection behavior, custom drag regions)
- `NSPasteboard` for clipboard, `NSItemProvider` / drag-and-drop APIs for drops
- Bridge AppKit notifications (`NSWorkspace`, `NSApplication.willTerminateNotification`) via `NotificationCenter` into SwiftUI

## Menu bar apps

- `MenuBarExtra` with `.menuBarExtraStyle(.window)` for popover-style UI, `.menu` for a plain menu
- `LSUIElement = true` in Info.plist to hide the Dock icon; `NSApp.setActivationPolicy(.accessory)` to toggle at runtime
- Always provide an explicit quit affordance — there's no Dock to quit from
- `NSStatusBar` for advanced status-item customization beyond what `MenuBarExtra` exposes

## Security and sandboxing

- App Sandbox is the default for App Store apps — enable only entitlements actually needed
- Hardened Runtime is required for notarization; it blocks unsigned code loading
- Security-scoped bookmarks for persistent file access across launches outside the container
- Keychain Services (or `SecKey`/`SecItem`) for credentials — never `UserDefaults` or plaintext
- Temporary-exception entitlements (`com.apple.security.temporary-exception.*`) are a last resort and may block App Store review

## Distribution

- App Store: archive via Xcode Organizer or `xcodebuild -exportArchive`
- Direct distribution: Developer ID code signing + notarization + stapling — unsigned/un-notarized apps trip Gatekeeper
- Sparkle framework for auto-update outside the App Store; ship `appcast.xml` from a stable URL
- DMG with custom layout for polished installs; ZIP for simple distribution

## System extensions and entitlements

- Network Extensions (App Proxy, Packet Tunnel, Content Filter, DNS Proxy) — each has its own entitlement and review
- Endpoint Security for file/process monitoring; DriverKit replaces kexts for hardware drivers
- System extensions require provisioning, entitlements, and user approval in System Settings
- `OSSystemExtensionRequest` to install at runtime; handle the approval-pending state explicitly

## Testing

- Swift Testing (`@Test`, `#expect`) for unit and integration tests
- XCUITest with `XCUIApplication` for menu, toolbar, and window automation
- Test under sandbox — disabling it for tests hides bugs that show up in production
- Accessibility Inspector to verify VoiceOver and keyboard navigation before shipping

## Project layout

- Cross-platform domain code in a shared SPM target; macOS UI in a macOS-only target
- One Mac app target per product; helper tools (XPC services, login items, extensions) are separate targets
- Resources scoped per target — Mac assets and iOS assets share a catalog only if they're identical
