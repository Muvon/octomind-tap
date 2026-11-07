# muvon/mcp-variety

Local MCP server that picks an approach and form (opening, length, ending) for each piece of a repeated job, never repeating a recent combination for the same scope, and checks drafts for common AI-writing tells and openings reused from recent pieces. No LLM, no network.

## MCP Server

- **Package**: `mcp-variety` (GitHub commit pin until the PyPI release)
- **Transport**: stdio
- **Command**: `uvx --from git+https://github.com/muvon/mcp-variety@fefd684340927eaddf6db0b2707f4208a6094cae mcp-variety`

## Authentication

None.

| Variable | Required | Description |
|----------|----------|-------------|
| `VARIETY_MCP_STATE_DIR` | No | Directory where recent picks are stored |
| `VARIETY_MCP_WINDOW` | No | How many recent picks to avoid repeating |

## Available Tools

| Tool | Description |
|------|-------------|
| `variety_pick` | Pick an approach and form for one piece (`kind`, `scope`, optional `avoid`) |
| `variety_kinds` | List the supported kinds: post, reply, article, email, script, update |
| `variety_check` | Check a draft for AI-writing tells and, with `scope`, an opening reused from recent pieces (`text`, optional `scope`) |

## Configuration Example

```toml
[[mcp.servers]]
name = "variety"
type = "stdio"
command = "uvx"
args = ["--from", "git+https://github.com/muvon/mcp-variety@fefd684340927eaddf6db0b2707f4208a6094cae", "mcp-variety"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/muvon/mcp-variety)
