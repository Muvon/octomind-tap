---
name: device-computer-automation
title: "Desktop Device UI Automation"
description: "Operate the local computer's native UI — macOS, Linux, or Windows — via the desktop-automation MCP server. Covers OS accessibility / screen-recording permissions, pixel-anchor targeting (no semantic UI tree), region-capture discipline under the MCP response cap, window focus and multi-monitor handling, keyboard / mouse / clipboard sequencing, and the safety boundary around destructive desktop actions and screen-lock / biometric bypass. Activate when the user wants to drive a native desktop app or the OS shell at the GUI layer. Pairs with the device:operator agent which carries the shared snapshot → verify → record discipline; this skill carries the desktop-specific tooling and rules and pulls the device-computer capability automatically."
license: Apache-2.0
compatibility: "Requires the device:operator agent. The host OS must grant Accessibility and Screen Recording permissions (macOS), or the equivalent input-monitoring permission (Linux / Windows), to the process running the MCP server."
domains: device
capabilities: device-computer
rules:
  - session(device) content(desktop)
  - session(device) content(macos)
  - session(device) content(windows)
  - session(device) content(cursor)
  - session(device) content(keystrokes)
  - match(\b(on|in)\s+my\s+(mac|macbook|laptop|computer|pc|desktop)\b)
  - match(\b(move|click|drag)\s+(the\s+)?(mouse|cursor|pointer)\b)
  - match(\b(type|press)\s+(into|on)\s+(the\s+)?(active|focused)\s+window\b)
  - match(\bautomate\s+(a\s+)?(native|desktop)\s+(app|application)\b)
  - match(\bscreenshot\s+(my|the)\s+(screen|desktop)\s+and\s+(click|interact)\b)
  - match(\b(robotjs|nut\.js)\b)
metadata:
  tags: "desktop macos linux windows mouse keyboard screenshot native robotjs"
---

## Overview

This skill turns the `device:operator` agent into a desktop-UI driver. It activates when the user talks about controlling their local computer (macOS, Linux, Windows) at the GUI layer and brings in the `device-computer` capability — the `desktop-automation` MCP server, RobotJS-backed — so the agent has tools to move and click the mouse, type keys, and capture the screen.

The agent already carries the universal discipline (snapshot → locate → act → verify → record, `run.json` schema, checkpoint policy, secret redaction, output directory layout). This skill carries only what is desktop-specific: which tools exist on `desktop-automation`, how to target without a semantic UI tree, how to live within the response-size cap, how to handle OS permissions and multi-monitor setups, and which desktop-specific safety boundaries cannot be crossed.

## Mental model

A desktop is the opposite of a mobile device in two important ways. First, there is no semantic UI tree — RobotJS sees pixels and reports cursor positions; it does not enumerate buttons by accessibility id. Second, "the screen" is huge, often multi-monitor, and shared with whatever else the user has running. You target visually, you capture small regions, and you confirm window focus before every keystroke.

Three immovable invariants on the desktop:

1. The desktop is the last resort. If the same outcome can be reached by a terminal command (`developer:*`, shell capability) or a browser action (`browser:general`), propose that and stop. The GUI layer is slow, fragile, and hard to verify; reserve it for native apps that genuinely have no automation API.
2. Window focus is part of state. You do not type until you have just-now confirmed the target window is foregrounded. A keystroke into the wrong window can submit a chat message, delete a tab, or trigger a destructive shortcut.
3. The MCP response has a ~1 MB cap. Full-screen screenshots on modern displays will exceed it and silently return nothing useful. Always prefer region captures sized to the target.

## Tooling — what desktop-automation gives you

The `desktop-automation` MCP server exposes a small surface. There is no semantic UI tree; every action is coordinate-based.

| Family | Tools | Notes |
|---|---|---|
| Screen | `get_screen_size`, `screen_capture` | Capture full screen or a region; full-screen often exceeds the 1 MB response cap on Retina / 4K displays |
| Mouse | `mouse_move`, `mouse_click` | Origin is top-left of the primary display |
| Keyboard | `keyboard_type`, `keyboard_press` | `keyboard_press` accepts named keys and modifier combos (Cmd+S, Ctrl+Shift+T, etc.) |

Always call `get_screen_size` once at run start and record it in `run.json.target.screen`. If the user resizes a window or changes display arrangement mid-run, re-screenshot before the next click — `get_screen_size` itself does not change, but the visual layout of the target window did.

## Targeting without a UI tree

You cannot ask the OS "where is the Save button". You can only screenshot, recognize it visually (or by known fixed offset), and click. Rules:

1. Prefer high-contrast, stable anchors:
   - Toolbar icons at known offsets from the title bar.
   - Menu items at fixed offsets from the menu-bar / window top.
   - Keyboard shortcuts when one exists for the action (a `Cmd+S` is a thousand times more reliable than locating a "Save" toolbar icon).
2. Avoid pixel-perfect targeting of small UI (< 16 px). Click the center of the visible region with a small margin (~2–3 px inset).
3. Do not carry coordinates between sessions. Today's "Save" button is not at yesterday's coordinates — DPI, theme, window position, and accent settings all shift pixels. Re-screenshot and re-locate every run.
4. After every click, capture a focused region around the expected next state and confirm it arrived. Do not chain clicks without a verifying capture.

When a keyboard shortcut exists for the action, use it instead of a mouse click. `Cmd+W` to close a tab, `Cmd+F` to open find, `Cmd+S` to save — these bypass the pixel-anchor problem entirely.

## Screen-capture discipline

