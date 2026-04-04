# microsoft/playwright

Playwright browser automation MCP server. Navigate, click, fill forms, take screenshots, and interact with web pages.

## MCP Server

- **Package**: `@playwright/mcp`
- **Transport**: stdio
- **Command**: `npx @playwright/mcp@latest`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `browser_navigate` | Navigate to URL |
| `browser_click` | Click element |
| `browser_fill` | Fill form field |
| `browser_screenshot` | Take screenshot |
| `browser_snapshot` | Accessibility snapshot |
| `browser_evaluate` | Run JavaScript |
| `browser_select_option` | Select dropdown |

## Configuration Example

```toml
[[mcp.servers]]
name = "playwright"
type = "stdio"
command = "npx"
args = ["-y", "@playwright/mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Uses accessibility trees — no vision models needed. 60+ CLI options. Supports Chrome, Firefox, WebKit.

## Links

- [Homepage](https://github.com/microsoft/playwright-mcp)
