# tailwindlabs/tailwindcss

TailwindCSS MCP server. Search docs, get utilities/colors, convert CSS to Tailwind, and generate component templates.

## MCP Server

- **Package**: `tailwindcss-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y tailwindcss-mcp-server`

## Authentication

None required

| Variable | Required | Description |
|----------|----------|-------------|
| — | — | No environment variables required |

## Available Tools

| Tool | Description |
|------|-------------|
| `get_tailwind_utilities` | Utility classes |
| `get_tailwind_colors` | Color palette |
| `search_tailwind_docs` | Search docs |
| `convert_css_to_tailwind` | CSS to Tailwind |
| `generate_component_template` | Component template |
| `generate_color_palette` | Generate palette |
| `install_tailwind` | Installation guide |

## Configuration Example

```toml
[[mcp.servers]]
name = "tailwindcss"
type = "stdio"
command = "npx"
args = ["-y", "tailwindcss-mcp-server"]
timeout_seconds = 60
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/tailwindcss-mcp-server)
