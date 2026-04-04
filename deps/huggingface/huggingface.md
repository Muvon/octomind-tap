# huggingface/huggingface

Hugging Face Hub MCP server. Access ML models, datasets, Spaces, and Gradio apps.

## MCP Server

- **Package**: `@llmindset/hf-mcp-server`
- **Transport**: stdio
- **Command**: `npx @llmindset/hf-mcp-server`

## Authentication

Hugging Face Token

| Variable | Required | Description |
|----------|----------|-------------|
| `DEFAULT_HF_TOKEN` | No | Fallback HF token (dev/test only) |

## Available Tools

| Tool | Description |
|------|-------------|
| `*Auto-discovered*` | Model access, dataset operations, Space deployment, Hub collaboration |

## Configuration Example

```toml
[[mcp.servers]]
name = "huggingface"
type = "stdio"
command = "npx"
args = ["-y", "@llmindset/hf-mcp-server"]
timeout_seconds = 60
env = { DEFAULT_HF_TOKEN = "your-value" }
tools = []
```

**Notes:** Also available as remote: https://huggingface.co/mcp?login. Dashboard on port 3000.

## Links

- [Homepage](https://github.com/huggingface/hf-mcp-server)
