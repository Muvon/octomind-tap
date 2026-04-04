# sveltejs/svelte

Official Svelte/SvelteKit documentation and tooling MCP server.

## MCP Server

- **Package**: `@sveltejs/mcp`
- **Transport**: stdio
- **Command**: `npx -y @sveltejs/mcp`

## Authentication

API key (optional, for Voyage embeddings)

| Variable | Required | Description |
|----------|----------|-------------|
| `VOYAGE_API_KEY` | No | For embeddings support |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Svelte/SvelteKit documentation and tooling |

## Configuration Example

```toml
[[mcp.servers]]
name = "svelte"
type = "stdio"
command = "npx"
args = ["-y", "@sveltejs/mcp"]
timeout_seconds = 60
env = { VOYAGE_API_KEY = "your-value" }
tools = []
```

**Notes:** Official Svelte package.

## Links

- [Homepage](https://github.com/sveltejs/ai-tools)
