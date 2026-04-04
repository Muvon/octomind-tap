# auth0/auth0

Auth0 Management API MCP server. Manage applications, APIs, actions, logs, and authentication forms.

## MCP Server

- **Package**: `@auth0/auth0-mcp-server`
- **Transport**: stdio
- **Command**: `npx @auth0/auth0-mcp-server run`

## Authentication

OAuth 2.0 device authorization flow (credentials stored in system keychain)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `create_application` | Create Auth0 app |
| `list_applications` | List apps |
| `manage_apis` | Manage APIs |
| `deploy_actions` | Deploy actions |
| `query_logs` | Query auth logs |
| `customize_forms` | Customize login forms |

## Configuration Example

```toml
[[mcp.servers]]
name = "auth0"
type = "stdio"
command = "npx"
args = ["-y", "@auth0/auth0-mcp-server"]
timeout_seconds = 60
tools = []
```

**Notes:** BETA. Init with: npx @auth0/auth0-mcp-server init. Supports --read-only mode. Auto-redacts secrets.

## Links

- [Homepage](https://www.npmjs.com/package/@auth0/auth0-mcp-server)
