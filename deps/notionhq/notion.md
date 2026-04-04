# notionhq/notion

Official Notion MCP server. Query data sources, manage pages, edit content in Markdown, search, and manage comments.

## MCP Server

- **Package**: `@notionhq/notion-mcp-server`
- **Transport**: stdio
- **Command**: `npx @notionhq/notion-mcp-server`

## Authentication

Notion integration token (Bearer)

| Variable | Required | Description |
|----------|----------|-------------|
| `NOTION_TOKEN` | Yes | Integration token (ntn_****) |

## Available Tools

| Tool | Description |
|------|-------------|
| `query` | Query data sources |
| `retrieve_page` | Get page |
| `create_page` | Create page |
| `update_page` | Update page |
| `search` | Search by title/ID |
| `create_comment` | Add comment |
| `list_templates` | List templates |

## Configuration Example

```toml
[[mcp.servers]]
name = "notion"
type = "stdio"
command = "npx"
args = ["-y", "@notionhq/notion-mcp-server"]
timeout_seconds = 60
env = { NOTION_TOKEN = "your-value" }
tools = []
```

**Notes:** Official Notion package. 22 tools. HTTP transport: --transport http. May sunset in favor of remote Notion MCP.

## Links

- [Homepage](https://www.npmjs.com/package/@notionhq/notion-mcp-server)
