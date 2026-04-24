# cloudflare/cloudflare

Official Cloudflare MCP server. Manage Workers, KV, R2, D1, and DNS.

## MCP Server

- **Package**: `@cloudflare/mcp-server-cloudflare`
- **Transport**: stdio
- **Command**: `npx -y @cloudflare/mcp-server-cloudflare`

## Authentication

API token

| Variable | Required | Description |
|----------|----------|-------------|
| `CLOUDFLARE_API_TOKEN` | Yes | API token from Cloudflare dashboard |

## Available Tools

| Tool | Description |
|------|-------------|
| `workers` | Deploy and manage Workers |
| `kv` | Key-value storage operations |
| `r2` | Object storage management |
| `d1` | SQL database operations |
| `dns` | DNS record management |

## Configuration Example

```toml
[[mcp.servers]]
name = "cloudflare"
type = "stdio"
command = "npx"
args = ["-y", "@cloudflare/mcp-server-cloudflare"]
timeout_seconds = 60
env = { CLOUDFLARE_API_TOKEN = "your-value" }
tools = []
```

**Notes:** Official Cloudflare package.

## Links

- [Homepage](https://github.com/cloudflare/mcp-server-cloudflare)
