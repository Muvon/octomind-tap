# salesforce/salesforce

Salesforce CRM MCP server. Query objects, manage records, run Apex code, and handle triggers and debug logs.

## MCP Server

- **Package**: `@tsmztech/mcp-server-salesforce`
- **Transport**: stdio
- **Command**: `npx -y @tsmztech/mcp-server-salesforce`

## Authentication

Three options: Salesforce CLI, Username/Password, or OAuth 2.0

| Variable | Required | Description |
|----------|----------|-------------|
| `SALESFORCE_CONNECTION_TYPE` | Yes | Salesforce_CLI, User_Password, or OAuth_2.0_Client_Credentials |
| `SALESFORCE_USERNAME` | No | Username (for User_Password) |
| `SALESFORCE_PASSWORD` | No | Password (for User_Password) |
| `SALESFORCE_TOKEN` | No | Security token |
| `SALESFORCE_INSTANCE_URL` | No | Instance URL |
| `SALESFORCE_CLIENT_ID` | No | OAuth client ID |
| `SALESFORCE_CLIENT_SECRET` | No | OAuth client secret |

## Available Tools

| Tool | Description |
|------|-------------|
| `search_objects` | Search Salesforce objects |
| `describe_object` | Object schema |
| `query_records` | SOQL queries |
| `create_record` | Create record |
| `update_record` | Update record |
| `execute_apex` | Run Apex code |
| `manage_triggers` | Trigger management |
| `get_debug_logs` | Debug logs |

## Configuration Example

```toml
[[mcp.servers]]
name = "salesforce"
type = "stdio"
command = "npx"
args = ["-y", "@tsmztech/mcp-server-salesforce"]
timeout_seconds = 60
env = { SALESFORCE_CONNECTION_TYPE = "your-value", SALESFORCE_USERNAME = "your-value", SALESFORCE_PASSWORD = "your-value", SALESFORCE_TOKEN = "your-value", SALESFORCE_INSTANCE_URL = "your-value", SALESFORCE_CLIENT_ID = "your-value", SALESFORCE_CLIENT_SECRET = "your-value" }
tools = []
```

**Notes:** 16 tools. Supports all three Salesforce auth methods.

## Links

- [Homepage](https://www.npmjs.com/package/@tsmztech/mcp-server-salesforce)
