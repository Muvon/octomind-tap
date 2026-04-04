# figma/figma

Figma design system MCP server. Read Figma files, access components, variables, and design tokens for design-to-code workflows.

## MCP Server

- **Package**: `figma-developer-mcp`
- **Transport**: stdio
- **Command**: `npx -y figma-developer-mcp`

## Authentication

Figma Personal Access Token

| Variable | Required | Description |
|----------|----------|-------------|
| `FIGMA_API_TOKEN` | Yes | Personal access token from Figma |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_file` | Read Figma file |
| `get_components` | List components |
| `get_variables` | Get design variables |
| `get_styles` | Get design styles |

## Configuration Example

```toml
[[mcp.servers]]
name = "figma"
type = "stdio"
command = "npx"
args = ["-y", "figma-developer-mcp"]
timeout_seconds = 60
env = { FIGMA_API_TOKEN = "your-value" }
tools = []
```

**Notes:** Rate limited by Figma API.

## Links

- [Homepage](https://www.npmjs.com/package/figma-developer-mcp)
