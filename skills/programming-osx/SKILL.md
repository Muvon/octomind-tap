---
name: programming-osx
title: "macOS Development"
description: "macOS platform patterns, SwiftUI for Mac, AppKit integration, sandboxing, notarization, and distribution practices. Auto-activates for Mac app projects."
license: Apache-2.0
compatibility: "Requires Xcode 16+ and macOS 15+ SDK."
capabilities: programming-swift
domains: developer
rules:
  - content(macos)
  - content(osx)
  - content(appkit)
  - content(cocoa)
  - match(mac.+app|macos.+app|osx.+app|desktop.+app)
---

# macOS Development

## Conventions

- SwiftUI for Mac first — AppKit only for advanced window management and legacy APIs
- NavigationSplitView for sidebar-detail patterns — the canonical Mac layout
- Settings scene for app preferences window — SwiftUI-native replacement for custom NSWindow-based preferences
- MenuBarExtra for menu bar utilities — no AppDelegate boilerplate needed
- Window and WindowGroup scenes for multi-window management
- Respect system appearance — support light/dark mode, accent colors, vibrancy
- Human Interface Guidelines for Mac — toolbar, sidebar, inspector patterns

## SwiftUI on macOS

- NavigationSplitView with two or three columns — sidebar, content, detail
- .inspector(isPresented:) modifier for right-panel property inspectors
- Toolbar with .toolbar {} — placement: .primaryAction, .navigation, .automatic
- Table for multi-column sortable, selectable data display — native Mac pattern
- .focusedSceneValue for routing menu bar commands to the active window/document
- .commands modifier for custom menu items with keyboard shortcuts (CommandMenu, Button)
- .defaultSize, .windowResizability, .windowStyle for window dimension and chrome control
- @SceneStorage for persisting per-scene state across launches; system restores window frames automatically
- @Environment(\.openWindow) for programmatic window creation — openWindow(id:) or openWindow(value:)
- @Environment(\.dismissWindow) and @Environment(\.pushWindow) for window lifecycle control

## AppKit Integration

- NSViewRepresentable / NSViewControllerRepresentable for embedding AppKit views in SwiftUI
- NSWindow access via NSApplication.shared.windows for frame, level, behavior control
- NSHostingController / NSHostingView to embed SwiftUI inside AppKit-based apps
- NSPasteboard for clipboard operations, NSDraggingDestination for drag and drop
- Combine AppKit lifecycle events (NSApplication notifications) with SwiftUI via NotificationCenter

## Menu Bar Apps

- MenuBarExtra scene with .menuBarExtraStyle(.window) for popover-style UI
- Info.plist: LSUIElement = true (Application is agent) to hide dock icon
- NSApp.setActivationPolicy(.accessory) for runtime dock icon visibility control
- Provide explicit quit action in UI — menu bar apps have no Dock quit option
- NSStatusBar for advanced status item customization beyond MenuBarExtra capabilities

## Security & Sandboxing

- App Sandbox entitlements — enable only capabilities the app actually uses
- Hardened Runtime required for notarization — prevents unsigned code loading
- Security-scoped bookmarks for persistent file access outside sandbox container
- Keychain Services for credential storage — never store secrets in plaintext or UserDefaults
- com.apple.security.temporary-exception.* entitlements as absolute last resort

## Distribution

- Notarization required for apps distributed outside App Store — Apple scans for malware
- Developer ID code signing for direct distribution — codesign with proper identity
- App Store distribution via Xcode Organizer or xcodebuild export
- Installer packages with productbuild for multi-component installations
- Sparkle framework for auto-update mechanism outside App Store
- DMG or ZIP for simple app distribution — staple notarization ticket before shipping

## System Extensions

- Network Extensions — App Proxy, Packet Tunnel, Content Filter, DNS Proxy providers
- Endpoint Security framework — file monitoring, process control, antivirus/EDR
- DriverKit for user-space hardware drivers — modern replacement for kernel extensions (kexts)
- System extensions require provisioning profile, entitlements, and notarization
- OSSystemExtensionRequest for installation — user must approve in System Settings

## Testing

- Swift Testing (@Test, #expect) for unit and integration tests
- XCTest UI testing with XCUIApplication for Mac-specific interactions (menus, toolbars)
- Test sandbox entitlements separately — sandbox restrictions affect runtime behavior
- Accessibility Inspector for verifying VoiceOver and keyboard navigation compatibility

## Tooling

| Command | Purpose |
|---------|---------|
| `xcodebuild -scheme App build` | Build the project |
| `xcodebuild test -scheme App` | Run tests |
| `codesign --options runtime -s "Developer ID Application: Team (ID)" App.app` | Sign for distribution |
| `xcrun notarytool submit App.zip --wait` | Notarize the app |
| `xcrun stapler staple App.app` | Staple notarization ticket |
| `productbuild --component App.app /Applications Installer.pkg` | Create installer package |
| `spctl --assess -v App.app` | Verify Gatekeeper acceptance |
