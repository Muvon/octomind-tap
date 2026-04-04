# trello/trello

Trello project management MCP server. Manage boards, lists, cards, members, labels, checklists, and comments.

## MCP Server

- **Package**: `@iflow-mcp/trello-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y @iflow-mcp/trello-mcp-server`

## Authentication

Trello API key + token

| Variable | Required | Description |
|----------|----------|-------------|
| `TRELLO_API_KEY` | Yes | Trello API key |
| `TRELLO_TOKEN` | Yes | Trello auth token |

## Available Tools

| Tool | Description |
|------|-------------|
| `list_boards` | List boards |
| `list_cards` | List cards |
| `create_card` | Create card |
| `update_card` | Update card |
| `manage_checklists` | Checklist operations |
| `manage_labels` | Label operations |
| `add_comment` | Add comment |

## Configuration Example

```toml
[[mcp.servers]]
name = "trello"
type = "stdio"
command = "npx"
args = ["-y", "@iflow-mcp/trello-mcp-server"]
timeout_seconds = 60
env = { TRELLO_API_KEY = "your-value", TRELLO_TOKEN = "your-value" }
tools = []
```

**Notes:** 60+ tools. Alternative: @delorenj/mcp-server-trello (294 stars, more popular).

## Links

- [Homepage](https://www.npmjs.com/package/@iflow-mcp/trello-mcp-server)
