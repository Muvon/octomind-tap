# supabase/supabase

Supabase MCP server. Manage projects, databases, migrations, Edge Functions, storage, and access documentation.

## MCP Server

- **Package**: `Remote: https://mcp.supabase.com/mcp`
- **Transport**: stdio
- **Command**: `Remote HTTP endpoint (or local: http://localhost:54321/mcp)`

## Authentication

OAuth 2.1 (automatic prompt during setup)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `manage_projects` | Project operations |
| `manage_tables` | Table operations |
| `run_migrations` | Database migrations |
| `run_sql` | Execute SQL |
| `manage_edge_functions` | Edge Functions |
| `search_docs` | Documentation search |

## Configuration Example

```toml
[[mcp.servers]]
name = "supabase"
type = "stdio"
command = "npx"
args = ["-y", "Remote: https://mcp.supabase.com/mcp"]
timeout_seconds = 60
tools = []
```

**Notes:** 40+ tools. Remote endpoint recommended. Supports ?read_only=true and ?features= query params.

## Links

- [Homepage](https://www.npmjs.com/package/@supabase/mcp-server-supabase)
