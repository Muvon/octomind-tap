# shinpr/mcp-image

Image generation MCP server with one tool, `generate_image`, backed by OpenAI GPT Image 2.5 (Flare for `fast`/`balanced`, Sunburst for `quality`), Google Nano Banana 2.1 (Nano Banana Pro for `quality`), or ByteDance Seedream. It writes every image to disk and returns the file path, so agents without a shell can still place the file in their deliverable. Reference images (`inputImagePaths`, up to 16 for OpenAI and 14 for Gemini) drive edits, product shots, and consistent characters.

## MCP Server

- **Package**: `mcp-image` (pinned in the capability files)
- **Transport**: stdio
- **Command**: `npx -y mcp-image@0.18.2`
- **Runtime**: Node.js 22+

## Authentication

API key for the selected provider.

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | For `IMAGE_PROVIDER=openai` | OpenAI API key; the GPT Image 2.5 models may require a verified organization |
| `GEMINI_API_KEY` | For `IMAGE_PROVIDER=gemini` | Google AI Studio (Gemini API) key |
| `ARK_API_KEY` | For `IMAGE_PROVIDER=seedream` | BytePlus ModelArk key |
| `IMAGE_PROVIDER` | No | `openai`, `gemini`, or `seedream` (the tap sets it per capability provider) |
| `IMAGE_OUTPUT_DIR` | No | Where images are saved (the tap uses `./image-out` in the project) |
| `IMAGE_QUALITY` | No | Default preset: `fast`, `balanced`, or `quality` |
| `SKIP_PROMPT_ENHANCEMENT` | No | `true` sends the prompt as written instead of rewriting it with a text model |

## Available Tools

| Tool | Description |
|------|-------------|
| `generate_image` | Generate from a prompt, or edit/combine reference images (`inputImagePaths`, absolute paths under the project, the output dir, or /tmp). Options: `aspectRatio` (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9), `imageSize` (1K/2K/4K), `quality` (fast/balanced/quality), `fileName` (.png/.jpg), `maintainCharacterConsistency`, `blendImages`, `useWorldKnowledge` |

## Configuration Example

```toml
[[mcp.servers]]
name = "image-gen"
type = "stdio"
command = "sh"
args = ["-c", "mkdir -p \"$PWD/image-out\"; IMAGE_OUTPUT_DIR=\"$PWD/image-out\" IMAGE_PROVIDER=openai IMAGE_QUALITY=balanced SKIP_PROMPT_ENHANCEMENT=true exec npx -y mcp-image@0.18.2"]
timeout_seconds = 300
env = { OPENAI_API_KEY = "{{ENV:OPENAI_API_KEY}}" }
tools = []
```

## Links

- [Repository](https://github.com/shinpr/mcp-image)
- [OpenAI image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
- [Gemini image generation](https://ai.google.dev/gemini-api/docs/image-generation)
