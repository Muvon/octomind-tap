# stability-ai/stable-diffusion

Stable Diffusion local image generation MCP server. Generate and upscale images using a local SD WebUI instance.

## MCP Server

- **Package**: `image-gen-mcp (GitHub — build locally)`
- **Transport**: stdio
- **Command**: `node /path/to/image-gen-mcp/build/index.js`

## Authentication

Optional HTTP Basic Auth

| Variable | Required | Description |
|----------|----------|-------------|
| `SD_WEBUI_URL` | Yes | Stable Diffusion WebUI URL |
| `SD_AUTH_USER` | No | WebUI username |
| `SD_AUTH_PASS` | No | WebUI password |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Generate from text |
| `get_sd_models` | List models |
| `set_sd_model` | Switch model |
| `get_sd_upscalers` | List upscalers |
| `upscale_images` | Upscale image |

## Configuration Example

```toml
[[mcp.servers]]
name = "stable-diffusion"
type = "stdio"
command = "npx"
args = ["-y", "image-gen-mcp (GitHub — build locally)"]
timeout_seconds = 60
env = { SD_WEBUI_URL = "your-value", SD_AUTH_USER = "your-value", SD_AUTH_PASS = "your-value" }
tools = []
```

**Notes:** Requires local Stable Diffusion WebUI running with --api flag.

## Links

- [Homepage](https://mcpservers.org/servers/Ichigo3766/image-gen-mcp)