The 1 MB MCP response cap is the dominant performance constraint on this skill. Strategies:

- Default to region captures sized to the smallest rectangle that contains the target. A 600×400 region around a dialog beats a 5120×2880 full-screen capture every time.
- For full-screen captures, ask the user to lower resolution or arrange windows so the target fits in a small region first. Do not silently return a corrupted / truncated capture.
- For verifying a state change, capture only the region where the change is expected — not the whole screen.

If a capture is unexpectedly empty / truncated, treat it as a tool failure. Do not click based on what you "expected" to see.

## Window focus and multi-monitor

Before any `keyboard_type` or shortcut press, you must have confirmed in the last action that the target window is foregrounded. On macOS / Windows, foreground is owned by the window manager — you can confirm by screenshotting the title bar (active windows have distinct chrome). When in doubt, ask the user to click into the target window first; do not "click to focus" yourself unless the user authorized it.

Multi-monitor setups:

- Coordinates are relative to the primary display's top-left. Secondary displays may have positive coordinates (to the right / below) or negative (to the left / above of the primary).
- Confirm which display the target window is on before clicking. Get the user to bring it to the primary display if you cannot reliably address coordinates on the secondary one.
- A click that lands on the wrong display silently activates whatever window happened to be under those coordinates. That is exactly the failure mode this skill exists to prevent.

## Host prerequisites and permissions

The skill's `device-computer` capability brings in `desktop-automation` automatically. The host needs OS permissions for the process running the MCP server (typically Terminal, iTerm, or the IDE that launched the agent).

macOS:
- `System Settings → Privacy & Security → Accessibility` — toggle on for the process.
- `System Settings → Privacy & Security → Screen Recording` — toggle on for the process.
- Some apps additionally require `Input Monitoring`.

Linux:
- X11: usually works without extra permissions for the user's display.
- Wayland: most RobotJS-style tools have limited or no support; if the user is on Wayland, propose alternatives (xdotool under XWayland, ydotool with proper setup) or escalate.

Windows:
- Run the process from a session that has UI access. Per-monitor DPI scaling needs to be considered — capture coordinates may need adjustment.

If a tool call fails with what looks like a permission error, stop and tell the user the exact toggle to flip. Do not retry blindly — the next attempt will fail the same way.

## Desktop-specific failure modes

The agent's `failures[]` reason enum extends with these on desktop:

| `reason` | What it means |
|---|---|
| `anchor_not_found` | Region capture didn't contain the expected anchor pixels after a fresh screenshot |
| `window_focus_lost` | A keystroke was about to land in a different window than intended; aborted |
| `capture_too_large` | Full-screen capture exceeded the response cap; retry with a smaller region |
| `permission_denied` | OS accessibility / screen-recording permission missing for the host process |
| `wayland_unsupported` | The host is on Wayland and the tool cannot drive it; escalate |
| `wrong_display` | The target window is on a non-primary display and coordinates cannot be reliably addressed |
| `unexpected_modal` | An OS / app dialog appeared that the user did not authorize |

Use these strings precisely. Generic reasons make the run unreviewable.

## Safety boundary

Hard "no" — never attempt, even on request:

- Bypass screen-lock, login window, or password / biometric prompts.
- Drag a file to the Trash / Recycle Bin without explicit user confirmation in this turn.
- Force-quit, restart, shut down, or log out the user's session.
- Modify system settings (firewall, FileVault, security & privacy, user accounts).
- Click through a "permanently delete" dialog.

Soft "stop and confirm" — these need explicit user confirmation in this turn:

- Closing windows / apps that may have unsaved changes.
- Saving a file over an existing path on disk.
- Clearing browser caches, signed-in sessions, or cookies via the app's UI.
- Initiating a paid action, purchase, or in-app subscription in a desktop app.
- Sending a message or posting publicly from the user's desktop client.

If a destructive shortcut is even possible in the focused window (`Cmd+Shift+Delete`, `Ctrl+W` with unsaved work, `Cmd+Q` on an editor), confirm with the user before pressing it.

## When to refuse and route

This skill exists to drive native desktop applications. Refuse and route when:

- The task is a web page → recommend `browser:general` (Playwright). The DOM is far more reliable than pixel-pushing on a browser window.
- The task is a shell command, file edit, build, or git operation → recommend `developer:*` or `devops:*`. Use the CLI.
- The task is a mobile app or simulator → the wrong device skill is active. The `device-mobile-automation` skill should be running instead.

## Checklist

- [ ] `get_screen_size` was called and host info recorded in `run.json.target`
- [ ] OS permissions verified (or a clean failure with instructions for the user)
- [ ] Region captures used by default; full-screen only when justified and within the size cap
- [ ] Window focus confirmed in the immediately-preceding capture before any keystroke
- [ ] Coordinates derived fresh from today's screenshots, never reused from a prior session
- [ ] Keyboard shortcuts preferred over pixel-anchor clicks when one exists
- [ ] Multi-monitor: target window confirmed to be on the primary display, or coordinates explicitly mapped to the right display
- [ ] Failure rows use desktop-specific reasons from the enum
- [ ] No hard-no actions attempted (screen-lock bypass, system-settings change, force-quit, permanent delete)
- [ ] Soft-stop actions had explicit user confirmation this turn
- [ ] Credentials redacted in `run.json`
- [ ] Run directory path echoed in the final response

## References

- [mcp-desktop-automation on GitHub](https://github.com/tanob/mcp-desktop-automation)
- [RobotJS](https://github.com/octalmage/robotjs)
