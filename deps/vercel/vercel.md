# vercel/vercel

Vercel deployment and project management MCP server.

## MCP Server

- **Package**: `vercel-mcp`
- **Transport**: stdio
- **Command**: `npx -y vercel-mcp`

## Authentication

Vercel API token

| Variable | Required | Description |
|----------|----------|-------------|
| `VERCEL_TOKEN` | Yes | Vercel API token |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Deployment, project management tools |

## Configuration Example

```toml
[[mcp.servers]]
name = "vercel"
type = "stdio"
command = "npx"
args = ["-y", "vercel-mcp"]
timeout_seconds = 60
env = { VERCEL_TOKEN = "your-value" }
tools = []
```

**Notes:** Package availability unverified — may not exist on npm.

## Links

- [Homepage](https://www.npmjs.com/package/vercel-mcp)
