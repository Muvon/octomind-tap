---
name: device-mobile-automation
title: "Mobile Device UI Automation"
description: "Operate iOS and Android devices — real hardware, simulators, and emulators — via the mobile-mcp server. Covers device discovery and selection, app install / launch / terminate, accessibility-tree targeting, taps / swipes / typing / device-button presses, orientation handling, and the safety boundary around app-store / jailbreak / biometric / in-app-purchase protections. Activate when the user wants to drive a phone or tablet (iPhone, Android, iOS Simulator, Android Emulator) through a UI flow. Pairs with the device:operator agent which carries the shared snapshot → verify → record discipline; this skill carries the mobile-specific tooling and rules and pulls the device-mobile capability automatically."
license: Apache-2.0
compatibility: "Requires the device:operator agent. iOS work needs Xcode + Xcode CLT and a paired developer-mode device or simulator. Android work needs platform-tools (adb) on PATH and an emulator or USB-debug-enabled device."
domains: device
capabilities: device-mobile
rules:
  - session(device) content(iphone)
  - session(device) content(android)
  - session(device) content(phone)
  - session(device) content(simulator)
  - session(device) content(emulator)
  - session(device) content(ios)
  - match(\b(on|to|in)\s+(my\s+)?(iphone|ipad|android|phone|tablet)\b)
  - match(\b(ios|android)\s+(simulator|emulator|device)\b)
  - match(\b(install|launch|open|terminate)\s+(the\s+)?app\s+on\b)
  - match(\b(tap|swipe|scroll)\s+(through\s+)?(the\s+)?(app|screen|view)\b)
  - match(\bautomate\s+(my|the)\s+(phone|iphone|ipad|android|tablet)\b)
metadata:
  tags: "mobile ios android iphone simulator emulator app automation mobile-mcp"
---

## Overview

This skill turns the `device:operator` agent into a mobile-device driver. It activates when the user talks about a phone or tablet (real or simulated) and brings in the `device-mobile` capability — the `mobile-mcp` MCP server — so the agent has tools to list devices, manage apps, snapshot the UI tree, tap by accessibility-id, type, swipe, press device buttons, and rotate the screen.

The agent already carries the universal discipline (snapshot → locate → act → verify → record, `run.json` schema, checkpoint policy, secret redaction, output directory layout). This skill carries only what is mobile-specific: which tools exist on `mobile-mcp`, how to target elements on a mobile UI tree, how to handle iOS/Android prerequisites and dialogs, and which mobile-specific safety boundaries cannot be crossed.

## Mental model

A phone is not a desktop. The UI is touch-first, layouts shift on orientation, every screen has an accessibility tree the OS will hand you, and the operating system itself owns half the surface (permission prompts, app-store sheets, biometric overlays, status bar). You target by semantic id when one exists; you reason about the active app, the active screen, and the active orientation as part of your state model.

Three immovable invariants on mobile:

1. The active device is part of state. `list_devices` runs first if the user did not pick one. If multiple are connected, you do not guess — you stop and ask. After a `set_screen_size` or rotation, you re-snapshot before issuing any coordinate-based action; the old coordinates are gone.
2. OS overlays are not your screens. Permission prompts, biometric sheets, app-store dialogs, and the share sheet are owned by iOS / Android — not by the app you are testing. They appear unexpectedly. You stop, screenshot, and ask the user how to answer. You never auto-tap "Allow" or "Don't Allow".
3. App-store, jailbreak, root, DRM, and biometric protections are off-limits. The agent's `critical` block already says so; this skill restates it because mobile is where these protections live.

## Tooling — what mobile-mcp gives you

The `mobile-mcp` MCP server exposes tool families. Use the most semantic option available before falling back.

| Family | Use for |
|---|---|
| Device discovery | `list_devices`, `get_screen_size`, `set_screen_size`, `get_orientation`, `set_orientation` |
| App management | List installed apps, `install_app`, `uninstall_app`, `launch_app` (by bundle id / package), `terminate_app` |
| Screen interaction | Take screenshot, list UI elements (accessibility tree), `click`, `double_tap`, `long_press`, `swipe` |
| Input | `type_text`, `press_button` (home, back, volume up/down, power), `open_url` (deep links) |

Always start a run with `list_devices` if the user did not name one. Record the chosen device id, platform (`ios` / `android`), OS version, and screen size into `run.json` under `target`.

## Element targeting

Mobile UIs are introspectable. Targets go through a strict preference order:

1. `accessibility-id` — the most stable selector iOS / Android expose. Always try this first.
2. `label` or `name` — visible UI text the OS reports for the element.
3. `role` — when the element is a button / textfield / link and only one matches the screen.
4. Exact text content — last resort among semantic options. Beware of dynamic text (counts, timestamps).
5. Coordinates — fallback only when no semantic selector is present. Re-derive from a fresh snapshot every time.

If the target element is not in the tree, scroll the smallest plausible amount and re-snapshot — do not swipe blindly through the app looking for it. After three failed scroll-and-look passes, the step has failed (`selector_not_found`); record and stop.

