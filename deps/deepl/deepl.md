# deepl/deepl

Official DeepL translation MCP server. Text and document translation supporting 30+ languages.

## MCP Server

- **Package**: `deepl-mcp-server`
- **Transport**: stdio
- **Command**: `npx -y deepl-mcp-server`

## Authentication

API key

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPL_API_KEY` | Yes | API key from deepl.com |

## Available Tools

| Tool | Description |
|------|-------------|
| `translate_text` | Translate text between languages |
| `translate_document` | Translate documents (PDF, DOCX, PPTX) |

## Configuration Example

```toml
[[mcp.servers]]
name = "deepl"
type = "stdio"
command = "npx"
args = ["-y", "deepl-mcp-server"]
timeout_seconds = 60
env = { DEEPL_API_KEY = "your-value" }
tools = []
```

**Notes:** Official DeepL package (published by deepl-com).

## Links

- [Homepage](https://github.com/DeepLcom/deepl-mcp-server)
