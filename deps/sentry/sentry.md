# sentry/sentry

Sentry error tracking MCP server. Search events, issues, and use AI-powered diagnostics.

## MCP Server

- **Package**: `@sentry/mcp-server`
- **Transport**: stdio
- **Command**: `npx @sentry/mcp-server@latest --access-token=YOUR_TOKEN`

## Authentication

User Auth Token (scopes: org:read, project:read/write, team:read/write, event:write)

| Variable | Required | Description |
|----------|----------|-------------|
| `SENTRY_ACCESS_TOKEN` | Yes | Sentry auth token |
| `EMBEDDED_AGENT_PROVIDER` | No | openai or anthropic (for AI search) |
| `SENTRY_HOST` | No | Self-hosted Sentry URL |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_events` | Search error events |
| `search_issues` | Search issues |

## Configuration Example

```toml
[[mcp.servers]]
name = "sentry"
type = "stdio"
command = "npx"
args = ["-y", "@sentry/mcp-server"]
timeout_seconds = 60
env = { SENTRY_ACCESS_TOKEN = "your-value", EMBEDDED_AGENT_PROVIDER = "your-value", SENTRY_HOST = "your-value" }
tools = []
```

**Notes:** LLM provider (OpenAI/Anthropic) required for AI search features. Supports self-hosted Sentry.

## Links

- [Homepage](https://www.npmjs.com/package/@sentry/mcp-server)