After any orientation change or `set_screen_size`, every previous coordinate is invalid. Snapshot again before the next coordinate-based action.

## Device prerequisites

The skill's `device-mobile` capability brings in `mobile-mcp` automatically. The host still needs the platform tooling.

iOS:
- Xcode and Xcode command-line tools (`xcode-select --install`).
- For real devices: a paired device with developer mode enabled.
- For simulators: an iOS Simulator runtime that matches the target OS version.

Android:
- Android platform-tools on PATH (`adb` resolvable in the shell).
- For real devices: USB debugging enabled; the device authorized in `adb devices`.
- For emulators: a running AVD.

If a tool call fails with what looks like a missing prerequisite, stop and tell the user exactly what to install or enable. Do not retry the same tool blindly.

## OS dialogs and unexpected overlays

Treat every OS-level overlay as a signal that the run cannot continue without user input:

| Overlay | Action |
|---|---|
| App permission prompt (camera, contacts, notifications, location, photos, microphone, tracking) | Stop. Screenshot. Ask how to answer. Never auto-tap Allow / Deny. |
| Biometric prompt (Face ID / Touch ID / fingerprint) | Stop. The user must authenticate physically; you cannot. |
| App-store sign-in / payment confirmation sheet | Stop. Confirm with the user before any tap. |
| OS update / battery / storage warning banner | Stop. Screenshot. Let the user dismiss it. |
| Share sheet | Treat the share sheet as a different surface; stop if it was unexpected. |

Append a `failures[]` row with `reason: "unexpected_dialog"` and `last_snapshot` pointing at the dialog screenshot. Set status to `partial` (if past a checkpoint) or `failed` (if not). Wait for user direction.

## Mobile-specific failure modes

The agent's `failures[]` reason enum extends with these on mobile:

| `reason` | What it means |
|---|---|
| `selector_not_found` | Element with that accessibility-id / label / role was not in the tree after a fresh snapshot and up to three scroll-and-look passes |
| `launch_timeout` | `launch_app` did not reach a known ready element within 10 s |
| `app_not_installed` | The bundle id / package the flow needs is not present on the device; ask whether to install |
| `permission_denied` | An OS-level permission is blocking (push, network, location, etc.); user must grant |
| `unexpected_dialog` | A system / app-store / biometric sheet appeared mid-flow |
| `device_unavailable` | The chosen device disappeared (USB unplug, simulator quit, host suspend) |
| `orientation_drift` | A coordinate-based action happened after rotation without a re-snapshot — bug in the flow itself; abort and re-plan |

Be precise. Do not bucket everything into a vague reason — the next person replaying the run uses these strings to triage.

## Multi-platform / regression sweeps

When the user asks to run the same flow on more than one platform (typical: iOS + Android, or two iOS versions), produce one run directory per device, each with its own `run.json` and checkpoints. Slug them `<base-slug>--ios` / `<base-slug>--android` so they sort together.

A diff is only useful when the same checkpoint exists on both runs. If the flow legitimately diverges (different screens, different copy), note the divergence in `notes.md` rather than forcing both checkpoints to match.

## Safety boundary

Hard "no" — never attempt, even on request:

- Jailbreak or root the device.
- Bypass the App Store, Play Store, or sideloading protections beyond what the OS already permits for development.
- Defeat DRM, attestation (DeviceCheck, Play Integrity), or anti-tampering checks.
- Bypass biometric or screen-lock prompts.
- Auto-tap through an in-app-purchase or subscription-confirmation sheet.
- Persist credentials, OTPs, recovery codes, or session tokens to disk. They go to the device this session and stay there.

Soft "stop and confirm" — these need explicit user confirmation in this turn:

- Account deletion, password reset, sign-out from a synced account.
- Removing or reinstalling an app that holds user data.
- Sending a message, posting publicly, or initiating a paid action from the user's account.
- Changing the device language, region, or developer settings.

## Checklist

- [ ] `list_devices` was called and the chosen device is recorded in `run.json.target`
- [ ] Platform tooling prerequisites verified (or a clean failure with instructions for the user)
- [ ] Every action used the semantic-first targeting order (accessibility-id → label → role → text → coords)
- [ ] Snapshots taken after each rotation or screen-size change before any coordinate action
- [ ] OS / app-store / biometric / share-sheet dialogs stopped the run — none were auto-dismissed
- [ ] Failure rows use mobile-specific reasons from the enum, not generic strings
- [ ] No hard-no actions attempted (jailbreak, DRM bypass, biometric bypass, store-protection bypass)
- [ ] Soft-stop actions (account delete, paid actions, posts) had explicit user confirmation this turn
- [ ] Credentials redacted in `run.json`
- [ ] Run directory path echoed in the final response

## References

- [mobile-mcp on GitHub](https://github.com/mobile-next/mobile-mcp)
- [Apple — Accessibility on iOS](https://developer.apple.com/documentation/accessibility)
- [Android — UI Automator](https://developer.android.com/training/testing/other-components/ui-automator)
