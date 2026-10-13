---
name: device-computer-automation
title: "Desktop Device UI Automation"
description: "Operate the local computer's native UI (macOS, Linux, or Windows) via the desktop-automation MCP server. Covers OS accessibility and screen-recording permissions, pixel-anchor targeting (no semantic UI tree), full-screen capture limits under the MCP response cap, HiDPI coordinate mapping, window focus and multi-monitor handling, keyboard and mouse sequencing, and the safety boundary around destructive desktop actions and screen-lock or biometric bypass. Activate when the user wants to drive a native desktop app or the OS shell at the GUI layer. Pairs with the device:operator agent, which carries the shared snapshot, verify, and record discipline; this skill carries the desktop-specific tooling and rules and pulls the device-computer capability automatically."
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

1. The desktop is the last resort. If the same outcome can be reached by a terminal command or a DOM-driven browser-automation action, propose that and stop. Native apps often have a scriptable path too: on macOS, AppleScript/JXA via `osascript` (scriptable apps, or System Events UI scripting through the Accessibility API) and `shortcuts run`; on Windows, PowerShell and UI Automation; on Linux, D-Bus, AT-SPI, or `xdotool` under X11. The GUI layer is slow, fragile, and hard to verify; reserve it for apps that genuinely have no automation API.
2. Window focus is part of state. You do not type until you have just-now confirmed the target window is foregrounded. A keystroke into the wrong window can submit a chat message, delete a tab, or trigger a destructive shortcut.
3. The screenshot is the only state you get, and it is expensive. `screen_capture` returns the whole primary display; the server's MCP response cap is about 1 MB, and its author reports only ~800×600 as reliably under it. On Retina / 4K displays a capture can fail outright — treat that as a tool failure, never click from memory.

## Tooling — what desktop-automation gives you

The `desktop-automation` server (pinned 0.1.6) exposes six tools. There is no semantic UI tree and no region capture; every action is coordinate-based.

| Tool | Arguments | Notes |
|---|---|---|
| `get_screen_size` | none | Logical screen size in points — the coordinate space `mouse_move` uses |
| `screen_capture` | none | Full primary display, returned inline and kept as a `screenshot://<id>` resource; it cannot write a file |
| `mouse_move` | `x`, `y` | Origin top-left of the primary display |
| `mouse_click` | `button` (left/right/middle), `double` | Clicks wherever the pointer is — always `mouse_move` first |
| `keyboard_type` | `text` | Types at the current focus |
| `keyboard_press` | `key`, `modifiers` (`command`, `control`, `shift`, `alt`) | Lowercase key names (`enter`, `tab`, `escape`, `s`) |

Call `get_screen_size` once at run start and record it in `run.json.target.screen`. On HiDPI displays the screenshot is in physical pixels (2× on Retina) while `mouse_move` takes logical points: divide screenshot coordinates by the ratio of image width to `get_screen_size` width before moving. Checkpoint evidence is the capture id, since the tool cannot save PNGs.

## Targeting without a UI tree

You cannot ask the OS "where is the Save button". You can only screenshot, recognize it visually (or by known fixed offset), and click. Rules:

1. Prefer high-contrast, stable anchors:
   - Toolbar icons at known offsets from the title bar.
   - Menu items at fixed offsets from the menu-bar / window top.
   - Keyboard shortcuts when one exists for the action (a `Cmd+S` is a thousand times more reliable than locating a "Save" toolbar icon).
2. Avoid pixel-perfect targeting of small UI (< 16 px). Click the center of the visible region with a small margin (~2–3 px inset).
3. Do not carry coordinates between sessions. Today's "Save" button is not at yesterday's coordinates — DPI, theme, window position, and accent settings all shift pixels. Re-screenshot and re-locate every run.
4. After every click, capture the screen and confirm the expected next state arrived. Do not chain clicks without a verifying capture.

When a keyboard shortcut exists for the action, use it instead of a mouse click. `Cmd+W` to close a tab, `Cmd+F` to open find, `Cmd+S` to save — these bypass the pixel-anchor problem entirely.

## Screen-capture discipline

The response-size cap is the dominant constraint on this skill. Strategies:

- Before the run, ask the user to set a lower or scaled display resolution if captures fail — that is the only lever, because the tool cannot crop.
- Capture only when you need to locate or verify, not after every keystroke.
- If a capture is empty, errors, or is truncated, record `capture_too_large` or the error and stop. Do not click based on what you "expected" to see.

## Window focus and multi-monitor

Before any `keyboard_type` or shortcut press, you must have confirmed in the last action that the target window is foregrounded. On macOS / Windows, foreground is owned by the window manager — you can confirm by screenshotting the title bar (active windows have distinct chrome). When in doubt, ask the user to click into the target window first; do not "click to focus" yourself unless the user authorized it.

Multi-monitor setups:

- Coordinates are relative to the primary display's top-left. Secondary displays may have positive coordinates (to the right / below) or negative (to the left / above of the primary).
- `screen_capture` shows only the primary display, so you cannot verify anything on a secondary one. Ask the user to move the target window to the primary display before the run.
- A click that lands on the wrong display silently activates whatever window happened to be under those coordinates. That is exactly the failure mode this skill exists to prevent.

## Host prerequisites and permissions

The skill's `device-computer` capability brings in `desktop-automation` automatically. The host needs OS permissions for the process running the MCP server (typically Terminal, iTerm, or the IDE that launched the agent).

macOS:
- `System Settings → Privacy & Security → Accessibility` — toggle on for the process.
- `System Settings → Privacy & Security → Screen & System Audio Recording` — toggle on for the process. Since macOS Sequoia the system re-asks for this periodically ("Allow For One Month"); a capture that suddenly fails mid-project is usually that prompt waiting for the user.
- Some apps additionally require `Input Monitoring`.

Linux:
- X11: usually works without extra permissions for the user's display.
- Wayland: RobotJS injects input through X11, so it reaches only XWayland windows; native Wayland apps ignore it. Propose ydotool or the desktop's portal-based tools, or escalate.

Windows:
- Run the process in the interactive user session. A non-elevated process cannot send input to an elevated (administrator) window — User Interface Privilege Isolation silently drops it — so target windows must run at the same integrity level. Per-monitor DPI scaling shifts coordinates; map them as on HiDPI macOS.

If a tool call fails with what looks like a permission error, stop and tell the user the exact toggle to flip. Do not retry blindly — the next attempt will fail the same way.

## Desktop-specific failure modes

The agent's `failures[]` reason enum extends with these on desktop:

| `reason` | What it means |
|---|---|
| `anchor_not_found` | A fresh screen capture didn't contain the expected anchor |
| `window_focus_lost` | A keystroke was about to land in a different window than intended; aborted |
| `capture_too_large` | `screen_capture` failed or came back truncated at the current resolution; ask the user to lower it |
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

Refuse and route when:

- The task is a web page → DOM-driven browser automation is far more reliable than pixel-pushing a browser window.
- The task is a shell command, file edit, build, or git operation → CLI work.
- The task is a mobile app or simulator → the `device-mobile-automation` skill should be active instead.

## Checklist

- [ ] `get_screen_size` was called and host info recorded in `run.json.target`
- [ ] OS permissions verified (or a clean failure with instructions for the user)
- [ ] Screen captures succeeded at the current resolution, and screenshot pixels were mapped to logical points before every `mouse_move`
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
