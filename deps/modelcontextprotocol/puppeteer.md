# modelcontextprotocol/puppeteer

Official MCP Puppeteer server. Browser automation, screenshots, form filling, and JavaScript execution.

## MCP Server

- **Package**: `@modelcontextprotocol/server-puppeteer`
- **Transport**: stdio
- **Command**: `npx -y @modelcontextprotocol/server-puppeteer`

## Authentication

None

| Variable | Required | Description |
|----------|----------|-------------|
| `PUPPETEER_LAUNCH_OPTIONS` | No | JSON-encoded launch options |
| `ALLOW_DANGEROUS` | No | Allow security-reducing args |

## Available Tools

| Tool | Description |
|------|-------------|
| `puppeteer_navigate` | Navigate to URL |
| `puppeteer_screenshot` | Take screenshot |
| `puppeteer_click` | Click element |
| `puppeteer_fill` | Fill input |
| `puppeteer_select` | Select option |
| `puppeteer_evaluate` | Execute JavaScript |

## Configuration Example

```toml
[[mcp.servers]]
name = "puppeteer"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-puppeteer"]
timeout_seconds = 60
env = { PUPPETEER_LAUNCH_OPTIONS = "your-value", ALLOW_DANGEROUS = "your-value" }
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer)
