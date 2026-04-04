# replicate/replicate

Replicate AI image generation MCP server. Generate images and SVGs using Flux Schnell and Recraft V3 models.

## MCP Server

- **Package**: `replicate-flux-mcp`
- **Transport**: stdio
- **Command**: `npx -y replicate-flux-mcp`

## Authentication

API token

| Variable | Required | Description |
|----------|----------|-------------|
| `REPLICATE_API_TOKEN` | Yes | API token from Replicate account |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Generate image from text |
| `generate_multiple_images` | Batch generate 1-10 images |
| `generate_image_variants` | 2-10 variations |
| `generate_svg` | Vector graphics via Recraft V3 |
| `prediction_list` | Recent predictions |
| `get_prediction` | Prediction details |

## Configuration Example

```toml
[[mcp.servers]]
name = "replicate"
type = "stdio"
command = "npx"
args = ["-y", "replicate-flux-mcp"]
timeout_seconds = 60
env = { REPLICATE_API_TOKEN = "your-value" }
tools = []
```

## Links

- [Homepage](https://www.npmjs.com/package/replicate-flux-mcp)
