# twilio/twilio

Twilio MCP server. Access all Twilio public APIs for SMS, voice, messaging, and communications.

## MCP Server

- **Package**: `@twilio-alpha/mcp`
- **Transport**: stdio
- **Command**: `npx -y @twilio-alpha/mcp ACCOUNT_SID/API_KEY:API_SECRET`

## Authentication

Twilio credentials passed as arg: ACCOUNT_SID/API_KEY:API_SECRET

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `*All Twilio APIs*` | SMS, voice, messaging, and all Twilio public APIs via OpenAPI |

## Configuration Example

```toml
[[mcp.servers]]
name = "twilio"
type = "stdio"
command = "npx"
args = ["-y", "@twilio-alpha/mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** Official Twilio Labs package. Exposes all Twilio Public APIs. Use --services or --tags to filter. Alternative: github.com/BrennerSpear/twilio-mcp (simpler, just send_text).

## Links

- [Homepage](https://www.npmjs.com/package/@twilio-alpha/mcp)
