# modelcontextprotocol/git

Official MCP Git server. Read, search, and manipulate local Git repositories.

## MCP Server

- **Package**: `@modelcontextprotocol/server-git`
- **Transport**: stdio
- **Command**: `npx @modelcontextprotocol/server-git`

## Authentication

None (local filesystem)

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `git_log` | View commit history |
| `git_diff` | View changes |
| `git_status` | Repository status |
| `git_show` | Show commit details |
| `git_branch` | Branch operations |

## Configuration Example

```toml
[[mcp.servers]]
name = "git"
type = "stdio"
command = "npx"
args = ["-y", "@modelcontextprotocol/server-git"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://github.com/modelcontextprotocol/servers/tree/main/src/git)
