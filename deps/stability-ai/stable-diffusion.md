# stability-ai/stable-diffusion

MCP server for the hosted Stability AI API (Stable Diffusion 3.5 and Stable Image models): text-to-image, background removal, outpainting, search-and-replace and recolor edits, sketch/style/structure control, and fast or creative upscaling. Images are saved to a local directory (the tap uses `./image-out` in the project) and listed as MCP resources. It calls Stability's cloud API; no local GPU or WebUI is involved.

## MCP Server

- **Package**: `mcp-server-stability-ai` (community, pinned in the capability file)
- **Transport**: stdio
- **Command**: `npx -y mcp-server-stability-ai@0.2.0`

## Authentication

API key from platform.stability.ai.

| Variable | Required | Description |
|----------|----------|-------------|
| `STABILITY_AI_API_KEY` | Yes | Stability AI API key |
| `IMAGE_STORAGE_DIRECTORY` | No | Where images are saved (the tap sets `./image-out`) |
| `GCS_PROJECT_ID`, `GCS_CLIENT_EMAIL`, `GCS_PRIVATE_KEY`, `GCS_BUCKET_NAME` | No | Store images in Google Cloud Storage instead (remote setups) |

## Available Tools

| Tool | Description |
|------|-------------|
| `stability-ai-generate-image` | Text-to-image with Stable Image Core/Ultra |
| `stability-ai-generate-image-sd35` | Text-to-image with Stable Diffusion 3.5 models |
| `stability-ai-remove-background` | Cut out the subject |
| `stability-ai-outpaint` | Extend an image in any direction |
| `stability-ai-search-and-replace`, `stability-ai-search-and-recolor` | Prompt-targeted edits |
| `stability-ai-replace-background-and-relight` | New background with matched lighting |
| `stability-ai-control-sketch`, `stability-ai-control-style`, `stability-ai-control-structure` | Guided generation from a sketch, style, or structure reference |
| `stability-ai-upscale-fast`, `stability-ai-upscale-creative` | Upscaling |
| `stability-ai-0-list-resources` | List saved images |

## Configuration Example

```toml
[[mcp.servers]]
name = "stable-diffusion"
type = "stdio"
command = "sh"
args = ["-c", "mkdir -p \"$PWD/image-out\"; IMAGE_STORAGE_DIRECTORY=\"$PWD/image-out\" exec npx -y mcp-server-stability-ai@0.2.0"]
timeout_seconds = 120
env = { STABILITY_AI_API_KEY = "{{ENV:STABILITY_AI_API_KEY}}" }
tools = []
```

**Notes:** The package has had no release since March 2025; the default image provider (GPT Image 2.5) and the Nano Banana provider cover current models.

## Links

- [Repository](https://github.com/tadasant/mcp-server-stability-ai)
- [Stability AI API](https://platform.stability.ai/docs/api-reference)
