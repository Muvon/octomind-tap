# mobile-next/mobile-mcp

Mobile MCP server for scalable mobile automation across iOS and Android. Drives real devices and simulators/emulators via accessibility snapshots and coordinate-based interaction — install/launch apps, take screenshots, tap/swipe/type, press device buttons, manage orientation.

## MCP Server

- **Package**: `@mobilenext/mobile-mcp`
- **Transport**: stdio (default) — optional SSE via `--listen <port>`
- **Command**: `npx -y @mobilenext/mobile-mcp@latest`

## Authentication

None for stdio. For SSE server mode, optional Bearer token.

| Variable | Required | Description |
|----------|----------|-------------|
| `MOBILEMCP_DISABLE_TELEMETRY` | No | Set to `1` to disable anonymous usage telemetry |
| `MOBILEMCP_AUTH` | No | Bearer token for SSE server mode (only when `--listen` is set) |

## Available Tools

| Tool family | Capabilities |
|-------------|--------------|
| Device management | List connected devices, get/set screen size, get/set orientation |
| App management | List installed apps, launch / terminate / install / uninstall apps |
| Screen interaction | Take screenshot, list UI elements, click / double-tap / long-press at coordinates, swipe |
| Input & navigation | Type text, press device buttons (home, back, volume, power), open URLs |

## Configuration Example

```toml
[[mcp.servers]]
name = "mobile-mcp"
type = "stdio"
command = "npx"
args = ["-y", "@mobilenext/mobile-mcp@latest"]
timeout_seconds = 120
env = { MOBILEMCP_DISABLE_TELEMETRY = "1" }
tools = []
```

## Requirements

- **Node.js v22+**
- **For iOS**: Xcode + Xcode command-line tools (`xcode-select --install`). For real devices: a paired device with developer mode enabled. For simulators: a recent iOS Simulator runtime.
- **For Android**: Android platform-tools (`adb` on `$PATH`). For real devices: USB debugging enabled. For emulators: a running AVD.

## Links

- [GitHub](https://github.com/mobile-next/mobile-mcp)
- [npm](https://www.npmjs.com/package/@mobilenext/mobile-mcp)
