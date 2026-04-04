# airtable/airtable

Airtable database MCP server. Full CRUD operations, schema management, batch processing, comments, and webhooks.

## MCP Server

- **Package**: `@rashidazarang/airtable-mcp`
- **Transport**: stdio
- **Command**: `npx -y @rashidazarang/airtable-mcp`

## Authentication

Personal Access Token (PAT) with scopes: data.records:read/write, schema.bases:read/write

| Variable | Required | Description |
|----------|----------|-------------|
| `AIRTABLE_TOKEN` | Yes | Personal Access Token from airtable.com/create/tokens |
| `AIRTABLE_BASE_ID` | No | Default base ID |

## Available Tools

| Tool | Description |
|------|-------------|
| `create_record` | Create records |
| `read_records` | Read records |
| `update_record` | Update records |
| `delete_record` | Delete records |
| `list_tables` | List tables |
| `create_table` | Create tables |
| `whoami` | Identity verification |

## Configuration Example

```toml
[[mcp.servers]]
name = "airtable"
type = "stdio"
command = "npx"
args = ["-y", "@rashidazarang/airtable-mcp"]
timeout_seconds = 60
env = { AIRTABLE_TOKEN = "your-value", AIRTABLE_BASE_ID = "your-value" }
tools = []
```

**Notes:** 42 tools total including batch operations, governance controls, and 10 analytical prompts.

## Links

- [Homepage](https://www.npmjs.com/package/@rashidazarang/airtable-mcp)
