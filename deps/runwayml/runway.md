# runwayml/runway

RunwayML Gen-4 video and image generation MCP server. Generate, edit, and upscale videos from text and images.

## MCP Server

- **Package**: `runway-api-mcp-server (GitHub only — build locally)`
- **Transport**: stdio
- **Command**: `git clone + npm install + npm run build`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `RUNWAYML_API_SECRET` | Yes | Runway API key |

## Available Tools

| Tool | Description |
|------|-------------|
| `runway_generateVideo` | Create video from image+text |
| `runway_generateImage` | Generate image |
| `runway_upscaleVideo` | Upscale resolution |
| `runway_editVideo` | Edit video |
| `runway_getTask` | Task status |
| `runway_getOrg` | Org info |

## Configuration Example

```toml
[[mcp.servers]]
name = "runway"
type = "stdio"
command = "npx"
args = ["-y", "runway-api-mcp-server (GitHub only — build locally)"]
timeout_seconds = 60
env = { RUNWAYML_API_SECRET = "your-value" }
tools = []
```

**Notes:** Not on npm — build from source. Generated media expires after 24 hours. Requires paid Runway Developer account.

## Links

- [Homepage](https://github.com/runwayml/runway-api-mcp-server)
